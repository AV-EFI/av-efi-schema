"""Relations between records: references, dangling records and purging."""

import copy

import pytest

from avefi_schema import model_pydantic_v2 as efi
from avefi_validate import (
    CheckResult,
    Code,
    DIRECTED_RELATIONS,
    EQUIVALENCE_RELATIONS,
    HashableId,
    pass_checks,
)
from avefi_validate.records import reference_cycles

from helpers import (
    ITEM,
    MANIFESTATION,
    WORK,
    broken_hierarchy,
    records,
)

LOCAL = "avefi:LocalResource"


def _local(identifier):
    """Return a local reference to ``identifier``."""
    return {"category": LOCAL, "id": identifier}


def _analytic(identifier, parent):
    """Return an analytic work that is part of ``parent``."""
    record = copy.deepcopy(WORK)
    record["has_identifier"] = [_local(identifier)]
    record["type"] = "Analytic"
    record["is_part_of"] = [_local(parent)]
    return record


def _manifestation(identifier, **links):
    """Return a manifestation with ``identifier`` and extra links."""
    record = copy.deepcopy(MANIFESTATION)
    record["has_identifier"] = [_local(identifier)]
    record.update(copy.deepcopy(links))
    return record


def _item(identifier, manifestation):
    """Return an item of ``manifestation`` with ``identifier``."""
    record = copy.deepcopy(ITEM)
    record["has_identifier"] = [_local(identifier)]
    record["is_item_of"] = _local(manifestation)
    return record


class TestRemoveInvalid:
    """The destructive paths, which had no coverage at all."""

    def test_unresolvable_reference_is_reported(self, validator):
        orphan = records(ITEM)
        assert not pass_checks(orphan, validator)

    def test_unresolvable_reference_is_purged_on_request(self, validator):
        orphan = records(ITEM)
        pass_checks(orphan, validator, remove_invalid=True)
        assert orphan == []

    def test_complete_hierarchy_survives_a_purge(self, validator):
        complete = records(WORK, MANIFESTATION, ITEM)
        assert pass_checks(complete, validator, remove_invalid=True)
        assert len(complete) == 3

    def test_work_without_items_is_dangling(self, validator):
        assert not pass_checks(records(WORK), validator)

    def test_dangling_work_is_removed_on_request(self, validator):
        lonely = records(WORK)
        pass_checks(lonely, validator, remove_invalid=True)
        assert lonely == []

    def test_duplicate_identifiers_are_rejected(self, validator):
        duplicate = records(WORK, WORK, MANIFESTATION, ITEM)
        result = pass_checks(duplicate, validator)
        assert not result.passed
        assert result.invalid == 1
        assert any(
            diagnostic.code is Code.DUPLICATE_IDENTIFIER
            for diagnostic in result.diagnostics
        )

    def test_duplicate_identifiers_are_removed_on_request(self, validator):
        duplicate = records(WORK, WORK, MANIFESTATION, ITEM)
        pass_checks(duplicate, validator, remove_invalid=True)
        identifiers = [
            identifier.id
            for record in duplicate
            for identifier in record.has_identifier
        ]
        assert len(identifiers) == len(set(identifiers))

    def test_removing_a_parent_removes_its_children(self, validator):
        broken_work = copy.deepcopy(WORK)
        broken_work["has_primary_title"]["has_name"] = "x" * 1000
        hierarchy = records(broken_work, MANIFESTATION, ITEM)
        pass_checks(hierarchy, validator, remove_invalid=True)
        assert hierarchy == [], (
            "Children of a removed record must not survive it"
        )

    def test_a_reference_cycle_terminates(self, validator):
        """Mutually referencing records used to exhaust the stack."""
        cycle = records(_analytic("w1", "w2"), _analytic("w2", "w1"))

        result = pass_checks(cycle, validator, remove_invalid=True)
        assert isinstance(result, CheckResult)
        assert not result.passed
        assert cycle == []


class TestReferenceCycles:
    """Ordered relations must be acyclic; equivalence may be mutual."""

    def test_hierarchy_cycle_is_reported_for_every_member(self, validator):
        result = pass_checks(
            records(_analytic("w1", "w2"), _analytic("w2", "w1")),
            validator,
        )

        assert not result.passed
        assert result.invalid == 2
        diagnostics = [
            diagnostic
            for diagnostic in result.diagnostics
            if diagnostic.code is Code.REFERENCE_CYCLE
        ]
        assert [d.record for d in diagnostics] == [
            "WorkVariant.w1",
            "WorkVariant.w2",
        ]
        assert diagnostics[0].pointer == "/is_part_of"
        assert diagnostics[0].params == {
            "members": ["WorkVariant.w1", "WorkVariant.w2"],
            "relations": ["is_part_of"],
        }

    def test_self_reference_is_a_cycle(self, validator):
        result = pass_checks(records(_analytic("w1", "w1")), validator)

        assert result.invalid == 1
        diagnostic = result.diagnostics[0]
        assert diagnostic.code is Code.REFERENCE_CYCLE
        assert diagnostic.params == {
            "members": ["WorkVariant.w1"],
            "relations": ["is_part_of"],
        }

    def test_mixed_relations_form_one_cycle(self, validator):
        second = copy.deepcopy(WORK)
        second["has_identifier"] = [_local("w2")]
        second["is_variant_of"] = _local("w1")
        result = pass_checks(
            records(_analytic("w1", "w2"), second), validator
        )

        diagnostics = [
            diagnostic
            for diagnostic in result.diagnostics
            if diagnostic.code is Code.REFERENCE_CYCLE
        ]
        assert [d.record for d in diagnostics] == [
            "WorkVariant.w1",
            "WorkVariant.w2",
        ]
        assert diagnostics[0].params["relations"] == [
            "is_part_of",
            "is_variant_of",
        ]
        assert {
            diagnostic.record: diagnostic.pointer
            for diagnostic in diagnostics
        } == {
            "WorkVariant.w1": "/is_part_of",
            "WorkVariant.w2": "/is_variant_of",
        }

    def test_mutual_same_as_is_allowed(self, validator):
        records_ = records(
            WORK,
            _manifestation("m1", same_as=[_local("m2")]),
            _manifestation("m2", same_as=[_local("m1")]),
            _item("i1", "m1"),
            _item("i2", "m2"),
        )

        assert pass_checks(records_, validator).passed

    def test_mutual_copy_of_is_allowed(self, validator):
        first = _item("i1", "m1")
        first["is_copy_of"] = [_local("i2")]
        second = _item("i2", "m1")
        second["is_copy_of"] = [_local("i1")]

        assert pass_checks(
            records(WORK, MANIFESTATION, first, second), validator
        ).passed

    def test_mutual_derivative_is_rejected(self, validator):
        first = _item("i1", "m1")
        first["is_derivative_of"] = [_local("i2")]
        second = _item("i2", "m1")
        second["is_derivative_of"] = [_local("i1")]
        result = pass_checks(
            records(WORK, MANIFESTATION, first, second), validator
        )

        assert result.invalid == 2
        assert any(
            diagnostic.code is Code.REFERENCE_CYCLE
            and diagnostic.params["relations"] == ["is_derivative_of"]
            for diagnostic in result.diagnostics
        )

    def test_self_equivalence_is_rejected(self, validator):
        result = pass_checks(
            records(
                WORK,
                _manifestation("m1", same_as=[_local("m1")]),
                _item("i1", "m1"),
            ),
            validator,
        )

        assert result.invalid == 1
        assert result.dependants == 1
        diagnostic = result.diagnostics[0]
        assert diagnostic.record == "Manifestation.m1"
        assert diagnostic.pointer == "/same_as"
        assert diagnostic.params["relations"] == ["same_as"]

    def test_cycle_removes_members_and_cascades(self, validator):
        cycle = records(
            _analytic("w1", "w2"),
            _analytic("w2", "w1"),
            copy.deepcopy(MANIFESTATION),
            copy.deepcopy(ITEM),
        )

        result = pass_checks(cycle, validator, remove_invalid=True)

        assert result.invalid == 2
        assert result.dependants == 2
        assert cycle == []
        reasons = {
            removal.record: removal.reason for removal in result.removals
        }
        assert reasons["WorkVariant.w1"] is Code.REMOVED_AS_INVALID
        assert reasons["WorkVariant.w2"] is Code.REMOVED_AS_INVALID
        assert reasons["Manifestation.m1"] is Code.REMOVED_AS_DEPENDANT
        assert reasons["Item.i1"] is Code.REMOVED_AS_DEPENDANT

    def test_diagnostics_are_stable(self, validator):
        first = pass_checks(
            records(_analytic("w1", "w2"), _analytic("w2", "w1")),
            validator,
        )
        second = pass_checks(
            records(_analytic("w1", "w2"), _analytic("w2", "w1")),
            validator,
        )

        def signature(result):
            return [
                (diagnostic.record, diagnostic.pointer, diagnostic.params)
                for diagnostic in result.diagnostics
            ]

        assert signature(first) == signature(second)

    def test_a_long_chain_does_not_exhaust_the_stack(self):
        """Cycle detection is iterative, so depth is not a limit."""
        length = 5000
        chain = []
        for index in range(length):
            document = {
                "category": "avefi:WorkVariant",
                "type": "Analytic",
                "has_primary_title": {
                    "type": "PreferredTitle",
                    "has_name": "x",
                },
                "has_identifier": [_local(f"w{index}")],
            }
            if index + 1 < length:
                document["is_part_of"] = [_local(f"w{index + 1}")]
            chain.append(
                efi.MovingImageRecordTypeAdapter.validate_python(document)
            )

        lookup = {}
        for record in chain:
            identifiers = [
                HashableId(identifier)
                for identifier in record.has_identifier
            ]
            for reference in identifiers:
                lookup[reference] = (record, identifiers)

        assert reference_cycles(chain, lookup) == []



class TestInvalidCounts:
    """pass_checks reports invalid and dependant record counts.

    ``invalid`` counts the records that fail their own checks,
    ``dependants`` the records removed as a consequence.

    """

    def test_counts_without_removing(self, validator):
        hierarchy = broken_hierarchy()
        result = pass_checks(hierarchy, validator)
        assert not result.passed
        assert result.invalid == 1
        assert result.dependants == 2
        # Without remove_invalid the caller's list is untouched.
        assert len(hierarchy) == 3

    def test_counts_while_removing(self, validator):
        hierarchy = broken_hierarchy()
        result = pass_checks(hierarchy, validator, remove_invalid=True)
        assert not result.passed
        assert result.invalid == 1
        assert result.dependants == 2
        assert hierarchy == []

    def test_valid_hierarchy_reports_zero(self, validator):
        result = pass_checks(records(WORK, MANIFESTATION, ITEM), validator)
        assert result.passed
        assert result.invalid == 0
        assert result.dependants == 0

    def test_result_is_truthy_along_passed(self, validator):
        ok = pass_checks(records(WORK, MANIFESTATION, ITEM), validator)
        bad = broken_hierarchy()
        assert ok
        assert not pass_checks(bad, validator)


def test_relation_tables_are_public_and_disjoint():
    """Consumers build graphs from these tables, so both are contract."""
    assert set(DIRECTED_RELATIONS) == set(EQUIVALENCE_RELATIONS)
    directed = {
        attribute
        for attributes in DIRECTED_RELATIONS.values()
        for attribute in attributes
    }
    equivalence = {
        attribute
        for attributes in EQUIVALENCE_RELATIONS.values()
        for attribute in attributes
    }
    assert not directed & equivalence
