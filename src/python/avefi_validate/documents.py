"""Conformance of a single AVefi record.

Two different things are checked here, and they are kept together
because they answer the same question for a caller — may this record
be registered as it stands:

1. the record against the packaged JSON Schema, which is where the
   LinkML data type patterns live (the generated pydantic bindings do
   not carry them);
2. the rules a record has to satisfy in addition to the schema, such
   as primary title types and the field length limits.

Cross-record relations are in :mod:`avefi_validate.records`; the
file-level operation is in :mod:`avefi_validate.removal`.

"""

from collections import defaultdict
from contextlib import suppress
from datetime import date, datetime
from decimal import Decimal
import logging
import re

from avefi_schema import model_pydantic_v2 as efi
from jsonschema.exceptions import best_match

from .limits import DEFAULT_LIMITS
from .records import (
    CheckResult,
    HashableId,
    dangling_record,
    discard_record,
    purge_dependant_records,
)

log = logging.getLogger(__name__)


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
        successfully), ``invalid`` (number of directly invalid records)
        and ``dependants`` (number of records removed as a consequence).

    """
    id_lookup = {}
    dependants_by_ref = defaultdict(list)
    all_was_fine = True
    removed_refs = set()
    invalid = 0
    dependants = 0
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
            log.error(
                f"{len(unnamed)} record(s) name the placeholder issuer"
                f" {placeholder_issuer_id}; the data provider has to be"
                f" named before identifiers are registered for them"
            )

    # Check records and track dependencies
    for rec in working.copy():
        error = best_match(schema_validator.iter_errors(as_document(rec)))
        if error is not None:
            raise error

        if not rec.has_identifier:
            raise ValueError(f"has_identifier is missing in record: {rec}")
        try:
            if has_invalid_value(
                rec,
                preserve_status_removed=preserve_status_removed,
                limits=limits,
            ):
                all_was_fine = False
                invalid += 1
                removed_refs.update(
                    [HashableId(id_) for id_ in rec.has_identifier]
                )
                discard_record(working, rec)
                continue
        except Exception as e:
            raise RuntimeError(
                f"Error while checking record {rec.has_identifier[0].id}",
            ) from e

        record_ids = []
        for identifier in rec.has_identifier:
            record_id = HashableId(identifier)
            if record_id in id_lookup or record_id in removed_refs:
                all_was_fine = False
                err_msg = f"Identifier is not unique: {record_id}"
                if remove_invalid:
                    log.error(err_msg)
                    invalid += 1
                    removed_refs.update(
                        [HashableId(id_) for id_ in rec.has_identifier]
                    )
                    discard_record(working, rec)
                    # Remove the other record with that same ID as well
                    dependants += purge_dependant_records(
                        record_id,
                        working,
                        id_lookup,
                        dependants_by_ref,
                        removed_refs,
                    )
                else:
                    raise ValueError(err_msg)
                for record_id in record_ids:
                    with suppress(KeyError):
                        del id_lookup[record_id]
                record_ids = []
                break
            record_ids.append(record_id)
            id_lookup[record_id] = (rec, record_ids)
        if not record_ids:
            continue
        if isinstance(rec, efi.WorkVariant):
            link_attributes = ("is_part_of", "is_variant_of")
        elif isinstance(rec, efi.Manifestation):
            # Ignore has_item here
            link_attributes = ("is_manifestation_of", "same_as")
        elif isinstance(rec, efi.Item):
            link_attributes = ("is_item_of", "is_copy_of", "is_derivative_of")
        else:
            raise ValueError(f"Cannot handle {type(rec)} (record={rec})")
        for attr_name in link_attributes:
            attr = getattr(rec, attr_name)
            if attr is None:
                attr = []
            elif not isinstance(attr, list):
                attr = [attr]
            for identifier in attr:
                ref = HashableId(identifier)
                dependants_by_ref[ref].append(record_id)

    # Check for references (to parent records) that cannot be resolved
    for ref in list(dependants_by_ref.keys()):
        if (
            ref not in id_lookup
            and ref.identifier.category == "avefi:LocalResource"
        ):
            all_was_fine = False
            dependants += purge_dependant_records(
                ref,
                working,
                id_lookup,
                dependants_by_ref,
                removed_refs,
            )
            if ref not in removed_refs:
                log.error(f"Unresolvable reference: {ref.identifier.id}")

    # Check for records that should be associated with items but are not
    for rec in working.copy():
        is_dangling, purged = dangling_record(
            rec,
            working,
            id_lookup,
            dependants_by_ref,
            removed_refs,
            remove_dangling=True,
        )
        if is_dangling:
            all_was_fine = False
            dependants += purged
    return CheckResult(all_was_fine, invalid=invalid, dependants=dependants)


def has_invalid_value(
    efi_record,
    preserve_status_removed=False,
    limits=DEFAULT_LIMITS,
):
    def any_empty_has_name(elem_generator):
        if any([not elem.has_name for elem in elem_generator]):
            log.error(f"Empty has_name in {efi_record.has_identifier[0].id}")
            return True
        return False

    if exceeds_field_limit(efi_record, limits=limits):
        return True
    if has_invalid_date(efi_record):
        return True
    for event in efi_record.has_event:
        for activity in event.has_activity:
            if any_empty_has_name(activity.has_agent):
                return True
        if any_empty_has_name(event.located_in):
            return True
    if isinstance(efi_record, efi.WorkVariant):
        if any_empty_has_name(efi_record.has_genre):
            return True
        if any_empty_has_name(efi_record.has_subject):
            return True
        if (
            efi_record.has_primary_title
            and efi_record.has_primary_title.type
            not in (
                "PreferredTitle",
                "SuppliedDevisedTitle",
            )
        ):
            log.error(
                f"Primary title type for work records is supposed to be"
                f" one of ('PreferredTitle', 'SuppliedDevisedTitle'), found:"
                f" {efi_record.has_primary_title.type} in record"
                f" {efi_record.has_identifier[0].id}"
            )
            return True
    else:
        if (
            efi_record.has_primary_title
            and efi_record.has_primary_title.type
            not in (
                "TitleProper",
                "SuppliedDevisedTitle",
            )
        ):
            log.error(
                f"Primary title type for non-work records is supposed to be"
                f" one of ('TitleProper', 'SuppliedDevisedTitle'), found:"
                f" {efi_record.has_primary_title.type} in record"
                f" {efi_record.has_identifier[0].id}"
            )
            return True
        if (
            not preserve_status_removed
            and isinstance(efi_record, efi.Item)
            and efi_record.has_access_status == "Removed"
            and not any(
                ident.category == "avefi:AVefiResource"
                for ident in efi_record.has_identifier
            )
        ):
            log.error(
                f"Do not expect has_access_status=Removed for an item"
                f" without a PID: {efi_record.has_identifier[0].id}"
            )
            return True
    return False


def exceeds_field_limit(efi_record, limits=DEFAULT_LIMITS):
    titles = []
    if efi_record.has_primary_title:
        titles.append(efi_record.has_primary_title)
    titles.extend(efi_record.has_alternative_title)
    for title in titles:
        if len(title.has_name) > limits.line_limit:
            log.error(
                f"Record {efi_record.has_identifier[0].id} violates limit of"
                f" {limits.line_limit} characters on title length:"
                f" {title.has_name}"
            )
            return True
    if efi_record.category != "avefi:WorkVariant":
        for note in efi_record.has_note:
            if len(note) >= limits.text_limit:
                log.error(
                    f"Record {efi_record.has_identifier[0].id} violates limit"
                    f" of {limits.text_limit} characters on has_note"
                    f" entries"
                )
                return True
    return False


def has_invalid_date(efi_record):
    for event in efi_record.has_event:
        if event.has_date and not re.search(
            r"^-?([1-9][0-9]{3,}|0[0-9]{3})(-(0[1-9]|1[0-2])(-(0[1-9]|[12][0-9]|3[01]))?)?[?~]?(/-?([1-9][0-9]{3,}|0[0-9]{3})(-(0[1-9]|1[0-2])(-(0[1-9]|[12][0-9]|3[01]))?)?[?~]?)?$",
            event.has_date,
        ):
            log.error(
                f"Record {efi_record.has_identifier[0].id} has event(s) with"
                f" invalid value in has_date: {event.has_date}"
            )
            return True

        # Check if this is a period expression (contains '/')
        if event.has_date and "/" in event.has_date:
            # Split period and clean each part (keep only digits and hyphens)
            period_parts = event.has_date.split("/")
            if len(period_parts) == 2:
                # Remove all characters except digits and hyphens
                clean_start = re.sub(r"[^0-9-]", "", period_parts[0])
                clean_end = re.sub(r"[^0-9-]", "", period_parts[1])

                # Perform lexicographical comparison
                # Equality is valid, only invalid when start > end
                if clean_start > clean_end:
                    log.error(
                        f"Record {efi_record.has_identifier[0].id} has"
                        f" event with invalid period: {event.has_date}"
                        f" (start {clean_start} must be less than or equal to"
                        f" end {clean_end})"
                    )
                    return True
    return False
