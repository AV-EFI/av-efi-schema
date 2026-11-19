"""The file-level operation behind ``--remove-invalid``.

Checking a file and repairing it are different decisions. This module
performs both, but reports what it did as data, so that the command
line entry point and programmatic callers can present the same result
in their own way.

Removal is destructive, so it happens only when explicitly asked for
and only after the whole file has been checked: a record that is
invalid because a record it depends on is invalid goes with it.

"""

from dataclasses import dataclass, field
import logging
import pathlib

from avefi_schema import model_pydantic_v2 as efi

from . import io
from .documents import pass_checks, placeholder_issuer_records
from .limits import DEFAULT_LIMITS
from .records import CheckResult
from .report import Code, FileReport

log = logging.getLogger(__name__)

#: Diagnostics that no rewrite can repair, because nothing is left to
#: write, or because the problem is not a property of a record.
UNREPAIRABLE = (Code.FILE_UNREADABLE, Code.FILE_INVALID_JSON, Code.INTERNAL_ERROR)


@dataclass
class FileCheck:
    """Outcome of checking one file.

    ``records`` is the (possibly shortened) list the check ran on,
    ``initial_count`` how many records the file held before. The file
    was rewritten only when ``rewritten`` is true. ``report`` is the
    same outcome as structured data.

    """

    path: pathlib.Path
    records: list[efi.MovingImageRecord]
    initial_count: int
    result: CheckResult
    unnamed: list[efi.MovingImageRecord] = field(default_factory=list)
    rewritten: bool = False
    report: FileReport | None = None


def check_file(
    path: pathlib.Path | str,
    *,
    schema_validator,
    remove_invalid=False,
    preserve_status_removed=False,
    placeholder_issuer_id: str | None = None,
    limits=DEFAULT_LIMITS,
) -> FileCheck:
    """Check one file, removing invalid records if asked to.

    Parameters
    ----------
    path : pathlib.Path or str
        File holding one record or a list of records.
    schema_validator
        Validator as returned by
        :func:`avefi_validate.schema.get_schema_validator`.
    remove_invalid : bool
        Rewrite the file without the invalid records and their
        dependants.
    preserve_status_removed : bool
        Accept items with access status Removed even without a PID.
    placeholder_issuer_id : str or None
        Issuer id that means "the data provider is unspecified". When
        given and a record names it, the file is not rewritten: the
        issuer is a property of the submission, not of a record that
        could be dropped.
    limits : Limits
        Field length limits to enforce.

    Returns
    -------
    FileCheck
        The records, the counts and whether the file was rewritten.

    """
    path = pathlib.Path(path)
    loaded = io.load_with_diagnostics(path)
    records = loaded.records
    initial_count = loaded.initial_count

    unnamed = (
        placeholder_issuer_records(records, placeholder_issuer_id)
        if placeholder_issuer_id
        else []
    )
    result = pass_checks(
        records,
        schema_validator,
        # A file naming no data provider is not repaired by emptying
        # it. See the comment in pass_checks().
        remove_invalid=remove_invalid and not unnamed,
        preserve_status_removed=preserve_status_removed,
        placeholder_issuer_id=placeholder_issuer_id,
        limits=limits,
    )
    diagnostics = list(loaded.diagnostics) + list(result.diagnostics)
    removals = list(result.removals)

    # A file changes when parsing dropped items or the checks removed
    # records that referred to them. ``result.invalid`` and
    # ``result.dependants`` are computed on a copy when the caller did
    # not ask for a rewrite, which is why they are consulted here rather
    # than the length of ``records``.
    changed = (
        len(records) != initial_count
        or result.invalid
        or result.dependants
    )
    rewritten = False
    if remove_invalid and not unnamed and changed:
        io.dump(records, path)
        rewritten = True
        log.info("Rewrote %s", path)

    passed = _passed(
        diagnostics=diagnostics,
        unnamed=unnamed,
        remove_invalid=remove_invalid,
        rewritten=rewritten,
        changed=changed,
    )
    report = FileReport(
        path=path,
        sha256=loaded.sha256,
        initial=initial_count,
        remaining=len(records) if rewritten else initial_count,
        invalid=result.invalid,
        dependants=result.dependants,
        passed=passed,
        rewritten=rewritten,
        diagnostics=diagnostics,
        removed=removals,
    )
    return FileCheck(
        path=path,
        records=records,
        initial_count=initial_count,
        result=result,
        unnamed=unnamed,
        rewritten=rewritten,
        report=report,
    )


def _passed(
    *,
    diagnostics,
    unnamed,
    remove_invalid,
    rewritten,
    changed,
) -> bool:
    """Return whether the file may be considered clean after the run."""
    if unnamed:
        return False
    if any(d.code in UNREPAIRABLE for d in diagnostics):
        return False
    if not diagnostics:
        return True
    if not remove_invalid:
        return False
    # A rewrite is what turns failing data into a passing file. If
    # nothing had to change, there was no problem to repair.
    return rewritten or not changed
