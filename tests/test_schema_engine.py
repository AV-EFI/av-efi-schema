"""The Rust and Python schema engines behind one diagnostic surface.

The engine is an installation detail, so these tests pin the facts a
consumer may rely on: the same codes, pointers, ``params`` and counts,
and a message that is generated from those facts rather than from an
engine's prose.

"""

import json
import sys
from pathlib import Path

import pytest

from avefi_validate import pass_checks
from avefi_validate.documents import _schema_message, as_document
from avefi_validate.engine import (
    PythonSchemaValidator,
    RustSchemaValidator,
    build_schema_validator,
    iter_schema_errors,
)
from avefi_validate.io import loads_with_diagnostics
from avefi_validate.normalise import loads_normalised
from avefi_validate.schema import get_schema_validator, load_schema
from utils.version_snapshots import CASES_DIR, _limits

SCHEMA = load_schema()


@pytest.fixture(scope="module")
def python_engine():
    return PythonSchemaValidator(SCHEMA)


@pytest.fixture(scope="module")
def rust_engine():
    pytest.importorskip("jsonschema_rs")
    return RustSchemaValidator(SCHEMA)


def _diagnostics(validator, case):
    args = case.get("args") or {}
    load = loads_normalised if args.get("normalise") else loads_with_diagnostics
    loaded = load(json.dumps(case["records"]))
    result = pass_checks(
        loaded.records,
        validator,
        remove_invalid=bool(args.get("remove_invalid", False)),
        preserve_status_removed=bool(
            args.get("preserve_status_removed", False)
        ),
        placeholder_issuer_id=args.get("placeholder_issuer_id"),
        limits=_limits(args.get("limits")),
    )
    return list(loaded.diagnostics) + list(result.diagnostics), result


def _key(diagnostic):
    return (
        str(diagnostic.code),
        str(diagnostic.severity),
        diagnostic.record,
        diagnostic.pointer,
        repr(diagnostic.params),
        diagnostic.message,
    )


def _errors(validator, document, category):
    return sorted(
        (
            error.validator,
            tuple(error.absolute_path),
            repr(error.validator_value),
            _schema_message(error),
        )
        for error in iter_schema_errors(validator, document, category)
    )


def test_the_rust_engine_is_the_default_when_installed(monkeypatch):
    pytest.importorskip("jsonschema_rs")
    monkeypatch.delenv("AVEFFI_VALIDATE_ENGINE", raising=False)
    monkeypatch.setattr("avefi_validate.schema._VALIDATOR", None)
    assert get_schema_validator().engine == "rust"


def test_an_engine_can_be_selected(monkeypatch):
    monkeypatch.setenv("AVEFFI_VALIDATE_ENGINE", "python")
    assert build_schema_validator(SCHEMA).engine == "python"
    monkeypatch.setenv("AVEFFI_VALIDATE_ENGINE", "rust")
    assert build_schema_validator(SCHEMA).engine == "rust"


def test_a_missing_rust_engine_falls_back(monkeypatch):
    monkeypatch.delenv("AVEFFI_VALIDATE_ENGINE", raising=False)
    monkeypatch.setitem(sys.modules, "jsonschema_rs", None)
    assert build_schema_validator(SCHEMA).engine == "python"
    monkeypatch.setenv("AVEFFI_VALIDATE_ENGINE", "rust")
    with pytest.raises(ImportError):
        build_schema_validator(SCHEMA)


def test_the_engines_agree_on_the_version_corpus(python_engine, rust_engine):
    differences = []
    for path in sorted(CASES_DIR.glob("*.json")):
        case = json.loads(path.read_text(encoding="utf-8"))
        python_diagnostics, python_result = _diagnostics(python_engine, case)
        rust_diagnostics, rust_result = _diagnostics(rust_engine, case)
        if [list(map(_key, python_diagnostics))] != [
            list(map(_key, rust_diagnostics))
        ] or (python_result.invalid, python_result.dependants) != (
            rust_result.invalid,
            rust_result.dependants,
        ):
            differences.append(path.stem)
    assert differences == []


def test_required_errors_name_each_missing_property(python_engine, rust_engine):
    document = {}
    for validator in (python_engine, rust_engine):
        messages = {
            error[3]
            for error in _errors(validator, document, "Item")
            if error[0] == "required"
        }
        assert messages == {
            "missing required property 'is_item_of'",
            "missing required property 'category'",
        }


def test_additional_properties_name_the_extra_keys(python_engine, rust_engine):
    document = {
        "category": "avefi:Item",
        "is_item_of": [],
        "bogus": 1,
        "more": 2,
    }
    for validator in (python_engine, rust_engine):
        messages = {
            error[3]
            for error in _errors(validator, document, "Item")
            if error[0] == "additionalProperties"
        }
        assert messages == {"unexpected properties: 'bogus', 'more'"}


def test_type_errors_use_the_expected_types_in_schema_order(
    python_engine, rust_engine
):
    document = {
        "category": "avefi:Item",
        "is_item_of": [],
        "has_identifier": "not-a-list",
    }
    for validator in (python_engine, rust_engine):
        messages = {
            error[3]
            for error in _errors(validator, document, "Item")
            if error[0] == "type"
        }
        assert messages == {"value is not of type 'array', 'null'"}


def test_the_engines_agree_on_messages_for_every_used_keyword(
    python_engine, rust_engine
):
    case = json.loads(
        (CASES_DIR / "empty_name.json").read_text(encoding="utf-8")
    )
    pattern = next(
        as_document(record)
        for record in loads_with_diagnostics(
            json.dumps(case["records"])
        ).records
    )
    mutations = {
        "required": ({"category": "avefi:Item"}, "Item"),
        "type": (
            {
                "category": "avefi:Item",
                "is_item_of": [],
                "has_identifier": "not-a-list",
            },
            "Item",
        ),
        "enum": ({"category": "Bogus", "is_item_of": []}, "Item"),
        "additionalProperties": (
            {"category": "avefi:Item", "is_item_of": [], "bogus": 1},
            "Item",
        ),
        "anyOf": (
            {
                "category": "avefi:Item",
                "is_item_of": [],
                "has_duration": {"has_value": "PT1H32M"},
            },
            "Item",
        ),
        "pattern": (pattern, "WorkVariant"),
    }
    for keyword, (document, category) in mutations.items():
        assert _errors(python_engine, document, category) == _errors(
            rust_engine, document, category
        ), keyword


def test_format_is_not_enforced(python_engine, rust_engine):
    document = {
        "category": "avefi:Item",
        "is_item_of": [],
        "has_webresource": ["not a uri"],
    }
    for validator in (python_engine, rust_engine):
        keywords = {
            error[0] for error in _errors(validator, document, "Item")
        }
        assert "format" not in keywords


def test_a_raw_python_validator_still_works(python_engine):
    from jsonschema.validators import validator_for

    raw = validator_for(SCHEMA)(SCHEMA)
    case = json.loads(
        (CASES_DIR / "empty_name.json").read_text(encoding="utf-8")
    )
    adapted, _ = _diagnostics(python_engine, case)
    direct, _ = _diagnostics(raw, case)
    assert [list(map(_key, adapted))] == [list(map(_key, direct))]
    assert [diagnostic.code for diagnostic in direct] == [
        "schema.violation"
    ]
