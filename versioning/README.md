# Versioning: contributor mechanics

The public promise is in
[`src/docs/versioning.md`](../src/docs/versioning.md). This page is for
people changing the repository: what each check does, how to regenerate
it, and when a human has to decide.

The short version: edit the schema or the validator, run
`uv run doit version_snapshots` when acceptance rules moved, bump the
two versions the way the guide says, add a `CHANGELOG.md` section, then
push. The pre-push hook regenerates the derivatives and runs the gate
for you; install it once per clone with `uv run doit install_hooks`.

## The two numbers

| | `src/avefi_schema/model.yaml` → `version:` | `pyproject.toml` → `version` |
|---|---|---|
| Shape | quoted `MAJOR.MINOR` string | full SemVer |
| Means | which data contract this is | which artefact this is |
| Moves when | validity changes | any schema, validator, report or binding change |
| Rule | independent of the package version | moves in the same release when the schema moves |

The numbers are independent. The schema continues the public schema
history: the 2023 release was `1.0`, and the LinkML contract starts at
`2.0`. The package is still `0.x` because the validator's failure
contract is not stable yet, so schema `2.0` ships in package `0.3.0`.

For the package, at `0.x` the minor slot is the breaking slot: both a
breaking and an additive validator change bump the minor. The
classifier still records which is which, because the changelog and the
package's eventual `1.0` transition depend on it.

## What enforces it

| Layer | Where | Needs git |
|---|---|---|
| Wiring invariants | `tests/test_versioning.py` | no |
| Structural schema classifier | `utils/version_contract.py`, `tests/test_version_contract.py` | no |
| Verdict snapshot | `tests/data/version_contract/`, `tests/test_verdict_snapshot.py` | no |
| Public surface snapshot | `tests/data/api_surface.json`, `tests/test_api_surface.py` | no |
| Local hooks | `.pre-commit-config.yaml`, `.githooks/version-gate` | yes |
| The gate | `utils/version_gate.py`, `tests/test_version_gate.py` | yes |

The gate compares the working tree with a base revision:

    uv run doit version_check                    # HEAD~1
    uv run doit version_check --base origin/main
    GITHUB_BASE_REF=main uv run doit version_check

It reads the base copies of `model.yaml`, `pyproject.toml`, the
generated JSON Schema, both snapshots and `CHANGELOG.md` with `git
show`, and takes the changed paths from `git diff --name-only`. It never
re-runs the generators on the base revision, which is why the generated
schema is committed.

## Local hooks and CI

The `pre-commit` package owns both hook types. Install them once per
clone:

    uv run doit install_hooks

`pre-commit install` refuses to run while `core.hooksPath` is set, so
the task unsets a local value first and fails with a clear message if a
global value is still in place.

At commit time the standard hooks check trailing whitespace, final
newlines, and YAML/TOML syntax, and fix whitespace where they can.
Generated outputs (`project/`, the all-in-one example, and
`avefi_er_diagram.md`) are excluded from the auto-fix hooks because the
generators emit trailing whitespace themselves; otherwise the next push
would regenerate it and fail the dirty check.

At push time `.githooks/version-gate`:

1. refuses to run while tracked changes are uncommitted, because the
   gate reads the working tree;
2. runs `uv run doit --always-execute`, which forces every generator
   even when `.doit.db` thinks the targets are current;
3. fails if that changed the working tree, so a hand-edited or stale
   derivative cannot be pushed;
4. runs `uv run doit version_check --base <merge-base>` against
   `origin/main`, `upstream/main` or `main` when one exists.

CI runs the same checks in the same order — pre-commit, forced
generation, a strict `git status`, the version tests and the gate — so
`git push --no-verify` skips only the faster feedback. The workflow
picks the merge base for pull requests and `github.event.before` for
pushes, and falls back to `HEAD~1`.

## Snapshots

The structural diff cannot see what the validator decides, and a new
rule may not change the schema at all. Two snapshots close that hole.

### Verdict corpus

`tests/data/version_contract/cases/<name>.json` holds a small record
list plus an optional `args` block:

```json
{
  "description": "What this case pins down.",
  "records": [ ... ],
  "args": {"remove_invalid": true, "limits": {"line_limit": 200}}
}
```

`verdict_outcome` records only stable facts: the verdict (`passed`,
`failed`, `raised`), `stage` and exception *class* for a raise, the
`invalid`, `dependants` and `remaining` counts, and the sorted
diagnostic codes. Messages are not part of the contract.

The corpus goes through the same tolerant loader as the command line,
so a case with one unparseable record still records what happened to
the others; it does not raise just because one item is malformed.
`raised` is reserved for an unexpected failure of the validator
itself.

Regenerate both snapshots after an intentional rule change:

    uv run doit version_snapshots

Or set `UPDATE_SNAPSHOTS=1` for a single test module. Commit the new
snapshot together with the version bump the gate requires. A narrowing
that turns a passing case into a failing one is breaking for anyone
whose data is now rejected, even when the change is a bug fix.

Removing a diagnostic code is also breaking: a consumer that branches
on it has nothing left to match. Adding one is additive. Both are
classifier-visible, so the gate asks for the bump the change requires.

### Public surface

`tests/data/api_surface.json` records every name in
`avefi_validate.__all__`: functions and parameters (name, kind, whether
a default exists), dataclass fields, enum members. A new helper that no
corpus case exercises still changes this snapshot.

## The classifier

`utils/version_contract.py` normalises away descriptions, titles,
comments, examples, defaults and deprecations, then walks the two
documents. The decided rows:

| Change | Verdict |
|---|---|
| `$defs` entry added / removed | minor / major |
| optional property added / property removed | minor / major |
| property added and made required | major |
| `required` entry added / removed | major / minor |
| `enum` member added / removed | minor / major |
| `type` widened / narrowed | minor / major |
| `max*` increased / decreased or removed / added | minor / major |
| `min*` decreased / increased or removed / added | minor / major |
| `pattern` removed / added | minor / major |
| `additionalProperties` opened / closed | minor / major |
| `const` removed / added or changed | minor / major |
| root `anyOf`/`oneOf` member added / removed | minor / major |
| `$id` changed | major |

Everything the classifier cannot prove is `inconclusive` and fails the
gate until a decision entry exists: a changed `pattern`, an added or
changed `format`, any `$ref` edit, `metamodel_version`, and keywords it
does not model (`allOf`, `not`, `uniqueItems`, …). This is deliberate:
guessing that a regular expression only widened is worse than asking a
reviewer.

A change of *meaning* with no structural change is invisible to the
classifier. The changelog section is where such a change must be stated
in words.

## Reviewed decisions

`versioning/decisions.toml` is the only human override. One entry per
inconclusive change, valid only for the release that carries it:

```toml
[[change]]
schema_version = "1.3"
path = "/$defs/Curie/properties/id/pattern"
reviewed = "minor"
reason = "the new pattern matches every string the old one matched"
```

`path` is the slash-separated JSON pointer from the gate report.
`reviewed` is the strictest severity the reviewer is willing to defend;
it is folded into the required bump. Entries for another
`schema_version` are ignored, so an override cannot be recycled.

## Rules the gate applies

| Rule | Meaning |
|---|---|
| R1 | both versions parse; the schema version is `MAJOR.MINOR` |
| R2 | neither version decreases |
| R3 | a structural schema change moves the schema version by the required amount |
| R3b | the schema version did not move without a schema change |
| R4 | a schema release also moves the package (any increase) |
| R5 | retired: the schema and package versions are independent |
| R6 | a change of verdicts moves the package by the classified amount |
| R7 | any edit under `src/avefi_schema/` or `src/python/avefi_validate/` moves at least the patch |
| R8 | a change of the public surface moves the package by the classified amount |
| R9 | `CHANGELOG.md` has a section for the new package version with `Schema:` and `Validator:` lines |
| R10 | every inconclusive schema change has a matching decision entry |

The bootstrap exception: a base revision whose `model.yaml` has no
`version` only requires the new one to be set. It applies once, to the
commit that introduces the mechanism.

## Adding a corpus case

1. Write the case under `tests/data/version_contract/cases/`, with a
   `description` that says which rule it pins down.
2. Run `uv run doit version_snapshots`; the new outcome appears in
   `expected.json`.
3. Read the outcome: if it is not what you intended, fix the case, not
   the snapshot.
4. Commit case and snapshot together. A new case alone is a minor
   change; changing an existing outcome is classified by direction
   (passing → failing is breaking).
