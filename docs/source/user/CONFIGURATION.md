# Configuration reference

This page explains the settings this layer defines. Standard variables and
fields are defined upstream; each section links the relevant manual and
describes the local choices.

## How settings combine

BitBake reads `bblayers.conf` and each layer's `conf/layer.conf` first, then
`local.conf` (written by kas from each fragment's `local_conf_header`), then
the machine file and the files it requires. A plain `=` assignment replaces a value. `?=` assigns only
if nothing has assigned the variable yet, so the first `?=` wins, and `??=` is
a weak default that any other assignment overrides. `:append`, `+=`, and
`:prepend` add to a value, and a `:<machine>` suffix limits a line to that
machine. See the BitBake manual on
[default values](https://docs.yoctoproject.org/bitbake/bitbake-user-manual/bitbake-user-manual-metadata.html#setting-a-default-value)
and the Yocto Project [variable glossary](https://docs.yoctoproject.org/ref-manual/variables.html).

Upstream defaults below come from meta-qcom's
[qcom-base.inc](https://github.com/qualcomm-linux/meta-qcom/blob/46261cd7cb48521654ec1ed9fdd3b4897718a2b7/conf/machine/include/qcom-base.inc),
[qcom-common.inc](https://github.com/qualcomm-linux/meta-qcom/blob/46261cd7cb48521654ec1ed9fdd3b4897718a2b7/conf/machine/include/qcom-common.inc),
and [image_types_qcom.bbclass](https://github.com/qualcomm-linux/meta-qcom/blob/46261cd7cb48521654ec1ed9fdd3b4897718a2b7/classes-recipe/image_types_qcom.bbclass).

## Layer

[conf/layer.conf](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/offline-layer-documentation/conf/layer.conf)
registers the layer; every value is required for the layer to load.

| Setting | Value and purpose |
| --- | --- |
| `BBPATH .=` | Appends the layer directory so BitBake finds `conf/` and machine files here. |
| `BBFILES +=` | Parses recipes and appends at `recipes-*/*/*.bb` and `*.bbappend`. |
| `BBFILE_COLLECTIONS +=`, `BBFILE_PATTERN_qcom-3rdparty` | Names the collection `qcom-3rdparty` and matches files under this layer. |
| `BBFILE_PRIORITY_qcom-3rdparty` | `5`; the priority when several layers provide the same recipe. |
| `LAYERDEPENDS_qcom-3rdparty` | `core qcom`: requires OpenEmbedded-Core and meta-qcom. |
| `LAYERSERIES_COMPAT_qcom-3rdparty` | `wrynose`: the Yocto Project release series this branch supports. The lint workflow reads its last word. |
| `BBFILES_DYNAMIC +=` | Parses `dynamic-layers/qcom-distro/` only when the `qcom-distro` layer (meta-qcom-distro) is present. |

## Machines

[rubikpi3.conf](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/offline-layer-documentation/conf/machine/rubikpi3.conf)
builds a UFS image flashed with QDL.
[radxa-dragon-q6a.conf](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/offline-layer-documentation/conf/machine/radxa-dragon-q6a.conf)
builds a disk image and leaves boot firmware to the board's SPI NOR. The
`#@TYPE`, `#@NAME`, and `#@DESCRIPTION` comments name each machine for layer
tools. "Not set" means the upstream default applies.

| Setting (type) | Default when unset | `rubikpi3` | `radxa-dragon-q6a` |
| --- | --- | --- | --- |
| `require conf/machine/include/qcom-qcs6490.inc` (path) | Required: the QCS6490 SoC baseline | Required | Required |
| `PREFERRED_PROVIDER_virtual/kernel ?=` (recipe) | `linux-qcom-next` | `linux-qcom-next`, set before the SoC include so it takes effect | `linux-qcom-next`, after the include, so it repeats the default |
| `MACHINE_FEATURES +=` (list) | `alsa bluetooth usbgadget usbhost wifi` | Adds `efi pci` | Adds `efi pci` |
| `KERNEL_CMDLINE_EXTRA:append` (string) | Empty for non-real-time kernels | Appends `deferred_probe_timeout=30`, so the HDMI bridge can probe | Not set |
| `KERNEL_DEVICETREE` (list of `.dtb` paths) | Empty: no device tree | `qcom/qcs6490-thundercomm-rubikpi3.dtb` | `qcom/qcs6490-radxa-dragon-q6a.dtb` |
| `QCOM_DTB_DEFAULT ?=` (DTB name) | `multi-dtb`, which packages the DTBs in a FIT image | `qcs6490-thundercomm-rubikpi3` | `qcs6490-radxa-dragon-q6a` |
| `QCOM_BOOT_FIRMWARE` (recipe) | Empty: no boot firmware in the flash package | `firmware-qcom-boot-rubikpi3` | `""` |
| `QCOM_BOOT_FILES_SUBDIR` (deploy subdirectory) | Empty | `rubikpi3` | `""` |
| `QCOM_PARTITION_FILES_SUBDIR` (deploy subdirectory) | `${QCOM_BOOT_FILES_SUBDIR}` | `?= partitions/qcs6490-thundercomm-rubikpi3/ufs`, deployed by `qcom-partition-conf` from qcom-ptool | `""` |
| `QCOM_PARTITION_FILES_SUBDIR_SPINOR` (deploy subdirectory) | Empty | Not set | `""`, repeating the default |
| `QCOM_PARTITION_CONF` (recipe) | `qcom-partition-conf` | Not set | `""`: no partition tables |
| `QCOM_CDT_FILE` (file name without `.bin`) | Unset: no CDT | `RubikPi3_CDT`, packaged as `cdt.bin` | `""` |
| `QCOM_ESP_IMAGE` (recipe) | `esp-qcom-image` when `efi` is a machine feature | Not set | `""`: the wic image creates the ESP |
| `WKS_FILE` (kickstart file) | `<image>.<machine>.wks` | Not set | `efi-uki-bootdisk.wks.in` from OpenEmbedded-Core: an ESP with systemd-boot and a unified kernel image |
| `QCOM_VFAT_SECTOR_SIZE ?=` (bytes) | `4096`, for UFS | Not set | `512`, for SD cards; use `4096` for UFS |
| `QCOM_BOOTIMG_ROOTFS ?=` (kernel `root=` value) | `PARTLABEL=rootfs` | Not set | `PARTLABEL=root`; no effect, because `qcom-base.inc` assigns it first |
| `IMAGE_FSTYPES +=` (list) | `qcom-base.inc` adds `ext4` and `qcomflash` | Not set | Adds `wic wic.gz wic.bmap` |
| `MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS +=` (package list) | The SoC include adds `packagegroup-qcom-boot-essential` and `packagegroup-machine-essential-qcom-qcs6490-soc` | Repeats both and adds `packagegroup-rubikpi3-firmware` | Repeats both and adds `packagegroup-radxa-dragon-q6a-firmware`, `packagegroup-radxa-dragon-q6a-hexagon-dsp-binaries`, and `qairt-sdk-hexagon-v68` |

## Recipes and appends

| File | Local choices |
| --- | --- |
| [packagegroup-rubikpi3.bb](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/offline-layer-documentation/recipes-bsp/packagegroups/packagegroup-rubikpi3.bb) | One `${PN}-firmware` package. It recommends the Adreno GPU firmware only when `DISTRO_FEATURES` contains `opencl`, `opengl`, or `vulkan`, plus QUPv3, video, board audio, and compute firmware. Wi-Fi and Bluetooth firmware are omitted until they reach linux-firmware. |
| [packagegroup-radxa-dragon-q6a.bb](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/offline-layer-documentation/recipes-bsp/packagegroups/packagegroup-radxa-dragon-q6a.bb) | `${PN}-firmware` recommends the same conditional GPU firmware plus camera, LT9611UXC HDMI bridge, board audio and compute, QUPv3, and video firmware. `${PN}-hexagon-dsp-binaries` requires the board's ADSP and CDSP binaries, so images can omit them. |
| [firmware-qcom-boot-rubikpi3_20260621.bb](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/offline-layer-documentation/recipes-bsp/firmware-boot/firmware-qcom-boot-rubikpi3_20260621.bb) | Fetches `rubikpi-ai/boot-assets` at a pinned `SRCREV` under `LicenseRef-LICENSE.qcom-2`. It skips the default toolchain dependencies and the configure and compile tasks, is architecture-independent, and only builds for `rubikpi3`. `do_deploy` installs the binaries and CDT into `QCOM_BOOT_IMG_SUBDIR` (`rubikpi3`), which matches the machine's `QCOM_BOOT_FILES_SUBDIR`. |
| [linux-qcom-next_git.bbappend](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/offline-layer-documentation/recipes-kernel/linux/linux-qcom-next_git.bbappend) | The unconditional `FILESEXTRAPATHS:prepend` adds `recipes-kernel/linux/linux-qcom-next/`, which does not exist, so it has no effect. For `radxa-dragon-q6a` only, it adds the `radxa-dragon-q6a/` directory and appends `realtek-eth-8169.cfg` to `SRC_URI`. |
| [realtek-eth-8169.cfg](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/offline-layer-documentation/recipes-kernel/linux/radxa-dragon-q6a/realtek-eth-8169.cfg) | A [kernel configuration fragment](https://docs.yoctoproject.org/kernel-dev/common.html#creating-configuration-fragments) that builds in the RTL8169 Ethernet driver (`CONFIG_R8169`) with its PHY and MDIO support (`CONFIG_PHYLIB`, `CONFIG_FIXED_PHY`, `CONFIG_REALTEK_PHY`, `CONFIG_MDIO_BUS`, `CONFIG_FWNODE_MDIO`, `CONFIG_OF_MDIO`, `CONFIG_ACPI_MDIO`) and `CONFIG_NET_SELFTESTS`, all `=y`. It leaves `CONFIG_REALTEK_PHY_HWMON` disabled. Options it omits keep the kernel's configured values. |
| [qcom-multimedia-image.bbappend](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/offline-layer-documentation/dynamic-layers/qcom-distro/recipes-products/images/qcom-multimedia-image.bbappend) | For `rubikpi3`, `INCOMPATIBLE_LICENSE_EXCEPTIONS:append` lets `qcom-multimedia-image` ship `firmware-qcom-boot-rubikpi3` under `LicenseRef-LICENSE.qcom-2`. It applies only with meta-qcom-distro. |

## kas fragments

The fragments in [ci/](https://github.com/devdocsorg/meta-qcom-3rdparty/tree/docs/offline-layer-documentation/ci)
use kas configuration format `version: 14`; the
[kas project configuration](https://kas.readthedocs.io/en/latest/userguide/project-configuration.html)
defines each key. Combine them with `:`, for example
`ci/rubikpi3.yml:ci/qcom-distro.yml`. The `yaml-language-server` comment lets
editors validate a file against the kas schema.

| File | Sets |
| --- | --- |
| `base.yml` | Includes meta-qcom's `ci/base.yml`: `nodistro`, OpenEmbedded-Core and BitBake, and the `core-image-base` target. Tracks meta-qcom `master`; the empty `meta-qcom-3rdparty` entry adds this checkout as a layer. |
| `rubikpi3.yml`, `radxa-dragon-q6a.yml` | Include `base.yml` and set `machine`. |
| `meta-qcom.yml` | Declares the meta-qcom repository on `master` for the fragments below. |
| `qcom-distro.yml` | Includes meta-qcom's `ci/qcom-distro.yml`: `qcom-distro`, its extra layers, and four Qualcomm Linux images. |
| `ci.yml` | Includes meta-qcom's `ci/ci.yml`: its CI build settings, ccache, and the shared-state mirror. |
| `mirror.yml` | Includes meta-qcom's `ci/mirror.yml`: the Yocto Project shared-state mirror. |
| `linux-qcom-next.yml` | Forces `PREFERRED_PROVIDER_virtual/kernel = "linux-qcom-next"` in `local.conf`. |
| `world.yml` | Excludes every recipe from `world` except those in meta-qcom and this layer, and builds `world`. |

## Environment

[.env.example](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/offline-layer-documentation/.env.example)
documents the optional environment variables for kas-container builds. Nothing
loads the file; export the values in your shell. kas documents its
[environment variables](https://kas.readthedocs.io/en/latest/userguide/env-vars.html).

## CI workflows

The workflows in
[.github/workflows/](https://github.com/devdocsorg/meta-qcom-3rdparty/tree/docs/offline-layer-documentation/.github/workflows)
use GitHub's [workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax).

- `pr.yml`: pull requests to `main` that change more than Markdown; runs `build-yocto.yml`.
- `push.yml`: pushes to `main`; runs `build-yocto.yml`.
- `nightly-build.yml`: daily or on demand; runs `build-yocto.yml`, skipping a build whose inputs already built successfully.
- `nightly-build-wrynose.yml`: daily; starts `nightly-build.yml` on `wrynose`.
- `build-yocto.yml`: called by the three above; runs `yocto-patchreview` and `yocto-check-layer`, then builds every machine with `nodistro` and `qcom-distro` through meta-qcom's compile workflow. Its jobs run only in the `qualcomm-linux` organisation.
- `bitbake-lint.yml`: pull requests changing BitBake files outside `ci/` and `.github/`; reports oelint-adv findings on the changed files without failing.
- `markdownlint.yml`: pull requests and pushes to `main` changing Markdown; runs markdownlint with `.github/.markdownlint.yaml`.
- `documentation.yml`: pull requests and pushes to `main`; runs the documentation `setup` and `check` targets.
- `qcom-preflight-checks.yml`: pull requests, pushes to `main`, and on demand; runs Qualcomm's preflight workflow with only its repolinter check enabled.
- `backport.yml`: merged pull requests to `main` labelled `backport wrynose`; opens the backport pull request.
- `stales.yml`: daily; marks inactive issues and pull requests stale and closes stale pull requests.
- `test-pr.yml`, `test.yml`, `test-distro.yml`, `publish-results.yml`: LAVA boot tests and result publishing. They stay disconnected until a machine has a lab device.

## Repository settings

| File | Setting | Value and purpose |
| --- | --- | --- |
| [.markdownlint.yaml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/offline-layer-documentation/.github/.markdownlint.yaml) | `MD013` | `false`: no line-length limit. |
| | `MD024` | `siblings_only: true`: repeated headings are allowed under different parents. |
| | `MD033` | `false`: inline HTML is allowed. |
| | `MD041` | `true`: each file starts with a top-level heading. |
| [CODEOWNERS](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/offline-layer-documentation/.github/CODEOWNERS) | `*` | `@ricardosalveti @ndechesne` review every path, including documentation. |

The [markdownlint rules](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md)
not listed keep their defaults. Documentation build settings are commented in
place in `docs/source/conf.py`, `docs/source/Makefile`, and `.gitignore`.
