# CI configuration

kas fragments that compose the CI builds, and the check scripts that CI runs inside
the kas container. The [build tutorial](../docs/source/user/USAGE.md) uses the
machine fragments, and the
[configuration reference](../docs/source/user/CONFIGURATION.md#kas-configuration)
explains each fragment's settings.

## Files

- [README.md](README.md) — Describes the CI configuration and lists its files.
- [base.yml](base.yml) — Builds this layer on top of the base configuration of [meta-qcom](https://github.com/qualcomm-linux/meta-qcom).
- [rubikpi3.yml](rubikpi3.yml) — Selects the Thundercomm RUBIK Pi 3 machine.
- [radxa-dragon-q6a.yml](radxa-dragon-q6a.yml) — Selects the Radxa Dragon Q6A machine.
- [meta-qcom.yml](meta-qcom.yml) — Declares the meta-qcom repository for the fragments that include its files.
- [qcom-distro.yml](qcom-distro.yml) — Adds meta-qcom's Qualcomm Linux distribution configuration.
- [ci.yml](ci.yml) — Adds meta-qcom's CI build settings.
- [mirror.yml](mirror.yml) — Adds meta-qcom's shared-state mirror setting.
- [linux-qcom-next.yml](linux-qcom-next.yml) — Forces the `linux-qcom-next` kernel.
- [world.yml](world.yml) — Builds every recipe of meta-qcom and this layer.
- [kas-container-shell-helper.sh](kas-container-shell-helper.sh) — Runs a check script inside the kas container with this layer's base configuration.
- [yocto-patchreview.sh](yocto-patchreview.sh) — Reviews the layer's patches and fails on malformed sign-off or upstream-status tags.
- [yocto-check-layer.sh](yocto-check-layer.sh) — Runs the Yocto Project layer compatibility checks for every machine in the layer.
- [yocto-buildstats.sh](yocto-buildstats.sh) — Charts and summarises the build statistics of the latest build.
