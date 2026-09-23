# Configuration

## Loading and precedence

The checked-in files are safe examples for the supported boards. BitBake values
are strings (including space-separated lists); their operators and overrides
control when those strings are combined. `=` replaces, `?=` supplies the first
unset default, `??=` supplies a weak default, `+=` adds with a space, `.= / =.`
concatenate, `:=` expands immediately, and `:append`, `:prepend`, and `:remove`
apply with the active machine/package overrides. See the authoritative
[BitBake assignment and override rules](https://docs.yoctoproject.org/bitbake/dev/bitbake-user-manual/bitbake-user-manual-metadata.html#basic-syntax).
An empty assignment explicitly clears a value; removing it can restore inherited
behaviour. Keep machine-specific changes under their machine override.

[kas 4.8.2 configuration](https://kas.readthedocs.io/en/4.8.2/userguide/project-configuration.html)
owns YAML field types, required fields, include merging, repository selection,
and lockfile precedence. Includes load parent settings; the colon-separated
composition adds local fragments. The checked-in `master` branches float unless
you create a lockfile. This layer declares `wrynose` compatibility; use matching
layer revisions rather than mixing release branches.

## Layer and recipes

The [Yocto variable glossary](https://docs.yoctoproject.org/dev/ref-manual/variables.html)
owns standard variable types, defaults, and examples. The following links identify
the relevant definitions while recording this layer's choices.

| Source and settings | Local purpose and safe values |
| --- | --- |
| [layer.conf](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/conf/layer.conf): [BBPATH](https://docs.yoctoproject.org/dev/ref-manual/variables.html#term-BBPATH), [BBFILES](https://docs.yoctoproject.org/dev/ref-manual/variables.html#term-BBFILES) | Adds this layer to metadata lookup and discovers `recipes-*/*/*.bb` and `.bbappend`; removing these entries makes its metadata unavailable. |
| [BBFILE_COLLECTIONS](https://docs.yoctoproject.org/dev/ref-manual/variables.html#term-BBFILE_COLLECTIONS), [BBFILE_PATTERN](https://docs.yoctoproject.org/dev/ref-manual/variables.html#term-BBFILE_PATTERN), [BBFILE_PRIORITY](https://docs.yoctoproject.org/dev/ref-manual/variables.html#term-BBFILE_PRIORITY) | Collection `qcom-3rdparty`, regex anchored at `${LAYERDIR}`, and numeric priority string `5` identify this layer's files and recipe precedence. |
| [LAYERDEPENDS](https://docs.yoctoproject.org/dev/ref-manual/variables.html#term-LAYERDEPENDS), [LAYERSERIES_COMPAT](https://docs.yoctoproject.org/dev/ref-manual/variables.html#term-LAYERSERIES_COMPAT) | Requires the `core` and `qcom` collections and declares `wrynose`; these are compatibility constraints, not branches downloaded by BitBake. |
| [BBFILES_DYNAMIC](https://docs.yoctoproject.org/dev/ref-manual/variables.html#term-BBFILES_DYNAMIC) | Activates `dynamic-layers/qcom-distro/*/*/*.bb` and `.bbappend` only when `qcom-distro` exists. |
| [Boot firmware recipe](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/recipes-bsp/firmware-boot/firmware-qcom-boot-rubikpi3_20260621.bb): [SUMMARY](https://docs.yoctoproject.org/dev/ref-manual/variables.html#term-SUMMARY), [DESCRIPTION](https://docs.yoctoproject.org/dev/ref-manual/variables.html#term-DESCRIPTION), [LICENSE](https://docs.yoctoproject.org/dev/ref-manual/variables.html#term-LICENSE), [LIC_FILES_CHKSUM](https://docs.yoctoproject.org/dev/ref-manual/variables.html#term-LIC_FILES_CHKSUM) | Identifies the board's signed binaries and checks vendor `LICENSE.txt` against its MD5. `LicenseRef-LICENSE.qcom-2` describes the fetched firmware, independently of this layer's MIT licence. Preserve the checksum until the upstream licence is reviewed. |
| [SRC_URI](https://docs.yoctoproject.org/dev/ref-manual/variables.html#term-SRC_URI), [SRCREV](https://docs.yoctoproject.org/dev/ref-manual/variables.html#term-SRCREV) | Fetches `rubikpi-ai/boot-assets`, HTTPS transport, `main`, destination `${BP}`, at `10b868574aa4d06fb3836399d10eb5c792765504`; the fixed revision is the reproducible source example. |
| [INHIBIT_DEFAULT_DEPS](https://docs.yoctoproject.org/dev/ref-manual/variables.html#term-INHIBIT_DEFAULT_DEPS), `do_configure[noexec]`, `do_compile[noexec]`, `allarch`, `deploy` | Values `1` suppress toolchain defaults and configure/compile tasks for prebuilt firmware. [Task flags](https://docs.yoctoproject.org/bitbake/dev/bitbake-user-manual/bitbake-user-manual-metadata.html#variable-flags) and the [deploy class](https://docs.yoctoproject.org/dev/ref-manual/classes.html#deploy) define execution and staging; `addtask deploy before do_build after do_install` schedules the documented deploy task. |
| `QCOM_BOOT_IMG_SUBDIR`, [COMPATIBLE_MACHINE](https://docs.yoctoproject.org/dev/ref-manual/variables.html#term-COMPATIBLE_MACHINE) | Required local destination string `rubikpi3` and regex `(rubikpi3)` restrict deployment to that board. No user-facing fallback is provided by this recipe. |
| [Packagegroups](https://github.com/qualcomm-linux/meta-qcom-3rdparty/tree/8927b428bcaea0c47186beeb9d9446061c785e9c/recipes-bsp/packagegroups): [PACKAGES](https://docs.yoctoproject.org/dev/ref-manual/variables.html#term-PACKAGES), [RRECOMMENDS](https://docs.yoctoproject.org/dev/ref-manual/variables.html#term-RRECOMMENDS), [RDEPENDS](https://docs.yoctoproject.org/dev/ref-manual/variables.html#term-RDEPENDS) | Both recipes inherit `packagegroup` and replace `PACKAGES` with their firmware group; Radxa also exposes a DSP-binary group with hard dependencies. Firmware recommendations remain optional at image resolution. Either `opencl`, `opengl`, or `vulkan` in `DISTRO_FEATURES` adds the GPU firmware; otherwise that pair is omitted. Exact package lists stay in the recipes. RUBIK Pi omits unavailable Wi-Fi/Bluetooth firmware. |
| [Kernel append](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/recipes-kernel/linux/linux-qcom-next_git.bbappend): [FILESEXTRAPATHS](https://docs.yoctoproject.org/dev/ref-manual/variables.html#term-FILESEXTRAPATHS), `SRC_URI` | Prepends `${THISDIR}/${BPN}:` and, for Radxa, `${THISDIR}/radxa-dragon-q6a:`. Only Radxa appends `file://realtek-eth-8169.cfg`; other boards retain the parent kernel configuration. |
| [Distro image append](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/dynamic-layers/qcom-distro/recipes-products/images/qcom-multimedia-image.bbappend): [INCOMPATIBLE_LICENSE_EXCEPTIONS](https://docs.yoctoproject.org/dev/ref-manual/variables.html#term-INCOMPATIBLE_LICENSE_EXCEPTIONS) | Appends only `firmware-qcom-boot-rubikpi3:LicenseRef-LICENSE.qcom-2`, only for RUBIK Pi and `qcom-multimedia-image` with the distro layer enabled; it does not relax other firmware licences. |

### Ethernet kernel fragment

[realtek-eth-8169.cfg](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/recipes-kernel/linux/radxa-dragon-q6a/realtek-eth-8169.cfg)
sets built-in (`y`) support for `NET_SELFTESTS`, `R8169`, `MDIO_BUS`, `PHYLIB`,
`FIXED_PHY`, `REALTEK_PHY`, `FWNODE_MDIO`, `OF_MDIO`, and `ACPI_MDIO`. These enable
network self-tests, the Ethernet driver, PHY support, and MDIO discovery through
firmware nodes, device tree, and ACPI. `REALTEK_PHY_HWMON` is explicitly disabled
(`n`, represented by the commented “is not set” line), so PHY hardware-monitor
support is not requested. Omitted symbols keep the parent kernel configuration;
Kconfig dependency resolution can constrain these requests. Types, dependencies,
and help text are maintained in the kernel's
[Ethernet](https://github.com/qualcomm-linux/kernel/blob/d49c33864d06e9672dce57738be8851384578fcf/drivers/net/ethernet/Kconfig),
[Realtek](https://github.com/qualcomm-linux/kernel/blob/d49c33864d06e9672dce57738be8851384578fcf/drivers/net/ethernet/realtek/Kconfig),
[PHY](https://github.com/qualcomm-linux/kernel/blob/d49c33864d06e9672dce57738be8851384578fcf/drivers/net/phy/Kconfig), and
[MDIO](https://github.com/qualcomm-linux/kernel/blob/d49c33864d06e9672dce57738be8851384578fcf/drivers/net/mdio/Kconfig) definitions.

## Machines

Both [machine files](https://github.com/qualcomm-linux/meta-qcom-3rdparty/tree/8927b428bcaea0c47186beeb9d9446061c785e9c/conf/machine)
require `qcom-qcs6490.inc` and append `efi pci` to inherited `MACHINE_FEATURES`.
The upstream [SoC include](https://github.com/qualcomm-linux/meta-qcom/blob/1d8048f3a515eeef3758868566ec847b63065811/conf/machine/include/qcom-qcs6490.inc),
[base defaults](https://github.com/qualcomm-linux/meta-qcom/blob/1d8048f3a515eeef3758868566ec847b63065811/conf/machine/include/qcom-base.inc), and
[common defaults](https://github.com/qualcomm-linux/meta-qcom/blob/1d8048f3a515eeef3758868566ec847b63065811/conf/machine/include/qcom-common.inc)
own inherited behaviour. The board values below are safe examples, not interchangeable
hardware settings. Weak defaults can be overridden in build configuration;
explicit `=` values and package selections are part of each board definition.

| Settings | RUBIK Pi 3 | Radxa Dragon Q6A |
| --- | --- | --- |
| `PREFERRED_PROVIDER_virtual/kernel` (provider name) | `linux-qcom-next`, set before the SoC include so its first `?=` wins. | `linux-qcom-next` after the include; the include's earlier `?=` controls when already set. |
| `KERNEL_DEVICETREE`, `QCOM_DTB_DEFAULT` (DTB path and basename) | `qcom/qcs6490-thundercomm-rubikpi3.dtb`; default `qcs6490-thundercomm-rubikpi3`. | `qcom/qcs6490-radxa-dragon-q6a.dtb`; default `qcs6490-radxa-dragon-q6a`. |
| `KERNEL_CMDLINE_EXTRA` (kernel arguments) | Appends `deferred_probe_timeout=30`, allowing the HDMI bridge time to probe. | No local addition. |
| `QCOM_BOOT_FIRMWARE`, `QCOM_BOOT_FILES_SUBDIR`, `QCOM_CDT_FILE` (recipe, directory, and CDT basename) | `firmware-qcom-boot-rubikpi3`, `rubikpi3`, and `RubikPi3_CDT`. | Explicitly empty; Radxa supplies and flashes SPI NOR firmware separately. |
| `QCOM_PARTITION_FILES_SUBDIR` (relative asset path) | Default `partitions/qcs6490-thundercomm-rubikpi3/ufs` from `qcom-ptool` via `qcom-partition-conf`. | Empty, along with `QCOM_PARTITION_FILES_SUBDIR_SPINOR` and `QCOM_PARTITION_CONF`, disabling managed partition firmware assets. |
| `WKS_FILE`, `QCOM_ESP_IMAGE` (image description and recipe) | Inherited image defaults. | `efi-uki-bootdisk.wks.in` builds the ESP and root filesystem together; empty `QCOM_ESP_IMAGE` avoids a separate ESP image. |
| `QCOM_VFAT_SECTOR_SIZE`, `QCOM_BOOTIMG_ROOTFS` (numeric string and root selector) | Inherited 4096-byte/UFS and `PARTLABEL=rootfs` defaults. | Defaults `512` for SD and `PARTLABEL=root`; use `4096` for a UFS target only with the corresponding layout. |
| `IMAGE_FSTYPES` (list) | Inherited Qualcomm image formats. | Adds `wic wic.gz wic.bmap`. |
| `MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS` (package list) | Boot essentials, QCS6490 SoC essentials, and board firmware. | The same SoC/boot groups, Radxa firmware, Radxa Hexagon DSP binaries, and `qairt-sdk-hexagon-v68`. |

Boot image field definitions and consumption are in upstream
[image_types_qcom.bbclass](https://github.com/qualcomm-linux/meta-qcom/blob/1d8048f3a515eeef3758868566ec847b63065811/classes-recipe/image_types_qcom.bbclass)
and [qcom-common-binary.inc](https://github.com/qualcomm-linux/meta-qcom/blob/1d8048f3a515eeef3758868566ec847b63065811/conf/machine/include/qcom-common-binary.inc).
The SoC also selects an additional boot packagegroup; inspect inherited selections
when changing a machine, not just its local recommendations.

## Kas composition

All fragments use schema version `14`. A null local repository entry means the
current checkout; it does not download a replacement. `ci/base.yml` imports the
parent `meta-qcom/ci/base.yml` and adds this layer. `ci/meta-qcom.yml` declares the
same HTTPS `meta-qcom` repository on `master` for include-only compositions.
`ci/rubikpi3.yml` and `ci/radxa-dragon-q6a.yml` include the base and set their
matching `machine` string; the parent otherwise uses `unset`.

`ci/qcom-distro.yml`, `ci/ci.yml`, and `ci/mirror.yml` import the corresponding
parent fragment after declaring `meta-qcom`. Those upstream files own distro
layers/image targets, CI defaults, and sstate mirrors. `ci/linux-qcom-next.yml`
adds a `local_conf_header.kernelprovider` block assigning
`PREFERRED_PROVIDER_virtual/kernel = "linux-qcom-next"`.
`ci/world.yml` selects target `world`, excludes other layers with
`EXCLUDE_FROM_WORLD = "1"`, and re-enables `layer-qcom` and `layer-qcom-3rdparty`
with `0` overrides. Its scope is these two layers, not every recipe in all layers.
See the [parent fragments at the reviewed revision](https://github.com/qualcomm-linux/meta-qcom/tree/1d8048f3a515eeef3758868566ec847b63065811/ci)
and the [image tutorial](USAGE.md) for a complete composition example.

## Environment

The layer does not load `.env` automatically. The root `.env.example` documents
optional shell exports; existing values should be retained by local setup.
[kas-container environment variables](https://kas.readthedocs.io/en/4.8.2/userguide/kas-container.html)
define the inherited cache and container behaviour.

| Setting | Purpose, unset behaviour, and safe example |
| --- | --- |
| `KAS_CONTAINER` | Optional executable path; the wrapper looks up `kas-container` on `PATH` if unset. Use an absolute installed path. |
| `KAS_WORK_DIR` | Optional host working directory; kas otherwise works from its configured/default directory. Local checks explicitly set an external path such as `/tmp/meta-qcom-work`. |
| `DL_DIR`, `SSTATE_DIR` | Optional download and shared-state cache directories; the build defaults apply if unset. Use external writable paths such as `/tmp/yocto-cache/downloads` and `/tmp/yocto-cache/sstate-cache`. |
| `KAS_YAMLS` | Shell convenience string passed as the kas configuration argument, such as `ci/rubikpi3.yml:ci/qcom-distro.yml`; the layer does not read it independently. |
| `REPO_DIR`, `WORK_DIR` | Required positional directory arguments inside CI helpers, normally `/repo` and `/work` supplied by the wrapper. The helpers validate both directories. |

The wrapper derives `TOPDIR` from its own path and converts the required script
argument to a repository-relative path before invoking kas. Buildstats derives
`BUILDSTATS` from BitBake's `TMPDIR`, selects the newest directory by sorted name,
adds the parent layer's chart tool to `PATH`, writes SVG charts under `buildstats`,
and writes the duration-sorted, unhighlighted summary to `buildstats.log`.
These are derived script values, not additional settings to export.

## Automation

GitHub owns standard trigger, permission, concurrency, expression, job, matrix,
and reusable-workflow field semantics in its
[workflow syntax reference](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax).
Each linked source records the exact trigger and configuration. Action inputs and
unset defaults belong to the linked action contracts, rather than a parallel
manual here. Secret names identify protected GitHub configuration; no secret value
belongs in local example files.

| Workflow | Repository choices and contracts |
| --- | --- |
| [build-yocto.yml](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/.github/workflows/build-yocto.yml) | Callable `profile` defaults to string `full` (`pr` is supplied by PRs); `skip_if_github_cached` defaults false and output `build_skipped` reflects a successful-marker hit. Concurrency cancels older runs for the same PR/commit. Owner-gated Qualcomm jobs use self-hosted `qcom-u2404`, `amd64` runners, shared `/efsx/qli/meta-qcom`, and shallow clone depth `1`. Setup downloads the latest kas tag, locks the base+distro composition, and shares locks plus the executable as the required `kas` artifact. A SHA256 of the lock and checkout keys a repository/workflow/ref-scoped success marker. Nightly caching can skip the two machines × two distros compile matrix; world builds run for `nodistro` only. Patchreview precedes layer checking. The [compile contract](https://github.com/qualcomm-linux/meta-qcom/blob/1d8048f3a515eeef3758868566ec847b63065811/.github/workflows/compile.yml) owns empty kernel override strings and build inputs; the [print-build-output action](https://github.com/qualcomm-linux/meta-qcom/blob/1d8048f3a515eeef3758868566ec847b63065811/.github/actions/print-build-output/action.yml) consumes `build-url*` summaries. [Cache restore](https://github.com/actions/cache/blob/v5/restore/action.yml) is lookup-only and [save](https://github.com/actions/cache/blob/v5/save/action.yml) runs only after successful compile. |
| [pr.yml](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/.github/workflows/pr.yml), [push.yml](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/.github/workflows/push.yml) | Main PR builds ignore Markdown and the Markdown lint configuration, upload the `Event File`, and pass `profile: pr`; main pushes call the full build. Documentation-tool source changes therefore still trigger the build workflow. Local pre-PR helper requirements are unchanged by path filters. |
| [nightly-build.yml](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/.github/workflows/nightly-build.yml), [nightly-build-wrynose.yml](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/.github/workflows/nightly-build-wrynose.yml) | UTC schedules `22 0 * * *` and `22 23 * * *` run the cached nightly build and dispatch it on `wrynose`, respectively. The normal nightly workflow also allows manual dispatch and inherits secrets. The dispatcher exposes the job token only to `gh` as `GH_TOKEN`; schedule edits follow the account guidance in the source. |
| [test-pr.yml](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/.github/workflows/test-pr.yml), [test.yml](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/.github/workflows/test.yml) | The privileged completed-build chain reads artifacts as data, resolves PR destination from `event.json`, and cancels stale PR-head test runs. Testing is explicitly disabled (`false &&`, empty device lists) because neither board has a lab entry. The retained plan pin is `95c77fdf4c202ccbfd50c2d449760ebb151287a0`, testkit pin `testkit-2026.07.19`, project `meta-qcom-3rdparty`, and both distro names are passed through. Required `build_id` and optional PR strings are forwarded; successful child summaries become comma-separated artifact IDs. [PR comments](https://github.com/thollander/actions-comment-pull-request/blob/24bffb9b452ba05a4f3f77933840a6a841d1b32b/action.yml) use tag `test-results` and summarize the tested head without accumulating comments. |
| [test-distro.yml](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/.github/workflows/test-distro.yml) | Its documented workflow-call inputs identify build, comma-separated devices, distro, plan/testkit refs, project, and optional premerge devices, suffix, and PR metadata. [Plan generation](https://github.com/qualcomm-linux/meta-qcom/blob/1d8048f3a515eeef3758868566ec847b63065811/.github/actions/lava-test-plans/action.yml) selects `boottest`/`premerge` and distro-specific plans. [LAVA](https://github.com/foundriesio/lava-action/blob/v13/action.yaml) uses `lava.infra.foundries.io` and protected `LAVATOKEN`, waits up to 120 minutes, fails incomplete/failed jobs, and saves result and job detail artifacts. Submission jobs continue on error so all outcomes can be summarized; premerge runs only after every boot passes and a nonempty premerge list is supplied. [Matrix write](https://github.com/qualcomm-linux/github-action-matrix-outputs-write/blob/v3/action.yml) and [read](https://github.com/qualcomm-linux/github-action-matrix-outputs-read/blob/2b2498aa0fc6c565e02af0f3a3c5b7e1b6ae07f4/action.yml) aggregate named per-device results. The [summary action](https://github.com/qualcomm-linux/meta-qcom/blob/1d8048f3a515eeef3758868566ec847b63065811/.github/actions/test-job-summary/action.yml) generates the distro-prefixed artifact and job summary when successful work exists without failed dependencies. |
| [publish-results.yml](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/.github/workflows/publish-results.yml) | Requires workflow ID, event name/file, and commit strings. Downloads result artifacts (also current-run artifacts when different), requires XML, and creates an [app token](https://github.com/actions/create-github-app-token/blob/v3/action.yml) for client `2291458` from `TEST_REPORTING_APP_TOKEN`, scoped to checks/PR writes. The [publisher](https://github.com/EnricoMi/publish-unit-test-result-action/blob/c950f6fb443cb5af20a377fd0dfaa78838901040/action.yml) reads `artifacts/**/*.xml`, fails on failures or inconclusive results, and includes individual runs and suite logs. |
| [backport.yml](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/.github/workflows/backport.yml) | The closed-PR target event acts only after merges into `main`. [Backport action](https://github.com/korthout/backport-action/blob/7c3f6cd5843cac11bc59a04a1b7699af93261670/action.yml) uses `QUIC_YOCTO_BACKPORT_PAT`, matches `^backport (wrynose)$`, and names branches `backport/${pull_number}-to-${target_branch}`. It checks out base code. |
| [stales.yml](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/.github/workflows/stales.yml) | [Stale action](https://github.com/actions/stale/blob/v9/action.yml) runs daily at 01:30 UTC, marks after 30 days, closes PRs after another 5 days, and never automatically closes issues (`-1`). `bug,enhancement` labels are exempt; updates remove stale labels for both item types, capped at 100 operations per run. The configured messages explain those outcomes. |
| [bitbake-lint.yml](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/.github/workflows/bitbake-lint.yml) | PR changes in BitBake formats outside CI/hidden workflows trigger [bitbake-lint](https://github.com/qualcomm-linux/bitbake-lint-action/blob/1b3b5e7d6753138d75e7d179dd956c437824cb7a/action.yml). Full history supports diff-only lint; the last `LAYERSERIES_COMPAT_qcom` token supplies release, informational reports are hidden, and `exit_zero: true` keeps reports advisory. |
| [markdownlint.yml](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/.github/workflows/markdownlint.yml) | Markdown/config changes on PRs and main pushes run the pinned [Markdown action](https://github.com/DavidAnson/markdownlint-cli2-action/blob/6b51ade7a9e4a75a7ad929842dd298a3804ebe8b/action.yml) over `**/*.md`. `.github/.markdownlint.yaml` disables line length and inline-HTML restrictions, limits duplicate headings to siblings, and requires a first heading. [Rule definitions](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md) own allowed options and defaults. |
| [qcom-preflight-checks.yml](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/8927b428bcaea0c47186beeb9d9446061c785e9c/.github/workflows/qcom-preflight-checks.yml) | PRs, main pushes, and manual dispatch call the [v2 orchestrator](https://github.com/qualcomm/qcom-reusable-workflows/blob/v2/.github/workflows/reusable-qcom-preflight-checks-orchestrator.yml). Only repolinter is enabled; Semgrep, dependency, copyright, commit-email, commit-message, and ARMOR checks are explicitly false. [Repolinter](https://github.com/qualcomm/qcom-reusable-workflows/blob/v2/.github/workflows/reusable-repolinter-check.yml) uses the organisation rules when no local `repolint.json` exists. |

Shared [checkout v6](https://github.com/actions/checkout/blob/v6/action.yml),
[upload v6](https://github.com/actions/upload-artifact/blob/v6/action.yml), and
[download v7](https://github.com/actions/download-artifact/blob/v7/action.yml)
contracts own credential, depth, token, run, ID, path, and missing-file defaults.
Build jobs disable persisted checkout credentials; diff/reporting jobs fetch full
history. Artifacts carry lockfiles, build results, and event data across jobs.

The documentation workflow uses the same Make targets as local setup, Python
3.12.13, and uv 0.12.3 through the pinned
[setup-uv contract](https://github.com/astral-sh/setup-uv/blob/d0cc045d04ccac9d8b7881df0226f9e82c39688e/action.yml).
The Makefile fixes shdoc and BitBake revisions; `requirements.txt` declares direct
Python pins and `requirements.lock` resolves transitive pins. Sphinx `conf.py`
comments document each setting: MyST and autodoc/native extraction, `README` as
root, four heading-anchor levels, strict cross-references, local templates,
a generated entry redirect, and search summaries disabled for `file://` use. External `Path`, `Sphinx`,
and `CalledProcessError` types retain their displayed signatures without local
cross-reference targets (`nitpick_ignore`); other missing targets remain errors.
The native extension's format sets determine supported extraction and reject new
unsupported source; these are tool constants, not runtime configuration.
`.gitignore` excludes environment secrets, local tools, bytecode, doctrees, and
intermediate references while preserving `.env.example` and the committed site.
The wildcard `CODEOWNERS` assigns all changes to the existing two maintainers.
