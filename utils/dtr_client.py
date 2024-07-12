import copy
from dataclasses import dataclass
import getpass
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

    def process_schema(self):
        data_type_stubs = []
        for enum in self.schemaview.all_enums():
            data_type_stubs.append((enum, self.convert_enum(enum)))
        for schema_type in self.schemaview.all_types().values():
            if schema_type.from_schema not in EFI_SCHEMA_IDS:
                continue
            induced_type = self.schemaview.induced_type(schema_type.name)
            data_type_stubs.append(
                (induced_type, self.convert_type(induced_type)))
        for obj, dtr_content in data_type_stubs.items():
            check_data_type(obj, dtr_content)

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

    def check_data_type(self, obj: meta.Definition, dtr_content):
        dtr_content['ExpectedUse'] = DTR_CONFIG['dtr_expected_use']
        pid = obj.annotations.get('pid')
        if pid:
            pid = pid.value
            # dtr_content['Identifier'] = pid
            response = self.doip.get(
                '0.DOIP/Op.Retrieve', pid)
            data_type = response.json()
            present_content = copy.deepcopy(data_type['attributes']['content'])
            del present_content['provenance']
            try:
                del present_content['Identifier']
            except KeyError:
                pass
            if present_content != dtr_content:
                if not self.sync_mode:
                    log.warning(
                        f"Deviation from DTR (local: {dtr_content},"
                        f" {response.request.url}: {present_content})")
                    return None
                else:
                    data_type = self.update_registry(
                        obj, dtr_content, old_data_type=data_type)
        else:
            if not self.sync_mode:
                log.warning(f"No PID for {obj.name} yet")
                return None
            data_type = self.update_registry(obj, dtr_content)
        return data_type

    def update_registry(self, obj, new_content, old_data_type=None):
        new_content['ExpectedUse'] = DTR_CONFIG['dtr_expected_use']
        if type(obj) in (meta.EnumDefinition, meta.TypeDefinition):
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
            obj.annotations['pid'] = annotations.Annotation(
                tag='pid', value=pid)
            source_obj = self.get_source_definition(obj)
            if 'annotations' not in source_obj:
                try:
                    idx = list(source_obj.keys()).index('description')
                except ValueError:
                    idx = 0
                source_obj.insert(idx, 'annotations', [])
            for el in source_obj['annotations']:
                if 'pid' in el:
                    el.update({'pid': pid})
                    break
            else:
                source_obj['annotations'].insert(0, {'pid': pid})
            self.save_source_definition(obj)
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
    }

    def get_source_definition(self, obj: meta.Definition):
        parsed_source = self.cache[obj.from_schema]['parsed_source']
        source_section = self._meta_to_yaml_section_map[type(obj)]
        return parsed_source[source_section][obj.name]

    def save_source_definition(self, obj: meta.Definition):
        self.cache.save(obj.from_schema)


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
