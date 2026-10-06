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

With [`kas-container`](https://github.com/siemens/kas/blob/master/kas-container)
and Docker or Podman installed, build an image for a board from a checkout of
this repository:

```sh
kas-container build ci/rubikpi3.yml
```

The [build tutorial](docs/source/user/USAGE.md) gives the prerequisites, the
expected output, and how long the build takes.

## Branches

| Branch | Purpose | Status | Build from it | Contributions |
| --- | --- | --- | --- | --- |
| `main` | Primary development branch, with focus on upstream support and compatibility with the most recent Yocto Project release. | Active development; compatible with Yocto Project 6.1 (`blacksail`) | Yes: `rubikpi3` and `radxa-dragon-q6a` | [Pull requests](docs/source/contributing/CONTRIBUTING.md#29--target-branches) |
| `wrynose` | LTS branch based on the Yocto Project 6.0 release, used by Qualcomm Linux 2.x. | Maintained LTS release branch | Yes, for Qualcomm Linux 2.x: `rubikpi3` and `radxa-dragon-q6a` | [Backports from `main`](docs/source/contributing/CONTRIBUTING.md#29--target-branches) |
| `scarthgap` | Qualcomm Linux >= 1.4, aligned with Yocto Project 5.0 (LTS). | Not documented; Yocto Project 5.0 is supported until April 2028 ([releases](https://wiki.yoctoproject.org/wiki/Releases)); last change on 2025-09-03 ([b411da7](https://github.com/qualcomm-linux/meta-qcom-3rdparty/commit/b411da79d08b3726eeba85df834627008b31fd7c)) | No: layer and CI configuration only, no machines | [Qualcomm Linux 1.x changes](docs/source/contributing/CONTRIBUTING.md#29--target-branches) |
| `kirkstone` | Qualcomm Linux <= 1.3, aligned with Yocto Project 4.0 (LTS). | Not documented; Yocto Project 4.0 is end of life ([releases](https://wiki.yoctoproject.org/wiki/Releases)); last change on 2025-04-09 ([d2f48af](https://github.com/qualcomm-linux/meta-qcom-3rdparty/commit/d2f48af6ee98870294be24c16673dde7fa941543)) | No: layer and CI configuration only, no machines | [Not documented](docs/source/contributing/CONTRIBUTING.md#29--target-branches) |
| `next` | Not documented; the commit that adds it to the push build gives it CI coverage so it can validate workflow changes before they land on `main` ([9d6a08d](https://github.com/qualcomm-linux/meta-qcom-3rdparty/commit/9d6a08df6bf47047d359794155f315fae5c6b96d)). | Not documented; declares Yocto Project 6.0 (`wrynose`) compatibility; last change on 2026-08-20 ([9d6a08d](https://github.com/qualcomm-linux/meta-qcom-3rdparty/commit/9d6a08df6bf47047d359794155f315fae5c6b96d)) | Not documented; holds `radxa-dragon-q6a`, `uno-q`, and `ventuno-q` | [Not documented](docs/source/contributing/CONTRIBUTING.md#29--target-branches) |

This table lists every branch. [BRANCHES.md](BRANCHES.md) describes how each
long-lived branch is maintained and how it relates to `main`.

## Machine Support

See [`conf/machine`](conf/machine/README.md) for the complete list of supported devices.

## Documentation

Build the documentation site with `make -f docs/source/Makefile setup html` from
the repository root, then open `docs/site/index.html` directly in a browser. The
[documentation guide](docs/README.md) lists the prerequisites.

- [Build tutorial](docs/source/user/USAGE.md) — Build an image for a board and find the flashable output.
- [Configuration reference](docs/source/user/CONFIGURATION.md) — Settings in the machine, layer, kas, kernel, environment, and CI files.
- [Development setup](docs/source/contributing/DEVELOPMENT.md) — Install the documentation tools and run the checks before a pull request.
- [Function reference](docs/source/contributing/README.md#function-reference) — Generated from the comments on the layer's shell functions and BitBake tasks.

## Contributing

Please read [docs/source/contributing/CONTRIBUTING.md](docs/source/contributing/CONTRIBUTING.md) for the contribution
workflow, the layer scope rules and the commit subject and message
requirements before opening a pull request. Follow the
[Code of Conduct](CODE_OF_CONDUCT.md) when participating.

## Communication

- **GitHub Issues:** [meta-qcom-3rdparty issues](https://github.com/qualcomm-linux/meta-qcom-3rdparty/issues)
- **Pull Requests:** [meta-qcom-3rdparty pull requests](https://github.com/qualcomm-linux/meta-qcom-3rdparty/pulls)

## Maintainer(s)

- Ricardo Salveti <ricardo.salveti@oss.qualcomm.com>
- Nicolas Dechesne <nicolas.dechesne@oss.qualcomm.com>

## License

This layer is licensed under the MIT license. Check out [LICENSE](LICENSE)
for more details. [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) keeps the
notices for the documentation tools and templates adapted from other projects.

## Folders

- [.github/](.github/) — Holds [CODEOWNERS](.github/CODEOWNERS), the [workflows](.github/workflows/), the issue and pull request templates, and the documentation build helpers.
- [ci/](ci/README.md) — Contains the kas configuration fragments and the check scripts that CI runs.
- [conf/](conf/README.md) — Holds the layer configuration and the machine definitions.
- [docs/](docs/README.md) — Contains the documentation source and explains how to build the site.
- [dynamic-layers/](dynamic-layers/README.md) — Holds metadata that applies only when another layer is present.
- [recipes-bsp/](recipes-bsp/README.md) — Contains the board firmware recipe and the machine packagegroups.
- [recipes-kernel/](recipes-kernel/README.md) — Contains the kernel append and its configuration fragment.

## Files

- [README.md](README.md) — Introduces the layer, its branches, and its contents.
- [BRANCHES.md](BRANCHES.md) — Describes the maintenance and merge relationship of each long-lived branch.
- [CONTRIBUTING.md](CONTRIBUTING.md) — Points to the contributor guide and development setup.
- [AGENTS.md](AGENTS.md) — Points automation agents to the agent guide.
- [CLAUDE.md](CLAUDE.md) — Links to `AGENTS.md` for agents that read this file name.
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) — States the participation standards and how to report conduct concerns.
- [SECURITY.md](SECURITY.md) — Explains how to report vulnerabilities and which branches receive security fixes.
- [LICENSE](LICENSE) — Contains the layer's MIT licence.
- [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) — Keeps the licence notices for adapted documentation tools and templates.
- [.env.example](.env.example) — Documents the environment settings for kas-container builds and the command that loads them.
- [.gitignore](.gitignore) — Keeps local environment files, the documentation environment, and the generated site out of Git.
