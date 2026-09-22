# Build an image for a supported board

This layer produces Yocto board support, consumed by an image build. This tutorial
uses Thundercomm RUBIK Pi 3 and `core-image-base`; Radxa Dragon Q6A uses the same
steps with `ci/radxa-dragon-q6a.yml`.

## Prerequisites

Complete the [development environment](../contributing/DEVELOPMENT.md), including
container smoke tests and work/cache directories. Allow enough disk and memory
for a Yocto image build; the inherited base configuration stops work when disk
space is low. Internet access is needed for source downloads. A hardware board is
not needed to build or inspect the image.

## Build and inspect the output

1. From the repository root, inspect the selected machine and output target:

   ```sh
   "$KAS_CONTAINER" dump ci/rubikpi3.yml
   ```

   Expect `machine: rubikpi3`, `distro: nodistro`, and target `core-image-base`,
   with `meta-qcom-3rdparty`, `meta-qcom`, OE-Core, and BitBake in the repository
   list. The [configuration reference](CONFIGURATION.md) explains these values.

2. Run the board build from the [shared build procedure](../contributing/AGENTS.md#3-build-with-kas-container-ci-style):

   ```sh
   "$KAS_CONTAINER" build ci/rubikpi3.yml
   ```

   kas prepares the layers, enters the container, and runs BitBake. A successful
   run ends with the BitBake task summary and deploys image files under
   `$KAS_WORK_DIR/build/tmp/deploy/images/rubikpi3/`.

3. Inspect the image output:

   ```sh
   ls "$KAS_WORK_DIR/build/tmp/deploy/images/rubikpi3/"
   ```

   Expect the `core-image-base-rubikpi3` image artifacts, its package manifest,
   kernel/device tree files, and board boot assets selected by the image classes.
   The exact filenames depend on inherited image types and revisions. This verifies
   build output; it does not flash storage or establish that the board boots.

For Qualcomm distro images, use the existing qcom-distro composition in the
[agent guide](../contributing/AGENTS.md#3-build-with-kas-container-ci-style). It
selects additional layers and image targets; the RUBIK Pi boot-firmware licence
exception applies only to the matching multimedia image.

Radxa Dragon Q6A creates WIC disk images (ESP and root filesystem). Its SPI NOR
firmware is managed separately by Radxa; this layer does not generate it. RUBIK Pi
3 receives vendor boot firmware and its CDT through the pinned `boot-assets`
recipe. Follow the board vendor's flashing instructions for the board and storage
in use after reviewing the generated artifacts.

## Use an existing Yocto workspace

In a configured workspace with compatible OE-Core and `meta-qcom` layers:

```sh
git clone https://github.com/qualcomm-linux/meta-qcom-3rdparty.git
bitbake-layers add-layer ../meta-qcom-3rdparty
```

Set the desired `MACHINE` and image target in that workspace. Branch compatibility
and the dynamic Qualcomm distro integration are described in
[configuration](CONFIGURATION.md).
