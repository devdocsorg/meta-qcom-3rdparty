# Build an image for a board

This tutorial builds `core-image-base` for the Thundercomm RUBIK Pi 3
(`rubikpi3`) with kas-container, the way CI builds each machine, and finds the
image to flash. The same steps build `radxa-dragon-q6a`.

## Prerequisites

- An x86-64 Linux host that meets the Yocto Project
  [system requirements](https://docs.yoctoproject.org/ref-manual/system-requirements.html),
  including their free disk space.
- Git, and Docker or Podman usable without `sudo`.
- [kas-container](https://github.com/siemens/kas/blob/master/kas-container) on
  `PATH`, or its path in `KAS_CONTAINER`, as in the
  [agent guide](../contributing/AGENTS.md#1-prerequisites).

## 1. Clone the layer

```sh
git clone https://github.com/qualcomm-linux/meta-qcom-3rdparty.git
cd meta-qcom-3rdparty
```

Use `-b wrynose` for Qualcomm Linux 2.x; the [README](https://github.com/qualcomm-linux/meta-qcom-3rdparty#branches)
lists the other branches.

## 2. Choose where downloads and shared state go

Optional: keep downloads and shared state outside the checkout so later builds
reuse them:

```sh
export DL_DIR="$HOME/yocto-cache/downloads"
export SSTATE_DIR="$HOME/yocto-cache/sstate-cache"
mkdir -p "$DL_DIR" "$SSTATE_DIR"
```

## 3. Build the image

```sh
kas-container build ci/rubikpi3.yml
```

kas clones [meta-qcom](https://github.com/qualcomm-linux/meta-qcom),
[openembedded-core](https://github.com/openembedded/openembedded-core), and
[bitbake](https://github.com/openembedded/bitbake) into the checkout, then builds
`core-image-base` for `rubikpi3` without a distribution. To build the Qualcomm
Linux images instead, add the distro fragment:
`kas-container build ci/rubikpi3.yml:ci/qcom-distro.yml`. The first build
downloads and compiles every package.

## 4. Find the image

The build directory is `build/` in the kas work directory, which is the checkout
unless `KAS_WORK_DIR` is set:

```sh
ls build/tmp/deploy/images/rubikpi3/core-image-base-rubikpi3.rootfs.qcomflash.tar.gz
```

Expected result: the build ends without errors, and the listed archive holds
the root file system, kernel, device tree, partition tables, and RUBIK Pi 3 boot
firmware ready for flashing with QDL. Flash it as [meta-qcom](https://github.com/qualcomm-linux/meta-qcom)'s
[flashing guide](https://github.com/qualcomm-linux/meta-qcom/blob/master/docs/flashing.md)
describes.

For `radxa-dragon-q6a`, the image to write to an SD card, UFS, or NVMe device is
`core-image-base-radxa-dragon-q6a.rootfs.wic.gz`, with a matching `.wic.bmap`
for `bmaptool`; its boot firmware stays in the board's SPI NOR flash.
