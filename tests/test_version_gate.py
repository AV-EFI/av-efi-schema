"""The gate's rules, tested without git.

``evaluate`` is pure: it compares two snapshots and returns a report.
The git loader only fills those snapshots in, so the rules can be
exercised against fabricated revisions.
"""

from __future__ import annotations

from utils.version_gate import Decision, Snapshot, evaluate

WORK = {"$defs": {"Work": {"type": "object", "properties": {}}}}
WORK_AND_ITEM = {
    "$defs": {
        "Work": {"type": "object", "properties": {}},
        "Item": {"type": "object", "properties": {}},
    }
}
def changelog(version: str, schema: str) -> str:
    """Return a changelog with one complete release section."""
    return (
        "# Changelog\n\n"
        f"## {version}\n\n"
        f"Schema: {schema} (as released)\n"
        "Validator: unchanged\n"
    )


CHANGELOG = changelog("0.3.0", "0.3")


def snapshot(**changes) -> Snapshot:
    """Return a consistent snapshot, updated by ``changes``."""
    values = {
        "schema_version": "0.2",
        "package_version": "0.2.0",
        "schema": WORK,
        "verdicts": {"case": {"outcome": "passed"}},
        "api": {"helper": {"kind": "function", "params": []}},
        "changelog": "",
    }
    values.update(changes)
    return Snapshot(**values)


def rules(report) -> set[str]:
    return {rule for rule, _ in report.problems}


def test_a_correct_release_passes():
    report = evaluate(
        snapshot(),
        snapshot(
            schema_version="0.3",
            package_version="0.3.0",
            schema=WORK_AND_ITEM,
            changelog=CHANGELOG,
            paths=frozenset({"src/avefi_schema/model.yaml"}),
        ),
    )
    assert report.ok, report.lines()


def test_the_bootstrap_revision_is_exempt():
    """The first commit that adds versions cannot compare them."""
    report = evaluate(
        snapshot(schema_version=None, package_version=None, schema={}),
        snapshot(schema_version="2.0"),
    )
    assert report.ok, report.lines()
    assert any("no versions yet" in note for note in report.notes)


def test_r1_rejects_a_malformed_schema_version():
    report = evaluate(
        snapshot(),
        snapshot(schema_version="0.2.1"),
    )
    assert "R1" in rules(report)


def test_r1_rejects_a_malformed_package_version():
    report = evaluate(snapshot(), snapshot(package_version="0.2"))
    assert "R1" in rules(report)


def test_r2_rejects_a_decrease():
    report = evaluate(
        snapshot(schema_version="0.3", package_version="0.3.0"),
        snapshot(schema_version="0.2", package_version="0.2.0"),
    )
    assert "R2" in rules(report)


def test_r3_requires_the_schema_version_to_move():
    report = evaluate(snapshot(), snapshot(schema=WORK_AND_ITEM))
    assert "R3" in rules(report)


def test_r3_accepts_the_required_minor_bump_at_zero():
    report = evaluate(
        snapshot(),
        snapshot(
            schema_version="0.3",
            package_version="0.3.0",
            schema=WORK_AND_ITEM,
            changelog=CHANGELOG,
        ),
    )
    assert report.ok, report.lines()


def test_r3b_rejects_moving_the_schema_version_alone():
    report = evaluate(
        snapshot(),
        snapshot(schema_version="0.3", package_version="0.3.0", changelog=CHANGELOG),
    )
    assert "R3b" in rules(report)


def test_r4_requires_the_package_to_move_with_the_schema():
    report = evaluate(
        snapshot(),
        snapshot(schema_version="0.3", schema=WORK_AND_ITEM),
    )
    assert "R4" in rules(report)


def test_r4_accepts_a_schema_major_ahead_of_the_package():
    """The schema continues the public history; the package is separate."""
    report = evaluate(
        snapshot(),
        snapshot(
            schema_version="2.0",
            package_version="0.3.0",
            schema=WORK_AND_ITEM,
            changelog=changelog("0.3.0", "2.0"),
        ),
    )
    assert report.ok, report.lines()


def test_r6_requires_a_bump_when_a_verdict_tightens():
    report = evaluate(
        snapshot(),
        snapshot(verdicts={"case": {"outcome": "failed"}}),
    )
    assert "R6" in rules(report)


def test_r6_is_satisfied_by_a_minor_bump_at_zero():
    report = evaluate(
        snapshot(),
        snapshot(
            package_version="0.3.0",
            verdicts={"case": {"outcome": "failed"}},
            changelog=changelog("0.3.0", "0.2"),
        ),
    )
    assert report.ok, report.lines()


def test_r7_requires_a_patch_for_any_validator_edit():
    report = evaluate(
        snapshot(),
        snapshot(paths=frozenset({"src/python/avefi_validate/limits.py"})),
    )
    assert "R7" in rules(report)


def test_r7_is_satisfied_by_a_patch():
    report = evaluate(
        snapshot(),
        snapshot(
            package_version="0.2.1",
            changelog=changelog("0.2.1", "0.2"),
            paths=frozenset({"src/python/avefi_validate/limits.py"}),
        ),
    )
    assert report.ok, report.lines()


def test_r8_requires_a_bump_when_the_surface_changes():
    report = evaluate(snapshot(), snapshot(api={}))
    assert "R8" in rules(report)


def test_r9_requires_a_changelog_section():
    report = evaluate(snapshot(), snapshot(package_version="0.2.1"))
    assert "R9" in rules(report)


def test_r9_requires_both_lines():
    report = evaluate(
        snapshot(),
        snapshot(
            package_version="0.2.1",
            changelog="## 0.2.1\n\nSchema: 0.2\n",
        ),
    )
    assert "R9" in rules(report)


def test_r10_requires_a_decision_for_an_inconclusive_change():
    before = {"$defs": {"Work": {"pattern": "^a$"}}}
    after = {"$defs": {"Work": {"pattern": "^b$"}}}
    report = evaluate(
        snapshot(schema=before),
        snapshot(
            schema_version="0.3",
            package_version="0.3.0",
            schema=after,
            changelog=CHANGELOG,
        ),
    )
    assert "R10" in rules(report)


def test_r10_accepts_a_reviewed_decision():
    before = {"$defs": {"Work": {"pattern": "^a$"}}}
    after = {"$defs": {"Work": {"pattern": "^b$"}}}
    report = evaluate(
        snapshot(schema=before),
        snapshot(
            schema_version="0.3",
            package_version="0.3.0",
            schema=after,
            changelog=CHANGELOG,
        ),
        [Decision(schema_version="0.3", path="/$defs/Work/pattern", reviewed="minor")],
    )
    assert report.ok, report.lines()


def test_a_decision_for_another_release_is_not_reused():
    before = {"$defs": {"Work": {"pattern": "^a$"}}}
    after = {"$defs": {"Work": {"pattern": "^b$"}}}
    report = evaluate(
        snapshot(schema=before),
        snapshot(
            schema_version="0.3",
            package_version="0.3.0",
            schema=after,
            changelog=CHANGELOG,
        ),
        [Decision(schema_version="0.2", path="/$defs/Work/pattern", reviewed="minor")],
    )
    assert "R10" in rules(report)
