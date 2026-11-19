"""Relations between records: references, dangling records and purging."""

import copy

import pytest

from avefi_validate import CheckResult, Code, pass_checks

from helpers import (
    ITEM,
    MANIFESTATION,
    WORK,
    broken_hierarchy,
    records,
)


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
        first = copy.deepcopy(WORK)
        second = copy.deepcopy(WORK)
        second["has_identifier"] = [
            {"category": "avefi:LocalResource", "id": "w2"}
        ]
        first["is_part_of"] = [{"category": "avefi:LocalResource", "id": "w2"}]
        second["is_part_of"] = [
            {"category": "avefi:LocalResource", "id": "w1"}
        ]
        first["type"] = second["type"] = "Analytic"
        cycle = records(first, second)

        # The assertion that matters is that this returns at all: the
        # purge used to recurse until the stack was exhausted.
        result = pass_checks(cycle, validator, remove_invalid=True)
        assert isinstance(result, CheckResult)
        assert isinstance(result.passed, bool)


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
