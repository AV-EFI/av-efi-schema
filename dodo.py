import copy
import json
import jsonref
from pathlib import Path
from urllib.request import urlopen
import yaml


DOIT_CONFIG = {
    'action_string_formatting': 'new',
    'default_tasks': [
        'pid_schema',
        'vocabularies',
        'python',
        'convert',
    ],
}
HERE = Path(__file__).parent
DOCS_DIR = HERE / 'docs'
UTILS_DIR = HERE / 'utils'
VOCAB_DIR = HERE / 'Controlled_Vocabularies'
WORKING_DIR = HERE / 'KIP_DTR'
YAML_SCHEMA = HERE / 'av_efi_schema.yaml'
JSON_SCHEMA = YAML_SCHEMA.with_suffix('.json')
PYTHON_BINDINGS = YAML_SCHEMA.with_suffix('.py')
PID_SCHEMAS = [
    HERE / 'av_efi_schema_workvariant.json',
    HERE / 'av_efi_schema_manifestation.json',
    HERE / 'av_efi_schema_item.json',
]


SCHEMA_PIDS = {
    'work': '21.T11148/31b848e871121c47d064',
    'manifestation': '21.T11148/ef6836b80e4d64e574e3',
    'item': '21.T11148/b0047df54c686b9df82a',
}
#TYPEAPI = 'http://typeapi.pidconsortium.net/dtype/schema/JSON/'
#REQUEST_PARAMS = '/?cached=true'
TYPEAPI = 'http://typeapi.lab.pidconsortium.net/v1/types/schema/'
REQUEST_PARAMS = '?refresh=true'


def task_vocabularies():
    """Generate JSON enum lists for typeapi from LinkML schema."""
    return {
        'actions': [generate_json_enum_files],
        'file_dep': [YAML_SCHEMA],
    }


def generate_json_enum_files(dependencies, targets):
    VOCAB_BASE_URL = 'https://raw.githubusercontent.com/' \
        'AV-EFI/av-efi-schema/main/Controlled_Vocabularies/'
    with open(dependencies[0], 'r') as f:
        schema = yaml.safe_load(f)
    for key, enum_dict in schema['enums'].items():
        output = {
            '$id': key,
            'enum': list(enum_dict['permissible_values'].keys()),
        }
        output_path = VOCAB_DIR / f"{key}.json"
        with output_path.open('w') as f:
            f.write(json.dumps(output, indent=2, sort_keys=True))


def expand_and_split_json_schema(dependencies, targets):
    """Generate separate schemas for work, manifestation and item."""
    schema_path = Path(dependencies[0])
    with schema_path.open('r') as f:
        schema = jsonref.load(f, proxies=False, jsonschema=True)
    for i in range(len(schema['properties']['has_record']['items']['anyOf'])):
        name = schema['properties']['has_record']['items']['anyOf'][i]['title']
        output = copy.deepcopy(schema)
        output['$id'] = f"{schema['$id']}-{name.lower()}"
        output['title'] = output['$id'].rpartition('/')[2]
        output['description'] = \
            f"Auto-generated from {schema['$id']} for {name} PIDs"
        output['properties']['has_record'] = \
            output['properties']['has_record']['items']['anyOf'][i]
        del output['$defs']
        output_path = schema_path.with_stem(
            f"{schema_path.stem}_{name.lower()}")
        with output_path.open('w') as f:
            jsonref.dump(output, f, indent=4)


def task_pid_schema():
    """Generate derived schemas for WorkVariant, Manifestation, Item."""
    return {
        'actions': [expand_and_split_json_schema],
        'file_dep': [JSON_SCHEMA],
        'task_dep': ['sync_dependencies'],
        'targets': PID_SCHEMAS,
    }


def task_jsonschema():
    """Generate derived JSON Schema."""
    return {
        'actions': [
            "gen-json-schema {dependencies} > {targets}",
        ],
        'file_dep': [YAML_SCHEMA],
        'task_dep': ['sync_dependencies'],
        'targets': [JSON_SCHEMA],
    }


def task_python():
    """Generate python bindings."""
    return {
        'actions': [
            "gen-python {dependencies} > {targets}",
        ],
        'file_dep': [YAML_SCHEMA],
        'task_dep': ['sync_dependencies'],
        'targets': [PYTHON_BINDINGS],
    }


def task_docs():
    """Build documentation from LinkML schema."""
    return {
        'actions': [
            "gen-doc -d {targets} {dependencies}",
        ],
        'file_dep': [YAML_SCHEMA],
        'task_dep': ['sync_dependencies'],
        'targets': [DOCS_DIR],
    }


def task_sync_dependencies():
    """Install dependencies according to pdm.lock (for developers)."""
    return {
        'actions': [
            'pdm sync',
        ],
        'file_dep': ['pdm.lock'],
    }


def task_update_linkml():
    """Update dependencies (linkml, etc.)."""
    return {
        'actions': [
            'pdm update -u',
        ],
        'uptodate': (True,),
    }


def task_fetch_efi_schemas():
    """Fetch EFI JSON Schemas from the Data Type Registry."""
    def fetch_efi_schema(task):
        efi_type = task.name.rpartition(':')[2]
        pid = SCHEMA_PIDS[efi_type]
        response = urlopen(f"{TYPEAPI}{pid}{REQUEST_PARAMS}")
        jsondata = json.loads(response.read())
        if 'error' in jsondata.get('status', '').lower():
            raise RuntimeError(
                f"Request to {response.url} yielded this response: {jsondata}")
        with open(task.targets[0], 'w+') as f:
            f.write(json.dumps(jsondata, indent=4, sort_keys=True))

    for efi_type in SCHEMA_PIDS.keys():
        yield {
            'name': efi_type,
            'actions': [
                fetch_efi_schema,
            ],
            'targets': [
                WORKING_DIR / f"schema_{efi_type}_DTR.json",
            ],
            'clean': True,
            'uptodate': (True,),
            'verbosity': 2}


def task_convert():
    """Convert EFI Schemas from JSON into reStructuredText."""
    invoke = {
        'json2csv': f"python {UTILS_DIR / 'efischema2csv.py'}",
        'csv2rst':  f"python {UTILS_DIR / 'third_party' / 'csv2rst.py'} -w 50",
    }
    for efi_type in SCHEMA_PIDS.keys():
        for src, dst in (('json', 'csv'), ('csv', 'rst')):
            yield {
                'name': f"{efi_type}_{src}2{dst}",
                'actions': [
                    ' '.join([
                        invoke[f"{src}2{dst}"],
                        '-i', '{dependencies}', '-o', '{targets}',
                    ]),
                ],
                'file_dep': [
                    WORKING_DIR / f"schema_{efi_type}_DTR.{src}",
                ],
                'targets': [
                    WORKING_DIR / f"schema_{efi_type}_DTR.{dst}",
                ],
                'verbosity': 2,
            }
