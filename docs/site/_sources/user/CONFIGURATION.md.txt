# Configuration reference

## Loading and precedence

This is a Yocto layer, not a standalone application. It does not load `.env`.
Export shell settings explicitly; the {download}`safe environment example <../../../.env.example>`
is an offline attachment for the [development walkthrough](../contributing/DEVELOPMENT.md).
`KAS_YAMLS` is an example variable consumed by the command that expands it, not a
setting implicitly read by kas.

kas processes the selected YAML fragments and their `header.includes`; later
configuration merges can override earlier settings. `ci/base.yml` imports
`meta-qcom/ci/base.yml`. The `meta-qcom` repository uses `master`; the local layer
entry uses the current checkout. Optional distro/CI/mirror fragments import their
counterparts from that same parent layer. Upstream defaults therefore depend on
the resolved parent revision. Record layer SHAs for repeatable product builds.

BitBake reads `conf/layer.conf`, then the selected machine and inherited recipe or
class settings. `=` assigns a string; `?=` sets the first weak default if unset;
`+=` appends a space-separated value; `.=` concatenates; `:=` expands immediately;
`:append` and `:prepend` apply at expansion. Machine overrides confine changes to
the named board. `${...}` expands variables; `${@...}` calls upstream Python and
contains no local function definition here. See the
[BitBake metadata syntax](https://docs.yoctoproject.org/bitbake/dev/bitbake-user-manual/bitbake-user-manual-metadata.html#basic-syntax).

## Environment and CI script settings

| Setting | Type, purpose, default/unset behaviour | Safe example |
| --- | --- | --- |
| `KAS_CONTAINER` | Optional executable path; helper searches PATH when unset. | `/home/user/.local/bin/kas-container` |
| `KAS_WORK_DIR` | Optional absolute work directory; kas otherwise uses its current directory. Keep outside checkout. | `/home/user/.cache/meta-qcom-3rdparty/work` |
| `DL_DIR` | Optional absolute download-cache path; inherits parent BitBake default when unset. | `/home/user/.cache/meta-qcom-3rdparty/downloads` |
| `SSTATE_DIR` | Optional absolute shared-state cache path; inherits parent default when unset. | `/home/user/.cache/meta-qcom-3rdparty/sstate-cache` |
| `KAS_YAMLS` | Optional colon-separated example input list; no implicit loading. | `ci/rubikpi3.yml:ci/qcom-distro.yml` |
| `REPO_DIR`, `WORK_DIR` | Required path arguments to the CI scripts; empty/missing paths fail. The helper supplies `/repo` and `/work`. | `/repo`, `/work` |
| `TOPDIR`, `SCRIPT` | Internal resolved paths in the shell helper; derived from its own location and first argument, not user defaults. | `/repo`, `ci/yocto-patchreview.sh` |
| `BUILDDIR` | Check-layer's temporary directory, created under `WORK_DIR`; no user setting in this script. | `/work/build-yocto-check-layer-XXXX` |
| `BUILDSTATS`, `CMD`, `PATH` | Buildstats script selects the latest BitBake stats directory, assembles chart/summary commands, and extends PATH with parent `pybootchartgui`; no override interface. | `/work/build/tmp/buildstats/20260901` |

## kas fragments

The [CI folder](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/offline-layer-guides/ci/README.md)
links each maintained fragment and script.

| Setting / files | Type, purpose, and default | Safe value |
| --- | --- | --- |
| `header.version` / every YAML | Required integer schema version. | `14` |
| `header.includes` / base | List of `{repo, file}` mappings importing the parent base composition. | `repo: meta-qcom`, `file: ci/base.yml` |
| `header.includes` / ci, mirror, qcom-distro | Ordered list of local `ci/meta-qcom.yml`, then the corresponding parent file. Optional fragments apply only when selected. | `file: ci/qcom-distro.yml` |
| `header.includes` / machine fragments | List of local paths importing the base configuration. | `ci/base.yml` |
| `repos.meta-qcom.url`, `.branch` | Required repository URL and branch in base/meta-qcom fragments; upstream default is explicitly `master`. | `https://github.com/qualcomm-linux/meta-qcom`, `master` |
| `repos.meta-qcom-3rdparty` | Null mapping uses the current checkout; do not invent a remote default. | Empty YAML value |
| `machine` | Required board string in the selected machine fragment. | `rubikpi3` or `radxa-dragon-q6a` |
| `local_conf_header.kernelprovider` | Optional literal block overriding the kernel provider when `ci/linux-qcom-next.yml` is selected. | `PREFERRED_PROVIDER_virtual/kernel = "linux-qcom-next"` |
| `local_conf_header.world_build` | Optional literal block excluding all recipes from world, then enabling qcom and qcom-3rdparty layer overrides. | `EXCLUDE_FROM_WORLD = "1"`, both layer overrides `"0"` |
| `target` / world | List of build targets, set to `world` by this fragment; otherwise inherits the base. | `world` |

The YAML language-server comment selects kas's upstream schema for editors and
does not affect a build.

## Layer settings

| Setting | Type, purpose, and default | Safe value |
| --- | --- | --- |
| `BBPATH` | Path string concatenated with the layer directory for metadata lookup. Required. | `:${LAYERDIR}` |
| `BBFILES` | Glob list appended for layer recipes and appends. Required. | `${LAYERDIR}/recipes-*/*/*.bb` and `*.bbappend` |
| `BBFILE_COLLECTIONS` | Collection-name list, appended. | `qcom-3rdparty` |
| `BBFILE_PATTERN_qcom-3rdparty` | Immediately expanded regular expression for this collection. | `^${LAYERDIR}/` |
| `BBFILE_PRIORITY_qcom-3rdparty` | Integer encoded as string; explicit priority. | `5` |
| `LAYERDEPENDS_qcom-3rdparty` | Required collection names; missing dependencies fail configuration. | `core qcom` |
| `LAYERSERIES_COMPAT_qcom-3rdparty` | Supported release-name list. | `wrynose` |
| `BBFILES_DYNAMIC` | Conditional collection/glob list; adds dynamic recipes only when qcom-distro is present. | `qcom-distro:${LAYERDIR}/dynamic-layers/qcom-distro/*/*/*.bbappend` |

## Machine settings

Both machines require `conf/machine/include/qcom-qcs6490.inc` from `meta-qcom`.
The included file supplies the SoC defaults before board overrides, except the
RUBIK Pi kernel provider, which is deliberately set before the include.
The [machine files](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/offline-layer-guides/conf/machine/README.md)
contain exact values; all values below are strings or space-separated lists.

| Setting | Purpose and assigned/default behaviour | Safe value |
| --- | --- | --- |
| `PREFERRED_PROVIDER_virtual/kernel` | Weak kernel-provider default; RUBIK Pi sets it before the SoC include. Radxa's assignment remains after the include, so the first upstream `?=` can win. | `linux-qcom-next` |
| `MACHINE_FEATURES` | Appends board features to SoC defaults. | `efi pci` |
| `KERNEL_CMDLINE_EXTRA:append` | RUBIK Pi appends a deferred-probe timeout in seconds. | `deferred_probe_timeout=30` (leading space appended) |
| `KERNEL_DEVICETREE` | Explicit DTB path for each board. | `qcom/qcs6490-thundercomm-rubikpi3.dtb` or `qcom/qcs6490-radxa-dragon-q6a.dtb` |
| `QCOM_DTB_DEFAULT` | Weak default DTB stem. | `qcs6490-thundercomm-rubikpi3` or `qcs6490-radxa-dragon-q6a` |
| `QCOM_BOOT_FIRMWARE` | RUBIK Pi boot recipe; explicitly empty on Radxa because SPI NOR is vendor-managed. | `firmware-qcom-boot-rubikpi3` |
| `QCOM_BOOT_FILES_SUBDIR` | RUBIK Pi deploy directory; explicitly empty on Radxa. | `rubikpi3` |
| `QCOM_PARTITION_FILES_SUBDIR` | RUBIK Pi weak default partition asset directory; explicitly empty on Radxa. | `partitions/qcs6490-thundercomm-rubikpi3/ufs` |
| `QCOM_CDT_FILE` | RUBIK Pi CDT stem; explicitly empty on Radxa. | `RubikPi3_CDT` |
| `QCOM_PARTITION_FILES_SUBDIR_SPINOR`, `QCOM_PARTITION_CONF` | Radxa explicitly disables boot partition packaging; RUBIK Pi inherits parent defaults. | Empty string on Radxa |
| `WKS_FILE` | Radxa's explicit EFI/UKI disk layout; RUBIK Pi inherits parent default. | `efi-uki-bootdisk.wks.in` |
| `QCOM_ESP_IMAGE` | Radxa disables the standalone ESP image, using its WKS instead. | Empty string |
| `QCOM_VFAT_SECTOR_SIZE` | Radxa weak default sector size as an integer string; override for UFS. | `512` for SD; `4096` for UFS |
| `QCOM_BOOTIMG_ROOTFS` | Radxa weak root partition identifier. | `PARTLABEL=root` |
| `IMAGE_FSTYPES` | Radxa appends disk-image formats to inherited list. | `wic wic.gz wic.bmap` |
| `MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS` | Appended board/SoC packages; Radxa also selects Hexagon DSP and QAIRT v68 packages. | `packagegroup-rubikpi3-firmware` |

Do not set `PREFERRED_PROVIDER_virtual/bootloader` for Radxa; its existing SPI NOR
EDK2 boots the generated OS image. `#@TYPE`, `#@NAME`, and `#@DESCRIPTION` are
machine description comments, not BitBake assignments.

## Recipes and kernel fragment

| Setting | Type, purpose, and default | Safe value |
| --- | --- | --- |
| `SUMMARY`, `DESCRIPTION` | Human-readable strings; recipes set their own descriptions. | `Boot firmware for Thundercomm RUBIK Pi 3` |
| `LICENSE`, `LIC_FILES_CHKSUM` | Required vendor licence identifier and source licence checksum. These do not replace the layer's MIT licence. | `LicenseRef-LICENSE.qcom-2`, `file://LICENSE.txt;md5=165287851294f2fb8ac8cbc5e24b02b0` |
| `SRC_URI` / firmware | Required Git fetch URL with protocol, branch, and unpack destination parameters. | `git://github.com/rubikpi-ai/boot-assets;protocol=https;branch=main;destsuffix=${BP}` |
| `SRCREV` | Required pinned firmware revision; no floating default. | `10b868574aa4d06fb3836399d10eb5c792765504` |
| `INHIBIT_DEFAULT_DEPS` | Boolean integer string disabling compiler/libc dependencies for prebuilt firmware. | `1` |
| `do_configure[noexec]`, `do_compile[noexec]` | Boolean task flags disabling these tasks for binary firmware. | `1` |
| `inherit allarch deploy` | Required class selection for firmware packaging/deployment, supplied upstream. | `allarch deploy` |
| `QCOM_BOOT_IMG_SUBDIR` | Relative deployment subdirectory. | `rubikpi3` |
| `COMPATIBLE_MACHINE` | Regular expression restricting the firmware recipe. | `(rubikpi3)` |
| `addtask deploy before do_build after do_install` | Task ordering; deploy runs after install and before build completion. | Existing ordering |
| `inherit packagegroup` | Upstream class providing packagegroup defaults. | `packagegroup` |
| `PACKAGES` | Explicit package-name list; Radxa includes a separate DSP package. | `${PN}-firmware`, `${PN}-hexagon-dsp-binaries` |
| `RRECOMMENDS:${PN}-firmware` | Recommended firmware-package list; GPU packages are conditional on opencl/opengl/vulkan in `DISTRO_FEATURES`. | `linux-firmware-qcom-vpu` |
| `RDEPENDS:${PN}-hexagon-dsp-binaries` | Radxa DSP runtime package requirements. | `hexagon-dsp-binaries-radxa-dragon-q6a-adsp` and `-cdsp` |
| `FILESEXTRAPATHS:prepend` | Immediately expanded search-path prefix for kernel source additions. | `${THISDIR}/${BPN}:` |
| `FILESEXTRAPATHS:prepend:radxa-dragon-q6a` | Radxa-only immediately expanded fragment directory. | `${THISDIR}/radxa-dragon-q6a:` |
| `SRC_URI:append:radxa-dragon-q6a` | Radxa-only file list appended to kernel inputs. | `file://realtek-eth-8169.cfg` (leading space appended) |
| `INCOMPATIBLE_LICENSE_EXCEPTIONS:append:rubikpi3` | Optional Qualcomm distro exception, applied only with the dynamic qcom-distro collection. | `firmware-qcom-boot-rubikpi3:LicenseRef-LICENSE.qcom-2` (leading space appended) |

The kernel fragment sets boolean Kconfig symbols `CONFIG_NET_SELFTESTS`,
`CONFIG_R8169`, `CONFIG_MDIO_BUS`, `CONFIG_PHYLIB`, `CONFIG_FIXED_PHY`,
`CONFIG_REALTEK_PHY`, `CONFIG_FWNODE_MDIO`, `CONFIG_OF_MDIO`, and `CONFIG_ACPI_MDIO`
to `y` to include the Realtek Ethernet driver, PHY, self-tests, and MDIO discovery
support. `CONFIG_REALTEK_PHY_HWMON` is explicitly unset (`n`) to exclude its hardware
monitoring. These override the parent kernel's configuration when Radxa is selected;
other machines do not receive the fragment.

## Workflow and documentation settings

The [workflow files](https://github.com/devdocsorg/meta-qcom-3rdparty/tree/docs/offline-layer-guides/.github/workflows)
own triggers, action pins, permissions, runners, and job ordering. GitHub supplies
`GITHUB_*` and event context. Secret values are configured in repository settings,
never in `.env` or committed files.

| Setting | Type, purpose, and default | Safe example |
| --- | --- | --- |
| `profile` | Optional string build-workflow input, default `full`; callers may select `pr`. | `pr` |
| `skip_if_github_cached` | Optional boolean, default false; nightly callers set true to reuse successful identical inputs. | `false` |
| `CACHE_DIR` | Hosted shared-cache path, explicitly `/efsx/qli/meta-qcom`. | Existing CI path |
| `KAS_CLONE_DEPTH` | Hosted clone-depth integer string, explicitly `1`. | `1` |
| Build matrix `machine`, `distro.name`, `distro.yamlfile` | Lists selecting the two boards and nodistro/qcom-distro combinations. | `rubikpi3`, `qcom-distro`, `:ci/qcom-distro.yml` |
| `build_id`, `devices`, `project_name`, `distro_name`, `lava_test_plans_ref`, `testkit_ref` | Required reusable test-workflow strings identifying artifacts, device selection, project/distro, and pinned test definitions. | `meta-qcom-3rdparty`, `nodistro`; empty devices keeps board tests disconnected |
| `pr_number`, `pr_url` | Optional strings carrying PR context, default empty. | `123`, `https://github.com/qualcomm-linux/meta-qcom-3rdparty/pull/123` |
| `LAVA_TEST_PLANS_REF`, `TESTKIT_REF` | Explicit revision/tag strings for test inputs. | `95c77fdf4c202ccbfd50c2d449760ebb151287a0`, `testkit-2026.07.19` |
| `commit`, `event_file`, `event_name`, `workflow_id` | Required result-publication inputs identifying the tested commit/event/run. | Candidate SHA, `artifacts/Event File/event.json`, `pull_request`, run ID |
| `devices_premerge`, `distro_suffix` | Optional test-workflow strings, default empty; select extra premerge devices and a distro suffix only when needed. | Empty string |
| `QUIC_YOCTO_BACKPORT_PAT`, `GITHUB_TOKEN`, `TEST_REPORTING_APP_TOKEN`, `LAVATOKEN` | Secret GitHub credentials supplied to existing actions; no literal/default credential. | Use repository-managed secrets |
| Stale thresholds and exemptions | Integers/booleans/lists: 30 days stale, 5 days to close, issues never auto-close (`-1`), 100 operations, bug/enhancement issues and enhancement PRs exempt; activity removes stale state. | Existing workflow values |
| Markdown `MD013`, `MD033`, `MD041`, `MD024.siblings_only` | Booleans: line-length/HTML checks false, first-heading check true, duplicate headings restricted to siblings. | Existing `.github/.markdownlint.yaml` |
| Sphinx `project`, `extensions`, `root_doc`, `myst_heading_anchors`, `nitpicky` | Inline documented string/list/integer/boolean settings in `conf.py`; project title, MyST/autodoc, README root, depth 4, strict references. | Repository configuration |
| Sphinx `exclude_patterns`, `templates_path`, `html_additional_pages`, `html_show_search_summary` | Inline documented list/mapping/boolean settings; local entry template and no fetch-based excerpts. | `False` for search summaries |
| Sphinx `nitpick_ignore` | Optional list, default empty; permits unlinked standard-library Path and CalledProcessError types while retaining strict local references. | Two explicit standard-library entries in `conf.py` |
| `SHDOC_REV` | Required Makefile revision string, pinned with the documentation toolchain. | `52917b2f3471fe77c745ede115494d2d5c9168d1` |

`requirements.txt` declares exact documentation package versions;
`requirements.lock` resolves every transitive version. `.gitignore` excludes local
environment files, caches, the tool clone, and generated reference Markdown, while
retaining `.env.example` and the committed site. No new application setting is
introduced by the documentation setup.
