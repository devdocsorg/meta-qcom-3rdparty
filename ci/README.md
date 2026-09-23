# CI configuration

kas fragments and helper scripts used by the GitHub workflows and for local
builds. Combine fragments with colons, as the
[usage tutorial](../docs/source/user/USAGE.md) and
[configuration reference](../docs/source/user/CONFIGURATION.md#kas-fragments) show.

## Files

- [README.md](README.md) — Describes the kas fragments and helper scripts.
- [base.yml](base.yml) — Includes meta-qcom's base kas configuration and adds this layer.
- [ci.yml](ci.yml) — Adds meta-qcom's CI build settings.
- [kas-container-shell-helper.sh](kas-container-shell-helper.sh) — Runs a script from this repository inside the kas container.
- [linux-qcom-next.yml](linux-qcom-next.yml) — Forces the `linux-qcom-next` kernel.
- [meta-qcom.yml](meta-qcom.yml) — Declares the meta-qcom repository for fragments that include its files.
- [mirror.yml](mirror.yml) — Adds meta-qcom's shared state mirror setting.
- [qcom-distro.yml](qcom-distro.yml) — Builds with the Qualcomm Linux distribution and its layers.
- [radxa-dragon-q6a.yml](radxa-dragon-q6a.yml) — Selects the Radxa Dragon Q6A machine.
- [rubikpi3.yml](rubikpi3.yml) — Selects the Thundercomm RUBIK Pi 3 machine.
- [world.yml](world.yml) — Builds every recipe from meta-qcom and this layer.
- [yocto-buildstats.sh](yocto-buildstats.sh) — Charts and summarises task durations from the latest build.
- [yocto-check-layer.sh](yocto-check-layer.sh) — Runs `yocto-check-layer` against every machine in this layer.
- [yocto-patchreview.sh](yocto-patchreview.sh) — Checks patch headers and fails on malformed sign-offs or upstream status.
