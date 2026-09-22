# CI build configurations and helper scripts

CI build configurations and helper scripts.

<!-- folder-index:start -->

## Files

- [README.md](README.md) — Introduces this folder and indexes its immediate contents.
- [base.yml](base.yml) — Imports the meta-qcom base build and adds this checkout as a layer.
- [ci.yml](ci.yml) — Imports the parent CI build settings.
- [kas-container-shell-helper.sh](kas-container-shell-helper.sh) — Runs a CI helper inside the configured kas environment.
- [linux-qcom-next.yml](linux-qcom-next.yml) — Selects the linux-qcom-next kernel provider.
- [meta-qcom.yml](meta-qcom.yml) — Declares the parent meta-qcom repository and master branch.
- [mirror.yml](mirror.yml) — Imports the parent download mirror settings.
- [qcom-distro.yml](qcom-distro.yml) — Imports the optional Qualcomm distro composition.
- [radxa-dragon-q6a.yml](radxa-dragon-q6a.yml) — Selects the Radxa Dragon Q6A machine with the base layers.
- [rubikpi3.yml](rubikpi3.yml) — Selects the RUBIK Pi 3 machine with the base layers.
- [world.yml](world.yml) — Enables world builds for the qcom and qcom-3rdparty collections.
- [yocto-buildstats.sh](yocto-buildstats.sh) — Generates charts and a summary from the latest BitBake build statistics.
- [yocto-check-layer.sh](yocto-check-layer.sh) — Clones the committed layer and checks its machines in an isolated build directory.
- [yocto-patchreview.sh](yocto-patchreview.sh) — Checks patch metadata and fails malformed sign-offs or upstream status.

<!-- folder-index:end -->
