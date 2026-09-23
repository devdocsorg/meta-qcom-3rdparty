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

Follow the [development setup](docs/source/contributing/DEVELOPMENT.md), then run
`kas-container build ci/rubikpi3.yml` from the checkout root. The
[image tutorial](docs/source/user/USAGE.md) explains how to inspect the output.
Browse the [reference documentation](docs/site/index.html) directly from a local
checkout, or read its [source homepage](docs/source/README.md).

## Branches

- **main:** Primary development branch, with focus on upstream support and
  compatibility with the most recent Yocto Project release.
- **wrynose:** LTS branch based on the Yocto Project 6.0 release, used by
  Qualcomm Linux 2.x.
- **scarthgap:** Qualcomm Linux >= 1.4, aligned with Yocto Project 5.0 (LTS).
- **kirkstone:** Qualcomm Linux <= 1.3, aligned with Yocto Project 4.0 (LTS).

The upstream `next` branch integrates changes for testing before `main`; use it
for integration validation and send normal contributions to `main`.
The release branches above are maintained separately; choose matching layers when
building and send release fixes to the matching branch. The fork's `upstream`
branch retains its imported baseline, and `docs/offline-guides-and-layer-map` is
this documentation review branch. Long-lived maintenance relationships are in
[BRANCHES.md](BRANCHES.md); the canonical location after adoption is
[BRANCHES.md on main](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/main/BRANCHES.md).

## Machine Support

See [conf/machine](conf/machine/README.md) for the complete list of supported devices.

## Contributing

Please submit any patches against the `meta-qcom-3rdparty` layer by using
the GitHub pull-request feature. Fork the repo, create a branch,
do the work, rebase from upstream, and create the pull request.

For some useful guidelines when submitting patches, please refer to:
[Preparing Changes for Submission](https://docs.yoctoproject.org/dev/contributor-guide/submit-changes.html#preparing-changes-for-submission)

Pull requests will be discussed within the GitHub pull-request infrastructure.

Read the [contribution procedure](CONTRIBUTING.md) for project scope and setup.

## Communication

- **GitHub Issues:** [meta-qcom-3rdparty issues](https://github.com/qualcomm-linux/meta-qcom-3rdparty/issues)
- **Pull Requests:** [meta-qcom-3rdparty pull requests](https://github.com/qualcomm-linux/meta-qcom-3rdparty/pulls)

## Maintainer(s)

- Ricardo Salveti <ricardo.salveti@oss.qualcomm.com>
- Nicolas Dechesne <nicolas.dechesne@oss.qualcomm.com>

## License

This layer is licensed under the MIT license. Check out [LICENSE](LICENSE)
for more details.

## Folders

- [.github](.github) — Owns workflows, issue and PR templates, review ownership, and documentation tooling.
- [ci](ci/README.md) — Contains kas compositions and CI helper scripts.
- [conf](conf/README.md) — Defines layer discovery and supported machines.
- [docs](docs/README.md) — Contains documentation sources and generated output.
- [dynamic-layers](dynamic-layers/README.md) — Activates extensions for optional distribution layers.
- [recipes-bsp](recipes-bsp/README.md) — Supplies board firmware and packagegroups.
- [recipes-kernel](recipes-kernel/README.md) — Extends the upstream kernel for supported boards.

## Files

- [.env.example](.env.example) — Documents safe optional build environment exports.
- [.gitignore](.gitignore) — Excludes secrets and local build environments.
- [AGENTS.md](AGENTS.md) — Directs automation to the maintained agent procedure.
- [BRANCHES.md](BRANCHES.md) — Explains branch purposes and maintenance relationships.
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) — Defines community conduct and private reporting.
- [CONTRIBUTING.md](CONTRIBUTING.md) — Links the contribution procedure and development setup.
- [COPYING.MIT](COPYING.MIT) — Contains the layer’s approved MIT licence text.
- [LICENSE](LICENSE) — Exposes the approved licence through the required discovery filename.
- [README.md](README.md) — Orients readers and indexes this folder.
- [SECURITY.md](SECURITY.md) — Explains private vulnerability reporting and supported branches.

<!-- repository-map:start -->

## Repository map

### Connections (1/2)

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

### Connections (2/2)

```mermaid
flowchart LR
    r0["meta-qcom-3rdparty (you are here)"]
    click r0 href "https://github.com/qualcomm-linux/meta-qcom-3rdparty" _blank
    r1["linux-firmware"]
    click r1 href "https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git" _blank
    r2["dsp-binaries"]
    click r2 href "https://github.com/linux-msm/dsp-binaries" _blank
    r3["qrtr"]
    click r3 href "https://github.com/linux-msm/qrtr" _blank
    r4["rmtfs"]
    click r4 href "https://github.com/linux-msm/rmtfs" _blank
    r5["tqftpserv"]
    click r5 href "https://github.com/linux-msm/tqftpserv" _blank
    r6["openembedded-core"]
    click r6 href "https://github.com/openembedded/openembedded-core" _blank
    r7["meta-qcom"]
    click r7 href "https://github.com/qualcomm-linux/meta-qcom" _blank
    r8["fastrpc"]
    click r8 href "https://github.com/qualcomm/fastrpc" _blank
    r9["systemd"]
    click r9 href "https://github.com/systemd/systemd" _blank
    r0 -->|"adds third-party board support to"| r7
    r7 -->|"packages sources from"| r3
    r7 -->|"packages sources from"| r4
    r7 -->|"packages sources from"| r5
    r7 -->|"packages sources from"| r8
    r7 -->|"packages sources from"| r2
    r0 -->|"uses base Linux build recipes from"| r6
    r6 -->|"builds EFI boot tools from"| r9
    r6 -->|"packages firmware releases from"| r1
    style r0 fill:#e6f3ff,stroke:#0969da,stroke-width:3px,color:#182c43
```

[Full Qualcomm repository map](https://github.com/devdocsorg/qualcomm-repository-map).

<!-- Generated from https://github.com/devdocsorg/qualcomm-repository-map at e7ba6a7430d9b584c9c978636903d24901c515a8; dataset SHA-256: d7dac00d05ca2eec298c967fbdbb07af974055e4da05e42a86f2ada8f859c513. -->

<!-- repository-map:end -->
