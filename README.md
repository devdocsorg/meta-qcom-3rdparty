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
supported by Qualcomm are available via
[meta-qcom](https://github.com/qualcomm-linux/meta-qcom) instead.

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

To build an image for a supported board, follow the
[usage tutorial](docs/source/user/USAGE.md).

## Branches

| Branch | Purpose | Status | Build from it | Contributions |
| --- | --- | --- | --- | --- |
| **main** | Primary development branch, with focus on upstream support and compatibility with the most recent Yocto Project release. | Active development | Yes: `rubikpi3` and `radxa-dragon-q6a` | [Yes](docs/source/contributing/CONTRIBUTING.md#27--submitting-changes) |
| **wrynose** | LTS branch based on the Yocto Project 6.0 release, used by Qualcomm Linux 2.x. | LTS; Yocto Project 6.0 is supported until April 2030 ([releases](https://wiki.yoctoproject.org/wiki/Releases)) | Yes: `rubikpi3` and `radxa-dragon-q6a` | [Backports from main](docs/source/contributing/CONTRIBUTING.md#27--submitting-changes) |
| **scarthgap** | Qualcomm Linux >= 1.4, aligned with Yocto Project 5.0 (LTS). | LTS; receives security fixes under [SECURITY.md](SECURITY.md) while Yocto Project 5.0 is supported, until April 2028 ([releases](https://wiki.yoctoproject.org/wiki/Releases)); last change 2025-09-03 | No: it holds only layer and CI configuration, no machines | [Qualcomm Linux 1.x support](docs/source/contributing/CONTRIBUTING.md#4--downstream-baseline--qualcomm-linux-1x) |
| **kirkstone** | Qualcomm Linux <= 1.3, aligned with Yocto Project 4.0 (LTS). | No longer receives security fixes: [SECURITY.md](SECURITY.md) covers only current LTS releases, and Yocto Project 4.0 is end of life ([releases](https://wiki.yoctoproject.org/wiki/Releases)); last change 2025-04-09 | No: it holds only layer and CI configuration, no machines | Not documented |
| **next** | Not documented | Not documented; last change 2026-08-20 | Not documented; it holds the `radxa-dragon-q6a`, `uno-q`, and `ventuno-q` machines | Not documented |

This table lists every branch in the upstream repository.
[BRANCHES.md](BRANCHES.md) describes how the long-lived branches relate to `main`.

## Machine Support

See [conf/machine](conf/machine/README.md) for the complete list of supported devices.

## Documentation

Build the documentation site with `make -f docs/source/Makefile setup html` from
the repository root, then open `docs/site/index.html` directly in a browser. The
[documentation guide](docs/README.md) explains where its source lives.

- [Usage tutorial](docs/source/user/USAGE.md) — Build an image for a supported board, or add the layer to an existing build.
- [Configuration reference](docs/source/user/CONFIGURATION.md) — Understand the layer, machine, kas, and workflow settings.
- [Development setup](docs/source/contributing/DEVELOPMENT.md) — Prepare a checkout, run the layer checks, and build the documentation.
- [Function reference](docs/source/contributing/README.md#function-reference) — Browse the documented shell functions and BitBake tasks in the built site.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) for where to submit patches and how
they are reviewed. Follow the [Code of Conduct](CODE_OF_CONDUCT.md) when
participating.

## Communication

- **GitHub Issues:** [meta-qcom-3rdparty issues](https://github.com/qualcomm-linux/meta-qcom-3rdparty/issues)
- **Pull Requests:** [meta-qcom-3rdparty pull requests](https://github.com/qualcomm-linux/meta-qcom-3rdparty/pulls)

## Maintainer(s)

- Ricardo Salveti <ricardo.salveti@oss.qualcomm.com>
- Nicolas Dechesne <nicolas.dechesne@oss.qualcomm.com>

## License

This layer is licensed under the MIT license. Check out [LICENSE](LICENSE)
for more details. [NOTICE](NOTICE) retains the notices for the documentation
tools and templates adapted from other projects.

## Folders

- [.github/](.github/) — Holds [CODEOWNERS](.github/CODEOWNERS), issue and pull request templates, CI workflows, and the documentation build scripts.
- [ci/](ci/README.md) — Contains the kas build fragments and the scripts CI uses to check the layer.
- [conf/](conf/README.md) — Declares the layer and its machine configurations.
- [docs/](docs/README.md) — Contains the documentation source and explains how to build the site.
- [dynamic-layers/](dynamic-layers/README.md) — Holds metadata that applies only when another layer is in the build.
- [recipes-bsp/](recipes-bsp/README.md) — Contains the board firmware and packagegroup recipes.
- [recipes-kernel/](recipes-kernel/README.md) — Adapts the Linux kernel recipe for the supported boards.

## Files

- [README.md](README.md) — Introduces the layer, its branches, and its contents.
- [AGENTS.md](AGENTS.md) — Points automation agents to the agent guide.
- [BRANCHES.md](BRANCHES.md) — Describes how each long-lived branch relates to `main`.
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) — States participation standards and how to report conduct concerns.
- [CONTRIBUTING.md](CONTRIBUTING.md) — Points to the contribution guide and development setup.
- [LICENSE](LICENSE) — Contains the MIT licence.
- [NOTICE](NOTICE) — Retains the notices for the adapted documentation tools and templates.
- [SECURITY.md](SECURITY.md) — Explains how to report vulnerabilities privately.
- [.env.example](.env.example) — Documents the optional environment settings for kas builds and checks.
- [.gitignore](.gitignore) — Keeps local settings and generated documentation out of version control.
