License: CC BY 4.0
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

The [project/ subdirectory](./project/) is dual licensed under the MIT
license
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


# Schema for Audio-Visual Material

This repository has been created in order to track the development of
schemas and controlled vocabularies as part of the [AVefi project][].
Some [documentation and examples][] are provided too. Validation
against this schema is enforced during PID registration. For this
purpose, the schema is deployed to the [Data Type Registry][] and
there available as the [AVefi Kernel Information Profile][AVefi_KIP].

[AVefi project]: https://projects.tib.eu/av-efi/
[documentation and examples]: https://av-efi.github.io/av-efi-schema/
[Data Type Registry]: https://faircore4eosc.eu/eosc-core-components/eosc-data-type-registry-dtr
[AVefi_KIP]: https://typeregistry.lab.pidconsortium.net/#objects/21.T11969/873d5c9f6ebbffecf1df

## Validating records

The [Python bindings](./project/python/avefi_schema/) are distributed
together with the JSON Schema they were generated from and with a
validator, so the checks always belong to the version of the schema
that is installed. Install the package as described in the [example on
using the Python bindings](./examples/python/README.md), then check
one or more export files:

```console
$ avefi-validate export.json
```

Each file is checked against the packaged JSON Schema and against the
submission rules that the schema cannot express: field length limits,
primary title types, identifier uniqueness, and references to local
identifiers that cannot be resolved within the same file. Add
`--remove-invalid` to rewrite a file without the invalid records and
the records that depend on them, or `--placeholder-issuer-id` to also
reject records that still name a placeholder data provider. The
command accepts several files and exits non-zero if any of them fails
the checks.

Validation is strict by default. Add `--normalise` to repair values
that are unambiguous but do not match the schema's pattern before they
are checked: `PT22M24S` becomes `PT00H22M24S`, `2024-4-5` becomes
`2024-04-05`, and a known resolver prefix such as
`https://www.wikidata.org/entity/` is stripped from an identifier.
`--normalise` validates the repaired view without writing; combine it
with `--remove-invalid` to write the repaired file. A value that cannot
be repaired safely — an empty name, a calendar-dependent `P1M`
duration, or a timestamp without a timezone — is left for the strict
checks to report. Each repair is reported as a `value.normalised`
warning carrying `params.before`, `params.after` and `params.rule`.

The same repair is available to downstream packages. Install the Rust
engine so loading and validation run at full speed:

```console
$ pip install "avefi-schema[fast]"
```

```python
from avefi_validate import dump, get_schema_validator, load_normalised, pass_checks

loaded = load_normalised("export.json")
result = pass_checks(loaded.records, get_schema_validator())
dump(loaded.records, "export.normalised.json")
```

`get_schema_validator()` selects the Rust engine when it is installed
and falls back to the pure-Python engine otherwise.
`loaded.normalisations` lists every rewrite; `loaded.diagnostics` still
lists parse problems.

Failures are reported as readable lines by default. Add
`--format json` to write one structured document to stdout instead, or
`--report PATH` to write it to a file while keeping the human-readable
output on stderr. Each finding carries a stable `code`, an RFC 6901
`pointer` and per-code `params`; the `message` is for people and may
change. The full contract is in the
[versioning guide](./src/docs/versioning.md#the-report-contract).

Schema validation uses the Rust [`jsonschema-rs`][jsonschema_rs] engine
when it is installed and the pure-Python `jsonschema` engine otherwise.
The Rust engine is an optional extra, not a hard dependency: install
`avefi-schema[fast]` where a wheel is available, or the plain package
everywhere. Both engines report the same codes, pointers,
`params.keyword`, `params.expected` and counts; messages and the order
of findings are descriptive.

In this repository, run it through the development environment:

```console
$ uv sync
$ uv run avefi-validate examples/json/menschen_am_sonntag_all_in_one.json
```

## Developer notes

The schema is developed using the [LinkML framework][LinkML]. The [src
subdirectory](./src/) contains the schema source in YAML and some
additional documentation in markdown. The [project
subdirectory](./project/) contains derivatives auto-generated using
the tools provided by LinkML and others. In particular, derived
JSONSchemas describing the PIDs for a film work, manifestation and
item can be found in the [project/jsonschema/epic/
subdirectory](./project/jsonschema/epic/). Additionally, the
[project/python/avefi_schema/
subdirectory](./project/python/avefi_schema/) contains python bindings
capable of generating schema compliant moving image metadata records.

In this repository, housekeeping tasks are managed by the [doit task
runner][doit], i.e. a central file [dodo.py](./dodo.py) in the root
directory. In order to get things up and running, you should [install
the uv Python package manager][uv_install] as explained and
recommended on their website first or just use `pip uv` in a
virtualenv. Then, you can proceed as follows:

```console
$ uv --version                 # just make sure that uv is properly instaled
uv 0.8.11
$ uv sync                      # pull in dependencies on initial setup and occasionally after git pull
[Lots of messages about required packages]
$ uv run doit                  # update derivatives in project/ after changes have been made in src/
$ uv run doit docs             # generate documentation in docs/ directory
$ uv run doit serve_site       # serve static site of docs locally for testing
```

Please note that `uv run doit docs` is automatically executed as part
of the [docs workflow](.github/workflows/docs.yml), hence no need to
run it locally in order to update the online documentation.

In order to push the latest changes to the Kernel Information Profile
in the Data Type REgistry, use the following commands:

```console
$ uv run doit check_dtr --sync
```

This relies on a custom [LinkML generator for the Data Type
Registry][dtr_gen] which is part of this repository. Please note that
updates to the Type Registry may result in changes to the schema
source files in order to record newly generated PIDs for non-existent
infoTypes. Make sure to commit those changes right away so as not to
lose the relation between LinkML classes or types and infoTypes in the
Type Registry.

## Versioning

The data-contract version and the package version are independent. The
[versioning guide](https://av-efi.github.io/av-efi-schema/versioning/)
states the compatibility promise and the report contract.
[AGENTS.md](./AGENTS.md) and [versioning/README.md](./versioning/README.md)
cover the contributor rules and the checks that enforce them.

[LinkML]: https://linkml.io/
[doit]: https://pydoit.org/
[jsonschema_rs]: https://pypi.org/project/jsonschema-rs/
[uv_install]: https://docs.astral.sh/uv/getting-started/installation/
[dtr_gen]: ./utils/README.md
