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
the selected [build configuration](ci/radxa-dragon-q6a.yml):

```sh
kas-container dump ci/radxa-dragon-q6a.yml
```

The [documentation guide](docs/README.md) links the tutorial,
[configuration reference](docs/source/user/CONFIGURATION.md), and the Sphinx build
for the [generated function reference](docs/source/contributing/README.md#function-reference).

Open [docs/site/index.html](docs/site/index.html) directly in a browser for the locally browsable site.
See the [nearby repository map](#repository-map) for this layer's
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

See [conf/machine](conf/machine/README.md) for the complete list of supported devices.

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

Follow the [Code of Conduct](CODE_OF_CONDUCT.md) when participating, and use the
[security policy](SECURITY.md) to report vulnerabilities.

## Maintainer(s)

- Ricardo Salveti <ricardo.salveti@oss.qualcomm.com>
- Nicolas Dechesne <nicolas.dechesne@oss.qualcomm.com>

See [CODEOWNERS](.github/CODEOWNERS) for review ownership by repository path.

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

<!-- repository-map:start -->

## Repository map

**You are here: [qualcomm-linux/meta-qcom-3rdparty](https://github.com/qualcomm-linux/meta-qcom-3rdparty)**

OpenEmbedded/Yocto Project BSP layer for Third-Party Maintained Qualcomm based platforms

### Outgoing connections

#### Depends on

- [qualcomm-linux/meta-qcom-3rdparty](https://github.com/qualcomm-linux/meta-qcom-3rdparty) → **depends on** → [openembedded/openembedded-core](https://github.com/openembedded/openembedded-core)
  - wrynose-compatible main snapshot 8927b428bcae; required layer collection.
  - [Explore openembedded/openembedded-core](https://github.com/devdocsorg/qualcomm-repository-map/blob/b17820e6a872efac49ed5a041112e6da25fdf342/maps/openembedded--openembedded-core.md) · [evidence 1](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/conf/layer.conf)
- [qualcomm-linux/meta-qcom-3rdparty](https://github.com/qualcomm-linux/meta-qcom-3rdparty) → **depends on** → [qualcomm-linux/meta-qcom](https://github.com/qualcomm-linux/meta-qcom)
  - wrynose-compatible main snapshot 8927b428bcae; required layer collection.
  - [Explore qualcomm-linux/meta-qcom](https://github.com/devdocsorg/qualcomm-repository-map/blob/b17820e6a872efac49ed5a041112e6da25fdf342/maps/qualcomm-linux--meta-qcom.md) · [evidence 1](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/conf/layer.conf)

#### Fetches source from

- [qualcomm-linux/meta-qcom-3rdparty](https://github.com/qualcomm-linux/meta-qcom-3rdparty) → **fetches source from** → [rubikpi-ai/boot-assets](https://github.com/rubikpi-ai/boot-assets)
  - RUBIK Pi 3 boot firmware only; pinned by the recipe SRCREV.
  - [Explore rubikpi-ai/boot-assets](https://github.com/devdocsorg/qualcomm-repository-map/blob/b17820e6a872efac49ed5a041112e6da25fdf342/maps/rubikpi-ai--boot-assets.md) · [evidence 1](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/recipes-bsp/firmware-boot/firmware-qcom-boot-rubikpi3_20260621.bb)

#### Integrates with

- [qualcomm-linux/meta-qcom-3rdparty](https://github.com/qualcomm-linux/meta-qcom-3rdparty) → **integrates with** → [qualcomm-linux/meta-qcom-distro](https://github.com/qualcomm-linux/meta-qcom-distro)
  - Optional: the dynamic layer applies only when qcom-distro is present.
  - [Explore qualcomm-linux/meta-qcom-distro](https://github.com/devdocsorg/qualcomm-repository-map/blob/b17820e6a872efac49ed5a041112e6da25fdf342/maps/qualcomm-linux--meta-qcom-distro.md) · [evidence 1](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/conf/layer.conf)

#### Uses automation from

- [qualcomm-linux/meta-qcom-3rdparty](https://github.com/qualcomm-linux/meta-qcom-3rdparty) → **uses automation from** → [qualcomm-linux/bitbake-lint-action](https://github.com/qualcomm-linux/bitbake-lint-action)
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [Explore qualcomm-linux/bitbake-lint-action](https://github.com/devdocsorg/qualcomm-repository-map/blob/b17820e6a872efac49ed5a041112e6da25fdf342/maps/qualcomm-linux--bitbake-lint-action.md) · [evidence 1](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/.github/workflows/bitbake-lint.yml)
- [qualcomm-linux/meta-qcom-3rdparty](https://github.com/qualcomm-linux/meta-qcom-3rdparty) → **uses automation from** → [qualcomm-linux/github-action-matrix-outputs-read](https://github.com/qualcomm-linux/github-action-matrix-outputs-read)
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [Explore qualcomm-linux/github-action-matrix-outputs-read](https://github.com/devdocsorg/qualcomm-repository-map/blob/b17820e6a872efac49ed5a041112e6da25fdf342/maps/qualcomm-linux--github-action-matrix-outputs-read.md) · [evidence 1](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/.github/workflows/test-distro.yml)
- [qualcomm-linux/meta-qcom-3rdparty](https://github.com/qualcomm-linux/meta-qcom-3rdparty) → **uses automation from** → [qualcomm-linux/github-action-matrix-outputs-write](https://github.com/qualcomm-linux/github-action-matrix-outputs-write)
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [Explore qualcomm-linux/github-action-matrix-outputs-write](https://github.com/devdocsorg/qualcomm-repository-map/blob/b17820e6a872efac49ed5a041112e6da25fdf342/maps/qualcomm-linux--github-action-matrix-outputs-write.md) · [evidence 1](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/.github/workflows/test-distro.yml)
- [qualcomm-linux/meta-qcom-3rdparty](https://github.com/qualcomm-linux/meta-qcom-3rdparty) → **uses automation from** → [qualcomm-linux/meta-qcom](https://github.com/qualcomm-linux/meta-qcom)
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [Explore qualcomm-linux/meta-qcom](https://github.com/devdocsorg/qualcomm-repository-map/blob/b17820e6a872efac49ed5a041112e6da25fdf342/maps/qualcomm-linux--meta-qcom.md) · [evidence 1](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/.github/workflows/build-yocto.yml) · [evidence 2](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/.github/workflows/build-yocto.yml) · [evidence 3](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/.github/workflows/test-distro.yml) · [evidence 4](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/.github/workflows/test-distro.yml) · [evidence 5](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/.github/workflows/test-distro.yml)
- [qualcomm-linux/meta-qcom-3rdparty](https://github.com/qualcomm-linux/meta-qcom-3rdparty) → **uses automation from** → [qualcomm/qcom-reusable-workflows](https://github.com/qualcomm/qcom-reusable-workflows)
  - GitHub Actions integration at the evidence revision; workflow/action refs are specified by the calling files. This is not a runtime dependency.
  - [Explore qualcomm/qcom-reusable-workflows](https://github.com/devdocsorg/qualcomm-repository-map/blob/b17820e6a872efac49ed5a041112e6da25fdf342/maps/qualcomm--qcom-reusable-workflows.md) · [evidence 1](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/.github/workflows/qcom-preflight-checks.yml)

#### Uses indirectly

- [qualcomm-linux/meta-qcom-3rdparty](https://github.com/qualcomm-linux/meta-qcom-3rdparty) → **uses indirectly** → [qualcomm-linux/qcom-ptool](https://github.com/qualcomm-linux/qcom-ptool)
  - Partition tooling is supplied through meta-qcom; this is an indirect relationship, not an extra layer dependency.
  - [Explore qualcomm-linux/qcom-ptool](https://github.com/devdocsorg/qualcomm-repository-map/blob/b17820e6a872efac49ed5a041112e6da25fdf342/maps/qualcomm-linux--qcom-ptool.md) · [evidence 1](https://github.com/qualcomm-linux/meta-qcom/blob/c6729710f055e1c0337c830030ab25eef7f293a5/recipes-bsp/partition/qcom-ptool.inc) · [evidence 2](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/conf/machine/rubikpi3.conf)

### Full ecosystem map

[Explore the Qualcomm repository map](https://github.com/devdocsorg/qualcomm-repository-map).

The shared map is private and requires repository access. The repository and evidence links above point directly to their public sources.

Connections apply to the linked evidence revisions; use release-compatible revisions for a build.

Dataset SHA-256: `602a68056238817dccee9f98db5c06ea20d0bb165a53a0c23ff2d0423240dfca`.
Generated from [central map revision `b17820e6a872`](https://github.com/devdocsorg/qualcomm-repository-map/tree/b17820e6a872efac49ed5a041112e6da25fdf342). Edit the shared dataset and regenerate to change connections.

<!-- repository-map:end -->
