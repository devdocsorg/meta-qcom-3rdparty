# Configuration reference

This page explains the settings this layer chooses. [BitBake](https://github.com/openembedded/bitbake) variables are defined
in the Yocto Project [variable glossary](https://docs.yoctoproject.org/ref-manual/variables.html),
and [kas](https://github.com/siemens/kas) keys in the kas [project configuration](https://kas.readthedocs.io/en/latest/userguide/project-configuration.html)
reference; those pages give each standard field's syntax and type. Unless a row
says otherwise, settings are optional strings, and "default" is the value that
applies when the line is removed. `?=` and `??=` assign weak defaults that an
earlier or stronger assignment, such as one in `local.conf`, overrides.

## Machines

[`conf/machine/rubikpi3.conf`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006c/conf/machine/rubikpi3.conf)
defines the Thundercomm RUBIK Pi 3, and
[`conf/machine/radxa-dragon-q6a.conf`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006c/conf/machine/radxa-dragon-q6a.conf)
the Radxa Dragon Q6A. Both use the QCS6490 SoC. Defaults come from
[meta-qcom](https://github.com/qualcomm-linux/meta-qcom)'s
[`qcom-base.inc`](https://github.com/qualcomm-linux/meta-qcom/blob/b6b6e1b04ed09116936dbb5926dd830eafdc52a2/conf/machine/include/qcom-base.inc),
[`qcom-common.inc`](https://github.com/qualcomm-linux/meta-qcom/blob/b6b6e1b04ed09116936dbb5926dd830eafdc52a2/conf/machine/include/qcom-common.inc),
and [`image_types_qcom.bbclass`](https://github.com/qualcomm-linux/meta-qcom/blob/b6b6e1b04ed09116936dbb5926dd830eafdc52a2/classes-recipe/image_types_qcom.bbclass).

| Setting | `rubikpi3` | `radxa-dragon-q6a` | Purpose | Required | Default |
| --- | --- | --- | --- | --- | --- |
| `PREFERRED_PROVIDER_virtual/kernel ?=` | `linux-qcom-next` | `linux-qcom-next` | Kernel recipe. Set before the SoC include, because the first weak assignment wins. | No | `linux-qcom-next` |
| `require` | `conf/machine/include/qcom-qcs6490.inc` | same | SoC baseline from meta-qcom. | Yes | None |
| `MACHINE_FEATURES +=` | `efi pci` | `efi pci` | Adds UEFI boot and PCIe to meta-qcom's feature list. | No | `alsa bluetooth usbgadget usbhost wifi` |
| `KERNEL_CMDLINE_EXTRA:append` | `deferred_probe_timeout=30` | — | Gives the HDMI bridge time to probe so `/dev/dri/card0` appears. | No | Nothing appended |
| `KERNEL_DEVICETREE` | `qcom/qcs6490-thundercomm-rubikpi3.dtb` | `qcom/qcs6490-radxa-dragon-q6a.dtb` | Device tree the kernel builds. | Yes | None |
| `QCOM_DTB_DEFAULT ?=` | `qcs6490-thundercomm-rubikpi3` | `qcs6490-radxa-dragon-q6a` | Device tree packaged as `dtb.bin` for the boot firmware. | No | `multi-dtb` |
| `QCOM_BOOT_FIRMWARE` | `firmware-qcom-boot-rubikpi3` | `""` | Recipe whose boot binaries go into the flashable package. | No | `""` (none) |
| `QCOM_BOOT_FILES_SUBDIR` | `rubikpi3` | `""` | Deploy subfolder holding those binaries. | No | `""` |
| `QCOM_PARTITION_FILES_SUBDIR` | `?= partitions/qcs6490-thundercomm-rubikpi3/ufs` | `""` | Partition layout from `qcom-partition-conf`, which comes from [qcom-ptool](https://github.com/qualcomm-linux/qcom-ptool). | No | `QCOM_BOOT_FILES_SUBDIR` |
| `QCOM_PARTITION_FILES_SUBDIR_SPINOR` | — | `""` | SPI NOR partition layout; blank, as meta-qcom's default is. | No | `""` |
| `QCOM_PARTITION_CONF` | — | `""` | Recipe that provides partition files; blank skips it. | No | `qcom-partition-conf` |
| `QCOM_CDT_FILE` | `RubikPi3_CDT` | `""` | CDT file name, without `.bin`, packaged as `cdt.bin`. | No | Unset (no CDT) |
| `MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS +=` | SoC packagegroups and `packagegroup-rubikpi3-firmware` | SoC packagegroups, `packagegroup-radxa-dragon-q6a-firmware`, `packagegroup-radxa-dragon-q6a-hexagon-dsp-binaries`, `qairt-sdk-hexagon-v68` | Board firmware for the image. `packagegroup-qcom-boot-essential` and `packagegroup-machine-essential-qcom-qcs6490-soc` repeat the SoC include's values. | No | The SoC include's two packagegroups |

The Radxa Dragon Q6A boots from firmware that Radxa flashes into SPI NOR, so its
machine builds only the disk image:

| Setting | Value | Purpose | Default |
| --- | --- | --- | --- |
| `WKS_FILE` | `efi-uki-bootdisk.wks.in` | [OpenEmbedded-Core](https://github.com/openembedded/openembedded-core)'s kickstart for an EFI system partition with systemd-boot and a unified kernel image, plus the root file system. | `${IMAGE_BASENAME}.${MACHINE}.wks` |
| `QCOM_ESP_IMAGE` | `""` | Skips meta-qcom's separate ESP image; the kickstart creates the ESP. | `esp-qcom-image` when `MACHINE_FEATURES` has `efi` |
| `QCOM_VFAT_SECTOR_SIZE ?=` | `512` | Sector size of the vfat images meta-qcom creates, for SD cards; set `4096` for UFS. | `4096` |
| `QCOM_BOOTIMG_ROOTFS ?=` | `PARTLABEL=root` | Root device that meta-qcom's boot images put in the kernel command line. | `PARTLABEL=rootfs` |
| `IMAGE_FSTYPES +=` | `wic.gz wic.bmap` | Writes the compressed disk image and its block map. | meta-qcom's `ext4 qcomflash` |

## Layer

[`conf/layer.conf`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006c/conf/layer.conf)
registers the layer. Every line is required for the layer to load.

| Setting | Value | Purpose |
| --- | --- | --- |
| `BBPATH .=` | `:${LAYERDIR}` | Lets BitBake find this layer's `conf/` and classes. |
| `BBFILES +=` | `recipes-*/*/*.bb`, `recipes-*/*/*.bbappend` | Recipes and appends to parse. |
| `BBFILE_COLLECTIONS +=` | `qcom-3rdparty` | Collection name used by the settings below and in overrides. |
| `BBFILE_PATTERN_qcom-3rdparty :=` | `^${LAYERDIR}/` | Assigns files under this layer to the collection. |
| `BBFILE_PRIORITY_qcom-3rdparty` | `5` | Priority against other layers providing the same recipe. |
| `LAYERDEPENDS_qcom-3rdparty` | `core qcom` | Requires OpenEmbedded-Core and meta-qcom. |
| `LAYERSERIES_COMPAT_qcom-3rdparty` | `blacksail` | Yocto Project 6.1 release series this branch supports. |
| `BBFILES_DYNAMIC +=` | `qcom-distro:` with `dynamic-layers/qcom-distro/*/*/*.bb` and `.bbappend` | Parses the `dynamic-layers/qcom-distro/` metadata only when the `qcom-distro` collection, [meta-qcom-distro](https://github.com/qualcomm-linux/meta-qcom-distro), is present. |

## Appends

| File | Setting | Value | Purpose | Required | Default |
| --- | --- | --- | --- | --- | --- |
| [`linux-qcom-next_git.bbappend`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006c/recipes-kernel/linux/linux-qcom-next_git.bbappend) | `FILESEXTRAPATHS:prepend:radxa-dragon-q6a`, `SRC_URI:append:radxa-dragon-q6a` | `radxa-dragon-q6a/`, `file://realtek-eth-8169.cfg` | Adds the kernel fragment below for that machine only. | No | Kernel built without the fragment |
| [`qcom-multimedia-image.bbappend`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006c/dynamic-layers/qcom-distro/recipes-products/images/qcom-multimedia-image.bbappend) | `INCOMPATIBLE_LICENSE_EXCEPTIONS:append:rubikpi3` | `firmware-qcom-boot-rubikpi3:LICENSE.qcom-2` | Lets that image ship the boot firmware despite the distribution's licence restrictions. | Yes, for that image on `rubikpi3` | No exception |

### Kernel fragment

[`realtek-eth-8169.cfg`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006c/recipes-kernel/linux/radxa-dragon-q6a/realtek-eth-8169.cfg)
builds the Realtek r8169 Ethernet driver and the PHY and MDIO support it uses
into the kernel. Each line sets a Kconfig symbol of the kernel that
`linux-qcom-next` builds ([qualcomm-linux/kernel](https://github.com/qualcomm-linux/kernel) at
`e428097a36d210c50991063f17ee0848e9eb68a8`). Without the fragment, a symbol keeps
the value from that kernel's configuration.

| Symbol | Value | Type | Purpose |
| --- | --- | --- | --- |
| `CONFIG_R8169` | `y` | tristate | Realtek 8169/8168/8101/8125 Ethernet driver. |
| `CONFIG_REALTEK_PHY` | `y` | tristate | Realtek PHY driver. |
| `CONFIG_PHYLIB`, `CONFIG_FIXED_PHY` | `y` | tristate | PHY support and fixed-link PHY emulation. |
| `CONFIG_FWNODE_MDIO`, `CONFIG_OF_MDIO`, `CONFIG_ACPI_MDIO` | `y` | tristate | MDIO helpers for firmware nodes, device tree, and ACPI. |
| `CONFIG_NET_SELFTESTS` | `y` | tristate | Generic network self-tests used by PHY drivers. |
| `CONFIG_MDIO_BUS` | `y` | — | Not defined in that kernel, so the line has no effect. |
| `CONFIG_REALTEK_PHY_HWMON` | not set | bool | Leaves out hardware monitoring for Realtek PHYs. |

## kas configuration

The `ci/` fragments compose builds; list several separated by `:`. Each uses kas
configuration format `header.version` 14.

| File | Settings | Purpose | Required | Without it |
| --- | --- | --- | --- | --- |
| [`base.yml`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006c/ci/base.yml) | Includes meta-qcom's `ci/base.yml`; `repos`: meta-qcom from its `master` branch, and this repository as the local repository | Base build: meta-qcom's base sets `nodistro`, OpenEmbedded-Core, BitBake, and the `core-image-base` target. | Yes: the machine fragments include it | The machine fragments cannot load |
| [`rubikpi3.yml`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006c/ci/rubikpi3.yml), [`radxa-dragon-q6a.yml`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006c/ci/radxa-dragon-q6a.yml) | Include `ci/base.yml`; `machine` | Select a board. | Yes: one machine fragment per build | meta-qcom's `machine: unset`, which fails |
| [`meta-qcom.yml`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006c/ci/meta-qcom.yml) | `repos`: meta-qcom from `master` | Lets the fragments below include meta-qcom's files. | Only through the fragments that include it | Those fragments fail to resolve their meta-qcom includes |
| [`qcom-distro.yml`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006c/ci/qcom-distro.yml) | Includes `ci/meta-qcom.yml` and meta-qcom's `ci/qcom-distro.yml` | Builds the `qcom-distro` distribution with its layers and images. | No | `nodistro` and `core-image-base` |
| [`ci.yml`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006c/ci/ci.yml) | Includes `ci/meta-qcom.yml` and meta-qcom's `ci/ci.yml` | CI build settings, which CI puts first in every build. | No | Builds without meta-qcom's CI settings |
| [`mirror.yml`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006c/ci/mirror.yml) | Includes `ci/meta-qcom.yml` and meta-qcom's `ci/mirror.yml` | Adds the Yocto Project shared-state mirror. | No | No shared-state mirror |
| [`linux-qcom-next.yml`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006c/ci/linux-qcom-next.yml) | `local_conf_header` `kernelprovider`: `PREFERRED_PROVIDER_virtual/kernel = "linux-qcom-next"` | Forces the `linux-qcom-next` kernel over a machine's weak choice. | No | The machine's kernel choice |
| [`world.yml`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006c/ci/world.yml) | `local_conf_header` `world_build`: `EXCLUDE_FROM_WORLD = "1"`, then `"0"` for the `qcom` and `qcom-3rdparty` layers; `target`: `world` | Builds every recipe of meta-qcom and this layer. | No | The base `core-image-base` target |

## Environment

[`.env.example`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006c/.env.example)
documents the variables `kas-container` and
[`kas-container-shell-helper.sh`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006c/ci/kas-container-shell-helper.sh)
read. Copy it to `.env` and load it with `set -a; . ./.env; set +a`; a variable
already set in the environment keeps its value. All are optional paths.

| Variable | Purpose | Default | Safe example |
| --- | --- | --- | --- |
| `KAS_CONTAINER` | `kas-container` script the helper runs | `kas-container` from `PATH` | `$HOME/.local/bin/kas-container` |
| `KAS_WORK_DIR` | Folder for kas checkouts and `build/` | Current folder | `$HOME/kas-work` |
| `DL_DIR` | Shared download cache | `build/downloads` in `KAS_WORK_DIR` | `$HOME/yocto-cache/downloads` |
| `SSTATE_DIR` | Shared-state cache | `build/sstate-cache` in `KAS_WORK_DIR` | `$HOME/yocto-cache/sstate-cache` |

## CI workflows

Each [workflow](https://github.com/devdocsorg/meta-qcom-3rdparty/tree/docs/upgrade-test-1006c/.github/workflows)
is listed with its trigger and what it does. The build jobs run only in the
`qualcomm-linux` organisation.

- [`pr.yml`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006c/.github/workflows/pr.yml): pull requests to `main` that change files other than Markdown and its lint configuration; runs `build-yocto.yml`.
- [`push.yml`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006c/.github/workflows/push.yml): pushes to `main`; runs `build-yocto.yml`.
- [`nightly-build.yml`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006c/.github/workflows/nightly-build.yml): daily or manual; runs `build-yocto.yml`, skipping a build that already succeeded for the same inputs.
- [`nightly-build-wrynose.yml`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006c/.github/workflows/nightly-build-wrynose.yml): daily; starts the nightly build on `wrynose`.
- [`build-yocto.yml`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006c/.github/workflows/build-yocto.yml): called by the three above; runs `yocto-patchreview` and `yocto-check-layer`, and builds each machine with `nodistro` (plus a world build) and `qcom-distro` through meta-qcom's compile workflow.
- [`bitbake-lint.yml`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006c/.github/workflows/bitbake-lint.yml): pull requests that change BitBake files outside `.github/` and `ci/`; lints the changed lines and reports without failing.
- [`markdownlint.yml`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006c/.github/workflows/markdownlint.yml): pushes to `main` and pull requests that change Markdown; checks it with [`.github/.markdownlint.yaml`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006c/.github/.markdownlint.yaml).
- [`documentation.yml`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006c/.github/workflows/documentation.yml): pull requests and pushes to `main`; builds the documentation site and checks the function reference and offline browsing.
- [`qcom-preflight-checks.yml`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006c/.github/workflows/qcom-preflight-checks.yml): pull requests, pushes to `main`, and manual runs; runs Qualcomm's preflight checks with only the repolinter check enabled.
- [`backport.yml`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006c/.github/workflows/backport.yml): a merged pull request to `main`; opens a backport pull request for each `backport wrynose` label.
- [`test-pr.yml`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006c/.github/workflows/test-pr.yml), [`test.yml`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006c/.github/workflows/test.yml), [`test-distro.yml`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006c/.github/workflows/test-distro.yml), [`publish-results.yml`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006c/.github/workflows/publish-results.yml): LAVA boot tests after a pull request build and their results; disabled because no machine in this layer has a LAVA device.
- [`stales.yml`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006c/.github/workflows/stales.yml): daily; marks inactive issues and pull requests as stale and closes stale pull requests.

The documentation tools' settings are explained by comments in
[`conf.py`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006c/docs/source/conf.py)
and the [`Makefile`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006c/docs/source/Makefile),
and reviewers by comments in [`CODEOWNERS`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006c/.github/CODEOWNERS).
