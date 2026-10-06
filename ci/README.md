# CI build fragments and checks

[kas](https://kas.readthedocs.io/en/latest/userguide.html) fragments that compose
the CI builds, and the scripts that run the layer checks inside kas-container.
The [configuration reference](../docs/source/user/CONFIGURATION.md#kas-build-fragments)
explains each fragment, and the [agent guide](../docs/source/contributing/AGENTS.md)
shows how CI combines them.

## Files

- [README.md](README.md) — Describes the build fragments and check scripts.
- [base.yml](base.yml) — Builds this layer on [meta-qcom](https://github.com/qualcomm-linux/meta-qcom)'s base configuration.
- [ci.yml](ci.yml) — Adds [meta-qcom](https://github.com/qualcomm-linux/meta-qcom)'s CI settings.
- [linux-qcom-next.yml](linux-qcom-next.yml) — Selects the `linux-qcom-next` kernel.
- [meta-qcom.yml](meta-qcom.yml) — Declares the [meta-qcom](https://github.com/qualcomm-linux/meta-qcom) repository for fragments that include its files.
- [mirror.yml](mirror.yml) — Adds [meta-qcom](https://github.com/qualcomm-linux/meta-qcom)'s download mirror settings.
- [qcom-distro.yml](qcom-distro.yml) — Builds with [meta-qcom](https://github.com/qualcomm-linux/meta-qcom)'s Qualcomm distribution fragment.
- [radxa-dragon-q6a.yml](radxa-dragon-q6a.yml) — Selects the `radxa-dragon-q6a` machine.
- [rubikpi3.yml](rubikpi3.yml) — Selects the `rubikpi3` machine.
- [world.yml](world.yml) — Builds every recipe in [meta-qcom](https://github.com/qualcomm-linux/meta-qcom) and this layer.
- [kas-container-shell-helper.sh](kas-container-shell-helper.sh) — Runs a check script inside kas-container with this layer mounted.
- [yocto-buildstats.sh](yocto-buildstats.sh) — Charts and summarises the latest build's task timings.
- [yocto-check-layer.sh](yocto-check-layer.sh) — Runs `yocto-check-layer` against every machine in the layer.
- [yocto-patchreview.sh](yocto-patchreview.sh) — Fails when a patch in the layer has a malformed sign-off or Upstream-Status tag.
