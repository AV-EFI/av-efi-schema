"""Unit tests for the structural schema classifier.

Each test is one row of the compatibility table in
``versioning/README.md``. Together they decide whether the gate can be
trusted: everything the classifier cannot prove has to be reported as
``inconclusive`` so that a reviewer signs it off.

"""

from __future__ import annotations

import pytest

from utils.version_contract import (
    INCONCLUSIVE,
    MAJOR,
    MINOR,
    NONE,
    classify,
    required_schema_bump,
    bump_satisfied,
)


def document(**changes):
    """Return a small but realistic schema root, updated by ``changes``."""
    root = {
        "$defs": {"Work": {"type": "object", "properties": {}}},
        "anyOf": [{"$ref": "#/$defs/Work"}],
    }
    root.update(changes)
    return root


def defs(work):
    """Return a document whose single definition is ``work``."""
    return document(**{"$defs": {"Work": work}})


def severity(before, after) -> str:
    return classify(before, after).severity


def assert_inconclusive(before, after) -> None:
    """Assert the change needs a reviewer, not a guessed severity."""
    verdict = classify(before, after)
    assert verdict.inconclusive, f"decided as {verdict.severity}: {verdict.changes}"


def test_identical_documents_need_nothing():
    assert severity(document(), document()) == NONE


def test_descriptions_titles_and_examples_are_ignored():
    before = defs({"type": "object", "description": "old", "title": "Old"})
    after = defs(
        {
            "type": "object",
            "description": "new",
            "title": "New",
            "examples": [{"a": 1}],
        }
    )
    verdict = classify(before, after)
    assert verdict.severity == NONE
    assert verdict.changes == ()


def test_the_root_contract_version_is_not_a_schema_change():
    """The gate compares ``model.yaml`` separately; it must not double count."""
    assert severity({"version": "0.2"}, {"version": "0.3"}) == NONE


def test_a_property_named_version_is_still_compared():
    before = defs({"properties": {"version": {"type": "string"}}})
    after = defs({"properties": {"version": {"type": "integer"}}})
    assert severity(before, after) == MAJOR


@pytest.mark.parametrize(
    ("before", "after", "expected"),
    [
        pytest.param(
            document(),
            document(**{"$defs": {"Work": {"type": "object", "properties": {}}, "New": {"type": "string"}}}),
            MINOR,
            id="definition-added",
        ),
        pytest.param(
            document(**{"$defs": {"Work": {}, "Old": {}}}),
            document(**{"$defs": {"Work": {}}}),
            MAJOR,
            id="definition-removed",
        ),
    ],
)
def test_definition_membership(before, after, expected):
    assert severity(before, after) == expected


@pytest.mark.parametrize(
    ("before", "after", "expected"),
    [
        pytest.param(
            defs({"properties": {"a": {"type": "string"}}}),
            defs(
                {
                    "properties": {
                        "a": {"type": "string"},
                        "b": {"type": "string"},
                    }
                }
            ),
            MINOR,
            id="optional-property-added",
        ),
        pytest.param(
            defs(
                {
                    "properties": {
                        "a": {"type": "string"},
                        "b": {"type": "string"},
                    }
                }
            ),
            defs(
                {
                    "properties": {"a": {"type": "string"}},
                    "required": ["b"],
                }
            ),
            MAJOR,
            id="property-removed",
        ),
        pytest.param(
            defs({"properties": {"a": {"type": "string"}}}),
            defs(
                {
                    "properties": {
                        "a": {"type": "string"},
                        "b": {"type": "string"},
                    },
                    "required": ["b"],
                }
            ),
            MAJOR,
            id="required-property-added",
        ),
        pytest.param(
            defs(
                {
                    "properties": {"a": {"type": "string"}},
                    "required": ["a"],
                }
            ),
            defs({"properties": {"a": {"type": "string"}}}),
            MINOR,
            id="required-property-relaxed",
        ),
        pytest.param(
            defs({"properties": {}}),
            defs(
                {
                    "properties": {"type": {"type": "string"}},
                    "required": ["type"],
                }
            ),
            MAJOR,
            id="required-property-named-type",
        ),
        pytest.param(
            defs({"properties": {}}),
            defs({"properties": {"required": {"type": "string"}}}),
            MINOR,
            id="optional-property-named-required",
        ),
        pytest.param(
            defs({"properties": {"pattern": {"type": "string"}}}),
            defs({"properties": {}}),
            MAJOR,
            id="property-named-pattern-removed",
        ),
        pytest.param(
            defs({"properties": {}}),
            defs({"properties": {"maxLength": {"type": "integer"}}}),
            MINOR,
            id="property-named-maxLength",
        ),
        pytest.param(
            defs({"properties": {}}),
            defs({"properties": {"$schema": {"type": "string"}}}),
            MINOR,
            id="property-named-schema-keyword",
        ),
    ],
)
def test_object_membership(before, after, expected):
    assert severity(before, after) == expected


@pytest.mark.parametrize(
    ("before", "after", "expected"),
    [
        pytest.param(
            {"enum": ["a"]}, {"enum": ["a", "b"]}, MINOR, id="enum-widened"
        ),
        pytest.param(
            {"enum": ["a", "b"]}, {"enum": ["a"]}, MAJOR, id="enum-narrowed"
        ),
        pytest.param(
            {"type": ["string"]}, {"type": ["string", "null"]}, MINOR,
            id="type-list-widened",
        ),
        pytest.param(
            {"type": ["string", "null"]}, {"type": ["string"]}, MAJOR,
            id="type-list-narrowed",
        ),
        pytest.param(
            {"type": "string"}, {"type": ["string", "null"]}, MINOR
        ),
        pytest.param(
            {"type": ["string", "null"]}, {"type": "string"}, MAJOR
        ),
        pytest.param({"type": "string"}, {"type": "integer"}, MAJOR),
    ],
)
def test_value_sets(before, after, expected):
    assert severity(defs(before), defs(after)) == expected


@pytest.mark.parametrize(
    ("before", "after", "expected"),
    [
        pytest.param(
            {"maxLength": 10}, {"maxLength": 5}, MAJOR, id="max-tightened"
        ),
        pytest.param(
            {"maxLength": 5}, {"maxLength": 10}, MINOR, id="max-relaxed"
        ),
        pytest.param({}, {"maxLength": 10}, MAJOR, id="max-added"),
        pytest.param({"maxLength": 10}, {}, MINOR, id="max-removed"),
        pytest.param(
            {"minItems": 1}, {"minItems": 2}, MAJOR, id="min-tightened"
        ),
        pytest.param(
            {"minItems": 2}, {"minItems": 1}, MINOR, id="min-relaxed"
        ),
        pytest.param({}, {"minimum": 0}, MAJOR, id="minimum-added"),
        pytest.param({"maximum": 9}, {"maximum": 99}, MINOR),
    ],
)
def test_numeric_bounds(before, after, expected):
    assert severity(defs(before), defs(after)) == expected


@pytest.mark.parametrize(
    ("before", "after", "expected"),
    [
        pytest.param({}, {"pattern": "^a$"}, MAJOR, id="pattern-added"),
        pytest.param({"pattern": "^a$"}, {}, MINOR, id="pattern-removed"),
        pytest.param(
            {"pattern": "^a$"},
            {"pattern": "^[ab]$"},
            INCONCLUSIVE,
            id="pattern-changed",
        ),
        pytest.param({"format": "uri"}, {}, MINOR, id="format-removed"),
        pytest.param({}, {"format": "uri"}, INCONCLUSIVE, id="format-added"),
        pytest.param(
            {"$ref": "#/$defs/A"},
            {"$ref": "#/$defs/B"},
            INCONCLUSIVE,
            id="ref-changed",
        ),
    ],
)
def test_constraints_that_need_a_reviewer(before, after, expected):
    before, after = defs(before), defs(after)
    if expected == INCONCLUSIVE:
        assert_inconclusive(before, after)
    else:
        assert severity(before, after) == expected


@pytest.mark.parametrize(
    ("before", "after", "expected"),
    [
        pytest.param(
            {"additionalProperties": True},
            {"additionalProperties": False},
            MAJOR,
            id="closed",
        ),
        pytest.param(
            {"additionalProperties": False},
            {"additionalProperties": True},
            MINOR,
            id="opened",
        ),
        pytest.param({}, {"additionalProperties": False}, MAJOR),
        pytest.param({}, {"additionalProperties": True}, MINOR),
        pytest.param({}, {"const": "a"}, MAJOR, id="const-added"),
        pytest.param({"const": "a"}, {}, MINOR, id="const-removed"),
        pytest.param({"const": "a"}, {"const": "b"}, MAJOR),
    ],
)
def test_keywords(before, after, expected):
    assert severity(defs(before), defs(after)) == expected


def test_identifier_change_is_breaking():
    assert severity({"$id": "old"}, {"$id": "new"}) == MAJOR


def test_metamodel_version_is_inconclusive():
    assert_inconclusive(
        {"metamodel_version": "1.11"}, {"metamodel_version": "1.12"}
    )


def test_root_union_membership():
    smaller = document(anyOf=[{"$ref": "#/$defs/Work"}])
    larger = document(
        anyOf=[{"$ref": "#/$defs/Work"}, {"$ref": "#/$defs/Item"}]
    )
    assert severity(smaller, larger) == MINOR
    assert severity(larger, smaller) == MAJOR


def test_unknown_keyword_is_inconclusive():
    assert_inconclusive(defs({}), defs({"uniqueItems": True}))


def test_an_inconclusive_change_is_kept_beside_the_decided_severity():
    before = document(**{"$defs": {"Work": {"pattern": "^a$"}, "Old": {}}})
    after = document(**{"$defs": {"Work": {"pattern": "^b$"}}})
    verdict = classify(before, after)
    assert verdict.severity == MAJOR
    assert [change.path for change in verdict.inconclusive] == [
        "/$defs/Work/pattern"
    ]
    assert verdict.requires_bump


def test_report_lines_name_the_path_and_the_verdict():
    verdict = classify({"$defs": {"A": {}}}, {"$defs": {}})
    assert any(
        "/$defs/A" in line and MAJOR in line for line in verdict.lines()
    )


@pytest.mark.parametrize(
    ("verdict", "major", "expected"),
    [
        pytest.param(NONE, 0, NONE),
        pytest.param(NONE, 1, NONE),
        pytest.param("patch", 0, NONE),
        pytest.param(MINOR, 0, MINOR),
        pytest.param(MINOR, 1, MINOR),
        pytest.param(MAJOR, 0, MINOR, id="0.x-minor-is-breaking"),
        pytest.param(MAJOR, 1, MAJOR),
    ],
)
def test_required_schema_bump(verdict, major, expected):
    assert required_schema_bump(verdict, major) == expected


@pytest.mark.parametrize(
    ("old", "new", "required", "expected"),
    [
        pytest.param("0.2", "0.3", MINOR, True),
        pytest.param("0.2", "0.2", MINOR, False),
        pytest.param("0.2", "0.4", MINOR, True),
        pytest.param("1.2", "2.0", MAJOR, True),
        pytest.param("1.2", "1.3", MAJOR, False),
        pytest.param("1.2", "1.2", NONE, True),
        pytest.param("nonsense", "1.2", MINOR, False),
    ],
)
def test_bump_satisfied(old, new, required, expected):
    assert bump_satisfied(old, new, required) is expected
