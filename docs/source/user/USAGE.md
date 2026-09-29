# Build an image for a supported board

This tutorial builds `core-image-base` for the Thundercomm RUBIK Pi 3
(`rubikpi3`) with the layer's kas fragments, then locates the image to flash.

## Prerequisites

- An x86-64 Linux host with Docker or Podman, network access, and the free
  disk space and memory in the Yocto Project
  [system requirements](https://docs.yoctoproject.org/6.0/ref-manual/system-requirements.html).
- [kas-container](https://kas.readthedocs.io/en/4.8.2/userguide/kas-container.html)
  4.8.2.

## 1. Get the layer

```sh
git clone https://github.com/qualcomm-linux/meta-qcom-3rdparty.git
cd meta-qcom-3rdparty
```

## 2. Choose work and cache directories

kas clones the other layers and builds under `KAS_WORK_DIR`; keep it and the
caches outside the checkout. The [environment settings](CONFIGURATION.md#environment)
explain each variable.

```sh
export KAS_WORK_DIR="$HOME/yocto/kas-work"
export DL_DIR="$HOME/yocto/cache/downloads"
export SSTATE_DIR="$HOME/yocto/cache/sstate-cache"
mkdir -p "$KAS_WORK_DIR" "$DL_DIR" "$SSTATE_DIR"
```

## 3. Build

```sh
"${KAS_CONTAINER:-kas-container}" build ci/rubikpi3.yml
```

[ci/rubikpi3.yml](CONFIGURATION.md#kas-fragments) selects the machine and
includes `ci/base.yml`, which fetches [meta-qcom](https://github.com/qualcomm-linux/meta-qcom),
[OpenEmbedded-Core](https://github.com/openembedded/openembedded-core), and
[BitBake](https://github.com/openembedded/bitbake) and builds `core-image-base` without a distribution. Use
`ci/radxa-dragon-q6a.yml` for the Radxa Dragon Q6A, or append
`:ci/qcom-distro.yml` to build the Qualcomm Linux distribution images instead.

`ci/base.yml` follows the `master` branch of [meta-qcom](https://github.com/qualcomm-linux/meta-qcom) and its
dependencies.
When they move to a Yocto Project release that the layer's
`LAYERSERIES_COMPAT_qcom-3rdparty` does not list, BitBake stops before building
with a layer compatibility error.

## Expected result

The build ends with BitBake's task summary and no failed tasks. The image
directory `$KAS_WORK_DIR/build/tmp/deploy/images/rubikpi3/` contains:

- `core-image-base-rubikpi3.rootfs.qcomflash/`, the flashable package with the
  boot firmware, partition tables, and root file system.
- `core-image-base-rubikpi3.rootfs.ext4`, the root file system image.

Flash the `qcomflash` package over USB with QDL, as
[meta-qcom's flashing guide](https://github.com/qualcomm-linux/meta-qcom/blob/master/docs/flashing.md)
describes. For `radxa-dragon-q6a`, the directory also holds
`core-image-base-radxa-dragon-q6a.rootfs.wic.gz` and its `.wic.bmap`; write that
disk image to the SD card or other boot medium, for example with
`bmaptool copy`. The board's SPI NOR firmware is flashed separately.
