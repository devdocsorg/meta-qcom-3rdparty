# Configuration reference

[BitBake](https://github.com/openembedded/bitbake) reads the layer and machine files, kas reads the `ci/` files, and the
kernel recipe merges the configuration fragment. The
[Yocto Project variable glossary](https://docs.yoctoproject.org/dev/ref-manual/variables.html)
and the [kas configuration reference](https://kas.readthedocs.io/en/latest/userguide/project-configuration.html#configuration-reference)
define the standard settings, their types, and their defaults; this page covers
the values this layer sets and why.

BitBake applies [its assignment operators](https://docs.yoctoproject.org/bitbake/bitbake-user-manual/bitbake-user-manual-metadata.html#basic-syntax)
in parse order: `=` sets a value, `?=` sets it only if nothing has set it yet
(the first `?=` wins), `??=` is a default that any other assignment replaces,
`+=` and `.=` append, and `:append` applies after all assignments. A suffix such as
`:rubikpi3` limits a setting to that machine. kas writes `local_conf_header`
text into `local.conf`, which BitBake parses before the machine file, so a
`local.conf` value set with `=` replaces the machine file's `?=` default.

## Layer: conf/layer.conf

[conf/layer.conf](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006d/conf/layer.conf)
registers the layer with BitBake. The collection name is `qcom-3rdparty`.

| Setting | Value | Purpose | Required; behaviour when unset |
| --- | --- | --- | --- |
| [`BBPATH`](https://docs.yoctoproject.org/dev/ref-manual/variables.html#term-BBPATH) | `.= ":${LAYERDIR}"` | Lets BitBake find this layer's `conf/machine` files. | Required for the machines to be found. |
| [`BBFILES`](https://docs.yoctoproject.org/dev/ref-manual/variables.html#term-BBFILES) | `+= "${LAYERDIR}/recipes-*/*/*.bb ${LAYERDIR}/recipes-*/*/*.bbappend"` | Selects the recipes and appends two folders below each `recipes-*` folder. | Required; without it no recipe is parsed. |
| [`BBFILE_COLLECTIONS`](https://docs.yoctoproject.org/dev/ref-manual/variables.html#term-BBFILE_COLLECTIONS) | `+= "qcom-3rdparty"` | Names the layer; the name also creates the `layer-qcom-3rdparty` override that `ci/world.yml` uses. | Required. |
| [`BBFILE_PATTERN_qcom-3rdparty`](https://docs.yoctoproject.org/dev/ref-manual/variables.html#term-BBFILE_PATTERN) | `:= "^${LAYERDIR}/"` | Matches the recipe files that belong to the layer. | Required; BitBake reports an error when it is not defined. |
| [`BBFILE_PRIORITY_qcom-3rdparty`](https://docs.yoctoproject.org/dev/ref-manual/variables.html#term-BBFILE_PRIORITY) | `= "5"` | Decides which layer's recipe wins when two layers provide the same one. | Optional; unset, BitBake uses one more than the highest priority among the layer's dependencies. |
| [`LAYERDEPENDS_qcom-3rdparty`](https://docs.yoctoproject.org/dev/ref-manual/variables.html#term-LAYERDEPENDS) | `= "core qcom"` | Requires [OpenEmbedded-Core](https://github.com/openembedded/openembedded-core) and [`meta-qcom`](https://github.com/qualcomm-linux/meta-qcom). | Optional; BitBake stops with an error when a listed layer is missing. |
| [`LAYERSERIES_COMPAT_qcom-3rdparty`](https://docs.yoctoproject.org/dev/ref-manual/variables.html#term-LAYERSERIES_COMPAT) | `= "blacksail"` | Declares the Yocto Project release series (6.1) the layer supports. | Optional; unset, BitBake warns. A series the core layer does not support stops the build. |
| [`BBFILES_DYNAMIC`](https://docs.yoctoproject.org/dev/ref-manual/variables.html#term-BBFILES_DYNAMIC) | `+= "qcom-distro:${LAYERDIR}/dynamic-layers/qcom-distro/*/*/*.bb qcom-distro:${LAYERDIR}/dynamic-layers/qcom-distro/*/*/*.bbappend"` | Adds the `dynamic-layers/qcom-distro` files only when the `qcom-distro` layer from [`meta-qcom-distro`](https://github.com/qualcomm-linux/meta-qcom-distro) is in the build. | Optional. |

## Machines: conf/machine

[rubikpi3.conf](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006d/conf/machine/rubikpi3.conf)
describes the Thundercomm RUBIK Pi 3 and
[radxa-dragon-q6a.conf](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006d/conf/machine/radxa-dragon-q6a.conf)
the Radxa Dragon Q6A; both use the QCS6490 SoC. kas selects one with its
`machine:` key. Defaults come from `meta-qcom`'s
[qcom-base.inc](https://github.com/qualcomm-linux/meta-qcom/blob/b6b6e1b04ed09116936dbb5926dd830eafdc52a2/conf/machine/include/qcom-base.inc),
[qcom-common.inc](https://github.com/qualcomm-linux/meta-qcom/blob/b6b6e1b04ed09116936dbb5926dd830eafdc52a2/conf/machine/include/qcom-common.inc),
and [image_types_qcom.bbclass](https://github.com/qualcomm-linux/meta-qcom/blob/b6b6e1b04ed09116936dbb5926dd830eafdc52a2/classes-recipe/image_types_qcom.bbclass).
Every value is a string; `-` means the machine does not set it.

| Setting | rubikpi3 | radxa-dragon-q6a | Purpose | Default when unset |
| --- | --- | --- | --- | --- |
| `require conf/machine/include/qcom-qcs6490.inc` | yes | yes | Pulls in the QCS6490 SoC settings from `meta-qcom`. | Required. |
| [`PREFERRED_PROVIDER_virtual/kernel`](https://docs.yoctoproject.org/dev/ref-manual/variables.html#term-PREFERRED_PROVIDER) | `?= "linux-qcom-next"` | `?= "linux-qcom-next"` | Kernel recipe; set before the SoC include because the first `?=` wins. | `linux-qcom-next`, from qcom-base.inc. |
| [`MACHINE_FEATURES`](https://docs.yoctoproject.org/dev/ref-manual/variables.html#term-MACHINE_FEATURES) | `+= "efi pci"` | `+= "efi pci"` | Adds UEFI boot and PCI support to the SoC features. | `alsa bluetooth usbgadget usbhost wifi`, from qcom-common.inc. |
| `KERNEL_CMDLINE_EXTRA:append` | `" deferred_probe_timeout=30"` | - | Gives the HDMI bridge time to probe before the display driver gives up. | Empty; `meta-qcom`'s `ci/base.yml` adds `qcom_scm.download_mode=1`. |
| [`KERNEL_DEVICETREE`](https://docs.yoctoproject.org/dev/ref-manual/variables.html#term-KERNEL_DEVICETREE) | `"qcom/qcs6490-thundercomm-rubikpi3.dtb"` | `"qcom/qcs6490-radxa-dragon-q6a.dtb"` | Device tree the kernel builds. | Required. |
| `QCOM_DTB_DEFAULT` | `?= "qcs6490-thundercomm-rubikpi3"` | `?= "qcs6490-radxa-dragon-q6a"` | Device tree image that `qcomflash` installs as `dtb.bin`. | `multi-dtb`, a FIT image of several device trees. |
| `QCOM_BOOT_FIRMWARE` | `"firmware-qcom-boot-rubikpi3"` | `""` | Recipe whose boot firmware the `qcomflash` package includes; empty includes none. | Empty. |
| `QCOM_BOOT_FILES_SUBDIR` | `"rubikpi3"` | `""` | Deploy folder that holds the boot firmware. | Empty. |
| `QCOM_PARTITION_FILES_SUBDIR` | `?= "partitions/qcs6490-thundercomm-rubikpi3/ufs"` | `""` | Partition table files, from [`qcom-ptool`](https://github.com/qualcomm-linux/qcom-ptool) through `qcom-partition-conf`. | The `QCOM_BOOT_FILES_SUBDIR` value. |
| `QCOM_PARTITION_FILES_SUBDIR_SPINOR` | - | `""` | SPI NOR partition files; empty, as the default. | Empty. |
| `QCOM_PARTITION_CONF` | - | `""` | Partition configuration recipe; empty builds none. | `qcom-partition-conf`. |
| `QCOM_CDT_FILE` | `"RubikPi3_CDT"` | `""` | Configuration data table that `qcomflash` packages as `cdt.bin`. | Unset: no table. |
| [`WKS_FILE`](https://docs.yoctoproject.org/dev/ref-manual/variables.html#term-WKS_FILE) | - | `"efi-uki-bootdisk.wks.in"` | Disk layout: an EFI system partition with systemd-boot and a unified kernel image, then the root file system. | Unset: no disk image. |
| `QCOM_ESP_IMAGE` | - | `""` | Leaves out the separate EFI system partition image, which the disk layout replaces. | `esp-qcom-image` when `efi` is a machine feature. |
| `QCOM_VFAT_SECTOR_SIZE` | - | `?= "512"` | FAT sector size for SD cards; use `"4096"` for UFS. | `4096`. |
| `QCOM_BOOTIMG_ROOTFS` | - | `?= "PARTLABEL=root"` | Root device for the kernel command line. No effect: qcom-base.inc sets `?= "PARTLABEL=rootfs"` first. | `PARTLABEL=rootfs`. |
| [`IMAGE_FSTYPES`](https://docs.yoctoproject.org/dev/ref-manual/variables.html#term-IMAGE_FSTYPES) | - | `+= "wic.gz wic.bmap"` | Adds the compressed disk image and its block map. | `ext4 qcomflash`, from qcom-base.inc. |
| [`MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS`](https://docs.yoctoproject.org/dev/ref-manual/variables.html#term-MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS) | `+=` the SoC package groups and `packagegroup-rubikpi3-firmware` | `+=` the SoC package groups, the board firmware and DSP package groups, and `qairt-sdk-hexagon-v68` | Board firmware for every image. The SoC package groups repeat the SoC include's list. | The SoC include's list. |

Each value above is a safe example. To change a `?=` value, set it with `=` in
`local.conf`; a value the machine file sets with `=` needs a machine override,
such as `KERNEL_DEVICETREE:rubikpi3 = "..."`.

## Recipes and appends

| File | Setting | Purpose |
| --- | --- | --- |
| [packagegroup-rubikpi3.bb](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006d/recipes-bsp/packagegroups/packagegroup-rubikpi3.bb) | `PACKAGES`, `RRECOMMENDS:${PN}-firmware` | Defines `packagegroup-rubikpi3-firmware`: GPU firmware when `DISTRO_FEATURES` has `opencl`, `opengl`, or `vulkan`, then serial engine, video, audio, and compute DSP firmware. Wi-Fi and Bluetooth firmware are not in [`linux-firmware`](https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/) yet. |
| [packagegroup-radxa-dragon-q6a.bb](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006d/recipes-bsp/packagegroups/packagegroup-radxa-dragon-q6a.bb) | `PACKAGES`, `RRECOMMENDS:${PN}-firmware`, `RDEPENDS:${PN}-hexagon-dsp-binaries` | Defines the firmware group (the same GPU condition, camera, HDMI bridge, audio, compute, serial engine, and video firmware) and a separate group for the audio and compute DSP binaries. |
| [firmware-qcom-boot-rubikpi3_20260915.bb](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006d/recipes-bsp/firmware-boot/firmware-qcom-boot-rubikpi3_20260915.bb) | `SRC_URI`, `SRCREV`, `LICENSE`, `COMPATIBLE_MACHINE = "(rubikpi3)"`, `QCOM_BOOT_IMG_SUBDIR = "rubikpi3"` | Fetches the vendor's [boot-assets](https://github.com/rubikpi-ai/boot-assets) `qli2.0` branch at a fixed commit and deploys it for `rubikpi3` only; its `do_deploy` task is in the function reference. |
| [linux-qcom-next_git.bbappend](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006d/recipes-kernel/linux/linux-qcom-next_git.bbappend) | `FILESEXTRAPATHS:prepend:radxa-dragon-q6a`, `SRC_URI:append:radxa-dragon-q6a` | For `radxa-dragon-q6a` only, adds the `radxa-dragon-q6a/` folder to the file search path and the Ethernet fragment below to the kernel sources. |
| [qcom-multimedia-image.bbappend](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006d/dynamic-layers/qcom-distro/recipes-products/images/qcom-multimedia-image.bbappend) | `INCOMPATIBLE_LICENSE_EXCEPTIONS:append:rubikpi3` | Lets `qcom-multimedia-image` ship the boot firmware under `LICENSE.qcom-2` on `rubikpi3`. |

The standard settings are defined in the variable glossary:
[`SRC_URI`](https://docs.yoctoproject.org/dev/ref-manual/variables.html#term-SRC_URI),
[`FILESEXTRAPATHS`](https://docs.yoctoproject.org/dev/ref-manual/variables.html#term-FILESEXTRAPATHS), and
[`INCOMPATIBLE_LICENSE_EXCEPTIONS`](https://docs.yoctoproject.org/dev/ref-manual/variables.html#term-INCOMPATIBLE_LICENSE_EXCEPTIONS).

### Kernel fragment: realtek-eth-8169.cfg

The `linux-qcom-next` recipe merges
[realtek-eth-8169.cfg](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006d/recipes-kernel/linux/radxa-dragon-q6a/realtek-eth-8169.cfg)
into the kernel configuration for the Radxa Dragon Q6A's Realtek Ethernet. The
types and defaults come from the Kconfig files of
[`kernel`](https://github.com/qualcomm-linux/kernel) at the revision the recipe pins,
e428097a.

| Option | Value | Kconfig type and default | Purpose |
| --- | --- | --- | --- |
| `CONFIG_R8169` | `y` | tristate, `n`; needs PCI | Realtek 8169/8168/8101/8125 Ethernet driver. |
| `CONFIG_NET_SELFTESTS` | `y` | tristate that follows `PHYLIB` | Network self-tests. |
| `CONFIG_MDIO_BUS` | `y` | No such option at this revision, so the line has no effect. | - |
| `CONFIG_PHYLIB` | `y` | tristate, `n` | PHY device support. |
| `CONFIG_FIXED_PHY` | `y` | tristate, `n` | Fixed-link PHY emulation. |
| `CONFIG_REALTEK_PHY` | `y` | tristate, `n` | Realtek PHY driver. |
| `CONFIG_REALTEK_PHY_HWMON` | not set | bool, `n` | Leaves out the Realtek PHY temperature sensor. |
| `CONFIG_FWNODE_MDIO` | `y` | tristate that follows `ACPI` or `OF` | Firmware-node MDIO accessors. |
| `CONFIG_OF_MDIO` | `y` | tristate that follows `OF` | Device-tree MDIO accessors. |
| `CONFIG_ACPI_MDIO` | `y` | tristate that follows `ACPI` | ACPI MDIO accessors. |

## Build configurations: ci/

kas reads these files; their keys are defined in the
[kas configuration reference](https://kas.readthedocs.io/en/latest/userguide/project-configuration.html#configuration-reference).
Every file sets `header.version: 14`, the kas configuration format version.

| File | Settings | Purpose |
| --- | --- | --- |
| [base.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006d/ci/base.yml) | `includes` `meta-qcom`'s `ci/base.yml`; `repos` `meta-qcom` (URL, `master`) and `meta-qcom-3rdparty` (no URL: this checkout) | Common build: `meta-qcom`'s base file adds OpenEmbedded-Core and BitBake, `nodistro`, and the `core-image-base` target. |
| [rubikpi3.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006d/ci/rubikpi3.yml), [radxa-dragon-q6a.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006d/ci/radxa-dragon-q6a.yml) | `includes` `ci/base.yml`; `machine` | One file per board. |
| [qcom-distro.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006d/ci/qcom-distro.yml) | `includes` `ci/meta-qcom.yml` and `meta-qcom`'s `ci/qcom-distro.yml` | Switches to the `qcom-distro` distribution with its layers and image targets. |
| [ci.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006d/ci/ci.yml), [mirror.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006d/ci/mirror.yml) | `includes` `ci/meta-qcom.yml` and the matching `meta-qcom` file | CI build settings, and the Yocto Project shared-state mirror. |
| [meta-qcom.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006d/ci/meta-qcom.yml) | `repos` `meta-qcom` (URL, `master`) | Declares `meta-qcom` for the files that include from it. |
| [linux-qcom-next.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006d/ci/linux-qcom-next.yml) | `local_conf_header` `kernelprovider` | Sets `PREFERRED_PROVIDER_virtual/kernel = "linux-qcom-next"`. |
| [world.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006d/ci/world.yml) | `local_conf_header` `world_build`; `target: world` | Limits the `world` target to the recipes in the `qcom` and `qcom-3rdparty` layers. |

## Environment

[.env.example](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006d/.env.example)
documents the `KAS_CONTAINER`, `KAS_WORK_DIR`, `DL_DIR`, and `SSTATE_DIR`
settings that `kas-container` and `ci/kas-container-shell-helper.sh` read, and
the command that loads them.

## Repository checks

| File | Setting | Purpose |
| --- | --- | --- |
| [.markdownlint.yaml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006d/.github/.markdownlint.yaml) | `MD013: false`, `MD024: siblings_only`, `MD033: false`, `MD041: true` | Allows long lines, repeated headings in different sections, and inline HTML; requires a top-level heading first. Other [markdownlint rules](https://github.com/DavidAnson/markdownlint#rules--aliases) keep their defaults. |
| [CODEOWNERS](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006d/.github/CODEOWNERS) | `*  @ricardosalveti @ndechesne` | Makes both maintainers code owners of every path, documentation included. |

### Workflows

| Workflow | Trigger | What it does |
| --- | --- | --- |
| [backport.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006d/.github/workflows/backport.yml) | A pull request merged into `main` | Opens backport pull requests for the `backport wrynose` label. |
| [bitbake-lint.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006d/.github/workflows/bitbake-lint.yml) | Pull requests that change BitBake files outside `.github/` and `ci/` | Lints the changed files with [bitbake-lint-action](https://github.com/qualcomm-linux/bitbake-lint-action) without failing the check. |
| [build-yocto.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006d/.github/workflows/build-yocto.yml) | Called by the build workflows | Runs `yocto-patchreview` and `yocto-check-layer`, and builds both machines with and without `qcom-distro`. Runs only in the `qualcomm-linux` organisation. |
| [pr.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006d/.github/workflows/pr.yml) | Pull requests to `main` that change files other than Markdown and `.markdownlint.yaml` | Runs the build. |
| [push.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006d/.github/workflows/push.yml) | Pushes to `main` | Runs the build. |
| [nightly-build.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006d/.github/workflows/nightly-build.yml) | Daily, or by hand | Runs the build unless the same inputs already built successfully. |
| [nightly-build-wrynose.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006d/.github/workflows/nightly-build-wrynose.yml) | Daily | Starts the nightly build on `wrynose`. |
| [markdownlint.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006d/.github/workflows/markdownlint.yml) | Pull requests and pushes to `main` that change Markdown | Lints every Markdown file with `.markdownlint.yaml`. |
| [qcom-preflight-checks.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006d/.github/workflows/qcom-preflight-checks.yml) | Pull requests, pushes to `main`, or by hand | Runs [qcom-reusable-workflows](https://github.com/qualcomm/qcom-reusable-workflows)' preflight checks with only the repository linter enabled. |
| [documentation.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006d/.github/workflows/documentation.yml) | Pull requests and pushes to `main` | Builds this site and checks its function reference and offline browsing. |
| [stales.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006d/.github/workflows/stales.yml) | Daily | Marks inactive issues and pull requests stale, then closes stale pull requests. |
| [test-pr.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006d/.github/workflows/test-pr.yml), [test.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006d/.github/workflows/test.yml), [test-distro.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006d/.github/workflows/test-distro.yml), [publish-results.yml](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006d/.github/workflows/publish-results.yml) | After a pull request build | Runs boot tests in LAVA and publishes the results; no machine has a LAVA device yet, so the tests do not run. |
