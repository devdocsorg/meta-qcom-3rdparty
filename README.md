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

## Branches

| Branch | Purpose | Status | Build from it | Contributions |
| --- | --- | --- | --- | --- |
| `main` | Primary development branch, with focus on upstream support and compatibility with the most recent Yocto Project release. | Development branch; [last change](https://github.com/qualcomm-linux/meta-qcom-3rdparty/commits/main) 2026-09-30 | Yes: [the layer's machines](conf/machine/) | Upstream-baseline changes ([contribution guide](docs/source/contributing/CONTRIBUTING.md#3--upstream-baseline)) |
| `wrynose` | LTS branch based on the Yocto Project 6.0 release, used by Qualcomm Linux 2.x. | Release branch; Yocto Project 6.0 is supported until April 2030 ([releases](https://wiki.yoctoproject.org/wiki/Releases)) | Yes: the same machines as `main` | Backports from `main`, or changes that apply only to `wrynose` ([contribution guide](docs/source/contributing/CONTRIBUTING.md#29--release-branches)) |
| `scarthgap` | Qualcomm Linux >= 1.4, aligned with Yocto Project 5.0 (LTS). | Not documented; Yocto Project 5.0 is supported until April 2028 ([releases](https://wiki.yoctoproject.org/wiki/Releases)); [last change](https://github.com/qualcomm-linux/meta-qcom-3rdparty/commits/scarthgap) 2025-09-03 | No: the branch holds only `conf/layer.conf` and CI configuration, so it has no board support to build | Qualcomm Linux 1.x downstream-baseline changes ([contribution guide](docs/source/contributing/CONTRIBUTING.md#4--downstream-baseline--qualcomm-linux-1x)) |
| `kirkstone` | Qualcomm Linux <= 1.3, aligned with Yocto Project 4.0 (LTS). | Not documented; Yocto Project 4.0 is end of life ([releases](https://wiki.yoctoproject.org/wiki/Releases)); [last change](https://github.com/qualcomm-linux/meta-qcom-3rdparty/commits/kirkstone) 2025-04-09 | No: the branch holds only `conf/layer.conf` and CI configuration | Not documented; [SECURITY.md](SECURITY.md#branches-maintained-with-security-fixes) accepts patches only for the LTS releases and `main` |
| `next` | Not documented | Not documented; [last change](https://github.com/qualcomm-linux/meta-qcom-3rdparty/commits/next) 2026-08-20 | Not documented; its tree has machine configurations for radxa-dragon-q6a, uno-q, and ventuno-q | Not documented |

[BRANCHES.md](BRANCHES.md) describes how the branches relate to `main`.

## Machine Support

See `conf/machine` for the complete list of supported devices.

## Contributing

Please read [docs/source/contributing/CONTRIBUTING.md](docs/source/contributing/CONTRIBUTING.md) for the contribution
workflow, the layer scope rules and the commit subject and message
requirements before opening a pull request.

## Communication

- **GitHub Issues:** [meta-qcom-3rdparty issues](https://github.com/qualcomm-linux/meta-qcom-3rdparty/issues)
- **Pull Requests:** [meta-qcom-3rdparty pull requests](https://github.com/qualcomm-linux/meta-qcom-3rdparty/pulls)

## Maintainer(s)

- Ricardo Salveti <ricardo.salveti@oss.qualcomm.com>
- Nicolas Dechesne <nicolas.dechesne@oss.qualcomm.com>

## License

This layer is licensed under the MIT license. Check out [LICENSE](LICENSE)
for more details.
