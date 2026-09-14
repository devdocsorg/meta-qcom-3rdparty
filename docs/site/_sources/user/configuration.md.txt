# Configuration

## Host paths

`.env.example` documents the optional `KAS_CONTAINER`, `KAS_WORK_DIR`, `DL_DIR`,
and `SSTATE_DIR` strings, their defaults, and example paths. Source it explicitly
as shown in the [tutorial](../contributing/usage.md). The example retains existing environment
values and keeps build output and caches outside the checkout.

## Layer and recipe settings

BitBake stores variables as strings. `=` assigns a value; `?=` supplies a default
only when unset; `:=` expands immediately; `+=` appends with a space; `.=` and
`=.` append and prepend without a separator. `:append` and `:prepend` concatenate
at expansion time. A machine suffix scopes an assignment to that machine.
Omitted settings retain values from the selected layers and classes, so defaults
vary by machine and release. Empty strings explicitly clear inherited values.
`require` loads a mandatory file; `inherit` applies the named classes.

The table gives each setting's purpose, interpreted type, and an example from
this layer. Current assignments and overrides remain in the source files.

| Setting | Purpose and interpreted type | Example |
| --- | --- | --- |
| `BBPATH` | Colon-separated search path for layer configuration and classes. | `:${LAYERDIR}` |
| `BBFILES` | Space-separated recipe and append path globs. | `${LAYERDIR}/recipes-*/*/*.bb` |
| `BBFILE_COLLECTIONS` | Space-separated names identifying this layer collection. | `qcom-3rdparty` |
| `BBFILE_PATTERN_qcom-3rdparty` | Regular expression matching files belonging to this layer. | `^${LAYERDIR}/` |
| `BBFILE_PRIORITY_qcom-3rdparty` | Integer priority used to order competing recipes. | `5` |
| `LAYERDEPENDS_qcom-3rdparty` | Space-separated required layer collection names. | `core qcom` |
| `LAYERSERIES_COMPAT_qcom-3rdparty` | Space-separated compatible Yocto release codenames. | `wrynose` |
| `BBFILES_DYNAMIC` | Collection-qualified recipe globs, enabled only when that layer is present. | `qcom-distro:${LAYERDIR}/dynamic-layers/qcom-distro/*/*/*.bbappend` |
| `MACHINE_FEATURES` | Space-separated hardware capabilities exposed to recipes. | `efi pci` |
| `KERNEL_DEVICETREE` | Space-separated device-tree build targets. | `qcom/qcs6490-radxa-dragon-q6a.dtb` |
| `PREFERRED_PROVIDER_virtual/kernel` | Recipe-name string selecting the kernel provider. | `linux-qcom-next` |
| `QCOM_BOOT_FIRMWARE` | Recipe-name string supplying boot firmware; empty disables it. | `""` |
| `QCOM_BOOT_FILES_SUBDIR` | Relative path string for boot firmware; empty disables packaging. | `""` |
| `QCOM_PARTITION_FILES_SUBDIR` | Relative path string for partition metadata; empty disables it. | `""` |
| `QCOM_PARTITION_FILES_SUBDIR_SPINOR` | Relative path string for SPI NOR partition metadata; empty disables it. | `""` |
| `QCOM_PARTITION_CONF` | Partition configuration path string; empty disables it. | `""` |
| `QCOM_CDT_FILE` | CDT filename string; empty disables the selected CDT. | `""` |
| `WKS_FILE` | Wic kickstart filename string selecting the disk image layout. | `efi-uki-bootdisk.wks.in` |
| `QCOM_ESP_IMAGE` | Recipe-name string for a separate ESP image; empty uses no separate recipe. | `""` |
| `QCOM_VFAT_SECTOR_SIZE` | Integer sector size in bytes for FAT image creation. | `512` |
| `QCOM_BOOTIMG_ROOTFS` | String identifying the kernel root filesystem device or label. | `PARTLABEL=root` |
| `QCOM_DTB_DEFAULT` | Default board DTB basename string, without the .dtb suffix. | `qcs6490-radxa-dragon-q6a` |
| `IMAGE_FSTYPES` | Space-separated output image format names. | `wic wic.gz wic.bmap` |
| `MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS` | Space-separated recommended machine runtime packages. | `packagegroup-rubikpi3-firmware` |
| `KERNEL_CMDLINE_EXTRA` | Space-separated additional kernel command-line arguments. | `deferred_probe_timeout=30` |
| `INCOMPATIBLE_LICENSE_EXCEPTIONS` | Space-separated package:licence exceptions for the selected machine. | `firmware-qcom-boot-rubikpi3:LicenseRef-LICENSE.qcom-2` |
| `SUMMARY` | Short package description string. | `Boot firmware for Thundercomm RUBIK Pi 3` |
| `DESCRIPTION` | Detailed package description string. | `Qualcomm-signed SoC boot firmware and Rubik Pi 3-specific LUN 6  payloads from rubikpi-ai/boot-assets.` |
| `LICENSE` | SPDX expression or source-supplied licence identifier string. | `LicenseRef-LICENSE.qcom-2` |
| `LIC_FILES_CHKSUM` | Space-separated licence file URLs and expected checksums. | `file://LICENSE.txt;md5=165287851294f2fb8ac8cbc5e24b02b0` |
| `SRC_URI` | Space-separated source URLs and local files, with fetcher parameters. | `git://github.com/rubikpi-ai/boot-assets;protocol=https;branch=main;destsuffix=${BP}` |
| `SRCREV` | Git revision string selecting the source commit. | `10b868574aa4d06fb3836399d10eb5c792765504` |
| `INHIBIT_DEFAULT_DEPS` | Boolean string (0/1) disabling the usual default build dependencies. | `1` |
| `QCOM_BOOT_IMG_SUBDIR` | Relative deployment subdirectory string for boot images. | `rubikpi3` |
| `COMPATIBLE_MACHINE` | Regular expression limiting the recipe to matching machine overrides. | `(rubikpi3)` |
| `PACKAGES` | Space-separated output package names. | `${PN}-firmware` |
| `RRECOMMENDS` | Space-separated optional runtime packages for the named output package. | `linux-firmware-qcom-vpu` |
| `RDEPENDS` | Space-separated required runtime packages for the named output package. | `hexagon-dsp-binaries-radxa-dragon-q6a-adsp` |
| `FILESEXTRAPATHS` | Colon-separated additional search paths for recipe files. | `${THISDIR}/${BPN}:` |

`SRC_URI` fetcher parameters are strings: `protocol=https` chooses transport,
`branch=main` validates the selected Git branch, and `destsuffix=${BP}` names
the checkout directory. `LIC_FILES_CHKSUM` lists licence paths and expected
MD5 checksums; use the actual source checksum, not an arbitrary example.
`do_configure[noexec]` and `do_compile[noexec]` are boolean-string task flags:
`"1"` skips the task body; omission leaves normal task execution enabled.
`addtask deploy before do_build after do_install` declares task ordering.

Inspect an effective value with `bitbake-getvar VARIABLE` or
`bitbake-getvar -r RECIPE VARIABLE` inside the configured build shell.

## kas fragments

| Key | Type, purpose, and default behaviour | Example |
| --- | --- | --- |
| `header.version` | Required integer schema version | `14` |
| `header.includes` | Optional list of local paths or repository/file mappings; absent adds no includes | `ci/base.yml` |
| `header.includes[].repo`, `.file` | Required strings for an external include: repository name and relative path | `meta-qcom`, `ci/base.yml` |
| `repos.*.url`, `.branch` | Git URL and branch strings; remote URL is required, branch may use kas defaults | `https://github.com/qualcomm-linux/meta-qcom`, `master` |
| `repos.meta-qcom-3rdparty` | Null entry selecting this working checkout | No remote URL |
| `machine` | Machine-name string; base value is `unset` until a board fragment selects it | `radxa-dragon-q6a` |
| `local_conf_header` | Optional mapping of names to BitBake configuration strings; absent adds no local settings | `kernelprovider` selects `linux-qcom-next` |
| `target` | List of BitBake targets; inherited through includes | `core-image-base`; `world.yml` selects `world` |

`world.yml` sets `EXCLUDE_FROM_WORLD` to string `"1"` globally and `"0"` for
`layer-qcom` and `layer-qcom-3rdparty`. Without that fragment, inherited inclusion
settings apply. `kas-container dump` shows the final merged configuration.

## Kernel and documentation settings

The README beside the kernel `.cfg` documents each requested symbol. The kernel
validates these requests; omitted symbols retain defconfig or earlier settings.

[conf.py](../conf.py) documents optional Sphinx settings and generates reference
pages from source comments using shdoc. [requirements.txt](../requirements.txt)
pins the Python build dependencies. The repository's
[documentation build instructions](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/devdocs/required-files-sphinx/docs/README.md#build-the-documentation)
pin the shdoc executable.
