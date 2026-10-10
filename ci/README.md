# CI configuration

kas fragments that compose the builds, and the helper scripts that run the
layer checks inside [kas-container](https://github.com/siemens/kas). The
[configuration reference](../docs/source/user/CONFIGURATION.md#kas-fragments)
explains each fragment's settings.

## Files

- [README.md](README.md) — Lists the kas fragments and helper scripts.
- [base.yml](base.yml) — Adds this layer to [`meta-qcom`](https://github.com/qualcomm-linux/meta-qcom)'s base build configuration.
- [ci.yml](ci.yml) — Adds `meta-qcom`'s CI build settings.
- [kas-container-shell-helper.sh](kas-container-shell-helper.sh) — Runs a repository script in kas-container's shell for `base.yml`, passing it the checkout and work directory.
- [linux-qcom-next.yml](linux-qcom-next.yml) — Selects the `linux-qcom-next` kernel.
- [meta-qcom.yml](meta-qcom.yml) — Declares the `meta-qcom` repository for the fragments that include its files.
- [mirror.yml](mirror.yml) — Adds `meta-qcom`'s sstate mirror setting.
- [qcom-distro.yml](qcom-distro.yml) — Adds `meta-qcom`'s Qualcomm Linux distribution configuration.
- [radxa-dragon-q6a.yml](radxa-dragon-q6a.yml) — Builds for the Radxa Dragon Q6A.
- [rubikpi3.yml](rubikpi3.yml) — Builds for the Thundercomm RUBIK Pi 3.
- [world.yml](world.yml) — Builds every recipe of this layer and `meta-qcom`.
- [yocto-buildstats.sh](yocto-buildstats.sh) — Charts and summarises the latest build's task statistics.
- [yocto-check-layer.sh](yocto-check-layer.sh) — Runs `yocto-check-layer` on this layer for all its machines.
- [yocto-patchreview.sh](yocto-patchreview.sh) — Runs `patchreview` and fails on malformed patch sign-offs or upstream status.
