# Build an image for a supported board

This tutorial builds the `core-image-base` image for the Thundercomm RUBIK Pi 3
(`rubikpi3`) with [kas-container](https://github.com/siemens/kas), the way CI builds it, and finds the flashable
package it produces.

## Prerequisites

- A Linux build host that meets the
  [Yocto Project build host requirements](https://docs.yoctoproject.org/brief-yoctoprojectqs/index.html#compatible-linux-distribution),
  including at least 140 GB of free disk space and 32 GB of RAM, with network
  access for the layers and source downloads.
- Git, and [Docker](https://docs.docker.com/engine/install/) (tested with
  29.7) or Podman, usable without `sudo`: `docker run --rm hello-world` succeeds.
- [kas-container](https://kas.readthedocs.io/en/latest/userguide/kas-container.html)
  5.5 on your `PATH`:

  ```sh
  mkdir -p ~/.local/bin
  curl -sSfL -o ~/.local/bin/kas-container https://raw.githubusercontent.com/siemens/kas/5.5/kas-container
  chmod +x ~/.local/bin/kas-container
  ```

## 1. Clone the repository

This proposal's runnable checkout is its review branch:

```sh
git clone -b docs/upgrade-test-1010a https://github.com/devdocsorg/meta-qcom-3rdparty.git
cd meta-qcom-3rdparty
```

## 2. Choose the work directories

Copy the environment settings, edit the paths in `.env` if you want other
locations, then load them and create the work directory:

```sh
cp .env.example .env
set -a; . ./.env; set +a
mkdir -p "$KAS_WORK_DIR"
```

## 3. Build the image

```sh
kas-container build ci/rubikpi3.yml
```

[`ci/rubikpi3.yml`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1010a/ci/rubikpi3.yml)
selects the machine and includes `ci/base.yml`, which brings in
[`meta-qcom`](https://github.com/qualcomm-linux/meta-qcom)'s base configuration:
[oe-core](https://github.com/openembedded/openembedded-core) and [BitBake](https://github.com/openembedded/bitbake) at the revisions `meta-qcom` pins, the `nodistro`
distribution, and the `core-image-base` target.

The build is the long step. CI reuses a warm download and sstate cache, and its
image step for this machine took about 2 minutes after a world build in the
[`rubikpi3/nodistro` job](https://github.com/qualcomm-linux/meta-qcom-3rdparty/actions/runs/36785803193/job/110130170699)
of 30 September 2026. A first build without such a cache downloads and compiles
every component and takes much longer; the project publishes no time for it.

## 4. Find the result

```sh
ls "$KAS_WORK_DIR/build/tmp/deploy/images/rubikpi3/"
```

Expected result: the listing includes
`core-image-base-rubikpi3.rootfs.qcomflash.tar.gz`, the flashable package with
the boot firmware, partition tables, and root file system, and
`core-image-base-rubikpi3.rootfs.ext4`. To write the package to the board,
follow `meta-qcom`'s
[flashing instructions](https://github.com/qualcomm-linux/meta-qcom/blob/master/docs/flashing.md).

For the Qualcomm Linux distribution's images, add its fragment:
`kas-container build ci/rubikpi3.yml:ci/qcom-distro.yml`. For the Radxa Dragon
Q6A, use `ci/radxa-dragon-q6a.yml`; it also produces a `.wic.gz` disk image.
The [configuration reference](CONFIGURATION.md) explains these files.
