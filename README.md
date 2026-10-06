# meta-qcom-3rdparty

[![Build on push (main)](https://img.shields.io/github/actions/workflow/status/qualcomm-linux/meta-qcom-3rdparty/push.yml?label=Build%20on%20push%20(main))](https://github.com/qualcomm-linux/meta-qcom-3rdparty/actions/workflows/push.yml)
[![Nightly Build (main)](https://img.shields.io/github/actions/workflow/status/qualcomm-linux/meta-qcom-3rdparty/nightly-build.yml?label=Nightly%20Build%20(main))](https://github.com/qualcomm-linux/meta-qcom-3rdparty/actions/workflows/nightly-build.yml)

[![Build on push (wrynose)](https://img.shields.io/github/actions/workflow/status/qualcomm-linux/meta-qcom-3rdparty/push.yml?branch=wrynose&label=Build%20on%20push%20(wrynose))](https://github.com/qualcomm-linux/meta-qcom-3rdparty/actions/workflows/push.yml?query=branch%3Awrynose)
[![Nightly Build (wrynose)](https://img.shields.io/github/actions/workflow/status/qualcomm-linux/meta-qcom-3rdparty/nightly-build.yml?branch=wrynose&label=Nightly%20Build%20(wrynose))](https://github.com/qualcomm-linux/meta-qcom-3rdparty/actions/workflows/nightly-build.yml?query=branch%3Awrynose)

## Introduction

OpenEmbedded/Yocto Project BSP layer for Third-Party Maintained Qualcomm based
platforms.

This layer provides additional recipes and machine configuration files for
Third-Party Maintained Qualcomm platforms. Reference boards that are officially
supported by Qualcomm are available via [`meta-qcom`](https://github.com/qualcomm-linux/meta-qcom) instead.

This layer depends on:

```text
URI: https://github.com/openembedded/openembedded-core.git
layers: meta
branch: master
revision: HEAD

URI: https://github.com/qualcomm-linux/meta-qcom.git
branch: master
revision: HEAD
```

## Build an image

Build a RUBIK Pi 3 image with [kas-container](https://github.com/siemens/kas)
from the directory that contains your clone, which also receives the build:

```sh
kas-container build meta-qcom-3rdparty/ci/rubikpi3.yml
```

The [build tutorial](docs/source/user/USAGE.md) lists the prerequisites, the
files the build produces, and how long the build takes.

## Branches

| Branch | Purpose and status | Build from it | Contributions |
| --- | --- | --- | --- |
| `main` | Primary development branch, with focus on upstream support and compatibility with the most recent Yocto Project release. Active: CI builds every push. | Yes: `rubikpi3` and `radxa-dragon-q6a`. | [New work](docs/source/contributing/CONTRIBUTING.md#29--target-branches) |
| `wrynose` | LTS branch based on the Yocto Project 6.0 release, used by Qualcomm Linux 2.x. CI builds it nightly. The [Yocto Project](https://wiki.yoctoproject.org/wiki/Releases) supports 6.0 until April 2030. | Yes: `rubikpi3` and `radxa-dragon-q6a`. | [Backports from `main`](docs/source/contributing/CONTRIBUTING.md#29--target-branches) |
| `scarthgap` | Qualcomm Linux >= 1.4, aligned with Yocto Project 5.0 (LTS). Maintenance status not documented. The [Yocto Project](https://wiki.yoctoproject.org/wiki/Releases) supports 5.0 until April 2028. [Last commit](https://github.com/qualcomm-linux/meta-qcom-3rdparty/commits/scarthgap): 2025-09-03. | No: it holds the layer configuration and CI files, with no machines. | [Qualcomm Linux 1.x boards](docs/source/contributing/CONTRIBUTING.md#29--target-branches) |
| `kirkstone` | Qualcomm Linux <= 1.3, aligned with Yocto Project 4.0 (LTS). The [Yocto Project](https://wiki.yoctoproject.org/wiki/Releases) lists 4.0 as end of life. [Last commit](https://github.com/qualcomm-linux/meta-qcom-3rdparty/commits/kirkstone): 2025-04-09. | No: it holds the layer configuration and CI files, with no machines. | [Not documented](docs/source/contributing/CONTRIBUTING.md#29--target-branches) |
| `next` | Purpose and status not documented. [Last commit](https://github.com/qualcomm-linux/meta-qcom-3rdparty/commits/next): 2026-08-20. | Not documented; its tree holds the `radxa-dragon-q6a`, `uno-q`, and `ventuno-q` machines. | [Not documented](docs/source/contributing/CONTRIBUTING.md#29--target-branches) |

This table lists every branch. [BRANCHES.md](BRANCHES.md) describes how the
long-lived branches are maintained.

## Machine Support

See [conf/machine](conf/machine/README.md) for the complete list of supported devices.

## Contributing

Please read [docs/source/contributing/CONTRIBUTING.md](docs/source/contributing/CONTRIBUTING.md) for the contribution
workflow, the layer scope rules and the commit subject and message
requirements before opening a pull request.

## Documentation

Build the documentation site from the repository root, then open
`docs/site/index.html` directly in a browser:

```sh
make -f docs/source/Makefile setup html
```

The [documentation guide](docs/README.md) lists the build prerequisites and where
the source lives.

- [Build tutorial](docs/source/user/USAGE.md) — Build an image for a supported board.
- [Configuration reference](docs/source/user/CONFIGURATION.md) — Settings in the layer, machine, kas, and kernel files.
- [Development setup](docs/source/contributing/DEVELOPMENT.md) — Prepare a checkout, run the layer checks, and build the documentation.
- [Agent guide](docs/source/contributing/AGENTS.md) — Run builds and checks the same way CI does.

## Communication

- **GitHub Issues:** [meta-qcom-3rdparty issues](https://github.com/qualcomm-linux/meta-qcom-3rdparty/issues)
- **Pull Requests:** [meta-qcom-3rdparty pull requests](https://github.com/qualcomm-linux/meta-qcom-3rdparty/pulls)

## Maintainer(s)

- Ricardo Salveti <ricardo.salveti@oss.qualcomm.com>
- Nicolas Dechesne <nicolas.dechesne@oss.qualcomm.com>

## License

This layer is licensed under the MIT license. Check out [LICENSE](LICENSE)
for more details. [NOTICE](NOTICE) holds the licences of the documentation
tooling and templates adapted from other projects.

## Folders

- [.github/](.github/) — Holds [CODEOWNERS](.github/CODEOWNERS), the [issue templates](.github/ISSUE_TEMPLATE/), the [pull request template](.github/PULL_REQUEST_TEMPLATE/pr_template.md), the CI workflows, and the documentation build helpers.
- [ci/](ci/README.md) — Holds the kas build configurations and the layer check scripts that CI runs.
- [conf/](conf/README.md) — Holds the layer configuration and the machine definitions.
- [docs/](docs/README.md) — Holds the documentation source and explains how to build the site.
- [dynamic-layers/](dynamic-layers/README.md) — Holds recipes that apply only when another layer is present.
- [recipes-bsp/](recipes-bsp/README.md) — Holds the board firmware and package group recipes.
- [recipes-kernel/](recipes-kernel/README.md) — Holds the kernel recipe append and its configuration fragment.

## Files

- [.env.example](.env.example) — Documents the environment settings the kas build commands read.
- [.gitignore](.gitignore) — Keeps local environment files and documentation build output out of version control.
- [AGENTS.md](AGENTS.md) — Points automation agents to the agent guide.
- [BRANCHES.md](BRANCHES.md) — Describes how each long-lived branch is maintained.
- [CLAUDE.md](CLAUDE.md) — Links to `AGENTS.md` for agents that read this file name.
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) — States the participation standards and how to report conduct concerns.
- [CONTRIBUTING.md](CONTRIBUTING.md) — Points to the contribution guide.
- [LICENSE](LICENSE) — Contains the layer's MIT licence.
- [NOTICE](NOTICE) — Contains the licences of the documentation tooling and templates adapted from other projects.
- [README.md](README.md) — Introduces the layer, its branches, and its contents.
- [SECURITY.md](SECURITY.md) — Explains how to report vulnerabilities.
