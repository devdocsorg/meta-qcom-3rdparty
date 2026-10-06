# Build an image for the RUBIK Pi 3

This tutorial builds `core-image-base` for the Thundercomm RUBIK Pi 3 with
`kas-container` from [kas](https://github.com/siemens/kas), which runs kas,
[BitBake](https://github.com/openembedded/bitbake), and the build dependencies in
a container. The result is the flashable `qcomflash` package and an ext4 root file
system.

## Prerequisites

- An x86-64 Linux host that meets the Yocto Project
  [system requirements](https://docs.yoctoproject.org/dev/ref-manual/system-requirements.html),
  with network access.
- Git and [Docker](https://docs.docker.com/engine/install/), tested with 29.7.
- [`kas-container`](https://kas.readthedocs.io/en/latest/userguide/kas-container.html) 5.5 on
  your `PATH`, for example:

  ```sh
  mkdir -p ~/.local/bin
  curl -sSfL -o ~/.local/bin/kas-container https://raw.githubusercontent.com/siemens/kas/5.5/kas-container
  chmod +x ~/.local/bin/kas-container
  ```

## 1. Clone the layer

```sh
git clone -b docs/upgrade-test-1006d https://github.com/devdocsorg/meta-qcom-3rdparty.git
cd meta-qcom-3rdparty
```

## 2. Set the work directories

Keep the kas checkouts, the build, and the caches outside the repository. Copy
the example settings, adjust the paths if needed, load them, and create the work
directory;
[.env.example](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006d/.env.example)
explains each setting:

```sh
cp .env.example .env
set -a; . ./.env; set +a
mkdir -p "$KAS_WORK_DIR"
```

## 3. Build the image

```sh
kas-container build ci/rubikpi3.yml
```

kas clones [`meta-qcom`](https://github.com/qualcomm-linux/meta-qcom),
[OpenEmbedded-Core](https://github.com/openembedded/openembedded-core), and BitBake
into `$KAS_WORK_DIR`, then BitBake runs about 6,300 tasks to build the image. The
project's CI reuses a shared-state cache and builds this machine, including a
world build, in about
[9 minutes](https://github.com/qualcomm-linux/meta-qcom-3rdparty/actions/runs/36785803193).
A first build without that cache compiles every task from source; on a 16-core
host limited to 4 tasks at a time, one had reached only about half of its tasks
after 54 minutes.

## Expected result

```sh
ls "$KAS_WORK_DIR/build/tmp/deploy/images/rubikpi3/"
```

The folder holds the deploy files, including these links to the latest image:

```text
core-image-base-rubikpi3.rootfs.ext4
core-image-base-rubikpi3.rootfs.qcomflash
core-image-base-rubikpi3.rootfs.qcomflash.tar.gz
```

The `qcomflash` folder and its `.tar.gz` archive hold the boot firmware, partition
tables, and root file system; `meta-qcom`'s
[flashing guide](https://github.com/qualcomm-linux/meta-qcom/blob/master/docs/flashing.md)
installs them on the board.

For the Radxa Dragon Q6A, build `ci/radxa-dragon-q6a.yml` instead; it also
produces a `.wic.gz` disk image. To build the Qualcomm Linux distribution images,
add `ci/qcom-distro.yml`: `kas-container build ci/rubikpi3.yml:ci/qcom-distro.yml`.
