# Configuration reference

This page covers the settings this layer maintains: the layer and machine
configuration, the [kas](https://github.com/siemens/kas) build fragments, the kernel fragment, the CI workflows,
and the repository tooling. Standard variables link to the
[Yocto Project variable glossary](https://docs.yoctoproject.org/ref-manual/variables.html);
`QCOM_*` variables are defined by [`meta-qcom`](https://github.com/qualcomm-linux/meta-qcom)
in [`qcom-base.inc`](https://github.com/qualcomm-linux/meta-qcom/blob/master/conf/machine/include/qcom-base.inc),
[`qcom-common.inc`](https://github.com/qualcomm-linux/meta-qcom/blob/master/conf/machine/include/qcom-common.inc),
and [`image_types_qcom.bbclass`](https://github.com/qualcomm-linux/meta-qcom/blob/master/classes-recipe/image_types_qcom.bbclass),
which give the defaults below.

## Loading and precedence

[BitBake](https://github.com/openembedded/bitbake) reads [`conf/layer.conf`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1010a/conf/layer.conf)
when the layer is in `BBLAYERS`, and the machine file named by `MACHINE`. In
BitBake syntax, `?=` sets a value only if none is set yet, so the first `?=`
read wins; `??=` is a weaker default used only when nothing else sets the
variable; `=` and `:append` replace or extend it
([syntax](https://docs.yoctoproject.org/bitbake/bitbake-user-manual/bitbake-user-manual-metadata.html)).
kas merges the fragments named on its command line, separated by `:`, after
their includes; later fragments override earlier ones
([kas project configuration](https://kas.readthedocs.io/en/latest/userguide/project-configuration.html)).
Environment settings for local builds are documented in
[`.env.example`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1010a/.env.example).

## Layer

Every setting in `conf/layer.conf` is required for BitBake to use the layer.

| Setting | Purpose | Type | When unset | Value |
| --- | --- | --- | --- | --- |
| [`BBPATH`](https://docs.yoctoproject.org/ref-manual/variables.html#term-BBPATH) `.=` | Lets BitBake find this layer's `conf/` files | `:`-separated paths | The layer's machines are not found | `:${LAYERDIR}` |
| [`BBFILES`](https://docs.yoctoproject.org/ref-manual/variables.html#term-BBFILES) `+=` | Registers the recipes and appends | Space-separated globs | No recipe is parsed | `recipes-*/*/*.bb`, `recipes-*/*/*.bbappend` |
| [`BBFILE_COLLECTIONS`](https://docs.yoctoproject.org/ref-manual/variables.html#term-BBFILE_COLLECTIONS) `+=` | Names the layer for the settings below and the `layer-qcom-3rdparty` override | Name | The layer has no collection | `qcom-3rdparty` |
| [`BBFILE_PATTERN_qcom-3rdparty`](https://docs.yoctoproject.org/ref-manual/variables.html#term-BBFILE_PATTERN) | Assigns the layer's files to the collection | Regular expression | Files are not assigned | `^${LAYERDIR}/` |
| [`BBFILE_PRIORITY_qcom-3rdparty`](https://docs.yoctoproject.org/ref-manual/variables.html#term-BBFILE_PRIORITY) | Breaks ties when another layer has the same recipe | Integer | One above its highest dependency | `5` |
| [`LAYERDEPENDS_qcom-3rdparty`](https://docs.yoctoproject.org/ref-manual/variables.html#term-LAYERDEPENDS) | Requires the [oe-core](https://github.com/openembedded/openembedded-core) (`core`) and `meta-qcom` (`qcom`) layers | Collection names | No dependency check | `core qcom` |
| [`LAYERSERIES_COMPAT_qcom-3rdparty`](https://docs.yoctoproject.org/ref-manual/variables.html#term-LAYERSERIES_COMPAT) | Declares the compatible release series | Series names | BitBake warns | `blacksail` |
| [`BBFILES_DYNAMIC`](https://docs.yoctoproject.org/ref-manual/variables.html#term-BBFILES_DYNAMIC) `+=` | Adds `dynamic-layers/qcom-distro/` recipes and appends only when [`meta-qcom-distro`](https://github.com/qualcomm-linux/meta-qcom-distro) (`qcom-distro`) is present | `collection:glob` entries | Those appends are not used | `qcom-distro:…/*/*/*.bb`, `qcom-distro:…/*/*/*.bbappend` |

## Machines

[`rubikpi3.conf`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1010a/conf/machine/rubikpi3.conf)
and [`radxa-dragon-q6a.conf`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1010a/conf/machine/radxa-dragon-q6a.conf)
start with `#@TYPE`, `#@NAME`, and `#@DESCRIPTION` comments naming the board, and
both `require conf/machine/include/qcom-qcs6490.inc`, the QCS6490 SoC baseline
from `meta-qcom`. All settings are optional for BitBake; the values are this
layer's choices.

| Setting | Purpose | Type | When unset | `rubikpi3` | `radxa-dragon-q6a` |
| --- | --- | --- | --- | --- | --- |
| [`PREFERRED_PROVIDER_virtual/kernel`](https://docs.yoctoproject.org/ref-manual/variables.html#term-PREFERRED_PROVIDER) `?=` | Kernel recipe; set before the SoC include so this `?=` is read first | Recipe name | `linux-qcom-next` from `qcom-base.inc`, the same value | `linux-qcom-next` | `linux-qcom-next` |
| [`MACHINE_FEATURES`](https://docs.yoctoproject.org/ref-manual/variables.html#term-MACHINE_FEATURES) `+=` | Adds EFI and PCI support to the SoC defaults | Space-separated features | The SoC include's defaults only | `efi pci` | `efi pci` |
| [`KERNEL_CMDLINE_EXTRA`](https://github.com/qualcomm-linux/meta-qcom/blob/master/recipes-kernel/images/esp-qcom-image.bb) `:append` | Gives the HDMI bridge time to probe before display setup gives up | Kernel arguments | Default probe timeout | `deferred_probe_timeout=30` | Not set |
| [`KERNEL_DEVICETREE`](https://docs.yoctoproject.org/ref-manual/variables.html#term-KERNEL_DEVICETREE) | Device tree the kernel builds | Path under `arch/arm64/boot/dts` | No board device tree | `qcom/qcs6490-thundercomm-rubikpi3.dtb` | `qcom/qcs6490-radxa-dragon-q6a.dtb` |
| `QCOM_DTB_DEFAULT` `?=` | Default device tree for the boot firmware | DTB name without suffix | `multi-dtb` | `qcs6490-thundercomm-rubikpi3` | `qcs6490-radxa-dragon-q6a` |
| `QCOM_BOOT_FIRMWARE` | Recipe that deploys the boot firmware | Recipe name or empty | `""`: no boot firmware | `firmware-qcom-boot-rubikpi3` | `""`: Radxa flashes it separately |
| `QCOM_BOOT_FILES_SUBDIR` | Deploy subfolder holding the boot firmware | Path | `""` | `rubikpi3` | `""` |
| `QCOM_PARTITION_FILES_SUBDIR` | Partition layout from [`qcom-ptool`](https://github.com/qualcomm-linux/qcom-ptool), deployed by `qcom-partition-conf` | Path | `QCOM_BOOT_FILES_SUBDIR` | `partitions/qcs6490-thundercomm-rubikpi3/ufs` (`?=`) | `""` |
| `QCOM_PARTITION_FILES_SUBDIR_SPINOR` | SPI NOR partition layout | Path | `""` | Not set | `""` |
| `QCOM_PARTITION_CONF` | Recipe that deploys partition layouts | Recipe name or empty | `qcom-partition-conf` | Not set | `""` |
| `QCOM_CDT_FILE` | CDT file packaged as `cdt.bin` | File name without `.bin` | No CDT | `RubikPi3_CDT` | `""` |
| [`WKS_FILE`](https://docs.yoctoproject.org/ref-manual/variables.html#term-WKS_FILE) | Disk layout for the `wic` image: a GPT disk with an EFI system partition booted by systemd-boot and an ext4 root partition | Kickstart file name from oe-core | No `wic` layout | Not set | `efi-uki-bootdisk.wks.in` |
| `QCOM_ESP_IMAGE` | Separate EFI system partition image | Recipe name or empty | `esp-qcom-image` when `efi` is a machine feature | Not set | `""`: the `wic` image holds the partition |
| `QCOM_VFAT_SECTOR_SIZE` `?=` | FAT sector size | Bytes | `4096` (UFS) | Not set | `512` (SD card) |
| `QCOM_BOOTIMG_ROOTFS` `?=` | Root device for the kernel command line | `root=` value | `PARTLABEL=rootfs` | Not set | `PARTLABEL=root` is set, but the parsed value is `PARTLABEL=rootfs`: `qcom-base.inc` sets it first |
| [`IMAGE_FSTYPES`](https://docs.yoctoproject.org/ref-manual/variables.html#term-IMAGE_FSTYPES) `+=` | Adds a compressed disk image and its block map | Image types | `ext4 qcomflash` | Not set | `wic.gz wic.bmap` |
| [`MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS`](https://docs.yoctoproject.org/ref-manual/variables.html#term-MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS) `+=` | Packages every image recommends | Package names | The SoC include's two packagegroups | See below | See below |

Both machines add `packagegroup-qcom-boot-essential` and
`packagegroup-machine-essential-qcom-qcs6490-soc`, repeating the SoC include,
and their own firmware packagegroup, `packagegroup-rubikpi3-firmware` or
`packagegroup-radxa-dragon-q6a-firmware`, from
[`recipes-bsp/packagegroups`](https://github.com/devdocsorg/meta-qcom-3rdparty/tree/docs/upgrade-test-1010a/recipes-bsp/packagegroups).
`radxa-dragon-q6a` also adds `packagegroup-radxa-dragon-q6a-hexagon-dsp-binaries`
(its ADSP and CDSP binaries) and `qairt-sdk-hexagon-v68` (the Hexagon v68
libraries of the Qualcomm AI Runtime SDK from `meta-qcom`).

Two appends configure other layers' recipes:
[`linux-qcom-next_git.bbappend`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1010a/recipes-kernel/linux/linux-qcom-next_git.bbappend)
adds `radxa-dragon-q6a/` to `FILESEXTRAPATHS` and the kernel fragment below to
`SRC_URI` for `radxa-dragon-q6a` only, and
[`qcom-multimedia-image.bbappend`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1010a/dynamic-layers/qcom-distro/recipes-products/images/qcom-multimedia-image.bbappend)
adds `firmware-qcom-boot-rubikpi3:LICENSE.qcom-2` to
[`INCOMPATIBLE_LICENSE_EXCEPTIONS`](https://docs.yoctoproject.org/ref-manual/variables.html#term-INCOMPATIBLE_LICENSE_EXCEPTIONS)
for `rubikpi3`, so that image can ship the boot firmware.

## Kernel fragment

[`realtek-eth-8169.cfg`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1010a/recipes-kernel/linux/radxa-dragon-q6a/realtek-eth-8169.cfg)
enables the Radxa Dragon Q6A's Realtek PCIe Ethernet. The kernel recipe merges it
over `defconfig` and its own fragments; every line is optional, and an option it
does not set keeps the value of that base. Types and dependencies
are in the [kernel's Kconfig files](https://github.com/qualcomm-linux/kernel/tree/e428097a36d210c50991063f17ee0848e9eb68a8)
at the revision `linux-qcom-next` builds.

| Option | Type | When unset | Value | Purpose |
| --- | --- | --- | --- | --- |
| `CONFIG_R8169` | tristate | Off: the base's `prune.config` disables it | `y` | Realtek 8169/8168/8101/8125 Ethernet driver, built in |
| `CONFIG_REALTEK_PHY` | tristate | `y`: `R8169` selects it | `y` | Realtek PHY driver |
| `# CONFIG_REALTEK_PHY_HWMON is not set` | bool | Off: it has no default | off | No hardware-monitor sensor for the PHY |
| `CONFIG_PHYLIB` | tristate | `y`: `R8169` selects it | `y` | PHY device support |
| `CONFIG_FIXED_PHY` | tristate | `y`: `OF_MDIO` selects it | `y` | Fixed-link PHY emulation |
| `CONFIG_MDIO_BUS` | — | — | `y` | No Kconfig symbol of this name exists at that revision, so the line has no effect |
| `CONFIG_FWNODE_MDIO`, `CONFIG_OF_MDIO`, `CONFIG_ACPI_MDIO`, `CONFIG_NET_SELFTESTS` | tristate without a prompt | The derived value | `y` | MDIO bus accessors and network self-tests; Kconfig derives their values from `PHYLIB`, `OF`, and `ACPI`, so these lines cannot change them |

## kas fragments

Every file in [`ci/`](https://github.com/devdocsorg/meta-qcom-3rdparty/tree/docs/upgrade-test-1010a/ci)
sets `header: version: 14`, the kas configuration format. `meta-qcom-3rdparty`
listed under `repos` without a URL is this checkout.

| File | Settings |
| --- | --- |
| `base.yml` | Includes `meta-qcom`'s `ci/base.yml` (oe-core, BitBake, `nodistro`, target `core-image-base`, and `meta-qcom`'s lock file) and adds this layer and `meta-qcom` from `master`. |
| `rubikpi3.yml`, `radxa-dragon-q6a.yml` | Include `base.yml` and set `machine`. |
| `meta-qcom.yml` | Declares `meta-qcom` from `master`, for the fragments below. |
| `ci.yml`, `mirror.yml`, `qcom-distro.yml` | Include `meta-qcom.yml` and the `meta-qcom` fragment of the same name: CI build settings, the Yocto Project sstate mirror, or the Qualcomm Linux distribution with its layers and image targets. |
| `linux-qcom-next.yml` | Sets `PREFERRED_PROVIDER_virtual/kernel = "linux-qcom-next"` in `local.conf`, overriding the machine's `?=`. |
| `world.yml` | Sets `EXCLUDE_FROM_WORLD = "1"` with `0` for the `layer-qcom` and `layer-qcom-3rdparty` overrides, and targets `world`, so a world build covers only these two layers. |

## CI workflows

| Workflow | Trigger and purpose |
| --- | --- |
| [`backport.yml`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1010a/.github/workflows/backport.yml) | A merged pull request to `main`: opens backport pull requests for the `backport wrynose` label. |
| [`bitbake-lint.yml`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1010a/.github/workflows/bitbake-lint.yml) | Pull requests changing BitBake files outside `.github/` and `ci/`: lints the changed lines with [`bitbake-lint-action`](https://github.com/qualcomm-linux/bitbake-lint-action); findings do not fail the job. |
| [`build-yocto.yml`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1010a/.github/workflows/build-yocto.yml) | Called by the build workflows, in `qualcomm-linux` only: runs `yocto-patchreview` and `yocto-check-layer`, and builds both machines with `nodistro` and `qcom-distro`. |
| [`pr.yml`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1010a/.github/workflows/pr.yml) | Pull requests to `main` that change more than Markdown: runs `build-yocto.yml`. |
| [`push.yml`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1010a/.github/workflows/push.yml) | Pushes to `main`: runs `build-yocto.yml`. |
| [`nightly-build.yml`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1010a/.github/workflows/nightly-build.yml) | Daily or manual: runs `build-yocto.yml` unless the same inputs already built successfully. |
| [`nightly-build-wrynose.yml`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1010a/.github/workflows/nightly-build-wrynose.yml) | Daily: starts `nightly-build.yml` on `wrynose`. |
| [`test-pr.yml`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1010a/.github/workflows/test-pr.yml), [`test.yml`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1010a/.github/workflows/test.yml), [`test-distro.yml`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1010a/.github/workflows/test-distro.yml), [`publish-results.yml`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1010a/.github/workflows/publish-results.yml) | After "Build on PR": LAVA boot tests and result publishing. Disabled, because no machine in this layer has a LAVA device. |
| [`markdownlint.yml`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1010a/.github/workflows/markdownlint.yml) | Pushes to `main` and pull requests changing Markdown: checks every `*.md` file. |
| [`qcom-preflight-checks.yml`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1010a/.github/workflows/qcom-preflight-checks.yml) | Pull requests, pushes to `main`, and manual runs: runs [`qcom-reusable-workflows`](https://github.com/qualcomm/qcom-reusable-workflows)' preflight checks with only repolinter enabled. |
| [`stales.yml`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1010a/.github/workflows/stales.yml) | Daily: marks issues and pull requests stale after 30 days without activity and closes stale pull requests 5 days later. |
| [`documentation.yml`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1010a/.github/workflows/documentation.yml) | Pull requests and pushes to `main`: builds this site and checks the function reference and offline browsing. |

## Repository tooling

[`.markdownlint.yaml`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1010a/.github/.markdownlint.yaml)
configures the [markdownlint rules](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md)
for `markdownlint.yml`; every rule not listed keeps its default and is enabled.

| Rule | Type | Default | Value | Effect |
| --- | --- | --- | --- | --- |
| `MD013` line length | Boolean or options | Enabled, 80 characters | `false` | Lines may be any length |
| `MD024` duplicate headings | Boolean or options | Enabled for the whole file | `siblings_only: true` | Headings may repeat under different parents |
| `MD033` inline HTML | Boolean or options | Enabled | `false` | HTML is allowed |
| `MD041` first-line heading | Boolean or options | Enabled | `true` | Each file starts with a top-level heading |

[`CODEOWNERS`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1010a/.github/CODEOWNERS)
assigns every path, documentation included, to the maintainers. The
documentation build's settings are commented beside them in
[`conf.py`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1010a/docs/source/conf.py)
and the [`Makefile`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1010a/docs/source/Makefile).
