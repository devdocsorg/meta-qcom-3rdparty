# Build an image for a supported board

This tutorial builds `core-image-base` for the Thundercomm RUBIK Pi 3
(`rubikpi3`) with kas-container, the way CI does, and finds the flashable image
it produces. To add the layer to an existing BitBake build instead, see the
[Quick Start](../README.md#quick-start).

## Prerequisites

- A Linux host meeting the Yocto Project's
  [build host requirements](https://docs.yoctoproject.org/brief-yoctoprojectqs/index.html#compatible-linux-distribution),
  including at least 140 GB of free disk space and 32 GB of RAM.
- Docker or Podman, usable without `sudo`.
- [kas-container](https://kas.readthedocs.io/en/latest/userguide/kas-container.html) 5.5 on your `PATH`:

  ```sh
  mkdir -p ~/.local/bin
  curl -sSfL -o ~/.local/bin/kas-container https://raw.githubusercontent.com/siemens/kas/5.5/kas-container
  chmod +x ~/.local/bin/kas-container
  ```

- Network access: kas clones [meta-qcom](https://github.com/qualcomm-linux/meta-qcom),
  OpenEmbedded-Core, and BitBake, and BitBake downloads the sources.

## 1. Clone the layer

```sh
git clone https://github.com/qualcomm-linux/meta-qcom-3rdparty.git
cd meta-qcom-3rdparty
```

## 2. Choose the work and cache directories

kas checks out the other layers and builds in its work directory. Keep it, and
the download and shared-state caches, outside the checkout:

```sh
export KAS_WORK_DIR="$HOME/kas-work"
export DL_DIR="$HOME/yocto-cache/downloads"
export SSTATE_DIR="$HOME/yocto-cache/sstate-cache"
mkdir -p "$KAS_WORK_DIR"
```

The [configuration reference](CONFIGURATION.md#environment) describes these settings.

## 3. Build

```sh
kas-container build ci/rubikpi3.yml
```

`ci/rubikpi3.yml` selects the machine and includes meta-qcom's base
configuration, which selects the `nodistro` distribution and the
`core-image-base` target. For the Qualcomm Linux distribution and its images,
build `ci/rubikpi3.yml:ci/qcom-distro.yml` instead.

The first build downloads and compiles every package, so expect it to take
hours. For comparison, the project's CI job for this machine, which also builds
every recipe in both Qualcomm layers on 16-CPU, 64 GB runners with a shared
cache, took between 8 and 128 minutes across its recent successful runs,
depending on how much of the cache it could reuse. Later builds reuse
`SSTATE_DIR` and finish much faster.

## Expected result

kas-container exits with status 0, and
`$KAS_WORK_DIR/build/tmp/deploy/images/rubikpi3/` contains:

- `core-image-base-rubikpi3.rootfs.qcomflash.tar.gz`: the flashable package,
  holding the boot firmware, partition tables, and root file system.
- `core-image-base-rubikpi3.rootfs.qcomflash/`: the same files, unpacked.
- `core-image-base-rubikpi3.rootfs.ext4`: the root file system image.

The `radxa-dragon-q6a` build (`ci/radxa-dragon-q6a.yml`) also produces
`core-image-base-radxa-dragon-q6a.rootfs.wic.gz` and its `.wic.bmap` for an SD
card; its boot firmware is flashed separately, as its
[machine configuration](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006b/conf/machine/radxa-dragon-q6a.conf)
notes.
