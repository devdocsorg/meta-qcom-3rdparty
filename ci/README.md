# ci

Container helper scripts and kas configuration fragments.

## Files

- [README.md](README.md): Introduces this directory and lists its contents.
- [base.yml](base.yml): Combines the current layer with the upstream base build configuration.
- [ci.yml](ci.yml): Imports upstream CI-specific build settings.
- [kas-container-shell-helper.sh](kas-container-shell-helper.sh): Runs a repository script inside the base kas container shell.
- [linux-qcom-next.yml](linux-qcom-next.yml): Selects linux-qcom-next as the kernel provider.
- [meta-qcom.yml](meta-qcom.yml): Declares the upstream meta-qcom repository and branch.
- [mirror.yml](mirror.yml): Imports upstream download-mirror settings.
- [qcom-distro.yml](qcom-distro.yml): Imports the Qualcomm distro configuration.
- [radxa-dragon-q6a.yml](radxa-dragon-q6a.yml): Selects the Dragon Q6A machine and base configuration.
- [rubikpi3.yml](rubikpi3.yml): Selects the RUBIK Pi 3 machine and base configuration.
- [world.yml](world.yml): Selects world builds restricted to the two BSP layers.
- [yocto-buildstats.sh](yocto-buildstats.sh): Renders and summarizes the latest BitBake build statistics.
- [yocto-check-layer.sh](yocto-check-layer.sh): Checks a committed layer clone against all configured machines.
- [yocto-patchreview.sh](yocto-patchreview.sh): Checks patch metadata using the OpenEmbedded patch reviewer.
