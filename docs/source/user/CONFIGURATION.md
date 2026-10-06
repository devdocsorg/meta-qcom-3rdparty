# Configuration reference

BitBake reads [`conf/layer.conf`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006b/conf/layer.conf)
when the layer is in `bblayers.conf`, and `conf/machine/<MACHINE>.conf` when
`MACHINE` names one of this layer's machines. Recipes and appends apply once the
layer is enabled. kas merges the fragments named on its command line, separated
by `:`, in order, so a later fragment overrides an earlier one. A variable linked
to the [Yocto Project glossary](https://docs.yoctoproject.org/ref-manual/variables.html)
takes its type and default from there; this page records the values chosen here.
`?=` sets a value only if none is set yet, `+=` and `:append` add to the existing
value, and a `:<machine>` suffix applies a setting to that machine only.

## Layer

| Setting | Value here | Why |
| --- | --- | --- |
| [`BBPATH`](https://docs.yoctoproject.org/bitbake/bitbake-user-manual/bitbake-user-manual-ref-variables.html#term-BBPATH) | `.= ":${LAYERDIR}"` | Lets BitBake find this layer's `conf/` files. Required. |
| [`BBFILES`](https://docs.yoctoproject.org/ref-manual/variables.html#term-BBFILES) | `recipes-*/*/*.bb` and `recipes-*/*/*.bbappend` | Recipes and appends live two folders below a `recipes-*` folder. Required. |
| [`BBFILE_COLLECTIONS`](https://docs.yoctoproject.org/ref-manual/variables.html#term-BBFILE_COLLECTIONS), [`BBFILE_PATTERN`](https://docs.yoctoproject.org/ref-manual/variables.html#term-BBFILE_PATTERN) | `qcom-3rdparty`, `^${LAYERDIR}/` | Names the layer collection and the files that belong to it. Required. |
| [`BBFILE_PRIORITY`](https://docs.yoctoproject.org/ref-manual/variables.html#term-BBFILE_PRIORITY) | `5` | Precedence when another layer has a recipe of the same name. Optional; unset, BitBake uses one more than the highest priority among the layers it depends on. |
| [`LAYERDEPENDS`](https://docs.yoctoproject.org/ref-manual/variables.html#term-LAYERDEPENDS) | `core qcom` | The build stops unless OpenEmbedded-Core and [meta-qcom](https://github.com/qualcomm-linux/meta-qcom) are present. Optional; unset, BitBake checks no dependencies. |
| [`LAYERSERIES_COMPAT`](https://docs.yoctoproject.org/bitbake/bitbake-user-manual/bitbake-user-manual-ref-variables.html#term-LAYERSERIES_COMPAT) | `blacksail` | Release series this branch supports; the build stops when OpenEmbedded-Core is from another series. Optional; unset, BitBake only warns. |
| [`BBFILES_DYNAMIC`](https://docs.yoctoproject.org/ref-manual/variables.html#term-BBFILES_DYNAMIC) | `qcom-distro:` recipes and appends under `dynamic-layers/qcom-distro/` | Applies those files only when the `qcom-distro` layer from [meta-qcom-distro](https://github.com/qualcomm-linux/meta-qcom-distro) is present. Optional; unset, no files depend on other layers. |

## Machines

Both machines require `conf/machine/include/qcom-qcs6490.inc` from meta-qcom,
which sets the QCS6490 tune, adds `packagegroup-qcom-boot-additional`, and pulls
in `qcom-base.inc` and `qcom-common.inc`. The `#@TYPE`, `#@NAME`, and
`#@DESCRIPTION` comments name the machine for tools that list machines. The
`QCOM_*` settings are read by meta-qcom's
[`image_types_qcom`](https://github.com/qualcomm-linux/meta-qcom/blob/master/classes-recipe/image_types_qcom.bbclass)
class, which packages the flashable `qcomflash` image. All settings are optional
unless marked.

| Setting | Purpose | Type | When unset | `rubikpi3` | `radxa-dragon-q6a` |
| --- | --- | --- | --- | --- | --- |
| `PREFERRED_PROVIDER_virtual/kernel ?=` | Kernel recipe; set before the SoC include, because the first `?=` wins | Recipe name | `linux-qcom-next` from `qcom-base.inc` | `linux-qcom-next` | `linux-qcom-next` |
| [`MACHINE_FEATURES`](https://docs.yoctoproject.org/ref-manual/variables.html#term-MACHINE_FEATURES) `+=` | Adds board hardware to the SoC's `alsa bluetooth usbgadget usbhost wifi` | Space-separated features | SoC features only | `efi pci` | `efi pci` |
| `KERNEL_CMDLINE_EXTRA:append` | Kernel arguments added to the boot image and UKI command lines meta-qcom builds | String | No board arguments | `deferred_probe_timeout=30`, so the display driver waits for the HDMI bridge | Not set |
| [`KERNEL_DEVICETREE`](https://docs.yoctoproject.org/ref-manual/variables.html#term-KERNEL_DEVICETREE) | Device tree the kernel builds; required for these boards | `.dtb` path | No device tree | `qcom/qcs6490-thundercomm-rubikpi3.dtb` | `qcom/qcs6490-radxa-dragon-q6a.dtb` |
| `QCOM_DTB_DEFAULT ?=` | Device tree packed into `dtb.bin` | DTB name, or `multi-dtb` for a FIT image of all | `multi-dtb` | `qcs6490-thundercomm-rubikpi3` | `qcs6490-radxa-dragon-q6a` |
| `QCOM_BOOT_FIRMWARE` | Recipe whose deployed boot binaries go into the `qcomflash` package | Recipe name | No boot firmware | `firmware-qcom-boot-rubikpi3` | Empty: Radxa flashes the SPI NOR firmware separately |
| `QCOM_BOOT_FILES_SUBDIR` | Deploy subfolder holding those binaries | Path | Empty | `rubikpi3` | Empty |
| `QCOM_PARTITION_FILES_SUBDIR ?=` | Deploy subfolder with the partition files from [qcom-ptool](https://github.com/qualcomm-linux/qcom-ptool) | Path | `QCOM_BOOT_FILES_SUBDIR` | `partitions/qcs6490-thundercomm-rubikpi3/ufs` | Empty |
| `QCOM_PARTITION_FILES_SUBDIR_SPINOR` | Deploy subfolder with SPI NOR partition files | Path | Empty | Not set | Empty |
| `QCOM_PARTITION_CONF` | Recipe that deploys the partition files | Recipe name | `qcom-partition-conf` | Not set | Empty |
| `QCOM_CDT_FILE` | CDT file, without `.bin`, copied into the package as `cdt.bin` | File name | No CDT | `RubikPi3_CDT` | Empty |
| `QCOM_ESP_IMAGE` | Image recipe for the EFI system partition in the package | Recipe name | `esp-qcom-image` when `MACHINE_FEATURES` has `efi` | Not set | Empty: Wic creates the ESP |
| [`WKS_FILE`](https://docs.yoctoproject.org/ref-manual/variables.html#term-WKS_FILE) | Wic disk layout | Kickstart file name | `<image>.<machine>.wks` | Not set | `efi-uki-bootdisk.wks.in`: an ESP with systemd-boot and a UKI, then the root file system |
| `QCOM_VFAT_SECTOR_SIZE ?=` | Sector size of the vfat images | Bytes | `4096`, for UFS | Not set | `512`, for SD cards |
| `QCOM_BOOTIMG_ROOTFS ?=` | `root=` on the kernel command lines meta-qcom builds | Root device | `PARTLABEL=rootfs` | Not set | `PARTLABEL=root` |
| [`IMAGE_FSTYPES`](https://docs.yoctoproject.org/ref-manual/variables.html#term-IMAGE_FSTYPES) `+=` | Adds image formats to meta-qcom's `ext4 qcomflash` | Space-separated types | `ext4 qcomflash` | Not set | `wic.gz wic.bmap` |
| [`MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS`](https://docs.yoctoproject.org/ref-manual/variables.html#term-MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS) `+=` | Packages the board needs to boot | Space-separated packages | The SoC include's `packagegroup-qcom-boot-essential` and `packagegroup-machine-essential-qcom-qcs6490-soc` | Those two again, and `packagegroup-rubikpi3-firmware` | Those two again, `packagegroup-radxa-dragon-q6a-firmware`, `packagegroup-radxa-dragon-q6a-hexagon-dsp-binaries`, and `qairt-sdk-hexagon-v68` |

## Recipes and appends

Each recipe's fields follow their glossary definitions. The values that carry a
local choice:

| File | Setting | Value here and why |
| --- | --- | --- |
| [packagegroup-rubikpi3.bb](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006b/recipes-bsp/packagegroups/packagegroup-rubikpi3.bb) | `PACKAGES`, [`RRECOMMENDS`](https://docs.yoctoproject.org/ref-manual/variables.html#term-RRECOMMENDS) | One `-firmware` package recommending the QUP, video, audio, and compute firmware, plus the Adreno GPU firmware when `DISTRO_FEATURES` has `opencl`, `opengl`, or `vulkan`. Wi-Fi and Bluetooth firmware are omitted until upstream `linux-firmware` has them. |
| [packagegroup-radxa-dragon-q6a.bb](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006b/recipes-bsp/packagegroups/packagegroup-radxa-dragon-q6a.bb) | `PACKAGES`, `RRECOMMENDS`, [`RDEPENDS`](https://docs.yoctoproject.org/ref-manual/variables.html#term-RDEPENDS) | A `-firmware` package with the same GPU condition, the camera, HDMI bridge, audio, compute, QUP, and video firmware, and a separate `-hexagon-dsp-binaries` package that requires the ADSP and CDSP binaries, so an image can take the firmware without them. |
| [firmware-qcom-boot-rubikpi3_20260915.bb](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006b/recipes-bsp/firmware-boot/firmware-qcom-boot-rubikpi3_20260915.bb) | [`SRC_URI`](https://docs.yoctoproject.org/ref-manual/variables.html#term-SRC_URI), [`SRCREV`](https://docs.yoctoproject.org/ref-manual/variables.html#term-SRCREV), `LICENSE`, [`LIC_FILES_CHKSUM`](https://docs.yoctoproject.org/ref-manual/variables.html#term-LIC_FILES_CHKSUM) | Fetches the vendor's [boot-assets](https://github.com/rubikpi-ai/boot-assets) `qli2.0` branch at a fixed commit, under `LicenseRef-LICENSE.qcom-2`. |
| | [`INHIBIT_DEFAULT_DEPS`](https://docs.yoctoproject.org/ref-manual/variables.html#term-INHIBIT_DEFAULT_DEPS), `do_configure[noexec]`, `do_compile[noexec]`, `inherit allarch deploy` | `1`, `1`, `1`: the recipe only packages prebuilt binaries, so it needs no compiler, configure, or compile step; its package is architecture-independent and it deploys the binaries. |
| | `QCOM_BOOT_IMG_SUBDIR`, [`COMPATIBLE_MACHINE`](https://docs.yoctoproject.org/ref-manual/variables.html#term-COMPATIBLE_MACHINE), `addtask deploy` | `rubikpi3`, `(rubikpi3)`: deploys under the subfolder the machine's `QCOM_BOOT_FILES_SUBDIR` names, for this board only, before `do_build`. |
| [linux-qcom-next_git.bbappend](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006b/recipes-kernel/linux/linux-qcom-next_git.bbappend) | [`FILESEXTRAPATHS`](https://docs.yoctoproject.org/ref-manual/variables.html#term-FILESEXTRAPATHS)`:prepend:radxa-dragon-q6a`, `SRC_URI:append:radxa-dragon-q6a` | Adds `realtek-eth-8169.cfg` to the kernel for that board only. |
| [qcom-multimedia-image.bbappend](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006b/dynamic-layers/qcom-distro/recipes-products/images/qcom-multimedia-image.bbappend) | [`INCOMPATIBLE_LICENSE_EXCEPTIONS`](https://docs.yoctoproject.org/ref-manual/variables.html#term-INCOMPATIBLE_LICENSE_EXCEPTIONS)`:append:rubikpi3` | Allows `firmware-qcom-boot-rubikpi3` under `LICENSE.qcom-2` in that image on `rubikpi3`. |

### Kernel fragment

[`realtek-eth-8169.cfg`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006b/recipes-kernel/linux/radxa-dragon-q6a/realtek-eth-8169.cfg)
builds the Radxa board's Realtek Ethernet support into the kernel. Each line sets
a [Kconfig](https://docs.kernel.org/kbuild/kconfig-language.html) option of type
bool or tristate; an option not listed keeps the kernel configuration's value.

| Option | Value | Purpose |
| --- | --- | --- |
| `CONFIG_R8169` | `y` | Realtek 8169-family Ethernet driver. |
| `CONFIG_REALTEK_PHY` | `y` | Realtek PHY driver. |
| `CONFIG_REALTEK_PHY_HWMON` | Not set | Leaves out the PHY temperature sensor. |
| `CONFIG_PHYLIB`, `CONFIG_MDIO_BUS`, `CONFIG_FIXED_PHY` | `y` | PHY and MDIO bus support the driver uses. |
| `CONFIG_FWNODE_MDIO`, `CONFIG_OF_MDIO`, `CONFIG_ACPI_MDIO` | `y` | MDIO bus discovery from firmware descriptions. |
| `CONFIG_NET_SELFTESTS` | `y` | Network self-tests the driver can run. |

## kas fragments

Each [kas](https://kas.readthedocs.io/en/latest/userguide/project-configuration.html)
file in [`ci/`](https://github.com/devdocsorg/meta-qcom-3rdparty/tree/docs/upgrade-test-1006b/ci)
declares configuration format `version: 14`. Fragments that include `repo: meta-qcom`
files take their settings from meta-qcom's
[`ci/`](https://github.com/qualcomm-linux/meta-qcom/tree/master/ci) folder.

| File | Settings |
| --- | --- |
| `base.yml` | Includes meta-qcom's `ci/base.yml` (BitBake, OpenEmbedded-Core, `nodistro`, target `core-image-base`), takes meta-qcom from its `master` branch, and adds this layer. |
| `rubikpi3.yml`, `radxa-dragon-q6a.yml` | Include `base.yml` and set `machine`. |
| `qcom-distro.yml` | Adds meta-qcom's `ci/qcom-distro.yml`: the `qcom-distro` distribution, its layers, and its image targets. |
| `ci.yml`, `mirror.yml` | Add meta-qcom's CI build tuning and its shared-state mirror. |
| `meta-qcom.yml` | Declares the meta-qcom repository for the fragments above. |
| `linux-qcom-next.yml` | `PREFERRED_PROVIDER_virtual/kernel = "linux-qcom-next"`, a fixed assignment that overrides the machines' `?=`. |
| `world.yml` | Target `world`, with [`EXCLUDE_FROM_WORLD`](https://docs.yoctoproject.org/ref-manual/variables.html#term-EXCLUDE_FROM_WORLD) `= "1"` except for recipes from the `qcom` and `qcom-3rdparty` layers (`:layer-qcom` and `:layer-qcom-3rdparty` set to `"0"`). |

## Environment

[`.env.example`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006b/.env.example)
documents `KAS_CONTAINER`, `KAS_WORK_DIR`, `DL_DIR`, and `SSTATE_DIR`, with safe
examples and the command that loads them. kas defines the last three in its
[environment variable reference](https://kas.readthedocs.io/en/latest/userguide/env-vars.html).

## CI workflows

| Workflow | Trigger | What it does |
| --- | --- | --- |
| [pr.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006b/.github/workflows/pr.yml) | Pull requests to `main`, except Markdown-only changes | Runs `build-yocto.yml` with the `pr` profile. |
| [push.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006b/.github/workflows/push.yml) | Pushes to `main` | Runs `build-yocto.yml`. |
| [nightly-build.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006b/.github/workflows/nightly-build.yml) | Daily schedule or manual run | Runs `build-yocto.yml`, skipping inputs that already built successfully. |
| [nightly-build-wrynose.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006b/.github/workflows/nightly-build-wrynose.yml) | Daily schedule | Starts `nightly-build.yml` on `wrynose`. |
| [build-yocto.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006b/.github/workflows/build-yocto.yml) | Called by the build workflows; runs only in the `qualcomm-linux` organisation | Runs `yocto-patchreview` and `yocto-check-layer`, then builds each machine with `nodistro` and `qcom-distro` through meta-qcom's compile workflow. |
| [bitbake-lint.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006b/.github/workflows/bitbake-lint.yml) | Pull requests changing BitBake files | Reports [bitbake-lint-action](https://github.com/qualcomm-linux/bitbake-lint-action) findings on changed lines without failing. |
| [markdownlint.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006b/.github/workflows/markdownlint.yml) | Pushes to `main` and pull requests changing Markdown | Lints every Markdown file with `.github/.markdownlint.yaml`. |
| [documentation.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006b/.github/workflows/documentation.yml) | Pull requests and pushes to `main` | Builds the documentation site and checks its function reference and offline browsing. |
| [qcom-preflight-checks.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006b/.github/workflows/qcom-preflight-checks.yml) | Pull requests, pushes to `main`, manual runs | Runs Qualcomm's [preflight checks](https://github.com/qualcomm/qcom-reusable-workflows) with only the repolinter check enabled. |
| [backport.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006b/.github/workflows/backport.yml) | A pull request to `main` is merged | Opens backport pull requests for the `backport wrynose` label. |
| [stales.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006b/.github/workflows/stales.yml) | Daily schedule | Marks pull requests stale after 30 days and closes them 5 days later; issues are marked but not closed. |
| [test-pr.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006b/.github/workflows/test-pr.yml), [test.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006b/.github/workflows/test.yml), [test-distro.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006b/.github/workflows/test-distro.yml), [publish-results.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006b/.github/workflows/publish-results.yml) | After `Build on PR` completes | LAVA boot tests and result publishing; disabled until a machine has a LAVA device. |

## Repository settings

| File | Settings |
| --- | --- |
| [.markdownlint.yaml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006b/.github/.markdownlint.yaml) | `MD013: false` (no line-length limit), `MD024` with `siblings_only: true` (repeated headings allowed under different parents), `MD033: false` (inline HTML allowed), `MD041: true` (a file starts with a top-level heading). Other rules keep [markdownlint](https://github.com/DavidAnson/markdownlint)'s defaults. |
| [CODEOWNERS](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006b/.github/CODEOWNERS) | `*` assigns both maintainers to every path, documentation included. |
| [Issue templates](https://github.com/devdocsorg/meta-qcom-3rdparty/tree/docs/upgrade-test-1006b/.github/ISSUE_TEMPLATE) | Front matter `name` (required string) labels the template in GitHub's chooser; `about` (required string) says when to use it. |
| [PR template](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006b/.github/PULL_REQUEST_TEMPLATE/pr_template.md) | Selected by the `template=pr_template.md` parameter in the contribution guide's pull request link. |
| [.gitignore](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006b/.gitignore) | Ignores `.env` files except `.env.example`, the documentation tools in `.venv/`, the generated site, and its intermediates. |
