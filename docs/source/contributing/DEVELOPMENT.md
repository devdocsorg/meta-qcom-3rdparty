# Development environment

## Check out the documentation branch

This review checkout contains the documentation tools used below. Project patches
follow the [upstream contribution guide](CONTRIBUTING.md); the fork does not own
the Qualcomm layer.

```sh
git clone --branch docs/contributor-reference --single-branch \
  https://github.com/devdocsorg/meta-qcom-3rdparty.git
cd meta-qcom-3rdparty
```

## Install and configure the tools

Use Linux with Git, GNU make, GNU awk, and Docker. The tested toolchain uses
uv 0.12.3, Python 3.12.13, kas-container 4.8.2, and the matching
`ghcr.io/siemens/kas/kas:4.8.2` image. The documentation setup installs Python
locally through uv, Sphinx 9.1.0, MyST 5.1.0, Playwright 1.62.0, and bashlex 0.18.
It checks out shdoc at `52917b2f3471fe77c745ede115494d2d5c9168d1` and runs it with
GNU awk. No BitBake tasks are executed by the documentation extractor.

Install uv using its [installation instructions](https://docs.astral.sh/uv/getting-started/installation/),
selecting version 0.12.3. Install kas-container in a user-owned tools directory:

```sh
mkdir -p "$HOME/.local/bin"
curl --fail --location \
  https://raw.githubusercontent.com/siemens/kas/4.8.2/kas-container \
  --output "$HOME/.local/bin/kas-container"
chmod +x "$HOME/.local/bin/kas-container"
export KAS_CONTAINER="$HOME/.local/bin/kas-container"
```

Run the [agent guide's prerequisites](AGENTS.md#1-prerequisites), including the
Docker smoke test **before** the Podman test. Podman is optional. Then use its
[recommended environment](AGENTS.md#2-recommended-environment), preserving any
already-set work/cache directories. Concrete defaults for this walkthrough are:

```sh
export REPO_DIR="$PWD"
export KAS_WORK_DIR="${KAS_WORK_DIR:-$HOME/.cache/meta-qcom-3rdparty/work}"
export DL_DIR="${DL_DIR:-$HOME/.cache/meta-qcom-3rdparty/downloads}"
export SSTATE_DIR="${SSTATE_DIR:-$HOME/.cache/meta-qcom-3rdparty/sstate-cache}"
mkdir -p "$KAS_WORK_DIR" "$DL_DIR" "$SSTATE_DIR"
```

The [configuration reference](../user/CONFIGURATION.md) explains loading and
precedence. `.env.example` is documentation; no program automatically loads it.
Do not put credentials in the checkout.

## Build and check the documentation

Run these shared local/CI targets from the repository root:

```sh
make -f docs/source/Makefile setup
make -f docs/source/Makefile html
make -f docs/source/Makefile check
```

If Chromium is absent, `make -f docs/source/Makefile browser` installs a user-local
Playwright browser. `html` builds `docs/site/index.html` with warnings treated as
errors. Open that file directly; the whole site, native references, and search work
offline. `check` verifies native coverage and negative regressions, copies the site
outside the checkout, and tests it through `file://` with networking disabled.
It also requires generated output to be committed: a successful source change may
therefore need `git add docs/site` and inclusion in the change's commit before the
final clean-output check passes.

Shell functions and BitBake shell tasks use shdoc comments with purpose, argument
types, exit status, and an example. Python helpers use typed docstrings, Sphinx
autodoc, and Napoleon. The [contributor reference](README.md#function-reference)
includes internal helpers. Coverage independently parses source definitions and
rejects unsupported languages or embedded Python until an appropriate native
extractor is configured. Keep generated reference intermediates in the ignored
`.generated/` directory; commit their HTML with the site.

The Markdown CI uses the existing `.github/.markdownlint.yaml`. Run the same lint
locally with Node 22 and `markdownlint-cli2` 0.22.1:

```sh
npx --yes markdownlint-cli2@0.22.1 --config .github/.markdownlint.yaml '**/*.md' '#.venv/**' '#.tools/**' '#docs/source/contributing/.generated/**'
```

QC preflight uses the [Qualcomm Repolinter rules](https://github.com/qualcomm/.github/blob/main/repolint.json).
Source files, including documentation tools and bundled scripts, require truthful
copyright and licence headers. Keep imported full notices in
[THIRD_PARTY_NOTICES.md](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/contributor-reference/THIRD_PARTY_NOTICES.md).

## Validate the layer

The [agent guide](AGENTS.md#4-run-routine-checks-via-ci-helper-scripts) owns routine
`yocto-patchreview` and the required **patchreview, then yocto-check-layer** ordering
before opening or updating every PR, including documentation PRs. Run its helper
commands from the checkout root after committing the candidate: `yocto-check-layer`
clones the current Git revision internally, so uncommitted changes are not tested.
Record the cloned revision in review evidence.

The [build procedure](AGENTS.md#3-build-with-kas-container-ci-style) owns board and
world build commands. For code or board changes follow the contribution guide's
build, flash, and runtime validation requirements. Documentation-only changes do
not need a full image build, but still require the layer checks above. CI build
jobs run on Qualcomm's runners; local metadata checks do not prove a successful
image build or hardware boot. Boot-test workflows remain disconnected until boards
have LAVA devices.

## Maintain documentation and the repository map

Use the [canonical repository specification](https://github.com/devdocsorg/qli2-example-repo/blob/d0a24ba328d445b278e1b276b54c7defbfa8fca8/SPECIFICATION.md).
Update every affected folder's README inventory. The root README map is maintained
through the [shared map procedure](https://github.com/devdocsorg/qualcomm-repository-map/blob/main/data/README.md),
which requires access to that repository. Export only a committed shared revision,
using the canonical `qualcomm-linux/meta-qcom-3rdparty` identity. Run the shared map
and source checks; keep relationship evidence centrally. Sphinx never reads or
copies the root map.
