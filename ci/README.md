# ci

Composes kas builds and provides CI-equivalent validation helpers.

See the [configuration reference](../docs/source/user/CONFIGURATION.md) for settings and precedence.

## Files

- [README.md](README.md) — Introduces this folder and indexes its maintained contents.
- [base.yml](base.yml) — Includes the meta-qcom base composition and enables this layer.
- [ci.yml](ci.yml) — Includes the parent CI configuration.
- [kas-container-shell-helper.sh](kas-container-shell-helper.sh) — Runs a repository helper in the kas container environment.
- [linux-qcom-next.yml](linux-qcom-next.yml) — Selects the linux-qcom-next kernel provider for a build.
- [meta-qcom.yml](meta-qcom.yml) — Declares the parent meta-qcom checkout and branch.
- [mirror.yml](mirror.yml) — Includes the parent download-mirror configuration.
- [qcom-distro.yml](qcom-distro.yml) — Includes the optional Qualcomm distro image composition.
- [radxa-dragon-q6a.yml](radxa-dragon-q6a.yml) — Selects the Radxa Dragon Q6A machine.
- [rubikpi3.yml](rubikpi3.yml) — Selects the Thundercomm RUBIK Pi 3 machine.
- [world.yml](world.yml) — Restricts a world build to recipes in this layer and meta-qcom.
- [yocto-buildstats.sh](yocto-buildstats.sh) — Renders buildstats charts and a duration summary.
- [yocto-check-layer.sh](yocto-check-layer.sh) — Checks all local machines with upstream Yocto layer validation.
- [yocto-patchreview.sh](yocto-patchreview.sh) — Checks patch metadata and rejects malformed submission fields.
