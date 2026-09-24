# CI build configuration

These kas fragments compose builds as `ci/<machine>.yml[:<fragment>.yml]`, and
the scripts run the Yocto checks inside kas-container. The
[configuration reference](../docs/source/user/CONFIGURATION.md#kas-fragments)
explains the fragments, and the [function reference](../docs/site/contributing/README.html)
documents the scripts' functions.

## Files

- [README.md](README.md) — Describes the kas fragments and CI scripts.
- [base.yml](base.yml) — Includes [meta-qcom](https://github.com/qualcomm-linux/meta-qcom)'s base configuration and adds this layer.
- [ci.yml](ci.yml) — Adds [meta-qcom](https://github.com/qualcomm-linux/meta-qcom)'s CI build settings.
- [linux-qcom-next.yml](linux-qcom-next.yml) — Forces the `linux-qcom-next` kernel provider.
- [meta-qcom.yml](meta-qcom.yml) — Declares the [meta-qcom](https://github.com/qualcomm-linux/meta-qcom) repository for the fragments that include its files.
- [mirror.yml](mirror.yml) — Adds [meta-qcom](https://github.com/qualcomm-linux/meta-qcom)'s shared-state mirror setting.
- [qcom-distro.yml](qcom-distro.yml) — Builds with the Qualcomm Linux distribution and its images.
- [radxa-dragon-q6a.yml](radxa-dragon-q6a.yml) — Builds the Radxa Dragon Q6A machine.
- [rubikpi3.yml](rubikpi3.yml) — Builds the Thundercomm RUBIK Pi 3 machine.
- [world.yml](world.yml) — Builds every recipe of [meta-qcom](https://github.com/qualcomm-linux/meta-qcom) and this layer.
- [kas-container-shell-helper.sh](kas-container-shell-helper.sh) — Runs a CI script inside a kas-container shell.
- [yocto-buildstats.sh](yocto-buildstats.sh) — Charts and summarises the latest build's task durations.
- [yocto-check-layer.sh](yocto-check-layer.sh) — Runs `yocto-check-layer` against every machine in the layer.
- [yocto-patchreview.sh](yocto-patchreview.sh) — Checks patch headers and fails on malformed sign-offs or upstream status.
