"""Rewrite values so that they satisfy the patterns of the schema.

Reading is deliberately more forgiving than writing: archives receive
data from many converters, and a duration written as ``PT22M24S`` is
the same running time as ``PT00H22M24S``. This module turns the former
into the latter before the records are checked, so that a caller can
choose between judging the file as it is and judging the file after an
unambiguous repair.

Only values that fail their pattern are touched, and a rewrite is used
only when the result matches that same pattern. A value that already
conforms is never changed, which keeps strict reports and normalised
ones comparable. The input document is never mutated.

The rules are keyed by the pattern itself. The packaged JSON Schema
inlines the LinkML type patterns into the properties, so the pattern is
the only reliable handle the generated schema offers. ``tests`` asserts
that every pattern in the schema either has a rule or is listed in
``UNNORMALISED`` with a reason, so a schema change cannot silently
bypass normalisation.

"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
import re
from typing import Any, Callable

from . import io
from .schema import load_schema

# Patterns copied from the packaged JSON Schema. Keeping them as
# constants makes the rule table readable and lets the coverage test
# compare it with the schema document.
AAT_PATTERN = r"^300\d{6}$"
AVEFI_PATTERN = r"^21(\.([0-9A-Za-z])+)*/[!-~]+$"
ID_STRING_PATTERN = r"""^((?![\"&\'])\S)+$"""
TEXT_LINE_PATTERN = r"^.+$"
DOI_PATTERN = r"""^10\.[0-9]{4,9}(\.[0-9]+)*(/|%2F)((?![\"&\'])\S)+$"""
HTTP_URI_PATTERN = r"^https?://[^/?#]+(/[^?#]*(\?([^#]*))?(#(.*))?)?$"
UTC_TIMESTAMP_PATTERN = (
    r"^2[0-9]{3}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])"
    r"T([0-1][0-9]|2[0-3]):[0-5][0-9]:([0-5][0-9]|60)"
    r"(\.[0-9]+)?(Z|\+00:00)$"
)
DURATION_PATTERN = r"^PT[1-9]*[0-9][0-9]H[0-5][0-9]M[0-5][0-9]S$"
EIDR_PATTERN = r"""^10\.5240(/|%2F)((?![\"&\'])\S)+$"""
EDTF_DATE_PATTERN = (
    r"^-?([1-9][0-9]{3,}|0[0-9]{3})"
    r"(-(0[1-9]|1[0-2])(-(0[1-9]|[12][0-9]|3[01]))?)?[?~]?"
    r"(/-?([1-9][0-9]{3,}|0[0-9]{3})"
    r"(-(0[1-9]|1[0-2])(-(0[1-9]|[12][0-9]|3[01]))?)?[?~]?)?$"
)
FILMPORTAL_PATTERN = r"^[\da-f]{32}$"
GND_PATTERN = r"^[-\dX]+$"
ISIL_PATTERN = r"^[A-Z]{2}-[A-Za-z\-0-9:/]{1,15}$"
TGN_PATTERN = r"^[1-9][0-9]{6}$"
VIAF_PATTERN = r"^\d+$"
WIKIDATA_PATTERN = r"^[LPQ]\d+$"


@dataclass(frozen=True)
class Normalisation:
    """One value rewritten to satisfy a schema pattern.

    ``record`` is the label of the record the value belongs to, or
    ``None`` when the document is not a record. ``pointer`` is an RFC
    6901 pointer into that record, so it lines up with the pointer of a
    diagnostic. ``rule`` is a stable identifier for the rule that made
    the change, e.g. ``iso-duration``.

    """

    record: str | None
    pointer: str
    before: str
    after: str
    rule: str

    def to_dict(self) -> dict:
        """Return the change as JSON-compatible data."""
        return {
            "record": self.record,
            "pointer": self.pointer,
            "before": self.before,
            "after": self.after,
            "rule": self.rule,
        }


@dataclass(frozen=True)
class NormalisationResult:
    """A document after normalisation and the changes that were made."""

    document: Any
    changes: tuple[Normalisation, ...] = ()

    @property
    def changed(self) -> bool:
        """Whether any value was rewritten."""
        return bool(self.changes)


@dataclass(frozen=True)
class _Change:
    """A change before the record label is known."""

    pointer: str
    before: str
    after: str
    rule: str


# --- individual rules ---------------------------------------------------


_DURATION_RE = re.compile(
    r"P(?:(\d+)W)?(?:(\d+)D)?"
    r"(?:T(?:(\d+(?:[.,]\d+)?)H)?"
    r"(?:(\d+(?:[.,]\d+)?)M)?"
    r"(?:(\d+(?:[.,]\d+)?)S)?)?",
    re.IGNORECASE,
)
_EDTF_PART_RE = re.compile(
    r"(-?)(\d+)(?:-(\d{1,2}))?(?:-(\d{1,2}))?([?~]?)$"
)
_LINE_BREAK_RE = re.compile(r"\s*(?:\r\n|[\r\n\v\f\u2028\u2029])\s*")


def _decimal(text: str | None) -> Decimal:
    """Return an optional duration component as a decimal."""
    if text is None:
        return Decimal(0)
    return Decimal(text.replace(",", "."))


def _iso_duration(value: str) -> str | None:
    """Expand an ISO 8601 duration to the schema's fixed-hour form.

    Years and months are calendar dependent and are left alone. Weeks
    and days are converted to hours because the schema has no slot for
    them.

    """
    match = _DURATION_RE.fullmatch(value.strip())
    if match is None:
        return None
    weeks, days, hours, minutes, seconds = match.groups()
    if not any((weeks, days, hours, minutes, seconds)):
        return None
    total = (
        _decimal(weeks) * 604800
        + _decimal(days) * 86400
        + _decimal(hours) * 3600
        + _decimal(minutes) * 60
        + _decimal(seconds)
    )
    total_seconds = int(total.to_integral_value(rounding=ROUND_HALF_UP))
    if total_seconds < 0:
        return None
    whole_hours, remainder = divmod(total_seconds, 3600)
    whole_minutes, whole_seconds = divmod(remainder, 60)
    return (
        f"PT{whole_hours:02d}H{whole_minutes:02d}M{whole_seconds:02d}S"
    )


def _edtf_part(part: str) -> str | None:
    """Return one EDTF date component with padded fields."""
    match = _EDTF_PART_RE.fullmatch(part)
    if match is None:
        return None
    sign, year, month, day, qualifier = match.groups()
    if len(year) < 4:
        year = year.zfill(4)
    elif len(year) > 4 and year.startswith("0"):
        return None
    if month is None and day is not None:
        return None
    if month is not None and not 1 <= int(month) <= 12:
        return None
    if day is not None and not 1 <= int(day) <= 31:
        return None
    result = f"{sign}{year}"
    if month is not None:
        result += f"-{int(month):02d}"
    if day is not None:
        result += f"-{int(day):02d}"
    return result + qualifier


def _edtf_date(value: str) -> str | None:
    """Pad an EDTF date or interval, including common slash forms."""
    text = value.strip()
    if re.fullmatch(r"\d{4}/\d{1,2}/\d{1,2}[?~]?", text):
        text = text.replace("/", "-")
    elif re.fullmatch(r"\d{4}/\d{1,2}[?~]?", text):
        text = text.replace("/", "-")
    parts = text.split("/")
    if len(parts) > 2:
        return None
    normalised = []
    for part in parts:
        piece = _edtf_part(part)
        if piece is None:
            return None
        normalised.append(piece)
    return "/".join(normalised)


def _utc_timestamp(value: str) -> str | None:
    """Convert an explicitly zoned timestamp to UTC.

    A naive timestamp is returned unchanged on purpose: assuming a
    timezone would invent information. It then fails the schema pattern
    and is reported like any other violation.

    """
    text = value.strip()
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return None
    utc = parsed.astimezone(timezone.utc)
    if not 2000 <= utc.year <= 2999:
        return None
    result = utc.strftime("%Y-%m-%dT%H:%M:%S")
    if utc.microsecond:
        result += "." + f"{utc.microsecond:06d}".rstrip("0")
    return result + "Z"


def _text_line(value: str) -> str | None:
    """Trim a single-line value and replace line breaks with spaces."""
    return _LINE_BREAK_RE.sub(" ", value).strip() or None


def _id_string(value: str) -> str | None:
    """Trim whitespace around an identifier."""
    return value.strip() or None


def _http_uri(value: str) -> str | None:
    """Trim whitespace around a URI."""
    return value.strip() or None


def _strip_known(value: str, prefixes: tuple[str, ...]) -> str:
    """Strip the first matching known resolver prefix."""
    text = value.strip()
    lowered = text.lower()
    for prefix in prefixes:
        if lowered.startswith(prefix.lower()):
            return text[len(prefix) :].strip()
    return text


def _aat(value: str) -> str | None:
    return (
        _strip_known(
            value,
            (
                "aat:",
                "https://vocab.getty.edu/aat/",
                "http://vocab.getty.edu/aat/",
            ),
        )
        or None
    )


def _tgn(value: str) -> str | None:
    return (
        _strip_known(
            value,
            (
                "tgn:",
                "https://vocab.getty.edu/tgn/",
                "http://vocab.getty.edu/tgn/",
            ),
        )
        or None
    )


def _gnd(value: str) -> str | None:
    return (
        _strip_known(
            value,
            (
                "gnd:",
                "https://d-nb.info/gnd/",
                "http://d-nb.info/gnd/",
            ),
        )
        or None
    )


def _viaf(value: str) -> str | None:
    return (
        _strip_known(
            value,
            (
                "viaf:",
                "https://viaf.org/viaf/",
                "http://viaf.org/viaf/",
            ),
        )
        or None
    )


def _wikidata(value: str) -> str | None:
    text = _strip_known(
        value,
        (
            "wd:",
            "https://www.wikidata.org/entity/",
            "http://www.wikidata.org/entity/",
        ),
    )
    if not text:
        return None
    if text[0] in "lLpPqQ":
        text = text[0].upper() + text[1:]
    return text


def _filmportal(value: str) -> str | None:
    text = _strip_known(value, ("filmportal:",))
    return text.lower() or None


def _isil(value: str) -> str | None:
    text = _strip_known(value, ("isil:",))
    if not text:
        return None
    if len(text) >= 2:
        text = text[:2].upper() + text[2:]
    return text


def _doi(value: str) -> str | None:
    return (
        _strip_known(
            value,
            (
                "doi:",
                "https://doi.org/",
                "http://doi.org/",
                "https://dx.doi.org/",
                "http://dx.doi.org/",
            ),
        )
        or None
    )


def _eidr(value: str) -> str | None:
    return (
        _strip_known(
            value,
            (
                "eidr:",
                "https://doi.org/",
                "http://doi.org/",
                "https://dx.doi.org/",
                "http://dx.doi.org/",
            ),
        )
        or None
    )


def _avefi(value: str) -> str | None:
    return (
        _strip_known(
            value,
            (
                "hdl:",
                "https://hdl.handle.net/",
                "http://hdl.handle.net/",
            ),
        )
        or None
    )


#: Rules by the exact pattern they repair.
RULES: dict[str, tuple[str, Callable[[str], str | None]]] = {
    AAT_PATTERN: ("aat-id", _aat),
    AVEFI_PATTERN: ("av-efi-handle", _avefi),
    ID_STRING_PATTERN: ("id-string", _id_string),
    TEXT_LINE_PATTERN: ("text-line", _text_line),
    DOI_PATTERN: ("doi", _doi),
    HTTP_URI_PATTERN: ("http-uri", _http_uri),
    UTC_TIMESTAMP_PATTERN: ("utc-timestamp", _utc_timestamp),
    DURATION_PATTERN: ("iso-duration", _iso_duration),
    EIDR_PATTERN: ("eidr", _eidr),
    EDTF_DATE_PATTERN: ("edtf-date", _edtf_date),
    FILMPORTAL_PATTERN: ("filmportal-id", _filmportal),
    GND_PATTERN: ("gnd-id", _gnd),
    ISIL_PATTERN: ("isil", _isil),
    TGN_PATTERN: ("tgn-id", _tgn),
    VIAF_PATTERN: ("viaf-id", _viaf),
    WIKIDATA_PATTERN: ("wikidata-id", _wikidata),
}

#: Patterns that deliberately have no rule, with the reason.
UNNORMALISED: dict[str, str] = {}


# --- schema traversal ---------------------------------------------------


def _resolve(node: Any, root: dict) -> dict:
    """Follow a local ``$ref`` to its definition."""
    seen = 0
    while isinstance(node, dict) and "$ref" in node:
        seen += 1
        if seen > 10:
            return {}
        name = node["$ref"].rsplit("/", 1)[-1]
        node = (root.get("$defs") or {}).get(name, {})
    return node if isinstance(node, dict) else {}


def _branches(node: dict, root: dict) -> list:
    """Return the ``anyOf``/``oneOf`` alternatives of a node."""
    node = _resolve(node, root)
    branches = []
    for key in ("anyOf", "oneOf"):
        branches.extend(node.get(key) or [])
    return branches


def _ref_name(branch: Any) -> str | None:
    """Return the definition name a branch refers to, if any."""
    if not isinstance(branch, dict):
        return None
    ref = branch.get("$ref")
    if not isinstance(ref, str):
        return None
    return ref.rsplit("/", 1)[-1]


def _short_category(value: str) -> str:
    """Reduce a category or class URI to its final name."""
    return value.rsplit("/", 1)[-1].rsplit(":", 1)[-1]


def _properties_at(
    node: Any, root: dict, category: str | None = None
) -> dict:
    """Return the properties that apply to a value.

    A value that names its category selects the matching resource,
    record or event branch; this mirrors how the validator picks the
    branch of the root ``anyOf``. Other objects merge the properties of
    every alternative.

    """
    node = _resolve(node, root)
    properties = dict(node.get("properties") or {})
    branches = _branches(node, root)
    if category:
        wanted = _short_category(category).lower()
        for branch in branches:
            name = _ref_name(branch)
            if name is not None and name.lower() == wanted:
                properties.update(
                    _properties_at(branch, root, category)
                )
                return properties
            if name is None:
                selected = _properties_at(branch, root, category)
                if selected:
                    properties.update(selected)
                    return properties
        return properties
    for branch in branches:
        properties.update(_properties_at(branch, root))
    return properties


def _items_at(node: Any, root: dict) -> Any:
    """Return the item schema of an array node."""
    node = _resolve(node, root)
    if "items" in node:
        return node["items"]
    for branch in _branches(node, root):
        items = _items_at(branch, root)
        if items is not None:
            return items
    return None


def _patterns_at(node: Any, root: dict) -> list[str]:
    """Return the known patterns that could apply to a string value."""
    found = []

    def collect(current):
        current = _resolve(current, root)
        pattern = current.get("pattern")
        if isinstance(pattern, str):
            found.append(pattern)
        for branch in _branches(current, root):
            collect(branch)

    collect(node)
    return [p for p in dict.fromkeys(found) if p in RULES]


def _escape(part: Any) -> str:
    """Escape one JSON pointer segment."""
    return str(part).replace("~", "~0").replace("/", "~1")


def _normalise_value(
    value: Any,
    node: Any,
    root: dict,
    pointer: str,
    changes: list[_Change],
) -> Any:
    """Return ``value`` normalised against ``node``.

    Dicts and lists are copied only along paths that change, so an
    unchanged document is returned as the same object.

    """
    if isinstance(value, str):
        patterns = _patterns_at(node, root)
        if not patterns:
            return value
        if any(re.fullmatch(pattern, value) for pattern in patterns):
            return value
        for pattern in patterns:
            rule, normaliser = RULES[pattern]
            candidate = normaliser(value)
            if candidate is None or candidate == value:
                continue
            if re.fullmatch(pattern, candidate):
                changes.append(_Change(pointer, value, candidate, rule))
                return candidate
        return value

    if isinstance(value, list):
        items_node = _items_at(node, root)
        if items_node is None:
            return value
        normalised = []
        changed = False
        for index, item in enumerate(value):
            new_item = _normalise_value(
                item,
                items_node,
                root,
                f"{pointer}/{index}",
                changes,
            )
            normalised.append(new_item)
            changed = changed or new_item is not item
        return normalised if changed else value

    if isinstance(value, dict):
        category = value.get("category")
        properties = _properties_at(
            node,
            root,
            category if isinstance(category, str) else None,
        )
        if not properties:
            return value
        normalised = {}
        changed = False
        for key, item in value.items():
            child_node = properties.get(key)
            if child_node is None:
                normalised[key] = item
                continue
            new_item = _normalise_value(
                item,
                child_node,
                root,
                f"{pointer}/{_escape(key)}",
                changes,
            )
            normalised[key] = new_item
            changed = changed or new_item is not item
        return normalised if changed else value

    return value


def _record_label(record: dict) -> str | None:
    """Return the label the validator would use, from raw JSON."""
    category = record.get("category")
    if not isinstance(category, str):
        return None
    name = _short_category(category)
    identifiers = record.get("has_identifier") or []
    if isinstance(identifiers, dict):
        identifiers = [identifiers]
    for identifier in identifiers:
        if isinstance(identifier, dict):
            value = identifier.get("id")
            if value:
                return f"{name}.{value}"
    return name


# --- public surface -----------------------------------------------------


def normalise_document(
    document: Any, *, schema: dict | None = None
) -> NormalisationResult:
    """Return ``document`` with values rewritten to their patterns.

    ``document`` may be one record or a list of records. The input is
    not modified. ``schema`` defaults to the packaged AVefi schema.

    """
    root = schema if schema is not None else load_schema()

    if isinstance(document, list):
        normalised = []
        changes: list[Normalisation] = []
        changed = False
        for item in document:
            if not isinstance(item, dict):
                normalised.append(item)
                continue
            raw_changes: list[_Change] = []
            new_item = _normalise_value(item, root, root, "", raw_changes)
            label = _record_label(new_item)
            changes.extend(
                Normalisation(
                    record=label,
                    pointer=change.pointer,
                    before=change.before,
                    after=change.after,
                    rule=change.rule,
                )
                for change in raw_changes
            )
            normalised.append(new_item)
            changed = changed or new_item is not item
        return NormalisationResult(
            document=normalised if changed else document,
            changes=tuple(changes),
        )

    if isinstance(document, dict):
        raw_changes = []
        new_document = _normalise_value(
            document, root, root, "", raw_changes
        )
        label = _record_label(new_document)
        return NormalisationResult(
            document=new_document,
            changes=tuple(
                Normalisation(
                    record=label,
                    pointer=change.pointer,
                    before=change.before,
                    after=change.after,
                    rule=change.rule,
                )
                for change in raw_changes
            ),
        )

    return NormalisationResult(document=document)


def normalise_record(
    record: dict, *, schema: dict | None = None
) -> NormalisationResult:
    """Normalise a single record dictionary."""
    return normalise_document(record, schema=schema)


def normalise_for_loader(
    document: Any, *, schema: dict | None = None
) -> tuple[Any, list[Normalisation]]:
    """Return the loader's ``(document, changes)`` form."""
    result = normalise_document(document, schema=schema)
    return result.document, list(result.changes)


def loads_normalised(
    input: str, *, schema: dict | None = None
) -> io.LoadResult:
    """Load records from JSON, normalising before parsing them.

    Unlike :func:`avefi_validate.io.loads`, a malformed item does not
    abort the whole file: the tolerant loader is used, so the result
    carries the usable records, the parse diagnostics and the list of
    changes.

    """
    return io.loads_with_diagnostics(
        input,
        transform=lambda document: normalise_for_loader(
            document, schema=schema
        ),
    )


def load_normalised(
    source, *, schema: dict | None = None
) -> io.LoadResult:
    """Load records from a file, normalising before parsing them."""
    return io.load_with_diagnostics(
        source,
        transform=lambda document: normalise_for_loader(
            document, schema=schema
        ),
    )


__all__ = [
    "Normalisation",
    "NormalisationResult",
    "load_normalised",
    "loads_normalised",
    "normalise_document",
    "normalise_record",
]
