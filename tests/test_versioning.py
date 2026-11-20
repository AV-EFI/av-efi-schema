"""The two version numbers agree with each other and with the artefacts.

None of these tests needs git history: they catch the wiring mistakes
that would make the gate compare the wrong things, and they fail
immediately when a generator stops carrying the schema version.

"""

from __future__ import annotations

import hashlib
import json
import re
from importlib import metadata
from pathlib import Path
from tomllib import loads as toml_loads

from packaging.version import Version

from avefi_schema import model_pydantic_v2
from avefi_validate.schema import (
    package_version,
    schema_bytes,
    schema_fingerprint,
)
from utils.version_contract import SCHEMA_VERSION_RE
from utils.version_gate import (
    read_package_version,
    read_report_version,
    read_schema_version,
)

ROOT = Path(__file__).resolve().parents[1]
MODEL_YAML = ROOT / "src" / "avefi_schema" / "model.yaml"
PYPROJECT = ROOT / "pyproject.toml"
REPORT_PY = ROOT / "src" / "python" / "avefi_validate" / "report.py"
CHANGELOG = ROOT / "CHANGELOG.md"
JSON_SCHEMA = (
    ROOT / "project" / "jsonschema" / "avefi_schema" / "model.schema.json"
)
ZENSICAL = ROOT / "zensical.toml"
SRC_DOCS = ROOT / "src" / "docs"


def _schema_version() -> str:
    """Return the schema version declared by the LinkML source."""
    version = read_schema_version(MODEL_YAML.read_text(encoding="utf-8"))
    assert version is not None, "model.yaml has no version"
    return version


def _package_version() -> str:
    """Return the version declared by pyproject.toml."""
    version = read_package_version(PYPROJECT.read_text(encoding="utf-8"))
    assert version is not None, "pyproject.toml has no [project].version"
    return version


def test_schema_version_is_a_quoted_major_minor_string():
    """An unquoted ``0.3`` would be read as a float, or not at all."""
    raw = MODEL_YAML.read_text(encoding="utf-8")
    line = re.search(r"(?m)^version:\s*(.+)$", raw)
    assert line is not None, "model.yaml has no top-level version"
    value = line.group(1).strip()
    assert value.startswith('"') and value.endswith('"'), (
        f"version must be a quoted string, found {value!r}"
    )
    assert SCHEMA_VERSION_RE.match(_schema_version())


def test_generated_json_schema_carries_the_schema_version():
    document = json.loads(JSON_SCHEMA.read_text(encoding="utf-8"))
    assert document["version"] == _schema_version()


def test_generated_bindings_carry_the_schema_version():
    assert isinstance(model_pydantic_v2.version, str), (
        "the pydantic template used to render the string 'None'"
    )
    assert model_pydantic_v2.version == _schema_version()


def test_fingerprint_reports_the_schema_version():
    assert schema_fingerprint()["version"] == _schema_version()


def test_fingerprint_reports_the_installed_package_version():
    try:
        installed = metadata.version("avefi_schema")
    except metadata.PackageNotFoundError:
        installed = None
    assert package_version() == installed
    assert schema_fingerprint()["package"] == installed
    if installed is not None:
        assert installed == _package_version(), (
            "the checkout and the installed distribution disagree"
        )


def test_fingerprint_hashes_the_packaged_schema():
    fingerprint = schema_fingerprint()
    assert fingerprint["sha256"] == hashlib.sha256(schema_bytes()).hexdigest()
    assert fingerprint["source"] == "package:avefi_schema/model.schema.json"


def test_both_versions_are_pep_440():
    assert Version(_schema_version())
    assert Version(_package_version())


def test_package_uses_a_full_release_version():
    assert re.search(r"(?m)^version\s*=\s*\"\d+\.\d+\.\d+", PYPROJECT.read_text())


def test_the_gate_reads_the_report_contract_version():
    """The regex reader must see the constant the package exports."""
    from avefi_validate.report import REPORT_CONTRACT_VERSION

    text = REPORT_PY.read_text(encoding="utf-8")
    assert read_report_version(text) == REPORT_CONTRACT_VERSION
    assert SCHEMA_VERSION_RE.match(REPORT_CONTRACT_VERSION)


def test_the_changelog_names_the_report_contract():
    """The current release section agrees with the constant.

    Sections from before the contract existed say ``not yet defined``;
    once any section carries a number, every later release must too.
    The gate checks the same fact against git history.
    """
    from avefi_validate.report import REPORT_CONTRACT_VERSION

    text = CHANGELOG.read_text(encoding="utf-8")
    if re.search(r"(?m)^Report contract:\s*[0-9]+\.[0-9]+", text) is None:
        return
    version = _package_version()
    match = re.search(r"(?m)^##\s+" + re.escape(version) + r"\s*$", text)
    assert match is not None, f"CHANGELOG.md has no section for {version}"
    rest = text[match.end():]
    following = re.search(r"(?m)^##\s+", rest)
    section = rest[: following.start()] if following else rest
    line = re.search(
        r"(?m)^Report contract:\s*([0-9]+\.[0-9]+)", section
    )
    assert line is not None, (
        f"the {version} section has no numeric Report contract: line"
    )
    assert line.group(1) == REPORT_CONTRACT_VERSION


def _nav_targets(value) -> set[str]:
    """Return every file name mentioned in a Zensical navigation list."""
    if isinstance(value, str):
        return {value}
    if isinstance(value, list):
        found: set[str] = set()
        for item in value:
            found |= _nav_targets(item)
        return found
    if isinstance(value, dict):
        found = set()
        for item in value.values():
            found |= _nav_targets(item)
        return found
    return set()


def test_every_hand_written_page_is_reachable_from_the_site_nav():
    """A page that builds but is not in ``nav`` cannot be reached."""
    config = toml_loads(ZENSICAL.read_text(encoding="utf-8"))
    nav = _nav_targets(config["project"]["nav"])
    pages = {path.name for path in SRC_DOCS.glob("*.md")}
    assert pages <= nav, f"not in nav: {sorted(pages - nav)}"
