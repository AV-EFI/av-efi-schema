"""Record samples shared by the validator tests."""

import copy
import json

from avefi_validate import io

WORK = {
    "category": "avefi:WorkVariant",
    "type": "Monographic",
    "has_primary_title": {
        "type": "PreferredTitle",
        "has_name": "Die Brücke",
    },
    "has_identifier": [{"category": "avefi:LocalResource", "id": "w1"}],
}
MANIFESTATION = {
    "category": "avefi:Manifestation",
    "has_primary_title": {"type": "TitleProper", "has_name": "Die Brücke"},
    "is_manifestation_of": [{"category": "avefi:LocalResource", "id": "w1"}],
    "has_identifier": [{"category": "avefi:LocalResource", "id": "m1"}],
}
ITEM = {
    "category": "avefi:Item",
    "has_primary_title": {"type": "TitleProper", "has_name": "Die Brücke"},
    "is_item_of": {"category": "avefi:LocalResource", "id": "m1"},
    "has_identifier": [{"category": "avefi:LocalResource", "id": "i1"}],
}

#: The placeholder an issuer id carries while a mapping is tried out.
PLACEHOLDER_ISSUER_ID = "https://w3id.org/avefi/issuer/unspecified"


def records(*dicts):
    """Return the given record dictionaries as pydantic models."""
    return io.loads(json.dumps([copy.deepcopy(d) for d in dicts]))


def with_issuer(issuer_id):
    """Return a complete hierarchy whose work names ``issuer_id``."""
    work = copy.deepcopy(WORK)
    work["described_by"] = [
        {
            "has_issuer_id": issuer_id,
            "has_issuer_name": "Unspecified data provider",
            "has_source_key": ["k1"],
        }
    ]
    return records(work, MANIFESTATION, ITEM)


def broken_hierarchy():
    """Return a hierarchy whose work violates a submission rule.

    The title is longer than the line limit, which is not part of the
    schema: the record passes schema validation and fails the extra
    checks, so it is counted and removed rather than raising.

    """
    work = copy.deepcopy(WORK)
    work["has_primary_title"]["has_name"] = "x" * 1000
    return records(work, MANIFESTATION, ITEM)
