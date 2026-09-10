<!-- Generated from recipes-bsp/u-boot/u-boot-arduino_git.bb at wrynose @ e804c5eb (2026-09-08) by docsgen on 2026-09-08. Manual edits will be overwritten on regeneration; change the source, not this page. -->

# u-boot-arduino

Used by [conf/machine/uno-q.conf](../../conf/machine/uno-q.conf), which names `u-boot-arduino`. Pulls in OE-Core's [`u-boot-common.inc`](https://github.com/openembedded/openembedded-core/blob/wrynose/meta/recipes-bsp/u-boot/u-boot-common.inc) and [`u-boot.inc`](https://github.com/openembedded/openembedded-core/blob/wrynose/meta/recipes-bsp/u-boot/u-boot.inc).

A bootloader recipe builds the program that runs before the kernel and hands control to it, and a board's machine configuration names the one that board uses ([recipe](../../docs/glossary.md), [writing a new recipe](https://docs.yoctoproject.org/dev-manual/new-recipe.html)). This one builds U-Boot for the Arduino UNO Q from a pinned Arduino git revision, then wraps the result as an Android-style boot image the Qualcomm flash machinery accepts.

| Field | Detail |
| --- | --- |
| Recipe | [recipes-bsp/u-boot/u-boot-arduino_git.bb](u-boot-arduino_git.bb) |
| Version | `git`, from the filename; `PV` set to `2025.10+2026.01-rc3+git` |
| License | not set here; it comes from the required files listed under Compatibility |

## Configuration variables

| Variable | Effect |
| --- | --- |
| [`DEPENDS`](https://docs.yoctoproject.org/ref-manual/variables.html#term-DEPENDS) `+=` | Build-time dependencies: recipes that must be staged before this one builds. This file adds `bc-native`, `dtc-native`, `gnutls-native`, `python3-pyelftools-native`, `skales-native` and `xxd-native`. Extends the value set by OE-Core's [`u-boot-common.inc`](https://github.com/openembedded/openembedded-core/blob/wrynose/meta/recipes-bsp/u-boot/u-boot-common.inc#L7) and [`u-boot.inc`](https://github.com/openembedded/openembedded-core/blob/wrynose/meta/recipes-bsp/u-boot/u-boot.inc#L6). |
| [`SRC_URI`](https://docs.yoctoproject.org/ref-manual/variables.html#term-SRC_URI) `=` | Source locations the recipe fetches and unpacks. Reassigns the value OE-Core's [`u-boot-common.inc`](https://github.com/openembedded/openembedded-core/blob/wrynose/meta/recipes-bsp/u-boot/u-boot-common.inc#L17) sets. |
| `SRCBRANCH =` | Recipe-local variable substituted into the SCM parameters of `SRC_URI`. This file sets it to `qcom-mainline`. |
| [`SRCREV`](https://docs.yoctoproject.org/ref-manual/variables.html#term-SRCREV) `=` | Source revision fetched for the SCM entry in `SRC_URI`. This file sets it to `8008ca96a4dc53ddb3e51b96ea7e86d881ab7969`. Reassigns the value OE-Core's [`u-boot-common.inc`](https://github.com/openembedded/openembedded-core/blob/wrynose/meta/recipes-bsp/u-boot/u-boot-common.inc#L15) sets. |
| [`PV`](https://docs.yoctoproject.org/ref-manual/variables.html#term-PV) `=` | Package version. Left unset, the version is taken from the recipe filename. This file sets it to `2025.10+2026.01-rc3+git`. |
| [`COMPATIBLE_MACHINE`](https://docs.yoctoproject.org/ref-manual/variables.html#term-COMPATIBLE_MACHINE) `=` | Regular expression limiting the machines this recipe will build for. This file sets the pattern `(uno-q)`, which matches [`uno-q`](../../conf/machine/uno-q.md) in this layer. |
| [`do_compile[depends]`](https://docs.yoctoproject.org/bitbake/bitbake-user-manual/bitbake-user-manual-metadata.html#variable-flags) `+=` | Task-level dependency: the named task of another recipe must complete before this task runs. |

## Packages

| Variable | Effect |
| --- | --- |
| [`PROVIDES`](https://docs.yoctoproject.org/ref-manual/variables.html#term-PROVIDES) `+=` | Additional names this recipe satisfies, so other recipes can depend on it by those names. Adds the `u-boot` provided names. Extends the `virtual/bootloader` set from OE-Core's [`u-boot.inc`](https://github.com/openembedded/openembedded-core/blob/wrynose/meta/recipes-bsp/u-boot/u-boot.inc#L2). |

## Tasks

| Task | Scope | Comment |
| --- | --- | --- |
| `uboot_compile_config:append()` | `append` | |
| `uboot_deploy_config:append:qcom()` | `append`, SoC-family scope `qcom` (an override meta-qcom sets in `conf/machine/include/qcom-common.inc`) | The file notes: "Symlink the 'main' u-boot.bin to boot.img so the qcom image bbclass pick it up". |

## Compatibility

- Machines: [`uno-q`](../../conf/machine/uno-q.md), from `COMPATIBLE_MACHINE = "(uno-q)"`.
- `require recipes-bsp/u-boot/u-boot-common.inc`: this file is not in this layer; BitBake resolves it through `BBPATH` from another layer in the build.
- `require recipes-bsp/u-boot/u-boot.inc`: this file is not in this layer; BitBake resolves it through `BBPATH` from another layer in the build.
- Layer dependencies: `LAYERDEPENDS_qcom-3rdparty = "core qcom"` in [conf/layer.conf](../../conf/layer.conf). This repository pins no revision of those layers; the build supplies them, and `LAYERSERIES_COMPAT_qcom-3rdparty = "wrynose"` records the Yocto release series they must match.
