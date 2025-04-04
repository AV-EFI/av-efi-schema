# Only import modules from standard library here. Everything else
# should be imported from within function definition blocks (not
# starting with task_). This way, task_sync() gets a chance to update
# dependencies transparently even for this module
import copy
import json
from pathlib import Path

from doit import tools


DOIT_CONFIG = {
    'action_string_formatting': 'new',
    'default_tasks': [
        'jsonschema',
        'vocabularies',
        'python',
        'typescript',
        'json_lc_messages',
        'diagram',
    ],
}
HERE = Path(__file__).parent
SRC_DOCS_DIR = HERE / 'src' / 'docs'
DOCS_DIR = HERE / 'docs'
SCHEMA_OVERVIEW = DOCS_DIR / 'schema_overview.md'
ER_DIAGRAM = HERE / 'avefi_er_diagram.md'
SITE_DIR = HERE / 'site'
SCHEMA_NAME = 'avefi_schema'
SRC_SCHEMA_DIR = HERE / 'src' / SCHEMA_NAME
SRC_MODEL = SRC_SCHEMA_DIR / 'model.yaml'
SRC_SCHEMA_DEPENDENCIES = [
    SRC_MODEL,
    SRC_SCHEMA_DIR / 'vocab.yaml',
]
PROJECT_DIR = HERE / 'project'
JSON_SCHEMA = PROJECT_DIR / 'jsonschema' / SCHEMA_NAME \
    / f"{SRC_MODEL.stem}.schema.json"
EPIC_VOCAB_DIR = PROJECT_DIR / 'jsonschema' / 'epic' / 'vocabularies'
TYPESCRIPT_DIR = PROJECT_DIR / 'typescript'


def task_vocabularies():
    """Extract enum lists for typeapi from autogenerated json schema."""
    return {
        'actions': [
            'mkdir -p {targets}',
            generate_json_enum_files,
        ],
        'file_dep': [JSON_SCHEMA],
        'targets': [EPIC_VOCAB_DIR],
        'clean': ['rm -rf {targets}'],
    }


def generate_json_enum_files(dependencies, targets):
    """Generate vocabularies for use in the data type registry

    Results can be retrieved from
    https://raw.githubusercontent.com/AV-EFI/av-efi-schema/main/project/jsonschema/epic/vocabularies/

    """
    with open(dependencies[0], 'r') as f:
        schema = json.load(f)
    for key, value in schema['$defs'].items():
        if isinstance(value, dict):
            if 'enum' in value.keys():
                output = {'$id': key}
                output.update(value)
                output_path = EPIC_VOCAB_DIR / f"{key}.json"
                with output_path.open('w') as f:
                    json.dump(output, f, indent=2)
                    f.write('\n')


def task_jsonschema():
    """Generate derived JSON Schema."""
    return {
        'actions': [
            f"gen-json-schema --closed --title-from title"
            f" --top-class MovingImageRecord {SRC_MODEL}"
            f" > {{targets}}",
        ],
        'task_dep': ['sync_dependencies'],
        'file_dep': SRC_SCHEMA_DEPENDENCIES,
        'targets': [JSON_SCHEMA],
    }


def task_python():
    """Generate python bindings.

    Even though the designator slot "category" is declared required in
    the schema, let it be treated as optional by the generated
    bindings. This is convenient when constructors can determine that
    value automatically on instantiation.

    """
    def generate_bindings(module_name, class_name, source, target, **kwargs):
        import importlib
        gen_module = importlib.import_module(
            f"linkml.generators.{module_name}")
        gen = getattr(gen_module, class_name)(source, **kwargs)
        # Make category slot optional and rely on constructors to fill
        # it correctly
        if gen.schema.slots['category'].designates_type:
            gen.schema.slots['category'].required = False
        with open(target, 'w') as f:
            f.write(gen.serialize())

    python_model = PROJECT_DIR / 'python' / SCHEMA_NAME \
        / f"{SRC_MODEL.stem}.py"
    for module, cls, target, kwargs in [
            ('pythongen', 'PythonGenerator', python_model, {}),
            ('pydanticgen', 'PydanticGenerator',
             python_model.with_stem(f"{python_model.stem}_pydantic_v2"),
             {'pydantic_version': 2}),
    ]:
        yield {
            'name': module,
            'actions': [
                (generate_bindings, [module, cls, SRC_MODEL, target],
                 kwargs),
            ],
            'task_dep': ['sync_dependencies'],
            'file_dep': SRC_SCHEMA_DEPENDENCIES,
            'targets': [target],
        }


def task_typescript():
    """Generate typescript derivatives."""
    typescript_path = TYPESCRIPT_DIR / f"{SCHEMA_NAME}.ts"
    for cmd, target in [
            ('gen-typescript --log_level ERROR', typescript_path),
            ('gen-typescript --log_level ERROR --gen-type-utils',
             typescript_path.with_stem(f"{typescript_path.stem}_type_utils")),
    ]:
        yield {
            'name': cmd,
            'actions': [
                f"{cmd} {SRC_MODEL} > {{targets}}",
            ],
            'task_dep': ['sync_dependencies'],
            'file_dep': SRC_SCHEMA_DEPENDENCIES,
            'targets': [target],
        }


def task_json_lc_messages():
    """Generate locale message catalog in JSON."""
    def lc_messages_from_labels(dependencies, targets):
        import linkml_runtime as linkmlr
        schema = linkmlr.SchemaView(SRC_MODEL)
        lc_message_catalog = {}
        for lc_code in ('en', 'de'):
            lc_messages = lc_message_catalog.setdefault(lc_code, {})
            for cls in schema.all_classes().values():
                result = None
                for label, attrs in cls.structured_aliases.items():
                    if attrs.in_language == 'default' and result == None:
                        result = label
                    elif attrs.in_language == lc_code:
                        result = label
                if result:
                    lc_messages[schema.get_uri(cls.name)] = result
            for enum in schema.all_enums().values():
                for key, value in enum.permissible_values.items():
                    result = None
                    for label, attrs in value.structured_aliases.items():
                        if attrs.in_language == 'default' and result == None:
                            result = label
                        elif attrs.in_language == lc_code:
                            result = label
                    if result:
                        lc_messages[key] = result
        lc_messages_path = Path(targets[0])
        with open(lc_messages_path, 'w') as f:
            json.dump(
                lc_message_catalog, f, indent=4, sort_keys=True,
                ensure_ascii=False)
            f.write('\n')

    return {
        'actions': [
            lc_messages_from_labels,
        ],
        'task_dep': [
            'sync_dependencies',
        ],
        'file_dep': SRC_SCHEMA_DEPENDENCIES,
        'targets': [TYPESCRIPT_DIR / 'locale_messages.json'],
        'clean': True,
    }


def task_docs():
    """Build documentation from LinkML schema."""
    return {
        'actions': [
            gen_doc,
        ],
        'task_dep': [
            'sync_dependencies',
            'copy_src_docs',
            'diagram',
        ],
        'file_dep': SRC_SCHEMA_DEPENDENCIES,
        'targets': [SCHEMA_OVERVIEW],
        'clean': [f"rm -rf {DOCS_DIR}"],
    }


def gen_doc(dependencies, targets):
    """Essentially gen-doc tuned for less aggressive cut offs."""
    import re
    from linkml.generators import docgen

    # Be less aggressive about truncating long lines for tables
    def enshorten(input):
        """Custom filter to truncate long text intended to go in a table.

        Remove anything after a newline but do not cut off after full
        stops. This is required to preserve links.

        """
        if input is None:
            return ""
        match = re.search(r'^(.*?([.;?!] (?<!(etc|.\..)\. )|\n|$))', input)
        input = match.group()
        return input
    docgen.enshorten = enshorten

    index_file = Path(targets[0])
    gen = docgen.DocGenerator(
        SRC_MODEL,
        directory=index_file.parent,
        hierarchical_class_view=False,
        index_name=index_file.stem,
        sort_by='rank',
    )
    print(gen.serialize())


def task_diagram():
    """Generate diagram from LinkML schema."""
    return {
        'actions': [
            "gen-erdiagram -c WorkVariant -c Manifestation"
            " -c Item --follow-references {dependencies} > {targets}",
        ],
        'task_dep': ['sync_dependencies'],
        'file_dep': [SRC_MODEL],
        'targets': [ER_DIAGRAM],
    }


def task_copy_src_docs():
    """Copy files over from src/docs."""
    dependencies = list(SRC_DOCS_DIR.glob('*.md'))
    targets = [DOCS_DIR / d.name for d in dependencies]
    return {
        'actions': [
            f"mkdir -p {DOCS_DIR}",
            f"cp -rf {{dependencies}} {DOCS_DIR}",
        ],
        'file_dep': dependencies,
        'targets': targets,
    }


def task_build_site():
    """Build static site from provided documentation."""
    return {
        'actions': [
            'mkdocs build',
        ],
        'task_dep': ['docs'],
        'file_dep': [SCHEMA_OVERVIEW],
        'targets': [SITE_DIR / 'schema_overview' / 'index.html'],
        'clean': [f"rm -rf {SITE_DIR}"],
    }


def task_serve_site():
    """Serve documentation on localhost for testing."""
    return {
        'actions': [
            'mkdocs serve',
        ],
        'task_dep': ['build_site'],
    }


def task_deploy_site():
    """Deploy docs to GitHub Pages."""
    return {
        'actions': [
            'mkdocs gh-deploy',
        ],
        'task_dep': ['build_site'],
    }


def task_sync_dependencies():
    """Install dependencies according to pdm.lock (for developers)."""
    return {
        'actions': [
            'pdm sync',
        ],
        'file_dep': ['pdm.lock'],
    }


def task_update_dependencies():
    """Update dependencies (linkml, etc.)."""
    return {
        'actions': [
            'pdm update -u',
        ],
        'uptodate': (True,),
    }


def task_check_dtr():
    """Compare each type and class against Data Type Registry."""
    def check_dtr(sync):
        from utils import datatypegen
        dtr_gen = datatypegen.DataTypeGenerator(SRC_MODEL, sync_mode=sync)
        dtr_gen.process_schema()
    return {
        'actions': [tools.PythonInteractiveAction(check_dtr)],
        'params': [
            {
                'name': 'sync',
                'long': 'sync',
                'type': bool,
                'default': False,
                'help':
                'Ask for credentials and push changes to Data Type Registry.',
            },
        ],
    }
