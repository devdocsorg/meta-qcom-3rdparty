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
supported by Qualcomm are available via `meta-qcom` instead.

To build an image for a supported board, follow the
[usage tutorial](docs/source/user/USAGE.md).

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

## Branches

- **main:** Primary development branch, with focus on upstream support and
  compatibility with the most recent Yocto Project release.
- **wrynose:** LTS branch based on the Yocto Project 6.0 release, used by
  Qualcomm Linux 2.x.
- **scarthgap:** Qualcomm Linux >= 1.4, aligned with Yocto Project 5.0 (LTS).
- **kirkstone:** Qualcomm Linux <= 1.3, aligned with Yocto Project 4.0 (LTS).
- **next:** Staging branch for validating CI workflow changes; do not build
  from it or send contributions to it.

Build from `main` or from the branch matching your Qualcomm Linux release, and
send contributions to `main`. The backport workflow creates temporary
`backport/<number>-to-wrynose` branches for its pull requests.
[BRANCHES.md](BRANCHES.md) describes each branch's status and maintenance.

## Machine Support

See [conf/machine](conf/machine/README.md) for the complete list of supported devices.

## Documentation

Open [docs/site/index.html](docs/site/index.html) directly in a browser for the
generated documentation site; the [documentation guide](docs/README.md)
explains where its source lives and how to rebuild it.

- [Usage tutorial](docs/source/user/USAGE.md) — Build an image for a supported board and find the output.
- [Configuration reference](docs/source/user/CONFIGURATION.md) — Layer, machine, kas, environment, and workflow settings.
- [Development setup](docs/source/contributing/DEVELOPMENT.md) — Install the documentation tools and run the local checks.
- [Function reference](docs/source/contributing/README.md#function-reference) — Shell functions and BitBake tasks, generated from their comments.

## Contributing

Please submit any patches against the `meta-qcom-3rdparty` layer by using
the GitHub pull-request feature. Fork the repo, create a branch,
do the work, rebase from upstream, and create the pull request.

For some useful guidelines when submitting patches, please refer to:
[Preparing Changes for Submission](https://docs.yoctoproject.org/dev/contributor-guide/submit-changes.html#preparing-changes-for-submission)

Pull requests will be discussed within the GitHub pull-request infrastructure.

Read [CONTRIBUTING.md](CONTRIBUTING.md) for the contribution guide and
development setup, and follow the [Code of Conduct](CODE_OF_CONDUCT.md).
Report vulnerabilities privately as described in [SECURITY.md](SECURITY.md).

## Communication

- **GitHub Issues:** [meta-qcom-3rdparty issues](https://github.com/qualcomm-linux/meta-qcom-3rdparty/issues)
- **Pull Requests:** [meta-qcom-3rdparty pull requests](https://github.com/qualcomm-linux/meta-qcom-3rdparty/pulls)

## Maintainer(s)

- Ricardo Salveti <ricardo.salveti@oss.qualcomm.com>
- Nicolas Dechesne <nicolas.dechesne@oss.qualcomm.com>

## License

This layer is licensed under the MIT license. Check out [LICENSE](LICENSE)
for more details. [NOTICE](NOTICE) lists the licences of reused documentation
tooling and templates.

## Folders

- [.github/](.github/) — Holds [CODEOWNERS](.github/CODEOWNERS), issue and pull request templates, CI workflows, the markdownlint configuration, and the documentation check scripts.
- [ci/](ci/README.md) — Contains kas fragments and the helper scripts CI runs.
- [conf/](conf/README.md) — Contains the layer configuration and machine definitions.
- [docs/](docs/README.md) — Contains the documentation source and the generated site.
- [dynamic-layers/](dynamic-layers/README.md) — Contains additions that apply only when another layer is present.
- [recipes-bsp/](recipes-bsp/README.md) — Contains board firmware and packagegroup recipes.
- [recipes-kernel/](recipes-kernel/README.md) — Contains kernel appends and configuration fragments.

## Files

- [README.md](README.md) — Introduces the layer, its branches, documentation, and maintainers.
- [BRANCHES.md](BRANCHES.md) — Describes each long-lived branch and how it is maintained.
- [CONTRIBUTING.md](CONTRIBUTING.md) — Points to the contribution guide and development setup.
- [AGENTS.md](AGENTS.md) — Points automation agents to the agent guide.
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) — States participation standards and how to report conduct concerns.
- [SECURITY.md](SECURITY.md) — Explains how to report security issues and which branches receive fixes.
- [LICENSE](LICENSE) — Contains the layer's MIT licence.
- [NOTICE](NOTICE) — Contains the licence notices for reused documentation tooling and templates.
- [.env.example](.env.example) — Lists the environment settings for kas-container builds with safe example values.
- [.gitignore](.gitignore) — Keeps local environment files, the documentation environment, and build caches out of version control.

<!-- repository-map:start -->

## Repository map

```mermaid
flowchart LR
    r0["meta-qcom-3rdparty (you are here)"]
    click r0 href "https://github.com/qualcomm-linux/meta-qcom-3rdparty" _blank
    r1["meta-audioreach"]
    click r1 href "https://github.com/AudioReach/meta-audioreach" _blank
    r2["linux-firmware"]
    click r2 href "https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git" _blank
    r3["dsp-binaries"]
    click r3 href "https://github.com/linux-msm/dsp-binaries" _blank
    r4["qrtr"]
    click r4 href "https://github.com/linux-msm/qrtr" _blank
    r5["rmtfs"]
    click r5 href "https://github.com/linux-msm/rmtfs" _blank
    r6["tqftpserv"]
    click r6 href "https://github.com/linux-msm/tqftpserv" _blank
    r7["bitbake"]
    click r7 href "https://github.com/openembedded/bitbake" _blank
    r8["meta-openembedded"]
    click r8 href "https://github.com/openembedded/meta-openembedded" _blank
    r9["openembedded-core"]
    click r9 href "https://github.com/openembedded/openembedded-core" _blank
    r10["kernel"]
    click r10 href "https://github.com/qualcomm-linux/kernel" _blank
    r11["meta-ai"]
    click r11 href "https://github.com/qualcomm-linux/meta-ai" _blank
    r12["meta-qcom"]
    click r12 href "https://github.com/qualcomm-linux/meta-qcom" _blank
    r13["meta-qcom-distro"]
    click r13 href "https://github.com/qualcomm-linux/meta-qcom-distro" _blank
    r14["qcom-ptool"]
    click r14 href "https://github.com/qualcomm-linux/qcom-ptool" _blank
    r15["fastrpc"]
    click r15 href "https://github.com/qualcomm/fastrpc" _blank
    r16["boot-assets"]
    click r16 href "https://github.com/rubikpi-ai/boot-assets" _blank
    r17["kas"]
    click r17 href "https://github.com/siemens/kas" _blank
    r18["systemd"]
    click r18 href "https://github.com/systemd/systemd" _blank
    r19["meta-updater"]
    click r19 href "https://github.com/uptane/meta-updater" _blank
    r20["meta-security"]
    click r20 href "https://git.yoctoproject.org/meta-security" _blank
    r21["meta-selinux"]
    click r21 href "https://git.yoctoproject.org/meta-selinux" _blank
    r22["meta-virtualization"]
    click r22 href "https://git.yoctoproject.org/meta-virtualization" _blank
    r0 -->|"uses base Linux build recipes from"| r9
    r0 -->|"adds third-party board support to"| r12
    r0 -->|"can use Qualcomm Linux settings from"| r13
    r12 -->|"gets partition tools from"| r14
    r0 -->|"fetches RUBIK Pi boot firmware from"| r16
    r0 -->|"sets up and runs builds with"| r17
    r12 -->|"includes for Qualcomm Linux images"| r1
    r12 -->|"runs build tasks with"| r7
    r12 -->|"includes for Qualcomm Linux images"| r8
    r12 -->|"fetches Linux kernel sources from"| r10
    r12 -->|"includes for Qualcomm Linux images"| r11
    r12 -->|"includes for Qualcomm Linux images"| r22
    r12 -->|"includes for Qualcomm Linux images"| r21
    r12 -->|"includes for Qualcomm Linux images"| r20
    r12 -->|"includes for Qualcomm Linux images"| r19
    r12 -->|"fetches sources from"| r4
    r12 -->|"fetches sources from"| r5
    r12 -->|"fetches sources from"| r6
    r12 -->|"fetches sources from"| r15
    r12 -->|"fetches sources from"| r3
    r9 -->|"fetches sources from"| r2
    r12 -->|"uses base Linux build recipes from"| r9
    r9 -->|"fetches sources from"| r18
    style r0 fill:#e6f3ff,stroke:#0969da,stroke-width:3px,color:#182c43
```

[Full Qualcomm repository map](https://github.com/devdocsorg/qualcomm-repository-map).

<!-- Generated from https://github.com/devdocsorg/qualcomm-repository-map at 6516f060326ce5ac5708e4bd52b6eade17dd4652; dataset SHA-256: faeaa003512a56069acce7f99fbd2c42eb6d67bc29591a2f449a5e399f0b5028. -->

<!-- repository-map:end -->
