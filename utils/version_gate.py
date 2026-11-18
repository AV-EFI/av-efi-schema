"""Fail when a change and a version bump disagree.

The repository publishes one artefact that carries three contracts: the
data contract (the JSON Schema in ``src/avefi_schema``), the acceptance
rules (``src/python/avefi_validate``) and the public surface of the
validator. A version number is only useful if it moves when any of them
changes in a way a consumer would notice, so this module compares the
working tree with a base revision and checks that the numbers tell the
truth.

The rules are:

====  ====================================================================
R1    versions parse, the schema version is ``MAJOR.MINOR``
R2    neither version decreases
R3    a schema change moves the schema version by the required amount
R3b   a schema version moved without a schema change
R4    a schema change also moves the package version
R5    retired: the schema and package versions are independent
R6    a change of validator outcomes moves the package version
R7    any change to the schema or the validator moves at least the patch
R8    a change of the public surface moves the package version
R9    the changelog has a section for the new version
R10   inconclusive changes have a reviewed entry in ``decisions.toml``
====  ====================================================================

R5 was retired when the schema version was re-based to ``2.0``: the
schema tracks the public data contract, the package tracks the
artefact, and neither number bounds the other. A schema major may
therefore exceed the package major (schema ``2.0`` in package
``0.3.0``).

Run it with ``doit version_check``. It needs git history, so it is a CI
and pre-push tool, never something an installed distribution does.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from tomllib import loads as toml_loads

from . import version_contract as contract
from . import version_snapshots as snapshots

ROOT = Path(__file__).resolve().parent.parent

MODEL_YAML = "src/avefi_schema/model.yaml"
PYPROJECT = "pyproject.toml"
JSON_SCHEMA = "project/jsonschema/avefi_schema/model.schema.json"
VERDICTS = "tests/data/version_contract/expected.json"
API = "tests/data/api_surface.json"
CHANGELOG = "CHANGELOG.md"
DECISIONS = "versioning/decisions.toml"

#: Where the two contracts live, for R7.
WATCHED_PREFIXES = ("src/avefi_schema/", "src/python/avefi_validate/")

#: Full release versions accepted in ``pyproject.toml``.
PACKAGE_VERSION_RE = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:[-+][0-9A-Za-z.-]+)?$"
)


@dataclass(frozen=True)
class Snapshot:
    """What the gate needs to know about one revision."""

    schema_version: str | None = None
    package_version: str | None = None
    schema: dict = field(default_factory=dict)
    verdicts: dict = field(default_factory=dict)
    api: dict = field(default_factory=dict)
    paths: frozenset[str] = frozenset()
    changelog: str = ""


@dataclass(frozen=True)
class Decision:
    """A reviewed classification of an inconclusive change."""

    schema_version: str
    path: str
    reviewed: str
    reason: str = ""


@dataclass
class Report:
    """The outcome of a comparison."""

    problems: list[tuple[str, str]] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    old: Snapshot = field(default_factory=Snapshot)
    new: Snapshot = field(default_factory=Snapshot)

    @property
    def ok(self) -> bool:
        """Whether every rule holds."""
        return not self.problems

    def lines(self) -> list[str]:
        """Return a readable report."""
        rendered = [
            f"schema:  {self.old.schema_version} -> "
            f"{self.new.schema_version}",
            f"package: {self.old.package_version} -> "
            f"{self.new.package_version}",
        ]
        rendered.extend(f"note: {note}" for note in self.notes)
        if self.ok:
            rendered.append("ok: versions agree with the changes")
        else:
            rendered.extend(
                f"FAIL {rule}: {message}"
                for rule, message in self.problems
            )
        return rendered


def evaluate(
    old: Snapshot,
    new: Snapshot,
    decisions: list[Decision] | None = None,
) -> Report:
    """Compare two snapshots and return everything that disagrees."""
    decisions = decisions or []
    report = Report(old=old, new=new)

    _check_versions(old, new, report)
    bootstrap = not old.schema_version or not old.package_version
    if bootstrap:
        report.notes.append(
            "base revision carries no versions yet: bump checks skipped"
        )
        return report

    _check_schema(old, new, decisions, report)
    _check_package_moves_with_schema(old, new, report)
    _check_verdicts(old, new, report)
    _check_api(old, new, report)
    _check_watched_paths(old, new, report)
    _check_changelog(old, new, report)
    return report


def _check_versions(old: Snapshot, new: Snapshot, report: Report) -> None:
    """R1 and R2."""
    if not contract.SCHEMA_VERSION_RE.match(new.schema_version or ""):
        report.problems.append(
            (
                "R1",
                f"schema version {new.schema_version!r} in {MODEL_YAML}"
                " is not a quoted MAJOR.MINOR string",
            )
        )
    if not PACKAGE_VERSION_RE.match(new.package_version or ""):
        report.problems.append(
            (
                "R1",
                f"package version {new.package_version!r} is not a release",
            )
        )
    for label, before, after in (
        ("schema", old.schema_version, new.schema_version),
        ("package", old.package_version, new.package_version),
    ):
        if not before or not after:
            continue
        if contract.bump_satisfied(after, before, contract.PATCH):
            report.problems.append(
                ("R2", f"{label} version decreased: {before} -> {after}")
            )


def _check_schema(
    old: Snapshot,
    new: Snapshot,
    decisions: list[Decision],
    report: Report,
) -> None:
    """R3, R3b and R10."""
    verdict = contract.classify(old.schema, new.schema)
    severity, unresolved = _apply_decisions(
        verdict, new.schema_version, decisions
    )
    report.notes.extend(verdict.lines())

    if unresolved:
        report.problems.append(
            (
                "R10",
                "inconclusive schema changes need a reviewed entry in "
                f"{DECISIONS}: "
                + ", ".join(change.path for change in unresolved),
            )
        )

    required = contract.required_schema_bump(
        severity, _major(old.schema_version)
    )
    if required == contract.NONE:
        if new.schema_version != old.schema_version:
            report.problems.append(
                (
                    "R3b",
                    "schema version changed but the schema did not;"
                    " do not move it for validator-only work",
                )
            )
        return

    if new.schema_version == old.schema_version:
        report.problems.append(
            (
                "R3",
                f"schema changed ({severity}) but the version in"
                f" {MODEL_YAML} stayed at {new.schema_version}",
            )
        )
    elif not contract.bump_satisfied(
        old.schema_version, new.schema_version, required
    ):
        report.problems.append(
            (
                "R3",
                f"schema change needs a {required} bump;"
                f" {old.schema_version} -> {new.schema_version} is not"
                " enough",
            )
        )


def _apply_decisions(
    verdict: contract.Verdict,
    schema_version: str | None,
    decisions: list[Decision],
) -> tuple[str, list[contract.Change]]:
    """Resolve inconclusive changes through reviewed decisions."""
    severity = verdict.severity
    unresolved = []
    for change in verdict.inconclusive:
        decision = _find_decision(decisions, change.path, schema_version)
        if decision is None:
            unresolved.append(change)
            continue
        severity = _stricter(severity, decision.reviewed)
    return severity, unresolved


def _find_decision(
    decisions: list[Decision],
    path: str,
    schema_version: str | None,
) -> Decision | None:
    """Return the decision covering ``path`` for this release."""
    for decision in decisions:
        if decision.path == path and (
            decision.schema_version == schema_version
        ):
            return decision
    return None


def _check_package_moves_with_schema(
    old: Snapshot, new: Snapshot, report: Report
) -> None:
    """R4: a schema release is an artefact release."""
    if new.schema_version == old.schema_version:
        return
    if new.package_version == old.package_version:
        report.problems.append(
            (
                "R4",
                "the schema version moved, so the package version must"
                " move in the same release",
            )
        )


def _check_verdicts(old: Snapshot, new: Snapshot, report: Report) -> None:
    """R6."""
    if old.verdicts == new.verdicts:
        return
    severity, lines = snapshots.classify_verdicts(
        old.verdicts, new.verdicts
    )
    report.notes.extend(f"validator: {line}" for line in lines)
    required = _package_bump(severity, _major(old.package_version))
    if contract.bump_satisfied(
        old.package_version, new.package_version, required
    ):
        return
    report.problems.append(
        (
            "R6",
            "validator outcomes changed"
            f" ({', '.join(lines) or severity}), so the package needs a"
            f" {required} bump; it went {old.package_version} ->"
            f" {new.package_version}",
        )
    )


def _check_api(old: Snapshot, new: Snapshot, report: Report) -> None:
    """R8."""
    if old.api == new.api:
        return
    severity, lines = snapshots.classify_api(old.api, new.api)
    report.notes.extend(f"surface: {line}" for line in lines)
    required = _package_bump(severity, _major(old.package_version))
    if contract.bump_satisfied(
        old.package_version, new.package_version, required
    ):
        return
    report.problems.append(
        (
            "R8",
            "the public surface changed"
            f" ({', '.join(lines) or severity}), so the package needs a"
            f" {required} bump; it went {old.package_version} ->"
            f" {new.package_version}",
        )
    )


def _check_watched_paths(
    old: Snapshot, new: Snapshot, report: Report
) -> None:
    """R7: nothing under the two contracts changes silently."""
    touched = sorted(
        path
        for path in new.paths
        if path.startswith(WATCHED_PREFIXES)
    )
    if not touched:
        return
    if contract.bump_satisfied(
        old.package_version, new.package_version, contract.PATCH
    ):
        return
    report.problems.append(
        (
            "R7",
            "changed under the schema or the validator"
            f" ({', '.join(touched[:5])}{'…' if len(touched) > 5 else ''})"
            " but the package version did not move",
        )
    )


def _check_changelog(old: Snapshot, new: Snapshot, report: Report) -> None:
    """R9."""
    if new.package_version == old.package_version:
        return
    section = _changelog_section(new.changelog, new.package_version)
    if section is None:
        report.problems.append(
            (
                "R9",
                f"{CHANGELOG} has no section for {new.package_version}",
            )
        )
        return
    for label in ("Schema:", "Validator:"):
        if not _has_line(section, label):
            report.problems.append(
                (
                    "R9",
                    f"the {new.package_version} section in {CHANGELOG}"
                    f" needs a {label} line",
                )
            )
    schema_line = _line_starting_with(section, "Schema:")
    if (
        schema_line is not None
        and new.schema_version
        and new.schema_version not in schema_line
    ):
        report.problems.append(
            (
                "R9",
                f"the {new.package_version} section names a schema"
                f" version other than {new.schema_version}",
            )
        )


def _changelog_section(text: str, version: str) -> str | None:
    """Return the section body of ``version`` in a changelog."""
    pattern = re.compile(
        r"(?m)^##\s+" + re.escape(version) + r"\s*$"
    )
    match = pattern.search(text)
    if not match:
        return None
    rest = text[match.end():]
    following = re.search(r"(?m)^##\s+", rest)
    return rest[: following.start()] if following else rest


def _has_line(section: str, prefix: str) -> bool:
    """Whether a section carries a line starting with ``prefix``."""
    return _line_starting_with(section, prefix) is not None


def _line_starting_with(section: str, prefix: str) -> str | None:
    """Return the first line of a section starting with ``prefix``."""
    for line in section.splitlines():
        if line.strip().startswith(prefix):
            return line.strip()
    return None


def _package_bump(severity: str, major: int) -> str:
    """Map a verdict to the package component that has to move."""
    if severity == contract.NONE:
        return contract.NONE
    if severity == contract.PATCH:
        return contract.PATCH
    if severity == contract.MINOR:
        return contract.MINOR
    return contract.MAJOR if major >= 1 else contract.MINOR


def _stricter(left: str, right: str) -> str:
    """Return the stricter of two severities."""
    order = contract.SEVERITY
    if left not in order:
        return right
    if right not in order:
        return left
    return left if order[left] >= order[right] else right


def _major(version: str | None) -> int:
    """Return the major component of a version, or zero."""
    parts = _major_minor(version)
    return parts[0] if parts else 0


def _major_minor(version: str | None) -> tuple[int, int] | None:
    """Return the ``MAJOR.MINOR`` of a version."""
    match = re.match(
        r"^(0|[1-9]\d*)\.(0|[1-9]\d*)", str(version or "")
    )
    if not match:
        return None
    return int(match.group(1)), int(match.group(2))


# --- reading revisions --------------------------------------------------

_SCHEMA_VERSION_RE = re.compile(
    r"""(?m)^version:\s*["']?([^"'\s#]+)"""
)


def read_schema_version(text: str) -> str | None:
    """Return the top-level ``version`` of a LinkML schema document."""
    match = _SCHEMA_VERSION_RE.search(text)
    return match.group(1) if match else None


def read_package_version(text: str) -> str | None:
    """Return ``[project].version`` from a pyproject document."""
    try:
        return toml_loads(text)["project"]["version"]
    except (KeyError, ValueError):
        return _project_version_by_line(text)


def _project_version_by_line(text: str) -> str | None:
    """Read the version without a TOML parser, for old interpreters."""
    in_project = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("["):
            in_project = stripped == "[project]"
            continue
        if in_project:
            match = re.match(r'version\s*=\s*"([^"]+)"', stripped)
            if match:
                return match.group(1)
    return None


def load_decisions(path: Path | None = None) -> list[Decision]:
    """Return the reviewed classifications, if the file exists."""
    path = path or Path(ROOT, DECISIONS)
    if not path.exists():
        return []
    data = toml_loads(path.read_text(encoding="utf-8"))
    return [Decision(**entry) for entry in data.get("change", [])]


def _read_working_tree(path: str) -> str:
    """Return a file of the working tree, or an empty string."""
    full = Path(ROOT, path)
    return full.read_text(encoding="utf-8") if full.exists() else ""


def _read_git(revision: str, path: str) -> str:
    """Return a file of a revision, or an empty string."""
    try:
        return _git("show", f"{revision}:{path}")
    except subprocess.CalledProcessError:
        return ""


def _git(*args: str) -> str:
    """Run git and return stdout."""
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def _json(text: str, default):
    """Parse JSON text, falling back to a default."""
    if not text.strip():
        return default
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return default


def load_working_tree() -> Snapshot:
    """Read the versions and snapshots of the working tree."""
    return Snapshot(
        schema_version=read_schema_version(_read_working_tree(MODEL_YAML)),
        package_version=read_package_version(_read_working_tree(PYPROJECT)),
        schema=_json(_read_working_tree(JSON_SCHEMA), {}),
        verdicts=_json(_read_working_tree(VERDICTS), {}),
        api=_json(_read_working_tree(API), {}),
        paths=frozenset(),
        changelog=_read_working_tree(CHANGELOG),
    )


def load_revision(revision: str) -> Snapshot:
    """Read the versions and snapshots of a git revision."""
    return Snapshot(
        schema_version=read_schema_version(_read_git(revision, MODEL_YAML)),
        package_version=read_package_version(_read_git(revision, PYPROJECT)),
        schema=_json(_read_git(revision, JSON_SCHEMA), {}),
        verdicts=_json(_read_git(revision, VERDICTS), {}),
        api=_json(_read_git(revision, API), {}),
        paths=frozenset(),
        changelog=_read_git(revision, CHANGELOG),
    )


def changed_paths(base: str) -> frozenset[str]:
    """Return the paths that differ between ``base`` and the tree."""
    try:
        merge_base = _git("merge-base", base, "HEAD").strip()
    except subprocess.CalledProcessError:
        merge_base = base
    output = _git("diff", "--name-only", merge_base)
    return frozenset(line for line in output.splitlines() if line)


def main(argv: list[str] | None = None) -> int:
    """Run the gate and return a process exit code."""
    parser = argparse.ArgumentParser(
        prog="version_check",
        description=(
            "Check that the schema and package versions agree with the"
            " changes since a base revision."
        ),
    )
    parser.add_argument(
        "--base",
        default=None,
        help=(
            "Revision to compare against. Defaults to the pull request"
            " base, then HEAD~1."
        ),
    )
    args = parser.parse_args(argv)

    base = args.base or _default_base()
    try:
        old = load_revision(base)
    except subprocess.CalledProcessError as exc:  # pragma: no cover
        print(f"cannot read base revision {base}: {exc}", file=sys.stderr)
        return 2

    new = load_working_tree()
    new = Snapshot(
        schema_version=new.schema_version,
        package_version=new.package_version,
        schema=new.schema,
        verdicts=new.verdicts,
        api=new.api,
        paths=changed_paths(base),
        changelog=new.changelog,
    )

    report = evaluate(old, new, load_decisions())
    print("\n".join(report.lines()))
    return 0 if report.ok else 1


def _default_base() -> str:
    """Return the revision to compare against."""
    import os

    if os.environ.get("GITHUB_BASE_REF"):
        return f"origin/{os.environ['GITHUB_BASE_REF']}"
    return "HEAD~1"


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
