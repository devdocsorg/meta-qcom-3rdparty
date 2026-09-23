# Build and inspect a board image

Use the layer's kas fragments to produce an image for Thundercomm RUBIK Pi 3
or Radxa Dragon Q6A. You need a Linux build host, sufficient disk space for a
Yocto build, network access to upstream sources, and the
[development prerequisites and external caches](../contributing/DEVELOPMENT.md#checkout-and-prerequisites).
Run commands from the checkout root after the Docker/Podman smoke tests.

1. Select one board using its kas fragment. RUBIK Pi 3 is the example here:

   ```sh
   export KAS_YAMLS="ci/rubikpi3.yml"
   ```

   For Radxa, use `ci/radxa-dragon-q6a.yml`. Append `:ci/qcom-distro.yml`
   when building the Qualcomm distribution; omit it for the base `nodistro` image.

2. Inspect the merged configuration and record its resolved sources:

   ```sh
   "${KAS_CONTAINER:-kas-container}" dump "${KAS_YAMLS}"
   "${KAS_CONTAINER:-kas-container}" lock "${KAS_YAMLS}"
   ```

   Expect the selected `machine`, this layer, `meta-qcom`, OpenEmbedded Core,
   and BitBake. Optional distro layers appear only with the distro fragment.
   The lock file records revisions for repeatable builds; do not substitute layers
   from a different release. See [kas lockfiles](https://kas.readthedocs.io/en/4.8.2/userguide/project-configuration.html).

3. Build the image selected by that composition:

   ```sh
   "${KAS_CONTAINER:-kas-container}" build "${KAS_YAMLS}"
   ```

   The base composition selects `core-image-base`; the distro fragment selects
   the Qualcomm image. Follow the [CI-style build procedure](../contributing/AGENTS.md#3-build-with-kas-container-ci-style)
   for world builds and alternative combinations.

4. Inspect the deploy directory inside the kas build environment:

   ```sh
   "${KAS_CONTAINER:-kas-container}" shell "${KAS_YAMLS}" -c 'bitbake-getvar --value DEPLOY_DIR_IMAGE'
   ```

   The printed directory contains the selected machine's image, kernel, device
   tree, and image manifest. The manifest lists installed packages and versions.
   Radxa produces `wic`, compressed `wic.gz`, and `wic.bmap` OS disk artifacts;
   its SPI NOR firmware is managed separately by Radxa. RUBIK Pi 3 additionally
   deploys its board boot firmware and CDT for the inherited Qualcomm image tools.
   Compare the board and image names before using the artifacts on hardware.

A completed BitBake build and populated deploy directory establish image creation.
Booting and testing on the matching board establish runtime support. Use the
board vendor's flashing instructions and the inherited `meta-qcom` image tooling;
this tutorial does not overwrite connected storage. RUBIK Pi 3 Wi-Fi/Bluetooth
firmware is omitted by this layer's packagegroup; see [machine settings](CONFIGURATION.md#machines).
