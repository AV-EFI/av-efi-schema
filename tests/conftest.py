"""Shared fixtures for the validator tests."""

from pathlib import Path

import pytest

from avefi_validate import get_schema_validator


@pytest.fixture(scope="module")
def input_path(request):
    """Return a resolver for files in ``tests/data``."""

    def get_path(filename):
        return Path(request.path).parent / "data" / filename

    return get_path


@pytest.fixture(scope="module")
def validator():
    """Return the validator for the packaged schema, built once."""
    return get_schema_validator()
