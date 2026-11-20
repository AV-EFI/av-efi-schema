"""Conformance of a single AVefi record.

Two different things are checked here, and they are kept together
because they answer the same question for a caller -- may this record
be registered as it stands:

1. the record against the packaged JSON Schema, which is where the
   LinkML data type patterns live (the generated pydantic bindings do
   not carry them);
2. the rules a record has to satisfy in addition to the schema, such
   as primary title types and the field length limits.

The checks collect diagnostics instead of raising on the first
problem: a caller asking "is this file registrable?" is better served
by the complete list than by the first finding. Cross-record relations
are in :mod:`avefi_validate.records`; the file-level operation is in
:mod:`avefi_validate.removal`.

"""

from collections import defaultdict
from contextlib import suppress
from datetime import date, datetime
from decimal import Decimal
import logging
import re

from avefi_schema import model_pydantic_v2 as efi

from .engine import iter_schema_errors
from .limits import DEFAULT_LIMITS
from .records import (
    CheckResult,
    HashableId,
    dangling_record,
    discard_record,
    purge_dependant_records,
)
from .report import Code, Diagnostic, Removal, record_label

log = logging.getLogger(__name__)

#: An EDTF date or interval, as accepted by the submission rules.
DATE_RE = re.compile(
    r"^-?([1-9][0-9]{3,}|0[0-9]{3})"
    r"(-(0[1-9]|1[0-2])(-(0[1-9]|[12][0-9]|3[01]))?)?[?~]?"
    r"(/-?([1-9][0-9]{3,}|0[0-9]{3})"
    r"(-(0[1-9]|1[0-2])(-(0[1-9]|[12][0-9]|3[01]))?)?[?~]?)?$"
)


def _jsonable(value):
    """Return ``value`` in the form the JSON Schema describes.

    ``model_dump()`` returns the Python values of the bindings, while
    the schema describes their JSON form: dates and timestamps are
    strings there, and a decimal is a number. The bindings serialise a
    decimal as a string, because JSON has no exact decimal type, so it
    is passed on as a number here.

    """
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, dict):
        return {key: _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    return value


def as_document(record):
    """Return ``record`` as JSON-compatible data for schema validation."""
    return _jsonable(record.model_dump())


def placeholder_issuer_records(
    efi_records: list[efi.MovingImageRecord],
    placeholder_issuer_id: str,
) -> list[efi.MovingImageRecord]:
    """Return the records that still name the placeholder issuer.

    ``described_by.has_issuer_id`` says whose collection the record
    describes, and the generic format converters ship with a
    placeholder because a converter cannot know that. A record that
    still names it says that the data provider is unspecified, which is
    not something a persistent identifier may be registered for.

    """
    found = []
    for record in efi_records:
        described_by = record.described_by
        if described_by is None:
            continue
        entries = (
            described_by if isinstance(described_by, list) else [described_by]
        )
        if any(
            entry.has_issuer_id == placeholder_issuer_id for entry in entries
        ):
            found.append(record)
    return found


def _link_attributes(record):
    """Return the attributes that point from ``record`` to another record.

    These are the relations that make the referenced record's holder a
    dependant. ``Manifestation.has_item`` is the reverse direction and
    is deliberately not included: an item counts as a dependant through
    its own ``is_item_of``.

    """
    if isinstance(record, efi.WorkVariant):
        return ("is_part_of", "is_variant_of")
    if isinstance(record, efi.Manifestation):
        return ("is_manifestation_of", "same_as")
    if isinstance(record, efi.Item):
        return ("is_item_of", "is_copy_of", "is_derivative_of")
    return ()


def _as_identifiers(value):
    """Return ``value`` as a list of identifier objects."""
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _declared_referrers(efi_records):
    """Map each referenced id to the labels that refer to it.

    Built from the input before any record is removed. It is what lets
    a record whose dependants were all rejected be told apart from one
    that never had any: ``dependants_by_ref`` only knows the survivors.

    """
    referrers = defaultdict(set)
    for record in efi_records:
        label = record_label(record)
        for attr_name in _link_attributes(record):
            for identifier in _as_identifiers(
                getattr(record, attr_name, None)
            ):
                referrers[HashableId(identifier)].add(label)
    return referrers


def _pointer(path) -> str:
    """Return an RFC 6901 pointer for a jsonschema path."""
    parts = [
        str(part).replace("~", "~0").replace("/", "~1") for part in path
    ]
    return "/" + "/".join(parts) if parts else ""


def _branch_index(error) -> object:
    """Return the union branch a context error belongs to."""
    index = getattr(error, "branch_index", None)
    if index is not None:
        return index
    path = list(getattr(error, "schema_path", ()) or ())
    return path[0] if path else None


def _record_branch(error, record):
    """Return the ``anyOf``/``oneOf`` branch that belongs to ``record``.

    The root schema is a union over the record categories, so a
    validator that was handed the root schema validates every record
    against every category and fails all but one. Reporting the errors
    of the failing categories would drown the one that applies. The
    branch is identified by its ``$ref``, which names the generated
    class.

    Validators from :func:`~avefi_validate.schema.get_schema_validator`
    are already aimed at the record's branch; this remains for a raw
    validator a caller passed to :func:`pass_checks`.

    """
    if error.validator not in ("anyOf", "oneOf") or not error.context:
        return None
    options = error.validator_value
    if not isinstance(options, list):
        return None
    refs = []
    for option in options:
        if not isinstance(option, dict) or "$ref" not in option:
            return None
        refs.append(option["$ref"])
    wanted = type(record).__name__.lower()
    for index, ref in enumerate(refs):
        if ref.rsplit("/", 1)[-1].lower() == wanted:
            return [
                child
                for child in error.context
                if _branch_index(child) == index
            ]
    return None


def _schema_errors(errors, record):
    """Flatten the schema errors that apply to ``record``.

    Only the branch matching the record's category is descended into.
    A nested ``anyOf`` without ``$ref`` alternatives is kept as one
    diagnostic: expanding every alternative would report constraints
    from forms the value was never meant to have.

    """
    result = []
    for error in errors:
        branch = _record_branch(error, record)
        if branch is None:
            result.append(error)
        else:
            result.extend(_schema_errors(branch, record))
    return result


def _schema_message(error) -> str:
    """Return a readable message from the facts of the violation.

    The text is built from the keyword, the expected value and the
    structured details, not from the engine's sentence. Both engines
    therefore produce the same message for the same violation, and a
    change of engine cannot change a report. Messages are descriptive
    only; the contract is the code, the pointer and ``params``.

    """
    keyword = error.validator
    expected = error.validator_value
    details = getattr(error, "details", None) or {}
    if keyword in ("anyOf", "oneOf") and error.context:
        return "value does not match any of the allowed forms"
    if keyword == "required":
        prop = details.get("property")
        if prop is not None:
            return f"missing required property {prop!r}"
    elif keyword == "type":
        types = expected if isinstance(expected, list) else [expected]
        return "value is not of type " + ", ".join(
            repr(item) for item in types
        )
    elif keyword == "enum":
        return f"value is not one of {expected!r}"
    elif keyword == "pattern":
        return f"value does not match pattern {expected!r}"
    elif keyword == "additionalProperties":
        unexpected = details.get("unexpected") or []
        if unexpected:
            return "unexpected properties: " + ", ".join(
                repr(prop) for prop in unexpected
            )
        return "unexpected properties are not allowed"
    return f"value does not satisfy {keyword!r}"


def schema_diagnostics(efi_record, schema_validator) -> list[Diagnostic]:
    """Return every schema violation of ``efi_record``.

    The record is checked against its own schema branch, and the
    diagnostics are sorted by pointer and keyword so two engines, or
    two runs, describe the same record in the same order.

    """
    label = record_label(efi_record)
    errors = iter_schema_errors(
        schema_validator,
        as_document(efi_record),
        type(efi_record).__name__,
    )
    diagnostics = [
        Diagnostic(
            code=Code.SCHEMA_VIOLATION,
            message=_schema_message(error),
            record=label,
            pointer=_pointer(error.absolute_path),
            params={
                "keyword": error.validator,
                "expected": _jsonable(error.validator_value),
            },
        )
        for error in _schema_errors(errors, efi_record)
    ]
    diagnostics.sort(
        key=lambda diagnostic: (
            diagnostic.pointer or "",
            diagnostic.params.get("keyword") or "",
        )
    )
    return diagnostics


def _field_limit_diagnostics(record, limits, label) -> list[Diagnostic]:
    """Return one diagnostic per value beyond a length limit."""
    diagnostics = []
    titles = []
    if record.has_primary_title:
        titles.append(
            (
                "/has_primary_title/has_name",
                "has_primary_title.has_name",
                record.has_primary_title.has_name,
            )
        )
    for index, title in enumerate(record.has_alternative_title or []):
        titles.append(
            (
                f"/has_alternative_title/{index}/has_name",
                f"has_alternative_title.{index}.has_name",
                title.has_name,
            )
        )
    for pointer, field, value in titles:
        if len(value) > limits.line_limit:
            diagnostics.append(
                Diagnostic(
                    code=Code.FIELD_TOO_LONG,
                    message=(
                        f"title is {len(value)} characters, the limit is"
                        f" {limits.line_limit}"
                    ),
                    record=label,
                    pointer=pointer,
                    params={
                        "field": field,
                        "limit": limits.line_limit,
                        "length": len(value),
                    },
                )
            )
    if record.category != "avefi:WorkVariant":
        for index, note in enumerate(record.has_note or []):
            if len(note) >= limits.text_limit:
                diagnostics.append(
                    Diagnostic(
                        code=Code.FIELD_TOO_LONG,
                        message=(
                            f"note is {len(note)} characters, the limit is"
                            f" {limits.text_limit}"
                        ),
                        record=label,
                        pointer=f"/has_note/{index}",
                        params={
                            "field": f"has_note.{index}",
                            "limit": limits.text_limit,
                            "length": len(note),
                        },
                    )
                )
    return diagnostics


def _date_diagnostics(record, label) -> list[Diagnostic]:
    """Return one diagnostic per invalid or reversed event date."""
    diagnostics = []
    for index, event in enumerate(record.has_event or []):
        has_date = event.has_date
        if not has_date:
            continue
        if not DATE_RE.search(has_date):
            diagnostics.append(
                Diagnostic(
                    code=Code.DATE_INVALID,
                    message=f"event date is not a valid EDTF value: {has_date}",
                    record=label,
                    pointer=f"/has_event/{index}/has_date",
                    params={"date": has_date},
                )
            )
            continue
        if "/" not in has_date:
            continue
        parts = has_date.split("/")
        if len(parts) != 2:
            continue
        start = re.sub(r"[^0-9-]", "", parts[0])
        end = re.sub(r"[^0-9-]", "", parts[1])
        if start > end:
            diagnostics.append(
                Diagnostic(
                    code=Code.DATE_PERIOD_ORDER,
                    message=(
                        f"event period starts after it ends: {has_date}"
                        f" (start {start} must not exceed end {end})"
                    ),
                    record=label,
                    pointer=f"/has_event/{index}/has_date",
                    params={"date": has_date, "start": start, "end": end},
                )
            )
    return diagnostics


def _empty_name_diagnostics(
    values, base_pointer, field, label
) -> list[Diagnostic]:
    """Return one diagnostic per entry whose ``has_name`` is empty."""
    diagnostics = []
    for index, value in enumerate(values or []):
        if not value.has_name:
            diagnostics.append(
                Diagnostic(
                    code=Code.NAME_EMPTY,
                    message="has_name is empty",
                    record=label,
                    pointer=f"{base_pointer}/{index}/has_name",
                    params={"field": f"{field}.has_name"},
                )
            )
    return diagnostics


def _name_diagnostics(record, label) -> list[Diagnostic]:
    """Return every empty name below agents, places, genres and subjects."""
    diagnostics = []
    for event_index, event in enumerate(record.has_event or []):
        for activity_index, activity in enumerate(
            event.has_activity or []
        ):
            diagnostics.extend(
                _empty_name_diagnostics(
                    activity.has_agent,
                    f"/has_event/{event_index}/has_activity"
                    f"/{activity_index}/has_agent",
                    "has_event.has_activity.has_agent",
                    label,
                )
            )
        diagnostics.extend(
            _empty_name_diagnostics(
                event.located_in,
                f"/has_event/{event_index}/located_in",
                "has_event.located_in",
                label,
            )
        )
    if isinstance(record, efi.WorkVariant):
        diagnostics.extend(
            _empty_name_diagnostics(
                record.has_genre, "/has_genre", "has_genre", label
            )
        )
        diagnostics.extend(
            _empty_name_diagnostics(
                record.has_subject, "/has_subject", "has_subject", label
            )
        )
    return diagnostics


def _title_type_diagnostics(record, label) -> list[Diagnostic]:
    """Return a diagnostic when the primary title uses a wrong type."""
    if not record.has_primary_title:
        return []
    if isinstance(record, efi.WorkVariant):
        allowed = ("PreferredTitle", "SuppliedDevisedTitle")
    else:
        allowed = ("TitleProper", "SuppliedDevisedTitle")
    found = record.has_primary_title.type
    if found in allowed:
        return []
    return [
        Diagnostic(
            code=Code.TITLE_PRIMARY_TYPE,
            message=(
                f"primary title type is {found!r}, expected one of"
                f" {allowed}"
            ),
            record=label,
            pointer="/has_primary_title/type",
            params={"allowed": list(allowed), "found": found},
        )
    ]


def _removed_status_diagnostics(
    record, preserve_status_removed, label
) -> list[Diagnostic]:
    """Return a diagnostic for a removed item that has no PID yet."""
    if (
        preserve_status_removed
        or not isinstance(record, efi.Item)
        or record.has_access_status != "Removed"
    ):
        return []
    if any(
        identifier.category == "avefi:AVefiResource"
        for identifier in record.has_identifier or []
    ):
        return []
    return [
        Diagnostic(
            code=Code.REMOVED_WITHOUT_PID,
            message=(
                "access status is Removed but the item has no AVefi PID"
            ),
            record=label,
            pointer="/has_access_status",
            params={"status": "Removed"},
        )
    ]


def value_diagnostics(
    efi_record,
    preserve_status_removed=False,
    limits=DEFAULT_LIMITS,
) -> list[Diagnostic]:
    """Return every semantic rule ``efi_record`` violates.

    Unlike the former boolean check, this does not stop at the first
    violation: one record may be too long, carry a reversed period and
    leave a name empty at the same time, and a caller fixing them wants
    all three.
    """
    label = record_label(efi_record)
    diagnostics = []
    diagnostics.extend(_field_limit_diagnostics(efi_record, limits, label))
    diagnostics.extend(_date_diagnostics(efi_record, label))
    diagnostics.extend(_name_diagnostics(efi_record, label))
    diagnostics.extend(_title_type_diagnostics(efi_record, label))
    diagnostics.extend(
        _removed_status_diagnostics(
            efi_record, preserve_status_removed, label
        )
    )
    return diagnostics


def _internal_error(label: str, exc: BaseException) -> Diagnostic:
    """Return a diagnostic for an unexpected failure of one record."""
    return Diagnostic(
        code=Code.INTERNAL_ERROR,
        message=f"unexpected error while checking the record: {exc}",
        record=label,
        params={"error": type(exc).__name__},
    )


def pass_checks(
    efi_records: list[efi.MovingImageRecord],
    schema_validator,
    remove_invalid=False,
    preserve_status_removed=False,
    placeholder_issuer_id: str | None = None,
    limits=DEFAULT_LIMITS,
) -> CheckResult:
    """Check records against schema and additional rules.

    Validate against AVefi schema and check various additional rules
    like field length limits, required identifiers, resolvable
    references, etc.

    Data problems no longer raise: they are collected as diagnostics and
    the remaining records are still checked. The returned
    :class:`CheckResult` carries them, together with the counts callers
    already used.

    Note that this function may have obvious side effects on
    ``efi_records`` if ``remove_invalid`` is set to True.

    Parameters
    ----------
    efi_records : List[efi.MovingImageRecord]
        List of records in the AVefi schema.
    schema_validator
        Validator instance as returned by get_schema_validator().
    remove_invalid : bool
        Remove records from the list if they violate any of the rules.
    preserve_status_removed : bool
        Accept items with access status Removed even when they do not
        carry an AVefi PID yet.
    placeholder_issuer_id : str or None
        Issuer id that means "the data provider is unspecified". When
        given, records naming it fail. When None, the rule is not
        applied: it is a submission convention, not a schema rule.
    limits : Limits
        Field length limits to enforce.

    Returns
    -------
    CheckResult
        Result carrying ``passed`` (True if all checks have passed
        successfully), ``invalid`` (number of directly invalid records),
        ``dependants`` (number of records removed as a consequence) and
        the diagnostics and removals that explain both.

    """
    id_lookup = {}
    dependants_by_ref = defaultdict(list)
    all_was_fine = True
    removed_refs = set()
    invalid_origin = {}
    invalid = 0
    dependants = 0
    diagnostics: list[Diagnostic] = []
    removals: list[Removal] = []
    # The relations as they were declared in the input. The working set
    # loses them as records are rejected, so this snapshot is what lets
    # a parent with rejected children be distinguished from a genuine
    # orphan.
    input_referrers = _declared_referrers(efi_records)
    # Removals always happen on this list so that the cascade they cause
    # can be counted even when the caller does not want the file changed.
    # When ``remove_invalid`` is set, ``working`` is the caller's list and
    # the removals are real; otherwise it is a copy and only the analysis
    # proceeds.
    working = efi_records if remove_invalid else list(efi_records)

    # The issuer says whose collection this is, which is a property of
    # the conversion rather than of an individual record. The records
    # are therefore not removed for it, however ``remove_invalid`` is
    # set: a file emptied of everything is not a file whose data
    # provider has been named.
    if placeholder_issuer_id:
        unnamed = placeholder_issuer_records(
            efi_records, placeholder_issuer_id
        )
        if unnamed:
            all_was_fine = False
            for rec in unnamed:
                diagnostics.append(
                    Diagnostic(
                        code=Code.ISSUER_PLACEHOLDER,
                        message=(
                            "record names the placeholder issuer"
                            f" {placeholder_issuer_id}; the data provider"
                            " has to be named before identifiers are"
                            " registered for it"
                        ),
                        record=record_label(rec),
                        pointer="/described_by",
                        params={"issuer_id": placeholder_issuer_id},
                    )
                )

    # Check records and track dependencies. A record with data problems
    # is still examined for every problem, then dropped from the working
    # set so that its dependants cascade exactly as they would when the
    # caller asked for a rewrite.
    for rec in working.copy():
        label = record_label(rec)
        record_diagnostics = []
        try:
            record_diagnostics.extend(
                schema_diagnostics(rec, schema_validator)
            )
        except Exception as exc:  # noqa: BLE001 - one record must not abort
            record_diagnostics.append(_internal_error(label, exc))
        try:
            record_diagnostics.extend(
                value_diagnostics(
                    rec,
                    preserve_status_removed=preserve_status_removed,
                    limits=limits,
                )
            )
        except Exception as exc:  # noqa: BLE001 - one record must not abort
            record_diagnostics.append(_internal_error(label, exc))

        identifiers = list(rec.has_identifier or [])
        if not identifiers:
            record_diagnostics.append(
                Diagnostic(
                    code=Code.MISSING_IDENTIFIER,
                    message="has_identifier is missing",
                    record=label,
                    pointer="/has_identifier",
                    params={},
                )
            )

        if record_diagnostics:
            all_was_fine = False
            invalid += 1
            diagnostics.extend(record_diagnostics)
            for identifier in identifiers:
                ref = HashableId(identifier)
                removed_refs.add(ref)
                invalid_origin.setdefault(ref, label)
            discard_record(working, rec)
            removals.append(
                Removal(record=label, reason=Code.REMOVED_AS_INVALID)
            )
            continue

        link_attributes = _link_attributes(rec)
        if not link_attributes:
            all_was_fine = False
            invalid += 1
            diagnostics.append(
                _internal_error(
                    label, ValueError(f"Cannot handle {type(rec)}")
                )
            )
            discard_record(working, rec)
            removals.append(
                Removal(record=label, reason=Code.REMOVED_AS_INVALID)
            )
            continue

        record_ids = []
        duplicate = False
        for identifier in identifiers:
            record_id = HashableId(identifier)
            if record_id in id_lookup or record_id in removed_refs:
                duplicate = True
                all_was_fine = False
                invalid += 1
                diagnostics.append(
                    Diagnostic(
                        code=Code.DUPLICATE_IDENTIFIER,
                        message=f"identifier is not unique: {record_id}",
                        record=label,
                        pointer="/has_identifier",
                        params={"identifier": str(record_id)},
                    )
                )
                for id_ in identifiers:
                    ref = HashableId(id_)
                    removed_refs.add(ref)
                    invalid_origin.setdefault(ref, label)
                discard_record(working, rec)
                removals.append(
                    Removal(record=label, reason=Code.REMOVED_AS_INVALID)
                )
                dependants += purge_dependant_records(
                    record_id,
                    working,
                    id_lookup,
                    dependants_by_ref,
                    removed_refs,
                    removals=removals,
                    because=label,
                )
                for rid in record_ids:
                    with suppress(KeyError):
                        del id_lookup[rid]
                record_ids = []
                break
            record_ids.append(record_id)
            id_lookup[record_id] = (rec, record_ids)
        if duplicate or not record_ids:
            continue
        for attr_name in link_attributes:
            for identifier in _as_identifiers(
                getattr(rec, attr_name, None)
            ):
                ref = HashableId(identifier)
                dependants_by_ref[ref].append(record_id)

    # Check for references (to parent records) that cannot be resolved
    for ref in list(dependants_by_ref.keys()):
        if (
            ref not in id_lookup
            and ref.identifier.category == "avefi:LocalResource"
        ):
            all_was_fine = False
            dependant_label = _first_dependant_label(
                ref, dependants_by_ref, id_lookup
            )
            dependants += purge_dependant_records(
                ref,
                working,
                id_lookup,
                dependants_by_ref,
                removed_refs,
                removals=removals,
                because=invalid_origin.get(ref, str(ref)),
            )
            if ref not in removed_refs:
                diagnostics.append(
                    Diagnostic(
                        code=Code.REFERENCE_UNRESOLVED,
                        message=(
                            f"unresolvable reference:"
                            f" {ref.identifier.id}"
                        ),
                        record=dependant_label,
                        pointer=None,
                        params={"reference": str(ref)},
                    )
                )

    # Check for records that should be associated with items but are not
    for rec in working.copy():
        if not any(candidate is rec for candidate in working):
            continue
        is_dangling, purged = dangling_record(
            rec,
            working,
            id_lookup,
            dependants_by_ref,
            removed_refs,
            remove_dangling=True,
            diagnostics=diagnostics,
            removals=removals,
            input_referrers=input_referrers,
        )
        if is_dangling:
            all_was_fine = False
            dependants += purged
    return CheckResult(
        all_was_fine,
        invalid=invalid,
        dependants=dependants,
        diagnostics=diagnostics,
        removals=removals,
    )


def _first_dependant_label(ref, dependants_by_ref, id_lookup) -> str | None:
    """Return the label of the first record that refers to ``ref``."""
    for dependant in dependants_by_ref.get(ref, []):
        entry = id_lookup.get(dependant)
        if entry is not None:
            return record_label(entry[0])
    return None


def has_invalid_value(
    efi_record,
    preserve_status_removed=False,
    limits=DEFAULT_LIMITS,
):
    """Return whether any semantic rule rejects ``efi_record``."""
    return bool(
        value_diagnostics(
            efi_record,
            preserve_status_removed=preserve_status_removed,
            limits=limits,
        )
    )


def exceeds_field_limit(efi_record, limits=DEFAULT_LIMITS):
    """Return whether a title or note exceeds its length limit."""
    return bool(
        _field_limit_diagnostics(
            efi_record, limits, record_label(efi_record)
        )
    )


def has_invalid_date(efi_record):
    """Return whether an event carries an invalid or reversed date."""
    return bool(_date_diagnostics(efi_record, record_label(efi_record)))
