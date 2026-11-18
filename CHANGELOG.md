# Changelog

Two versions name a release: `schema.version` in
`src/avefi_schema/model.yaml` is the data contract, and the package
version in `pyproject.toml` is the artefact. Every section from 0.2.0
onwards records both, plus the state of the report contract.

See [the versioning guide](src/docs/versioning.md) for what the numbers
promise.

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
