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

## Getting Started

Follow the [usage tutorial](docs/source/contributing/USAGE.md) to prepare the workspace. Then inspect
the selected build configuration:

```sh
kas-container dump ci/radxa-dragon-q6a.yml
```

The [documentation guide](docs/README.md) links the tutorial, configuration
documentation, and the Sphinx build for the generated function reference.

Open `docs/site/index.html` directly in a browser for the locally browsable site.
See the [nearby repository map](docs/source/user/REPOSITORY_MAP.md) for this layer's
place in the Qualcomm ecosystem, and [development environment setup](docs/source/contributing/DEVELOPMENT.md)
to prepare a contributor checkout and the documentation toolchain.

## Branches

- **main:** Primary development branch, with focus on upstream support and
  compatibility with the most recent Yocto Project release.
- **wrynose:** LTS branch based on the Yocto Project 6.0 release, used by
  Qualcomm Linux 2.x.
- **scarthgap:** Qualcomm Linux >= 1.4, aligned with Yocto Project 5.0 (LTS).
- **kirkstone:** Qualcomm Linux <= 1.3, aligned with Yocto Project 4.0 (LTS).

- **next:** CI and workflow validation before changes land on `main`;
  use for testing and send new contributions through the `main` review process.

See [BRANCHES.md](BRANCHES.md) for branch relationships.

## Machine Support

See `conf/machine` for the complete list of supported devices.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) for the contribution guidelines.

Please submit any patches against the `meta-qcom-3rdparty` layer by using
the GitHub pull-request feature. Fork the repo, create a branch,
do the work, rebase from upstream, and create the pull request.

For some useful guidelines when submitting patches, please refer to:
[Preparing Changes for Submission](https://docs.yoctoproject.org/dev/contributor-guide/submit-changes.html#preparing-changes-for-submission)

Pull requests will be discussed within the GitHub pull-request infrastructure.

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

- [.github/](.github/): GitHub configuration, ownership, and contribution templates.
- [ci/](ci/README.md): Container helper scripts and kas configuration fragments.
- [conf/](conf/README.md): Layer registration and machine configuration.
- [docs/](docs/README.md): Documentation sources and the generated Sphinx website.
- [dynamic-layers/](dynamic-layers/README.md): Appends enabled only by matching optional layer collections.
- [recipes-bsp/](recipes-bsp/README.md): Board boot firmware and package groups.
- [recipes-kernel/](recipes-kernel/README.md): Kernel appends and configuration fragments.
- [skills/](skills/README.md): Points to skill documentation in the contributor guides.

## Files

- [.env.example](.env.example): Documents optional host paths with safe shell defaults.
- [.gitignore](.gitignore): Excludes local settings and generated documentation files.
- [AGENTS.md](AGENTS.md): Points to the agent instructions in the contributor documentation.
- [BRANCHES.md](BRANCHES.md): Documents branch purpose, maintenance, and integration relationships.
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md): Defines participation standards and reporting.
- [CONTRIBUTING.md](CONTRIBUTING.md): Links the existing contribution guide and named PR template.
- [LICENSE](LICENSE): Contains the MIT licence and original copyright notice.
- [README.md](README.md): Introduces this directory and lists its contents.
- [SECURITY.md](SECURITY.md): Routes private vulnerability reports to the appropriate maintainers.
