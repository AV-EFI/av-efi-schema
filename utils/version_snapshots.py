"""Snapshots of the behaviour a version number promises.

Three things are invisible in a structural diff of the schema but
decide what a consumer can rely on:

* what the validator decides for a fixed corpus of records;
* the public surface of ``avefi_validate``;
* the shape of the report document.

Freezing all three turns "did the validator change?" into "did an
expected outcome change?", which is the question SemVer actually
answers. The direction of a change also gives the severity: a case
that used to pass and now fails is a tightening, which is breaking for
anyone whose data now gets rejected.

Regenerate the snapshots with ``doit version_snapshots`` and commit the
result *together with* the version bump the change requires.
"""

from __future__ import annotations

import dataclasses
import inspect
import json
import re
from dataclasses import replace
from enum import Enum
from pathlib import Path
from typing import Any

from .version_contract import MAJOR, MINOR, NONE, SEVERITY

ROOT = Path(__file__).resolve().parent.parent
CASES_DIR = ROOT / "tests" / "data" / "version_contract" / "cases"
VERDICT_SNAPSHOT = ROOT / "tests" / "data" / "version_contract" / "expected.json"
API_SNAPSHOT = ROOT / "tests" / "data" / "api_surface.json"
REPORT_SURFACE = ROOT / "tests" / "data" / "report_surface.json"


# --- verdict corpus -----------------------------------------------------


def _load_case(case: dict):
    """Load one corpus case through the tolerant loader."""
    from avefi_validate.io import loads_with_diagnostics
    from avefi_validate.normalise import loads_normalised

    args = case.get("args") or {}
    load = loads_normalised if args.get("normalise") else loads_with_diagnostics
    return load(json.dumps(case["records"]))


def _check_loaded(case: dict, loaded):
    """Run the submission checks for one loaded case."""
    from avefi_validate import pass_checks
    from avefi_validate.schema import get_schema_validator

    args = case.get("args") or {}
    return pass_checks(
        loaded.records,
        get_schema_validator(),
        remove_invalid=bool(args.get("remove_invalid", False)),
        preserve_status_removed=bool(
            args.get("preserve_status_removed", False)
        ),
        placeholder_issuer_id=args.get("placeholder_issuer_id"),
        limits=_limits(args.get("limits")),
    )


def verdict_outcome(case: dict) -> dict:
    """Return the observable outcome of one case.

    Only stable facts are recorded: the verdict, the counts, the sorted
    diagnostic codes and the *name* of an exception class. Messages are
    not part of the contract and must stay free to change.

    The corpus goes through the tolerant loader, the same path the
    command line uses: a case with one unparseable record still says
    what happened to the others.

    """
    try:
        loaded = _load_case(case)
    except Exception as exc:  # noqa: BLE001 - the class name is the datum
        return {
            "outcome": "raised",
            "stage": "load",
            "exception": type(exc).__name__,
        }
    records = loaded.records

    try:
        result = _check_loaded(case, loaded)
    except Exception as exc:  # noqa: BLE001 - the class name is the datum
        return {
            "outcome": "raised",
            "stage": "check",
            "exception": type(exc).__name__,
        }

    diagnostics = list(loaded.diagnostics) + list(result.diagnostics)
    codes = {str(diagnostic.code) for diagnostic in diagnostics}
    if loaded.normalisations:
        codes.add("value.normalised")
    passed = result.passed and not diagnostics
    return {
        "outcome": "passed" if passed else "failed",
        "invalid": result.invalid,
        "dependants": result.dependants,
        "remaining": len(records),
        "codes": sorted(codes),
    }


def _limits(override: dict | None):
    """Return the default limits, optionally overridden by a case."""
    from avefi_validate import DEFAULT_LIMITS

    if not override:
        return DEFAULT_LIMITS
    return replace(DEFAULT_LIMITS, **override)


def collect_verdicts() -> dict:
    """Run every case in the corpus and return the outcomes."""
    outcomes = {}
    for path in sorted(CASES_DIR.glob("*.json")):
        case = json.loads(path.read_text(encoding="utf-8"))
        outcomes[path.stem] = verdict_outcome(case)
    return outcomes


def load_verdicts(path: Path = VERDICT_SNAPSHOT) -> dict:
    """Return the recorded outcomes, or an empty mapping."""
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    """Write ``data`` as stable, reviewable JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def classify_verdicts(old: dict, new: dict) -> tuple[str, list[str]]:
    """Return the bump a change of outcomes requires.

    A case that used to be accepted and now is not is a tightening:
    data that used to be registrable is rejected. The opposite
    direction is a loosening. Both are visible to a consumer, so
    neither is a patch.

    A code that disappears is breaking for a consumer that branches on
    it, so it counts as major; a new code is additive. Counts changing
    under the same verdict are a minor change, because they alter what a
    report says without altering whether a record is accepted.

    """
    severity = NONE
    lines = []
    for name in sorted(set(old) | set(new)):
        before = old.get(name)
        after = new.get(name)
        if before == after:
            continue
        if before is None:
            lines.append(f"{name}: new case")
            severity = _worse(severity, MINOR)
            continue
        if after is None:
            lines.append(f"{name}: case removed")
            severity = _worse(severity, MINOR)
            continue
        if _accepted(before) and not _accepted(after):
            lines.append(f"{name}: tightening")
            severity = _worse(severity, MAJOR)
        elif not _accepted(before) and _accepted(after):
            lines.append(f"{name}: loosening")
            severity = _worse(severity, MINOR)
        else:
            lines.append(f"{name}: same verdict, different detail")
            severity = _worse(severity, MINOR)
        removed_codes = sorted(set(_codes(before)) - set(_codes(after)))
        added_codes = sorted(set(_codes(after)) - set(_codes(before)))
        if removed_codes:
            lines.append(
                f"{name}: removed code(s) {', '.join(removed_codes)}"
            )
            severity = _worse(severity, MAJOR)
        elif added_codes:
            lines.append(f"{name}: added code(s) {', '.join(added_codes)}")
            severity = _worse(severity, MINOR)
    return severity, lines


def _codes(outcome: dict) -> list[str]:
    """Return the recorded diagnostic codes of an outcome."""
    codes = outcome.get("codes", [])
    return [str(code) for code in codes] if isinstance(codes, list) else []


def _accepted(outcome: dict) -> bool:
    """Whether the outcome reports no problem with the records."""
    return outcome.get("outcome") == "passed"


# --- report surface -----------------------------------------------------


def report_surface() -> dict:
    """Return the shape of the report document, without any values.

    The snapshot records what a consumer is entitled to branch on: the
    keys of every block, the codes and severities, and the pointer
    shapes and ``params`` keys observed for each code. Messages and
    values are deliberately absent, because they may change in any
    release.

    Pointer and ``params`` data come from the verdict corpus, so they
    are evidence rather than a declaration: a code that no case
    exercises carries empty lists.
    """
    from avefi_validate.removal import normalisation_diagnostics
    from avefi_validate.report import (
        Code,
        Diagnostic,
        FileReport,
        Removal,
        Report,
        Severity,
    )
    from avefi_validate.schema import schema_fingerprint

    empty = Report().to_dict()
    file = FileReport(path=Path(".")).to_dict()
    diagnostic = Diagnostic(Code.INTERNAL_ERROR, "").to_dict()
    removal = Removal(record="", reason=Code.REMOVED_AS_INVALID).to_dict()

    pointers = {code.value: set() for code in Code}
    params = {code.value: set() for code in Code}
    for path in sorted(CASES_DIR.glob("*.json")):
        case = json.loads(path.read_text(encoding="utf-8"))
        try:
            loaded = _load_case(case)
            result = _check_loaded(case, loaded)
        except Exception:  # noqa: BLE001 - a broken case has no surface
            continue
        for item in (
            list(loaded.diagnostics)
            + normalisation_diagnostics(loaded)
            + list(result.diagnostics)
        ):
            code = str(item.code)
            pointers.setdefault(code, set()).add(_pointer_shape(item.pointer))
            params.setdefault(code, set()).update(
                str(key) for key in item.params
            )

    return {
        "keys": sorted(empty),
        "blocks": {
            "tool": sorted(empty["tool"]),
            "report": sorted(empty["report"]),
            "schema": sorted(schema_fingerprint()),
            "file": sorted(file),
            "counts": sorted(file["counts"]),
            "diagnostic": sorted(diagnostic),
            "removal": sorted(removal),
        },
        "codes": sorted(code.value for code in Code),
        "severities": sorted(severity.value for severity in Severity),
        "pointers": {
            code: sorted(values) for code, values in sorted(pointers.items())
        },
        "params": {
            code: sorted(values) for code, values in sorted(params.items())
        },
    }


def _pointer_shape(pointer: str | None) -> str:
    """Return a pointer with concrete list indices removed."""
    if pointer is None:
        return "<none>"
    return re.sub(r"/\d+", "/*", pointer)


def classify_report(old: dict, new: dict) -> tuple[str, list[str]]:
    """Return the bump a change of the report surface requires.

    A removed key, code, severity or per-code ``params`` key breaks a
    consumer that reads it, so it is major. An added block, code or
    severity is additive and needs a minor bump.

    An added pointer shape or ``params`` key is only a note. Those come
    from the verdict corpus, which grows as cases are added; treating
    that growth as a contract change would make every new case a
    release. A *removed* pointer or key is still breaking, because it
    used to be observed and consumed.

    """
    severity = NONE
    lines: list[str] = []

    def record(level: str, line: str) -> None:
        nonlocal severity
        lines.append(line)
        severity = _worse(severity, level)

    def compare(label: str, before, after, additive: str) -> None:
        removed = sorted(set(before) - set(after))
        added = sorted(set(after) - set(before))
        if removed:
            record(MAJOR, f"{label}: removed {', '.join(removed)}")
        if added:
            record(additive, f"{label}: added {', '.join(added)}")

    compare("top level", old.get("keys", []), new.get("keys", []), MINOR)
    blocks = sorted(
        set(old.get("blocks", {})) | set(new.get("blocks", {}))
    )
    for block in blocks:
        compare(
            f"{block} block",
            old.get("blocks", {}).get(block, []),
            new.get("blocks", {}).get(block, []),
            MINOR,
        )
    compare("codes", old.get("codes", []), new.get("codes", []), MINOR)
    compare(
        "severities",
        old.get("severities", []),
        new.get("severities", []),
        MINOR,
    )
    for field, label in (("pointers", "pointer"), ("params", "params key")):
        before = old.get(field, {})
        after = new.get(field, {})
        for code in sorted(set(before) | set(after)):
            compare(
                f"{code} {label}",
                before.get(code, []),
                after.get(code, []),
                NONE,
            )
    return severity, lines


# --- public surface -----------------------------------------------------


def api_snapshot() -> dict:
    """Return the names, parameters and fields of the public surface."""
    import avefi_validate

    names = list(avefi_validate.__all__)
    if hasattr(avefi_validate, "Code"):
        names.append("Code")
    return {
        name: _describe(getattr(avefi_validate, name))
        for name in sorted(set(names))
    }


def _describe(value: Any) -> dict:
    """Return a stable description of one public name."""
    if inspect.isclass(value):
        if issubclass(value, Enum):
            return {
                "kind": "enum",
                "members": sorted(member.name for member in value),
            }
        if dataclasses.is_dataclass(value):
            return {
                "kind": "dataclass",
                "fields": [
                    [field.name, field.default is not dataclasses.MISSING]
                    for field in dataclasses.fields(value)
                ],
            }
        return {"kind": "class", "params": _params(value.__init__)}
    if callable(value):
        return {"kind": "function", "params": _params(value)}
    return {"kind": "constant", "type": type(value).__name__}


def _params(function: Any) -> list[list]:
    """Return the parameters of a callable, without ``self``."""
    params = []
    for parameter in inspect.signature(function).parameters.values():
        if parameter.name == "self":
            continue
        params.append(
            [
                parameter.name,
                parameter.kind.name,
                parameter.default is not inspect.Parameter.empty,
            ]
        )
    return params


def classify_api(old: dict, new: dict) -> tuple[str, list[str]]:
    """Return the bump a change of the public surface requires."""
    severity = NONE
    lines = []
    for name in sorted(set(old) | set(new)):
        before = old.get(name)
        after = new.get(name)
        if before == after:
            continue
        if before is None:
            lines.append(f"{name}: added")
            severity = _worse(severity, MINOR)
            continue
        if after is None:
            lines.append(f"{name}: removed")
            severity = _worse(severity, MAJOR)
            continue
        if before.get("kind") != after.get("kind"):
            lines.append(f"{name}: kind changed")
            severity = _worse(severity, MAJOR)
            continue
        verdict, detail = _classify_members(before, after)
        if verdict != NONE:
            lines.append(f"{name}: {detail}")
            severity = _worse(severity, verdict)
    return severity, lines


def _classify_members(before: dict, after: dict) -> tuple[str, str]:
    """Classify a change of a name that exists on both sides."""
    kind = before["kind"]
    if kind == "constant":
        return NONE, "same"
    if kind == "enum":
        return _classify_enum(
            before.get("members", []), after.get("members", [])
        )
    key = "fields" if kind == "dataclass" else "params"
    return _classify_sequence(before.get(key, []), after.get(key, []))


def _classify_enum(before: list, after: list) -> tuple[str, str]:
    """Adding a member widens, removing one narrows."""
    removed = sorted(set(before) - set(after))
    added = sorted(set(after) - set(before))
    if removed:
        return MAJOR, f"removed {', '.join(removed)}"
    if added:
        return MINOR, f"added {', '.join(added)}"
    return NONE, "same"


def _classify_sequence(before: list, after: list) -> tuple[str, str]:
    """Classify added, removed or reordered parameters or fields."""
    old_items = {_identity(item): item for item in before}
    new_items = {_identity(item): item for item in after}
    removed = sorted(set(old_items) - set(new_items))
    added = sorted(set(new_items) - set(old_items))
    if removed:
        return MAJOR, f"removed {', '.join(removed)}"

    for name in sorted(set(old_items) & set(new_items)):
        old_item = old_items[name]
        new_item = new_items[name]
        if _kind_of(old_item) != _kind_of(new_item):
            return MAJOR, f"{name} changed kind"
        old_default = _has_default(old_item)
        new_default = _has_default(new_item)
        if old_default and not new_default:
            return MAJOR, f"{name} lost its default"
        if new_default and not old_default:
            return MINOR, f"{name} gained a default"

    if _reordered(before, after):
        return MAJOR, "parameters reordered"

    if added:
        for name in added:
            if not _has_default(new_items[name]):
                return MAJOR, f"added required {name}"
        return MINOR, f"added {', '.join(added)}"

    return NONE, "same"


def _identity(item: Any) -> str:
    """Return a hashable identity for a member of a snapshot list."""
    if isinstance(item, str):
        return item
    return str(item[0])


def _kind_of(item: Any) -> Any:
    """Return the parameter kind of a snapshot member, if any."""
    if isinstance(item, list) and len(item) > 1:
        return item[1]
    return None


def _has_default(item: Any) -> bool:
    """Whether a snapshot member carries a default."""
    if isinstance(item, list) and item:
        return bool(item[-1])
    return False


def _reordered(before: list, after: list) -> bool:
    """Whether positional parameters appear in a different order."""
    old_names = [
        item[0]
        for item in before
        if isinstance(item, list)
        and str(item[1]).startswith("POSITIONAL")
    ]
    new_names = [
        item[0]
        for item in after
        if isinstance(item, list)
        and str(item[1]).startswith("POSITIONAL")
    ]
    shared = set(old_names) & set(new_names)
    return [n for n in old_names if n in shared] != [
        n for n in new_names if n in shared
    ]


def _worse(left: str, right: str) -> str:
    """Return the stricter of two severities."""
    return left if SEVERITY[left] >= SEVERITY[right] else right


__all__ = [
    "API_SNAPSHOT",
    "CASES_DIR",
    "REPORT_SURFACE",
    "VERDICT_SNAPSHOT",
    "api_snapshot",
    "classify_api",
    "classify_report",
    "classify_verdicts",
    "collect_verdicts",
    "load_verdicts",
    "report_surface",
    "verdict_outcome",
    "write_json",
]
