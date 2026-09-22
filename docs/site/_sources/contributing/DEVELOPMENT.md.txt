# Development environment

## 1. Check out this proposal

The documentation tools in this walkthrough are on the fork's review branch:

```sh
git clone --branch docs/offline-layer-guides https://github.com/devdocsorg/meta-qcom-3rdparty.git
cd meta-qcom-3rdparty
```

Use this directory for all commands below. Upstream layer changes still follow the
[Qualcomm Linux contribution procedure](CONTRIBUTING.md); the fork is the runnable
checkout for this documentation proposal.

## 2. Prepare tools

Use Git, GNU Make, GNU awk (`gawk`), and uv 0.12.3. `setup` installs Python 3.12,
Sphinx 9.1.0, MyST 5.1.0, Playwright 1.62.0, and the locked dependencies into
`.venv`. It installs shdoc at commit
`52917b2f3471fe77c745ede115494d2d5c9168d1` into `.tools/shdoc`.
Python AST and bashlex independently inventory definitions; shdoc and autodoc
produce their references. No build task is executed by extraction.
Use the [uv installation instructions](https://docs.astral.sh/uv/getting-started/installation/)
if uv is absent; install Git, Make, and GNU awk through your host's package manager.

```sh
make -f docs/source/Makefile setup
```

Expected result: `.venv/bin/sphinx-build --version` reports Sphinx 9.1.0 and
`.tools/shdoc/shdoc` exists at the pinned revision. System Chromium is used when
available. Otherwise install the user-local test browser:

```sh
make -f docs/source/Makefile browser
```

For layer checks and image builds, use kas-container 4.8.2 with Docker or Podman.
The [agent prerequisites](AGENTS.md#1-prerequisites) provide the container smoke
tests in required order: Docker first, then Podman if installed.
A user-local installation is available with `uv tool install 'kas==4.8.2'`;
put its binary directory on PATH or export `KAS_CONTAINER` to the absolute path.
Hosted Yocto CI resolves the latest kas-container release; 4.8.2 is the tested
local version, not a change to the project's CI policy.

## 3. Configure external build storage

[Configuration](../user/CONFIGURATION.md) explains precedence and defaults.
The project does not automatically load `.env`. Start with the safe
{download}`environment example <../../../.env.example>`, set paths for your host, and export
them explicitly. Preserve settings already supplied by your environment:

```sh
export REPO_DIR="$(pwd)"
export KAS_WORK_DIR="${KAS_WORK_DIR:-$HOME/.cache/meta-qcom-3rdparty/work}"
export DL_DIR="${DL_DIR:-$HOME/.cache/meta-qcom-3rdparty/downloads}"
export SSTATE_DIR="${SSTATE_DIR:-$HOME/.cache/meta-qcom-3rdparty/sstate-cache}"
mkdir -p "$KAS_WORK_DIR" "$DL_DIR" "$SSTATE_DIR"
```

These directories must remain outside the checkout. No secrets are needed for
public source fetches. Retain network access for setup and kas source fetching;
the generated documentation itself works offline.

## 4. Build and validate documentation

```sh
make -f docs/source/Makefile html
```

Open `docs/site/index.html` directly. Expect contributor and user navigation,
search results, and native function references, including `_is_dir` and `do_deploy`.
Every changed source file with functions needs native comments with purpose,
parameter and return types, examples, and failure behaviour. Adding embedded Python
or another unsupported language requires configuring its extractor before building.

After reviewing and staging regenerated output, commit sources and output together
with the [required sign-off](AGENTS.md#7-commit-message-best-practices-project-style),
then run:

```sh
make -f docs/source/Makefile check
```

Expected result: native coverage and mutation checks pass, copied-site search works
without networking, and Git reports no changed or untracked `docs/site` files.
CI invokes these same targets. The reference, doctree, and tool caches stay ignored.
The lockfile extends the skeleton only with bashlex 0.18 for independent shell
parsing. Update dependency pins deliberately and regenerate `requirements.lock`
with `uv pip compile --python-version 3.12 docs/source/requirements.txt -o docs/source/requirements.lock`.

## 5. Run repository checks

Run the [routine patch review](AGENTS.md#4-run-routine-checks-via-ci-helper-scripts).
Before every PR opening or update, run the two
[required checks in order](AGENTS.md#6-pull-request--contribution-workflow):
patchreview first, then check-layer. Commit the candidate beforehand because
check-layer internally clones the checkout. Verify that temporary clone's HEAD
matches the candidate commit. Documentation scope does not waive these checks.

The existing Markdown workflow lints all Markdown using
`.github/.markdownlint.yaml`. With Node.js 22 and markdownlint-cli2 installed,
check the tracked files so local tool caches are excluded:

```sh
git ls-files -z '*.md' | xargs -0 markdownlint-cli2 --config .github/.markdownlint.yaml
```

BitBake lint runs when layer metadata changes; hosted QC preflight and upstream
Yocto builds remain in their existing workflows. Hosted builds require Qualcomm's
runners and hosted checks must be reported separately from local results.
For product changes, also follow the existing build, flash, and runtime requirements
in [Contributing](CONTRIBUTING.md#21--pull-request-workflow).
The [usage tutorial](../user/USAGE.md) exercises the actual image output.
