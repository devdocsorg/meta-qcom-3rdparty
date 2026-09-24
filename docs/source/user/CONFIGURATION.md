# Configuration reference

The layer's behaviour comes from BitBake metadata: the layer configuration, one
machine configuration per board, kas fragments that compose builds, recipes and
appends, and the CI workflows. The values shown are this layer's own and serve as
safe examples. The build helpers' environment variables are documented in
[.env.example](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/.env.example).

## Loading and precedence

kas loads each fragment's `includes` first, then the fragments named on the
command line from left to right; later values replace earlier ones
([kas project configuration](https://kas.readthedocs.io/en/4.8.2/userguide/project-configuration.html)).
kas writes `local_conf_header` entries to `local.conf`. BitBake reads every
`conf/layer.conf`, then `local.conf`, then the machine configuration named by
`MACHINE`. A machine setting assigned with `?=` or `??=` is a default that
`local.conf` can replace; one assigned with `=` cannot
([BitBake assignment operators](https://docs.yoctoproject.org/bitbake/2.16/bitbake-user-manual/bitbake-user-manual-metadata.html#basic-syntax)).
A suffix such as `:rubikpi3` limits a line to that machine. Linked variable
names lead to their [Yocto Project 6.0 glossary](https://docs.yoctoproject.org/6.0/ref-manual/variables.html)
entries or to their [meta-qcom](https://github.com/qualcomm-linux/meta-qcom) definitions.

## Layer

[conf/layer.conf](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/conf/layer.conf)
registers the layer. Its settings are required unless marked optional.

| Setting | Purpose | Type | Value |
| --- | --- | --- | --- |
| [BBPATH](https://docs.yoctoproject.org/6.0/ref-manual/variables.html#term-BBPATH) | Lets BitBake find this layer's `conf/` files. | Colon-separated paths | Appends `${LAYERDIR}` |
| [BBFILES](https://docs.yoctoproject.org/6.0/ref-manual/variables.html#term-BBFILES) | Adds the recipes and appends. | Space-separated globs | `recipes-*/*/*.bb` and `*.bbappend` |
| [BBFILE_COLLECTIONS](https://docs.yoctoproject.org/6.0/ref-manual/variables.html#term-BBFILE_COLLECTIONS) | Names the layer for the settings below. | String | `qcom-3rdparty` |
| [BBFILE_PATTERN](https://docs.yoctoproject.org/6.0/ref-manual/variables.html#term-BBFILE_PATTERN) | Matches files that belong to the layer. | Regular expression | `^${LAYERDIR}/` |
| [BBFILE_PRIORITY](https://docs.yoctoproject.org/6.0/ref-manual/variables.html#term-BBFILE_PRIORITY) | Chooses between recipes of the same name; higher wins. | Integer | `5` |
| [LAYERDEPENDS](https://docs.yoctoproject.org/6.0/ref-manual/variables.html#term-LAYERDEPENDS) | Requires [OpenEmbedded-Core](https://github.com/openembedded/openembedded-core) (`core`) and [meta-qcom](https://github.com/qualcomm-linux/meta-qcom) (`qcom`). | Space-separated collections | `core qcom` |
| [LAYERSERIES_COMPAT](https://docs.yoctoproject.org/6.0/ref-manual/variables.html#term-LAYERSERIES_COMPAT) | Declares the compatible Yocto Project series; others fail the layer check. | Space-separated series | `wrynose` |
| [BBFILES_DYNAMIC](https://docs.yoctoproject.org/6.0/ref-manual/variables.html#term-BBFILES_DYNAMIC) | Optional. Loads `dynamic-layers/qcom-distro/` only when [meta-qcom-distro](https://github.com/qualcomm-linux/meta-qcom-distro) is present. | `collection:glob` list | `qcom-distro:` recipes and appends |

## Machines

Each file in [conf/machine/](https://github.com/devdocsorg/meta-qcom-3rdparty/tree/docs/layer-documentation/conf/machine)
describes one board, starts with `#@TYPE`, `#@NAME`, and `#@DESCRIPTION`
comments that name it, and requires the QCS6490 SoC include from [meta-qcom](https://github.com/qualcomm-linux/meta-qcom),
[qcom-qcs6490.inc](https://github.com/qualcomm-linux/meta-qcom/blob/1d8048f3a515eeef3758868566ec847b63065811/conf/machine/include/qcom-qcs6490.inc),
which supplies the defaults below. A blank value (`""`) turns a feature off.

| Setting | Purpose | Type | Default when unset | `rubikpi3` | `radxa-dragon-q6a` |
| --- | --- | --- | --- | --- | --- |
| [PREFERRED_PROVIDER_virtual/kernel](https://docs.yoctoproject.org/6.0/ref-manual/variables.html#term-PREFERRED_PROVIDER) | Kernel recipe. `rubikpi3` sets it before the SoC include so that its value is the one used. | Recipe name | `linux-qcom-next` | `?= "linux-qcom-next"` | `?= "linux-qcom-next"`, after the include, repeating the default |
| [MACHINE_FEATURES](https://docs.yoctoproject.org/6.0/ref-manual/variables.html#term-MACHINE_FEATURES) | Hardware features added to the SoC set. | Space-separated features | `alsa bluetooth usbgadget usbhost wifi` | `+= "efi pci"` | `+= "efi pci"` |
| [KERNEL_DEVICETREE](https://docs.yoctoproject.org/6.0/ref-manual/variables.html#term-KERNEL_DEVICETREE) | Device tree built with the kernel. | Path under `arch/arm64/boot/dts` | Empty | `qcom/qcs6490-thundercomm-rubikpi3.dtb` | `qcom/qcs6490-radxa-dragon-q6a.dtb` |
| [QCOM_DTB_DEFAULT](https://github.com/qualcomm-linux/meta-qcom/blob/1d8048f3a515eeef3758868566ec847b63065811/conf/machine/include/qcom-common.inc) | Device tree packaged as the default boot DTB. | DTB name without `.dtb` | `multi-dtb` | `?= "qcs6490-thundercomm-rubikpi3"` | `?= "qcs6490-radxa-dragon-q6a"` |
| [KERNEL_CMDLINE_EXTRA](https://github.com/qualcomm-linux/meta-qcom/blob/1d8048f3a515eeef3758868566ec847b63065811/recipes-kernel/images/esp-qcom-image.bb) | Extra kernel arguments. `rubikpi3` waits 30 s for deferred probes so the HDMI bridge can appear. | Space-separated arguments | Empty | `:append = " deferred_probe_timeout=30"` | Not set |
| [QCOM_BOOT_FIRMWARE](https://github.com/qualcomm-linux/meta-qcom/blob/1d8048f3a515eeef3758868566ec847b63065811/classes-recipe/image_types_qcom.bbclass) | Recipe deploying boot firmware into the flash package. | Recipe name | Empty: none | `firmware-qcom-boot-rubikpi3` | `""`: Radxa flashes firmware to SPI NOR separately |
| [QCOM_BOOT_FILES_SUBDIR](https://github.com/qualcomm-linux/meta-qcom/blob/1d8048f3a515eeef3758868566ec847b63065811/classes-recipe/image_types_qcom.bbclass) | Deploy subdirectory holding the boot firmware. | Directory name | Empty | `rubikpi3` | `""` |
| [QCOM_PARTITION_FILES_SUBDIR](https://github.com/qualcomm-linux/meta-qcom/blob/1d8048f3a515eeef3758868566ec847b63065811/classes-recipe/image_types_qcom.bbclass) | Partition layout from [qcom-ptool](https://github.com/qualcomm-linux/qcom-ptool), via `qcom-partition-conf`. | Deploy-relative path | `QCOM_BOOT_FILES_SUBDIR` | `?= "partitions/qcs6490-thundercomm-rubikpi3/ufs"` | `""` |
| [QCOM_PARTITION_FILES_SUBDIR_SPINOR, QCOM_PARTITION_CONF](https://github.com/qualcomm-linux/meta-qcom/blob/1d8048f3a515eeef3758868566ec847b63065811/classes-recipe/image_types_qcom.bbclass) | SPI NOR partition layout and the recipe that deploys partition files. | Path; recipe name | Empty; `qcom-partition-conf` | Not set | `""`, `""` |
| [QCOM_CDT_FILE](https://github.com/qualcomm-linux/meta-qcom/blob/1d8048f3a515eeef3758868566ec847b63065811/classes-recipe/image_types_qcom.bbclass) | Board CDT packaged as `cdt.bin`. | File name without `.bin` | Empty | `RubikPi3_CDT` | `""` |
| [MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS](https://docs.yoctoproject.org/6.0/ref-manual/variables.html#term-MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS) | Boot-essential packages: the two SoC packagegroups from the SoC include, repeated here, plus the board packagegroups. | Space-separated packages | The SoC packagegroups | Adds `packagegroup-rubikpi3-firmware` | Adds `packagegroup-radxa-dragon-q6a-firmware`, `-hexagon-dsp-binaries`, and `qairt-sdk-hexagon-v68` |

`radxa-dragon-q6a` boots from the Radxa UEFI firmware in SPI NOR and builds only
the OS disk, so it also sets:

| Setting | Purpose | Type | Default when unset | Value |
| --- | --- | --- | --- | --- |
| [WKS_FILE](https://docs.yoctoproject.org/6.0/ref-manual/variables.html#term-WKS_FILE) | Disk layout: an ESP with systemd-boot and a unified kernel image, then the root file system. | Kickstart file name | `${IMAGE_BASENAME}.${MACHINE}.wks` | `efi-uki-bootdisk.wks.in` |
| [QCOM_ESP_IMAGE](https://github.com/qualcomm-linux/meta-qcom/blob/1d8048f3a515eeef3758868566ec847b63065811/classes-recipe/image_types_qcom.bbclass) | Separate ESP image; the kickstart creates the ESP instead. | Recipe name | `esp-qcom-image` with the `efi` feature | `""` |
| [QCOM_VFAT_SECTOR_SIZE](https://github.com/qualcomm-linux/meta-qcom/blob/1d8048f3a515eeef3758868566ec847b63065811/conf/machine/include/qcom-common.inc) | Sector size of the generated FAT images: `512` for SD cards, `4096` for UFS. | Integer (bytes) | `4096` | `?= "512"` |
| [QCOM_BOOTIMG_ROOTFS](https://github.com/qualcomm-linux/meta-qcom/blob/1d8048f3a515eeef3758868566ec847b63065811/conf/machine/include/qcom-base.inc) | Root device on the kernel command line. | `root=` value | `PARTLABEL=rootfs` | `?= "PARTLABEL=root"` |
| [IMAGE_FSTYPES](https://docs.yoctoproject.org/6.0/ref-manual/variables.html#term-IMAGE_FSTYPES) | Adds the disk image, its compressed copy, and its block map. | Space-separated types | `ext4` and `qcomflash` from the SoC include | `+= "wic wic.gz wic.bmap"` |
| [PREFERRED_PROVIDER_virtual/bootloader](https://docs.yoctoproject.org/6.0/ref-manual/variables.html#term-PREFERRED_PROVIDER) | Deliberately unset: no U-Boot is built. | Recipe name | None | Not set |

## kas fragments

The files in [ci/](https://github.com/devdocsorg/meta-qcom-3rdparty/tree/docs/layer-documentation/ci)
use kas configuration format `version: 14` and compose a build as
`ci/<machine>.yml[:<fragment>.yml]`.

| File | Settings | Purpose |
| --- | --- | --- |
| `base.yml` | Includes [meta-qcom](https://github.com/qualcomm-linux/meta-qcom)'s `ci/base.yml`; `repos` pins `meta-qcom` to branch `master` and adds this checkout. | Common layers, `nodistro`, and the `core-image-base` target. |
| `rubikpi3.yml`, `radxa-dragon-q6a.yml` | Include `base.yml`; `machine` names the board. | One board build. |
| `meta-qcom.yml` | `repos` pins `meta-qcom` to `master`. | Lets the fragments below include [meta-qcom](https://github.com/qualcomm-linux/meta-qcom)'s files. |
| `qcom-distro.yml` | Includes `meta-qcom.yml` and [meta-qcom](https://github.com/qualcomm-linux/meta-qcom)'s `ci/qcom-distro.yml`. | Qualcomm Linux distribution and images. |
| `ci.yml`, `mirror.yml` | Include `meta-qcom.yml` and [meta-qcom](https://github.com/qualcomm-linux/meta-qcom)'s `ci/ci.yml` or `ci/mirror.yml`. | CI build settings and the Yocto Project shared-state mirror. |
| `linux-qcom-next.yml` | `local_conf_header` sets `PREFERRED_PROVIDER_virtual/kernel = "linux-qcom-next"`. | Forces the kernel provider. |
| `world.yml` | `local_conf_header` sets [EXCLUDE_FROM_WORLD](https://docs.yoctoproject.org/6.0/ref-manual/variables.html#term-EXCLUDE_FROM_WORLD) `= "1"`, then `"0"` for `layer-qcom` and `layer-qcom-3rdparty`; `target` is `world`. | Builds every recipe of [meta-qcom](https://github.com/qualcomm-linux/meta-qcom) and this layer. |

## Recipes and appends

| File | Settings | Purpose |
| --- | --- | --- |
| [firmware-qcom-boot-rubikpi3_20260621.bb](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/recipes-bsp/firmware-boot/firmware-qcom-boot-rubikpi3_20260621.bb) | [SRC_URI](https://docs.yoctoproject.org/6.0/ref-manual/variables.html#term-SRC_URI) and [SRCREV](https://docs.yoctoproject.org/6.0/ref-manual/variables.html#term-SRCREV) pin [rubikpi-ai/boot-assets](https://github.com/rubikpi-ai/boot-assets); `LICENSE` and `LIC_FILES_CHKSUM` identify its licence; `INHIBIT_DEFAULT_DEPS = "1"` and `noexec` configure and compile steps skip the toolchain; `QCOM_BOOT_IMG_SUBDIR = "rubikpi3"` is the deploy subdirectory; [COMPATIBLE_MACHINE](https://docs.yoctoproject.org/6.0/ref-manual/variables.html#term-COMPATIBLE_MACHINE) `= "(rubikpi3)"`. | Deploys the board's boot firmware and CDT. |
| [packagegroup-rubikpi3.bb](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/recipes-bsp/packagegroups/packagegroup-rubikpi3.bb), [packagegroup-radxa-dragon-q6a.bb](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/recipes-bsp/packagegroups/packagegroup-radxa-dragon-q6a.bb) | [PACKAGES](https://docs.yoctoproject.org/6.0/ref-manual/variables.html#term-PACKAGES) defines `${PN}-firmware`, and for Radxa `${PN}-hexagon-dsp-binaries`; `RRECOMMENDS` lists firmware, adding the Adreno GPU firmware only when `DISTRO_FEATURES` has `opencl`, `opengl`, or `vulkan`; Radxa's `RDEPENDS` pulls the ADSP and CDSP binaries. | Board firmware sets. RUBIK Pi 3 Wi-Fi and Bluetooth firmware is omitted until upstream [linux-firmware](https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/) has it. |
| [linux-qcom-next_git.bbappend](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/recipes-kernel/linux/linux-qcom-next_git.bbappend) | [FILESEXTRAPATHS](https://docs.yoctoproject.org/6.0/ref-manual/variables.html#term-FILESEXTRAPATHS) prepends `${THISDIR}/${BPN}`, a directory this layer does not have, and for Radxa `${THISDIR}/radxa-dragon-q6a`; `SRC_URI:append:radxa-dragon-q6a` adds `realtek-eth-8169.cfg`. | Radxa-only kernel options. |
| [realtek-eth-8169.cfg](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/recipes-kernel/linux/radxa-dragon-q6a/realtek-eth-8169.cfg) | Built-in (`=y`): `R8169` and `REALTEK_PHY` drivers, their `PHYLIB`, `MDIO_BUS`, `FWNODE_MDIO`, `OF_MDIO`, `ACPI_MDIO`, and `FIXED_PHY` support, and `NET_SELFTESTS`; `REALTEK_PHY_HWMON` is left unset. | Kernel configuration fragment for the Radxa Ethernet controller; use `=m` to build a driver as a module. |
| [qcom-multimedia-image.bbappend](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/dynamic-layers/qcom-distro/recipes-products/images/qcom-multimedia-image.bbappend) | [INCOMPATIBLE_LICENSE_EXCEPTIONS](https://docs.yoctoproject.org/6.0/ref-manual/variables.html#term-INCOMPATIBLE_LICENSE_EXCEPTIONS)`:append:rubikpi3` allows `firmware-qcom-boot-rubikpi3:LicenseRef-LICENSE.qcom-2`. | Lets the Qualcomm Linux multimedia image ship the RUBIK Pi 3 boot firmware. |

## CI workflows

Each file in [.github/workflows/](https://github.com/devdocsorg/meta-qcom-3rdparty/tree/docs/layer-documentation/.github/workflows):

- `pr.yml` — Pull requests to `main`, except Markdown-only changes: runs `build-yocto.yml`.
- `push.yml` — Pushes to `main`: runs `build-yocto.yml`.
- `nightly-build.yml` — Daily or on demand: runs `build-yocto.yml`, skipping inputs that already built.
- `nightly-build-wrynose.yml` — Daily: starts `nightly-build.yml` on `wrynose`.
- `build-yocto.yml` — Called by the three above: runs `yocto-patchreview` and `yocto-check-layer` and, in parallel, builds each machine with `nodistro` and `qcom-distro` through [meta-qcom](https://github.com/qualcomm-linux/meta-qcom)'s compile workflow.
- `bitbake-lint.yml` — Pull requests changing recipes or configuration: reports oelint-adv findings without failing.
- `markdownlint.yml` — Pull requests and `main` pushes changing Markdown: lints with [.markdownlint.yaml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/.github/.markdownlint.yaml).
- `documentation.yml` — Pull requests and `main` pushes: runs the documentation `check` from [DEVELOPMENT.md](../contributing/DEVELOPMENT.md).
- `qcom-preflight-checks.yml` — Pull requests, `main` pushes, or on demand: runs Qualcomm's repolinter check.
- `backport.yml` — A merged `main` pull request labelled `backport wrynose`: opens the backport pull request.
- `test-pr.yml`, `test.yml`, `test-distro.yml`, `publish-results.yml` — LAVA boot tests after a pull request build; disabled until a machine has a lab device.
- `stales.yml` — Daily: marks inactive issues and pull requests stale.
