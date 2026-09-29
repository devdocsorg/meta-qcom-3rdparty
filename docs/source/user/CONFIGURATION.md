# Configuration reference

The layer's settings are BitBake metadata and kas files that decide how images
are built. The tables list each local choice with its type, what applies when it
is absent, and the value used here, which is also a safe example. The
[Yocto Project variable glossary][glossary] defines the standard variables, and
the [BitBake manual][syntax] defines the assignment operators.

## How settings combine

- kas merges the files named on its command line, left to right, with their
  `includes`; later values override earlier ones ([kas project configuration][kas]).
- kas writes `local_conf_header` entries to `build/conf/local.conf` and sets
  `MACHINE` from `machine`, which loads `conf/machine/<machine>.conf`.
- BitBake reads `local.conf` before the machine configuration. A `=` there
  overrides a machine's `?=`. Within the machine configuration and its includes,
  the first `?=` wins, `??=` applies only when nothing else assigns the variable,
  and `+=` or `:append` add to the inherited value.

## Environment

[.env.example][env] documents `KAS_CONTAINER`, `KAS_WORK_DIR`, `DL_DIR`, and
`SSTATE_DIR`: optional paths that `kas-container` and the CI helper scripts read
([kas environment variables][kas-env]). Nothing loads the file.

## Layer

[conf/layer.conf][layer] registers the layer with BitBake.

| Setting | Value | Purpose and type | When absent |
| --- | --- | --- | --- |
| `BBPATH .=` | `:${LAYERDIR}` | Colon-separated search path for `conf/` and classes. | The machines are not found. |
| `BBFILES +=` | `${LAYERDIR}/recipes-*/*/*.bb` and `.bbappend` | Space-separated globs of recipes and appends to parse. | The recipes are not parsed. |
| `BBFILE_COLLECTIONS +=` | `qcom-3rdparty` | Collection name used by the settings below. | The layer has no collection. |
| `BBFILE_PATTERN_qcom-3rdparty :=` | `^${LAYERDIR}/` | Regular expression matching the layer's files. | BitBake reports an error. |
| `BBFILE_PRIORITY_qcom-3rdparty` | `5` | Integer; the higher priority wins when layers provide the same recipe. | BitBake derives a priority from the dependencies. |
| `LAYERDEPENDS_qcom-3rdparty` | `core qcom` | Collections that must be present: [OpenEmbedded-Core][oe-core] and [meta-qcom][mq]. | No dependency check. |
| `LAYERSERIES_COMPAT_qcom-3rdparty` | `wrynose` | Release series the layer supports; BitBake stops when the core layer is another series. The Bitbake Lint workflow reads it too. | BitBake warns. |
| `BBFILES_DYNAMIC +=` | `qcom-distro:` globs under `dynamic-layers/qcom-distro/` | Parses those files only when the `qcom-distro` collection is present. | Those files are never parsed. |

## Machines

Each machine configuration requires the [QCS6490 SoC include][soc] from [meta-qcom][mq],
which requires [qcom-base.inc][base] and [qcom-common.inc][common]. The
[qcomflash image type][qcomflash] reads the `QCOM_*` image settings.
[rubikpi3.conf][rubikpi3] and [radxa-dragon-q6a.conf][radxa] set:

| Setting | `rubikpi3` | `radxa-dragon-q6a` | Purpose, type, and value when unset |
| --- | --- | --- | --- |
| `PREFERRED_PROVIDER_virtual/kernel ?=` | `linux-qcom-next`, before the SoC include | `linux-qcom-next`, after it | Kernel recipe name. `qcom-base.inc` sets the same `?=` default, so the later assignment has no effect. |
| `MACHINE_FEATURES +=` | `efi pci` | `efi pci` | Space-separated features added to `alsa bluetooth usbgadget usbhost wifi`: UEFI boot and PCIe. |
| `KERNEL_CMDLINE_EXTRA:append` | `deferred_probe_timeout=30` | — | Kernel arguments; gives the HDMI bridge time to probe. Unset: the kernel's default timeout. |
| `KERNEL_DEVICETREE` | `qcom/qcs6490-thundercomm-rubikpi3.dtb` | `qcom/qcs6490-radxa-dragon-q6a.dtb` | Space-separated device trees to build. Required. |
| `QCOM_DTB_DEFAULT ?=` | `qcs6490-thundercomm-rubikpi3` | `qcs6490-radxa-dragon-q6a` | Device tree name for the boot image. Unset: `multi-dtb`, a FIT image of all device trees. |
| `QCOM_BOOT_FIRMWARE` | `firmware-qcom-boot-rubikpi3` | `""` | Recipe whose boot firmware the image packages. Unset or empty: none. |
| `QCOM_BOOT_FILES_SUBDIR` | `rubikpi3` | `""` | Deploy subdirectory holding that firmware. Unset: `""`. |
| `QCOM_PARTITION_FILES_SUBDIR` | `?= partitions/qcs6490-thundercomm-rubikpi3/ufs` | `""` | Deploy subdirectory of the partition tables, which `qcom-partition-conf` builds with `qcom-ptool`. Unset: `QCOM_BOOT_FILES_SUBDIR`. |
| `QCOM_PARTITION_FILES_SUBDIR_SPINOR` | — | `""` | Same for SPI NOR. Unset: `""`. |
| `QCOM_PARTITION_CONF` | — | `""` | Recipe that deploys the partition tables; empty disables it. Unset: `qcom-partition-conf`. |
| `QCOM_CDT_FILE` | `RubikPi3_CDT` | `""` | Base name of the CDT binary packaged as `cdt.bin`. Unset: no CDT. |
| `WKS_FILE` | — | `efi-uki-bootdisk.wks.in` | [OpenEmbedded-Core][oe-core] kickstart file for an ESP with systemd-boot and a UKI, plus the root file system. Unset: `<image>.<machine>.wks`. |
| `QCOM_ESP_IMAGE` | — | `""` | Separate ESP image recipe; empty because the disk image creates the ESP. Unset: `esp-qcom-image` with the `efi` feature. |
| `QCOM_VFAT_SECTOR_SIZE ?=` | — | `512` | FAT sector size in bytes: 512 for SD cards. Unset: `4096`, for UFS. |
| `QCOM_BOOTIMG_ROOTFS ?=` | — | `PARTLABEL=root` | Root device for the kernel command line. `qcom-base.inc` sets `PARTLABEL=rootfs` with an earlier `?=`, which wins. |
| `IMAGE_FSTYPES +=` | — | `wic wic.gz wic.bmap` | Image types added to `ext4 qcomflash`. |
| `MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS +=` | SoC packagegroups and `packagegroup-rubikpi3-firmware` | SoC packagegroups, the board's firmware and DSP packagegroups, and `qairt-sdk-hexagon-v68` | Packages every image recommends. The two SoC packagegroups repeat the SoC include's list. |

The Radxa Dragon Q6A boots from firmware in SPI NOR that Yocto does not build,
so its configuration blanks the boot firmware, partition, and CDT settings and
leaves `PREFERRED_PROVIDER_virtual/bootloader` unset.

## Kernel configuration fragment

For `radxa-dragon-q6a`, [linux-qcom-next_git.bbappend][kappend] adds
[realtek-eth-8169.cfg][kcfg] to the kernel configuration for the board's
Realtek Ethernet ([configuration fragments][fragments], [Kconfig types][kconfig]).
An option the fragment does not set keeps the kernel's default configuration.

| Options | Value | Purpose |
| --- | --- | --- |
| `CONFIG_R8169`, `CONFIG_REALTEK_PHY` | `y` | Build in the Realtek Ethernet and PHY drivers. |
| `CONFIG_PHYLIB`, `CONFIG_MDIO_BUS`, `CONFIG_FIXED_PHY`, `CONFIG_FWNODE_MDIO`, `CONFIG_OF_MDIO`, `CONFIG_ACPI_MDIO` | `y` | Build in the PHY and MDIO support those drivers use. |
| `CONFIG_NET_SELFTESTS` | `y` | Build in the network self-tests the PHY library offers. |
| `CONFIG_REALTEK_PHY_HWMON` | not set | Leave out the Realtek PHY temperature sensor. |

## kas fragments

Every file declares kas configuration format `version: 14`; the
`yaml-language-server` comment points editors at the kas schema.

| File | Sets |
| --- | --- |
| [base.yml][ci] | Includes `ci/base.yml` from [meta-qcom][mq] ([OpenEmbedded-Core][oe-core], [BitBake][bitbake], no distribution, target `core-image-base`) and adds [meta-qcom][mq] on `master` and this layer. |
| [rubikpi3.yml][ci], [radxa-dragon-q6a.yml][ci] | Include `base.yml` and set `machine`. |
| [meta-qcom.yml][ci] | Declares [meta-qcom][mq] on `master` for the fragments below. |
| [ci.yml][ci], [mirror.yml][ci], [qcom-distro.yml][ci] | Include the same-named [meta-qcom][mq] fragment: CI build settings, the shared-state mirror, or the Qualcomm Linux distribution with its layers and images. |
| [linux-qcom-next.yml][ci] | `PREFERRED_PROVIDER_virtual/kernel = "linux-qcom-next"` in `local.conf`. |
| [world.yml][ci] | `EXCLUDE_FROM_WORLD = "1"`, with `"0"` for `layer-qcom` and `layer-qcom-3rdparty`, and target `world`: builds every recipe of [meta-qcom][mq] and this layer. |

## Recipes and appends

| File | Local choices |
| --- | --- |
| [linux-qcom-next_git.bbappend][kappend] | Prepends `linux-qcom-next/`, which the layer does not have, to `FILESEXTRAPATHS`; for `radxa-dragon-q6a`, prepends `radxa-dragon-q6a/` and adds the fragment above to `SRC_URI`. |
| [qcom-multimedia-image.bbappend][image] | For `rubikpi3`, allows `firmware-qcom-boot-rubikpi3`'s `LicenseRef-LICENSE.qcom-2` licence in `qcom-multimedia-image` through `INCOMPATIBLE_LICENSE_EXCEPTIONS`. Parsed only with [meta-qcom-distro][mqd]. |
| [firmware-qcom-boot-rubikpi3_20260621.bb][fw] | Fetches [rubikpi-ai/boot-assets](https://github.com/rubikpi-ai/boot-assets) at the pinned `SRCREV`; skips default dependencies, configure, and compile because it only copies binaries; deploys to `QCOM_BOOT_IMG_SUBDIR = "rubikpi3"`, which must match the machine's `QCOM_BOOT_FILES_SUBDIR`; `COMPATIBLE_MACHINE` limits it to `rubikpi3`. |
| [packagegroup-rubikpi3.bb][pg], [packagegroup-radxa-dragon-q6a.bb][pg] | `PACKAGES` names the firmware packagegroup, and for Radxa the DSP one; the Adreno GPU firmware is recommended only when `DISTRO_FEATURES` has `opencl`, `opengl`, or `vulkan`. |

## CI workflows

| Workflow | Trigger and check |
| --- | --- |
| [backport.yml][wf] | A merged `main` pull request labelled `backport wrynose`: opens the backport pull request. |
| [bitbake-lint.yml][wf] | Pull requests changing BitBake files outside `.github/` and `ci/`: lints the changed lines without failing. |
| [build-yocto.yml][wf] | Called by the build workflows: kas lock, the CI helper checks, and builds of each machine with and without `qcom-distro`. Runs only in `qualcomm-linux`. |
| [pr.yml][wf], [push.yml][wf] | Pull requests to `main` that change more than Markdown, and pushes to `main`: the Yocto build. |
| [nightly-build.yml][wf], [nightly-build-wrynose.yml][wf] | Daily, and `nightly-build.yml` on demand: the Yocto build on `main` and `wrynose`, skipped when the same inputs already built. |
| [test-pr.yml][wf], [test.yml][wf], [test-distro.yml][wf], [publish-results.yml][wf] | LAVA boot tests and result publishing, disabled while no machine in the layer has a lab device. |
| [markdownlint.yml][wf] | Markdown changes on pull requests and `main`: markdownlint with [.markdownlint.yaml][mdl]. |
| [qcom-preflight-checks.yml][wf] | Pull requests, pushes to `main`, or manual: Qualcomm's preflight checks, of which only repolinter is enabled. |
| [stales.yml][wf] | Daily: marks inactive issues and pull requests stale and closes stale pull requests. |
| [documentation.yml][wf] | Pull requests and pushes to `main`: the documentation setup and check targets. |

[.markdownlint.yaml][mdl] turns off the line-length (MD013) and inline HTML
(MD033) rules, allows repeated headings that are not siblings (MD024), and
requires a top-level heading first (MD041). [CODEOWNERS][owners] makes the
maintainers the reviewers of every path.

[glossary]: https://docs.yoctoproject.org/6.0/ref-manual/variables.html
[mq]: https://github.com/qualcomm-linux/meta-qcom
[mqd]: https://github.com/qualcomm-linux/meta-qcom-distro
[oe-core]: https://github.com/openembedded/openembedded-core
[bitbake]: https://github.com/openembedded/bitbake
[syntax]: https://docs.yoctoproject.org/bitbake/2.18/bitbake-user-manual/bitbake-user-manual-metadata.html#basic-syntax
[kas]: https://kas.readthedocs.io/en/4.8.2/userguide/project-configuration.html
[kas-env]: https://kas.readthedocs.io/en/4.8.2/command-line.html#environment-variables
[fragments]: https://docs.yoctoproject.org/6.0/kernel-dev/common.html#creating-configuration-fragments
[kconfig]: https://www.kernel.org/doc/html/latest/kbuild/kconfig-language.html
[soc]: https://github.com/qualcomm-linux/meta-qcom/blob/87cec8c808e319afe843ca146c3ec0b90fb0baa8/conf/machine/include/qcom-qcs6490.inc
[base]: https://github.com/qualcomm-linux/meta-qcom/blob/87cec8c808e319afe843ca146c3ec0b90fb0baa8/conf/machine/include/qcom-base.inc
[common]: https://github.com/qualcomm-linux/meta-qcom/blob/87cec8c808e319afe843ca146c3ec0b90fb0baa8/conf/machine/include/qcom-common.inc
[qcomflash]: https://github.com/qualcomm-linux/meta-qcom/blob/87cec8c808e319afe843ca146c3ec0b90fb0baa8/classes-recipe/image_types_qcom.bbclass
[env]: https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/.env.example
[layer]: https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/conf/layer.conf
[rubikpi3]: https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/conf/machine/rubikpi3.conf
[radxa]: https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/conf/machine/radxa-dragon-q6a.conf
[kappend]: https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/recipes-kernel/linux/linux-qcom-next_git.bbappend
[kcfg]: https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/recipes-kernel/linux/radxa-dragon-q6a/realtek-eth-8169.cfg
[ci]: https://github.com/devdocsorg/meta-qcom-3rdparty/tree/docs/layer-documentation/ci
[image]: https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/dynamic-layers/qcom-distro/recipes-products/images/qcom-multimedia-image.bbappend
[fw]: https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/recipes-bsp/firmware-boot/firmware-qcom-boot-rubikpi3_20260621.bb
[pg]: https://github.com/devdocsorg/meta-qcom-3rdparty/tree/docs/layer-documentation/recipes-bsp/packagegroups
[wf]: https://github.com/devdocsorg/meta-qcom-3rdparty/tree/docs/layer-documentation/.github/workflows
[mdl]: https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/.github/.markdownlint.yaml
[owners]: https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/.github/CODEOWNERS
