# Repository map: qualcomm-linux/meta-qcom-3rdparty

**You are here: [qualcomm-linux/meta-qcom-3rdparty](https://github.com/qualcomm-linux/meta-qcom-3rdparty)**

OpenEmbedded/Yocto Project BSP layer for Third-Party Maintained Qualcomm based platforms

## Outgoing connections

### Depends on

- [qualcomm-linux/meta-qcom-3rdparty](https://github.com/qualcomm-linux/meta-qcom-3rdparty) → **depends on** → [openembedded/openembedded-core](https://github.com/openembedded/openembedded-core)
  - wrynose-compatible main snapshot 8927b428bcae; required layer collection.
  - [Explore openembedded/openembedded-core](https://github.com/devdocsorg/qualcomm-repository-map/blob/b17820e6a872efac49ed5a041112e6da25fdf342/maps/openembedded--openembedded-core.md) · [evidence 1](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/conf/layer.conf)
- [qualcomm-linux/meta-qcom-3rdparty](https://github.com/qualcomm-linux/meta-qcom-3rdparty) → **depends on** → [qualcomm-linux/meta-qcom](https://github.com/qualcomm-linux/meta-qcom)
  - wrynose-compatible main snapshot 8927b428bcae; required layer collection.
  - [Explore qualcomm-linux/meta-qcom](https://github.com/devdocsorg/qualcomm-repository-map/blob/b17820e6a872efac49ed5a041112e6da25fdf342/maps/qualcomm-linux--meta-qcom.md) · [evidence 1](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/conf/layer.conf)

### Fetches source from

- [qualcomm-linux/meta-qcom-3rdparty](https://github.com/qualcomm-linux/meta-qcom-3rdparty) → **fetches source from** → [rubikpi-ai/boot-assets](https://github.com/rubikpi-ai/boot-assets)
  - RUBIK Pi 3 boot firmware only; pinned by the recipe SRCREV.
  - [Explore rubikpi-ai/boot-assets](https://github.com/devdocsorg/qualcomm-repository-map/blob/b17820e6a872efac49ed5a041112e6da25fdf342/maps/rubikpi-ai--boot-assets.md) · [evidence 1](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/recipes-bsp/firmware-boot/firmware-qcom-boot-rubikpi3_20260621.bb)

### Integrates with

- [qualcomm-linux/meta-qcom-3rdparty](https://github.com/qualcomm-linux/meta-qcom-3rdparty) → **integrates with** → [qualcomm-linux/meta-qcom-distro](https://github.com/qualcomm-linux/meta-qcom-distro)
  - Optional: the dynamic layer applies only when qcom-distro is present.
  - [Explore qualcomm-linux/meta-qcom-distro](https://github.com/devdocsorg/qualcomm-repository-map/blob/b17820e6a872efac49ed5a041112e6da25fdf342/maps/qualcomm-linux--meta-qcom-distro.md) · [evidence 1](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/conf/layer.conf)

### Uses automation from

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

### Uses indirectly

- [qualcomm-linux/meta-qcom-3rdparty](https://github.com/qualcomm-linux/meta-qcom-3rdparty) → **uses indirectly** → [qualcomm-linux/qcom-ptool](https://github.com/qualcomm-linux/qcom-ptool)
  - Partition tooling is supplied through meta-qcom; this is an indirect relationship, not an extra layer dependency.
  - [Explore qualcomm-linux/qcom-ptool](https://github.com/devdocsorg/qualcomm-repository-map/blob/b17820e6a872efac49ed5a041112e6da25fdf342/maps/qualcomm-linux--qcom-ptool.md) · [evidence 1](https://github.com/qualcomm-linux/meta-qcom/blob/c6729710f055e1c0337c830030ab25eef7f293a5/recipes-bsp/partition/qcom-ptool.inc) · [evidence 2](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/conf/machine/rubikpi3.conf)

## Full ecosystem map

[Explore the Qualcomm repository map](https://github.com/devdocsorg/qualcomm-repository-map).

The shared map is private and requires repository access. The repository and evidence links above point directly to their public sources.

Connections apply to the linked evidence revisions; use release-compatible revisions for a build.

Dataset SHA-256: `602a68056238817dccee9f98db5c06ea20d0bb165a53a0c23ff2d0423240dfca`.
Generated from [central map revision `b17820e6a872`](https://github.com/devdocsorg/qualcomm-repository-map/tree/b17820e6a872efac49ed5a041112e6da25fdf342). Edit the shared dataset and regenerate to change connections.
