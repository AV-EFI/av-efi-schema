import json
from pathlib import Path
from urllib.request import urlopen


SCHEMA_PIDS = {
    'work': '21.T11148/31b848e871121c47d064',
    'manifestation': '21.T11148/ef6836b80e4d64e574e3',
    'item': '21.T11148/b0047df54c686b9df82a',
}
#TYPEAPI = 'http://typeapi.pidconsortium.net/dtype/schema/JSON/'
#REQUEST_PARAMS = '/?cached=true'
TYPEAPI = 'http://typeapi.lab.pidconsortium.net/v1/types/schema/'
REQUEST_PARAMS = '?refresh=true'
HERE = Path(__file__).parent
UTILS_DIR = HERE / 'utils'
WORKING_DIR = HERE / 'KIP_DTR'


DOIT_CONFIG = {'action_string_formatting': 'new'}


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
