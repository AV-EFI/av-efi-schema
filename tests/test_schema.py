"""The JSON Schema shipped as package data."""

import hashlib
from pathlib import Path

import pytest

from avefi_validate import schema

REPO_ROOT = Path(__file__).parents[1]
GENERATED = (
    REPO_ROOT / "project" / "jsonschema" / "avefi_schema" / "model.schema.json"
)


def test_the_schema_is_shipped_with_the_package():
    data = schema.load_schema()
    assert data.get("$id")
    assert data["type"] == "object"
    assert "$defs" in data or "definitions" in data


def test_the_validator_is_built_once():
    assert schema.get_schema_validator() is schema.get_schema_validator()


def test_fingerprint_identifies_the_schema():
    fingerprint = schema.schema_fingerprint()
    assert fingerprint["sha256"] == hashlib.sha256(
        schema.schema_bytes()
    ).hexdigest()
    assert fingerprint["source"].startswith("package:")
    assert fingerprint["id"] == schema.load_schema().get("$id")
    assert fingerprint["package"] == schema.package_version()
    assert fingerprint["version"] == schema.load_schema().get("version")


def test_the_packaged_copy_matches_the_generated_schema():
    """Running ``doit jsonschema`` must update both copies."""
    if not GENERATED.exists():  # installed distribution, no checkout
        pytest.skip("generated schema not available")
    assert schema.schema_bytes() == GENERATED.read_bytes()
