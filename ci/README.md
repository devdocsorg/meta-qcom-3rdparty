<!-- Generated from ci/ at wrynose @ 7649ae51 (2026-08-31) by docsgen on 2026-09-07. Manual edits will be overwritten on regeneration; change the source, not this page. -->

# ci/

The kas build-environment fragments a build composes, and the shell scripts CI runs inside that environment to build and validate the layer on top of `meta-qcom`. Used by [.github/workflows/build-yocto.yml](../.github/workflows/build-yocto.yml) and meta-qcom's compile action.

## Contents

| File | Description | Machine |
| --- | --- | --- |
| [ci/base.yml](base.yml) | kas fragment. Includes `ci/base.yml` from the `meta-qcom` repository (external). Declares repositories `meta-qcom` (branch `wrynose`), `meta-qcom-3rdparty` (this repository). Used by [.github/workflows/build-yocto.yml](../.github/workflows/build-yocto.yml) and [ci/kas-container-shell-helper.sh](kas-container-shell-helper.sh), which invoke it; [ci/radxa-dragon-q6a.yml](radxa-dragon-q6a.yml) and [ci/uno-q.yml](uno-q.yml), which include it. Derived from meta-qcom's `ci/base.yml` and kept in step by hand. | Not set |
| [ci/ci.yml](ci.yml) | kas fragment. Includes `ci/meta-qcom.yml` from this repository, `ci/ci.yml` from the `meta-qcom` repository (external). Used by meta-qcom's compile action, which invokes it. Derived from meta-qcom's `ci/ci.yml` and kept in step by hand. | Not set |
| [ci/kas-container-shell-helper.sh](kas-container-shell-helper.sh) | Shell script run with `/bin/sh -e`. Usage: `kas-container-shell-helper.sh /path/to/script`. An unchanged copy of meta-qcom's `ci/kas-container-shell-helper.sh`; change it there, not here. | Not set |
| [ci/linux-qcom-next.yml](linux-qcom-next.yml) | kas fragment. Adds `local_conf_header` entries `kernelprovider`. Used by [.github/workflows/build-yocto.yml](../.github/workflows/build-yocto.yml), which invokes it. An unchanged copy of meta-qcom's `ci/linux-qcom-next.yml`; change it there, not here. | Not set |
| [ci/meta-qcom.yml](meta-qcom.yml) | kas fragment. Declares repositories `meta-qcom` (branch `wrynose`). Used by [ci/ci.yml](ci.yml), [ci/mirror.yml](mirror.yml) and [ci/qcom-distro.yml](qcom-distro.yml), which include it. An unchanged copy of meta-qcom-distro's `ci/meta-qcom.yml`; change it there, not here. | Not set |
| [ci/mirror.yml](mirror.yml) | kas fragment. Includes `ci/meta-qcom.yml` from this repository, `ci/mirror.yml` from the `meta-qcom` repository (external). No consumer was found in the swept trees. Derived from meta-qcom's `ci/mirror.yml` and kept in step by hand. | Not set |
| [ci/qcom-distro.yml](qcom-distro.yml) | kas fragment. Includes `ci/meta-qcom.yml` from this repository, `ci/qcom-distro.yml` from the `meta-qcom` repository (external). Used by [.github/workflows/build-yocto.yml](../.github/workflows/build-yocto.yml) and meta-qcom's compile action, which invoke it. Derived from meta-qcom's `ci/qcom-distro.yml` and kept in step by hand. | Not set |
| [ci/radxa-dragon-q6a.yml](radxa-dragon-q6a.yml) | kas fragment. Includes `ci/base.yml` from this repository. Used by meta-qcom's compile action, which invokes it through the machine name. | [`radxa-dragon-q6a`](../conf/machine/radxa-dragon-q6a.md) |
| [ci/uno-q.yml](uno-q.yml) | kas fragment. Includes `ci/base.yml` from this repository. Used by meta-qcom's compile action, which invokes it through the machine name. | [`uno-q`](../conf/machine/uno-q.md) |
| [ci/world.yml](world.yml) | kas fragment. Adds `local_conf_header` entries `world_build`. Builds `world`. Used by meta-qcom's compile action, which invokes it. Derived from meta-qcom's `ci/world.yml` and kept in step by hand. | Not set |
| [ci/yocto-buildstats.sh](yocto-buildstats.sh) | Shell script run with `/bin/sh -e`. Usage: `yocto-buildstats.sh REPO_DIR WORK_DIR`. Derived from meta-qcom's `ci/yocto-buildstats.sh` and kept in step by hand. | Not set |
| [ci/yocto-check-layer.sh](yocto-check-layer.sh) | Shell script run with `/bin/bash -e`. Usage: `yocto-check-layer.sh REPO_DIR WORK_DIR`. Derived from meta-qcom's `ci/yocto-check-layer.sh` and kept in step by hand. | Not set |
| [ci/yocto-patchreview.sh](yocto-patchreview.sh) | Shell script run with `/bin/sh -e`. Usage: `yocto-patchreview.sh REPO_DIR WORK_DIR`. An unchanged copy of meta-qcom's `ci/yocto-patchreview.sh`; change it there, not here. | Not set |

## Description

kas is a declarative front end for BitBake and OpenEmbedded builds: a fragment declares the repositories to fetch, the layers and machine to configure, and `local_conf_header` blocks that are concatenated into `local.conf`. Fragments compose on a kas command line or through a header's own includes, with later-merged content overriding scalar keys and extending lists.

The fragments here layer on top of `meta-qcom`'s environment through cross-repository includes. The base fragment includes the like-named fragment from the external `meta-qcom` repository, where the distro, the core repositories and the shared `local_conf_header` entries live, and adds two declarations of its own: `meta-qcom` pinned to a branch, and this repository itself with no URL, which resolves to the checkout kas runs from. The two per-machine fragments each include that base and set `machine`, the minimal delta that makes a build concrete.

Of the six fragments that remain, one carries the `meta-qcom` repository pin alone, which the three cross-repository option fragments each include ahead of the external fragment they pull in: CI signature and package-class settings, an sstate mirror, and the full qcom-distro layer set. The last two stand alone. One pins `PREFERRED_PROVIDER_virtual/kernel`. The other sets `EXCLUDE_FROM_WORLD` for everything and then clears it again for the two Qualcomm layers, so that its `world` target builds the recipes those two layers provide rather than one image.

The shell scripts implement the CI-side checks that run inside a kas environment: a container shell helper that shells into the base environment and runs a named script, an OpenEmbedded-Core patch review that fails on malformed `Signed-off-by` or `Upstream-Status` tags, a `yocto-check-layer` compliance run that derives the machines to validate from `conf/machine/*.conf`, and a buildstats post-processor. Three pieces of this content, `world.yml`, `mirror.yml` and `yocto-buildstats.sh`, are not referenced by this repository's workflows, which are indexed in [.github/workflows/](../.github/workflows/README.md).
