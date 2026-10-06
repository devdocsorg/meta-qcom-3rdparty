# CI configuration

kas fragments that compose a build, and the scripts CI runs to check the layer.
Combine fragments with `:`, for example `ci/rubikpi3.yml:ci/qcom-distro.yml`; the
[configuration reference](../docs/source/user/CONFIGURATION.md#kas-fragments)
describes each one, and the [agent guide](../docs/source/contributing/AGENTS.md)
shows how to run the scripts.

## Files

- [README.md](README.md) — Introduces the kas fragments and CI scripts.
- [base.yml](base.yml) — Adds this layer to [meta-qcom](https://github.com/qualcomm-linux/meta-qcom)'s base build configuration.
- [ci.yml](ci.yml) — Adds meta-qcom's CI build tuning.
- [meta-qcom.yml](meta-qcom.yml) — Declares the meta-qcom repository for the fragments that include its files.
- [mirror.yml](mirror.yml) — Adds meta-qcom's shared-state mirror.
- [qcom-distro.yml](qcom-distro.yml) — Selects the Qualcomm Linux distribution, its layers, and its images.
- [linux-qcom-next.yml](linux-qcom-next.yml) — Selects the `linux-qcom-next` kernel.
- [world.yml](world.yml) — Builds every recipe in the Qualcomm layers.
- [radxa-dragon-q6a.yml](radxa-dragon-q6a.yml) — Selects the Radxa Dragon Q6A machine.
- [rubikpi3.yml](rubikpi3.yml) — Selects the Thundercomm RUBIK Pi 3 machine.
- [kas-container-shell-helper.sh](kas-container-shell-helper.sh) — Runs one of these scripts inside a kas-container shell.
- [yocto-check-layer.sh](yocto-check-layer.sh) — Runs `yocto-check-layer` against this layer's machines.
- [yocto-patchreview.sh](yocto-patchreview.sh) — Checks the layer's patches and fails on malformed sign-off or upstream-status tags.
- [yocto-buildstats.sh](yocto-buildstats.sh) — Charts and summarises the build statistics of the latest build.
