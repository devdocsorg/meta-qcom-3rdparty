# CI configuration

kas files and helper scripts for the layer's builds and checks, used by CI and
locally. The [configuration reference](../docs/source/user/CONFIGURATION.md#kas-files) explains each kas
file, and the [agent guide](../docs/source/contributing/AGENTS.md) shows how to
run them.

## Files

- [README.md](README.md) — Indexes the kas files and helper scripts.
- [base.yml](base.yml) — Base kas build: includes the base fragment from [meta-qcom](https://github.com/qualcomm-linux/meta-qcom) and adds this layer.
- [ci.yml](ci.yml) — Adds meta-qcom's CI build settings.
- [kas-container-shell-helper.sh](kas-container-shell-helper.sh) — Runs a helper script inside kas-container with the base build.
- [linux-qcom-next.yml](linux-qcom-next.yml) — Forces the `linux-qcom-next` kernel.
- [meta-qcom.yml](meta-qcom.yml) — Declares the meta-qcom repository for the fragments that include its files.
- [mirror.yml](mirror.yml) — Adds meta-qcom's shared-state mirror.
- [qcom-distro.yml](qcom-distro.yml) — Builds with the `qcom-distro` distribution and its layers.
- [radxa-dragon-q6a.yml](radxa-dragon-q6a.yml) — Selects the Radxa Dragon Q6A machine.
- [rubikpi3.yml](rubikpi3.yml) — Selects the Thundercomm RUBIK Pi 3 machine.
- [world.yml](world.yml) — Limits world builds to the recipes of meta-qcom and this layer.
- [yocto-buildstats.sh](yocto-buildstats.sh) — Charts and summarises the latest build's task statistics.
- [yocto-check-layer.sh](yocto-check-layer.sh) — Runs `yocto-check-layer` on the layer for all its machines.
- [yocto-patchreview.sh](yocto-patchreview.sh) — Reviews the layer's patches and fails on malformed sign-offs or upstream status.
