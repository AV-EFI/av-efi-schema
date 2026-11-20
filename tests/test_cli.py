"""The standalone command line entry point, tested as a user sees it."""

import json
import logging

from avefi_validate.cli import main

from helpers import ITEM, MANIFESTATION, PLACEHOLDER_ISSUER_ID, WORK


def _write(tmp_path, record_dicts, name="records.json"):
    target = tmp_path / name
    target.write_text(json.dumps(record_dicts), encoding="utf-8")
    return target


def _broken(tmp_path):
    """Return a file whose first record violates the line limit."""
    return _write(
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


def _placeholder(tmp_path):
    described_by = [
        {
            "has_issuer_id": PLACEHOLDER_ISSUER_ID,
            "has_issuer_name": "Unspecified data provider",
            "has_source_key": ["k1"],
        }
    ]
    return _write(
        tmp_path,
        [{**WORK, "described_by": described_by}, MANIFESTATION, ITEM],
    )


class TestReportsCounts:
    """The command reports invalid and dependant records apart."""

    def test_no_action_reports_both_counts(self, tmp_path, caplog):
        caplog.set_level(logging.INFO)
        target = _broken(tmp_path)
        exit_code = main([str(target)])
        assert exit_code != 0
        assert "1 invalid record" in caplog.text
        assert "2 dependant records" in caplog.text

    def test_no_action_does_not_rewrite_the_file(self, tmp_path, caplog):
        caplog.set_level(logging.INFO)
        target = _broken(tmp_path)
        before = target.read_text(encoding="utf-8")
        main([str(target)])
        assert target.read_text(encoding="utf-8") == before

    def test_remove_invalid_reports_both_counts(self, tmp_path, caplog):
        caplog.set_level(logging.INFO)
        target = _broken(tmp_path)
        exit_code = main(["--remove-invalid", str(target)])
        assert exit_code == 0
        assert "1 invalid record" in caplog.text
        assert "2 dependant records" in caplog.text
        assert json.loads(target.read_text(encoding="utf-8")) == []

    def test_a_valid_file_passes(self, tmp_path, caplog):
        caplog.set_level(logging.INFO)
        target = _write(tmp_path, [WORK, MANIFESTATION, ITEM])
        assert main([str(target)]) == 0
        assert "all 3 records passed" in caplog.text

    def test_a_missing_file_is_reported(self, tmp_path, caplog):
        caplog.set_level(logging.INFO)
        missing = tmp_path / "does-not-exist.json"
        assert main([str(missing)]) != 0
        assert "does-not-exist.json" in caplog.text


class TestPlaceholderIssuer:
    """The placeholder issuer is optional for a conversion-agnostic tool."""

    def test_the_file_passes_when_the_rule_is_not_asked_for(
        self, tmp_path, caplog
    ):
        caplog.set_level(logging.INFO)
        assert main([str(_placeholder(tmp_path))]) == 0

    def test_the_flag_rejects_it(self, tmp_path, caplog):
        caplog.set_level(logging.INFO)
        target = _placeholder(tmp_path)
        exit_code = main(
            ["--placeholder-issuer-id", PLACEHOLDER_ISSUER_ID, str(target)]
        )
        assert exit_code != 0
        assert "placeholder" in caplog.text.lower()

    def test_removing_invalid_records_does_not_hide_it(self, tmp_path, caplog):
        """--remove-invalid must not answer this by emptying the file."""
        caplog.set_level(logging.INFO)
        target = _placeholder(tmp_path)
        before = target.read_text(encoding="utf-8")
        exit_code = main(
            [
                "--remove-invalid",
                "--placeholder-issuer-id",
                PLACEHOLDER_ISSUER_ID,
                str(target),
            ]
        )
        assert exit_code != 0
        assert target.read_text(encoding="utf-8") == before


def _bad_duration(tmp_path):
    """Return a file whose item carries a valid but non-conforming duration."""
    item = {
        **ITEM,
        "has_duration": {"has_value": "PT22M24S"},
    }
    return _write(tmp_path, [WORK, MANIFESTATION, item])


class TestNormalise:
    """Normalising is opt-in and validates the repaired view."""

    def test_strict_validation_still_fails(self, tmp_path, caplog):
        caplog.set_level(logging.INFO)
        target = _bad_duration(tmp_path)
        before = target.read_text(encoding="utf-8")
        assert main([str(target)]) != 0
        assert target.read_text(encoding="utf-8") == before
        assert "value.normalised" not in caplog.text

    def test_normalise_validates_without_writing(self, tmp_path, caplog):
        caplog.set_level(logging.INFO)
        target = _bad_duration(tmp_path)
        before = target.read_text(encoding="utf-8")
        assert main(["--normalise", str(target)]) == 0
        assert target.read_text(encoding="utf-8") == before
        assert "PT22M24S" in caplog.text
        assert "PT00H22M24S" in caplog.text
        assert "1 value" in caplog.text

    def test_remove_invalid_writes_the_repaired_file(self, tmp_path):
        target = _bad_duration(tmp_path)
        assert main(["--normalise", "--remove-invalid", str(target)]) == 0
        data = json.loads(target.read_text(encoding="utf-8"))
        assert data[2]["has_duration"]["has_value"] == "PT00H22M24S"
        # The rewritten file now passes strict validation.
        assert main([str(target)]) == 0

    def test_json_report_carries_the_change(self, tmp_path, capsys):
        target = _bad_duration(tmp_path)
        assert main(["--normalise", "--format", "json", str(target)]) == 0
        data = json.loads(capsys.readouterr().out)
        diagnostic = next(
            diagnostic
            for diagnostic in data["files"][0]["diagnostics"]
            if diagnostic["code"] == "value.normalised"
        )
        assert diagnostic["severity"] == "warning"
        assert diagnostic["record"] == "Item.i1"
        assert diagnostic["pointer"] == "/has_duration/has_value"
        assert diagnostic["params"] == {
            "before": "PT22M24S",
            "after": "PT00H22M24S",
            "rule": "iso-duration",
        }
        assert data["passed"] is True
