<!-- Generated from recipes-bsp/firmware-boot/firmware-qcom-boot-qrb2210-arduino-imola_251020.bb at wrynose @ e804c5eb (2026-09-08) by docsgen on 2026-09-08. Manual edits will be overwritten on regeneration; change the source, not this page. -->

# firmware-qcom-boot-qrb2210-arduino-imola

Prebuilt bootloader images for Arduino UNO Q. Used by [conf/machine/uno-q.conf](../../conf/machine/uno-q.conf) and [dynamic-layers/qcom-distro/recipes-products/images/qcom-multimedia-image.bbappend](../../dynamic-layers/qcom-distro/recipes-products/images/qcom-multimedia-image.bbappend), which name `firmware-qcom-boot-qrb2210-arduino-imola`. Pulls in meta-qcom's [`firmware-qcom-boot-common.inc`](https://github.com/qualcomm-linux/meta-qcom/blob/wrynose/recipes-bsp/firmware-boot/firmware-qcom-boot-common.inc).

| Field | Detail |
| --- | --- |
| Recipe | [recipes-bsp/firmware-boot/firmware-qcom-boot-qrb2210-arduino-imola_251020.bb](firmware-qcom-boot-qrb2210-arduino-imola_251020.bb) |
| Version | `251020`, from the filename |
| License | `LICENSE.qcom`; `LIC_FILES_CHKSUM` points at `LICENSE`, `LICENSE` is not present in this layer, so the license text is verified against the fetched source |

## Configuration variables

| Variable | Effect |
| --- | --- |
| [`LIC_FILES_CHKSUM`](https://docs.yoctoproject.org/ref-manual/variables.html#term-LIC_FILES_CHKSUM) `=` | License files and their checksums. The build fails if the license text in the fetched source changes. |
| [`SRC_URI`](https://docs.yoctoproject.org/ref-manual/variables.html#term-SRC_URI) `=` | Source locations the recipe fetches and unpacks. |
| [`SRC_URI[sha256sum]`](https://docs.yoctoproject.org/ref-manual/variables.html#term-SRC_URI) `=` | SHA-256 checksum the fetcher verifies the downloaded archive against. |
| `BOOTBINARIES =` | Names the vendor archive fetched by `SRC_URI` and the directory it unpacks into, which the recipe builds from. This file sets it to `unoq-bootloader-emmc-linux-251020`. |
| `QCOM_BOOT_IMG_SUBDIR =` | Names the subdirectory of the deploy directory this recipe installs its boot binaries into; the machine's `QCOM_BOOT_FILES_SUBDIR` has to name the same directory for the flash package to find them. This file sets it to `qrb2210-arduino-imola`. |
| [`COMPATIBLE_MACHINE`](https://docs.yoctoproject.org/ref-manual/variables.html#term-COMPATIBLE_MACHINE) `=` | Regular expression limiting the machines this recipe will build for. This file sets the pattern `(uno-q)`, which matches [`uno-q`](../../conf/machine/uno-q.md) in this layer. |

## Tasks

No tasks are defined here; they come from the required files listed under Compatibility, which are not part of this layer.

## Compatibility

- Machines: [`uno-q`](../../conf/machine/uno-q.md), from `COMPATIBLE_MACHINE = "(uno-q)"`.
- `include recipes-bsp/firmware-boot/firmware-qcom-boot-common.inc`: this file is not in this layer; BitBake resolves it through `BBPATH` from another layer in the build.
- Layer dependencies: `LAYERDEPENDS_qcom-3rdparty = "core qcom"` in [conf/layer.conf](../../conf/layer.conf). This repository pins no revision of those layers; the build supplies them, and `LAYERSERIES_COMPAT_qcom-3rdparty = "wrynose"` records the Yocto release series they must match.
