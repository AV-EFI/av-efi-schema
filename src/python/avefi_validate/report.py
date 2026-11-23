"""Structured description of what a validation run found.

The command line has always turned failures into log lines. That is
useful to a person reading a terminal, but a caller that wants to act on
the result -- drop the bad records, route them to a review queue, count
them per code -- needs the same information as data.

Two representations are produced from one analysis:

``message``
    A sentence for a person. It may change in any release.
``code``, ``record``, ``pointer`` and the keys of ``params``
    The programmatic contract. A code keeps its meaning and its
    ``params`` keys for the life of its major version.

The distinction is what makes the report usable: a consumer branches on
``Code.FIELD_TOO_LONG`` and reads ``params["limit"]``, never on the
wording. See ``src/docs/versioning.md``.

"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Any, Mapping


class Severity(StrEnum):
    """How much a diagnostic matters."""

    ERROR = "error"
    WARNING = "warning"


class Code(StrEnum):
    """Stable identifiers for everything a run can report.

    Adding a code is an additive change; removing or renaming one
    breaks consumers that branch on it.

    """

    # The file as a whole.
    FILE_UNREADABLE = "file.unreadable"
    FILE_INVALID_JSON = "file.invalid_json"
    RECORD_UNPARSEABLE = "record.unparseable"

    # One record, against the schema and the submission rules.
    SCHEMA_VIOLATION = "schema.violation"
    VALUE_NORMALISED = "value.normalised"
    MISSING_IDENTIFIER = "record.missing_identifier"
    DUPLICATE_IDENTIFIER = "identifier.duplicate"
    FIELD_TOO_LONG = "field.too_long"
    DATE_INVALID = "date.invalid"
    DATE_PERIOD_ORDER = "date.period_order"
    NAME_EMPTY = "name.empty"
    TITLE_PRIMARY_TYPE = "title.primary_type"
    REMOVED_WITHOUT_PID = "access_status.removed_without_pid"

    # Relations between records.
    REFERENCE_UNRESOLVED = "reference.unresolved"
    REFERENCE_CYCLE = "reference.cycle"
    RECORD_DANGLING = "record.dangling"
    ANALYTIC_REFERENCED = "analytic.referenced_by_manifestation"
    ANALYTIC_WITHOUT_PARENT = "analytic.without_parent"
    ANALYTIC_PARENT_WITHOUT_ITEMS = "analytic.parent_without_items"

    # Submission convention rather than a property of one record.
    ISSUER_PLACEHOLDER = "issuer.placeholder"

    # The validator itself could not finish a record.
    INTERNAL_ERROR = "internal.error"

    # Why a record left the working set. ``REMOVED_AS_DEPENDANT`` is
    # also the diagnostic for a record that no longer has valid
    # dependants but was referred to by records that were rejected.
    REMOVED_AS_INVALID = "record.invalid"
    REMOVED_AS_DEPENDANT = "record.depends_on_invalid"


#: Name used in the ``tool`` block of a report document.
TOOL_NAME = "avefi-validate"

#: Version of the report document's own contract.
#:
#: This is independent of the schema version and of the package version.
#: It moves when the shape of the document or the meaning of a code,
#: pointer or ``params`` key changes, and never otherwise. Clients read
#: it from ``report.version`` and do not have to map package versions.
REPORT_CONTRACT_VERSION = "1.1"


def _jsonable(value: Any) -> Any:
    """Return ``value`` in a form ``json.dumps`` accepts.

    Diagnostic parameters are chosen by the validator, so they should
    already be plain data. This is a guard against an exception object
    or a set finding its way into a report: the report must always be
    writable.
    """
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    if isinstance(value, StrEnum):
        return value.value
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set, frozenset)):
        return [_jsonable(item) for item in value]
    return str(value)


def record_label(record: Any) -> str:
    """Return the stable label of a record for a diagnostic.

    The identifier is part of the label because a file may hold several
    records of one category. A record without an identifier -- which is
    itself reportable -- falls back to its class name.
    """
    name = type(record).__name__
    identifiers = getattr(record, "has_identifier", None) or []
    for identifier in identifiers:
        value = getattr(identifier, "id", None)
        if value:
            return f"{name}.{value}"
    return name


@dataclass(frozen=True)
class Diagnostic:
    """One finding: what is wrong, where, and with which parameters.

    ``record`` is the label of the record the finding belongs to, or
    ``None`` for a file-level finding. ``pointer`` is an RFC 6901 JSON
    pointer into that record, or ``None`` when no single field is at
    fault.
    """

    code: Code
    message: str
    severity: Severity = Severity.ERROR
    record: str | None = None
    pointer: str | None = None
    params: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Return the diagnostic as JSON-compatible data."""
        return {
            "code": str(self.code),
            "severity": str(self.severity),
            "record": self.record,
            "pointer": self.pointer,
            "params": {
                str(key): _jsonable(value)
                for key, value in self.params.items()
            },
            "message": self.message,
        }


@dataclass(frozen=True)
class Removal:
    """A record that left the working set, and why."""

    record: str
    reason: Code
    because: str | None = None

    def to_dict(self) -> dict:
        """Return the removal as JSON-compatible data."""
        return {
            "record": self.record,
            "reason": str(self.reason),
            "because": self.because,
        }


@dataclass
class FileReport:
    """Everything a run found in one file.

    ``initial`` counts the items in the file as read, including items
    that could not be parsed. ``remaining`` is how many records the file
    holds afterwards: equal to ``initial`` unless the file was
    rewritten. ``invalid`` and ``dependants`` separate records that
    failed their own checks from records removed only because something
    they refer to failed.
    """

    path: Path
    sha256: str | None = None
    initial: int = 0
    remaining: int = 0
    invalid: int = 0
    dependants: int = 0
    passed: bool = True
    rewritten: bool = False
    diagnostics: list[Diagnostic] = field(default_factory=list)
    removed: list[Removal] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Return the file report as JSON-compatible data."""
        return {
            "path": str(self.path),
            "sha256": self.sha256,
            "counts": {
                "initial": self.initial,
                "remaining": self.remaining,
                "invalid": self.invalid,
                "dependants": self.dependants,
            },
            "passed": self.passed,
            "rewritten": self.rewritten,
            "diagnostics": [
                diagnostic.to_dict() for diagnostic in self.diagnostics
            ],
            "removed": [removal.to_dict() for removal in self.removed],
        }


@dataclass
class Report:
    """The outcome of a whole run, over every file it was given."""

    package: str | None = None
    schema: dict = field(default_factory=dict)
    files: list[FileReport] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        """Whether every file passed or was repaired."""
        return all(file.passed for file in self.files)

    @property
    def exit_code(self) -> int:
        """Return the process exit code the run calls for."""
        return 0 if self.passed else 1

    def to_dict(self) -> dict:
        """Return the run report as JSON-compatible data."""
        return {
            "tool": {"name": TOOL_NAME, "package": self.package},
            "report": {"version": REPORT_CONTRACT_VERSION},
            "schema": dict(self.schema),
            "files": [file.to_dict() for file in self.files],
            "passed": self.passed,
        }


__all__ = [
    "Code",
    "Diagnostic",
    "FileReport",
    "REPORT_CONTRACT_VERSION",
    "Removal",
    "Report",
    "Severity",
]
