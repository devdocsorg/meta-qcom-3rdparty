# Build an image for a supported board

This tutorial builds `core-image-base` for the Thundercomm RUBIK Pi 3
(`rubikpi3`) with kas-container, the way CI builds each machine.

## Prerequisites

- A Linux host with Docker or Podman, network access, and the free disk space the
  [Yocto Project system requirements](https://docs.yoctoproject.org/ref-manual/system-requirements.html)
  ask for (at least 140 GB).
- Git and a current [kas-container](https://github.com/siemens/kas/blob/master/kas-container)
  release. CI downloads the latest one; kas-container 4.8.2 reads this configuration.

## 1. Clone the layer

```sh
git clone https://github.com/qualcomm-linux/meta-qcom-3rdparty.git
cd meta-qcom-3rdparty
```

## 2. Choose where the build goes

kas-container checks out [meta-qcom](https://github.com/qualcomm-linux/meta-qcom), [OpenEmbedded-Core](https://github.com/openembedded/openembedded-core), and
[BitBake](https://github.com/openembedded/bitbake) and builds in
`KAS_WORK_DIR`, which defaults to the current directory. Keep it and the shared
caches outside the checkout:

```sh
export KAS_WORK_DIR="$HOME/kas-work"
export DL_DIR="$HOME/yocto-cache/downloads"
export SSTATE_DIR="$HOME/yocto-cache/sstate-cache"
mkdir -p "$KAS_WORK_DIR" "$DL_DIR" "$SSTATE_DIR"
```

The [configuration reference](CONFIGURATION.md#environment-settings) describes
these settings.

## 3. Build

```sh
kas-container build ci/rubikpi3.yml
```

[ci/rubikpi3.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/ci/rubikpi3.yml)
selects the machine and includes the shared configuration, which builds
`core-image-base` without a distribution (`nodistro`). To build the Qualcomm Linux
distribution images instead, run
`kas-container build ci/rubikpi3.yml:ci/qcom-distro.yml`.

## Expected result

BitBake ends with `Tasks Summary: ... all succeeded`, and
`$KAS_WORK_DIR/build/tmp/deploy/images/rubikpi3/` contains:

- `core-image-base-rubikpi3.rootfs.qcomflash.tar.gz`, the flashable package with
  the boot firmware, partition tables, and root filesystem.
- `core-image-base-rubikpi3.rootfs.ext4`, the root filesystem image.

To write the package to the board, follow the
[meta-qcom flashing instructions](https://github.com/qualcomm-linux/meta-qcom/blob/master/docs/flashing.md).
