# Configuration reference

This layer supplies BitBake metadata and kas fragments. It is not a runtime
application and does not automatically read `.env`. The
[commented environment example](../../../.env.example) documents shell exports;
GitHub credentials remain in repository/organisation secrets.

## Loading and precedence

kas merges the colon-separated configuration files, follows `header.includes`,
and creates `bblayers.conf` and `local.conf` in its build directory. The local
`ci/base.yml` imports `meta-qcom/ci/base.yml`, so that parent's selected revision
owns default distro, targets, OE-Core, and BitBake repositories. A later machine
fragment sets `machine`; `ci/qcom-distro.yml` selects the optional distro layers
and image targets through the parent. `ci/ci.yml` and `ci/mirror.yml` likewise
import the parent's CI and mirror settings. Use `kas dump` to inspect the merged
composition and a kas lockfile when exact parent revisions matter.

BitBake loads each enabled layer's `conf/layer.conf`, the selected machine and its
`require` includes, then matching recipes/appends. `=` assigns a string, `:=`
expands it immediately, `.=` concatenates without a space, `+=` appends with a
space, and `?=` assigns only when unset (the first `?=` wins). `??=` is a weak
fallback. `:append`/`:prepend` apply during expansion; machine overrides restrict
board changes. `${...}` expands metadata; `${@...}` evaluates an inline Python
expression. The `qcom-distro` dynamic appends load only when that layer collection
exists. Inspect final values using `bitbake -e` or `bitbake-getvar`; shell environment
variables are not arbitrary BitBake overrides.

## Environment and helper arguments

All environment settings below are optional. Paths are writable absolute paths;
examples contain no credentials. The helper's two positional arguments,
`REPO_DIR` and `WORK_DIR`, are required existing directories; `_is_dir` exits on
invalid input. `TOPDIR`, `SCRIPT`, `BUILDDIR`, `BUILDSTATS`, and `CMD` in the scripts
are computed local values, not supported external settings.

| Setting | Purpose, default/unset behaviour, and safe example |
| --- | --- |
| `REPO_DIR` | Checkout path used by documented commands; no automatic layer default. Example `/work/meta-qcom-3rdparty`. |
| `KAS_WORK_DIR` | kas work/build root; unset uses kas's working directory. Example `/work/yocto`; keep outside the checkout. |
| `DL_DIR` | Download cache path; unset uses the build's `downloads`. Example `/work/cache/downloads`. |
| `SSTATE_DIR` | Shared task cache path; unset uses `sstate-cache` under the build. Example `/work/cache/sstate-cache`. |
| `KAS_CONTAINER` | Executable path; helper falls back to `which kas-container`. Example `/opt/kas/bin/kas-container`. |
| `KAS_YAMLS` | Shell convenience string of colon-separated fragments passed explicitly to kas; no automatic default. Example `ci/rubikpi3.yml:ci/qcom-distro.yml`. |
| `KAS_CONTAINER_ENGINE` | Wrapper runtime selector; default auto-detection. Example `docker`. |
| `KAS_CONTAINER_IMAGE_VERSION` | Container tag string; wrapper-version default. Example `4.8.2`. |
| `KAS_CLONE_DEPTH` | Positive integer clone depth; unset lets kas use its normal full-history policy. Existing CI sets `1`. |
| `PATH` | Executable search list; normal shell default. The buildstats helper appends OE-Core's `scripts/pybootchartgui`. |

## kas files

All YAML declarations are maintained in {download}`ci <../../../ci/README.md>`. `header.version`
is a required integer schema version, `14`; `header.includes` is an optional
ordered list, absent meaning no extra file. Include entries are path strings or
`repo`/`file` string pairs such as `meta-qcom` and `ci/base.yml`. `repos` maps names
to checkout settings. A blank `meta-qcom-3rdparty` entry uses this checkout;
`meta-qcom.url` is the HTTPS upstream URL and `.branch` is `master`. These are
required for the supplied composition; a lockfile may pin commits. No credentials
belong in those URLs.

| Fragment / field | Type, purpose, required/default behaviour, and example |
| --- | --- |
| `base.yml`, `meta-qcom.yml`: `repos.meta-qcom` | Required repository mapping; `url=https://github.com/qualcomm-linux/meta-qcom`, `branch=master`. |
| `rubikpi3.yml`, `radxa-dragon-q6a.yml`: `machine` | Required machine string for a board build; parent default `unset` is not a board. Example `rubikpi3`. |
| `qcom-distro.yml`: includes | Optional composition selecting parent `ci/qcom-distro.yml`; without it the base uses `nodistro` and `core-image-base`. |
| `ci.yml`, `mirror.yml`: includes | Optional parent CI or download-mirror configuration, not implicitly enabled by the local base. |
| `linux-qcom-next.yml`: `local_conf_header.kernelprovider` | Optional multiline BitBake string setting `PREFERRED_PROVIDER_virtual/kernel="linux-qcom-next"`. Without it use the selected machine/SoC provider. |
| `world.yml`: `local_conf_header.world_build` | Optional BitBake string setting `EXCLUDE_FROM_WORLD="1"`, then layer overrides `:layer-qcom="0"` and `:layer-qcom-3rdparty="0"`, restricting world targets to those layers. |
| `world.yml`: `target` | Optional list replacing image targets with `world`; omit the fragment for normal image output. |

## Layer discovery

These required settings live in [conf/layer.conf](../../../conf/layer.conf).
They describe the layer itself and are not user environment variables.

| Setting | Type and purpose | Assigned/default behaviour and safe value |
| --- | --- | --- |
| `BBPATH` | Colon-separated search path. | Appends `${LAYERDIR}` to inherited paths. |
| `BBFILES` | Space-separated recipe globs. | Appends `${LAYERDIR}/recipes-*/*/*.bb` and `*.bbappend`. |
| `BBFILE_COLLECTIONS` | Space-separated collection names. | Adds `qcom-3rdparty`. |
| `BBFILE_PATTERN_qcom-3rdparty` | Regular expression. | Required `^${LAYERDIR}/` identifies this layer's files. |
| `BBFILE_PRIORITY_qcom-3rdparty` | Integer string priority. | Assigned `5`; controls recipe priority. |
| `LAYERDEPENDS_qcom-3rdparty` | Space-separated required collections. | `core qcom`; both must be loaded. |
| `LAYERSERIES_COMPAT_qcom-3rdparty` | Space-separated Yocto series. | `wrynose` in this checkout; do not assume other series are compatible. |
| `BBFILES_DYNAMIC` | Collection-prefixed recipe globs. | Adds qcom-distro-specific `.bb`/`.bbappend` patterns only when `qcom-distro` is loaded. |

## Machine settings

Settings live in the {download}`machine files <../../../conf/machine/README.md>`. Values are
BitBake strings unless described as lists. Required board data is supplied by the
machine; optional overrides should be made in a separate configuration. The SoC
include is required and supplies inherited defaults. Empty Radxa values are
intentional assignments, not missing configuration.

| Setting | Purpose / type | Supplied default or assigned value; safe example |
| --- | --- | --- |
| `PREFERRED_PROVIDER_virtual/kernel` | Optional provider recipe string. | `?= "linux-qcom-next"`; RUBIK assigns before the include, Radxa after it, so an earlier SoC assignment can take precedence. |
| `MACHINE_FEATURES` | Feature list appended to SoC baseline. | Both add `efi pci`. |
| `KERNEL_CMDLINE_EXTRA:append` | Optional kernel argument string. | RUBIK adds `deferred_probe_timeout=30` with a separating space for the HDMI bridge. |
| `KERNEL_DEVICETREE` | Required DTB path/list. | RUBIK `qcom/qcs6490-thundercomm-rubikpi3.dtb`; Radxa `qcom/qcs6490-radxa-dragon-q6a.dtb`. |
| `QCOM_DTB_DEFAULT` | Optional default DTB basename. | `qcs6490-thundercomm-rubikpi3` or `qcs6490-radxa-dragon-q6a`, assigned with `?=`. |
| `QCOM_BOOT_FIRMWARE` | Boot-firmware recipe/list. | RUBIK `firmware-qcom-boot-rubikpi3`; Radxa empty to disable packaging. |
| `QCOM_BOOT_FILES_SUBDIR` | Deploy-relative firmware directory. | RUBIK `rubikpi3`; Radxa empty. |
| `QCOM_PARTITION_FILES_SUBDIR` | Partition asset subdirectory. | RUBIK `?= "partitions/qcs6490-thundercomm-rubikpi3/ufs"`; Radxa empty. |
| `QCOM_CDT_FILE` | CDT basename. | RUBIK `RubikPi3_CDT`; Radxa empty. |
| `QCOM_PARTITION_FILES_SUBDIR_SPINOR`, `QCOM_PARTITION_CONF` | Optional partition paths/recipe. | Radxa assigns both empty; RUBIK inherits SoC defaults. |
| `WKS_FILE` | Wic layout filename. | Radxa `efi-uki-bootdisk.wks.in`; RUBIK inherits its image/SoC layout. |
| `QCOM_ESP_IMAGE` | Optional separate ESP image recipe. | Radxa empty because Wic builds its ESP inline; otherwise inherited. |
| `QCOM_VFAT_SECTOR_SIZE` | Optional sector-size integer string. | Radxa `?= "512"` for SD; use `4096` only for an appropriate UFS target. |
| `QCOM_BOOTIMG_ROOTFS` | Optional root device identifier string. | Radxa `?= "PARTLABEL=root"`; otherwise inherited. |
| `IMAGE_FSTYPES` | Output-format list. | Radxa appends `wic wic.gz wic.bmap`; RUBIK inherits image defaults. |
| `MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS` | Recommended package list. | Both add SoC essentials and board firmware; Radxa also adds its Hexagon packagegroup and `qairt-sdk-hexagon-v68`. |

No `PREFERRED_PROVIDER_virtual/bootloader` is assigned for Radxa: its SPI NOR
firmware owns boot. See [supported machines](SUPPORTED_MACHINES.md) for that boundary.

## Recipe, append, and kernel settings

| Setting / source | Type, purpose, default/unset behaviour, and safe supplied value |
| --- | --- |
| `SUMMARY`, `DESCRIPTION` | Human-readable recipe strings; summaries identify board firmware/packagegroups. The boot recipe's description identifies vendor-signed assets. Metadata is supplied, not a runtime knob. |
| Boot `LICENSE`, `LIC_FILES_CHKSUM` | Required licence expression and source checksum string: `LicenseRef-LICENSE.qcom-2`, `file://LICENSE.txt;md5=165287851294f2fb8ac8cbc5e24b02b0`. Do not substitute the layer MIT licence. |
| Boot `SRC_URI`, `SRCREV` | Required fetch string and immutable revision: `git://github.com/rubikpi-ai/boot-assets;protocol=https;branch=main;destsuffix=${BP}` and `10b868574aa4d06fb3836399d10eb5c792765504`. |
| Boot `INHIBIT_DEFAULT_DEPS` | Boolean string `1`; suppress compiler/libc dependencies for prebuilt assets. Unset would use inherited defaults. |
| Boot `do_configure[noexec]`, `do_compile[noexec]` | Task flag boolean strings `1`; skip configure and compile for prebuilt firmware. |
| Boot `QCOM_BOOT_IMG_SUBDIR` | Required relative destination string `rubikpi3`. The inherited deploy class supplies `DEPLOYDIR`; BitBake supplies source path `S`. |
| Boot `COMPATIBLE_MACHINE` | Required regex `(rubikpi3)`; confines the recipe to this board. |
| Boot `inherit allarch deploy`, `addtask deploy before do_build after do_install` | Required class/task declarations; publish architecture-independent assets after install and before build completion. They do not configure a compiler task. |
| Packagegroup `PACKAGES` | Required package list. RUBIK supplies `${PN}-firmware`; Radxa also supplies `${PN}-hexagon-dsp-binaries`. |
| Packagegroup `RRECOMMENDS:${PN}-firmware` | Firmware package list. Adreno firmware is conditional on any of `opencl opengl vulkan` in inherited `DISTRO_FEATURES`; the expression's false value is empty. Other listed firmware is always recommended. |
| Radxa `RDEPENDS:${PN}-hexagon-dsp-binaries` | Required dependency list for ADSP/CDSP binaries supplied through parent layers; no dependency when that package is not selected. |
| Kernel append `FILESEXTRAPATHS:prepend` | Colon-separated search path; `${THISDIR}/${BPN}:`, plus `${THISDIR}/radxa-dragon-q6a:` under the board override. |
| Kernel append `SRC_URI:append:radxa-dragon-q6a` | Optional machine-scoped file fetch `file://realtek-eth-8169.cfg`; absent for other machines. |
| Dynamic append `INCOMPATIBLE_LICENSE_EXCEPTIONS:append:rubikpi3` | Optional package/licence exception string `firmware-qcom-boot-rubikpi3:LicenseRef-LICENSE.qcom-2`; applies only with qcom-distro's multimedia image. |

The [Radxa Ethernet fragment](../../../recipes-kernel/linux/radxa-dragon-q6a/realtek-eth-8169.cfg)
uses Kconfig booleans. `CONFIG_NET_SELFTESTS=y` enables network self-tests;
`CONFIG_R8169=y` builds the Ethernet driver; `CONFIG_MDIO_BUS=y` and
`CONFIG_PHYLIB=y` enable MDIO/PHY support; `CONFIG_FIXED_PHY=y` enables fixed PHYs;
`CONFIG_REALTEK_PHY=y` enables the Realtek PHY driver; `CONFIG_FWNODE_MDIO=y`,
`CONFIG_OF_MDIO=y`, and `CONFIG_ACPI_MDIO=y` enable firmware-node, device-tree, and
ACPI MDIO enumeration. `CONFIG_REALTEK_PHY_HWMON` is explicitly unset (`n`). Without
this optional board fragment, the selected kernel defaults apply.

## Documentation and repository configuration

[conf.py](../conf.py) comments document each Sphinx setting's type, default, and
purpose. [The Makefile](../Makefile) owns the optional Python executable path and
immutable extractor revisions. [requirements.txt](../requirements.txt) declares
exact tool versions and [requirements.lock](../requirements.lock) pins transitive
packages. Setup requires network access; the resulting site does not.

`.gitignore` excludes only documentation environments, caches, bytecode, and
intermediate reference sources; generated `docs/site/` is committed. The existing
[CODEOWNERS](../../../.github/CODEOWNERS) wildcard sends documentation and code
reviews to the two upstream maintainers. Markdown lint uses
[.markdownlint.yaml](../../../.github/.markdownlint.yaml): `MD013=false` permits long
lines, `MD024.siblings_only=true` restricts duplicate-heading checks to siblings,
`MD033=false` permits inline HTML, and `MD041=true` requires a leading H1.

## GitHub Actions settings

[Workflows](https://github.com/qualcomm-linux/meta-qcom-3rdparty/tree/main/.github/workflows) are loaded by GitHub, not kas. Workflow
`on` events, permissions, runners, matrices, job dependencies, conditions, and
pinned `uses` actions are declared inline. A fork does not gain the upstream
self-hosted runners or secrets. The build jobs explicitly require repository
owner `qualcomm-linux`. LAVA calls are disconnected while no machine has a device.

| Maintained setting | Type, required/default behaviour, purpose, and safe value |
| --- | --- |
| Build `profile` | Optional string `pr` or `full`, default `full`; callers label PR builds `pr`. The current common build implementation does not branch on the value. |
| Build `skip_if_github_cached` | Optional boolean, default false; nightly sets true to skip a previously successful lock/source combination. |
| Build `CACHE_DIR`, `KAS_CLONE_DEPTH` | Required upstream runner path `/efsx/qli/meta-qcom` and shallow-clone integer `1`; local caches use the environment settings above. |
| Build matrix | Required machine strings `rubikpi3`, `radxa-dragon-q6a`; distro objects `nodistro` (empty fragment) and `qcom-distro` (`:ci/qcom-distro.yml`). `world` is true only for nodistro; kernel override strings are empty. |
| Test `build_id` | Required string identifying an Actions build, e.g. `123456789`; no default. |
| Test `pr_number`, `pr_url` | Optional strings, default empty; populate test metadata when reviewing a PR. Example number `123` and the corresponding upstream PR URL. |
| Test-distro `devices` | Required comma-separated string; supplied empty while no board is registered. `devices_premerge` is optional and defaults empty (no extra pre-merge device set). |
| Test-distro `distro_name`, `distro_suffix` | Required `nodistro` or `qcom-distro`; optional suffix defaults empty. These select test plans and artifact names. |
| Test-distro `project_name` | Required plan namespace string `meta-qcom-3rdparty`, no default. |
| `LAVA_TEST_PLANS_REF`, `lava_test_plans_ref` | Required commit/tag/branch string; supplied `95c77fdf4c202ccbfd50c2d449760ebb151287a0` for the test-plan source. |
| `TESTKIT_REF`, `testkit_ref` | Required testkit tag/commit string; supplied `testkit-2026.07.19`. Boot-only plans do not yet consume test definitions. |
| Publish `workflow_id`, `event_name`, `event_file`, `commit` | Required strings: build run ID, trigger type, downloaded JSON path, and tested SHA. No defaults; use the originating run's actual values. |
| `GITHUB_TOKEN`, `github.token` | Runtime-scoped Actions token; required for authenticated Actions operations, automatically supplied by GitHub. Never add a literal example token. |
| `QUIC_YOCTO_BACKPORT_PAT` | Required secret for the backport action; unset prevents authenticated backports. Applies only to merged main PRs with `backport (wrynose)` labels. |
| `LAVATOKEN` | Required secret when submitting LAVA jobs to `lava.infra.foundries.io`; unset prevents submission. |
| `TEST_REPORTING_APP_TOKEN` | Required GitHub App private-key secret for result publishing; client ID `2291458` requests only checks and pull-request write permissions. |
| Preflight switches | Optional booleans explicitly enabling repolinter; semgrep, dependency review, copyright/license, commit-email, commit-message, and armor checks are false. |
| Stale policy | Integer days: stale after `30`, close PRs after `5`, issue close disabled with `-1`; string exemptions `bug,enhancement`; three remove-on-update booleans true; operation cap `100`. Inline messages explain inactivity handling. |
| Scheduling | Cron strings: nightly `22 0 * * *`, wrynose dispatcher `22 23 * * *`, stale `30 1 * * *`, interpreted in UTC by GitHub. Dispatcher explicitly selects `wrynose`. |
| Documentation | Pinned checkout/setup-uv actions and uv `0.12.3`; read-only contents permission, Ubuntu runner, shared Makefile setup/check targets. |

Intermediate workflow values such as `RUN_HASH`, `LOCK_HASH`, `SRC_HASH`, matrix
JSON, artifact IDs, result flags, and downloaded-event metadata are derived outputs,
not user settings. The existing workflow comments explain privilege separation,
cache-key construction, and disabled LAVA callers; preserve those constraints.
