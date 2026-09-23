# Build an image for a supported board

This tutorial builds `core-image-base` for the Thundercomm RUBIK Pi 3
(`rubikpi3`) with kas and finds the image to flash. Use
`ci/radxa-dragon-q6a.yml` instead to build for the Radxa Dragon Q6A.

## Prerequisites

- A Linux host with network access that meets the Yocto Project
  [system requirements](https://docs.yoctoproject.org/wrynose/ref-manual/system-requirements.html),
  including about 140 GB of free disk space.
- Docker or Podman, usable without `sudo`.
- [kas-container](https://github.com/siemens/kas/blob/master/kas-container)
  4.8 or newer on `PATH`; 4.8.2 was tested.

## 1. Clone the layer into a work directory

kas uses the current directory for layer checkouts and the `build/` directory.

```sh
mkdir -p ~/kas-work && cd ~/kas-work
git clone https://github.com/qualcomm-linux/meta-qcom-3rdparty.git
```

## 2. Keep caches outside the build

```sh
export DL_DIR="$HOME/yocto-cache/downloads"
export SSTATE_DIR="$HOME/yocto-cache/sstate-cache"
```

Later builds reuse them; the [configuration reference](CONFIGURATION.md#environment)
describes these and the other variables in `.env.example`.

## 3. Build the image

```sh
kas-container build meta-qcom-3rdparty/ci/rubikpi3.yml
```

`ci/rubikpi3.yml` selects the machine and includes `ci/base.yml`, which adds
meta-qcom, OE-Core, and BitBake and sets the target `core-image-base`. The first
build fetches every source and can take several hours.

To build with the Qualcomm Linux distribution instead of `nodistro`, append its
fragment. It replaces the target with meta-qcom's distribution images, such as
`qcom-multimedia-image`, whose files are named after those images:

```sh
kas-container build meta-qcom-3rdparty/ci/rubikpi3.yml:meta-qcom-3rdparty/ci/qcom-distro.yml
```

## Expected result

kas exits with status 0 and the image files are in
`build/tmp/deploy/images/rubikpi3/`:

- `core-image-base-rubikpi3.rootfs.qcomflash/`: the flashable package with boot
  firmware, partition tables, the EFI system partition, and the root filesystem.
- `core-image-base-rubikpi3.rootfs.qcomflash.tar.gz`: the same package as one
  archive, for copying to another host.
- `core-image-base-rubikpi3.rootfs.ext4`: the root filesystem on its own.

Flash the `qcomflash` directory with QDL as described in meta-qcom's
[Flashing images](https://github.com/qualcomm-linux/meta-qcom/blob/master/docs/flashing.md).
For `radxa-dragon-q6a`, the directory is `build/tmp/deploy/images/radxa-dragon-q6a/`
and `core-image-base-radxa-dragon-q6a.rootfs.wic.gz` with its `.wic.bmap` is
the disk image to write to an SD card, UFS, or NVMe drive.

## Add the layer to an existing build

In a build environment that already contains OE-Core and
[meta-qcom](https://github.com/qualcomm-linux/meta-qcom), which this layer
requires:

```sh
bitbake-layers add-layer ../meta-qcom-3rdparty
```

Then set `MACHINE = "rubikpi3"` or `MACHINE = "radxa-dragon-q6a"` in
`conf/local.conf` and run `bitbake core-image-base`.
