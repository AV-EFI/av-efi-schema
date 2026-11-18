# Versioning

Two numbers describe a release, and they answer two different
questions.

## Two versions

| | `schema.version` | package version |
|---|---|---|
| Where | `src/avefi_schema/model.yaml` | `pyproject.toml`, distribution metadata |
| Shape | `MAJOR.MINOR`, a quoted string | full SemVer, e.g. `0.3.1` |
| Means | which **data contract** this is | which **artefact** this is |
| Answers | "which schema judged this record?" | "is it safe to upgrade?" |
| Moves when | validity changes | any schema, validator, report or binding change |

The two numbers are independent. The schema version continues the
public schema history — the 2023 release was `1.0`, and the LinkML
contract starts at `2.0` — while the package version describes the
artefact and is still `0.x`. Neither number bounds the other: a
release that only tightens the validator moves the package and leaves
the schema alone, and schema `2.0` may ship in package `0.3.0`.

Two rules follow from that:

1. When the schema moves, the package moves in the same release, by
   the bump its own changes require.
2. Neither number ever decreases.

## The schema promise

> A document valid under `MAJOR.x` stays valid under every later
> `MAJOR.y`.

Within one major, a newer schema only ever accepts more. Any change
that could reject a document accepted before is a major change. This
promise is about the schema document; the validator enforces additional
semantic rules, which are versioned separately by the package.

## What bumps what

Schema changes:

| Change | Bump |
|---|---|
| Remove or rename a slot, class, type or enum member | major |
| Make an optional slot required | major |
| Tighten a bound, a `pattern` or cardinality | major |
| Change a slot's type or range, either direction | major |
| Change `$id` or a `category` discriminator value | major |
| Drop a record class from the root union | major |
| Add an optional slot, class, type or enum member | minor |
| Relax a constraint, make a required slot optional | minor |
| Add a record class to the root union | minor |
| Descriptions, titles, examples | neither |

Validator changes (package version, schema version unchanged):

| Change | Bump |
|---|---|
| Reject data that used to be accepted | major (at `0.x`: minor) |
| Accept data that used to be rejected | minor |
| Failure code or `params` added or changed | minor |
| Public helper added | minor |
| Public name, parameter or field removed or renamed | major |
| Wording, refactor, or documentation with the same verdicts | patch |

Two rules make the numbers usable:

- **A tightening is breaking even when it is a bug fix.** The number
  measures what a consumer has to do, not how correct the change was.
- **A patch is verdict-invisible.** No verdict, failure code or
  `params` key may change in a patch. That is why the package
  `MAJOR.MINOR` alone identifies the acceptance rules.

For the package at `0.x`, the minor slot is the breaking slot
(SemVer 2.0 §4), so both breaking and additive validator changes bump
the package minor. See [While the package is at 0.x](#while-the-package-is-at-0x).

## Which version judged my record

`schema_fingerprint()` reports the pair and the exact bytes:

```python
{
    "package": "0.3.0",          # which acceptance rules
    "source": "package:avefi_schema/model.schema.json",
    "id": "https://www.av-efi.net/av-efi-schema/model",
    "version": "2.0",            # which schema document
    "metamodel_version": "1.12.0",
    "sha256": "9c3750…",         # exact schema bytes
}
```

Store the whole object. `version` alone is not enough once the
validator has tightened: two records may have been judged against
schema `2.0` by different acceptance rules, and `package` is what tells
them apart. `sha256` pins the document even if a version number was
mistakenly reused.

## What you may rely on

- Documents valid under a schema major stay valid for the rest of that
  major.
- A package `MAJOR.MINOR` identifies one set of acceptance rules: two
  releases with the same major and minor accept the same records.
- Adding an enum member or a new failure code never invalidates an
  existing document or an existing consumer branch.
- Per-code `params` keys are contractual: a code keeps its keys for the
  life of its major version.
- A change of meaning with no structural trace is announced in the
  changelog; it is not inferable from the schema alone.

## While the package is at 0.x

The package is still at `0.x`, even though the schema is at `2.0`.
Before package `1.0`, each package minor release may break: both
breaking and additive validator changes land in the minor slot. Patch
releases still cannot change a verdict, so a patch is safe in the same
sense it will be after `1.0`.

Package `1.0` will be released when the validator's failure contract is
the primary path, its codes and `params` are exercised in production,
the generated artefacts and fingerprint are asserted in tests, and at
least one release has passed the versioning gate. At that point the
package `MAJOR.MINOR` becomes a stability promise rather than a
description.

## For contributors

The rules a change has to follow are in
[`AGENTS.md`](https://github.com/AV-EFI/av-efi-schema/blob/main/AGENTS.md).
The classifier, the snapshots and the gate are documented in
[`versioning/README.md`](https://github.com/AV-EFI/av-efi-schema/blob/main/versioning/README.md).
Run `uv run doit version_check` before pushing.
