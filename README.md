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
$ uv run doit serve-site       # serve static site of docs locally for testing
$ uv run doit deploy-site      # deploy static site of docs to GitHub Pages
```

In order to push the latest changes to the Kernel Information Profile
in the Data Type REgistry, use the following commands:

```console
$ uv run doit check_dtr --sync
```

This relies on a custom [LinkML generator for the Data Type
Registry][dtr_gen] which is part of this repository.

[LinkML]: https://linkml.io/
[doit]: https://pydoit.org/
[uv_install]: https://docs.astral.sh/uv/getting-started/installation/
[dtr_gen]: ./utils/README.md
