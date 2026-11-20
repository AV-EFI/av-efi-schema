"""The structured report: stable codes, pointers and JSON rendering."""

import copy
import json

from avefi_validate import (
    REPORT_CONTRACT_VERSION,
    Code,
    Diagnostic,
    FileReport,
    Removal,
    Report,
    Severity,
    pass_checks,
    value_diagnostics,
)
from avefi_validate.cli import main
from avefi_validate.io import loads_with_diagnostics

from helpers import ITEM, MANIFESTATION, WORK, broken_hierarchy, records


def _multi_violation():
    """Return one record that breaks several unrelated rules."""
    record = copy.deepcopy(WORK)
    record["has_primary_title"] = {
        "type": "TitleProper",
        "has_name": "x" * 1000,
    }
    record["has_genre"] = [{"has_name": ""}]
    record["has_event"] = [
        {
            "category": "avefi:ProductionEvent",
            "has_activity": [],
            "has_date": "1976/1975",
            "located_in": [],
        }
    ]
    return records(record)[0]


class TestDiagnosticCollection:
    def test_a_record_reports_every_violation(self):
        diagnostics = value_diagnostics(_multi_violation())
        codes = {diagnostic.code for diagnostic in diagnostics}
        assert codes == {
            Code.FIELD_TOO_LONG,
            Code.NAME_EMPTY,
            Code.DATE_PERIOD_ORDER,
            Code.TITLE_PRIMARY_TYPE,
        }

    def test_schema_and_semantic_violations_are_both_reported(self, validator):
        record = copy.deepcopy(WORK)
        record["has_primary_title"]["has_name"] = ""
        record["has_genre"] = [{"has_name": ""}]
        result = pass_checks(records(record), validator)
        codes = {diagnostic.code for diagnostic in result.diagnostics}
        assert Code.SCHEMA_VIOLATION in codes
        assert Code.NAME_EMPTY in codes
        assert result.invalid == 1

    def test_diagnostics_carry_a_pointer_into_the_record(self):
        diagnostics = value_diagnostics(_multi_violation())
        empty = next(
            diagnostic
            for diagnostic in diagnostics
            if diagnostic.code is Code.NAME_EMPTY
        )
        assert empty.pointer == "/has_genre/0/has_name"
        assert empty.record == "WorkVariant.w1"

    def test_counts_are_unchanged_by_the_report(self, validator):
        hierarchy = broken_hierarchy()
        result = pass_checks(hierarchy, validator)
        assert result.invalid == 1
        assert result.dependants == 2
        assert len(result.diagnostics) == 1


class TestTolerantLoading:
    def test_one_bad_item_does_not_cost_the_others(self):
        loaded = loads_with_diagnostics(
            json.dumps(
                [
                    {"category": "avefi:Unknown", "has_identifier": []},
                    WORK,
                    MANIFESTATION,
                    ITEM,
                ]
            )
        )
        assert loaded.initial_count == 4
        assert len(loaded.records) == 3
        assert [d.code for d in loaded.diagnostics] == [
            Code.RECORD_UNPARSEABLE
        ]
        assert loaded.diagnostics[0].params["index"] == 0

    def test_a_broken_file_does_not_stop_the_next(self, tmp_path, caplog):
        import logging

        caplog.set_level(logging.INFO)
        missing = tmp_path / "missing.json"
        good = tmp_path / "good.json"
        good.write_text(
            json.dumps([WORK, MANIFESTATION, ITEM]), encoding="utf-8"
        )
        assert main([str(missing), str(good)]) != 0
        assert "missing.json" in caplog.text
        assert "all 3 records passed" in caplog.text


class TestRemovalReasons:
    def test_cascade_names_the_record_it_depends_on(self, validator):
        hierarchy = records(
            {
                **WORK,
                "has_primary_title": {
                    "type": "PreferredTitle",
                    "has_name": "x" * 1000,
                },
            },
            MANIFESTATION,
            ITEM,
        )
        result = pass_checks(hierarchy, validator, remove_invalid=True)
        reasons = {
            (removal.record, removal.reason) for removal in result.removals
        }
        assert ("WorkVariant.w1", Code.REMOVED_AS_INVALID) in reasons
        assert (
            "Manifestation.m1",
            Code.REMOVED_AS_DEPENDANT,
        ) in reasons
        assert all(
            removal.because == "WorkVariant.w1"
            for removal in result.removals
            if removal.reason is Code.REMOVED_AS_DEPENDANT
        )


class TestRejectedDependants:
    """A parent whose children were rejected is not an orphan."""

    def _invalid_item(self):
        item = copy.deepcopy(ITEM)
        item["has_primary_title"]["has_name"] = ""
        return item

    def test_manifestation_reports_rejected_item_as_referrer(
        self, validator
    ):
        result = pass_checks(
            records(WORK, MANIFESTATION, self._invalid_item()), validator
        )
        diagnostic = next(
            d for d in result.diagnostics if d.record == "Manifestation.m1"
        )
        assert diagnostic.code is Code.REMOVED_AS_DEPENDANT
        assert str(diagnostic.code) == "record.depends_on_invalid"
        assert diagnostic.params["referrers"] == ["Item.i1"]
        assert not any(
            d.code is Code.RECORD_DANGLING
            and d.record == "Manifestation.m1"
            for d in result.diagnostics
        )

    def test_work_reports_the_rejected_manifestation_as_referrer(
        self, validator
    ):
        result = pass_checks(
            records(WORK, MANIFESTATION, self._invalid_item()), validator
        )
        diagnostic = next(
            d for d in result.diagnostics if d.record == "WorkVariant.w1"
        )
        assert diagnostic.code is Code.REMOVED_AS_DEPENDANT
        assert diagnostic.params["referrers"] == ["Manifestation.m1"]

    def test_genuine_orphan_keeps_record_dangling(self, validator):
        result = pass_checks(records(WORK), validator)
        diagnostic = next(
            d for d in result.diagnostics if d.record == "WorkVariant.w1"
        )
        assert diagnostic.code is Code.RECORD_DANGLING
        assert "referrers" not in diagnostic.params

    def test_cascade_removal_names_the_referrer(self, validator):
        result = pass_checks(
            records(WORK, MANIFESTATION, self._invalid_item()),
            validator,
            remove_invalid=True,
        )
        removals = {
            (removal.record, removal.reason, removal.because)
            for removal in result.removals
        }
        assert (
            "Manifestation.m1",
            Code.REMOVED_AS_DEPENDANT,
            "Item.i1",
        ) in removals
        assert (
            "WorkVariant.w1",
            Code.REMOVED_AS_DEPENDANT,
            "Manifestation.m1",
        ) in removals

    def test_json_reports_the_referrers(self, tmp_path, capsys):
        target = tmp_path / "records.json"
        target.write_text(
            json.dumps([WORK, MANIFESTATION, self._invalid_item()]),
            encoding="utf-8",
        )
        assert main(["--format", "json", str(target)]) != 0
        data = json.loads(capsys.readouterr().out)
        diagnostic = next(
            diagnostic
            for diagnostic in data["files"][0]["diagnostics"]
            if diagnostic["code"] == "record.depends_on_invalid"
            and diagnostic["record"] == "Manifestation.m1"
        )
        assert diagnostic["params"]["referrers"] == ["Item.i1"]


class TestReportDocument:
    def test_diagnostic_serialises_every_contractual_key(self):
        diagnostic = Diagnostic(
            code=Code.FIELD_TOO_LONG,
            message="too long",
            record="WorkVariant.w1",
            pointer="/has_primary_title/has_name",
            params={"field": "has_primary_title.has_name", "limit": 250},
        )
        assert diagnostic.to_dict() == {
            "code": "field.too_long",
            "severity": "error",
            "record": "WorkVariant.w1",
            "pointer": "/has_primary_title/has_name",
            "params": {
                "field": "has_primary_title.has_name",
                "limit": 250,
            },
            "message": "too long",
        }

    def test_report_serialises_files_and_outcome(self, tmp_path):
        file = FileReport(
            path=tmp_path / "records.json",
            initial=1,
            remaining=1,
            invalid=1,
            passed=False,
            diagnostics=[
                Diagnostic(Code.SCHEMA_VIOLATION, "bad", Severity.ERROR)
            ],
            removed=[
                Removal("WorkVariant.w1", Code.REMOVED_AS_INVALID)
            ],
        )
        report = Report(
            package="0.4.0",
            schema={"version": "2.0"},
            files=[file],
        )
        data = report.to_dict()
        assert data["tool"] == {"name": "avefi-validate", "package": "0.4.0"}
        assert data["report"] == {"version": REPORT_CONTRACT_VERSION}
        assert data["schema"] == {"version": "2.0"}
        assert data["passed"] is False
        assert data["files"][0]["counts"]["invalid"] == 1
        assert data["files"][0]["diagnostics"][0]["code"] == "schema.violation"
        assert data["files"][0]["removed"][0]["reason"] == "record.invalid"
        json.dumps(data)


class TestJsonOutput:
    def _write(self, tmp_path, record_dicts):
        target = tmp_path / "records.json"
        target.write_text(json.dumps(record_dicts), encoding="utf-8")
        return target

    def test_format_json_writes_one_document_to_stdout(
        self, tmp_path, capsys
    ):
        target = self._write(tmp_path, [WORK, MANIFESTATION, ITEM])
        assert main(["--format", "json", str(target)]) == 0
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data["passed"] is True
        assert data["tool"]["name"] == "avefi-validate"
        assert data["report"]["version"] == REPORT_CONTRACT_VERSION
        assert data["files"][0]["counts"]["initial"] == 3

    def test_report_path_writes_the_document_there(
        self, tmp_path, capsys
    ):
        target = self._write(tmp_path, [WORK, MANIFESTATION, ITEM])
        destination = tmp_path / "report.json"
        assert main(["--report", str(destination), str(target)]) == 0
        assert capsys.readouterr().out == ""
        data = json.loads(destination.read_text(encoding="utf-8"))
        assert data["passed"] is True

    def test_json_reports_a_failure_and_keeps_the_exit_code(
        self, tmp_path, capsys
    ):
        target = self._write(
            tmp_path,
            [
                {
                    **WORK,
                    "has_primary_title": {
                        "type": "PreferredTitle",
                        "has_name": "x" * 1000,
                    },
                },
                MANIFESTATION,
                ITEM,
            ],
        )
        assert main(["--format", "json", str(target)]) != 0
        data = json.loads(capsys.readouterr().out)
        assert data["passed"] is False
        file = data["files"][0]
        assert file["passed"] is False
        assert file["counts"] == {
            "initial": 3,
            "remaining": 3,
            "invalid": 1,
            "dependants": 2,
        }
        assert file["diagnostics"][0]["code"] == "field.too_long"
