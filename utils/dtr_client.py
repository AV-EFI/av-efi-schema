import copy
from dataclasses import dataclass
import getpass
import itertools
import logging
import pathlib
import urllib.parse as urlparse

import jsonasobj2
from linkml.generators.common.type_designators import get_type_designator_value
from linkml.generators.jsonschemagen import json_schema_types
from linkml.utils import generator
import linkml_runtime as linkmlr
from linkml_runtime.linkml_model import annotations, meta
import requests
from requests.exceptions import HTTPError, JSONDecodeError
from ruamel.yaml import YAML


log = logging.getLogger(__name__)


DTR_CONFIG = {
    'dtr_doip_endpoint': 'https://typeregistry.lab.pidconsortium.net/doip',
    'dtr_expected_use':
    'AVefi schema, see https://github.com/AV-EFI/av-efi-schema',
    'dtr_name_prefix': 'efi_',
    'dtr_writers': ['21.T11969/dc08291b058f16935275'],
}


EFI_SCHEMA_IDS = [
    'https://github.io/av-efi-schema/model',
    'https://github.io/av-efi-schema/vocab',
]
ENUM_BASE_URL = 'https://raw.githubusercontent.com/AV-EFI/av-efi-schema/main/project/jsonschema/epic/vocabularies/'


class NoPIDOnRecordError(Exception):
    pass


class DataTypeMismatchError(Exception):
    def __init__(self, our_content, their_content, their_endpoint):
        self.our_content = our_content
        self.their_content = their_content
        self.their_endpoint = their_endpoint
        super().__init__(
            f"Locally generated data type: {our_content} deviates"
            f" from {their_endpoint}: {their_content}")


@dataclass
class DataTypeGenerator(generator.Generator):
    """Generate output for the Data Type Registry

    Accept source_path to a schema in LinkML syntax and sync_mode as
    parameters at initialisation time. Depending on the latter,
    methods of this class will either just read from the Data Type
    Registry and warn on deviations from the local schema file, or
    they will update existing Data Types and register new ones as far
    as the right credentials can be provided (interactively).

    """
    valid_formats = ["dtr"]
    uses_schemaloader = False
    #file_extension = "schema.json"
    sync_mode: bool = False

    def __post_init__(self):
        super().__post_init__()
        self.doip = DTRClient(DTR_CONFIG['dtr_doip_endpoint'])
        self.verified_pids = {}

    def process_schema(self):
        for obj in itertools.chain(
                self.schemaview.all_enums().values(),
                self.schemaview.all_types().values(),
                self.schemaview.all_classes().values()):
            if 'TypeRegistrySubset' not in obj.in_subset:
                continue
            try:
                self.get_verified_pid(obj)
            except (NoPIDOnRecordError, DataTypeMismatchError) as e:
                log.warning(e)

    def get_verified_pid(self, obj: meta.Definition, *, cls=None, trunk=False):
        obj_type, src_locator = self.get_characteristics(
            obj, cls=cls, trunk=trunk)
        try:
            return get_by_path(self.verified_pids, src_locator)
        except KeyError:
            pass
        if 'TypeRegistrySubset' not in obj.in_subset and not trunk:
            set_by_path(self.verified_pids, src_locator, None)
            return None
        try:
            pid = obj.annotations.get(src_locator[-1]).value
        except AttributeError as e:
            if self.sync_mode:
                pid = None
            else:
                raise NoPIDOnRecordError(
                    f"No PID for {src_locator[:-2]} yet") from e
        if trunk:
            dtr_content = self.create_trunk_type(obj)
        elif obj_type == 'slot':
            dtr_content = self.convert_slot(obj, src_locator)
        else:
            dtr_content = getattr(self, f"convert_{obj_type}")(obj)
        dtr_content['ExpectedUse'] = DTR_CONFIG['dtr_expected_use']
        # dtr_content['Identifier'] = pid
        if pid:
            response = self.doip.get('0.DOIP/Op.Retrieve', pid)
            data_type = response.json()
            present_content = copy.deepcopy(data_type['attributes']['content'])
            for key in ('Identifier', 'provenance'):
                try:
                    del present_content[key]
                except KeyError:
                    pass
            if present_content != dtr_content:
                if self.sync_mode:
                    data_type = self.update_registry(
                        src_locator, dtr_content, old_data_type=data_type)
                else:
                    raise DataTypeMismatchError(
                        dtr_content, present_content, response.request.url)
        else:
            data_type = self.update_registry(src_locator, dtr_content)
            pid = data_type['id']
        set_by_path(self.verified_pids, src_locator, pid)
        return pid

    def get_characteristics(self, obj, cls=None, trunk=False):
        # drop 'Definition' suffix
        obj_type = type(obj).__name__[:-10].lower()
        src_locator = [
            obj.from_schema, self._meta_to_yaml_section_map[type(obj)],
            obj.name]
        if obj_type == 'slot':
            if cls is None:
                raise RuntimeError(
                    f"Missing cls parameter while processing slot {obj.name}")
            for a in self.schemaview.class_ancestors(cls.name, mixins=False):
                a_cls = self.schemaview.get_class(a)
                for loc in ('attributes', 'slot_usage'):
                    usage = a_cls[loc].get(obj.name)
                    if usage and (
                            usage['any_of'] or usage['exactly_one_of']):
                        src_locator = [
                            obj.from_schema,
                            self._meta_to_yaml_section_map[type(a_cls)],
                            a, loc, obj.name]
                        break
                else:
                    continue
                break
        if trunk:
            src_locator.extend(['annotations', 'trunk_pid'])
        else:
            src_locator.extend(['annotations', 'pid'])
        return obj_type, src_locator

    def convert_enum(self, enum: meta.EnumDefinition):
        result = {'name': f"{DTR_CONFIG['dtr_name_prefix']}{enum.name}"}
        if enum.description:
           result['description'] = enum.description
        result['Schema'] = {
            'Type': 'Enum',
            'Properties': [{
                'Property': '$ref',
                'Value': f"{ENUM_BASE_URL}{enum.name}.json",
            }],
        }
        return result

    def convert_type(self, schema_type: meta.TypeDefinition):
        schema_type = self.schemaview.induced_type(schema_type.name)
        result = {
            'name': f"{DTR_CONFIG['dtr_name_prefix']}{schema_type.name}",
        }
        if schema_type.description:
            result['description'] = schema_type.description
        dtr_schema = result.setdefault('Schema', {})
        typ, fmt = json_schema_types.get(
            schema_type.base.lower(), ("String", None))
        dtr_schema['Type'] = typ.capitalize()
        props = []
        if fmt:
            props.append({'Property': 'format', 'Value': fmt})
        for dtr_keyword, linkml_keyword in (
                ('pattern', 'pattern'),
                ('minimum', 'minimum_value'),
                ('maximum', 'maximum_value'),
                ('const',   'equals_string'),
                ('const',   'equals_number'),
        ):
            constraint = getattr(schema_type, linkml_keyword)
            if constraint:
                props.append({'Property': dtr_keyword, 'Value': constraint})
        dtr_annotations = schema_type.annotations.get('data_type_properties')
        if dtr_annotations:
            for p, v in jsonasobj2.as_dict(dtr_annotations)['value'].items():
                props.append({'Property': p, 'Value': v})
        if props:
            dtr_schema['Properties'] = props
        return result

    operator_map = {
        'all_of': 'allOf',
        'any_of': 'anyOf',
        'exactly_one_of': 'oneOf',
    }

    def convert_slot(self, slot: meta.SlotDefinition, src_locator):
        """Intended for slots with range expressions only."""
        bool_op = None
        for op in ('all_of', 'any_of', 'exactly_one_of'):
            if slot[op]:
                if bool_op:
                    raise NotImplementedError(
                        f"Cannot handle both {bool_op} and {op} on slot"
                        f" {slot.name}")
                bool_op = op
        assert bool_op, f"Should not have been called on slot {slot.name}"
        members = []
        for subschema in slot[bool_op]:
            obj = self.schemaview.get_element(subschema['range'])
            members.append((obj.name, self.get_verified_pid(obj)))
        if src_locator[1] == 'classes':
            type_name = f"{slot.name}__in_{src_locator[2]}"
        else:
            type_name = slot.name
        return self.create_bool_type(
            bool_op, type_name, slot.description, members)

    def convert_class(self, cls: meta.ClassDefinition):
        if cls.mixin:
            raise ValueError(
                f"{cls.name} is a mixin, hence should not be in"
                f" TypeRegistrySubset")
        children = self.get_nearest_non_abstract_descendants(cls)
        if children:
            description = \
                f"Wrapper InfoType validating instances of AVefi class" \
                f" {cls.name} and subclasses"
            if cls.abstract or 'TypeRegistrySubset' not in cls.in_subset:
                members = []
            else:
                members = [
                    (f"{cls.name}__Trunk",
                     self.get_verified_pid(cls, trunk=True)),
                ]
            for child in children:
                members.append(
                    (child.name, self.get_verified_pid(child)))
            return self.create_bool_type(
                'any_of', cls.name, description, members)
        else:
            result = self.create_trunk_type(cls)
            result['name'] = f"{DTR_CONFIG['dtr_name_prefix']}{cls.name}"
            return result

    def create_bool_type(self, bool_op, name, description, members):
        result = {
            'Schema': {
                'Type': 'Object',
                'addProps': True,
                'subCond': self.operator_map[bool_op]},
            'name': f"{DTR_CONFIG['dtr_name_prefix']}{name}",
            'description': description,
        }
        cls_properties = result['Schema'].setdefault('Properties', [])
        for member_name, pid in members:
            cls_properties.append({
                'Name': str(member_name),
                'Properties': {'Cardinality': '0 - 1'},
                'Type': pid,
            })
        return result

    def create_trunk_type(self, cls):
        result = {
            'Schema': {'Type': 'Object', 'addProps': False},
            'name': f"{DTR_CONFIG['dtr_name_prefix']}{cls.name}__Trunk",
        }
        if cls.description:
            result['description'] = cls.description
        cls_properties = []
        parents = self.schemaview.class_parents(cls.name, mixins=False)
        if parents:
            # Should be exactly one element since mixins have been ignored
            parent = self.schemaview.get_class(parents[0])
            cls_properties.append({
                'Name': f"{parent.name}__Trunk",
                'Properties': {
                    'Cardinality': '0 - 1',
                    'extractProperties': True,
                },
                'Type': self.get_verified_pid(parent, trunk=True),
            })
        slot_names = set(
            cls.slots + list(cls.slot_usage) + list(cls.attributes))
        designator = self.schemaview.get_type_designator_slot(cls.name)
        if designator:
            slot_names.add(designator.name)
        for slot_name in slot_names:
            slot = self.schemaview.induced_slot(slot_name, cls.name)
            if 'TypeRegistrySubset' not in slot.in_subset:
                continue
            prop = {'Name': self.aliased_slot_name(slot)}
            cls_properties.append(prop)
            slot_properties = prop.setdefault('Properties', {})
            slot_required = slot.required
            if slot.designates_type:
                slot_required = True
                type_value = get_type_designator_value(
                    self.schemaview, slot, cls)
                slot_properties['Const Value'] = type_value
            slot_properties['Cardinality'] = self.get_slot_cardinality(
                slot, slot_required)
            if any(len(slot[bool_op]) > 1
                   for bool_op in ('all_of', 'any_of', 'exactly_one_of')):
                pid = self.get_verified_pid(slot, cls=cls)
            else:
                range = self.schemaview.get_element(slot.range)
                if isinstance(range, meta.ClassDefinition):
                    if not self.schemaview.is_inlined(slot):
                        raise ValueError(f"{slot.name} must be inlined")
                    if slot.multivalued and not slot.inlined_as_list:
                        raise ValueError(
                            f"{slot.name} must be inlined as list")
                    if range.abstract \
                       and 'TypeRegistrySubset' not in range.in_subset:
                        range.in_subset.append('TypeRegistrySubset')
                pid = self.get_verified_pid(range)
                if pid is None:
                    raise ValueError(
                        f"No PID for {range.name} as range of {slot.name};"
                        f" perhaps {range.name} should be added to"
                        f" TypeRegistrySubset")
            prop['Type'] = pid
        if cls_properties:
            result['Schema']['Properties'] = cls_properties
        return result

    def get_nearest_non_abstract_descendants(self, cls):
        result = []
        for child_name in self.schemaview.get_children(cls.name, mixin=False):
            child = self.schemaview.get_class(child_name)
            if 'TypeRegistrySubset' in child.in_subset and not child.abstract:
                result.append(child)
            else:
                result.extend(self.get_nearest_non_abstract_descendants(child))
        return result

    def get_slot_cardinality(
            self, slot: meta.SlotDefinition, required: bool) -> str:
        if slot.multivalued:
            if required:
                return '1 - n'
            else:
                return '0 - n'
        else:
            if required:
                return '1'
            else:
                return '0 - 1'

    def update_registry(self, src_locator, new_content, old_data_type=None):
        new_content['ExpectedUse'] = DTR_CONFIG['dtr_expected_use']
        if src_locator[1] in ('enums', 'types'):
            dtr_type = 'BasicInfoType'
        else:
            dtr_type = 'InfoType'
        payload = {
            'type': dtr_type,
            'attributes': {
                'content': new_content,
            },
        }
        if DTR_CONFIG['dtr_writers']:
            payload['attributes']['acl'] = {
                'writers': DTR_CONFIG['dtr_writers'],
            }
        if old_data_type:
            provenance = old_data_type['attributes']['content'].get(
                'provenance')
            if provenance:
                new_content['provenance'] = provenance
            response = self.doip.post(
                '0.DOIP/Op.Update', old_data_type['id'], json=payload)
        else:
            response = self.doip.post(
                '0.DOIP/Op.Create', 'service', json=payload)
        data_type = response.json()
        pid = data_type['id']
        if not old_data_type or old_data_type.get('id') != pid:
            source_obj = self.get_source_definition(src_locator[:-2])
            if 'annotations' not in source_obj:
                src_obj_keys = list(source_obj.keys())
                for anchor in ('in_subset', 'description'):
                    try:
                        idx = src_obj_keys.index(anchor)
                        break
                    except ValueError:
                        pass
                else:
                    idx = 0
                source_obj.insert(idx, 'annotations', [])
            pid_slot = src_locator[-1]
            for el in source_obj['annotations']:
                if pid_slot in el:
                    el.update({pid_slot: pid})
                    break
            else:
                source_obj['annotations'].insert(0, {pid_slot: pid})
            self.save_source_definition(src_locator)
        return data_type

    @property
    def cache(self):
        try:
            return self._cache
        except AttributeError:
            self._cache = YAMLStore(self.schemaview)
            return self._cache

    _meta_to_yaml_section_map = {
        meta.EnumDefinition: 'enums',
        meta.TypeDefinition: 'types',
        meta.ClassDefinition: 'classes',
        meta.SlotDefinition: 'slots',
    }

    def get_source_definition(self, src_locator):
        return get_by_path(
            self.cache[src_locator[0]]['parsed_source'], src_locator[1:])

    def save_source_definition(self, src_locator):
        self.cache.save(src_locator[0])


def get_by_path(dct, keys):
    for key in keys:
        dct = dct[key]
    return dct


def set_by_path(dct, keys, value):
    for key in keys[:-1]:
        dct = dct.setdefault(key, {})
    dct[keys[-1]] = value


class YAMLStore(dict):
    def __init__(self, schemaview: linkmlr.utils.schemaview.SchemaView):
        self.yaml = YAML()
        self.load(pathlib.Path(schemaview.schema.source_file))

    def load(self, source_path: pathlib.Path):
        parsed_source = self.yaml.load(source_path)
        # prevent infinite recursion
        if parsed_source['id'] in self:
            return
        self[parsed_source['id']] = {
            'parsed_source': parsed_source,
            'source_path': source_path,
        }
        for entry in parsed_source.get('imports', []):
            if ':' not in entry:
                # definitely a local import, so go find the
                # corresponding file
                import_path = source_path.parent / pathlib.Path(
                    entry).with_suffix('.yaml')
                self.load(import_path)

    def save(self, source_id: str):
        self.yaml.dump(
            self[source_id]['parsed_source'],
            self[source_id]['source_path'])


class APIError(HTTPError):
    @classmethod
    def from_http_error(cls, e):
        try:
            msg = f"{e}: {e.response.json()}"
        except JSONDecodeError:
            msg = str(e)
        return cls(msg, response=e.response)


class DTRClient:
    """DOIP interface to the Data Type Registry.

    Provide get, post, and request methods as known from the requests
    package but instead of a url they expect DOIP operationId and
    targetId as positional parameters. Pass additional keyword
    arguments like json and headers to the requests.request method.
    Accept an endpoint parameter at initialisation time.

    """

    unrestricted_operations = [
        '0.DOIP/Op.Retrieve',
        '0.DOIP/Op.Search',
        '0.DOIP/Op.Hello',
        '20.DOIP/Op.Auth.Token',
    ]

    def __init__(self, endpoint, *args, **kwargs):
        self.endpoint = endpoint
        self.session = requests.Session(*args, **kwargs)

    def request(self, method, operation, target, *, headers=None, **kwargs):
        if not headers:
            headers = {}
        try:
            headers['Authorization'] = f"Bearer {self._token}"
        except AttributeError:
            # Do not authenticate unless required, so anybody can
            # check for current deviations between schema and data
            # type registry
            if operation not in self.unrestricted_operations:
                self.get_token()
                return self.request(
                    method, operation, target, headers=headers, **kwargs)
        r = self.session.request(
            method, self.endpoint, headers=headers,
            params={'operationId': operation, 'targetId': target}, **kwargs)
        if r.status_code == 401:
            if getattr(self, '_token', None):
                del self._token
            self.get_token()
            return self.request(
                method, operation, target, headers=headers, **kwargs)
        try:
            r.raise_for_status()
        except HTTPError as e:
            raise APIError.from_http_error(e) from e
        return r

    def get_token(self):
        r = self.post(
            '20.DOIP/Op.Auth.Token', 'service',
            json={
                'grant_type': 'password',
                'username': input('Username for data type registry: '),
                'password': getpass.getpass(),
            })
        self._token = r.json()['access_token']

    def get(self, operation, target, *args, **kwargs):
        return self.request('GET', operation, target, *args, **kwargs)

    def post(self, operation, target, *args, **kwargs):
        return self.request('POST', operation, target, *args, **kwargs)
