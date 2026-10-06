# Build configurations and checks

The [kas](https://github.com/siemens/kas) files here describe the CI builds, and
the scripts run the layer checks inside `kas-container`. The
[build tutorial](../docs/source/user/USAGE.md) uses them to build an image, the
[agent guide](../docs/source/contributing/AGENTS.md#4-run-routine-checks-via-ci-helper-scripts)
runs the checks, and the
[configuration reference](../docs/source/user/CONFIGURATION.md#build-configurations-ci)
explains each file's settings.

## Files

- [base.yml](base.yml) — Combines [`meta-qcom`](https://github.com/qualcomm-linux/meta-qcom)'s base build with this layer.
- [ci.yml](ci.yml) — Adds `meta-qcom`'s CI build settings.
- [kas-container-shell-helper.sh](kas-container-shell-helper.sh) — Runs one of these scripts in a `kas-container` shell set up from `base.yml`.
- [linux-qcom-next.yml](linux-qcom-next.yml) — Selects the `linux-qcom-next` kernel.
- [meta-qcom.yml](meta-qcom.yml) — Declares the `meta-qcom` repository for the files that include from it.
- [mirror.yml](mirror.yml) — Adds `meta-qcom`'s shared-state mirror setting.
- [qcom-distro.yml](qcom-distro.yml) — Switches the build to the `qcom-distro` distribution and its images.
- [radxa-dragon-q6a.yml](radxa-dragon-q6a.yml) — Builds for the Radxa Dragon Q6A.
- [README.md](README.md) — Describes the build configurations and check scripts.
- [rubikpi3.yml](rubikpi3.yml) — Builds for the Thundercomm RUBIK Pi 3.
- [world.yml](world.yml) — Builds every recipe in the `qcom` and `qcom-3rdparty` layers.
- [yocto-buildstats.sh](yocto-buildstats.sh) — Charts and summarises the task statistics of the latest build.
- [yocto-check-layer.sh](yocto-check-layer.sh) — Runs `yocto-check-layer` on this layer for every machine it defines.
- [yocto-patchreview.sh](yocto-patchreview.sh) — Reviews the layer's patches and fails on a malformed sign-off or `Upstream-Status` tag.
