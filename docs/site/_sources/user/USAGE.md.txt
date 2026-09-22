# Build a RUBIK Pi 3 firmware deployment

This tutorial uses the layer's boot-firmware recipe to produce files consumed by
Qualcomm's image tooling. It exercises a real deploy target without compiling an
entire operating-system image. It does not flash a board.

## Prerequisites

Complete the [development environment setup](../contributing/DEVELOPMENT.md),
including the container smoke test and writable external caches. Network access
is needed to fetch the pinned vendor assets, parent metadata, and uncached tools.
Use this branch's `rubikpi3` machine. Firmware has its own vendor licence; the
layer's MIT licence does not relicense fetched binaries.

## 1. Select the machine

From the layer checkout:

```sh
export KAS_YAMLS=ci/rubikpi3.yml
"${KAS_CONTAINER:-kas-container}" dump "$KAS_YAMLS"
```

Confirm that the resolved machine is `rubikpi3`, the distro is `nodistro`, and
both this layer and `meta-qcom` are in the composition. Record the resolved
repository commits for reproducibility. The
[machine reference](SUPPORTED_MACHINES.md) explains how the two boards differ.

## 2. Parse the selected firmware recipe

```sh
"${KAS_CONTAINER:-kas-container}" shell "$KAS_YAMLS" \
  --command 'bitbake -e firmware-qcom-boot-rubikpi3 > /work/firmware-environment.txt'
```

The command exits successfully and writes the evaluated metadata in your kas
work directory. Check `COMPATIBLE_MACHINE`, `SRCREV`, `QCOM_BOOT_IMG_SUBDIR`, and
`DEPLOY_DIR_IMAGE` there. The recipe pins the vendor source to
`10b868574aa4d06fb3836399d10eb5c792765504`; deploy uses the `rubikpi3` subdirectory.

## 3. Build and deploy the firmware

```sh
"${KAS_CONTAINER:-kas-container}" shell "$KAS_YAMLS" \
  --command 'bitbake firmware-qcom-boot-rubikpi3 -c deploy'
```

Expected result: completed tasks and boot assets under the resolved
`DEPLOY_DIR_IMAGE/rubikpi3/`, including `RubikPi3_CDT.bin` and the vendor `.elf`,
`.mbn`, `.fv`, and `.img` files present in the pinned source. `do_deploy` stages
those files through `DEPLOYDIR`; the inherited deploy class publishes them.
Read the [generated task reference](../contributing/.generated/index.rst) for
arguments and failure behaviour.

## 4. Use the deployment in an image

The machine selects this boot firmware and names `RubikPi3_CDT` through
`QCOM_CDT_FILE`. To produce a complete image, follow the existing
[CI-style build commands](../contributing/AGENTS.md#3-build-with-kas-container-ci-style).
The optional Qualcomm distro composition applies the recipe's machine-scoped
licence exception. Image builds take substantially more disk space and time than
this firmware deploy target; their success does not establish hardware boot success.

For a pre-existing compatible Yocto workspace, clone the layer and use
`bitbake-layers add-layer ../meta-qcom-3rdparty` after loading that workspace's
build environment. Its `core` and `qcom` dependencies must already be available.
Do not mix release branches; see {download}`branch guidance <../../../BRANCHES.md>`.
