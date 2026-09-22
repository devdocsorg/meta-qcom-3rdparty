# Configuration reference

This layer is BitBake metadata, with kas YAML fragments for assembling a workspace
and GitHub Actions YAML for CI. It has no application daemon or secret-bearing
runtime configuration. The safe [environment example](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/contributor-reference/.env.example)
is documentation; neither kas nor the scripts automatically loads it.

## Loading and precedence

kas loads `header.includes` first, resolves external includes from the named
repository, and merges the selected colon-separated fragments in order. Machine
fragments include `ci/base.yml`, which includes `meta-qcom/ci/base.yml`. The
optional `ci/qcom-distro.yml` adds the upstream distro composition. `local_conf_header`
blocks become BitBake `local.conf`; a later kas value overrides an earlier scalar.
Use `kas-container dump` to inspect the effective configuration.

BitBake loads `conf/layer.conf` for enabled layers, then machine configuration,
its required SoC include, and recipes/appends selected for those layers. `=` assigns,
`?=` assigns only if unset (the first applicable assignment wins), `??=` supplies
a weak default, `:=` expands immediately, `.=` concatenates without a space,
`+=` appends with a space, and `:append`/`:prepend` apply at expansion time.
A suffix such as `:rubikpi3` confines the assignment to that machine. `${VAR}`
expands a variable; `${@...}` evaluates a Python expression. The existing
[board example](../contributing/CONTRIBUTING.md#6--machine-example--thundercomm-rubik-pi-3)
explains why RUBIK Pi selects the kernel before the SoC include.

## Environment settings

These values are strings. The scripts receive `REPO_DIR` and `WORK_DIR` as
positional arguments, not by sourcing the example. Preserve existing cache values.

| Setting | Purpose, requirement, and unset/default behaviour | Safe example |
| --- | --- | --- |
| `KAS_CONTAINER` | Optional executable path; helper falls back to `which kas-container`. | `$HOME/.local/bin/kas-container` |
| `KAS_WORK_DIR` | Optional external kas workspace; otherwise kas uses the current workspace. | `$HOME/.cache/meta-qcom-3rdparty/work` |
| `DL_DIR` | Optional shared source download directory; otherwise inherited build default. | `$HOME/.cache/meta-qcom-3rdparty/downloads` |
| `SSTATE_DIR` | Optional shared build-state cache; otherwise inherited build default. | `$HOME/.cache/meta-qcom-3rdparty/sstate-cache` |
| `REPO_DIR` | Required first argument to the direct Yocto helpers, supplied as `/repo` by the container wrapper. | Checkout root |
| `WORK_DIR` | Required second helper argument, supplied as `/work` by the wrapper. | kas workspace |
| `KAS_YAMLS` | Optional shell convenience in the agent guide; not read by the wrapper, which always uses `ci/base.yml`. | `ci/rubikpi3.yml:ci/qcom-distro.yml` |
| `KAS_CLONE_DEPTH` | CI sets shallow clone depth as an integer string; unset leaves kas's clone default. | `1` |
| `CACHE_DIR` | CI's shared cache root string; build workflow passes it to upstream compile jobs. | `/srv/yocto-cache` |

## kas files

All local YAML fragments require `header.version: 14` (integer schema version).
`header.includes` is an optional ordered list of local paths or `{repo, file}`
objects; omitted means no includes. `repos` is a mapping of repository names to
checkout settings. A null entry means this local repository, not a missing URL.
The YAML language-server comment supplies editor validation and is not loaded by kas.

| File | Maintained values, defaults, and meaning |
| --- | --- |
| `ci/base.yml` | Includes `meta-qcom:ci/base.yml`; `repos.meta-qcom.url` is its HTTPS URL and `branch` is `master`; null `meta-qcom-3rdparty` selects this checkout. Upstream supplies `nodistro`, OE-Core, BitBake, and `core-image-base`. |
| `ci/meta-qcom.yml` | Declares the same required parent URL and `master` branch for reusable includes. |
| `ci/rubikpi3.yml` | Includes local base and assigns required `machine` string `rubikpi3`. |
| `ci/radxa-dragon-q6a.yml` | Includes local base and assigns required `machine` string `radxa-dragon-q6a`. |
| `ci/qcom-distro.yml` | Includes the parent declaration and `meta-qcom:ci/qcom-distro.yml`; optional composition selecting `qcom-distro` and its image target list. |
| `ci/ci.yml` | Includes the parent declaration and `meta-qcom:ci/ci.yml`; optional runner build configuration. |
| `ci/mirror.yml` | Includes the parent declaration and `meta-qcom:ci/mirror.yml`; optional mirror configuration. |
| `ci/linux-qcom-next.yml` | Optional `local_conf_header.kernelprovider` multiline string sets `PREFERRED_PROVIDER_virtual/kernel = "linux-qcom-next"`. |
| `ci/world.yml` | Optional `local_conf_header.world_build` string excludes all recipes (`EXCLUDE_FROM_WORLD = "1"`) then enables `layer-qcom` and `layer-qcom-3rdparty` with `"0"`; `target` is the string list `[world]`. |

`url` and `branch` are required strings for the external parent used here. `machine`
is required for a board build; the inherited base uses `unset` until selected.
`target` is an optional list replacing the inherited target when supplied.
`local_conf_header` is an optional name-to-multiline-string mapping; absent blocks
make no local.conf changes. Safe examples are the checked-in machine fragments.

## Layer settings

The following strings in `conf/layer.conf` are required layer declarations. They
are loaded for this enabled layer; omission means the layer no longer supplies
that declaration. Values shown are the maintained safe examples.

| Setting and value | Purpose |
| --- | --- |
| `BBPATH .= ":${LAYERDIR}"` | Extends metadata include lookup with this layer. |
| `BBFILES += "${LAYERDIR}/recipes-*/*/*.bb ${LAYERDIR}/recipes-*/*/*.bbappend"` | Adds recipe and append globs. |
| `BBFILE_COLLECTIONS += "qcom-3rdparty"` | Registers the layer collection. |
| `BBFILE_PATTERN_qcom-3rdparty := "^${LAYERDIR}/"` | Immediately expands the recipe ownership pattern. |
| `BBFILE_PRIORITY_qcom-3rdparty = "5"` | Integer string priority used in recipe selection. |
| `LAYERDEPENDS_qcom-3rdparty = "core qcom"` | Space-separated required collections. |
| `LAYERSERIES_COMPAT_qcom-3rdparty = "wrynose"` | Space-separated compatible Yocto series. |
| `BBFILES_DYNAMIC += "qcom-distro:…/*.bb qcom-distro:…/*.bbappend"` | Adds recipes/appends under `dynamic-layers/qcom-distro` only when the `qcom-distro` collection is enabled. |

## Machine settings

Both machine files require `conf/machine/include/qcom-qcs6490.inc` from `meta-qcom`.
Unset values are inherited from that include and upstream BitBake configuration;
this layer does not redefine those upstream defaults. Unless described as optional,
the checked-in assignment explicitly sets the board value. All values are strings,
with whitespace-separated lists where indicated.

| Setting | Purpose and board value / safe example |
| --- | --- |
| `MACHINE_FEATURES += "efi pci"` | Adds EFI and PCI capabilities to inherited features. |
| `PREFERRED_PROVIDER_virtual/kernel ?= "linux-qcom-next"` | Optional provider default if unset; RUBIK Pi sets it before the include, Radxa after it. Earlier provider defaults can therefore take precedence on Radxa. |
| `KERNEL_DEVICETREE` | DTB path; `qcom/qcs6490-thundercomm-rubikpi3.dtb` or `qcom/qcs6490-radxa-dragon-q6a.dtb`. |
| `QCOM_DTB_DEFAULT ?=` | Optional default DTB basename; `qcs6490-thundercomm-rubikpi3` or `qcs6490-radxa-dragon-q6a`. |
| `KERNEL_CMDLINE_EXTRA:append` | RUBIK Pi adds `deferred_probe_timeout=30` preceded by a space (seconds) for HDMI bridge probing. |
| `QCOM_BOOT_FIRMWARE` | RUBIK Pi selects `firmware-qcom-boot-rubikpi3`; Radxa explicitly empties it because SPI NOR firmware is managed externally. |
| `QCOM_BOOT_FILES_SUBDIR` | RUBIK Pi deploy subdirectory `rubikpi3`; empty on Radxa. |
| `QCOM_PARTITION_FILES_SUBDIR ?=` | RUBIK Pi default `partitions/qcs6490-thundercomm-rubikpi3/ufs`, supplied upstream through qcom-ptool; Radxa assigns empty. |
| `QCOM_CDT_FILE` | RUBIK Pi selects `RubikPi3_CDT`; Radxa empties it. |
| `QCOM_PARTITION_FILES_SUBDIR_SPINOR`, `QCOM_PARTITION_CONF` | Radxa empties partition-firmware inputs so qcomflash does not package them. RUBIK Pi inherits upstream values. |
| `WKS_FILE` | Radxa selects `efi-uki-bootdisk.wks.in`, generating an EFI partition and root filesystem. |
| `QCOM_ESP_IMAGE` | Radxa empties the separate ESP image because the WIC plugin builds it inline. |
| `QCOM_VFAT_SECTOR_SIZE ?= "512"` | Radxa optional integer string sector size; use `4096` for UFS when appropriate. |
| `QCOM_BOOTIMG_ROOTFS ?= "PARTLABEL=root"` | Radxa optional root identifier for the UKI command line. |
| `IMAGE_FSTYPES += "wic wic.gz wic.bmap"` | Radxa adds disk image, compressed image, and block map outputs. |
| `MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS +=` | Both add `packagegroup-qcom-boot-essential`, `packagegroup-machine-essential-qcom-qcs6490-soc`, and the board firmware packagegroup; Radxa additionally adds its Hexagon DSP packagegroup and `qairt-sdk-hexagon-v68`. |

## Recipes, appends, and kernel fragment

These settings are strings evaluated in the named recipe's context. An omitted
assignment retains BitBake/class/provider defaults; `inherit` is required for
the recipe's stated behaviour.

| File and setting | Purpose, default behaviour, and safe value |
| --- | --- |
| Firmware `SUMMARY`, `DESCRIPTION` | Human-readable strings identifying RUBIK Pi boot firmware and its source. |
| Firmware `LICENSE`, `LIC_FILES_CHKSUM` | Required vendor licence identifier `LicenseRef-LICENSE.qcom-2` and `file://LICENSE.txt;md5=165287851294f2fb8ac8cbc5e24b02b0`; these describe downloaded firmware, separate from this layer's MIT licence. |
| Firmware `SRC_URI`, `SRCREV` | Required Git fetch URL with HTTPS transport, `main` branch, `${BP}` destination, and immutable revision `10b868574aa4d06fb3836399d10eb5c792765504`. |
| Firmware `INHIBIT_DEFAULT_DEPS = "1"` | Boolean string disables default compiler/libc dependencies for binary firmware. |
| Firmware `do_configure[noexec]`, `do_compile[noexec] = "1"` | Boolean task flags skip configuration and compilation. |
| Firmware `inherit allarch deploy` | Uses architecture-independent packaging and the deploy task class. |
| Firmware `QCOM_BOOT_IMG_SUBDIR = "rubikpi3"` | Required deploy subdirectory consumed by the documented `do_deploy` task. |
| Firmware `COMPATIBLE_MACHINE = "(rubikpi3)"` | Required regular expression limits applicability. |
| Firmware `addtask deploy before do_build after do_install` | Schedules deployment after installation and before the overall build task. |
| Both packagegroup `SUMMARY` | Board description for package metadata. |
| Both packagegroup `inherit packagegroup` | Supplies empty packagegroup packages and package dependencies. |
| Both packagegroup `PACKAGES` | Explicit output list: `${PN}-firmware`, plus `${PN}-hexagon-dsp-binaries` on Radxa. |
| Both packagegroup `RRECOMMENDS:${PN}-firmware` | Optional firmware recommendations; GPU firmware appears only with `opencl`, `opengl`, or `vulkan` in `DISTRO_FEATURES`. Other names select board audio/compute, QUP, and video firmware. Radxa also selects camera/HDMI firmware. |
| Radxa `RDEPENDS:${PN}-hexagon-dsp-binaries` | Required ADSP/CDSP packages `hexagon-dsp-binaries-radxa-dragon-q6a-adsp` and `-cdsp`. |
| Kernel append `FILESEXTRAPATHS:prepend :=` | Extends file lookup immediately with `${THISDIR}/${BPN}:`; the Radxa override adds `${THISDIR}/radxa-dragon-q6a:`. |
| Kernel append `SRC_URI:append:radxa-dragon-q6a` | Adds `file://realtek-eth-8169.cfg` only for Radxa. |
| Dynamic multimedia append `INCOMPATIBLE_LICENSE_EXCEPTIONS:append:rubikpi3` | Allows `firmware-qcom-boot-rubikpi3:LicenseRef-LICENSE.qcom-2` only in that image/machine when the distro layer is enabled; no exception elsewhere. |

The Radxa kernel fragment sets tristate/boolean Kconfig values to `y` for
`CONFIG_NET_SELFTESTS` (network self-tests), `CONFIG_R8169` (Realtek PCI Ethernet),
`CONFIG_MDIO_BUS` (MDIO bus), `CONFIG_PHYLIB` (PHY framework), `CONFIG_FIXED_PHY`
(fixed-link PHY), `CONFIG_REALTEK_PHY` (Realtek PHY), `CONFIG_FWNODE_MDIO`
(firmware-node MDIO), `CONFIG_OF_MDIO` (device-tree MDIO), and `CONFIG_ACPI_MDIO`
(ACPI MDIO). It explicitly disables `CONFIG_REALTEK_PHY_HWMON` (PHY hardware
monitoring). These override inherited kernel defaults; final feasibility depends
on Kconfig dependencies. `y` is the safe checked-in example; an absent line leaves
the kernel's defaults intact.

## Documentation and CI configuration

Sphinx's [conf.py](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/contributor-reference/docs/source/conf.py)
documents each setting inline, including type and default. Requirements files pin
the Python dependencies; `Makefile` pins Python and shdoc, clears only `docs/site`,
and puts caches in ignored `.venv`, `.tools`, and `docs/.doctrees`. Gitignore rules
exclude local environments, generated reference intermediates, and Python caches;
`.env.example` is explicitly retained.

`.github/.markdownlint.yaml` disables line-length and inline-HTML rules, requires
an initial H1, and checks duplicate sibling headings. Values are booleans except
`MD024.siblings_only`, a boolean nested option. They override markdownlint defaults.

GitHub loads workflow YAML from `.github/workflows`. The following covers the
schema fields maintained in these files; omitted optional fields use GitHub's
defaults. Expressions `${{ … }}` resolve event/input/output values at runtime.
Secrets are configured in GitHub, never in an environment example.

| Field | Type, purpose, and default / safe example |
| --- | --- |
| `name`, `run-name` | Optional display strings; otherwise workflow filename/event context. |
| `on` | Required event mapping/list; `push`, `pull_request`, `workflow_dispatch`, `workflow_call`, `workflow_run`, and scheduled cron select when each workflow runs. |
| Event `branches`, `paths`, `paths-ignore`, `types`, `workflows` | Optional string lists filtering branches/files/actions/parent workflows; omitted means no corresponding filter. `main` is the ordinary push/PR target. |
| `schedule.cron` | Required five-field UTC schedule string for scheduled workflows; examples `22 0 * * *`, `22 23 * * *`, and `30 1 * * *`. |
| `permissions` | Optional token-scope mapping of `read`, `write`, or `none`; set only the capabilities each workflow/job needs. |
| `concurrency.group`, `cancel-in-progress` | Optional group string and boolean; default no group cancellation. PR builds and tests group by PR identity and cancel superseded runs. |
| `env` | Optional string mapping; omitted entries come from runner environment. Local cache/build/test refs are described here and in workflow comments. |
| `jobs`, `steps` | Required job mapping and ordered step list for runner jobs; reusable workflow jobs use `uses` instead of local steps. |
| `runs-on` | Required runner label or list for local jobs; `ubuntu-latest` or Qualcomm's self-hosted labels. |
| `needs`, `if` | Optional dependency list and boolean expression; omitted jobs have no dependencies and use ordinary success conditions. |
| `strategy.matrix`, `fail-fast` | Optional build/test combinations and boolean cancellation policy; `false` keeps other machine builds running after a failure. |
| `uses`, `with`, `secrets` | Action/workflow reference, typed parameter mapping, and explicit secret map or `inherit`; defaults are defined by the referenced action/workflow. |
| Step `id`, `name`, `run`, `shell` | Optional output identifier/display name, command string, and shell; command steps require `run`, with the runner's default shell unless set. |
| `outputs` | Optional named expression mapping exposing step/job/workflow results; absent means no named outputs. |
| `timeout-minutes`, `continue-on-error` | Optional integer limit (LAVA jobs use 120) and boolean failure policy; otherwise GitHub's limits and fatal failure apply. |
| Called input `type`, `required`, `default`, `description` | Type is string/boolean/number, `required` defaults false, missing explicit defaults are empty/false/zero, and description is optional prose. |

Reusable inputs keep their types/defaults adjacent in the source: build-yocto
`profile` is `full` (optional string, also accepts `pr`), and
`skip_if_github_cached` defaults false (boolean). Test workflows require build IDs,
device lists, distro, project, and test-plan/testkit revisions as strings;
optional PR identity, suffix, and premerge lists default empty. Publishing requires
the workflow/event/commit identifiers. Empty test device lists and the disabled
caller condition intentionally prevent hardware submission.

The `with` settings on pinned third-party actions are governed by those action
interfaces. Locally maintained choices include full-history checkout where
required (`fetch-depth: 0`), disabled checkout credential persistence where present,
cache lookup/save keys and paths, artifact names/IDs and globs, 120-minute LAVA
waiting, and stale/backport label policies. The source contains their exact values;
changing them changes CI behaviour. Backport only acts on merged PRs to `main`
with the `backport wrynose` label. QC preflight enables Repolinter while disabling
its other optional scans. The documentation workflow installs pinned uv and invokes
the same `setup` and `check` targets as contributors.
