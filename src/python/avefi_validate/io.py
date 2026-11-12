"""Reading and writing AVefi records.

This is the generic JSON I/O of the AVefi record format: it knows
nothing about conversion and nothing about the checks.

"""

import os
import pathlib
import tempfile

from avefi_schema import model_pydantic_v2 as efi
from pydantic import ValidationError

ENCODING = "utf-8"


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
