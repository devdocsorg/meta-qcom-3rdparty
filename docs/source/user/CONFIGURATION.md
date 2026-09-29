# Configuration reference

This page documents the settings this layer maintains. Standard BitBake and
Yocto Project variables are defined in the
[variables glossary](https://docs.yoctoproject.org/6.0/ref-manual/variables.html), and kas keys in the
[kas project configuration](https://kas.readthedocs.io/en/latest/userguide/project-configuration.html) reference; the tables below record this
layer's choices.

BitBake reads `conf/layer.conf` when the layer is added to `bblayers.conf`, and
the machine file named by `MACHINE`, together with each recipe's appends, when it
builds. `?=` sets a default only when nothing earlier assigned the variable, `??=`
is a weaker default that any other assignment replaces, and `:append` and `+=`
add to the value. A setting in `local.conf` or a kas `local_conf_header` replaces a
machine default. The `conf/layer.conf` settings are required for BitBake to load
the layer. A new machine needs the key elements that the
[machine example](../contributing/CONTRIBUTING.md#61--machine-configuration)
lists; the other settings are optional choices with the effects described below.
Every kas file needs `header: version`, and a kas build needs a `machine`.

## Environment settings

[.env.example](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/.env.example) documents the optional `KAS_CONTAINER`,
`KAS_WORK_DIR`, `DL_DIR`, and `SSTATE_DIR` settings, with safe values. kas reads
them from the shell environment; see kas's
[environment variables](https://kas.readthedocs.io/en/latest/userguide/env-vars.html).

## Layer configuration

[conf/layer.conf](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/conf/layer.conf) registers the layer.

| Setting | Value and purpose |
| --- | --- |
| [BBPATH](https://docs.yoctoproject.org/6.0/ref-manual/variables.html#term-BBPATH) | Appends the layer directory, so BitBake finds its `conf/` files. |
| [BBFILES](https://docs.yoctoproject.org/6.0/ref-manual/variables.html#term-BBFILES) | Adds `recipes-*/*/*.bb` and `.bbappend`. |
| [BBFILE_COLLECTIONS](https://docs.yoctoproject.org/6.0/ref-manual/variables.html#term-BBFILE_COLLECTIONS), [BBFILE_PATTERN](https://docs.yoctoproject.org/6.0/ref-manual/variables.html#term-BBFILE_PATTERN) | Names the collection `qcom-3rdparty` and assigns it every file under the layer. |
| [BBFILE_PRIORITY](https://docs.yoctoproject.org/6.0/ref-manual/variables.html#term-BBFILE_PRIORITY) | `5`; when several layers provide the same recipe, the highest priority wins regardless of version. |
| [LAYERDEPENDS](https://docs.yoctoproject.org/6.0/ref-manual/variables.html#term-LAYERDEPENDS) | `core qcom`: [OpenEmbedded-Core](https://github.com/openembedded/openembedded-core) and [meta-qcom](https://github.com/qualcomm-linux/meta-qcom) must be in the build. |
| [LAYERSERIES_COMPAT](https://docs.yoctoproject.org/6.0/ref-manual/variables.html#term-LAYERSERIES_COMPAT) | `wrynose`; BitBake stops when the [OpenEmbedded-Core](https://github.com/openembedded/openembedded-core) layer in the build belongs to another release series. |
| [BBFILES_DYNAMIC](https://docs.yoctoproject.org/6.0/ref-manual/variables.html#term-BBFILES_DYNAMIC) | Reads `dynamic-layers/qcom-distro/*/*/*.bb` and `.bbappend` only when the `qcom-distro` collection is present. |

## Machine configurations

Both machines require [meta-qcom](https://github.com/qualcomm-linux/meta-qcom)'s `conf/machine/include/qcom-qcs6490.inc`, which
supplies the QCS6490 defaults: the `linux-qcom-next` kernel, the `ext4` and
`qcomflash` image types, a 4096-byte VFAT sector size, and the SoC packagegroups.
The `#@TYPE`, `#@NAME`, and `#@DESCRIPTION` comments name the board.

### rubikpi3

[conf/machine/rubikpi3.conf](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/conf/machine/rubikpi3.conf) builds a flashable
`qcomflash` package with boot firmware from the vendor.

| Setting | Value and purpose |
| --- | --- |
| [PREFERRED_PROVIDER](https://docs.yoctoproject.org/6.0/ref-manual/variables.html#term-PREFERRED_PROVIDER)`_virtual/kernel` | `?= "linux-qcom-next"`, set before the SoC include so it takes precedence. |
| [MACHINE_FEATURES](https://docs.yoctoproject.org/6.0/ref-manual/variables.html#term-MACHINE_FEATURES) | Adds `efi pci` to the SoC defaults. |
| `KERNEL_CMDLINE_EXTRA:append` | Adds `deferred_probe_timeout=30`, so the HDMI bridge can probe before the display driver gives up. |
| [KERNEL_DEVICETREE](https://docs.yoctoproject.org/6.0/ref-manual/variables.html#term-KERNEL_DEVICETREE) | `qcom/qcs6490-thundercomm-rubikpi3.dtb`, built by the kernel. |
| `QCOM_DTB_DEFAULT` | `?= "qcs6490-thundercomm-rubikpi3"`: the device tree packaged for the boot firmware; unset, [meta-qcom](https://github.com/qualcomm-linux/meta-qcom) uses a multi-DTB image. |
| `QCOM_BOOT_FIRMWARE`, `QCOM_BOOT_FILES_SUBDIR` | `firmware-qcom-boot-rubikpi3` and `rubikpi3`: the recipe that deploys the boot binaries, and their deploy subfolder. |
| `QCOM_PARTITION_FILES_SUBDIR` | `?= "partitions/qcs6490-thundercomm-rubikpi3/ufs"`: the UFS partition layout from [qcom-ptool](https://github.com/qualcomm-linux/qcom-ptool), through [meta-qcom](https://github.com/qualcomm-linux/meta-qcom)'s `qcom-partition-conf`. |
| `QCOM_CDT_FILE` | `RubikPi3_CDT`: the board's CDT, packaged as `cdt.bin`. |
| [MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS](https://docs.yoctoproject.org/6.0/ref-manual/variables.html#term-MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS) | `packagegroup-qcom-boot-essential` and `packagegroup-machine-essential-qcom-qcs6490-soc`, which the SoC include already adds, and `packagegroup-rubikpi3-firmware`. |

### radxa-dragon-q6a

[conf/machine/radxa-dragon-q6a.conf](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/conf/machine/radxa-dragon-q6a.conf)
builds only the OS disk: an EFI system partition with systemd-boot and a unified
kernel image, plus the root filesystem. Radxa's EDK2 firmware in SPI NOR is
flashed separately, so the file leaves `PREFERRED_PROVIDER_virtual/bootloader`
unset.

| Setting | Value and purpose |
| --- | --- |
| `MACHINE_FEATURES` | Adds `efi pci`. |
| `KERNEL_DEVICETREE` | `qcom/qcs6490-radxa-dragon-q6a.dtb`. |
| `PREFERRED_PROVIDER_virtual/kernel` | `?= "linux-qcom-next"`, the same kernel the SoC include already selects. |
| `QCOM_BOOT_FIRMWARE`, `QCOM_BOOT_FILES_SUBDIR`, `QCOM_PARTITION_FILES_SUBDIR`, `QCOM_PARTITION_FILES_SUBDIR_SPINOR`, `QCOM_PARTITION_CONF`, `QCOM_CDT_FILE` | Empty, so the `qcomflash` package holds no Qualcomm boot firmware, partition tables, or CDT. |
| [WKS_FILE](https://docs.yoctoproject.org/6.0/ref-manual/variables.html#term-WKS_FILE), `QCOM_ESP_IMAGE` | `efi-uki-bootdisk.wks.in` creates the EFI system partition inside the disk image, so the separate ESP image is disabled with an empty value. |
| `QCOM_VFAT_SECTOR_SIZE` | `?= "512"` for SD cards; set `4096` for UFS. |
| `QCOM_BOOTIMG_ROOTFS` | `?= "PARTLABEL=root"` has no effect: the SoC include sets `PARTLABEL=rootfs` first. |
| `QCOM_DTB_DEFAULT` | `?= "qcs6490-radxa-dragon-q6a"`. |
| [IMAGE_FSTYPES](https://docs.yoctoproject.org/6.0/ref-manual/variables.html#term-IMAGE_FSTYPES) | Adds `wic wic.gz wic.bmap`: the disk image, its compressed copy, and a block map for `bmaptool`. |
| `MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS` | The two SoC packagegroups, `packagegroup-radxa-dragon-q6a-firmware`, `packagegroup-radxa-dragon-q6a-hexagon-dsp-binaries`, and `qairt-sdk-hexagon-v68`, the Qualcomm AI Runtime's Hexagon v68 libraries. |

## Recipes and appends

| File | Local choices |
| --- | --- |
| [firmware-qcom-boot-rubikpi3_20260621.bb](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/recipes-bsp/firmware-boot/firmware-qcom-boot-rubikpi3_20260621.bb) | Fetches [rubikpi-ai/boot-assets](https://github.com/rubikpi-ai/boot-assets) at a pinned `SRCREV` under `LicenseRef-LICENSE.qcom-2`; skips the default dependencies and the configure and compile tasks; builds only for `rubikpi3`; deploys to `QCOM_BOOT_IMG_SUBDIR = "rubikpi3"`. |
| [packagegroup-rubikpi3.bb](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/recipes-bsp/packagegroups/packagegroup-rubikpi3.bb) | One `-firmware` package recommending the QUP, video, audio, and compute firmware, plus the Adreno GPU firmware when `DISTRO_FEATURES` has `opencl`, `opengl`, or `vulkan`. Wi-Fi and Bluetooth firmware are omitted until upstream [linux-firmware](https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/) ships them. |
| [packagegroup-radxa-dragon-q6a.bb](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/recipes-bsp/packagegroups/packagegroup-radxa-dragon-q6a.bb) | A `-firmware` package with the same GPU condition plus camera, HDMI bridge, audio, compute, QUP, and video firmware, and a `-hexagon-dsp-binaries` package that requires the ADSP and CDSP binaries. |
| [linux-qcom-next_git.bbappend](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/recipes-kernel/linux/linux-qcom-next_git.bbappend) | Adds `linux-qcom-next/` beside the append to the file search path for every machine; that folder does not exist yet. For `radxa-dragon-q6a` only, adds `radxa-dragon-q6a/realtek-eth-8169.cfg` to `SRC_URI`. |
| [realtek-eth-8169.cfg](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/recipes-kernel/linux/radxa-dragon-q6a/realtek-eth-8169.cfg) | Builds in the RTL8169 Ethernet driver (`CONFIG_R8169`) and what it needs: `NET_SELFTESTS`, `MDIO_BUS`, `PHYLIB`, `FIXED_PHY`, `REALTEK_PHY`, `FWNODE_MDIO`, `OF_MDIO`, and `ACPI_MDIO`, all `=y`; `REALTEK_PHY_HWMON` stays unset. See the [kernel configuration fragments](https://docs.yoctoproject.org/6.0/kernel-dev/common.html#creating-configuration-fragments) guide. |
| [qcom-multimedia-image.bbappend](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/dynamic-layers/qcom-distro/recipes-products/images/qcom-multimedia-image.bbappend) | For `rubikpi3`, adds an [INCOMPATIBLE_LICENSE_EXCEPTIONS](https://docs.yoctoproject.org/6.0/ref-manual/variables.html#term-INCOMPATIBLE_LICENSE_EXCEPTIONS) entry so the image may ship `firmware-qcom-boot-rubikpi3` under `LicenseRef-LICENSE.qcom-2`. |

## kas files

The CI builds combine these files with `:`, for example
`ci/rubikpi3.yml:ci/qcom-distro.yml`. Every file declares `header: version: 14`,
and most start with a comment that points editors to the kas schema.

| File | Local choices |
| --- | --- |
| [base.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/ci/base.yml) | Includes [meta-qcom](https://github.com/qualcomm-linux/meta-qcom)'s `ci/base.yml`, which sets `nodistro`, the `core-image-base` target, [OpenEmbedded-Core](https://github.com/openembedded/openembedded-core), and [BitBake](https://github.com/openembedded/bitbake); fetches [meta-qcom](https://github.com/qualcomm-linux/meta-qcom) from its `master` branch and adds this checkout (`meta-qcom-3rdparty:` with no URL). |
| [rubikpi3.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/ci/rubikpi3.yml), [radxa-dragon-q6a.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/ci/radxa-dragon-q6a.yml) | Include `ci/base.yml` and set `machine`. |
| [meta-qcom.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/ci/meta-qcom.yml) | Declares [meta-qcom](https://github.com/qualcomm-linux/meta-qcom) at `master`, so fragments can include its files. |
| [qcom-distro.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/ci/qcom-distro.yml), [ci.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/ci/ci.yml), [mirror.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/ci/mirror.yml) | Include `meta-qcom.yml` and [meta-qcom](https://github.com/qualcomm-linux/meta-qcom)'s fragment of the same name: the Qualcomm Linux distribution and its layers, the CI build settings, and the Yocto Project shared-state mirror. |
| [linux-qcom-next.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/ci/linux-qcom-next.yml) | Assigns `PREFERRED_PROVIDER_virtual/kernel = "linux-qcom-next"` in `local.conf`, overriding a machine default. |
| [world.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/ci/world.yml) | Sets [EXCLUDE_FROM_WORLD](https://docs.yoctoproject.org/6.0/ref-manual/variables.html#term-EXCLUDE_FROM_WORLD) to `1` except for [meta-qcom](https://github.com/qualcomm-linux/meta-qcom) and this layer, and targets `world`. |

## Workflows

| Workflow | Trigger and purpose |
| --- | --- |
| [pr.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/.github/workflows/pr.yml) | Pull requests to `main` that change more than Markdown: runs the build workflow. |
| [push.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/.github/workflows/push.yml) | Pushes to `main`: runs the build workflow. |
| [nightly-build.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/.github/workflows/nightly-build.yml), [nightly-build-wrynose.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/.github/workflows/nightly-build-wrynose.yml) | Daily: build `main` and `wrynose`, skipping a build whose inputs already built successfully. |
| [build-yocto.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/.github/workflows/build-yocto.yml) | Called by the three above in the `qualcomm-linux` organisation: locks the kas layers, runs `yocto-patchreview` and `yocto-check-layer`, and builds each machine in the `matrix` with `nodistro` (plus a world build) and `qcom-distro`, through [meta-qcom](https://github.com/qualcomm-linux/meta-qcom)'s `compile.yml`. |
| [bitbake-lint.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/.github/workflows/bitbake-lint.yml) | Pull requests changing BitBake files outside `.github/` and `ci/`: reports lint findings on changed lines without failing. |
| [markdownlint.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/.github/workflows/markdownlint.yml) | Markdown changes: lints every Markdown file with [.markdownlint.yaml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/.github/.markdownlint.yaml). |
| [documentation.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/.github/workflows/documentation.yml) | Pull requests and pushes to `main`: builds and checks this documentation. |
| [qcom-preflight-checks.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/.github/workflows/qcom-preflight-checks.yml) | Pull requests and pushes to `main`: runs Qualcomm's preflight workflow with only the repolinter check enabled. |
| [test-pr.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/.github/workflows/test-pr.yml), [test.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/.github/workflows/test.yml), [test-distro.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/.github/workflows/test-distro.yml), [publish-results.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/.github/workflows/publish-results.yml) | LAVA boot testing after a pull-request build; disabled until a machine has a lab device, which is then listed in `test.yml`. |
| [backport.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/.github/workflows/backport.yml) | Merged pull requests to `main` labelled `backport wrynose`: opens the backport pull request. |
| [stales.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/.github/workflows/stales.yml) | Daily: marks issues and pull requests stale after 30 days without activity and closes stale pull requests 5 days later, except those labelled `bug` or `enhancement`. |

[CODEOWNERS](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/.github/CODEOWNERS) assigns every path to the maintainers.
The documentation build's pins are commented in its
[Makefile](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/docs/source/Makefile) and
[conf.py](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/docs/source/conf.py).
