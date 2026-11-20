"""Repairing values before they are checked, tested rule by rule."""

import copy
import json

import pytest

from avefi_validate import (
    Code,
    load_normalised,
    loads_normalised,
    normalise_document,
    normalise_record,
)
from avefi_validate.normalise import RULES, UNNORMALISED
from avefi_validate.schema import load_schema

from helpers import ITEM, MANIFESTATION, WORK


def _item(**duration):
    """Return an Item with a duration, as raw JSON."""
    record = copy.deepcopy(ITEM)
    record["has_duration"] = duration
    return record


class TestDurations:
    @pytest.mark.parametrize(
        ("before", "after"),
        [
            ("PT22M24S", "PT00H22M24S"),
            ("PT1H30M", "PT01H30M00S"),
            ("P1DT2H", "PT26H00M00S"),
            ("PT1.5H", "PT01H30M00S"),
            ("PT1H2M3.6S", "PT01H02M04S"),
            ("PT0S", "PT00H00M00S"),
        ],
    )
    def test_expands_to_fixed_hours(self, before, after):
        result = normalise_record(_item(has_value=before))
        assert result.document["has_duration"]["has_value"] == after
        assert result.changes[0].before == before
        assert result.changes[0].after == after
        assert result.changes[0].rule == "iso-duration"

    @pytest.mark.parametrize("value", ["P1M", "P1Y", "P", "PT", "banana"])
    def test_calendar_forms_are_left_alone(self, value):
        result = normalise_record(_item(has_value=value))
        assert result.document["has_duration"]["has_value"] == value
        assert not result.changed

    def test_fractional_seconds_round_to_nearest(self):
        result = normalise_record(_item(has_value="PT1.4S"))
        assert result.document["has_duration"]["has_value"] == "PT00H00M01S"
        result = normalise_record(_item(has_value="PT1.6S"))
        assert result.document["has_duration"]["has_value"] == "PT00H00M02S"

    def test_a_conforming_value_is_not_touched(self):
        document = _item(has_value="PT00H22M24S")
        result = normalise_record(document)
        assert result.document is document
        assert not result.changed


class TestDates:
    @pytest.mark.parametrize(
        ("before", "after"),
        [
            ("2024-4-5", "2024-04-05"),
            ("2024/04/24", "2024-04-24"),
            ("1980/12", "1980-12"),
            ("202-01", "0202-01"),
        ],
    )
    def test_pads_and_separates(self, before, after):
        record = copy.deepcopy(WORK)
        record["has_event"] = [
            {
                "category": "avefi:ProductionEvent",
                "has_date": before,
            }
        ]
        result = normalise_record(record)
        assert result.document["has_event"][0]["has_date"] == after
        assert result.changes[0].rule == "edtf-date"

    @pytest.mark.parametrize(
        "value",
        ["2024?", "1980-12-31/1981", "2024"],
    )
    def test_conforming_dates_are_not_touched(self, value):
        record = copy.deepcopy(WORK)
        record["has_event"] = [
            {
                "category": "avefi:ProductionEvent",
                "has_date": value,
            }
        ]
        result = normalise_record(record)
        assert result.document["has_event"][0]["has_date"] == value
        assert not result.changed

    def test_impossible_month_is_left_for_the_checks(self):
        record = copy.deepcopy(WORK)
        record["has_event"] = [
            {
                "category": "avefi:ProductionEvent",
                "has_date": "2024-13",
            }
        ]
        result = normalise_record(record)
        assert result.document["has_event"][0]["has_date"] == "2024-13"
        assert not result.changed


class TestTimestamps:
    def _record(self, value):
        record = copy.deepcopy(WORK)
        record["described_by"] = [
            {
                "last_modified": value,
                "has_issuer_id": "21.T11969/issuer",
                "has_issuer_name": "Provider",
            }
        ]
        return record

    @pytest.mark.parametrize(
        ("before", "after"),
        [
            ("2024-04-24T16:36:14+02:00", "2024-04-24T14:36:14Z"),
            ("2024-04-24T16:36+02:00", "2024-04-24T14:36:00Z"),
        ],
    )
    def test_converts_an_explicit_offset(self, before, after):
        result = normalise_record(self._record(before))
        assert result.document["described_by"][0]["last_modified"] == after
        assert result.changes[0].rule == "utc-timestamp"

    @pytest.mark.parametrize(
        "value",
        [
            "2024-04-24T16:36:14Z",
            "2024-04-24T16:36:14+00:00",
            "2024-04-24T16:36:14.500+00:00",
        ],
    )
    def test_a_conforming_timestamp_is_not_touched(self, value):
        result = normalise_record(self._record(value))
        assert result.document["described_by"][0]["last_modified"] == value
        assert not result.changed

    @pytest.mark.parametrize(
        "value",
        [
            "2024-04-24T16:36:14",
            "2024-04-24T16:36",
            "2024-04-24",
            "2024/04/24",
        ],
    )
    def test_naive_timestamps_are_not_assumed_to_be_utc(self, value):
        result = normalise_record(self._record(value))
        assert result.document["described_by"][0]["last_modified"] == value
        assert not result.changed


class TestTextAndIdentifiers:
    def test_text_line_is_trimmed_and_single_line(self):
        record = copy.deepcopy(WORK)
        record["has_primary_title"]["has_name"] = "  Die\nBrücke  "
        result = normalise_record(record)
        assert (
            result.document["has_primary_title"]["has_name"] == "Die Brücke"
        )
        assert result.changes[0].rule == "text-line"

    def test_empty_text_line_stays_empty(self):
        record = copy.deepcopy(WORK)
        record["has_primary_title"]["has_name"] = "   "
        result = normalise_record(record)
        assert result.document["has_primary_title"]["has_name"] == "   "
        assert not result.changed

    def test_avefi_handle_prefix_is_stripped(self):
        record = copy.deepcopy(ITEM)
        record["has_identifier"] = [
            {
                "category": "avefi:AVefiResource",
                "id": "https://hdl.handle.net/21.T11969/abc",
            }
        ]
        result = normalise_record(record)
        assert result.document["has_identifier"][0]["id"] == "21.T11969/abc"
        assert result.changes[0].rule == "av-efi-handle"

    def test_avefi_handle_is_trimmed(self):
        record = copy.deepcopy(ITEM)
        record["has_identifier"] = [
            {"category": "avefi:AVefiResource", "id": " 21.T11969/abc "}
        ]
        result = normalise_record(record)
        assert result.document["has_identifier"][0]["id"] == "21.T11969/abc"

    @pytest.mark.parametrize(
        ("category", "before", "after", "rule"),
        [
            (
                "avefi:TGNResource",
                "https://vocab.getty.edu/tgn/7000000",
                "7000000",
                "tgn-id",
            ),
            (
                "avefi:GNDResource",
                "https://d-nb.info/gnd/118540238",
                "118540238",
                "gnd-id",
            ),
            (
                "avefi:VIAFResource",
                "viaf:123456789",
                "123456789",
                "viaf-id",
            ),
            (
                "avefi:WikidataResource",
                "https://www.wikidata.org/entity/q42",
                "Q42",
                "wikidata-id",
            ),
            (
                "avefi:FilmportalResource",
                "filmportal:ABCDEF0123456789ABCDEF0123456789",
                "abcdef0123456789abcdef0123456789",
                "filmportal-id",
            ),
            (
                "avefi:EIDRResource",
                "eidr:10.5240/ABCD-1234",
                "10.5240/ABCD-1234",
                "eidr",
            ),
        ],
    )
    def test_authority_resolvers_are_stripped(
        self, category, before, after, rule
    ):
        record = copy.deepcopy(WORK)
        if category == "avefi:TGNResource":
            record["has_subject"] = [
                {
                    "category": "avefi:GeographicName",
                    "same_as": [
                        {"category": "avefi:TGNResource", "id": before}
                    ],
                }
            ]
            result = normalise_record(record)
            value = result.document["has_subject"][0]["same_as"][0]["id"]
        else:
            record["same_as"] = [{"category": category, "id": before}]
            result = normalise_record(record)
            value = result.document["same_as"][0]["id"]
        assert value == after
        assert result.changes[0].rule == rule

    def test_aat_prefix_is_stripped(self):
        record = copy.deepcopy(WORK)
        record["has_subject"] = [
            {
                "category": "avefi:Subject",
                "same_as": [
                    {"category": "avefi:AATResource", "id": "aat:300000000"}
                ],
            }
        ]
        result = normalise_record(record)
        assert (
            result.document["has_subject"][0]["same_as"][0]["id"]
            == "300000000"
        )
        assert result.changes[0].rule == "aat-id"

    def test_doi_resolver_is_stripped(self):
        record = copy.deepcopy(ITEM)
        record["same_as"] = [
            {
                "category": "avefi:DOIResource",
                "id": "https://doi.org/10.5240/ABCD-1234",
            }
        ]
        result = normalise_record(record)
        assert result.document["same_as"][0]["id"] == "10.5240/ABCD-1234"
        assert result.changes[0].rule == "doi"

    def test_isil_rule_strips_its_prefix(self):
        from avefi_validate.normalise import ISIL_PATTERN

        rule, normalise = RULES[ISIL_PATTERN]
        assert rule == "isil"
        assert normalise("isil:de-101") == "DE-101"

    def test_an_unknown_prefix_is_not_guessed(self):
        record = copy.deepcopy(WORK)
        record["same_as"] = [
            {"category": "avefi:WikidataResource", "id": "Q42-extra"}
        ]
        result = normalise_record(record)
        assert result.document["same_as"][0]["id"] == "Q42-extra"
        assert not result.changed


class TestDocument:
    def test_labels_name_the_record_and_pointer(self):
        record = _item(has_value="PT22M24S")
        result = normalise_document([record])
        change = result.changes[0]
        assert change.record == "Item.i1"
        assert change.pointer == "/has_duration/has_value"
        assert change.to_dict()["rule"] == "iso-duration"

    def test_the_input_document_is_not_mutated(self):
        record = _item(has_value="PT22M24S")
        original = copy.deepcopy(record)
        normalise_document([record])
        assert record == original

    def test_every_schema_pattern_has_a_rule_or_a_reason(self):
        schema = load_schema()
        patterns = set()

        def walk(node):
            if isinstance(node, dict):
                pattern = node.get("pattern")
                if isinstance(pattern, str):
                    patterns.add(pattern)
                for value in node.values():
                    walk(value)
            elif isinstance(node, list):
                for value in node:
                    walk(value)

        walk(schema)
        assert patterns <= set(RULES) | set(UNNORMALISED)
        assert not patterns & set(UNNORMALISED) & set(RULES)

    def test_every_registered_rule_key_is_a_schema_pattern(self):
        schema = load_schema()
        patterns = set()

        def walk(node):
            if isinstance(node, dict):
                pattern = node.get("pattern")
                if isinstance(pattern, str):
                    patterns.add(pattern)
                for value in node.values():
                    walk(value)
            elif isinstance(node, list):
                for value in node:
                    walk(value)

        walk(schema)
        assert set(RULES) <= patterns


class TestLoaders:
    def test_unparseable_duration_is_recovered(self):
        loaded = loads_normalised(json.dumps([_item(has_value="PT22M24S")]))
        assert not loaded.diagnostics
        assert len(loaded.records) == 1
        assert loaded.records[0].has_duration.has_value == "PT00H22M24S"
        assert len(loaded.normalisations) == 1
        assert loaded.normalisations[0].rule == "iso-duration"

    def test_file_loader_matches_string_loader(self, tmp_path):
        target = tmp_path / "records.json"
        target.write_text(
            json.dumps([_item(has_value="PT22M24S")]), encoding="utf-8"
        )
        loaded = load_normalised(target)
        assert loaded.records[0].has_duration.has_value == "PT00H22M24S"
        assert loaded.sha256 is not None

    def test_strict_loader_is_unchanged(self):
        from avefi_validate import io

        loaded = io.loads_with_diagnostics(
            json.dumps([_item(has_value="PT22M24S")])
        )
        assert len(loaded.records) == 1
        assert loaded.records[0].has_duration.has_value == "PT22M24S"
        assert not loaded.normalisations


class TestCodes:
    def test_normalisation_is_a_warning_code(self):
        assert Code.VALUE_NORMALISED == "value.normalised"
