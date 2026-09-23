# CI build inputs

Kas fragments compose machines, distributions, and checks; shell helpers mirror CI.

## Files

- [README.md](README.md) — Orients readers and indexes this folder.
- [base.yml](base.yml) — Includes the parent build and registers this layer.
- [ci.yml](ci.yml) — Includes the parent CI defaults.
- [kas-container-shell-helper.sh](kas-container-shell-helper.sh) — Runs a helper inside the base kas environment.
- [linux-qcom-next.yml](linux-qcom-next.yml) — Selects the Qualcomm next kernel provider.
- [meta-qcom.yml](meta-qcom.yml) — Declares the parent repository used by include fragments.
- [mirror.yml](mirror.yml) — Includes the parent shared-state mirror settings.
- [qcom-distro.yml](qcom-distro.yml) — Includes the optional Qualcomm distribution composition.
- [radxa-dragon-q6a.yml](radxa-dragon-q6a.yml) — Selects the Radxa Dragon Q6A machine.
- [rubikpi3.yml](rubikpi3.yml) — Selects the RUBIK Pi 3 machine.
- [world.yml](world.yml) — Restricts world builds to the Qualcomm and third-party layers.
- [yocto-buildstats.sh](yocto-buildstats.sh) — Renders build timing charts and a sorted summary.
- [yocto-check-layer.sh](yocto-check-layer.sh) — Checks layer compatibility in an isolated build directory.
- [yocto-patchreview.sh](yocto-patchreview.sh) — Checks patch and sign-off metadata.
