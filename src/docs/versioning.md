# Versioning

Two numbers describe a release, and they answer two different
questions.

## Two versions

| | `schema.version` | package version |
|---|---|---|
| Where | `src/avefi_schema/model.yaml` | `pyproject.toml`, distribution metadata |
| Shape | `MAJOR.MINOR`, a quoted string | full SemVer |
| Means | which **data contract** this is | which **artefact** this is |
| Answers | "which schema judged this record?" | "is it safe to upgrade?" |
| Moves when | validity changes | any schema, validator, report or binding change |

The two numbers are independent. The schema version continues the
public schema history — the 2023 release was `1.0`, and the LinkML
contract starts at `2.0` — while the package version describes the
artefact and is still `0.x`. Neither number bounds the other: a
release that only tightens the validator moves the package and leaves
the schema alone, and a schema may ship under more than one package
version.

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
    "package": "<package version>",  # which acceptance rules
    "source": "package:avefi_schema/model.schema.json",
    "id": "https://www.av-efi.net/av-efi-schema/model",
    "version": "2.0",            # which schema document
    "metamodel_version": "1.12.0",
    "sha256": "9c3750…",         # exact schema bytes
}
```

The package version in these examples is a placeholder for the
installed distribution; `CHANGELOG.md` names the current release.

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
- Changing which code a condition reports is a report-contract change:
  a consumer branching on the old code no longer sees it for that
  condition.

## The report contract

`avefi-validate --format json`, or `--report PATH`, writes one document
describing the run:

```json
{
  "tool": {"name": "avefi-validate", "package": "<package version>"},
  "schema": {"package": "<package version>", "version": "2.0", "sha256": "9c3750…"},
  "files": [
    {
      "path": "records.json",
      "sha256": "…",
      "counts": {"initial": 3, "remaining": 3, "invalid": 1, "dependants": 2},
      "passed": false,
      "rewritten": false,
      "diagnostics": [
        {
          "code": "field.too_long",
          "severity": "error",
          "record": "WorkVariant.w1",
          "pointer": "/has_primary_title/has_name",
          "params": {"field": "has_primary_title.has_name", "limit": 250, "length": 1000},
          "message": "title is 1000 characters, the limit is 250"
        }
      ],
      "removed": []
    }
  ],
  "passed": false
}
```

The machine-readable part is the `code`, `severity`, `record`,
`pointer` and the keys of `params`:

- `code` is a member of `avefi_validate.Code`. A code never changes
  meaning within its major version.
- `pointer` is an RFC 6901 JSON pointer into the record named by
  `record`, or `null` when no single field is at fault.
- The keys of `params` are fixed per code. Values may vary with the
  data.
- `message` is a sentence for a person and may change in any release.
  Do not parse it.

The `removed` list explains every record that left the working set,
with `record.invalid` for a record that failed its own checks and
`record.depends_on_invalid` for a record removed only because
something it refers to failed. `because` names the record that caused
the cascade.

A record that has no valid dependants left is reported as
`record.depends_on_invalid` when the input referred to it, with
`params.referrers` naming the records that pointed at it.
`record.dangling` is reserved for a record that nothing in the input
referred to. The two cases are different: an orphan has no children,
while a rejected parent has children that do not survive validation.
The same `record.depends_on_invalid` code is used in both `diagnostics`
and `removed`, so one can be matched against the other.

`--normalise` repairs values that are unambiguous but do not match
their schema pattern, and reports each repair as a `value.normalised`
warning with `params.before`, `params.after` and `params.rule` (for
example `iso-duration`). Warnings describe the difference between the
file as stored and the file as checked; they do not decide `passed`.
Strict runs emit no such warning, so their reports are unchanged. A
value that cannot be repaired safely is left as it was and fails the
strict checks as before.

`passed` is true for a file if it was clean before the run or was
repaired by `--remove-invalid`; an unreadable file, invalid JSON and a
placeholder issuer are never repaired. The process exit code is `0`
when every file passed and `1` otherwise.

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
Install the hooks once per clone with `uv run doit install_hooks`. The
pre-push hook regenerates the derivatives, refuses to run on an unclean tree,
and then runs `uv run doit version_check` against the merge base. CI enforces
the same checks.
