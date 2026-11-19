"""Reading and writing AVefi records.

This is the generic JSON I/O of the AVefi record format: it knows
nothing about conversion and nothing about the checks.

"""

from dataclasses import dataclass, field
import hashlib
import json
import os
import pathlib
import tempfile

from avefi_schema import model_pydantic_v2 as efi
from pydantic import ValidationError

from .report import Code, Diagnostic

ENCODING = "utf-8"


@dataclass
class LoadResult:
    """What could be read from a file, and what could not.

    ``initial_count`` is the number of items in the JSON document,
    including items that failed validation. ``diagnostics`` explains
    every item that was skipped and any reason the file could not be
    read at all.

    """

    records: list[efi.MovingImageRecord] = field(default_factory=list)
    initial_count: int = 0
    diagnostics: list[Diagnostic] = field(default_factory=list)
    sha256: str | None = None


def load_with_diagnostics(source: pathlib.Path | str) -> LoadResult:
    """Load AVefi records, keeping as much of the file as possible.

    ``load`` raises on the first problem, which is right for a caller
    that needs all-or-nothing parsing. A validator is the opposite: one
    unparseable record among ten thousand should cost that record, not
    the file, and an unreadable file should not stop the next one.

    A file that cannot be read or is not JSON yields no records and one
    file-level diagnostic. A list is parsed item by item; each item that
    pydantic rejects becomes a ``record.unparseable`` diagnostic and is
    skipped. A JSON object is treated as a single record.
    """
    path = pathlib.Path(source)
    try:
        raw = path.read_bytes()
    except OSError as exc:
        return LoadResult(
            diagnostics=[
                Diagnostic(
                    code=Code.FILE_UNREADABLE,
                    message=f"cannot read: {exc}",
                    params={"error": type(exc).__name__},
                )
            ]
        )
    digest = hashlib.sha256(raw).hexdigest()
    try:
        text = raw.decode(ENCODING)
    except UnicodeDecodeError as exc:
        return LoadResult(
            diagnostics=[
                Diagnostic(
                    code=Code.FILE_UNREADABLE,
                    message=f"cannot decode as {ENCODING}: {exc}",
                    params={"error": type(exc).__name__},
                )
            ],
            sha256=digest,
        )
    result = loads_with_diagnostics(text)
    result.sha256 = digest
    return result


def loads_with_diagnostics(input: str) -> LoadResult:
    """Load AVefi records from a JSON string, keeping every usable item.

    This is the per-item counterpart of :func:`loads`. It never raises
    for malformed input; the reason is returned as a diagnostic.
    """
    try:
        document = json.loads(input)
    except json.JSONDecodeError as exc:
        return LoadResult(
            diagnostics=[
                Diagnostic(
                    code=Code.FILE_INVALID_JSON,
                    message=f"invalid JSON: {exc.msg}",
                    params={
                        "line": exc.lineno,
                        "column": exc.colno,
                        "position": exc.pos,
                    },
                )
            ]
        )

    items = document if isinstance(document, list) else [document]
    records = []
    diagnostics = []
    for index, item in enumerate(items):
        try:
            records.append(
                efi.MovingImageRecordTypeAdapter.validate_python(item)
            )
        except ValidationError as exc:
            diagnostics.append(
                Diagnostic(
                    code=Code.RECORD_UNPARSEABLE,
                    message=_first_error_message(exc),
                    record=f"item[{index}]",
                    params={
                        "index": index,
                        "errors": _error_summaries(exc),
                    },
                )
            )
        except Exception as exc:  # noqa: BLE001 - one item must not abort
            diagnostics.append(
                Diagnostic(
                    code=Code.RECORD_UNPARSEABLE,
                    message=f"cannot parse record: {exc}",
                    record=f"item[{index}]",
                    params={
                        "index": index,
                        "errors": [{"type": type(exc).__name__}],
                    },
                )
            )
    return LoadResult(
        records=records,
        initial_count=len(items),
        diagnostics=diagnostics,
    )


def _first_error_message(exc: ValidationError) -> str:
    """Return the first pydantic message, with its location."""
    errors = exc.errors(include_url=False)
    if not errors:
        return "record does not match the AVefi model"
    first = errors[0]
    location = ".".join(str(part) for part in first.get("loc", ()))
    message = first.get("msg", "record does not match the AVefi model")
    return f"{location}: {message}" if location else message


def _error_summaries(exc: ValidationError) -> list[dict]:
    """Return the stable part of pydantic's error records.

    Exception objects and input values are left out: they are not
    JSON-compatible and they are not needed to act on the report.
    """
    summaries = []
    for error in exc.errors(include_url=False):
        summaries.append(
            {
                "loc": [str(part) for part in error.get("loc", ())],
                "type": error.get("type"),
                "msg": error.get("msg"),
            }
        )
    return summaries


def load(source: pathlib.Path | str) -> list[efi.MovingImageRecord]:
    """Load AVefi records from file."""
    with pathlib.Path(source).open(encoding=ENCODING) as f:
        input = f.read()
    return loads(input)


def loads(input: str) -> list[efi.MovingImageRecord]:
    """Load AVefi records from JSON string."""
    try:
        container = efi.MovingImageRecords.model_validate_json(input)
        return container.root
    except ValidationError as e:
        err0 = e.errors()[0]
        if err0.get("loc") == () and err0.get("type") == "list_type":
            record = efi.MovingImageRecordTypeAdapter.validate_json(input)
            return [record]
        raise


def dump(records: list[efi.MovingImageRecord], to_file: str):
    """Dump AVefi records to JSON file.

    The file is written atomically: output goes to a temporary file in
    the same directory which is then moved into place. An interrupted
    or failing write therefore cannot truncate an existing file.

    """
    target = pathlib.Path(to_file)
    fd, tmp_name = tempfile.mkstemp(
        dir=target.parent or pathlib.Path(),
        prefix=f".{target.name}.",
        suffix=".tmp",
    )
    try:
        with os.fdopen(fd, "w", encoding=ENCODING) as f:
            f.write(dumps(records, indent=2))
        os.replace(tmp_name, target)
    except BaseException:
        pathlib.Path(tmp_name).unlink(missing_ok=True)
        raise


#: Order in which record categories are emitted by sort_records().
CATEGORY_ORDER = ("avefi:WorkVariant", "avefi:Manifestation", "avefi:Item")


def sort_records(
    records: list[efi.MovingImageRecord],
) -> list[efi.MovingImageRecord]:
    """Return ``records`` in a stable, reproducible order.

    Converting the same input twice should yield byte identical
    output, which requires an order that does not depend on dictionary
    iteration or on the order in which input files happen to be read.
    Records are grouped by category, parents before children, and
    sorted by their identifiers within a group.

    """

    def key(record):
        try:
            category_rank = CATEGORY_ORDER.index(record.category)
        except ValueError:
            category_rank = len(CATEGORY_ORDER)
        identifiers = sorted(
            identifier.id for identifier in record.has_identifier or []
        )
        return (category_rank, identifiers, str(record.category))

    return sorted(records, key=key)


def dumps(records: list[efi.MovingImageRecord], indent=None) -> str:
    """Dump AVefi records to string (in JSON format)."""
    container = efi.MovingImageRecords(records)
    return container.model_dump_json(exclude_none=True, indent=indent)
