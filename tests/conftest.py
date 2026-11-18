"""Shared fixtures for the validator tests."""

import sys
from pathlib import Path

import pytest

from avefi_validate import get_schema_validator

# The versioning tests import the repository's ``utils`` package, which
# is not installed. Pytest puts the test file's directory on the path,
# not the repository root, so add that explicitly.
_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))


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
