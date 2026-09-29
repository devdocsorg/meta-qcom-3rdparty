# Configuration reference

This page explains the settings this layer maintains. Recipes and packagegroups
are explained with the board example in the
[contribution guide](../contributing/CONTRIBUTING.md).

## How settings combine

BitBake reads `conf/layer.conf` when the layer is listed in `BBLAYERS`, and a
machine file when `MACHINE` names it. `=` sets a value, `?=` sets it only if
nothing set it earlier, `??=` is a default that any other assignment replaces,
and `+=` and `:append` add to it; a `:<machine>` suffix limits a line to that
machine. The [BitBake syntax guide](https://docs.yoctoproject.org/bitbake/2.18/bitbake-user-manual/bitbake-user-manual-metadata.html)
defines these operators, and the
[variable glossary](https://docs.yoctoproject.org/6.0/ref-manual/variables.html)
defines each standard variable. kas merges the files it is given, joined with
`:`, from left to right after their `includes`; the
[kas project configuration](https://kas.readthedocs.io/en/latest/userguide/project-configuration.html)
defines each key.

## Layer

[conf/layer.conf](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/conf/layer.conf)
registers the layer. Every line is required; its value is the only safe one.

| Setting | Value | Purpose |
| --- | --- | --- |
| `BBPATH .=` | `:${LAYERDIR}` | Lets BitBake find this layer's `conf/` files. |
| `BBFILES +=` | `recipes-*/*/*.bb` and `*.bbappend` under `${LAYERDIR}` | Adds the recipes and appends. |
| `BBFILE_COLLECTIONS +=` | `qcom-3rdparty` | Names the layer; the `layer-qcom-3rdparty` override uses it. |
| `BBFILE_PATTERN_qcom-3rdparty :=` | `^${LAYERDIR}/` | Matches the files that belong to this layer. |
| `BBFILE_PRIORITY_qcom-3rdparty` | `5` | Ranks the layer when several layers provide the same recipe. |
| `LAYERDEPENDS_qcom-3rdparty` | `core qcom` | Requires [OpenEmbedded-Core](https://github.com/openembedded/openembedded-core) and [meta-qcom](https://github.com/qualcomm-linux/meta-qcom). |
| `LAYERSERIES_COMPAT_qcom-3rdparty` | `wrynose` | Declares the compatible Yocto Project release (6.0). |
| `BBFILES_DYNAMIC +=` | `qcom-distro:` recipes and appends under `dynamic-layers/qcom-distro/` | Uses those files only when [meta-qcom-distro](https://github.com/qualcomm-linux/meta-qcom-distro) is present. |

## Machines

[rubikpi3.conf](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/conf/machine/rubikpi3.conf)
and [radxa-dragon-q6a.conf](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/conf/machine/radxa-dragon-q6a.conf)
describe the two boards. Both start with `#@TYPE`, `#@NAME`, and `#@DESCRIPTION`
comments that name the machine, and both
`require conf/machine/include/qcom-qcs6490.inc`, the QCS6490 SoC baseline from
[meta-qcom](https://github.com/qualcomm-linux/meta-qcom).
Values are strings or space-separated lists. "Unset" gives the value without
the line. To try another value, set it for one machine in `local.conf`, for
example `QCOM_VFAT_SECTOR_SIZE:radxa-dragon-q6a = "4096"` for a UFS target.

| Setting | `rubikpi3` | `radxa-dragon-q6a` | Purpose; unset |
| --- | --- | --- | --- |
| `PREFERRED_PROVIDER_virtual/kernel ?=` | `linux-qcom-next`, before the SoC include | `linux-qcom-next`, after the SoC include | Kernel recipe. Only the first `?=` counts, so the Radxa line repeats the value the SoC include already set. Unset: `linux-qcom-next` from the SoC include. |
| `MACHINE_FEATURES +=` | `efi pci` | `efi pci` | Adds EFI boot and PCIe to the SoC features. Unset: neither. |
| `KERNEL_CMDLINE_EXTRA:append` | `deferred_probe_timeout=30`, after a space | — | Gives the HDMI bridge 30 seconds to probe so the display appears. Unset: the kernel's default timeout. |
| `KERNEL_DEVICETREE` | `qcom/qcs6490-thundercomm-rubikpi3.dtb` | `qcom/qcs6490-radxa-dragon-q6a.dtb` | Device tree the kernel builds. Unset: no board device tree. |
| `QCOM_DTB_DEFAULT ?=` | `qcs6490-thundercomm-rubikpi3` | `qcs6490-radxa-dragon-q6a` | Device tree packed as `dtb.bin`. Unset: `multi-dtb`, a FIT image of all device trees. |
| `QCOM_BOOT_FIRMWARE` | `firmware-qcom-boot-rubikpi3` | empty | Recipe whose boot firmware goes into the flashable package. Empty or unset: none; the Dragon Q6A's SPI NOR firmware comes from Radxa and is flashed separately. |
| `QCOM_BOOT_FILES_SUBDIR` | `rubikpi3` | empty | Deploy subfolder holding that boot firmware. Unset: empty. |
| `QCOM_PARTITION_FILES_SUBDIR` | `?= partitions/qcs6490-thundercomm-rubikpi3/ufs` | empty | Partition tables from [qcom-ptool](https://github.com/qualcomm-linux/qcom-ptool). Unset: `QCOM_BOOT_FILES_SUBDIR`. |
| `QCOM_PARTITION_FILES_SUBDIR_SPINOR` | — | empty | SPI NOR partition tables. Unset: empty. |
| `QCOM_PARTITION_CONF` | — | empty | Recipe that deploys the partition tables. Unset: `qcom-partition-conf`. |
| `QCOM_CDT_FILE` | `RubikPi3_CDT` | empty | Board CDT file packed as `cdt.bin`. Unset: none. |
| `WKS_FILE` | — | `efi-uki-bootdisk.wks.in` | [OpenEmbedded-Core](https://github.com/openembedded/openembedded-core)'s disk layout: an EFI system partition with systemd-boot and a unified kernel image, then the root filesystem. Unset: `<image>.<machine>.wks`, which this layer does not provide, so the `wic` image types would fail. |
| `QCOM_ESP_IMAGE` | — | empty | Skips the separate ESP image from [meta-qcom](https://github.com/qualcomm-linux/meta-qcom), since the disk layout creates it. Unset: `esp-qcom-image` on EFI machines. |
| `QCOM_VFAT_SECTOR_SIZE ?=` | — | `512` | FAT sector size for SD cards. Unset: `4096`, for UFS. |
| `QCOM_BOOTIMG_ROOTFS ?=` | — | `PARTLABEL=root` | Root device for the kernel command line. No effect: the SoC include already set `PARTLABEL=rootfs` with `?=`. |
| `IMAGE_FSTYPES +=` | — | `wic wic.gz wic.bmap` | Adds the disk image, its compressed copy, and a block map for `bmaptool`. Unset: the SoC's `ext4` and `qcomflash`. |
| `MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS +=` | `packagegroup-qcom-boot-essential`, `packagegroup-machine-essential-qcom-qcs6490-soc`, `packagegroup-rubikpi3-firmware` | the same two, `packagegroup-radxa-dragon-q6a-firmware`, `packagegroup-radxa-dragon-q6a-hexagon-dsp-binaries`, `qairt-sdk-hexagon-v68` | Packages recommended into every image. The first two repeat the SoC include; the rest add board firmware, DSP binaries, and the Hexagon v68 AI runtime. |

## Kernel

[linux-qcom-next_git.bbappend](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/recipes-kernel/linux/linux-qcom-next_git.bbappend)
changes the `linux-qcom-next` kernel from [meta-qcom](https://github.com/qualcomm-linux/meta-qcom).

| Setting | Value | Purpose |
| --- | --- | --- |
| `FILESEXTRAPATHS:prepend :=` | `${THISDIR}/${BPN}:` | Searches `recipes-kernel/linux/linux-qcom-next/`, which this layer does not have, so the line has no effect. |
| `FILESEXTRAPATHS:prepend:radxa-dragon-q6a :=` | `${THISDIR}/radxa-dragon-q6a:` | Lets the Radxa build find its kernel fragment. |
| `SRC_URI:append:radxa-dragon-q6a` | `file://realtek-eth-8169.cfg` | Merges that fragment into the kernel configuration. |

[realtek-eth-8169.cfg](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/recipes-kernel/linux/radxa-dragon-q6a/realtek-eth-8169.cfg)
builds the board's Realtek PCIe Ethernet support into the kernel. `=y` builds an
option in and `# ... is not set` disables it; without a line, the kernel's
`defconfig` and the [meta-qcom](https://github.com/qualcomm-linux/meta-qcom) fragments decide. `CONFIG_R8169=m` would build the
driver as a module instead. The options are tristate, except the boolean
`CONFIG_REALTEK_PHY_HWMON`. The
[kernel's Kconfig](https://github.com/qualcomm-linux/kernel/tree/qcom-next/drivers/net)
defines each option.

| Option | Value | Purpose |
| --- | --- | --- |
| `CONFIG_R8169` | `y` | Realtek RTL8169/8168/8101/8125 Ethernet driver. |
| `CONFIG_REALTEK_PHY` | `y` | Realtek PHY driver. |
| `CONFIG_PHYLIB`, `CONFIG_FIXED_PHY` | `y` | PHY support and fixed-link PHY emulation. |
| `CONFIG_FWNODE_MDIO`, `CONFIG_OF_MDIO`, `CONFIG_ACPI_MDIO` | `y` | MDIO bus access for PHYs described by device tree or ACPI. |
| `CONFIG_NET_SELFTESTS` | `y` | Generic network self-tests; follows `CONFIG_PHYLIB`. |
| `CONFIG_REALTEK_PHY_HWMON` | not set | Leaves out the PHY temperature sensor. |
| `CONFIG_MDIO_BUS` | `y` | Not an option in the kernel [meta-qcom](https://github.com/qualcomm-linux/meta-qcom) pins, so it is ignored. |

## Distribution images

[qcom-multimedia-image.bbappend](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/dynamic-layers/qcom-distro/recipes-products/images/qcom-multimedia-image.bbappend)
applies only with [meta-qcom-distro](https://github.com/qualcomm-linux/meta-qcom-distro). Its
`INCOMPATIBLE_LICENSE_EXCEPTIONS:append:rubikpi3` value, a space and
`firmware-qcom-boot-rubikpi3:LicenseRef-LICENSE.qcom-2`, lets the RUBIK Pi 3
image ship its boot firmware although the image's `INCOMPATIBLE_LICENSE` policy
rejects that licence. Unset: the policy rejects the firmware.

## kas files

The files in [ci/](https://github.com/devdocsorg/meta-qcom-3rdparty/tree/docs/layer-documentation/ci)
select what kas builds. Each starts with `header: version: 14`, the kas file format,
and most with a `yaml-language-server` comment that points editors at the kas schema.

| File | Settings | Purpose |
| --- | --- | --- |
| `base.yml` | `includes` [meta-qcom's `ci/base.yml`](https://github.com/qualcomm-linux/meta-qcom/blob/master/ci/base.yml); `repos: meta-qcom` from `https://github.com/qualcomm-linux/meta-qcom` branch `master`; `meta-qcom-3rdparty` with no URL | Shared base: [OpenEmbedded-Core](https://github.com/openembedded/openembedded-core), [BitBake](https://github.com/openembedded/bitbake), [meta-qcom](https://github.com/qualcomm-linux/meta-qcom), and this checkout, building `core-image-base` with `nodistro`. |
| `rubikpi3.yml`, `radxa-dragon-q6a.yml` | `includes: ci/base.yml`; `machine` | One file per board. |
| `meta-qcom.yml` | `repos: meta-qcom`, as in `base.yml` | Declares [meta-qcom](https://github.com/qualcomm-linux/meta-qcom) for the fragments below. |
| `qcom-distro.yml` | `includes: ci/meta-qcom.yml` and [meta-qcom's `ci/qcom-distro.yml`](https://github.com/qualcomm-linux/meta-qcom/blob/master/ci/qcom-distro.yml) | Builds with `qcom-distro` and its extra layers and images. |
| `ci.yml`, `mirror.yml` | `includes: ci/meta-qcom.yml` and [meta-qcom's `ci/ci.yml`](https://github.com/qualcomm-linux/meta-qcom/blob/master/ci/ci.yml) or [`ci/mirror.yml`](https://github.com/qualcomm-linux/meta-qcom/blob/master/ci/mirror.yml) | CI build tuning and the Yocto Project shared-state mirror. |
| `linux-qcom-next.yml` | `local_conf_header: kernelprovider` sets `PREFERRED_PROVIDER_virtual/kernel = "linux-qcom-next"` | Forces that kernel, overriding the machine's `?=`. |
| `world.yml` | `local_conf_header: world_build` sets `EXCLUDE_FROM_WORLD = "1"`, then `"0"` for `layer-qcom` and `layer-qcom-3rdparty`; `target: world` | Builds every recipe in [meta-qcom](https://github.com/qualcomm-linux/meta-qcom) and this layer. |

Combine a board file with the others, for example
`kas-container build ci/rubikpi3.yml:ci/qcom-distro.yml`.

## Environment settings

[.env.example](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/.env.example)
documents `KAS_CONTAINER`, `KAS_WORK_DIR`, `DL_DIR`, and `SSTATE_DIR`. Nothing
reads the file; export the settings before running kas-container.

## Repository and CI settings

| File | Settings |
| --- | --- |
| [CODEOWNERS](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/.github/CODEOWNERS) | `*` assigns every path, including documentation, to `@ricardosalveti` and `@ndechesne` for review. |
| [.markdownlint.yaml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/.github/.markdownlint.yaml) | Turns off `MD013` (line length) and `MD033` (inline HTML), limits `MD024` (repeated headings) to sibling headings, and requires `MD041` (a top-level first heading). Other [markdownlint rules](https://github.com/DavidAnson/markdownlint#rules--aliases) keep their defaults. |
| [.gitignore](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/.gitignore) | Keeps the documentation environment, build caches, and generated reference pages out of commits. |

Each [workflow](https://github.com/devdocsorg/meta-qcom-3rdparty/tree/docs/layer-documentation/.github/workflows)
runs as follows:

- `pr.yml` — pull requests to `main` that change more than Markdown: runs `build-yocto.yml`.
- `push.yml` — pushes to `main`: runs `build-yocto.yml`.
- `nightly-build.yml` — daily and on demand: runs `build-yocto.yml`, skipping inputs that already built; `nightly-build-wrynose.yml` starts it on `wrynose`.
- `build-yocto.yml` — called by the three above, in `qualcomm-linux` only: runs `yocto-patchreview` and `yocto-check-layer`, and builds each machine with `nodistro` and `qcom-distro` through [meta-qcom's `compile.yml`](https://github.com/qualcomm-linux/meta-qcom/blob/master/.github/workflows/compile.yml).
- `bitbake-lint.yml` — pull requests that change BitBake files: lints the changed lines with [bitbake-lint-action](https://github.com/qualcomm-linux/bitbake-lint-action) for the release in `conf/layer.conf`, reporting findings without failing.
- `markdownlint.yml` — pull requests, and pushes to `main`, that change Markdown: runs markdownlint with `.github/.markdownlint.yaml`.
- `qcom-preflight-checks.yml` — every pull request and push to `main`: runs the repolinter check from [qcom-reusable-workflows](https://github.com/qualcomm/qcom-reusable-workflows).
- `documentation.yml` — every pull request and push to `main`: builds and checks this site.
- `backport.yml` — a merged pull request to `main` labelled `backport wrynose`: opens the `wrynose` backport.
- `stales.yml` — daily: marks inactive issues and pull requests stale, and closes stale pull requests.
- `test-pr.yml`, `test.yml`, `test-distro.yml`, `publish-results.yml` — the LAVA boot-test chain; disconnected until a machine has a lab device.
