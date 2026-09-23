# ci

Composes kas builds and runs the CI helper scripts.

## Files

- [README.md](README.md) — Describes this folder and indexes its immediate contents.
- [base.yml](base.yml) — Loads meta-qcom’s base layers and adds this checkout.
- [ci.yml](ci.yml) — Includes the parent layer’s CI tuning.
- [kas-container-shell-helper.sh](kas-container-shell-helper.sh) — Runs a repository CI script in the base kas environment.
- [linux-qcom-next.yml](linux-qcom-next.yml) — Selects linux-qcom-next as the kernel provider.
- [meta-qcom.yml](meta-qcom.yml) — Declares the upstream meta-qcom repository and branch.
- [mirror.yml](mirror.yml) — Includes the parent sstate mirror configuration.
- [qcom-distro.yml](qcom-distro.yml) — Selects the Qualcomm distro’s layers and image targets.
- [radxa-dragon-q6a.yml](radxa-dragon-q6a.yml) — Selects Radxa Dragon Q6A on top of the shared base.
- [rubikpi3.yml](rubikpi3.yml) — Selects RUBIK Pi 3 on top of the shared base.
- [world.yml](world.yml) — Builds world for the qcom and qcom-3rdparty collections.
- [yocto-buildstats.sh](yocto-buildstats.sh) — Produces an SVG chart and task-duration summary from build statistics.
- [yocto-check-layer.sh](yocto-check-layer.sh) — Checks a fresh clone against dependencies and both machine definitions.
- [yocto-patchreview.sh](yocto-patchreview.sh) — Checks recipe patches for submission metadata.
