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

See `conf/machine` for the complete list of supported devices.

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
