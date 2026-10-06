# Configuration reference

The layer has no runtime configuration of its own: its settings are BitBake
metadata, kas build fragments, and CI workflows. This page explains the choices
the layer makes; the [BitBake syntax guide](https://docs.yoctoproject.org/bitbake/bitbake-user-manual/bitbake-user-manual-metadata.html)
and the [Yocto Project variable glossary](https://docs.yoctoproject.org/ref-manual/variables.html)
define the operators and standard variables.

## Loading and precedence

BitBake reads [layer.conf](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/build-prerequisites-test/conf/layer.conf)
when the layer is listed in `bblayers.conf`, the machine file named by `MACHINE`,
and then each recipe and its appends. `?=` sets a default that an earlier
assignment keeps, `??=` a weaker default, `+=` and `:append` add to a value, and
a `:<machine>` suffix applies a line only to that machine. kas writes the
`local_conf_header` entries of the selected fragments into `local.conf`; in a
`first.yml:second.yml` list, later fragments override earlier ones. The
[environment settings](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/build-prerequisites-test/.env.example)
choose where kas-container works and caches.

## Layer

[conf/layer.conf](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/build-prerequisites-test/conf/layer.conf)
registers the layer. Values are strings; every line except `BBFILES_DYNAMIC` is needed to use the layer.

| Setting | Purpose | Value |
| --- | --- | --- |
| `BBPATH .=` | Lets BitBake find this layer's `conf/` files | `:${LAYERDIR}` |
| `BBFILES +=` | Finds recipes and appends in each subfolder of a `recipes-*` folder | `${LAYERDIR}/recipes-*/*/*.bb`, `.bbappend` |
| `BBFILE_COLLECTIONS +=` | Names the layer collection | `qcom-3rdparty` |
| `BBFILE_PATTERN_qcom-3rdparty` | Assigns files under the layer to the collection | `^${LAYERDIR}/` |
| `BBFILE_PRIORITY_qcom-3rdparty` | Recipe priority against other layers; [meta-qcom](https://github.com/qualcomm-linux/meta-qcom) uses 6, so a recipe found in both layers comes from [meta-qcom](https://github.com/qualcomm-linux/meta-qcom) | `5` |
| `LAYERDEPENDS_qcom-3rdparty` | Required layer collections: [OpenEmbedded-Core](https://github.com/openembedded/openembedded-core) and [meta-qcom](https://github.com/qualcomm-linux/meta-qcom) | `core qcom` |
| `LAYERSERIES_COMPAT_qcom-3rdparty` | Yocto Project release series the layer supports | `blacksail` |
| `BBFILES_DYNAMIC +=` | Adds `dynamic-layers/qcom-distro/` recipes and appends only when [meta-qcom-distro](https://github.com/qualcomm-linux/meta-qcom-distro)'s `qcom-distro` collection is present | `qcom-distro:<path>` |

## Machines

Each [machine file](https://github.com/devdocsorg/meta-qcom-3rdparty/tree/docs/build-prerequisites-test/conf/machine)
starts with `#@TYPE`, `#@NAME`, and `#@DESCRIPTION` comments that name the board
for layer tools, and requires [meta-qcom](https://github.com/qualcomm-linux/meta-qcom)'s `conf/machine/include/qcom-qcs6490.inc`,
which supplies the QCS6490 SoC defaults. Both machines set:

| Setting | Purpose | Default without it | Value |
| --- | --- | --- | --- |
| `PREFERRED_PROVIDER_virtual/kernel ?=` | Kernel recipe; set before the SoC include because the first `?=` wins | `linux-qcom-next` from [meta-qcom](https://github.com/qualcomm-linux/meta-qcom) | `linux-qcom-next` |
| `MACHINE_FEATURES +=` | Adds EFI boot and PCI support to the SoC features | SoC features only | `efi pci` |
| `KERNEL_DEVICETREE` | Device tree built with the kernel | None | `qcom/qcs6490-<board>.dtb` |
| `QCOM_DTB_DEFAULT ?=` | Device tree selected at boot | `multi-dtb` | `qcs6490-<board>` |
| `MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS +=` | Packages every image recommends: repeats the SoC include's boot-service and QCS6490 kernel-module packagegroups and adds the board's firmware packagegroup | The first two only | `packagegroup-qcom-boot-essential packagegroup-machine-essential-qcom-qcs6490-soc packagegroup-<board>-firmware` |

[rubikpi3.conf](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/build-prerequisites-test/conf/machine/rubikpi3.conf)
flashes Qualcomm boot firmware from this layer:

| Setting | Purpose | Default without it | Value |
| --- | --- | --- | --- |
| `KERNEL_CMDLINE_EXTRA:append` | Gives the HDMI bridge time to probe, so the display device appears | [meta-qcom](https://github.com/qualcomm-linux/meta-qcom)'s arguments only | `deferred_probe_timeout=30` |
| `QCOM_BOOT_FIRMWARE` | Recipe that deploys the boot firmware | None | `firmware-qcom-boot-rubikpi3` |
| `QCOM_BOOT_FILES_SUBDIR` | Deploy subfolder holding that firmware | None | `rubikpi3` |
| `QCOM_PARTITION_FILES_SUBDIR ?=` | Partition layout from [qcom-ptool](https://github.com/qualcomm-linux/qcom-ptool), through [meta-qcom](https://github.com/qualcomm-linux/meta-qcom)'s `qcom-partition-conf` | `QCOM_BOOT_FILES_SUBDIR` | `partitions/qcs6490-thundercomm-rubikpi3/ufs` |
| `QCOM_CDT_FILE` | Board CDT, flashed as `cdt.bin` | None | `RubikPi3_CDT` |

[radxa-dragon-q6a.conf](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/build-prerequisites-test/conf/machine/radxa-dragon-q6a.conf)
boots from Radxa's SPI NOR firmware, so the image holds only the EFI system
partition and root file system:

| Setting | Purpose | Default without it | Value |
| --- | --- | --- | --- |
| `QCOM_BOOT_FIRMWARE`, `QCOM_BOOT_FILES_SUBDIR`, `QCOM_PARTITION_FILES_SUBDIR`, `QCOM_PARTITION_FILES_SUBDIR_SPINOR`, `QCOM_PARTITION_CONF`, `QCOM_CDT_FILE` | Leave Qualcomm boot firmware, partitions, and CDT out of the image | `qcom-partition-conf` for `QCOM_PARTITION_CONF`; empty otherwise | `""` |
| `WKS_FILE` | Disk layout: an ESP with systemd-boot and a unified kernel image, then the root file system | `<image>.<machine>.wks` | `efi-uki-bootdisk.wks.in` |
| `QCOM_ESP_IMAGE` | Disables [meta-qcom](https://github.com/qualcomm-linux/meta-qcom)'s separate ESP image; the disk layout creates it | `esp-qcom-image` with `efi` | `""` |
| `QCOM_VFAT_SECTOR_SIZE ?=` | Sector size of the ESP; SD cards use 512, UFS 4096 | `4096` | `512` |
| `QCOM_BOOTIMG_ROOTFS ?=` | Root device on the kernel command line | `PARTLABEL=rootfs` | `PARTLABEL=root` |
| `IMAGE_FSTYPES +=` | Adds a compressed disk image and its block map | `ext4 qcomflash` | `wic.gz wic.bmap` |
| `MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS +=` | Also recommends the Hexagon DSP binaries and the QAIRT SDK's Hexagon v68 libraries | As above | `packagegroup-radxa-dragon-q6a-hexagon-dsp-binaries qairt-sdk-hexagon-v68` |

## Recipes

- [firmware-qcom-boot-rubikpi3](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/build-prerequisites-test/recipes-bsp/firmware-boot/firmware-qcom-boot-rubikpi3_20260915.bb)
  fetches the vendor's boot binaries at a fixed `SRCREV` of the `qli2.0` branch of
  [boot-assets](https://github.com/rubikpi-ai/boot-assets) (licence `LicenseRef-LICENSE.qcom-2`). It builds no
  code (`INHIBIT_DEFAULT_DEPS`, configure and compile disabled), is architecture
  independent (`allarch`), and adds a deploy task that installs the files under
  `QCOM_BOOT_IMG_SUBDIR` (`rubikpi3`). It builds for `rubikpi3` only
  (`COMPATIBLE_MACHINE`).
- [packagegroup-rubikpi3](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/build-prerequisites-test/recipes-bsp/packagegroups/packagegroup-rubikpi3.bb)
  and [packagegroup-radxa-dragon-q6a](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/build-prerequisites-test/recipes-bsp/packagegroups/packagegroup-radxa-dragon-q6a.bb)
  recommend each board's firmware packages, including the camera firmware
  `camxfirmware-kodiak` on the Radxa board; the Adreno GPU firmware is
  included only when `DISTRO_FEATURES` has `opencl`, `opengl`, or `vulkan`. The
  Radxa packagegroup also requires the board's ADSP and CDSP binaries in its
  `-hexagon-dsp-binaries` package.
- [linux-qcom-next_git.bbappend](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/build-prerequisites-test/recipes-kernel/linux/linux-qcom-next_git.bbappend)
  adds `realtek-eth-8169.cfg` to the Radxa Dragon Q6A kernel. The fragment builds
  in the RTL8169 Ethernet driver with its Realtek PHY, PHY library, fixed-PHY, and
  MDIO bus support (devicetree, firmware-node, and ACPI), and network self-tests;
  `CONFIG_REALTEK_PHY_HWMON` stays off.
- [qcom-multimedia-image.bbappend](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/build-prerequisites-test/dynamic-layers/qcom-distro/recipes-products/images/qcom-multimedia-image.bbappend)
  allows the boot firmware's `LICENSE.qcom-2` in that image on `rubikpi3`, where
  the distribution would otherwise reject it as incompatible.

## kas build fragments

| Fragment | Effect |
| --- | --- |
| [base.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/build-prerequisites-test/ci/base.yml) | Includes [meta-qcom](https://github.com/qualcomm-linux/meta-qcom)'s `ci/base.yml` ([OpenEmbedded-Core](https://github.com/openembedded/openembedded-core), [BitBake](https://github.com/openembedded/bitbake), `nodistro`, `core-image-base`) and adds this checkout as a layer |
| [rubikpi3.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/build-prerequisites-test/ci/rubikpi3.yml), [radxa-dragon-q6a.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/build-prerequisites-test/ci/radxa-dragon-q6a.yml) | Include `base.yml` and set `machine` |
| [meta-qcom.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/build-prerequisites-test/ci/meta-qcom.yml) | Declares [meta-qcom](https://github.com/qualcomm-linux/meta-qcom)'s `master` branch for the fragments below |
| [qcom-distro.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/build-prerequisites-test/ci/qcom-distro.yml), [ci.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/build-prerequisites-test/ci/ci.yml), [mirror.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/build-prerequisites-test/ci/mirror.yml) | Include [meta-qcom](https://github.com/qualcomm-linux/meta-qcom)'s fragment of the same name: the Qualcomm distribution, CI settings, or download mirrors |
| [linux-qcom-next.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/build-prerequisites-test/ci/linux-qcom-next.yml) | Forces `PREFERRED_PROVIDER_virtual/kernel = "linux-qcom-next"` in `local.conf` |
| [world.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/build-prerequisites-test/ci/world.yml) | Builds `world`, limited by `EXCLUDE_FROM_WORLD` to the `qcom` and `qcom-3rdparty` layers |

Every fragment uses kas configuration format version 14.

## CI workflows

The [workflows](https://github.com/devdocsorg/meta-qcom-3rdparty/tree/docs/build-prerequisites-test/.github/workflows)
run on GitHub Actions:

- `push.yml`, `pr.yml`, and `nightly-build.yml` (daily, and on demand) call
  `build-yocto.yml`, which runs `yocto-patchreview` and `yocto-check-layer` and
  builds both machines with and without the Qualcomm distribution;
  `nightly-build-wrynose.yml` starts the nightly build on `wrynose`. Pull requests
  that change only Markdown skip the build.
- `bitbake-lint.yml` lints changed recipes and configuration on pull requests;
  `markdownlint.yml` lints Markdown with `.github/.markdownlint.yaml`.
- `documentation.yml` builds and checks this site on pull requests and pushes to `main`.
- `qcom-preflight-checks.yml` runs Qualcomm's repository lint (Repolinter) on pull
  requests and pushes to `main`.
- `backport.yml` opens `wrynose` backports for merged pull requests labelled
  `backport wrynose`; `stales.yml` marks issues and pull requests stale after 30
  days of inactivity and closes stale pull requests 5 days later.
- `test-pr.yml`, `test.yml`, `test-distro.yml`, and `publish-results.yml` run LAVA
  boot tests; they are disabled until a board has a LAVA device.

[CODEOWNERS](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/build-prerequisites-test/.github/CODEOWNERS)
assigns both maintainers to every path. The documentation build's settings are
explained by the comments in `docs/source/conf.py` and `docs/source/Makefile`.
