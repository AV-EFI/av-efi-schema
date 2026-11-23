"""Relations between AVefi records.

A submission is a set of records that reference each other, not a
list of independent documents. These helpers track identifiers, find
the records that depend on one being removed, and find records that
are dangling because nothing refers to them any more. They also find
the cycles that no registration order can satisfy.

Like the per-record checks, these functions collect diagnostics rather
than raising: a broken relation in one part of a file must not hide the
problems in another.

"""

from collections import defaultdict
from dataclasses import dataclass
import logging

from avefi_schema import model_pydantic_v2 as efi

from .report import Code, Diagnostic, Removal, record_label

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

    ``diagnostics`` explains why records failed and ``removals`` records
    what left the working set.

    """

    def __init__(
        self,
        passed: bool,
        invalid: int = 0,
        dependants: int = 0,
        diagnostics: list[Diagnostic] | None = None,
        removals: list[Removal] | None = None,
    ):
        self.passed = passed
        self.invalid = invalid
        self.dependants = dependants
        self.diagnostics = list(diagnostics or [])
        self.removals = list(removals or [])

    def __bool__(self) -> bool:
        """Behave like the old boolean return value."""
        return self.passed

    def __repr__(self) -> str:
        """Return a compact, readable description."""
        return (
            f"CheckResult(passed={self.passed}, invalid={self.invalid},"
            f" dependants={self.dependants},"
            f" diagnostics={len(self.diagnostics)})"
        )


#: Relations that say one record is above another. They have to form a
#: directed acyclic graph, or no consumer can register the records in a
#: valid order.
DIRECTED_RELATIONS = {
    efi.WorkVariant: ("is_part_of", "is_variant_of"),
    efi.Manifestation: ("is_manifestation_of",),
    efi.Item: ("is_item_of", "is_derivative_of"),
}

#: Relations that say two records are the same or copies of each
#: other. They are symmetric, so a mutual link is expected; only a
#: record pointing at itself is a cycle.
EQUIVALENCE_RELATIONS = {
    efi.WorkVariant: (),
    efi.Manifestation: ("same_as",),
    efi.Item: ("same_as", "is_copy_of"),
}


@dataclass(frozen=True)
class ReferenceCycle:
    """Records whose references form a cycle.

    ``members`` and ``relations`` are sorted. ``pointers`` pairs each
    member with the pointer of the relation that leads into the cycle,
    so every diagnostic points at the link that has to be removed.

    """

    members: tuple[str, ...]
    relations: tuple[str, ...]
    pointers: tuple[tuple[str, str], ...]


def _relations(record, table) -> tuple[str, ...]:
    """Return the attributes from ``table`` that apply to ``record``."""
    for cls, attributes in table.items():
        if isinstance(record, cls):
            return attributes
    return ()


def _references(value) -> list[efi.MovingImageResource]:
    """Return a link value as a list of identifiers."""
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def reference_cycles(
    efi_records: list[efi.MovingImageRecord],
    id_lookup: dict[
        HashableId, tuple[efi.MovingImageRecord, list[HashableId]]
    ],
) -> list[ReferenceCycle]:
    """Return the reference cycles in ``efi_records``.

    Every directed relation is an edge. Equivalence relations are
    edges only when they point at the record that carries them, which
    catches a record that is a copy of itself without rejecting the
    mutual ``same_as`` and ``is_copy_of`` links that describe two
    records of the same kind.

    References are resolved through ``id_lookup``, so identifiers
    outside the submission are not part of the graph. The traversal is
    iterative: a long chain of records must not exhaust the stack.

    """
    graph: dict[str, dict[str, set[str]]] = defaultdict(dict)

    def add_edge(source: str, attr_name: str, target: str) -> None:
        graph[source].setdefault(attr_name, set()).add(target)

    for record in efi_records:
        source = record_label(record)
        graph.setdefault(source, {})
        for attr_name in _relations(record, DIRECTED_RELATIONS):
            for identifier in _references(
                getattr(record, attr_name, None)
            ):
                entry = id_lookup.get(HashableId(identifier))
                if entry is not None:
                    add_edge(source, attr_name, record_label(entry[0]))
        for attr_name in _relations(record, EQUIVALENCE_RELATIONS):
            for identifier in _references(
                getattr(record, attr_name, None)
            ):
                entry = id_lookup.get(HashableId(identifier))
                if entry is not None and entry[0] is record:
                    add_edge(source, attr_name, source)

    def successors(node: str) -> list[str]:
        return sorted(
            target for targets in graph[node].values() for target in targets
        )

    index: dict[str, int] = {}
    lowlink: dict[str, int] = {}
    on_stack: set[str] = set()
    stack: list[str] = []
    components: list[tuple[str, ...]] = []
    counter = 0

    for root in sorted(graph):
        if root in index:
            continue
        index[root] = lowlink[root] = counter
        counter += 1
        stack.append(root)
        on_stack.add(root)
        frames = [(root, iter(successors(root)))]
        while frames:
            node, children = frames[-1]
            for target in children:
                if target not in index:
                    index[target] = lowlink[target] = counter
                    counter += 1
                    stack.append(target)
                    on_stack.add(target)
                    frames.append((target, iter(successors(target))))
                    break
                if target in on_stack:
                    lowlink[node] = min(lowlink[node], index[target])
            else:
                frames.pop()
                if frames:
                    parent = frames[-1][0]
                    lowlink[parent] = min(lowlink[parent], lowlink[node])
                if lowlink[node] == index[node]:
                    component = []
                    while True:
                        member = stack.pop()
                        on_stack.discard(member)
                        component.append(member)
                        if member == node:
                            break
                    components.append(tuple(sorted(component)))

    cycles = []
    for component in components:
        members = set(component)
        if len(component) == 1:
            node = component[0]
            if not any(node in targets for targets in graph[node].values()):
                continue
        relations = tuple(
            sorted(
                {
                    attr_name
                    for node in component
                    for attr_name, targets in graph[node].items()
                    if targets & members
                }
            )
        )
        pointers = []
        for node in component:
            for attr_name in sorted(graph[node]):
                if graph[node][attr_name] & members:
                    pointers.append((node, f"/{attr_name}"))
                    break
        cycles.append(
            ReferenceCycle(
                members=component,
                relations=relations,
                pointers=tuple(pointers),
            )
        )
    cycles.sort(key=lambda cycle: cycle.members)
    return cycles


def purge_dependant_records(
    ref: HashableId,
    record_list: list[efi.MovingImageRecord],
    id_lookup: dict[
        HashableId, tuple[efi.MovingImageRecord, list[HashableId]]
    ],
    dependants_by_ref: dict[HashableId, list[HashableId]],
    removed_refs: set[HashableId],
    visited: set[HashableId] | None = None,
    removals: list[Removal] | None = None,
    because: str | None = None,
    record_root: bool = True,
) -> int:
    """Remove all records identified by or dependant on ``ref``.

    Check whether ``ref`` has an associated record in ``id_lookup``,
    remove it from ``record_list`` and all its identifiers from
    ``id_lookup``. Recursively apply this function to all dependants
    of ``ref`` and all known identifiers of the same record.

    Records may reference each other in a cycle. ``visited`` keeps
    track of the identifiers already handled during one descent so that
    such a cycle terminates instead of exhausting the stack.

    ``removals`` collects a :class:`Removal` for every record that
    leaves ``record_list``. ``record_root`` is false when the caller has
    already recorded the reason for the record ``ref`` points at (the
    record that is invalid in its own right), so only its dependants are
    recorded here.

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
        if removals is not None and record_root:
            removals.append(
                Removal(
                    record=record_label(rec),
                    reason=Code.REMOVED_AS_DEPENDANT,
                    because=because,
                )
            )
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
                removals=removals,
                because=because,
                record_root=True,
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
    diagnostics: list[Diagnostic] | None = None,
    removals: list[Removal] | None = None,
    input_referrers: dict[HashableId, set[str]] | None = None,
) -> tuple[bool, int]:
    """Return whether the record is dangling and how many it purged.

    Return ``(is_dangling, purged)``. ``is_dangling`` is True if the
    record has neither items nor a PID yet; False for items, records
    with a PID, and records referenced by some child record. Excepted
    are works of type analytic, which are dangling unless linked to a
    parent with at least one child that is not a work.

    ``input_referrers`` maps an identifier to the labels of the input
    records that refer to it, before anything was removed. When a
    record has no dependants left but did have referrers in the input,
    it is reported as ``record.depends_on_invalid`` rather than
    ``record.dangling``: the children existed, they were rejected.
    ``record.dangling`` therefore means that nothing in the input
    referred to the record at all.

    When ``remove_dangling`` is set, a dangling record and its
    dependants are purged, and ``purged`` counts the records removed.

    A structural inconsistency (an analytic work referenced by a
    manifestation) used to raise. It is reported as a diagnostic now,
    so the rest of the file can still be checked.

    """
    label = record_label(rec)
    if rec.category == "avefi:Item":
        return False, 0
    ids = [HashableId(id_) for id_ in rec.has_identifier or []]
    if not ids:
        return False, 0
    if all(
        id_.identifier.category == "avefi:LocalResource"
        and id_ not in dependants_by_ref
        for id_ in ids
    ):
        is_dangling = False
        purged = 0
        cascade_referrers: list[str] = []
        if rec.category == "avefi:WorkVariant" and rec.type == "Analytic":
            # No manifestation should link to an analytic work.
            if any(
                id_ in dependants_by_ref
                and id_lookup[id_][0].category == "avefi:Manifestation"
                for id_ in ids
            ):
                _append(
                    diagnostics,
                    Diagnostic(
                        code=Code.ANALYTIC_REFERENCED,
                        message=(
                            "analytic work is referenced by a"
                            " manifestation"
                        ),
                        record=label,
                        pointer="/is_part_of",
                        params={
                            "identifier": ids[0].identifier.id,
                            "parent": None,
                        },
                    ),
                )
                is_dangling = True

            # Analytic works should always be part of another work.
            elif not rec.is_part_of:
                _append(
                    diagnostics,
                    Diagnostic(
                        code=Code.ANALYTIC_WITHOUT_PARENT,
                        message="analytic work is not part of another work",
                        record=label,
                        pointer="/is_part_of",
                        params={
                            "identifier": ids[0].identifier.id,
                            "parent": None,
                        },
                    ),
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
                        _append(
                            diagnostics,
                            Diagnostic(
                                code=Code.ANALYTIC_WITHOUT_PARENT,
                                message=(
                                    "analytic work is part of an"
                                    " unresolvable record"
                                ),
                                record=label,
                                pointer="/is_part_of",
                                params={
                                    "identifier": ids[0].identifier.id,
                                    "parent": str(ref),
                                },
                            ),
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
                        _append(
                            diagnostics,
                            Diagnostic(
                                code=Code.ANALYTIC_PARENT_WITHOUT_ITEMS,
                                message=(
                                    "analytic work is part of a work"
                                    " without items"
                                ),
                                record=label,
                                pointer="/is_part_of",
                                params={
                                    "identifier": ids[0].identifier.id,
                                    "parent": str(ref),
                                },
                            ),
                        )
                        is_dangling = True
        else:
            cascade_referrers = sorted(
                {
                    referrer
                    for id_ in ids
                    for referrer in (input_referrers or {}).get(id_, ())
                }
            )
            if cascade_referrers:
                code = Code.REMOVED_AS_DEPENDANT
                message = (
                    f"no valid dependants for {rec.category}"
                    f" {ids[0].identifier.id}:"
                    f" {len(cascade_referrers)} referring record(s)"
                    " were rejected"
                )
                params = {
                    "category": rec.category,
                    "identifier": ids[0].identifier.id,
                    "referrers": cascade_referrers,
                }
            else:
                code = Code.RECORD_DANGLING
                message = (
                    f"no items associated with {rec.category}"
                    f" {ids[0].identifier.id}"
                )
                params = {
                    "category": rec.category,
                    "identifier": ids[0].identifier.id,
                }
            _append(
                diagnostics,
                Diagnostic(
                    code=code,
                    message=message,
                    record=label,
                    params=params,
                ),
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
            if removals is not None:
                if cascade_referrers:
                    removals.append(
                        Removal(
                            record=label,
                            reason=Code.REMOVED_AS_DEPENDANT,
                            because=cascade_referrers[0],
                        )
                    )
                else:
                    removals.append(
                        Removal(
                            record=label,
                            reason=Code.REMOVED_AS_INVALID,
                        )
                    )
            purged = purge_dependant_records(
                ids[0],
                record_list,
                id_lookup,
                dependants_by_ref,
                removed_refs,
                removals=removals,
                because=label,
                record_root=False,
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
                            diagnostics=diagnostics,
                            removals=removals,
                            input_referrers=input_referrers,
                        )
                        purged += parent_purged
        return is_dangling, purged
    return False, 0


def _append(
    diagnostics: list[Diagnostic] | None, diagnostic: Diagnostic
) -> None:
    """Append ``diagnostic`` when a collector was supplied."""
    if diagnostics is not None:
        diagnostics.append(diagnostic)
