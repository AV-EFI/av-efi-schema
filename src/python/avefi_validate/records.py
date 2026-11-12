"""Relations between AVefi records.

A submission is a set of records that reference each other, not a
list of independent documents. These helpers track identifiers, find
the records that depend on one being removed, and find records that
are dangling because nothing refers to them any more.

"""

from collections import defaultdict
import logging

from avefi_schema import model_pydantic_v2 as efi

log = logging.getLogger(__name__)


def discard_record(
    record_list: list[efi.MovingImageRecord],
    record: efi.MovingImageRecord,
):
    """Remove ``record`` from ``record_list`` by identity.

    ``list.remove`` compares by equality, and pydantic models compare
    field by field. Two structurally identical records would therefore
    make the wrong object disappear.

    """
    for index, candidate in enumerate(record_list):
        if candidate is record:
            del record_list[index]
            return


class HashableId:
    def __init__(self, identifier: efi.MovingImageResource):
        self.identifier = identifier
        self.name = f"{self.identifier.category}.{self.identifier.id}"

    def __eq__(self, other) -> bool:
        """Check equality to another object."""
        return other.identifier == self.identifier

    def __hash__(self):
        """Return hash of the name attribute."""
        return hash(self.name)

    def __str__(self):
        """Return name attribute."""
        return self.name


class CheckResult:
    """Outcome of a single check pass.

    ``passed`` is True when no record is invalid. ``invalid`` counts
    the records that fail their own checks, ``dependants`` the records
    that would have to be removed as a consequence (records orphaned by
    one of the invalid ones). Both counts are computed whether or not
    ``remove_invalid`` is set.

    """

    def __init__(self, passed: bool, invalid: int = 0, dependants: int = 0):
        self.passed = passed
        self.invalid = invalid
        self.dependants = dependants

    def __bool__(self) -> bool:
        """Behave like the old boolean return value."""
        return self.passed

    def __repr__(self) -> str:
        """Return a compact, readable description."""
        return (
            f"CheckResult(passed={self.passed}, invalid={self.invalid},"
            f" dependants={self.dependants})"
        )


def purge_dependant_records(
    ref: HashableId,
    record_list: list[efi.MovingImageRecord],
    id_lookup: dict[
        HashableId, tuple[efi.MovingImageRecord, list[HashableId]]
    ],
    dependants_by_ref: dict[HashableId, list[HashableId]],
    removed_refs: set[HashableId],
    visited: set[HashableId] | None = None,
) -> int:
    """Remove all records identified by or dependant on ``ref``.

    Check whether ``ref`` has an associated record in ``id_lookup``,
    remove it from ``record_list`` and all its identifiers from
    ``id_lookup``. Recursively apply this function to all dependants
    of ``ref`` and all known identifiers of the same record.

    Records may reference each other in a cycle. ``visited`` keeps
    track of the identifiers already handled during one descent so that
    such a cycle terminates instead of exhausting the stack.

    Returns the number of records removed from ``record_list``.

    """
    if visited is None:
        visited = set()
    if ref in visited:
        return 0
    visited.add(ref)
    removed = 0
    try:
        rec, ids = id_lookup[ref]
    except KeyError:
        ids = [ref]
    else:
        discard_record(record_list, rec)
        removed += 1
        for record_id in ids:
            del id_lookup[record_id]
            removed_refs.add(record_id)
            log.debug(
                f"Reference to removed record: {record_id.identifier.id}"
            )

    for record_id in ids:
        visited.add(record_id)
        for dep_ref in dependants_by_ref[record_id]:
            removed += purge_dependant_records(
                dep_ref,
                record_list,
                id_lookup,
                dependants_by_ref,
                removed_refs,
                visited,
            )
        del dependants_by_ref[record_id]
    return removed


def dangling_record(
    rec: efi.MovingImageRecord,
    record_list: list[efi.MovingImageRecord],
    id_lookup: dict[HashableId, efi.MovingImageRecord],
    dependants_by_ref: dict[HashableId, list[HashableId]],
    removed_refs: set[HashableId],
    remove_dangling=False,
) -> tuple[bool, int]:
    """Return whether the record is dangling and how many it purged.

    Return ``(is_dangling, purged)``. ``is_dangling`` is True if the
    record has neither items nor a PID yet; False for items, records
    with a PID, and records referenced by some child record. Excepted
    are works of type analytic, which are dangling unless linked to a
    parent with at least one child that is not a work.

    When ``remove_dangling`` is set, a dangling record and its
    dependants are purged, and ``purged`` counts the records removed.

    Raises
    ------
    ValueError
        When a manifestation is linked to a work of type analytic.

    """
    if rec.category == "avefi:Item":
        return False, 0

    ids = [HashableId(id_) for id_ in rec.has_identifier]
    if all(
        id_.identifier.category == "avefi:LocalResource"
        and id_ not in dependants_by_ref
        for id_ in ids
    ):
        is_dangling = False
        purged = 0
        if rec.category == "avefi:WorkVariant" and rec.type == "Analytic":
            # No manifestation should link to an analytic work.
            if any(
                id_ in dependants_by_ref
                and id_lookup[id_][0].category == "avefi:Manifestation"
                for id_ in ids
            ):
                raise ValueError(
                    f"Analytic work unexpectedly referenced by"
                    f" manifestation(s): {ids[0].identifier.id}"
                )

            # Analytic works should always be part of another work.
            if not rec.is_part_of:
                log.error(
                    f"Analytic work without is_part_of: "
                    f"{rec.has_identifier[0].id}",
                )
                is_dangling = True
            else:
                # We need to make sure that parents of analytic works
                # actually have other dependants than the analytic
                # works themselves, i.e. a manifestation or
                # supplemental material.
                for identifier in rec.is_part_of:
                    if identifier.category != "avefi:LocalResource":
                        continue
                    ref = HashableId(identifier)
                    try:
                        parent, p_ids = id_lookup[ref]
                    except KeyError:
                        log.error(
                            f"Analytic work is part of an unresolvable"
                            f" record: {rec.has_identifier[0].id}"
                        )
                        is_dangling = True
                        continue
                    # TODO: Uncomment if approved by Metadaten-experts
                    # if parent.type != "Monographic":
                    #     log.error(
                    #         f"Analytic work {record_id} is part of work with"
                    #         f" type other than monographic: {ref}"
                    #     )
                    #     is_dangling = True
                    ref_deps = set()
                    for id_ in p_ids:
                        ref_deps.update(dependants_by_ref[id_])
                    if not ref_deps or all(
                        id_lookup[ref_dep][0].category == "avefi:WorkVariant"
                        for ref_dep in ref_deps
                    ):
                        log.error(
                            f"Analytic work is part of work without items: "
                            f"{rec.has_identifier[0].id}",
                        )
                        is_dangling = True
        else:
            log.error(
                f"No items associated with {rec.category}"
                f" {rec.has_identifier[0].id}"
            )
            is_dangling = True
        if is_dangling and remove_dangling:
            refs = []
            for attr_name in (
                "is_manifestation_of",
                "is_variant_of",
                "is_part_of",
            ):
                ref = getattr(rec, attr_name, None)
                if ref:
                    if isinstance(ref, list):
                        refs.extend(HashableId(r) for r in ref)
                    else:
                        refs.append(HashableId(ref))
            purged = purge_dependant_records(
                ids[0],
                record_list,
                id_lookup,
                dependants_by_ref,
                removed_refs,
            )
            for ref in refs:
                ref_deps = dependants_by_ref[ref]
                for id_ in ids:
                    if id_ in ref_deps:
                        ref_deps.remove(id_)
                if not ref_deps:
                    del dependants_by_ref[ref]
                    try:
                        parent, p_ids = id_lookup[ref]
                    except KeyError:
                        pass
                    else:
                        # Check whether parent is dangling now and
                        # remove, accordingly.
                        _, parent_purged = dangling_record(
                            parent,
                            record_list,
                            id_lookup,
                            dependants_by_ref,
                            removed_refs=removed_refs,
                            remove_dangling=True,
                        )
                        purged += parent_purged
        return is_dangling, purged
    return False, 0
