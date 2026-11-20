"""The report document's shape is part of its contract.

The verdict corpus pins what the validator decides and the public
surface pins its names. Neither covers the JSON a consumer actually
reads: the keys of every block, the pointer shapes and the ``params``
keys per code. Freezing that shape gives the gate something to compare,
so a removed key cannot ship without a report-contract bump.

Regenerate with
``UPDATE_SNAPSHOTS=1 uv run pytest tests/test_report_surface.py``.

"""

from __future__ import annotations

import json
import os

from utils.version_snapshots import (
    REPORT_SURFACE,
    classify_report,
    report_surface,
    write_json,
)

UPDATE = os.environ.get("UPDATE_SNAPSHOTS") == "1"


def load_snapshot() -> dict:
    """Return the recorded report surface, or an empty mapping."""
    if not REPORT_SURFACE.exists():
        return {}
    return json.loads(REPORT_SURFACE.read_text(encoding="utf-8"))


def test_the_snapshot_is_not_empty():
    assert load_snapshot(), "no recorded surface; run doit version_snapshots"


def test_the_surface_matches_the_snapshot():
    actual = report_surface()
    if UPDATE:
        write_json(REPORT_SURFACE, actual)
        return
    assert actual == load_snapshot()


def test_every_code_is_described():
    from avefi_validate.report import Code

    snapshot = load_snapshot()
    codes = {code.value for code in Code}
    assert set(snapshot["codes"]) == codes
    assert set(snapshot["pointers"]) == codes
    assert set(snapshot["params"]) == codes


def test_normalisation_warnings_are_described():
    """Normalisation is a load-time rewrite, not a check diagnostic."""
    snapshot = load_snapshot()
    assert snapshot["params"]["value.normalised"] == [
        "after",
        "before",
        "rule",
    ]
    assert snapshot["pointers"]["value.normalised"]


def test_pointer_shapes_hide_concrete_indices():
    for pointers in load_snapshot()["pointers"].values():
        for pointer in pointers:
            if pointer == "<none>":
                continue
            parts = pointer.split("/")
            assert not any(part.isdigit() for part in parts), pointer


def test_a_removed_top_level_key_is_breaking():
    old = {"keys": ["tool", "report", "schema", "files", "passed"]}
    new = {"keys": ["tool", "schema", "files", "passed"]}
    severity, lines = classify_report(old, new)
    assert severity == "major"
    assert "top level: removed report" in lines


def test_an_added_block_is_additive():
    old = {"blocks": {"tool": ["name"]}}
    new = {"blocks": {"tool": ["name"], "report": ["version"]}}
    severity, lines = classify_report(old, new)
    assert severity == "minor"
    assert "report block: added version" in lines


def test_removing_a_params_key_is_breaking():
    old = {"params": {"field.too_long": ["field", "length", "limit"]}}
    new = {"params": {"field.too_long": ["field", "length"]}}
    severity, lines = classify_report(old, new)
    assert severity == "major"
    assert "field.too_long params key: removed limit" in lines


def test_removing_a_pointer_is_breaking():
    old = {"pointers": {"name.empty": ["/has_primary_title/has_name"]}}
    new = {"pointers": {"name.empty": []}}
    severity, lines = classify_report(old, new)
    assert severity == "major"
    assert "name.empty pointer: removed /has_primary_title/has_name" in lines


def test_an_added_pointer_is_only_a_note():
    old = {"pointers": {"name.empty": []}}
    new = {"pointers": {"name.empty": ["/has_primary_title/has_name"]}}
    severity, lines = classify_report(old, new)
    assert severity == "none"
    assert "name.empty pointer: added /has_primary_title/has_name" in lines


def test_removing_a_code_is_breaking():
    old = {"codes": ["name.empty"]}
    new = {"codes": []}
    severity, _ = classify_report(old, new)
    assert severity == "major"


def test_adding_a_code_is_additive():
    old = {"codes": []}
    new = {"codes": ["name.empty"]}
    severity, _ = classify_report(old, new)
    assert severity == "minor"
