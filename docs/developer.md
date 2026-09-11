# Developer Notes

[Contribution Guidelines](contributing.md) holds the standards a change to this layer has to meet, and [AGENTS.md](../AGENTS.md) holds the command reference for builds and checks. This page ties the two to the tree itself: where content lives, what continuous integration runs on a pull request, and which of those checks run locally before one is opened. Building the layer and consuming it is the [Usage Guide](usage.md).

## Repository Layout

| Path | Contents |
| --- | --- |
| `conf/` | `layer.conf`, the layer's BitBake declarations, and `machine/`, one configuration file per machine |
| `recipes-bsp/` | Board firmware under `firmware-boot`, machine packagegroups under `packagegroups`, and the U-Boot recipe under `u-boot` |
| `recipes-kernel/` | Kernel recipes, appends and configuration fragments under `linux`, and image appends under `images` |
| `dynamic-layers/qcom-distro/` | Content that applies only when the `qcom-distro` layer is part of the build, gated by `BBFILES_DYNAMIC` in `conf/layer.conf` |
| `ci/` | kas fragments for the base environment, the individual machines and the build options, with the shell scripts for the layer checks and the build statistics |
| `.github/workflows/` | The GitHub Actions workflows described below |
| `docs/` | This documentation set |

[Usage Guide](usage.md) states what `conf/layer.conf` declares; for maintenance the point is that `LAYERDEPENDS_qcom-3rdparty` names the collections a build has to provide alongside this one, and `BBFILE_PRIORITY_qcom-3rdparty` ranks this layer against the others when more than one carries the same recipe. Every machine configuration here requires an SoC include from `meta-qcom` (`conf/machine/include/qcom-qcm2290.inc`, `conf/machine/include/qcom-qcs6490.inc` and `conf/machine/include/qcom-qcs8300.inc`), and those includes pull in `conf/machine/include/qcom-common.inc`, which prepends the `qcom` machine override. Qualcomm behavior common to all boards therefore keys on that override, while board-specific behavior stays behind a machine override, the isolation `contributing.md` section 2.2 asks for.

## Continuous Integration

A pull request runs the following workflows, each named here by its workflow `name:`.

- **Bitbake Lint** (`bitbake-lint.yml`) lints changed recipes and configuration files. It triggers on `**/*.bb`, `**/*.bbappend`, `**/*.bbclass`, `**/*.inc` and `**/*.conf` outside `.github/` and `ci/`, reads the Yocto release from `LAYERSERIES_COMPAT` in `conf/layer.conf`, and reports its findings without failing the job.
- **Markdown Lint** (`markdownlint.yml`) checks `**/*.md` against the rules in `.github/.markdownlint.yaml`.
- **Supported Machines** (`supported-machines.yml`) rewrites [Supported Machines](supported-machines.md) from the machine headers and fails when the page in the tree differs. It triggers on `conf/machine/*.conf`, `docs/supported-machines.md`, `ci/supported-machines.sh` and `.github/workflows/supported-machines.yml`.
- **QC Preflight Checks** (`qcom-preflight-checks.yml`) calls the reusable workflow `qualcomm/qcom-reusable-workflows/.github/workflows/reusable-qcom-preflight-checks-orchestrator.yml` with the `repolinter` check enabled.
- **Build on PR** (`pr.yml`) calls `build-yocto.yml` with the `pr` profile. The call locks the kas fragment stack, runs Yocto patch review and `yocto-check-layer`, and builds the machine matrix; the profile's one effect is to keep the alternate kernel rows of that matrix out of a pull request. Its `paths-ignore` skips the build for changes that touch only `**/*.md` and `.github/.markdownlint.yaml`.
- **Test PR build** (`test-pr.yml`) starts when a Build on PR run completes and, for a pull request that targets `main`, calls **Tests** (`test.yml`), which runs only as a called workflow (`workflow_call`). The two take the artifacts of the finished build, submit boot jobs to LAVA at the pinned test plan and testkit revisions (`LAVA_TEST_PLANS_REF`, `TESTKIT_REF`), the testkit one kept in step with `meta-qcom`, and publish the results back on the pull request.

A few checks reach a pull request from the organization rather than from a workflow in this tree, among them the Developer Certificate of Origin check that requires a `Signed-off-by` trailer on every commit.

## Running the Checks Locally

The two Yocto checks run through the container shell helper, which shells into the `ci/base.yml` environment and runs the named script inside it. Run patch review routinely, and `yocto-check-layer` before opening or updating a pull request.

```bash
ci/kas-container-shell-helper.sh ci/yocto-patchreview.sh
ci/kas-container-shell-helper.sh ci/yocto-check-layer.sh
```

Both need the container runtime described in `AGENTS.md` section 1. `ci/yocto-buildstats.sh` runs the same way and turns the statistics of a finished build into charts and a summary.

Markdown is linted with the tool and the configuration the workflow uses.

```bash
npx markdownlint-cli2 --config .github/.markdownlint.yaml '**/*.md'
```

The supported machines table is checked with two commands, the pair the Supported Machines workflow runs.

```bash
sh ci/supported-machines.sh
git diff --exit-code -- docs/supported-machines.md
```

A non-empty diff means a machine header changed without the page being rewritten from it.

## Adding a Machine

`contributing.md` section 6 walks through the files a new board needs and closes with a checklist of them. Three of those steps carry an obligation for the documentation and for CI.

- The machine configuration opens with the `#@TYPE: Machine`, `#@NAME` and `#@DESCRIPTION` header comments. [Supported Machines](supported-machines.md) is written from those three values, so run `sh ci/supported-machines.sh` and carry the updated page in the same change.
- The kas fragment `ci/<machine>.yml`, `ci/rubikpi3.yml` for instance, includes `ci/base.yml` and sets the machine, which is what makes the board buildable the way CI builds it.
- The build matrix in `.github/workflows/build-yocto.yml` needs a row for the machine, otherwise no pull request builds it.

## Contribution Flow

Changes target `main` first: fork `qualcomm-linux/meta-qcom-3rdparty`, work on a topic branch, rebase on the latest upstream `main`, open a pull request, and iterate in the review discussion (`AGENTS.md` section 6). Every commit carries a `Signed-off-by` trailer taken from the local git identity, so commit with `git commit -s`, keep one logical change per commit, and write the subject as `component: imperative summary` (`AGENTS.md` section 7). A change reaches a release branch after it merges rather than before: labeling the merged pull request `backport wrynose` makes `.github/workflows/backport.yml` open the backport pull request against that branch, the workflow matching the label by pattern.

**SPDX-License-Identifier:** MIT
