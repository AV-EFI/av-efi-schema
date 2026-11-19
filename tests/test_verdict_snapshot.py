"""The recorded validator outcomes must stay exactly as reviewed.

A change here is not automatically a bug: it is a change of the
acceptance rules, and therefore of the version. Regenerate with

    UPDATE_SNAPSHOTS=1 uv run pytest tests/test_verdict_snapshot.py

(``uv run doit version_snapshots`` does the same for both snapshots)
and bump the package as the gate requires.

"""

from __future__ import annotations

import json
import os

from utils.version_snapshots import (
    CASES_DIR,
    VERDICT_SNAPSHOT,
    classify_verdicts,
    collect_verdicts,
    load_verdicts,
    write_json,
)

UPDATE = os.environ.get("UPDATE_SNAPSHOTS") == "1"


def test_the_snapshot_is_not_empty():
    assert load_verdicts(), "no recorded outcomes; run doit version_snapshots"


def test_every_case_has_an_outcome():
    cases = {path.stem for path in CASES_DIR.glob("*.json")}
    recorded = set(load_verdicts())
    assert cases == recorded, (
        f"unrecorded: {sorted(cases - recorded)};"
        f" stale: {sorted(recorded - cases)}"
    )


def test_outcomes_match_the_snapshot():
    actual = collect_verdicts()
    if UPDATE:
        write_json(VERDICT_SNAPSHOT, actual)
        return
    assert actual == load_verdicts()


def test_cases_carry_their_purpose():
    """A case nobody can explain cannot be reviewed."""
    for path in CASES_DIR.glob("*.json"):
        case = json.loads(path.read_text(encoding="utf-8"))
        assert case.get("description"), f"{path.name} has no description"
        assert "records" in case, f"{path.name} has no records"


def test_a_tightened_case_requires_a_major_bump():
    old = {"case": {"outcome": "passed", "invalid": 0, "dependants": 0}}
    new = {"case": {"outcome": "failed", "invalid": 1, "dependants": 0}}
    severity, lines = classify_verdicts(old, new)
    assert severity == "major"
    assert lines == ["case: tightening"]


def test_a_loosened_case_requires_a_minor_bump():
    old = {"case": {"outcome": "failed", "invalid": 1, "dependants": 0}}
    new = {"case": {"outcome": "passed", "invalid": 0, "dependants": 0}}
    severity, lines = classify_verdicts(old, new)
    assert severity == "minor"
    assert lines == ["case: loosening"]


def test_a_new_case_is_a_minor_change():
    severity, _ = classify_verdicts({}, {"case": {"outcome": "passed"}})
    assert severity == "minor"


def test_removing_a_diagnostic_code_is_breaking():
    old = {"case": {"outcome": "failed", "codes": ["field.too_long"]}}
    new = {"case": {"outcome": "failed", "codes": []}}
    severity, lines = classify_verdicts(old, new)
    assert severity == "major"
    assert "case: removed code(s) field.too_long" in lines


def test_adding_a_diagnostic_code_is_minor():
    old = {"case": {"outcome": "failed", "codes": []}}
    new = {"case": {"outcome": "failed", "codes": ["field.too_long"]}}
    severity, lines = classify_verdicts(old, new)
    assert severity == "minor"
    assert "case: added code(s) field.too_long" in lines
