# CI build fragments and helper scripts

The kas fragments compose the builds that CI and the
[usage tutorial](../docs/source/user/USAGE.md) run; the
[configuration reference](../docs/source/user/CONFIGURATION.md#kas-fragments)
explains their settings. The scripts run the layer checks inside kas-container,
as the [agent guide](../docs/source/contributing/AGENTS.md#4-run-routine-checks-via-ci-helper-scripts)
shows.

## Files

- [README.md](README.md) — Describes the kas fragments and CI helper scripts.
- [base.yml](base.yml) — Includes the base build of [meta-qcom](https://github.com/qualcomm-linux/meta-qcom) and adds that layer and this one.
- [ci.yml](ci.yml) — Adds the CI build settings of [meta-qcom](https://github.com/qualcomm-linux/meta-qcom).
- [kas-container-shell-helper.sh](kas-container-shell-helper.sh) — Runs a CI script inside kas-container with the base configuration.
- [linux-qcom-next.yml](linux-qcom-next.yml) — Selects the `linux-qcom-next` kernel.
- [meta-qcom.yml](meta-qcom.yml) — Declares the [meta-qcom](https://github.com/qualcomm-linux/meta-qcom) repository for the fragments that reuse its configuration.
- [mirror.yml](mirror.yml) — Adds the shared-state mirror of [meta-qcom](https://github.com/qualcomm-linux/meta-qcom).
- [qcom-distro.yml](qcom-distro.yml) — Adds the Qualcomm Linux distribution build of [meta-qcom](https://github.com/qualcomm-linux/meta-qcom).
- [radxa-dragon-q6a.yml](radxa-dragon-q6a.yml) — Builds for the Radxa Dragon Q6A.
- [rubikpi3.yml](rubikpi3.yml) — Builds for the Thundercomm RUBIK Pi 3.
- [world.yml](world.yml) — Builds every recipe of [meta-qcom](https://github.com/qualcomm-linux/meta-qcom) and this layer.
- [yocto-buildstats.sh](yocto-buildstats.sh) — Charts and summarises the latest build's task statistics.
- [yocto-check-layer.sh](yocto-check-layer.sh) — Runs `yocto-check-layer` on the layer for all of its machines.
- [yocto-patchreview.sh](yocto-patchreview.sh) — Runs `patchreview.py` and fails on malformed patch tags.
