# Configuration

## Loading and syntax

kas merges included YAML depth-first, with later files and the including file
winning conflicting values. Its [4.8.2 configuration reference](https://kas.readthedocs.io/en/4.8.2/userguide/project-configuration.html#configuration-reference)
owns field types, optional fields, and inherited defaults. Local fragments are
listed below; their omitted fields inherit from meta-qcom’s selected branch.

BitBake loads `conf/layer.conf`, then the selected machine and its required SoC
include; recipes inherit the named classes. Its [assignment and override rules](https://docs.yoctoproject.org/bitbake/dev/bitbake-user-manual/bitbake-user-manual-metadata.html)
apply: `=` sets a string, `?=` supplies the first unset default, `+=` appends a
space-separated value, `:append` appends literally, and `:=` expands immediately.
Machine overrides confine board changes. The [Yocto variable glossary](https://docs.yoctoproject.org/ref-manual/variables.html)
owns standard variable definitions and inherited defaults. Values below are safe
repository examples, not secret credentials.

## Environment

The layer has no automatic dotenv loader. The commented
{download}`.env.example <../../../.env.example>`
explains every environment setting used by the local build guidance, including
path types and unset behaviour. Export settings explicitly or source a trusted
copy; existing work/cache values take precedence in the agent guide’s examples.
`ci/*.sh` accept repository and work directories as positional strings, except
`kas-container-shell-helper.sh`, which accepts the script path and supplies both
directories inside the container. Missing paths terminate the scripts.

## Kas compositions

All local YAML files require integer `header.version: 14`. `header.includes`
contains optional repository-relative paths or `{repo, file}` mappings; omitting
it leaves only that file’s settings. The selected paths are the safe examples.

| Fragment | Local values and purpose | Behaviour when omitted |
| --- | --- | --- |
| `ci/base.yml` | `repos.meta-qcom.url` is the canonical HTTPS layer URL; `branch: master` selects development; `includes` loads its `ci/base.yml`; empty `repos.meta-qcom-3rdparty` includes the current checkout. | A machine fragment needs this base for layers, target, and distro. |
| `ci/meta-qcom.yml` | Declares the same URL/branch for fragments requiring that external repository. | External includes cannot resolve without a repository declaration. |
| `ci/rubikpi3.yml` | Includes the local base; string `machine: rubikpi3` selects the board. | Base machine is `unset`; explicitly choose a supported machine. |
| `ci/radxa-dragon-q6a.yml` | Includes the local base; string `machine: radxa-dragon-q6a` selects the board. | As above. |
| `ci/qcom-distro.yml` | Includes the repository declaration and meta-qcom’s `ci/qcom-distro.yml`. | Base uses `nodistro` and `core-image-base`; this optional fragment chooses Qualcomm distro targets. |
| `ci/ci.yml` | Includes the repository declaration and parent CI settings. | CI-specific mirrors, package settings, and build tuning are not added. |
| `ci/mirror.yml` | Includes the repository declaration and parent mirror settings. | Normal fetch and sstate defaults apply. |
| `ci/linux-qcom-next.yml` | `local_conf_header.kernelprovider` is a multiline string setting `PREFERRED_PROVIDER_virtual/kernel = "linux-qcom-next"`. | Machine/provider defaults apply. |
| `ci/world.yml` | Multiline `local_conf_header.world_build` sets string `EXCLUDE_FROM_WORLD = "1"`, then overrides `layer-qcom` and `layer-qcom-3rdparty` to `"0"`; list `target: [world]` selects world. | Base target remains `core-image-base`; ordinary recipe world participation applies. |

Parent `ci/base.yml` supplies OpenEmbedded Core, BitBake, `nodistro`, build history,
cleanup, disk monitoring, mirrors, image features, and the image target. The distro
fragment adds meta-qcom-distro, meta-openembedded, meta-ai, meta-audioreach,
meta-virtualization, meta-selinux, meta-updater, and meta-security. Inspect the
[upstream base](https://github.com/qualcomm-linux/meta-qcom/blob/master/ci/base.yml)
and [distro fragment](https://github.com/qualcomm-linux/meta-qcom/blob/master/ci/qcom-distro.yml)
at your resolved revision for inherited values; this layer does not duplicate them.

## Layer registration

These required strings in `conf/layer.conf` register this layer. Keep the examples
unless intentionally changing layer identity or compatibility.

| Setting | Local purpose and safe value | Unset behaviour |
| --- | --- | --- |
| `BBPATH` | Append `:${LAYERDIR}` so BitBake can find layer configuration. | Configuration lookup omits this layer. |
| `BBFILES` | Append `${LAYERDIR}/recipes-*/*/*.bb` and `*.bbappend` globs. | Recipes are not discovered by these patterns. |
| `BBFILE_COLLECTIONS` | Add collection `qcom-3rdparty`. | Collection-specific declarations cannot identify this layer. |
| `BBFILE_PATTERN_qcom-3rdparty` | Immediately expanded regex `^${LAYERDIR}/` matches recipes. | Recipes cannot be associated with this collection. |
| `BBFILE_PRIORITY_qcom-3rdparty` | Integer string `5` orders recipe selection. | BitBake derives priority from dependencies. |
| `LAYERDEPENDS_qcom-3rdparty` | Space-separated collections `core qcom` are required. | Dependency checks cannot enforce those layers. |
| `LAYERSERIES_COMPAT_qcom-3rdparty` | Release list `wrynose` declares tested compatibility. | BitBake warns about missing compatibility. |
| `BBFILES_DYNAMIC` | Optional `qcom-distro:` patterns under `dynamic-layers/qcom-distro/*/*/` activate recipes/appends only with that collection. | The distro-specific licence exception is not applied. |

## Machine settings

Both machine files require `conf/machine/include/qcom-qcs6490.inc` from meta-qcom.
All values are BitBake strings; lists use spaces. Empty boot values are intentional
overrides, not missing settings. Defaults come from the SoC include unless a local
`?=` default is listed.

| Setting | RUBIK Pi 3 example and purpose | Radxa Dragon Q6A example and purpose |
| --- | --- | --- |
| `MACHINE_FEATURES` | Add `efi pci` capabilities. | Add `efi pci`. |
| `PREFERRED_PROVIDER_virtual/kernel` | Optional default `linux-qcom-next`, set before the include so it wins the first `?=`. | Optional `linux-qcom-next` default after the include; an earlier inherited assignment may win. |
| `KERNEL_CMDLINE_EXTRA:append` | Optional `deferred_probe_timeout=30` (with a leading space) allows HDMI bridge probing. | No local addition. |
| `KERNEL_DEVICETREE` | Required `qcom/qcs6490-thundercomm-rubikpi3.dtb`. | Required `qcom/qcs6490-radxa-dragon-q6a.dtb`. |
| `QCOM_DTB_DEFAULT` | Optional default `qcs6490-thundercomm-rubikpi3`. | Optional default `qcs6490-radxa-dragon-q6a`. |
| `QCOM_BOOT_FIRMWARE` | Recipe name `firmware-qcom-boot-rubikpi3` supplies signed assets. | Empty string disables packaged boot firmware. |
| `QCOM_BOOT_FILES_SUBDIR` | `rubikpi3` selects the boot asset directory. | Empty; SPI NOR firmware is managed separately. |
| `QCOM_PARTITION_FILES_SUBDIR` | Optional default `partitions/qcs6490-thundercomm-rubikpi3/ufs`. | Empty, because this builds an OS disk image. |
| `QCOM_CDT_FILE` | `RubikPi3_CDT` selects the board CDT. | Empty; not packaged. |
| `QCOM_PARTITION_FILES_SUBDIR_SPINOR`, `QCOM_PARTITION_CONF` | No local setting; inherited partition choices apply. | Empty strings disable parent partition packaging. |
| `WKS_FILE` | No local override. | Required `efi-uki-bootdisk.wks.in` selects ESP and UKI layout. |
| `QCOM_ESP_IMAGE` | Inherited default. | Empty disables the separate ESP image recipe. |
| `QCOM_VFAT_SECTOR_SIZE` | Inherited default. | Optional integer string `512` for SD; use `4096` for UFS. |
| `QCOM_BOOTIMG_ROOTFS` | Inherited default. | Optional string `PARTLABEL=root` identifies the root partition. |
| `IMAGE_FSTYPES` | Inherited image formats. | Add `wic wic.gz wic.bmap` disk image formats. |
| `MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS` | Add `packagegroup-qcom-boot-essential`, `packagegroup-machine-essential-qcom-qcs6490-soc`, and `packagegroup-rubikpi3-firmware`. | Add the same SoC groups, `packagegroup-radxa-dragon-q6a-firmware`, `packagegroup-radxa-dragon-q6a-hexagon-dsp-binaries`, and `qairt-sdk-hexagon-v68`. |

## Recipes and kernel fragment

The [board contribution example](../contributing/CONTRIBUTING.md)
explains how these settings fit together. The table covers each local recipe field;
standard defaults and operator syntax follow the references above.

| Files/settings | Purpose, type, and local example | Default or omission |
| --- | --- | --- |
| All recipes: `SUMMARY`; firmware: `DESCRIPTION` | Human-readable strings naming the platform and firmware contents. | BitBake supplies generic package metadata. |
| Firmware: `LICENSE`, `LIC_FILES_CHKSUM` | Required licence expression `LicenseRef-LICENSE.qcom-2` and `file://LICENSE.txt;md5=165287851294f2fb8ac8cbc5e24b02b0`. | Licence QA fails without valid metadata. |
| Firmware: `SRC_URI`, `SRCREV` | Git URI `git://github.com/rubikpi-ai/boot-assets;protocol=https;branch=main;destsuffix=${BP}` and fixed commit `10b868574aa4d06fb3836399d10eb5c792765504`. | No vendor assets are fetched; moving revisions need explicit policy. |
| Firmware: `INHIBIT_DEFAULT_DEPS` | Boolean string `1` skips unnecessary compiler/libc dependencies for binary assets. | Default dependencies remain enabled. |
| Firmware: `do_configure[noexec]`, `do_compile[noexec]` | Boolean strings `1` disable unused build stages. | Inherited configure/compile behaviour runs. |
| Firmware: `inherit allarch deploy` | Class names mark architecture-independent packaging and provide deploy staging. | Those class tasks and defaults are absent. |
| Firmware: `QCOM_BOOT_IMG_SUBDIR`, `COMPATIBLE_MACHINE` | Required directory string `rubikpi3` and regex `(rubikpi3)` select output location and compatible machine. | Recipe lacks board isolation/output location. |
| Firmware: `addtask deploy before do_build after do_install` | Required task ordering schedules deployment after install and before build completion. | Deploy is not linked into that task order. |
| Packagegroups: `inherit packagegroup`, `PACKAGES` | Class and package-name list; RUBIK Pi has `${PN}-firmware`, Radxa also `${PN}-hexagon-dsp-binaries`. | Generic packaging defaults do not express the intended groups. |
| Packagegroups: `RRECOMMENDS:${PN}-firmware` | Space-separated firmware packages; GPU packages are conditional on any `opencl opengl vulkan` distro feature through `bb.utils.contains_any`. | Recommended firmware is absent; exact lists remain in the linked recipe files. |
| Radxa: `RDEPENDS:${PN}-hexagon-dsp-binaries` | Required package names `hexagon-dsp-binaries-radxa-dragon-q6a-adsp` and `...-cdsp`. | DSP binaries are not installed by that group. |
| Kernel append: `FILESEXTRAPATHS:prepend` and `:prepend:radxa-dragon-q6a` | Immediately expanded paths `${THISDIR}/${BPN}:` and `${THISDIR}/radxa-dragon-q6a:` locate fragments. | Search uses inherited paths. |
| Kernel append: `SRC_URI:append:radxa-dragon-q6a` | Optional URI `file://realtek-eth-8169.cfg` adds Radxa Ethernet settings. | Kernel defaults apply. |
| Dynamic image append: `INCOMPATIBLE_LICENSE_EXCEPTIONS:append:rubikpi3` | Optional package/licence pair `firmware-qcom-boot-rubikpi3:LicenseRef-LICENSE.qcom-2` permits vendor boot assets for that image/machine. | Distro incompatibility policy rejects them. |

`realtek-eth-8169.cfg` sets boolean Kconfig symbols to `y` for `CONFIG_NET_SELFTESTS`
(network tests), `CONFIG_R8169` (Realtek Ethernet), `CONFIG_MDIO_BUS` (MDIO bus),
`CONFIG_PHYLIB` (PHY support), `CONFIG_FIXED_PHY` (fixed PHY), `CONFIG_REALTEK_PHY`
(Realtek PHY), `CONFIG_FWNODE_MDIO` (firmware-node MDIO), `CONFIG_OF_MDIO` (device-tree
MDIO), and `CONFIG_ACPI_MDIO` (ACPI MDIO). `CONFIG_REALTEK_PHY_HWMON` is explicitly
unset (`n`) to disable PHY hardware monitoring. Omitting a symbol retains the
selected kernel’s default or other fragments; dependency resolution may still
change the final `.config`. See the [kernel Kconfig language](https://www.kernel.org/doc/html/latest/kbuild/kconfig-language.html).

## CI and documentation settings

The [GitHub Actions syntax reference](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
owns standard `on`, `permissions`, `jobs`, `steps`, `uses`, matrices, conditions,
concurrency, environments, and reusable-workflow inputs. The local workflow YAML
keeps its field-level comments, defaults, and input descriptions; no deployment
credentials belong in the checkout.

| Local setting | Type, example, and behaviour |
| --- | --- |
| Build `profile`, `skip_if_github_cached` | Optional string `full` (`pr` also accepted) and boolean `false`; callers choose scope and successful-build-cache skipping. |
| Build `CACHE_DIR`, `KAS_CLONE_DEPTH` | Runner path `/efsx/qli/meta-qcom` and integer string `1`; the former is runner-specific, the latter limits cloned history. Local work uses the environment guide. |
| Build machine/distro matrix | Required lists select both boards and `nodistro`/`qcom-distro`; `world` is enabled only for nodistro. |
| Test `build_id`, `pr_number`, `pr_url` | Required workflow-run string and optional PR strings; omitted PR values are empty. |
| Test `LAVA_TEST_PLANS_REF`, `TESTKIT_REF` | Pinned commit `95c77fdf4c202ccbfd50c2d449760ebb151287a0` and tag `testkit-2026.07.19`; no environment fallback. |
| Test distro inputs | `build_id`, `devices`, `project_name`, `distro_name`, `lava_test_plans_ref`, and `testkit_ref` are required strings; `distro_suffix`, `devices_premerge`, `pr_number`, and `pr_url` are optional strings with empty defaults. Empty device lists submit no jobs. |
| Publish inputs | `commit`, `event_file`, `event_name`, and `workflow_id` are required strings identifying the tested revision and artifact context. |
| Secrets | GitHub supplies `GITHUB_TOKEN`; maintainers supply `QUIC_YOCTO_BACKPORT_PAT` for backports and `LAVATOKEN` for lab submission. They are required only by the corresponding active operation, with no safe credential default. |
| Preflight switches | Booleans enable repolinter and disable semgrep, dependency review, copyright-specific scanning, email/message scanning, and armor checks. Source header rules still apply through repolinter. |
| BitBake lint | `diff_only: true`, `hide: info`, inferred `release`, and `exit_zero: true` limit reporting to changed metadata and make it advisory. |
| Markdown lint | `MD013: false` permits long lines; `MD024.siblings_only: true` checks duplicate sibling headings; `MD033: false` permits HTML; `MD041: true` requires a title. Other rules keep upstream defaults. |
| Sphinx settings | Each setting in `conf.py` documents its type, default, and chosen value inline; `root_doc = "README"` and bundled search avoid server-only navigation. |
| Documentation setup | `.github/setup_tools.sh` pins required strings `GAWK_VERSION`, `GAWK_SHA256`, `SHDOC_REV`, and `SHDOC_SHA256`; its `TOOLS` path is derived from the checkout. Python 3.12.13 and the requirements lock select tooling. No runtime environment configuration is required for reading the site. |

Scheduler settings are cron strings: main nightly builds use `22 0 * * *`,
wrynose builds use their workflow’s schedule, and stale maintenance uses
`30 1 * * *`. Backports match the regex `^backport (wrynose)$` and create
`backport/<number>-to-<branch>` topics. Stale maintenance uses integer day counts
30/5, disables issue auto-close with `-1`, exempts `bug,enhancement`, removes stale
labels when updated (boolean `true`), and limits operations to 100 per run.
The message strings explain those actions; unset action inputs use the pinned
action’s defaults. See [actions/stale inputs](https://github.com/actions/stale#all-options)
and [backport-action inputs](https://github.com/korthout/backport-action#inputs).
