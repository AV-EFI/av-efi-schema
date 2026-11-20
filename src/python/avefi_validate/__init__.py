"""Validate AVefi records against the schema they are shipped with.

This package is part of the ``avefi-schema`` distribution, so the JSON
Schema it validates against is the one generated from the same LinkML
source as the Python bindings in :mod:`avefi_schema`.

The rules are split by concern:

``schema``
    Access to the packaged JSON Schema and its fingerprint.
``documents``
    Conformance of a single record: schema, identifiers, dates and
    field length limits.
``records``
    Relations between records: identifiers, references, dangling
    records and the cascade that removes them.
``removal``
    The file-level operation that drops invalid records in place.
``report``
    The stable, structured description of what a run found.
``limits``
    The field length limits enforced by ``documents``.
``normalise``
    Optional repair of values that fail their schema pattern, and a
    loader that applies it before parsing.

"""

from .documents import (
    exceeds_field_limit,
    has_invalid_date,
    has_invalid_value,
    pass_checks,
    placeholder_issuer_records,
    schema_diagnostics,
    value_diagnostics,
)
from .io import LoadResult, dump, dumps
from .limits import DEFAULT_LIMITS, Limits
from .normalise import (
    Normalisation,
    NormalisationResult,
    load_normalised,
    loads_normalised,
    normalise_document,
    normalise_record,
)
from .records import CheckResult, HashableId
from .removal import FileCheck, check_file
from .report import (
    Code,
    Diagnostic,
    FileReport,
    Removal,
    Report,
    Severity,
)
from .schema import get_schema_validator, load_schema, schema_fingerprint

__all__ = [
    "CheckResult",
    "Code",
    "DEFAULT_LIMITS",
    "Diagnostic",
    "FileCheck",
    "FileReport",
    "HashableId",
    "Limits",
    "LoadResult",
    "Normalisation",
    "NormalisationResult",
    "Removal",
    "Report",
    "Severity",
    "check_file",
    "dump",
    "dumps",
    "exceeds_field_limit",
    "get_schema_validator",
    "has_invalid_date",
    "has_invalid_value",
    "load_normalised",
    "load_schema",
    "loads_normalised",
    "normalise_document",
    "normalise_record",
    "pass_checks",
    "placeholder_issuer_records",
    "schema_diagnostics",
    "schema_fingerprint",
    "value_diagnostics",
]
