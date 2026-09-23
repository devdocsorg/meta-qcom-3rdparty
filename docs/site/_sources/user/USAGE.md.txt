# Build a RUBIK Pi 3 image

## Prerequisites

Prepare the checkout, kas-container, container runtime, and external work/cache
directories using [development setup](../contributing/DEVELOPMENT.md#checkout-and-prerequisites).
Use a Linux build host with enough disk space for a Yocto image build and network
access to the configured source mirrors. No board is needed to produce artifacts.
The [machine configuration](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/main/conf/machine/rubikpi3.conf)
selects the QCS6490 baseline and this layer’s boot firmware.

## 1. Select the machine

From the checkout root, inspect the composition and fetch its layers:

```sh
"${KAS_CONTAINER:-kas-container}" checkout ci/rubikpi3.yml
```

The composition adds this layer to meta-qcom, OpenEmbedded Core, and BitBake.
The base chooses `nodistro` and `core-image-base`; the machine fragment overrides
its unset machine with `rubikpi3`. Branches follow upstream development, so record
the resolved revisions for a reproducible build.

## 2. Build the image

Use [the agent guide’s kas build procedure](../contributing/AGENTS.md#3-build-with-kas-container-ci-style)
for Qualcomm distro or world builds. For a smaller base image:

```sh
"${KAS_CONTAINER:-kas-container}" build ci/rubikpi3.yml
```

Expected result: kas and BitBake exit successfully and populate the machine’s
deploy directory. To build the Qualcomm Linux image targets instead, append
`:ci/qcom-distro.yml`; this adds the distro’s layers and target images. The
[configuration reference](CONFIGURATION.md#kas-compositions) lists these choices.

## 3. Inspect and retain the output

```sh
find "${KAS_WORK_DIR}/build/tmp/deploy/images/rubikpi3" -maxdepth 1 -type f -printf '%f\n'
```

The deploy directory contains image artifacts, the selected device tree, and boot
assets assembled by the inherited meta-qcom image classes. Keep the image, its
manifest, and the build configuration together. File names and formats depend on
the selected image/distro; a successful documentation build does not create them.

To inspect the resolved recipe environment without compiling an image:

```sh
"${KAS_CONTAINER:-kas-container}" shell ci/rubikpi3.yml -c 'bitbake-getvar -r core-image-base DEPLOY_DIR_IMAGE'
```

Use the reported directory if the build configuration overrides `TMPDIR`.
Do not flash a different board’s boot firmware. Follow the board vendor’s current
flashing procedure for hardware deployment. RUBIK Pi 3 Wi-Fi and Bluetooth blobs
are omitted by this layer’s packagegroup; the board can boot without them.

## Other machines and existing workspaces

Use `ci/radxa-dragon-q6a.yml` for Radxa Dragon Q6A. This configuration builds the
OS disk image (ESP and root filesystem); Radxa manages SPI NOR firmware separately.
Its default sector size is 512 for SD; UFS requires the documented 4096 override.
The [machine folder](https://github.com/qualcomm-linux/meta-qcom-3rdparty/tree/main/conf/machine)
contains the complete supported-machine list.

For an existing compatible Yocto workspace with `core` and `qcom` already enabled,
clone the layer and run `bitbake-layers add-layer ../meta-qcom-3rdparty` from that
workspace’s initialised build shell. This branch declares `wrynose` compatibility;
keep all layer release branches aligned. See the [branch guide](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/offline-contributor-guides/BRANCHES.md).
