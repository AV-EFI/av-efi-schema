"""Command line entry point of the standalone AVefi validator.

The command checks a file and reports what it found; it says nothing
about where the records came from. Callers with a narrower workflow
can wrap it and add their own arguments on top, without this command
depending on them.

Two renderings share one analysis. The default writes readable lines to
stderr, exactly like the command always did. ``--format json`` writes
the same result as one JSON document to stdout, for a caller that wants
to act on the outcome. ``--report PATH`` writes the JSON document
without changing the human output.

"""

import argparse
import json
import logging
import pathlib
import sys

from .limits import DEFAULT_LIMITS, Limits
from .removal import check_file
from .schema import get_schema_validator, schema_fingerprint
from .report import Code, Diagnostic, FileReport, Report, Severity

log = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    """Return the argument parser of ``avefi-validate``."""
    parser = argparse.ArgumentParser(
        prog="avefi-validate",
        description=(
            "Validate AVefi records against the schema of the installed"
            " avefi-schema package."
        ),
    )
    parser.add_argument(
        "files",
        nargs="+",
        type=pathlib.Path,
        help="JSON file holding an AVefi record or a list of records.",
    )
    parser.add_argument(
        "-r",
        "--remove-invalid",
        action="store_true",
        help="Rewrite the file without invalid records and their dependants.",
    )
    parser.add_argument(
        "--preserve-status-removed",
        action="store_true",
        help=(
            "Accept items with access status Removed even without a PID"
            " yet."
        ),
    )
    parser.add_argument(
        "--placeholder-issuer-id",
        default=None,
        metavar="ISSUER_ID",
        help=(
            "Also reject records whose described_by names this issuer id,"
            " e.g. https://w3id.org/avefi/issuer/unspecified."
        ),
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=DEFAULT_LIMITS.line_limit,
        metavar="CHARS",
        help="Maximum length of a title line (default: %(default)s).",
    )
    parser.add_argument(
        "--text-limit",
        type=int,
        default=DEFAULT_LIMITS.text_limit,
        metavar="CHARS",
        help="Maximum length of a note (default: %(default)s).",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help=(
            "How to render the result. 'json' writes one document to"
            " stdout; human-readable lines stay on stderr (default:"
            " text)."
        ),
    )
    parser.add_argument(
        "--report",
        type=pathlib.Path,
        default=None,
        metavar="PATH",
        help=(
            "Write the JSON report to PATH ('-' for stdout). Independent"
            " of --format."
        ),
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help=(
            "Log debug messages, including every dependency removed, and"
            " show diagnostic codes in the text output."
        ),
    )
    return parser


def _record(count: int) -> str:
    """Return ``record`` or ``records`` to match ``count``."""
    return "record" if count == 1 else "records"


def _log_diagnostics(report: FileReport, verbose: bool) -> None:
    """Write one line per finding to the log."""
    for diagnostic in report.diagnostics:
        where = ""
        if diagnostic.record:
            where = f": {diagnostic.record}"
            if diagnostic.pointer:
                where += f" at {diagnostic.pointer}"
        suffix = f" [{diagnostic.code}]" if verbose else ""
        message = f"{report.path}{where}: {diagnostic.message}{suffix}"
        if diagnostic.severity == Severity.ERROR:
            log.error(message)
        else:
            log.warning(message)


def _unparseable(report: FileReport) -> int:
    """Return how many items of ``report`` could not be parsed."""
    return sum(
        1
        for diagnostic in report.diagnostics
        if diagnostic.code == Code.RECORD_UNPARSEABLE
    )


def _log_summary(outcome, args) -> None:
    """Write the one-line summary users of the command rely on."""
    report = outcome.report
    result = outcome.result
    if outcome.unnamed:
        log.error(
            "%s: %d %s name the placeholder issuer %s, so the data"
            " provider is unspecified and no persistent identifier"
            " may be registered for them",
            report.path,
            len(outcome.unnamed),
            _record(len(outcome.unnamed)),
            args.placeholder_issuer_id,
        )
        return
    if any(
        diagnostic.code
        in (
            Code.FILE_UNREADABLE,
            Code.FILE_INVALID_JSON,
            Code.INTERNAL_ERROR,
        )
        for diagnostic in report.diagnostics
    ):
        # The diagnostic line already says what happened; a count of
        # invalid records would only be misleading.
        return
    if report.passed:
        unparseable = _unparseable(report)
        if (
            args.remove_invalid
            and unparseable
            and not result.invalid
            and not result.dependants
        ):
            log.info(
                "%s: removed %d unparseable %s",
                report.path,
                unparseable,
                _record(unparseable),
            )
        elif args.remove_invalid and (
            result.invalid or result.dependants or report.rewritten
        ):
            log.info(
                "%s: removed %d invalid %s and %d dependant %s",
                report.path,
                result.invalid,
                _record(result.invalid),
                result.dependants,
                _record(result.dependants),
            )
        else:
            log.info(
                "%s: all %d %s passed the checks successfully",
                report.path,
                report.initial,
                _record(report.initial),
            )
        return
    unparseable = _unparseable(report)
    if unparseable and not result.invalid and not result.dependants:
        log.error(
            "%s: %d %s could not be parsed and were not checked",
            report.path,
            unparseable,
            _record(unparseable),
        )
        return
    log.error(
        "%s: found %d invalid %s (%d dependant %s would also be"
        " removed; no action taken)",
        report.path,
        result.invalid,
        _record(result.invalid),
        result.dependants,
        _record(result.dependants),
    )


def _internal_report(path: pathlib.Path, exc: BaseException) -> FileReport:
    """Return a report for a file whose check raised unexpectedly."""
    return FileReport(
        path=path,
        passed=False,
        diagnostics=[
            Diagnostic(
                code=Code.INTERNAL_ERROR,
                message=f"unexpected error: {exc}",
                params={"error": type(exc).__name__},
            )
        ],
    )


def _write_json(report: Report, target: pathlib.Path) -> None:
    """Write ``report`` as one JSON document to ``target`` or stdout."""
    text = json.dumps(report.to_dict(), indent=2, ensure_ascii=False) + "\n"
    if str(target) == "-":
        sys.stdout.write(text)
    else:
        target.write_text(text, encoding="utf-8")


def main(argv=None) -> int:
    """Run the validator and return the process exit code."""
    args = build_parser().parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(name)s: %(message)s",
        stream=sys.stderr,
    )

    limits = Limits(line_limit=args.limit, text_limit=args.text_limit)
    schema_validator = get_schema_validator()
    schema = schema_fingerprint()
    files = []

    for path in args.files:
        log.info("Processing %s", path)
        try:
            outcome = check_file(
                path,
                schema_validator=schema_validator,
                remove_invalid=args.remove_invalid,
                preserve_status_removed=args.preserve_status_removed,
                placeholder_issuer_id=args.placeholder_issuer_id,
                limits=limits,
            )
        except Exception as exc:  # noqa: BLE001 - one file must not abort
            report = _internal_report(path, exc)
            files.append(report)
            _log_diagnostics(report, args.verbose)
            log.error("%s: %s", path, report.diagnostics[0].message)
            continue
        files.append(outcome.report)
        _log_diagnostics(outcome.report, args.verbose)
        _log_summary(outcome, args)

    report = Report(
        package=schema.get("package"),
        schema=schema,
        files=files,
    )
    destination = args.report
    if destination is None and args.format == "json":
        destination = pathlib.Path("-")
    if destination is not None:
        try:
            _write_json(report, destination)
        except OSError as exc:
            log.error("cannot write report %s: %s", destination, exc)
            return 1
    return report.exit_code


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
