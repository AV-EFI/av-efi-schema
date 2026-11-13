"""Access to the JSON Schema shipped with this distribution.

The schema is package data: ``dodo.py`` writes
``project/jsonschema/avefi_schema/model.schema.json`` and links it
next to the generated bindings, so an installed ``avefi-schema``
always validates against the schema of its own version.

"""

from importlib import resources
import hashlib
import json
import logging

from jsonschema.validators import validator_for

log = logging.getLogger(__name__)

#: Name of the packaged schema document.
SCHEMA_RESOURCE = "model.schema.json"

#: Identifies the origin recorded in schema fingerprints.
SCHEMA_SOURCE = f"package:avefi_schema/{SCHEMA_RESOURCE}"

_VALIDATOR = None


def schema_bytes() -> bytes:
    """Return the packaged AVefi JSON Schema as bytes."""
    return (
        resources.files("avefi_schema")
        .joinpath(SCHEMA_RESOURCE)
        .read_bytes()
    )


def load_schema() -> dict:
    """Return the packaged AVefi JSON Schema."""
    return json.loads(schema_bytes())


def get_schema_validator():
    """Return a validator for the packaged AVefi JSON Schema.

    The validator is built once per process: it is immutable, and
    rebuilding it for every checked file would make a large submission
    needlessly slow.

    """
    global _VALIDATOR
    if _VALIDATOR is None:
        schema = load_schema()
        cls = validator_for(schema)
        cls.check_schema(schema)
        _VALIDATOR = cls(schema)
    return _VALIDATOR


def schema_fingerprint() -> dict:
    """Return an identification of the AVefi schema in use.

    Recording it in a conversion report makes the conversion
    reproducible after the fact: the hash identifies the exact schema
    document a file was checked against, independent of the package
    version.

    """
    raw = schema_bytes()
    schema = json.loads(raw)
    return {
        "source": SCHEMA_SOURCE,
        "id": schema.get("$id"),
        "version": schema.get("version"),
        "metamodel_version": schema.get("metamodel_version"),
        "sha256": hashlib.sha256(raw).hexdigest(),
    }
