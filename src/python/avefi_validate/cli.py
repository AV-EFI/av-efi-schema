"""Command line entry point of the standalone AVefi validator.

The command checks a file and reports what it found; it says nothing
about where the records came from. Callers with a narrower workflow
can wrap it and add their own arguments on top, without this command
depending on them.

"""

import argparse
import logging
import pathlib
import sys

from .limits import DEFAULT_LIMITS, Limits
from .removal import check_file
from .schema import get_schema_validator

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
        "-v",
        "--verbose",
        action="store_true",
        help="Log debug messages, including every dependency removed.",
    )
    return parser


def _record(count: int) -> str:
    """Return ``record`` or ``records`` to match ``count``."""
    return "record" if count == 1 else "records"


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
    failed = False

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
        except OSError as e:
            failed = True
            log.error("%s: cannot read: %s", path, e)
            continue
        result = outcome.result

        if outcome.unnamed:
            failed = True
            log.error(
                "%s: %d %s name the placeholder issuer %s, so the data"
                " provider is unspecified and no persistent identifier"
                " may be registered for them",
                path,
                len(outcome.unnamed),
                _record(len(outcome.unnamed)),
                args.placeholder_issuer_id,
            )
        elif result.passed:
            log.info(
                "%s: all %d %s passed the checks successfully",
                path,
                outcome.initial_count,
                _record(outcome.initial_count),
            )
        elif args.remove_invalid:
            log.info(
                "%s: removed %d invalid %s and %d dependant %s",
                path,
                result.invalid,
                _record(result.invalid),
                result.dependants,
                _record(result.dependants),
            )
        else:
            failed = True
            log.error(
                "%s: found %d invalid %s (%d dependant %s would also be"
                " removed; no action taken)",
                path,
                result.invalid,
                _record(result.invalid),
                result.dependants,
                _record(result.dependants),
            )

    return 1 if failed else 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
