"""Checks a single record has to pass, beyond the JSON Schema."""

import copy

import pytest

from avefi_validate import DEFAULT_LIMITS, io
from avefi_validate.documents import (
    exceeds_field_limit,
    has_invalid_value,
    pass_checks,
)

from helpers import (
    ITEM,
    PLACEHOLDER_ISSUER_ID,
    WORK,
    records,
    with_issuer,
)


class TestPeriods:
    """The period rules, previously asserted inside `if` blocks."""

    def test_analytic_works_validate(self, input_path, validator):
        sample_file = input_path("analytic_works.json")
        efi_records = io.load(sample_file)
        assert efi_records, "Fixture must not be empty"
        assert pass_checks(efi_records, validator), (
            f"Failed to validate {sample_file}"
        )

    def test_valid_period_passes(self, input_path, validator):
        efi_records = io.load(input_path("analytic_works.json"))
        assert pass_checks(efi_records, validator)

    @pytest.mark.parametrize(
        ("period", "expected"),
        [("1975/1976", True), ("1975/1975", True), ("1976/1975", False)],
    )
    def test_period_order(self, input_path, validator, period, expected):
        efi_records = io.load(input_path("analytic_works.json"))
        record = copy.deepcopy(efi_records[0])
        assert record.has_event, "Fixture record must carry an event"
        record.has_event[0].has_date = period

        assert (
            bool(pass_checks([record], validator, remove_invalid=False))
            is expected
        )


class TestFieldLimits:
    def test_overlong_title_is_invalid(self):
        record = copy.deepcopy(WORK)
        record["has_primary_title"]["has_name"] = "x" * 1000
        assert has_invalid_value(records(record)[0])

    def test_title_at_the_limit_is_accepted(self):
        record = copy.deepcopy(WORK)
        record["has_primary_title"]["has_name"] = "x" * DEFAULT_LIMITS.line_limit
        assert not exceeds_field_limit(records(record)[0])

    def test_limits_can_be_overridden(self):
        record = copy.deepcopy(WORK)
        record["has_primary_title"]["has_name"] = "x" * 10
        from avefi_validate import Limits

        assert not exceeds_field_limit(records(record)[0])
        assert exceeds_field_limit(
            records(record)[0], limits=Limits(line_limit=5)
        )


class TestDateValidation:
    """The date rules, locked in independently of the event loop."""

    def _work_with_event(self, has_date=None):
        record = copy.deepcopy(WORK)
        event = {
            "category": "avefi:ProductionEvent",
            "has_activity": [],
            "located_in": [],
        }
        if has_date is not None:
            event["has_date"] = has_date
        record["has_event"] = [event]
        return records(record)[0]

    def test_record_without_events_is_not_rejected(self):
        record = copy.deepcopy(WORK)
        record["has_event"] = []
        assert not has_invalid_value(records(record)[0])

    def test_invalid_date_is_rejected(self):
        record = self._work_with_event(has_date="19/75")
        assert has_invalid_value(record)

    def test_invalid_date_is_purged_on_request(self, validator):
        # A reversed period passes the schema (it is a valid EDTF
        # interval) but is rejected by the additional date rule.
        bad = self._work_with_event(has_date="1976/1975")
        record_list = [bad]
        pass_checks(record_list, validator, remove_invalid=True)
        assert record_list == []

    def test_period_reversal_via_has_invalid_value(self):
        record = self._work_with_event(has_date="1976/1975")
        assert has_invalid_value(record)


class TestPreserveStatusRemoved:
    """The option used to be declared but never passed on."""

    def _removed_item(self):
        item = copy.deepcopy(ITEM)
        item["has_access_status"] = "Removed"
        return records(item)[0]

    def test_removed_without_pid_is_invalid_by_default(self):
        assert has_invalid_value(self._removed_item())

    def test_removed_without_pid_is_accepted_when_preserved(self):
        assert not has_invalid_value(
            self._removed_item(), preserve_status_removed=True
        )


class TestPlaceholderIssuer:
    """A file naming no data provider must not reach registration.

    A converter may refuse to emit such a file unless it is told to,
    but a file produced that way, or by invoking a converter module
    directly rather than through its command line, still reaches the
    validator. The check runs before identifiers are registered, so it
    is the last step that can notice this.

    The rule is a submission convention rather than a schema rule, so
    it applies only when the caller names the placeholder: a caller
    that knows nothing about how the file was produced passes ``None``.

    """

    def test_a_named_issuer_passes(self, validator):
        named = with_issuer("https://w3id.org/isil/DE-MUS-000000")
        assert pass_checks(
            named, validator, placeholder_issuer_id=PLACEHOLDER_ISSUER_ID
        )

    def test_the_placeholder_issuer_does_not_pass(self, validator):
        assert not pass_checks(
            with_issuer(PLACEHOLDER_ISSUER_ID),
            validator,
            placeholder_issuer_id=PLACEHOLDER_ISSUER_ID,
        )

    def test_the_rule_is_off_by_default(self, validator):
        assert pass_checks(with_issuer(PLACEHOLDER_ISSUER_ID), validator)

    def test_removing_invalid_records_does_not_empty_the_file(self, validator):
        """The issuer is not something a record can be dropped for."""
        placeholder = with_issuer(PLACEHOLDER_ISSUER_ID)
        pass_checks(
            placeholder,
            validator,
            remove_invalid=True,
            placeholder_issuer_id=PLACEHOLDER_ISSUER_ID,
        )
        assert len(placeholder) == 3
