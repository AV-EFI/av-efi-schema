"""The public surface of ``avefi_validate`` is part of the contract.

The verdict corpus covers rules; it cannot cover a helper that happens
to have no case. Freezing the names, parameters and enum members makes
every such change visible to the gate, and gives it a severity.

Regenerate with ``UPDATE_SNAPSHOTS=1 uv run pytest tests/test_api_surface.py``.

"""

from __future__ import annotations

import os

import avefi_validate

from utils.version_snapshots import (
    API_SNAPSHOT,
    api_snapshot,
    classify_api,
    write_json,
)

UPDATE = os.environ.get("UPDATE_SNAPSHOTS") == "1"


def load_snapshot() -> dict:
    """Return the recorded public surface, or an empty mapping."""
    import json

    if not API_SNAPSHOT.exists():
        return {}
    return json.loads(API_SNAPSHOT.read_text(encoding="utf-8"))


def test_the_package_declares_what_it_exports():
    assert avefi_validate.__all__, "avefi_validate declares no __all__"


def test_the_snapshot_is_not_empty():
    assert load_snapshot(), "no recorded surface; run doit version_snapshots"


def test_the_surface_matches_the_snapshot():
    actual = api_snapshot()
    if UPDATE:
        write_json(API_SNAPSHOT, actual)
        return
    assert actual == load_snapshot()


def test_every_public_name_is_described():
    snapshot = load_snapshot()
    assert set(snapshot) == set(avefi_validate.__all__) | (
        {"Code"} if hasattr(avefi_validate, "Code") else set()
    )


def test_a_removed_helper_is_breaking():
    old = {"helper": {"kind": "function", "params": []}}
    assert classify_api(old, {})[0] == "major"


def test_a_new_helper_is_additive():
    new = {"helper": {"kind": "function", "params": []}}
    assert classify_api({}, new)[0] == "minor"


def test_a_new_required_parameter_is_breaking():
    old = {"f": {"kind": "function", "params": [["a", "POSITIONAL_OR_KEYWORD", False]]}}
    new = {
        "f": {
            "kind": "function",
            "params": [
                ["a", "POSITIONAL_OR_KEYWORD", False],
                ["b", "POSITIONAL_OR_KEYWORD", False],
            ],
        }
    }
    assert classify_api(old, new)[0] == "major"


def test_a_new_optional_parameter_is_additive():
    old = {"f": {"kind": "function", "params": [["a", "POSITIONAL_OR_KEYWORD", False]]}}
    new = {
        "f": {
            "kind": "function",
            "params": [
                ["a", "POSITIONAL_OR_KEYWORD", False],
                ["b", "POSITIONAL_OR_KEYWORD", True],
            ],
        }
    }
    assert classify_api(old, new)[0] == "minor"


def test_an_enum_member_addition_is_additive():
    old = {"Code": {"kind": "enum", "members": ["a"]}}
    new = {"Code": {"kind": "enum", "members": ["a", "b"]}}
    assert classify_api(old, new)[0] == "minor"


def test_an_enum_member_removal_is_breaking():
    old = {"Code": {"kind": "enum", "members": ["a", "b"]}}
    new = {"Code": {"kind": "enum", "members": ["a"]}}
    assert classify_api(old, new)[0] == "major"
