# AVefi Schema Development Guide

This repository turns a LinkML schema into Python, TypeScript, JSON
Schema and documentation artefacts. This file covers the rules an agent
or contributor must follow; usage lives in `README.md`.

## Layout

- `src/avefi_schema/model.yaml`, `vocab.yaml` — the only hand-edited schema.
- `src/docs/` — hand-written documentation; copied to `docs/` by `doit docs`.
- `project/`, `docs/`, `avefi_er_diagram.md` — generated; never edit by hand.
- `dodo.py`, `utils/` — tasks, generators and templates.

## Commands

| Purpose | Command |
|---|---|
| Install dependencies | `uv sync` |
| Install git hooks once per clone | `uv run doit install_hooks` |
| Regenerate derivatives | `uv run doit` |
| Force every generator (CI parity) | `uv run doit --always-execute` |
| One target | `uv run doit jsonschema` (`python`, `typescript`, `docs`) |
| Pre-commit checks | `uv run pre-commit run --all-files` |
| Tests | `uv run pytest -q` |
| Version gate | `uv run doit version_check --base <merge-base>` |
| Re-record verdict snapshots | `uv run doit version_snapshots` |
| Data Type Registry | `uv run doit check_dtr` (`--sync` to push) |

## Rules

1. Edit the schema, then regenerate and commit the derivatives in the
   same commit.
2. `project/`, `docs/` and `avefi_er_diagram.md` are generated. Add
   hand-written pages under `src/docs/` and to `nav` in `zensical.toml`.
3. The schema version (`model.yaml`) and package version
   (`pyproject.toml`) are independent. A schema change moves both; a
   validator-only change moves only the package. At `0.x`, the package
   minor is the breaking slot; patches are verdict-invisible.
4. Every release adds a `CHANGELOG.md` section with `Schema:`,
   `Validator:` and `Report contract:` lines.
5. Failure codes, pointers and `params` keys are the report's
   contractual surface; messages are not. A new code is additive, a
   removed code is breaking, and neither may change silently.
6. An inconclusive gate result (for example a changed `pattern`) needs
   a reviewed entry in `versioning/decisions.toml`; do not guess.
7. New types and classes in `TypeRegistrySubset` need DTR PIDs: run
   `uv run doit check_dtr` after adding them.
8. CI runs pre-commit, `doit --always-execute`, a strict `git status`,
   the version tests and the gate. The pre-push hook is fast feedback;
   `--no-verify` skips only that, never CI.

Mechanics: [`versioning/README.md`](versioning/README.md). Public
promise: [`src/docs/versioning.md`](src/docs/versioning.md).

## Commit hygiene

- Keep commits focused and follow the existing history: plain
  imperative subjects, no conventional-commit prefixes.
- Significant AI assistance requires one trailer:

      Assisted-by: <agent_name>:<model_name>

  `model_name` is the model identifier only, with no provider or hoster
  prefix. If planning and implementation used different models, use the
  model that made the planning decisions.
