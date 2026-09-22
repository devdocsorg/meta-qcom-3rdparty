# Build a RUBIK Pi 3 image

This tutorial uses the layer's machine configuration to produce a Yocto image for
Thundercomm RUBIK Pi 3. Prerequisites are the [development setup](../contributing/DEVELOPMENT.md),
working container runtime, network access to public sources, and sufficient disk
space and time for a Yocto build. A board is needed only for subsequent hardware
validation; this tutorial finishes at deployable build output.

## 1. Select the board and image

From the checkout, inspect [the machine configuration](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/offline-layer-guides/conf/machine/rubikpi3.conf)
and [kas fragment](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/offline-layer-guides/ci/rubikpi3.yml).
It includes `ci/base.yml`, which imports the base layers and BitBake from `meta-qcom`.
The [configuration reference](CONFIGURATION.md) explains the optional distro fragment.
Keep the [external storage exports](../contributing/DEVELOPMENT.md#3-configure-external-build-storage)
in the same shell.

## 2. Verify the selected layer before building

```sh
"${KAS_CONTAINER:-kas-container}" shell ci/rubikpi3.yml -c 'bitbake-layers show-layers'
```

Expected result: the layer list includes `qcom-3rdparty`, `qcom`, and the core
layer. This metadata check does not compile an image.

## 3. Build the image

```sh
"${KAS_CONTAINER:-kas-container}" shell ci/rubikpi3.yml -c 'bitbake core-image-base'
```

BitBake fetches dependencies, compiles packages, and creates deploy artifacts for
`rubikpi3`. The shared [agent build guide](../contributing/AGENTS.md#3-build-with-kas-container-ci-style)
also covers the Qualcomm distro and world-build compositions.

## 4. Inspect the output

```sh
"${KAS_CONTAINER:-kas-container}" shell ci/rubikpi3.yml -c 'bitbake-getvar --value DEPLOY_DIR_IMAGE'
```

List the returned directory inside the kas shell. Expect `core-image-base-rubikpi3`
image artifacts and associated boot files, with filenames and formats determined
by the selected upstream layers. The container's `/work` maps to `KAS_WORK_DIR`
on the host. Preserve the build configuration and layer revisions with your image.
Consult the board vendor's flashing procedure before writing any storage; this
repository's contributor policy requires flashing and runtime validation for
product changes. Producing files alone does not establish successful boot.

## Use another board or an existing workspace

Select `ci/radxa-dragon-q6a.yml` for Radxa Dragon Q6A. Its Yocto output is an OS disk
image; SPI NOR firmware is managed and flashed separately by Radxa.
The [machine inventory](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/offline-layer-guides/conf/machine/README.md)
links both definitions. To integrate the layer into an existing compatible Yocto
workspace, retain the original manual route:

```sh
git clone https://github.com/qualcomm-linux/meta-qcom-3rdparty.git
bitbake-layers add-layer ../meta-qcom-3rdparty
```

Use matching release branches for all layers, including the required `core` and
`qcom` collections. See [branch guidance](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/offline-layer-guides/BRANCHES.md).
