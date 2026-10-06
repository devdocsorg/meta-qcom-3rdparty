# Build an image for a third-party board

This tutorial builds `core-image-base` for the Thundercomm RUBIK Pi 3
(`rubikpi3`) with the same [kas](https://github.com/siemens/kas) configuration that CI uses, and finds the package
that flashes the board.

## Prerequisites

- A Linux build host with Git, curl, and Docker or Podman. `kas-container` runs
  the build inside the kas container, so [BitBake](https://github.com/openembedded/bitbake) and its host tools do not need
  to be installed.
- Free disk space and memory as the Yocto Project
  [system requirements](https://docs.yoctoproject.org/ref-manual/system-requirements.html)
  describe: at least 140 GB of disk and 32 GB of RAM.
- Network access to GitHub and the source mirrors the recipes fetch from.

## 1. Install kas-container

CI downloads the `kas-container` script from the newest kas release. Install the
5.5 release script:

```sh
mkdir -p ~/.local/bin
curl -sSfL -o ~/.local/bin/kas-container https://raw.githubusercontent.com/siemens/kas/refs/tags/5.5/kas-container
chmod +x ~/.local/bin/kas-container
```

## 2. Clone the layer and choose a work directory

```sh
git clone https://github.com/qualcomm-linux/meta-qcom-3rdparty.git
cd meta-qcom-3rdparty
mkdir -p ~/kas-work
export KAS_WORK_DIR=~/kas-work
```

kas checks out [meta-qcom](https://github.com/qualcomm-linux/meta-qcom),
[OpenEmbedded-Core](https://github.com/openembedded/openembedded-core), and BitBake into `KAS_WORK_DIR` and builds in its `build/`
folder, outside the checkout. To keep downloads and shared state in other
folders as well, set the variables that `.env.example` documents; the
[configuration reference](CONFIGURATION.md#environment) explains them.

## 3. Build the image

```sh
~/.local/bin/kas-container build ci/rubikpi3.yml
```

[`ci/rubikpi3.yml`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006c/ci/rubikpi3.yml)
selects the `rubikpi3` machine and includes meta-qcom's base configuration, which
uses `nodistro` and builds `core-image-base`. Add `:ci/qcom-distro.yml` to the
argument to build the Qualcomm Linux distribution's images instead.

How long it takes: on CI's 16-vCPU runners, which also build every recipe of
meta-qcom and this layer in the same job, this configuration takes
from under ten minutes with a warm shared-state cache
([example](https://github.com/qualcomm-linux/meta-qcom-3rdparty/actions/runs/36785803193))
to about two hours
([example](https://github.com/qualcomm-linux/meta-qcom-3rdparty/actions/runs/36506511249)).
A first build on your host has no cache: it downloads every source and compiles
the toolchain and all packages, so plan for hours, more on a host with fewer
cores or less memory.

## Expected result

The command exits with status 0 and BitBake reports that all tasks succeeded.
The images are in `~/kas-work/build/tmp/deploy/images/rubikpi3/`, including:

- `core-image-base-rubikpi3.rootfs.qcomflash.tar.gz`: the flashable package with
  the boot firmware, partition tables, and root file system.
- `core-image-base-rubikpi3.rootfs.ext4`: the root file system image.

Flash the package with QDL as meta-qcom's
[flashing guide](https://github.com/qualcomm-linux/meta-qcom/blob/b6b6e1b04ed09116936dbb5926dd830eafdc52a2/docs/flashing.md)
describes; put the board into EDL mode as its vendor documents.

To build the Radxa Dragon Q6A instead, use `ci/radxa-dragon-q6a.yml`. Radxa flashes that board's boot firmware into its SPI NOR flash separately, so
the build also writes `core-image-base-radxa-dragon-q6a.rootfs.wic.gz`, a disk
image with the EFI system partition and root file system for SD, UFS, or NVMe
storage.
