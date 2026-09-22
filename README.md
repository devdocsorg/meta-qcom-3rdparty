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
supported by Qualcomm are available via [meta-qcom](https://github.com/qualcomm-linux/meta-qcom) instead.

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

## First build and documentation

Start with the [development environment](docs/source/contributing/DEVELOPMENT.md).
From the checkout root, build RUBIK Pi 3 with `kas-container build ci/rubikpi3.yml`.
Follow the [image tutorial](docs/source/user/USAGE.md) to inspect the output.
Open [docs/site/index.html](docs/site/index.html) directly for offline guides,
configuration, and native function references.

## Branches

- **main:** Primary development branch, with focus on upstream support and
  compatibility with the most recent Yocto Project release.
- **wrynose:** LTS branch based on the Yocto Project 6.0 release, used by
  Qualcomm Linux 2.x.
- **scarthgap:** Qualcomm Linux >= 1.4, aligned with Yocto Project 5.0 (LTS).
- **kirkstone:** Qualcomm Linux <= 1.3, aligned with Yocto Project 4.0 (LTS).

See [branch maintenance](BRANCHES.md) for the upstream/fork relationship,
release contribution routes, and the complete fork branch inventory.
`next` is an upstream integration branch; use `main` for routine development.
`docs/contributor-reference` is this fork’s runnable documentation review branch.

### Fork topic branches

Each topic below is a fork integration or review branch, not a supported release.
Build it only to work on its named subject; ordinary contributions go upstream
as described in [branch maintenance](BRANCHES.md).

| Branches | Purpose and status |
| --- | --- |
| `devdocs/main`, `devdocs/build` | Fork integration and build work; review with the topic author before depending on it. |
| `devdocs/docs-v3`, `devdocs/generated-tutorials`, `devdocs/required-files-sphinx`, `devdocs/source-file-docs`, `devdocs/wrynose/docs`, `devdocs/wrynose/docs-v2` | Documentation topics; use only to review those proposals. |
| `docs/offline-layer-guides`, `docs/qli-2-tutorials`, `docs/repository-documentation`, `test/qualcomm-upgrade-astra`, `docs/contributor-reference` | Documentation review/test topics; this guide's runnable setup selects `docs/contributor-reference`. |
| `devdocs/imx219-cam2` | Camera integration topic; not the upstream board baseline. |
| `devdocs/s3-cache-backup` | Build-cache integration topic; not a release branch. |
| `devdocs/vscode` | Editor integration topic; not a release branch. |
| `radxa-dragon-q6a-hdmi`, `radxa-dragon-q6a-hdmi-cmdline-extra`, `radxa-dragon-q6a-hdmi-deferred-config`, `radxa-dragon-q6a-hdmi-uki-cmdline` | Radxa display bring-up topics; use only for that investigation. |
| `njjetha` | Personal topic with no declared release role; confirm its purpose with the author before use. |
| `upstream` | Separately maintained raw upstream baseline for fork review; do not send contributions here. |

## Machine Support

See [conf/machine](conf/machine/README.md) for the complete list of supported devices.

## Contributing

Please submit any patches against the `meta-qcom-3rdparty` layer by using
the GitHub pull-request feature. Fork the repo, create a branch,
do the work, rebase from upstream, and create the pull request.

For some useful guidelines when submitting patches, please refer to:
[Preparing Changes for Submission](https://docs.yoctoproject.org/dev/contributor-guide/submit-changes.html#preparing-changes-for-submission)

Pull requests will be discussed within the GitHub pull-request infrastructure.
See [CONTRIBUTING.md](CONTRIBUTING.md) for the contribution guide and required checks.

## Communication

- **GitHub Issues:** [meta-qcom-3rdparty issues](https://github.com/qualcomm-linux/meta-qcom-3rdparty/issues)
- **Pull Requests:** [meta-qcom-3rdparty pull requests](https://github.com/qualcomm-linux/meta-qcom-3rdparty/pulls)

## Maintainer(s)

- Ricardo Salveti <ricardo.salveti@oss.qualcomm.com>
- Nicolas Dechesne <nicolas.dechesne@oss.qualcomm.com>

Documentation reviews use the existing [CODEOWNERS](.github/CODEOWNERS).
Participants follow the [Code of Conduct](CODE_OF_CONDUCT.md); report
vulnerabilities privately through [SECURITY.md](SECURITY.md).

## License

This layer is licensed under the MIT license. Check out [LICENSE](LICENSE)
for more details. Imported documentation material has separate
[third-party notices](THIRD_PARTY_NOTICES.md).

## Folders

- [.github/](.github/) — Owns review templates, code ownership, validation tools, and CI workflows.
- [ci/](ci/README.md) — kas build compositions and CI helper scripts.
- [conf/](conf/README.md) — BitBake layer and machine configuration.
- [docs/](docs/README.md) — Documentation source and committed offline output.
- [dynamic-layers/](dynamic-layers/README.md) — Metadata enabled by optional layer collections.
- [recipes-bsp/](recipes-bsp/README.md) — Board firmware and packagegroup recipes.
- [recipes-kernel/](recipes-kernel/README.md) — Machine-specific kernel additions.

## Files

- [.env.example](.env.example) — Documents safe shell environment values without automatic loading.
- [.gitignore](.gitignore) — Excludes local environments, downloaded tools, and build intermediates.
- [AGENTS.md](AGENTS.md) — Directs automation to its authoritative instructions.
- [BRANCHES.md](BRANCHES.md) — Explains branch maintenance and contribution destinations.
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) — Defines participant conduct and private reporting.
- [CONTRIBUTING.md](CONTRIBUTING.md) — Directs contributors to the maintained contribution procedure.
- [COPYING.MIT](COPYING.MIT) — Retains the approved MIT licence text.
- [LICENSE](LICENSE) — Resolves to the approved MIT licence in COPYING.MIT.
- [README.md](README.md) — Describes this folder and indexes its contents.
- [SECURITY.md](SECURITY.md) — Provides private vulnerability reporting and support policy.
- [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) — Preserves full notices for reused documentation material.

<!-- repository-map:start -->

## Repository map

```mermaid
flowchart LR
    r0["meta-qcom-3rdparty (you are here)"]
    click r0 href "https://github.com/qualcomm-linux/meta-qcom-3rdparty" _blank
    r1["meta-audioreach"]
    click r1 href "https://github.com/AudioReach/meta-audioreach" _blank
    r2["uv"]
    click r2 href "https://github.com/astral-sh/uv" _blank
    r3["MyST-Parser"]
    click r3 href "https://github.com/executablebooks/MyST-Parser" _blank
    r4["gawk"]
    click r4 href "https://git.savannah.gnu.org/cgit/gawk.git/" _blank
    r5["bashlex"]
    click r5 href "https://github.com/idank/bashlex" _blank
    r6["playwright-python"]
    click r6 href "https://github.com/microsoft/playwright-python" _blank
    r7["bitbake"]
    click r7 href "https://github.com/openembedded/bitbake" _blank
    r8["meta-openembedded"]
    click r8 href "https://github.com/openembedded/meta-openembedded" _blank
    r9["openembedded-core"]
    click r9 href "https://github.com/openembedded/openembedded-core" _blank
    r10["cpython"]
    click r10 href "https://github.com/python/cpython" _blank
    r11["kernel"]
    click r11 href "https://github.com/qualcomm-linux/kernel" _blank
    r12["meta-ai"]
    click r12 href "https://github.com/qualcomm-linux/meta-ai" _blank
    r13["meta-qcom"]
    click r13 href "https://github.com/qualcomm-linux/meta-qcom" _blank
    r14["meta-qcom-distro"]
    click r14 href "https://github.com/qualcomm-linux/meta-qcom-distro" _blank
    r15["qcom-ptool"]
    click r15 href "https://github.com/qualcomm-linux/qcom-ptool" _blank
    r16["shdoc"]
    click r16 href "https://github.com/reconquest/shdoc" _blank
    r17["boot-assets"]
    click r17 href "https://github.com/rubikpi-ai/boot-assets" _blank
    r18["kas"]
    click r18 href "https://github.com/siemens/kas" _blank
    r19["sphinx"]
    click r19 href "https://github.com/sphinx-doc/sphinx" _blank
    r20["meta-updater"]
    click r20 href "https://github.com/uptane/meta-updater" _blank
    r21["meta-security"]
    click r21 href "https://git.yoctoproject.org/meta-security" _blank
    r22["meta-selinux"]
    click r22 href "https://git.yoctoproject.org/meta-selinux" _blank
    r23["meta-virtualization"]
    click r23 href "https://git.yoctoproject.org/meta-virtualization" _blank
    r0 -->|"uses base Linux build recipes from"| r9
    r0 -->|"adds third-party board support to"| r13
    r0 -->|"can use Qualcomm Linux settings from"| r14
    r13 -->|"gets partition tools from"| r15
    r0 -->|"fetches RUBIK Pi boot firmware from"| r17
    r0 -->|"sets up and runs builds with"| r18
    r13 -->|"includes for Qualcomm Linux images"| r1
    r13 -->|"runs build tasks with"| r7
    r13 -->|"includes for Qualcomm Linux images"| r8
    r13 -->|"fetches Linux kernel sources from"| r11
    r13 -->|"includes for Qualcomm Linux images"| r12
    r13 -->|"includes for Qualcomm Linux images"| r23
    r13 -->|"includes for Qualcomm Linux images"| r22
    r13 -->|"includes for Qualcomm Linux images"| r21
    r13 -->|"includes for Qualcomm Linux images"| r20
    r0 -->|"generates shell reference with"| r16
    r0 -->|"builds documentation with"| r19
    r0 -->|"parses Markdown with"| r3
    r0 -->|"checks offline browsing with"| r6
    r0 -->|"checks shell coverage with"| r5
    r0 -->|"sets up documentation with"| r2
    r0 -->|"runs documentation tools with"| r10
    r0 -->|"runs shell extraction with"| r4
    style r0 fill:#e6f3ff,stroke:#0969da,stroke-width:3px,color:#182c43
```

[Full Qualcomm repository map](https://github.com/devdocsorg/qualcomm-repository-map).

<!-- Generated from https://github.com/devdocsorg/qualcomm-repository-map at 292d855cabcc72bc52a0ac8a2504f3c1e89e1b84; dataset SHA-256: e9edd3db51efccb03c67457eb648e4b66097a83dda9cc341da4efa418e10a97d. -->

<!-- repository-map:end -->
