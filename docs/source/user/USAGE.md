# Build an image for a supported board

This tutorial builds `core-image-base` for the Thundercomm RUBIK Pi 3
(`rubikpi3`) with kas and flashes it over USB. The same steps build the Radxa
Dragon Q6A (`radxa-dragon-q6a`), whose output step 4 describes.

## Prerequisites

- A networked x86-64 Linux host that meets the [Yocto Project system requirements](https://docs.yoctoproject.org/ref-manual/system-requirements.html).
- Git, Docker or Podman, and [kas-container](https://github.com/siemens/kas/blob/master/kas-container) on your `PATH`.
- To flash a RUBIK Pi 3: a USB-C cable and QDL, set up with meta-qcom's [flashing guide](https://github.com/qualcomm-linux/meta-qcom/blob/46261cd7cb48521654ec1ed9fdd3b4897718a2b7/docs/flashing.md).

## 1. Clone the layer

```sh
git clone https://github.com/qualcomm-linux/meta-qcom-3rdparty.git
cd meta-qcom-3rdparty
```

## 2. Choose a work directory

kas clones meta-qcom, OpenEmbedded-Core, and BitBake into its work directory
and builds there. Keep it outside the checkout; the
[agent guide](../contributing/AGENTS.md#2-recommended-environment) also shows
shared download and build caches.

```sh
export KAS_WORK_DIR="$HOME/kas-work"
mkdir -p "$KAS_WORK_DIR"
```

## 3. Build the image

```sh
kas-container build ci/rubikpi3.yml
```

`ci/rubikpi3.yml` selects the machine and includes `ci/base.yml`, which builds
`core-image-base` without a distro. For the Qualcomm Linux images, build
`ci/rubikpi3.yml:ci/qcom-distro.yml` instead. A first build takes hours.

## 4. Find the output

The build ends without errors. `$KAS_WORK_DIR/build/tmp/deploy/images/rubikpi3/`
contains `core-image-base-rubikpi3.rootfs.qcomflash.tar.gz` and the unpacked
`core-image-base-rubikpi3.rootfs.qcomflash/` directory: boot firmware,
partition tables, and root file system for QDL.

For `radxa-dragon-q6a`, `images/radxa-dragon-q6a/` holds
`core-image-base-radxa-dragon-q6a.rootfs.wic.gz` and its `.wic.bmap`, a disk
image for an SD card, UFS, or NVMe drive. Radxa supplies the board's SPI NOR
boot firmware separately.

## 5. Flash the RUBIK Pi 3

Put the board in Emergency Download (EDL) mode, connect it over USB-C, and run:

```sh
cd "$KAS_WORK_DIR/build/tmp/deploy/images/rubikpi3/core-image-base-rubikpi3.rootfs.qcomflash"
qdl --debug prog_firehose_ddr.elf rawprogram*.xml patch*.xml
```

QDL reports each partition it programs and exits with status 0. Restart the
board out of EDL mode to boot the new image.

## Use native kas or an existing Yocto environment

To build a reference image using [kas](https://kas.readthedocs.io/):

```bash
kas build meta-qcom-3rdparty/ci/<machine.yml>
```

Otherwise add this layer to your existing Yocto environment:

```bash
git clone https://github.com/qualcomm-linux/meta-qcom-3rdparty.git
bitbake-layers add-layer ../meta-qcom-3rdparty
```

Add meta-qcom first, since this layer depends on it, and set `MACHINE` to a
machine from `conf/machine`.
