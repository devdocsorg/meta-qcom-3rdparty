# Build an image for a board

This tutorial builds the `core-image-base` image for the Thundercomm RUBIK Pi 3
(`rubikpi3`) with kas-container and finds the files to flash. The same steps
build the Radxa Dragon Q6A with `ci/radxa-dragon-q6a.yml`.

## Prerequisites

- A Linux host that meets the Yocto Project's
  [build host requirements](https://docs.yoctoproject.org/brief-yoctoprojectqs/index.html#compatible-linux-distribution):
  at least 140 GB of free disk space and 32 GB of RAM.
- Docker or Podman, and
  [kas-container](https://kas.readthedocs.io/en/latest/userguide/kas-container.html),
  tested with kas-container 4.8.2 and Docker 29.7.
- Git and network access to fetch the layers and their sources.

## 1. Clone the layer

```sh
git clone -b docs/upgrade-test-1007a https://github.com/devdocsorg/meta-qcom-3rdparty.git
cd meta-qcom-3rdparty
```

This proposal branch carries the `.env.example` file used in the next step.

## 2. Choose the work and cache directories

```sh
cp .env.example .env
set -a; . ./.env; set +a
mkdir -p "$KAS_WORK_DIR"
```

Edit `.env` before loading it to move the directories; the comments in
[.env.example](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1007a/.env.example)
describe each setting. The work directory holds the layer checkouts and the
build, so keep it outside this checkout.

## 3. Build the image

```sh
"${KAS_CONTAINER:-kas-container}" build ci/rubikpi3.yml
```

[ci/rubikpi3.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1007a/ci/rubikpi3.yml)
selects the machine and includes the base fragment, which takes
`core-image-base` and the `nodistro` distribution from
[`meta-qcom`](https://github.com/qualcomm-linux/meta-qcom). To build with the
Qualcomm reference distribution instead, add its fragment:
`ci/rubikpi3.yml:ci/qcom-distro.yml`.

In CI, with shared download and shared-state caches, the `rubikpi3/nodistro`
job ran its world and image builds in about 7 minutes
([nightly run](https://github.com/qualcomm-linux/meta-qcom-3rdparty/actions/runs/37555820036/job/112586309806)).
The caches decide the time: when 188 of the world build's 6,326 shared-state
entries missed, the same job's world build took about 2 hours
([nightly run](https://github.com/qualcomm-linux/meta-qcom-3rdparty/actions/runs/36506511249/job/109209256651)).
A first build with empty caches reuses none of the image's roughly 6,400 tasks,
so plan for hours, not minutes.

## Expected result

The build ends without errors, and
`$KAS_WORK_DIR/build/tmp/deploy/images/rubikpi3/` holds these links to the
latest timestamped files:

| File | Contents |
| --- | --- |
| `core-image-base-rubikpi3.rootfs.ext4` | The root file system image. |
| `core-image-base-rubikpi3.rootfs.qcomflash/` | The flashable package: boot firmware, partition tables, and the root file system. |
| `core-image-base-rubikpi3.rootfs.qcomflash.tar.gz` | The same package as a tarball. |

The `qcomflash` package comes from
[image_types_qcom.bbclass](https://github.com/qualcomm-linux/meta-qcom/blob/9e35027ec5d241619a1b1e32b0aaf542a6886645/classes-recipe/image_types_qcom.bbclass)
in meta-qcom. To add the layer to an existing Yocto Project build instead,
follow the [quick start](../README.md#quick-start).
