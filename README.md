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

With Docker and [kas-container](https://kas.readthedocs.io/en/latest/userguide/kas-container.html)
installed, build `core-image-base` for the Thundercomm RUBIK Pi 3 from the
repository root:

```sh
kas-container build ci/rubikpi3.yml
```

The [build tutorial](docs/source/user/USAGE.md) lists the prerequisites, the
expected output, and how long the first build takes.

## Branches

| Branch | Purpose | Status | Build from it | Contributions |
| --- | --- | --- | --- | --- |
| `main` | Primary development branch, with focus on upstream support and compatibility with the most recent Yocto Project release. | Development; compatible with the `blacksail` release series ([Yocto Project 6.1](https://wiki.yoctoproject.org/wiki/Releases)) | Yes: `radxa-dragon-q6a` and `rubikpi3` | [Default target](docs/source/contributing/CONTRIBUTING.md#branches-and-backports) |
| `wrynose` | LTS branch based on the Yocto Project 6.0 release, used by Qualcomm Linux 2.x. | Long-term support; [Yocto Project 6.0](https://wiki.yoctoproject.org/wiki/Releases) is supported until April 2030 | Yes: `radxa-dragon-q6a` and `rubikpi3` | [Backports from `main`](docs/source/contributing/CONTRIBUTING.md#branches-and-backports) |
| `scarthgap` | Qualcomm Linux >= 1.4, aligned with Yocto Project 5.0 (LTS). | [Yocto Project 5.0](https://wiki.yoctoproject.org/wiki/Releases) is supported until April 2028; [last commit](https://github.com/qualcomm-linux/meta-qcom-3rdparty/commits/scarthgap) 2025-09-03 | No board support to build: the branch holds only `conf/layer.conf` and CI configuration | [Qualcomm Linux 1.x changes](docs/source/contributing/CONTRIBUTING.md#branches-and-backports) |
| `kirkstone` | Qualcomm Linux <= 1.3, aligned with Yocto Project 4.0 (LTS). | [Yocto Project 4.0](https://wiki.yoctoproject.org/wiki/Releases) is end of life; [last commit](https://github.com/qualcomm-linux/meta-qcom-3rdparty/commits/kirkstone) 2025-04-09 | No board support to build: the branch holds only `conf/layer.conf` and CI configuration | [SECURITY.md](SECURITY.md) accepts patches only for LTS releases and `main`; [see the guide](docs/source/contributing/CONTRIBUTING.md#branches-and-backports) |
| `next` | Not documented | Not documented; [last commit](https://github.com/qualcomm-linux/meta-qcom-3rdparty/commits/next) 2026-08-20 | Not documented; it holds the `radxa-dragon-q6a`, `uno-q`, and `ventuno-q` machines for the `wrynose` release series | [Not documented](docs/source/contributing/CONTRIBUTING.md#branches-and-backports) |

This table lists every branch. [BRANCHES.md](BRANCHES.md)
describes how the long-lived branches relate to `main`.

## Machine Support

See [`conf/machine`](conf/machine/README.md) for the complete list of supported devices.

## Documentation

Build the documentation site with `make -f docs/source/Makefile setup html` from
the repository root, after installing its
[prerequisites](docs/source/contributing/DEVELOPMENT.md#prerequisites), then open
`docs/site/index.html` directly in a browser. The
[documentation guide](docs/README.md) explains where its source lives.

- [Build tutorial](docs/source/user/USAGE.md): build an image for a supported board.
- [Configuration reference](docs/source/user/CONFIGURATION.md): the layer, machine, recipe, kas, and environment settings.
- [Development setup](docs/source/contributing/DEVELOPMENT.md): install the documentation tools, build, and check locally.

## Contributing

Please read [the contribution guide](docs/source/contributing/CONTRIBUTING.md) for the contribution
workflow, the layer scope rules and the commit subject and message
requirements before opening a pull request.

## Communication

- **GitHub Issues:** [meta-qcom-3rdparty issues](https://github.com/qualcomm-linux/meta-qcom-3rdparty/issues)
- **Pull Requests:** [meta-qcom-3rdparty pull requests](https://github.com/qualcomm-linux/meta-qcom-3rdparty/pulls)

Report vulnerabilities privately through [SECURITY.md](SECURITY.md).

## Maintainer(s)

- Ricardo Salveti <ricardo.salveti@oss.qualcomm.com>
- Nicolas Dechesne <nicolas.dechesne@oss.qualcomm.com>

## License

This layer is licensed under the MIT license. Check out [LICENSE](LICENSE)
for more details. [NOTICE](NOTICE) keeps the licence notices for the
documentation tools and templates adapted from other projects.

## Folders

- [.github/](.github/) — Holds [CODEOWNERS](.github/CODEOWNERS), the [issue templates](.github/ISSUE_TEMPLATE/), the [pull request template](.github/PULL_REQUEST_TEMPLATE/pr_template.md), the CI workflows, and the documentation helper scripts.
- [ci/](ci/README.md) — Holds the kas build fragments and the scripts CI runs for layer checks.
- [conf/](conf/README.md) — Holds the layer configuration and the machine definitions.
- [docs/](docs/README.md) — Contains the documentation source and explains how to build the site.
- [dynamic-layers/](dynamic-layers/README.md) — Holds appends that apply only when another layer is present.
- [recipes-bsp/](recipes-bsp/README.md) — Holds board firmware and package group recipes.
- [recipes-kernel/](recipes-kernel/README.md) — Holds the kernel append and its configuration fragments.

## Files

- [README.md](README.md) — Introduces the layer, its branches, and its contents.
- [AGENTS.md](AGENTS.md) — Points automation agents to the agent guide.
- [CLAUDE.md](CLAUDE.md) — Links to `AGENTS.md` for tools that read this name.
- [BRANCHES.md](BRANCHES.md) — Describes how each long-lived branch is maintained and relates to `main`.
- [CONTRIBUTING.md](CONTRIBUTING.md) — Points to the contribution guide.
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) — States participation standards and how to report conduct concerns.
- [SECURITY.md](SECURITY.md) — Explains how to report vulnerabilities and which branches receive security fixes.
- [LICENSE](LICENSE) — Contains the layer's MIT licence.
- [NOTICE](NOTICE) — Keeps the licence notices for adapted documentation tools and templates.
- [.env.example](.env.example) — Documents the environment settings for kas builds and how to load them.
- [.gitignore](.gitignore) — Keeps local environment files, the documentation tools, and the generated site out of version control.

<!-- repository-map:start -->

## Repository map

```mermaid
flowchart LR
    r0["meta-qcom-3rdparty (you are here)"]
    click r0 href "https://github.com/qualcomm-linux/meta-qcom-3rdparty" _blank
    r1["kernel"]
    click r1 href "https://github.com/qualcomm-linux/kernel" _blank
    r2["meta-ai"]
    click r2 href "https://github.com/qualcomm-linux/meta-ai" _blank
    r3["meta-qcom"]
    click r3 href "https://github.com/qualcomm-linux/meta-qcom" _blank
    r4["meta-qcom-distro"]
    click r4 href "https://github.com/qualcomm-linux/meta-qcom-distro" _blank
    r5["meta-qcom-hwe"]
    click r5 href "https://github.com/qualcomm-linux/meta-qcom-hwe" _blank
    r6["qcom-ptool"]
    click r6 href "https://github.com/qualcomm-linux/qcom-ptool" _blank
    r7["fastrpc"]
    click r7 href "https://github.com/qualcomm/fastrpc" _blank
    r0 -->|"adds third-party board support to"| r3
    r0 -->|"builds on (scarthgap)"| r5
    r0 -->|"can use Qualcomm Linux settings from"| r4
    r3 -->|"gets partition tools from"| r6
    r3 -->|"fetches Linux kernel sources from"| r1
    r3 -->|"adds recipes when combined with"| r2
    r3 -->|"adds recipes when combined with"| r4
    r3 -->|"fetches sources from"| r7
    style r0 fill:#e6f3ff,stroke:#0969da,stroke-width:3px,color:#182c43
```

[Full Qualcomm repository map](https://github.com/devdocsorg/qualcomm-repository-map).

<!-- Generated from https://github.com/devdocsorg/qualcomm-repository-map at 4540c908de04298d6455f07df2763bcf7e1b874e; dataset SHA-256: c7c7eecf7ffa34b0dcce1a19f6251dde20304522d0063a2b3695b5645d5ef518. -->

<!-- repository-map:end -->
