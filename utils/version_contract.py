"""Classify differences between two AVefi JSON Schema documents.

The schema version in ``src/avefi_schema/model.yaml`` promises one
thing: a record valid under ``MAJOR.MINOR`` stays valid under every
later ``MAJOR``. This module turns a structural comparison of two
schema documents into the bump that promise requires.

The comparison is deliberately narrow. It decides what it can prove —
membership, required-ness, types, numeric bounds — and reports the rest
as ``INCONCLUSIVE`` so that a human has to look at it. Guessing a
verdict for a regular-expression change is worse than admitting that
the question needs a reviewer; :mod:`utils.version_gate` insists on a
reviewed entry in ``versioning/decisions.toml`` for those.

Nothing here touches the file system or git: the gate adds history.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any

#: The verdicts a difference can carry.
MAJOR = "major"
MINOR = "minor"
PATCH = "patch"
NONE = "none"
INCONCLUSIVE = "inconclusive"

#: Used to keep the strictest verdict of a set of changes.
SEVERITY = {NONE: 0, PATCH: 1, MINOR: 2, MAJOR: 3}

#: Keys that never decide whether a document validates.
NON_SEMANTIC = frozenset(
    {"description", "title", "$comment", "examples", "default", "deprecated"}
)

#: Bounds where a larger value accepts more documents.
_MAX_BOUNDS = frozenset(
    {"maxItems", "maxLength", "maxProperties", "maxContains", "maximum"}
)

#: Bounds where a smaller value accepts more documents.
_MIN_BOUNDS = frozenset(
    {"minItems", "minLength", "minProperties", "minContains", "minimum"}
)

_MISSING = object()

#: Matches a ``MAJOR.MINOR`` schema version.
SCHEMA_VERSION_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)$")


@dataclass(frozen=True)
class Change:
    """One difference between two schema documents.

    ``path`` is a slash-separated JSON pointer without a leading
    ``#``, ``kind`` one of ``added``, ``removed`` or ``changed``, and
    ``verdict`` the compatibility class the change implies.

    """

    path: str
    kind: str
    verdict: str
    old: Any = None
    new: Any = None

    def __str__(self) -> str:
        """Return a single readable line for reports."""
        if self.kind == "added":
            value = f" {_short(self.new)}"
        elif self.kind == "removed":
            value = f" {_short(self.old)}"
        else:
            value = f" {_short(self.old)} -> {_short(self.new)}"
        return f"{self.path or '/'} ({self.kind}){value}: {self.verdict}"


@dataclass(frozen=True)
class Verdict:
    """The strictest decided change plus everything left open."""

    severity: str = NONE
    changes: tuple[Change, ...] = ()
    inconclusive: tuple[Change, ...] = ()

    @property
    def requires_bump(self) -> bool:
        """Whether the schema version has to move."""
        return self.severity in (MAJOR, MINOR)

    def lines(self) -> list[str]:
        """Return one line per change, for a gate report."""
        return [str(change) for change in self.changes]


def normalise(document: Any) -> Any:
    """Return ``document`` without keys that do not affect validity.

    The root ``version`` is the contract version itself; the gate
    compares it separately from ``model.yaml``, so leaving it in the
    structural diff would make every schema release look inconclusive.

    """
    return _normalise(document, root=True)


def _normalise(value: Any, root: bool = False) -> Any:
    """Recursively drop non-semantic keys."""
    if isinstance(value, dict):
        return {
            key: _normalise(item)
            for key, item in value.items()
            if key not in NON_SEMANTIC
            and not (root and key == "version")
        }
    if isinstance(value, list):
        return [_normalise(item) for item in value]
    return value


def diff(old: Any, new: Any) -> list[Change]:
    """Return the structural differences between two documents."""
    changes: list[Change] = []
    _walk(normalise(old), normalise(new), "", changes)
    return changes


def classify(old: Any, new: Any) -> Verdict:
    """Return the bump required to move from ``old`` to ``new``."""
    document = normalise(new)
    changes = tuple(_classify(change, document) for change in diff(old, new))
    decided = [c for c in changes if c.verdict != INCONCLUSIVE]
    severity = NONE
    for change in decided:
        if SEVERITY[change.verdict] > SEVERITY[severity]:
            severity = change.verdict
    return Verdict(
        severity=severity,
        changes=changes,
        inconclusive=tuple(
            c for c in changes if c.verdict == INCONCLUSIVE
        ),
    )


def _walk(old: Any, new: Any, path: str, out: list[Change]) -> None:
    """Collect differences between ``old`` and ``new`` into ``out``."""
    if isinstance(old, dict) and isinstance(new, dict):
        for key in sorted(set(old) | set(new), key=str):
            child = f"{path}/{key}"
            if key not in old:
                out.append(Change(child, "added", NONE, None, new[key]))
            elif key not in new:
                out.append(Change(child, "removed", NONE, old[key], None))
            else:
                _walk(old[key], new[key], child, out)
        return

    if isinstance(old, list) and isinstance(new, list):
        if _is_scalar_list(old) and _is_scalar_list(new):
            # Membership, not order, decides validity for ``enum``,
            # ``required`` and the alternatives of ``type``.
            for item in new:
                if item not in old:
                    out.append(Change(path, "added", NONE, None, item))
            for item in old:
                if item not in new:
                    out.append(Change(path, "removed", NONE, item, None))
            return
        old_refs = _ref_list(old)
        new_refs = _ref_list(new)
        if old_refs is not None and new_refs is not None:
            for ref in new_refs:
                if ref not in old_refs:
                    out.append(Change(path, "added", NONE, None, ref))
            for ref in old_refs:
                if ref not in new_refs:
                    out.append(Change(path, "removed", NONE, ref, None))
            return
        if old != new:
            out.append(Change(path, "changed", NONE, old, new))
        return

    if old != new:
        out.append(Change(path, "changed", NONE, old, new))


def _is_scalar_list(value: list) -> bool:
    """Whether a list holds hashable scalars only."""
    return all(
        isinstance(item, (str, int, float, bool)) or item is None
        for item in value
    )


def _ref_list(value: list) -> list[str] | None:
    """Return the ``$ref`` targets of a list, or None if not all are refs."""
    refs = []
    for item in value:
        if not isinstance(item, dict) or set(item) != {"$ref"}:
            return None
        refs.append(str(item["$ref"]))
    return refs


def _segments(path: str) -> list[str]:
    """Split a schema path into its keys."""
    return [segment for segment in path.split("/") if segment]


def _lookup(document: Any, segments: list[str]) -> Any:
    """Return the node at ``segments``, or ``_MISSING``."""
    node = document
    for segment in segments:
        if isinstance(node, dict) and segment in node:
            node = node[segment]
        elif isinstance(node, list):
            try:
                node = node[int(segment)]
            except (ValueError, IndexError):
                return _MISSING
        else:
            return _MISSING
    return node


def _classify(change: Change, document: Any) -> Change:
    """Attach a verdict to a raw difference."""
    verdict = _verdict(change, document)
    return Change(
        change.path, change.kind, verdict, change.old, change.new
    )


def _verdict(change: Change, document: Any) -> str:
    """Return the verdict of one difference."""
    segments = _segments(change.path)
    leaf = segments[-1] if segments else ""
    added = change.kind == "added"
    removed = change.kind == "removed"

    # A property of a class. This comes first: a slot may itself be
    # called ``type``, ``$id`` or ``maxLength``.
    if len(segments) >= 2 and segments[-2] == "properties":
        if removed:
            return MAJOR
        if added:
            return _property_verdict(segments, document)

    if leaf == "$id":
        return MAJOR
    if leaf in ("$schema", "metamodel_version"):
        return INCONCLUSIVE
    if leaf in _MAX_BOUNDS or leaf in _MIN_BOUNDS:
        return _bound_verdict(change, leaf)

    # A definition appearing or disappearing.
    if len(segments) == 2 and segments[0] == "$defs":
        return MINOR if added else MAJOR

    # The record union at the root of the document.
    if segments in (["anyOf"], ["oneOf"]):
        return MINOR if added else MAJOR
    if segments in (["allOf"], ["not"]):
        return INCONCLUSIVE

    if leaf == "required":
        return MAJOR if added else MINOR
    if leaf == "enum":
        return MINOR if added else MAJOR
    if leaf == "type":
        return _type_verdict(change)
    if leaf == "const":
        return MINOR if removed else MAJOR
    if leaf == "additionalProperties":
        return _additional_properties_verdict(change)
    if leaf == "pattern":
        if added:
            return MAJOR
        if removed:
            return MINOR
        return INCONCLUSIVE
    if leaf == "format":
        return MINOR if removed else INCONCLUSIVE
    if leaf == "$ref":
        return INCONCLUSIVE
    if leaf == "items":
        if added:
            return MAJOR
        if removed:
            return MINOR
        return INCONCLUSIVE
    if leaf == "properties":
        return MAJOR

    if leaf in (
        "allOf",
        "anyOf",
        "oneOf",
        "not",
        "if",
        "then",
        "else",
        "contains",
        "prefixItems",
        "propertyNames",
        "patternProperties",
        "dependentRequired",
        "dependentSchemas",
        "unevaluatedItems",
        "unevaluatedProperties",
        "exclusiveMaximum",
        "exclusiveMinimum",
        "multipleOf",
        "uniqueItems",
    ):
        return INCONCLUSIVE

    return INCONCLUSIVE


def _type_verdict(change: Change) -> str:
    """Return the verdict of a change to a ``type`` keyword.

    A ``type`` is either one name or a list of names; the order does not
    matter. Gaining a name widens the accepted values, losing one
    narrows them.

    """
    if change.kind == "added":
        return MINOR
    if change.kind == "removed":
        return MAJOR
    old = _type_names(change.old)
    new = _type_names(change.new)
    if old is None or new is None:
        return MAJOR
    return MINOR if old <= new else MAJOR


def _type_names(value: Any) -> frozenset[str] | None:
    """Return the names in a ``type`` keyword, or None if malformed."""
    if isinstance(value, str):
        return frozenset({value})
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return frozenset(value)
    return None


def _bound_verdict(change: Change, leaf: str) -> str:
    """Return the verdict of an added, removed or moved numeric bound."""
    if change.kind == "added":
        return MAJOR
    if change.kind == "removed":
        return MINOR
    old, new = change.old, change.new
    if not isinstance(old, (int, float)) or not isinstance(new, (int, float)):
        return INCONCLUSIVE
    if old == new:
        return NONE
    if leaf in _MAX_BOUNDS:
        return MAJOR if new < old else MINOR
    return MAJOR if new > old else MINOR


def _additional_properties_verdict(change: Change) -> str:
    """Return the verdict of a change to ``additionalProperties``."""
    if change.kind == "added":
        # The keyword was absent, which permits anything.
        return MAJOR if change.new is False else MINOR
    if change.kind == "removed":
        return MINOR
    if change.old is True and change.new is False:
        return MAJOR
    if change.old is False and change.new is True:
        return MINOR
    return INCONCLUSIVE


def _property_verdict(segments: list[str], document: Any) -> str:
    """Return the verdict of an added property.

    An added property is additive unless the same change also makes it
    required, in which case documents without it stop validating.

    """
    container = _lookup(document, segments[:-2])
    name = segments[-1]
    if isinstance(container, dict) and name in container.get("required", []):
        return MAJOR
    return MINOR


def _short(value: Any, limit: int = 60) -> str:
    """Render a value compactly for a report line."""
    try:
        text = json.dumps(value, ensure_ascii=False, sort_keys=True)
    except TypeError:  # pragma: no cover - defensive
        text = repr(value)
    if len(text) > limit:
        text = text[: limit - 1] + "…"
    return text


def required_schema_bump(severity: str, major: int) -> str:
    """Return the schema version component that has to move.

    The schema version is ``MAJOR.MINOR`` with no patch component, so a
    patch-level difference cannot move it. While the major is zero,
    SemVer's minor slot is the breaking slot.

    """
    if severity == NONE or severity == PATCH:
        return NONE
    if major == 0:
        return MINOR
    return severity


def bump_satisfied(old: str, new: str, required: str) -> bool:
    """Whether ``new`` is a sufficient bump over ``old``."""
    if required == NONE:
        return True
    old_parts = _version_parts(old)
    new_parts = _version_parts(new)
    if old_parts is None or new_parts is None:
        return False
    if required == PATCH:
        return new_parts > old_parts
    if required == MINOR:
        return new_parts[:2] > old_parts[:2]
    return new_parts[0] > old_parts[0]


def _version_parts(version: str) -> tuple[int, int, int] | None:
    """Return the release triple of a version string."""
    match = re.match(
        r"^(0|[1-9]\d*)\.(0|[1-9]\d*)(?:\.(0|[1-9]\d*))?", str(version)
    )
    if not match:
        return None
    return (
        int(match.group(1)),
        int(match.group(2)),
        int(match.group(3) or 0),
    )
