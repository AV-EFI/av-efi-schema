# Changelog

Two versions name a release: `schema.version` in
`src/avefi_schema/model.yaml` is the data contract, and the package
version in `pyproject.toml` is the artefact. Every section from 0.2.0
onwards records both, plus the state of the report contract.

See [the versioning guide](src/docs/versioning.md) for what the numbers
promise.

## 0.4.1

The environment variable that forces a schema engine is spelled
`AVEFI_VALIDATE_ENGINE`. The previous name carried a third `F`, so a
caller that set it was silently ignored.

Schema: 2.0 (unchanged)
Validator: patch — the engine override reads `AVEFI_VALIDATE_ENGINE`;
acceptance rules, codes, pointers and `params` are unchanged
Report contract: 1.0 (unchanged)

## 0.4.0

Validation now describes its result as data. A bad record no longer
aborts the run: each file is checked item by item, every schema and
semantic violation is collected, and cross-record failures are reported
with the record that caused the cascade. The command line keeps its
readable output on stderr and can write the same result as one JSON
document through `--format json` or `--report PATH`. The document names
the version of its own format as `report.version`, so a consumer can
check compatibility without mapping package versions to report shapes.

`load()` and `loads()` still raise for callers that need
all-or-nothing parsing; the new tolerant functions keep whatever could
be parsed. The public helpers `has_invalid_value`,
`exceeds_field_limit` and `has_invalid_date` keep their boolean
results.

A record whose children were all rejected is no longer reported as an
orphan. Validation snapshots the relations declared in the input before
any record is removed, so it can tell a record that never had
dependants from one whose dependants failed their own checks. The first
keeps `record.dangling`; the second reports `record.depends_on_invalid`
with `params.referrers`. Which records are accepted, the `invalid` and
`dependants` counts, and the exit code are unchanged.

Validation can now repair values that are unambiguous but fail their
schema pattern before checking them. `--normalise` validates the
repaired view without writing; `--normalise --remove-invalid` writes
the repaired file. The new `value.normalised` warning reports every
rewrite with `params.before`, `params.after` and `params.rule`.
Downstream packages can use `normalise_document`, `normalise_record`,
`load_normalised` and `loads_normalised`, then write the result with
`dump`. Strict validation remains the default, and values that cannot
be repaired safely — an empty name, a calendar-dependent `P1M`
duration, or a timestamp without a timezone — are left for the strict
checks.

Schema validation now uses the Rust `jsonschema_rs` engine when it is
installed and falls back to the pure-Python `jsonschema` engine
otherwise. The Rust engine is an optional extra,
`avefi-schema[fast]`, not a hard dependency, so a plain install stays
available on every platform. Each record is checked against its own
schema branch instead of the root union. Both engines produce the same
codes, pointers, `params.keyword`, `params.expected` and counts, and
messages are generated from those facts rather than from the engine's
prose, so they are stable across engines and remain descriptive. On
the reference 20 MB delivery, the Rust engine validates all 11,879
records in under a second and a strict run drops from about 40 s to a
few seconds.

Schema: 2.0 (unchanged)
Validator: additive — `avefi_validate.report` adds `Code`,
`Diagnostic`, `Removal`, `FileReport` and `Report`, and the package
exports `REPORT_CONTRACT_VERSION`; `CheckResult` carries diagnostics
and removals; `io` adds
`load_with_diagnostics()` and `loads_with_diagnostics()`; a record
whose dependants were all rejected is removed with
`record.depends_on_invalid` and `because` naming the referrer; adds
opt-in normalisation of values that fail their schema pattern;
validates each record against its own schema branch; uses the optional
Rust `jsonschema-rs` engine (`avefi-schema[fast]`) when installed and
the Python engine otherwise; messages are generated from the keyword
and the expected value
Report contract: 1.0 (codes, pointers and `params` keys are the
contract; `report.version` names this version; a record whose input
referrers were rejected reports `record.depends_on_invalid` with
`params.referrers`, while `record.dangling` means nothing in the input
referred to it; `value.normalised` is a warning code;
`params.keyword` and `params.expected` are identical whichever schema
engine runs; messages and diagnostic order are descriptive)

## 0.3.0

Work since 0.2.0 is mostly release infrastructure around an unchanged
data model: the schema and package versions are now independent and
machine-checked, provenance reports both, the rules are documented for
contributors and consumers, and pre-commit plus CI keep the generated
artefacts in step. Python 3.11 is the new floor, and the lockfile was
refreshed.

Schema: 2.0 (first versioned LinkML contract)
Validator: additive — `schema_fingerprint()` now reports the `package`
version next to the schema version, so provenance distinguishes a
validator release from a schema release
Packaging: requires Python 3.11+ (Python 3.10 is end-of-life)
Tooling: version gate, pre-commit hooks and CI enforcement added
Report contract: not yet defined

## 0.2.0

The schema is now developed in LinkML: `model.yaml` and `vocab.yaml` are
the only hand-edited sources, and the Python (Pydantic v2), TypeScript,
JSON Schema and documentation artefacts are generated from them. This is
a breaking change to the first published schema, `v1.0`.

Schema: none (the LinkML schema carried no `version` key; the 2023
`v1.0` release was the previous published schema)
Validator: as released — standalone `avefi-validate` package and the
JSON Schema shipped as package data
Report contract: not yet defined

## Version 0.1 as of Arpil 13th 2023
initial commit
