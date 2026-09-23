# CI configuration

kas fragments that define the layer's builds, and the scripts CI runs inside
kas-container. The [configuration reference](../docs/source/user/CONFIGURATION.md#kas-fragments)
explains each fragment, the [agent guide](../docs/source/contributing/AGENTS.md)
shows how to run the scripts, and the
[function reference](../docs/source/contributing/README.md#function-reference)
documents their functions.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [base.yml](base.yml) — Includes meta-qcom's base configuration and adds this layer.
- [ci.yml](ci.yml) — Adds meta-qcom's CI build settings.
- [kas-container-shell-helper.sh](kas-container-shell-helper.sh) — Runs a CI script inside kas-container with the base configuration.
- [linux-qcom-next.yml](linux-qcom-next.yml) — Forces the linux-qcom-next kernel.
- [meta-qcom.yml](meta-qcom.yml) — Declares the meta-qcom repository for the distro, CI, and mirror fragments.
- [mirror.yml](mirror.yml) — Adds meta-qcom's shared-state mirror.
- [qcom-distro.yml](qcom-distro.yml) — Builds the Qualcomm Linux distro and its images.
- [radxa-dragon-q6a.yml](radxa-dragon-q6a.yml) — Selects the Radxa Dragon Q6A machine.
- [rubikpi3.yml](rubikpi3.yml) — Selects the Thundercomm RUBIK Pi 3 machine.
- [world.yml](world.yml) — Builds every recipe in meta-qcom and this layer.
- [yocto-buildstats.sh](yocto-buildstats.sh) — Charts and summarises the task statistics of the latest build.
- [yocto-check-layer.sh](yocto-check-layer.sh) — Runs yocto-check-layer on this layer for every machine it defines.
- [yocto-patchreview.sh](yocto-patchreview.sh) — Runs patchreview and fails on malformed patch sign-offs or Upstream-Status tags.
