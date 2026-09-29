# Build an image for a supported board

This tutorial builds a flashable `core-image-base` image for the Thundercomm
RUBIK Pi 3 with the layer's kas files, then adds the layer to an existing
Yocto Project build.

## Prerequisites

- A Linux host that meets the
  [Yocto Project build host requirements](https://docs.yoctoproject.org/ref-manual/system-requirements.html).
- Git, and Docker or Podman.
- [kas-container](https://kas.readthedocs.io/en/latest/userguide/kas-container.html),
  or a native [kas](https://kas.readthedocs.io/) installation.

## 1. Clone the layer into a work directory

kas places the other layers, the downloads, and the build output in the
directory it runs from, so start in an empty work directory:

```sh
mkdir qcom-3rdparty-work
cd qcom-3rdparty-work
git clone https://github.com/qualcomm-linux/meta-qcom-3rdparty.git
```

## 2. Build the image

To build a reference image using [kas](https://kas.readthedocs.io/):

```sh
kas-container build meta-qcom-3rdparty/ci/rubikpi3.yml
```

With a native kas installation, run `kas build meta-qcom-3rdparty/ci/<machine.yml>`
instead. `ci/rubikpi3.yml` selects the `rubikpi3` machine and includes
`ci/base.yml`, which fetches [meta-qcom](https://github.com/qualcomm-linux/meta-qcom),
[OpenEmbedded-Core](https://github.com/openembedded/openembedded-core), and [BitBake](https://github.com/openembedded/bitbake) and builds `core-image-base` without a
distribution (`nodistro`). Use `ci/radxa-dragon-q6a.yml` for the Radxa Dragon
Q6A. To build the Qualcomm Linux distribution images instead, append
`:meta-qcom-3rdparty/ci/qcom-distro.yml` to the kas file argument.

The first build downloads every source and takes hours. To share downloads and
build results between work directories, export the `DL_DIR` and `SSTATE_DIR`
settings described in the
[environment example](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/.env.example).

## Expected result

BitBake ends with a `Tasks Summary` line reporting that all tasks succeeded.
`build/tmp/deploy/images/rubikpi3/` then contains
`core-image-base-rubikpi3.rootfs.qcomflash.tar.gz`, the flashable package with
the boot firmware, partition tables, and root filesystem. Flash it as described
in [meta-qcom](https://github.com/qualcomm-linux/meta-qcom)'s
[flashing guide](https://github.com/qualcomm-linux/meta-qcom/blob/master/docs/flashing.md).

For `radxa-dragon-q6a`, the same folder under `radxa-dragon-q6a/` contains
`core-image-base-radxa-dragon-q6a.rootfs.wic.gz` and its `.wic.bmap`: a disk
image with an EFI system partition and the root filesystem. The board's SPI NOR
boot firmware is flashed separately with Radxa's tools.

## Add the layer to an existing build

Otherwise add this layer to your existing Yocto environment. The build must
already contain [OpenEmbedded-Core](https://github.com/openembedded/openembedded-core) and
[meta-qcom](https://github.com/qualcomm-linux/meta-qcom), because
`conf/layer.conf` depends on both. From the build directory:

```sh
git clone https://github.com/qualcomm-linux/meta-qcom-3rdparty.git ../meta-qcom-3rdparty
bitbake-layers add-layer ../meta-qcom-3rdparty
```

Set `MACHINE = "rubikpi3"` or `MACHINE = "radxa-dragon-q6a"` in
`conf/local.conf`, then build an image with `bitbake core-image-base`.

Expected result: `bitbake-layers show-layers` lists the `qcom-3rdparty` layer
with priority 5, and the image appears under `tmp/deploy/images/<machine>/`.
