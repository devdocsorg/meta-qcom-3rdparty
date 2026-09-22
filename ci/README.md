# kas build compositions and CI helper scripts

kas build compositions and CI helper scripts.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [base.yml](base.yml) — Assembles this layer with the upstream meta-qcom base.
- [ci.yml](ci.yml) — Selects upstream CI configuration.
- [kas-container-shell-helper.sh](kas-container-shell-helper.sh) — Invokes a CI helper in the kas container.
- [linux-qcom-next.yml](linux-qcom-next.yml) — Selects the linux-qcom-next kernel provider.
- [meta-qcom.yml](meta-qcom.yml) — Declares the parent meta-qcom checkout.
- [mirror.yml](mirror.yml) — Selects upstream source/build mirror configuration.
- [qcom-distro.yml](qcom-distro.yml) — Selects the optional Qualcomm distro composition.
- [radxa-dragon-q6a.yml](radxa-dragon-q6a.yml) — Selects Radxa Dragon Q6A for kas builds.
- [rubikpi3.yml](rubikpi3.yml) — Selects Thundercomm RUBIK Pi 3 for kas builds.
- [world.yml](world.yml) — Builds all recipes in the two Qualcomm layers.
- [yocto-buildstats.sh](yocto-buildstats.sh) — Summarises BitBake build statistics.
- [yocto-check-layer.sh](yocto-check-layer.sh) — Checks layer compatibility and both machine definitions.
- [yocto-patchreview.sh](yocto-patchreview.sh) — Checks recipe patch metadata.
