# CI configuration

kas files that select what to build, and the scripts CI runs inside kas-container.
The [configuration reference](../docs/source/user/CONFIGURATION.md#kas-files)
explains the kas files, and the
[agent guide](../docs/source/contributing/AGENTS.md) shows how to run the scripts.

## Files

- [README.md](README.md) — Lists the kas files and CI scripts.
- [base.yml](base.yml) — Shared build: [meta-qcom](https://github.com/qualcomm-linux/meta-qcom)'s base configuration plus this layer.
- [rubikpi3.yml](rubikpi3.yml) — Builds the Thundercomm RUBIK Pi 3 machine.
- [radxa-dragon-q6a.yml](radxa-dragon-q6a.yml) — Builds the Radxa Dragon Q6A machine.
- [meta-qcom.yml](meta-qcom.yml) — Declares the [meta-qcom](https://github.com/qualcomm-linux/meta-qcom) repository for the fragments below.
- [qcom-distro.yml](qcom-distro.yml) — Switches the build to the Qualcomm Linux distribution.
- [ci.yml](ci.yml) — Applies [meta-qcom](https://github.com/qualcomm-linux/meta-qcom)'s CI build settings.
- [mirror.yml](mirror.yml) — Uses the Yocto Project shared-state mirror.
- [linux-qcom-next.yml](linux-qcom-next.yml) — Forces the `linux-qcom-next` kernel.
- [world.yml](world.yml) — Builds every recipe in [meta-qcom](https://github.com/qualcomm-linux/meta-qcom) and this layer.
- [kas-container-shell-helper.sh](kas-container-shell-helper.sh) — Runs one of these scripts inside kas-container with `base.yml`.
- [yocto-patchreview.sh](yocto-patchreview.sh) — Fails on patches with a malformed sign-off or upstream status.
- [yocto-check-layer.sh](yocto-check-layer.sh) — Runs `yocto-check-layer` on this layer for every machine it defines.
- [yocto-buildstats.sh](yocto-buildstats.sh) — Charts and summarises the last build's task timings.
