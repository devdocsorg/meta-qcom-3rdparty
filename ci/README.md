# CI configuration

[kas](https://kas.readthedocs.io/) files that compose the CI builds, and the
scripts that check the layer inside the kas container. The
[configuration reference](../docs/source/user/CONFIGURATION.md#kas-files)
explains each kas setting, and the
[agent guide](../docs/source/contributing/AGENTS.md) shows how to run them.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [base.yml](base.yml) — Adds this layer to [meta-qcom](https://github.com/qualcomm-linux/meta-qcom)'s base build configuration.
- [ci.yml](ci.yml) — Applies [meta-qcom](https://github.com/qualcomm-linux/meta-qcom)'s CI build settings.
- [linux-qcom-next.yml](linux-qcom-next.yml) — Forces the `linux-qcom-next` kernel.
- [meta-qcom.yml](meta-qcom.yml) — Declares the [meta-qcom](https://github.com/qualcomm-linux/meta-qcom) repository for the fragments that include its files.
- [mirror.yml](mirror.yml) — Uses the Yocto Project shared-state mirror through [meta-qcom](https://github.com/qualcomm-linux/meta-qcom)'s fragment.
- [qcom-distro.yml](qcom-distro.yml) — Builds the Qualcomm Linux distribution through [meta-qcom](https://github.com/qualcomm-linux/meta-qcom)'s fragment.
- [radxa-dragon-q6a.yml](radxa-dragon-q6a.yml) — Selects the Radxa Dragon Q6A machine.
- [rubikpi3.yml](rubikpi3.yml) — Selects the Thundercomm RUBIK Pi 3 machine.
- [world.yml](world.yml) — Builds every recipe from [meta-qcom](https://github.com/qualcomm-linux/meta-qcom) and this layer.
- [kas-container-shell-helper.sh](kas-container-shell-helper.sh) — Runs a check script inside the kas container with the base configuration.
- [yocto-buildstats.sh](yocto-buildstats.sh) — Charts and summarises the latest build's task times.
- [yocto-check-layer.sh](yocto-check-layer.sh) — Runs the Yocto Project layer compatibility checks on every machine.
- [yocto-patchreview.sh](yocto-patchreview.sh) — Fails on patches with a malformed `Signed-off-by` or `Upstream-Status`.
