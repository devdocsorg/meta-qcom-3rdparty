# Build an image

This tutorial builds `core-image-base` for the Thundercomm RUBIK Pi 3 with
[kas-container](https://kas.readthedocs.io/en/latest/userguide/kas-container.html),
the way CI builds it, and finds the image files to flash.

## Prerequisites

- A Linux host with Docker or Podman that your user can run, and Git.
- [kas-container](https://github.com/siemens/kas/blob/master/kas-container) on
  `PATH`; this tutorial was checked with kas-container 4.8.2.
- Network access and the disk space described in the Yocto Project's
  [system requirements](https://docs.yoctoproject.org/ref-manual/system-requirements.html).

## 1. Clone the layer

```sh
git clone https://github.com/qualcomm-linux/meta-qcom-3rdparty.git
cd meta-qcom-3rdparty
```

## 2. Choose work directories

Keep the kas work directory and the shared caches outside the checkout. The
[environment settings](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/build-prerequisites-test/.env.example)
explain each variable:

```sh
export KAS_WORK_DIR="$HOME/yocto/kas-work"
export DL_DIR="$HOME/yocto/downloads"
export SSTATE_DIR="$HOME/yocto/sstate-cache"
mkdir -p "$KAS_WORK_DIR" "$DL_DIR" "$SSTATE_DIR"
```

## 3. Build

```sh
kas-container build ci/rubikpi3.yml
```

kas clones [meta-qcom](https://github.com/qualcomm-linux/meta-qcom),
[OpenEmbedded-Core](https://github.com/openembedded/openembedded-core), and [BitBake](https://github.com/openembedded/bitbake) into the work directory, then builds
`core-image-base` without a distribution (`nodistro`). To build with the Qualcomm
distribution instead, add its fragment:
`kas-container build ci/rubikpi3.yml:ci/qcom-distro.yml`.

## Expected result

The build exits with status 0 and writes the images to
`$KAS_WORK_DIR/build/tmp/deploy/images/rubikpi3/`:

- `core-image-base-rubikpi3.rootfs.ext4` — the root file system.
- `core-image-base-rubikpi3.rootfs.qcomflash/` — the boot firmware, partition
  tables, and images, laid out for flashing.
- `core-image-base-rubikpi3.rootfs.qcomflash.tar.gz` — the same files as one archive.

For the Radxa Dragon Q6A, build `ci/radxa-dragon-q6a.yml`. Its output folder,
`radxa-dragon-q6a`, also holds `core-image-base-radxa-dragon-q6a.rootfs.wic.gz`
and its `.wic.bmap`, the disk image for an SD card, UFS, or NVMe drive.
