# Configuration reference

This page documents the settings the layer maintains. The
[BitBake user manual](https://docs.yoctoproject.org/bitbake/bitbake-user-manual/bitbake-user-manual-metadata.html)
defines the assignment operators, and the
[Yocto Project variable glossary](https://docs.yoctoproject.org/ref-manual/variables.html)
and the [kas configuration reference](https://kas.readthedocs.io/en/latest/userguide/project-configuration.html#configuration-reference)
define the standard fields. The tables give this layer's values and choices; each
value shown is also a safe example. Environment settings for kas-container are
documented in
[.env.example](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1007a/.env.example).

## Loading and precedence

kas writes the build configuration from the kas files in `ci/`: each file's
`includes` are merged first, in order, and the including file can override them.
[BitBake](https://github.com/openembedded/bitbake) then reads `conf/layer.conf` because the layer is in the build, and
`conf/machine/<machine>.conf` for the selected machine. In BitBake files, `=` sets
a value, `?=` sets it only if nothing set it earlier, `+=` and `:append` add to
it, and a `:<machine>` suffix limits an assignment to that machine.

## Layer configuration

[conf/layer.conf](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1007a/conf/layer.conf)
registers the layer as the `qcom-3rdparty` collection. All its settings are
required for the layer to work as described, except `BBFILE_PRIORITY` and
`BBFILES_DYNAMIC`.

| Setting | Value | Purpose | Type | When unset |
| --- | --- | --- | --- | --- |
| `BBPATH .=` | `":${LAYERDIR}"` | Lets BitBake find the layer's `conf/` files. | Colon-separated paths | The machine configurations are not found. |
| `BBFILES +=` | `recipes-*/*/*.bb` and `.bbappend` under `${LAYERDIR}` | Adds the recipes and appends two levels below each `recipes-*` folder. | Space-separated globs | The layer's recipes are not parsed. |
| `BBFILE_COLLECTIONS +=` | `"qcom-3rdparty"` | Names the collection that the `BBFILE_*` and `LAYER*` settings use. | Collection names | The layer is not registered. |
| `BBFILE_PATTERN_qcom-3rdparty :=` | `"^${LAYERDIR}/"` | Matches the files that belong to this layer. | Regular expression | BitBake reports an error. |
| `BBFILE_PRIORITY_qcom-3rdparty` | `"5"` | Ranks the layer's recipes when another layer has the same recipe; [meta-qcom](https://github.com/qualcomm-linux/meta-qcom) uses 6. | Integer | BitBake derives a priority from the layer dependencies. |
| `LAYERDEPENDS_qcom-3rdparty` | `"core qcom"` | Requires [OE-Core](https://github.com/openembedded/openembedded-core) and [meta-qcom](https://github.com/qualcomm-linux/meta-qcom). | Collection names | Missing dependencies are not reported. |
| `LAYERSERIES_COMPAT_qcom-3rdparty` | `"blacksail"` | Declares support for Yocto Project 6.1. A core layer that supports none of the listed releases stops the build. | Release codenames | BitBake warns that the layer does not declare compatibility. |
| `BBFILES_DYNAMIC +=` | `qcom-distro:` patterns for `dynamic-layers/qcom-distro/*/*/*.bb` and `.bbappend` | Adds the files under `dynamic-layers/qcom-distro/` only when [meta-qcom-distro](https://github.com/qualcomm-linux/meta-qcom-distro) is in the build. | `collection:pattern` pairs | The dynamic-layer files are ignored. |

## Machine configurations

Each file in
[conf/machine/](https://github.com/devdocsorg/meta-qcom-3rdparty/tree/docs/upgrade-test-1007a/conf/machine)
starts with `#@TYPE`, `#@NAME`, and `#@DESCRIPTION` comments naming the board, then
builds on the QCS6490 SoC configuration from meta-qcom. Defaults come from that
include chain
([qcom-qcs6490.inc](https://github.com/qualcomm-linux/meta-qcom/blob/9e35027ec5d241619a1b1e32b0aaf542a6886645/conf/machine/include/qcom-qcs6490.inc))
and from meta-qcom's
[image_types_qcom.bbclass](https://github.com/qualcomm-linux/meta-qcom/blob/9e35027ec5d241619a1b1e32b0aaf542a6886645/classes-recipe/image_types_qcom.bbclass).
"Not set" means the machine keeps the default.

| Setting | Purpose and type | Default | `rubikpi3` | `radxa-dragon-q6a` |
| --- | --- | --- | --- | --- |
| `PREFERRED_PROVIDER_virtual/kernel ?=` | Kernel recipe (recipe name). Set before the SoC include, because the first `?=` wins. | `linux-qcom-next` | `linux-qcom-next` | `linux-qcom-next` |
| `require` | SoC configuration (include path); required. | None | `conf/machine/include/qcom-qcs6490.inc` | Same |
| `MACHINE_FEATURES +=` | Hardware features (space-separated names). | `alsa bluetooth usbgadget usbhost wifi` | `efi pci` | `efi pci` |
| `KERNEL_CMDLINE_EXTRA:append` | Extra kernel arguments (string). Gives the lt9611 HDMI bridge time to probe before the display driver gives up. | No addition | `" deferred_probe_timeout=30"` | Not set |
| `KERNEL_DEVICETREE` | Device trees the kernel builds (space-separated paths); required. | None | `qcom/qcs6490-thundercomm-rubikpi3.dtb` | `qcom/qcs6490-radxa-dragon-q6a.dtb` |
| `QCOM_DTB_DEFAULT ?=` | Device tree the firmware boots by default (name without `.dtb`). | `multi-dtb` | `qcs6490-thundercomm-rubikpi3` | `qcs6490-radxa-dragon-q6a` |
| `QCOM_BOOT_FIRMWARE` | Recipe that deploys the boot firmware for the `qcomflash` package (recipe name, or empty for none). | Empty | `firmware-qcom-boot-rubikpi3` | `""`: Radxa flashes the SPI NOR firmware separately |
| `QCOM_BOOT_FILES_SUBDIR` | Folder of the deployed boot files (path). | Empty | `rubikpi3` | `""` |
| `QCOM_PARTITION_FILES_SUBDIR` | Partition layout from [qcom-ptool](https://github.com/qualcomm-linux/qcom-ptool) (path; `?=` in `rubikpi3`). | `QCOM_BOOT_FILES_SUBDIR` | `partitions/qcs6490-thundercomm-rubikpi3/ufs` | `""` |
| `QCOM_PARTITION_FILES_SUBDIR_SPINOR` | SPI NOR partition layout (path). | Empty | Not set | `""` |
| `QCOM_PARTITION_CONF` | Recipe that deploys partition tables (recipe name, or empty for none). | `qcom-partition-conf` | Not set | `""` |
| `QCOM_CDT_FILE` | Board CDT file name without `.bin` (string). | None: no CDT is installed | `RubikPi3_CDT` | `""` |
| `WKS_FILE` | Disk layout for the `wic` image (kickstart file name). | `<image>.<machine>.wks` | Not set | `efi-uki-bootdisk.wks.in`: an EFI system partition with systemd-boot and a unified kernel image |
| `QCOM_ESP_IMAGE` | Separate EFI system partition image (recipe name, or empty). | `esp-qcom-image` when `efi` is a machine feature | Not set | `""`, because the `wic` layout creates the partition |
| `QCOM_VFAT_SECTOR_SIZE ?=` | FAT sector size in bytes (integer). | `4096`, suited to UFS | Not set | `512` for SD cards |
| `QCOM_BOOTIMG_ROOTFS ?=` | Root device on the kernel command line (string). | `PARTLABEL=rootfs` | Not set | `PARTLABEL=root`, which has no effect: `qcom-base.inc` sets `PARTLABEL=rootfs` with an earlier `?=` |
| `IMAGE_FSTYPES +=` | Image formats (space-separated types). | `ext4 qcomflash` | Not set | `wic.gz wic.bmap` |
| `MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS +=` | Packages every image recommends (package names). The first two repeat what the SoC include adds. | The SoC include's boot and SoC packagegroups | `packagegroup-qcom-boot-essential`, `packagegroup-machine-essential-qcom-qcs6490-soc`, `packagegroup-rubikpi3-firmware` | The same two, `packagegroup-radxa-dragon-q6a-firmware`, `packagegroup-radxa-dragon-q6a-hexagon-dsp-binaries`, `qairt-sdk-hexagon-v68` |

`radxa-dragon-q6a` leaves `PREFERRED_PROVIDER_virtual/bootloader` unset on
purpose: the board boots the Radxa EDK2 firmware from SPI NOR, not U-Boot.

## Recipe appends and kernel configuration

| File | Setting and value | Purpose |
| --- | --- | --- |
| [linux-qcom-next_git.bbappend](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1007a/recipes-kernel/linux/linux-qcom-next_git.bbappend) | `FILESEXTRAPATHS:prepend:radxa-dragon-q6a := "${THISDIR}/radxa-dragon-q6a:"` | Lets the kernel recipe find this layer's fragment, for `radxa-dragon-q6a` only. |
| Same | `SRC_URI:append:radxa-dragon-q6a = " file://realtek-eth-8169.cfg"` | Merges the Ethernet fragment below into the kernel configuration. |
| [qcom-multimedia-image.bbappend](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1007a/dynamic-layers/qcom-distro/recipes-products/images/qcom-multimedia-image.bbappend) | `INCOMPATIBLE_LICENSE_EXCEPTIONS:append:rubikpi3 = " firmware-qcom-boot-rubikpi3:LICENSE.qcom-2"` | Allows the boot firmware's licence in that meta-qcom-distro image, for `rubikpi3` only. |

[realtek-eth-8169.cfg](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1007a/recipes-kernel/linux/radxa-dragon-q6a/realtek-eth-8169.cfg)
enables the board's Realtek Ethernet. Each line sets a Kconfig symbol: `=y` builds
it into the kernel, and `# CONFIG_... is not set` leaves it disabled. Symbols the
fragment does not name keep the `linux-qcom-next` configuration. Types are from
the kernel revision that
[linux-qcom-next](https://github.com/qualcomm-linux/meta-qcom/blob/9e35027ec5d241619a1b1e32b0aaf542a6886645/recipes-kernel/linux/linux-qcom-next_git.bb)
pins in [kernel](https://github.com/qualcomm-linux/kernel); a symbol without a
prompt takes its value from its defaults, so its line has no effect.

| Symbol | Value | Purpose | Type |
| --- | --- | --- | --- |
| `CONFIG_R8169` | `y` | Realtek 8169/8168/8101/8125 Ethernet driver. | tristate |
| `CONFIG_PHYLIB` | `y` | PHY device support. | tristate |
| `CONFIG_FIXED_PHY` | `y` | Fixed-link PHY emulation. | tristate |
| `CONFIG_REALTEK_PHY` | `y` | Realtek PHY driver. | tristate |
| `CONFIG_REALTEK_PHY_HWMON` | not set | Hardware-monitoring support for Realtek PHYs stays off. | bool |
| `CONFIG_NET_SELFTESTS` | `y` | Network self-tests; follows `PHYLIB`. | tristate without a prompt |
| `CONFIG_FWNODE_MDIO`, `CONFIG_OF_MDIO`, `CONFIG_ACPI_MDIO` | `y` | Firmware-node, device-tree, and ACPI MDIO bus accessors. | tristate without a prompt |
| `CONFIG_MDIO_BUS` | `y` | MDIO bus support in older kernels; that kernel revision does not define it, so the line has no effect. | Not defined |

## kas files

Every file in
[ci/](https://github.com/devdocsorg/meta-qcom-3rdparty/tree/docs/upgrade-test-1007a/ci)
sets `header.version: 14`, the kas configuration format it uses (required). The
fields below are optional; kas defaults to machine `qemux86-64`, distribution
`nodistro`, and target `core-image-minimal`.

| File | Settings | Purpose |
| --- | --- | --- |
| `base.yml` | `includes` meta-qcom's `ci/base.yml`; `repos.meta-qcom` at `https://github.com/qualcomm-linux/meta-qcom`, `branch: master`; `repos.meta-qcom-3rdparty` with no value, which adds this checkout as a layer | Base build: meta-qcom's base fragment supplies OE-Core, BitBake, `nodistro`, and `core-image-base`, with commits pinned by its `base.lock.yml`. |
| `meta-qcom.yml` | `repos.meta-qcom` as in `base.yml` | Declares the meta-qcom repository for the fragments below. |
| `ci.yml` | `includes` `ci/meta-qcom.yml` and meta-qcom's `ci/ci.yml` | Adds meta-qcom's CI build settings. |
| `mirror.yml` | `includes` `ci/meta-qcom.yml` and meta-qcom's `ci/mirror.yml` | Adds meta-qcom's shared-state mirror. |
| `qcom-distro.yml` | `includes` `ci/meta-qcom.yml` and meta-qcom's `ci/qcom-distro.yml` | Switches to `qcom-distro` and adds its layers. |
| `linux-qcom-next.yml` | `local_conf_header.kernelprovider`: `PREFERRED_PROVIDER_virtual/kernel = "linux-qcom-next"` | Forces the `linux-qcom-next` kernel, overriding a machine's `?=` choice. |
| `rubikpi3.yml`, `radxa-dragon-q6a.yml` | `includes` `ci/base.yml`; `machine: rubikpi3` or `radxa-dragon-q6a` | Selects a board on top of the base build. |
| `world.yml` | `local_conf_header.world_build`: `EXCLUDE_FROM_WORLD = "1"`, then `"0"` for `layer-qcom` and `layer-qcom-3rdparty`; `target: world` | Limits world builds to the recipes of meta-qcom and this layer, plus what they depend on. |

## CI workflows

Each workflow in
[.github/workflows/](https://github.com/devdocsorg/meta-qcom-3rdparty/tree/docs/upgrade-test-1007a/.github/workflows)
is listed with its triggers and what it does. The jobs in `build-yocto.yml` run
only in the `qualcomm-linux` organisation.

- [backport.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1007a/.github/workflows/backport.yml): a pull request merged into `main`; opens a backport pull request for each `backport wrynose` label.
- [bitbake-lint.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1007a/.github/workflows/bitbake-lint.yml): a pull request that changes BitBake files outside `.github/` and `ci/`; lints the changed lines with [bitbake-lint-action](https://github.com/qualcomm-linux/bitbake-lint-action) without failing the pull request.
- [build-yocto.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1007a/.github/workflows/build-yocto.yml): called by the build workflows; runs `yocto-patchreview` and `yocto-check-layer`, and builds both machines with `nodistro` and `qcom-distro` through meta-qcom's compile workflow.
- [markdownlint.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1007a/.github/workflows/markdownlint.yml): a push to `main` or a pull request that changes Markdown; lints it with the rules in `.github/.markdownlint.yaml`.
- [nightly-build-wrynose.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1007a/.github/workflows/nightly-build-wrynose.yml): nightly; starts the nightly build on `wrynose`.
- [nightly-build.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1007a/.github/workflows/nightly-build.yml): nightly or manual; runs the build unless the same inputs already built successfully.
- [pr.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1007a/.github/workflows/pr.yml): a pull request to `main` that changes more than Markdown; runs the build.
- [publish-results.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1007a/.github/workflows/publish-results.yml): called by `test-pr.yml`; publishes the LAVA test results.
- [push.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1007a/.github/workflows/push.yml): a push to `main`; runs the build.
- [qcom-preflight-checks.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1007a/.github/workflows/qcom-preflight-checks.yml): a pull request, a push to `main`, or a manual run; runs Qualcomm's [preflight checks](https://github.com/qualcomm/qcom-reusable-workflows), with only the repolinter check enabled.
- [stales.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1007a/.github/workflows/stales.yml): daily; marks issues and pull requests stale after 30 days without activity and closes stale pull requests 5 days later.
- [test-distro.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1007a/.github/workflows/test-distro.yml): called by `test.yml`; submits LAVA boot and pre-merge jobs for one distribution.
- [test-pr.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1007a/.github/workflows/test-pr.yml): a completed "Build on PR" run; would test the build in LAVA, but its test job is disabled because no machine has a LAVA device.
- [test.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1007a/.github/workflows/test.yml): called by `test-pr.yml`; tests `nodistro` and `qcom-distro`, with no devices listed.

## Repository settings

[CODEOWNERS](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1007a/.github/CODEOWNERS),
and [.gitignore](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1007a/.gitignore)
explain their settings in comments beside them.
[.github/.markdownlint.yaml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1007a/.github/.markdownlint.yaml)
configures the Markdown lint workflow; the
[markdownlint rules](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md)
define each rule. Every setting is optional, and an unlisted rule keeps its default.

| Setting | Value | Purpose | Type | Default |
| --- | --- | --- | --- | --- |
| `MD013` | `false` | Turns off the line-length rule. | Boolean or rule options | On, with 80-character lines |
| `MD024.siblings_only` | `true` | Allows repeated heading text unless the headings share a parent. | Boolean | `false`: any repeated heading fails |
| `MD033` | `false` | Allows inline HTML. | Boolean or rule options | On |
| `MD041` | `true` | Requires a top-level heading on each file's first line. | Boolean or rule options | On |
