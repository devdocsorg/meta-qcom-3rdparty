# Development environment

Use a Linux checkout for the kas container workflow. Documentation also builds in
WSL. The layer produces Yocto images; documentation changes do not require an
entire image build. Read the [contributor guide](CONTRIBUTING.md) before changing
BSP behaviour.

## 1. Check out the layer

```sh
git clone https://github.com/qualcomm-linux/meta-qcom-3rdparty.git
cd meta-qcom-3rdparty
git switch -c docs/my-change
```

For a fork, clone that fork and preserve upstream contribution routing. See
{download}`branch guidance <../../../BRANCHES.md>` before selecting a release. For a
reproducible review, record the checkout commit and kas-resolved parent revisions.
The development kas fragments follow parent branches, so later resolutions can
change independently of this layer.

## 2. Prepare build tooling

The tested build setup uses Git, Docker, and kas-container 4.8.2 with the
`ghcr.io/siemens/kas/kas:4.8.2` image. Use an existing installation where available.
For a user-local kas wrapper with [uv](https://docs.astral.sh/uv/):

```sh
uv tool install 'kas==4.8.2'
export KAS_CONTAINER="$HOME/.local/bin/kas-container"
```

The [agent guide](AGENTS.md#1-prerequisites) owns the required Docker/Podman smoke
test order and the [shared-cache setup](AGENTS.md#2-recommended-environment).
Set real writable paths outside the checkout for `KAS_WORK_DIR`, `DL_DIR`, and
`SSTATE_DIR`; preserve existing values. `.env.example` is documentation, not an
automatically loaded environment. See [configuration](../user/CONFIGURATION.md).

Follow the [CI-style build procedure](AGENTS.md#3-build-with-kas-container-ci-style)
and [ordered patch/layer checks](AGENTS.md#6-pull-request--contribution-workflow).
A successful patch review writes `status.json` without malformed patch metadata;
a successful layer check completes with no failed tests. The helper always uses
`ci/base.yml`; a first run fetches parent layers. The layer checker clones the
committed checkout, so commit the intended BSP changes before its final run.

## 3. Install documentation tools

Prerequisites are Git, GNU Make, Bash, GNU awk (`gawk`), and uv. The tested host
uses uv 0.12.3, GNU awk 5.4.1, and Bash 5.3. The setup command selects Python 3.12
(tested 3.12.13), installs exact Python packages from the lockfile, and fetches
immutable shdoc and BitBake parser revisions declared in the Makefile.

```sh
make -f docs/source/Makefile setup
make -f docs/source/Makefile browser
```

Reused infrastructure notices are in {download}`THIRD_PARTY_NOTICES.md <../../../THIRD_PARTY_NOTICES.md>`; generated assets bundle their own upstream licences.

The documentation-only `.venv` is recreated by setup. Extractors are stored in
ignored `.doc-tools/`; neither directory belongs in the generated site. The
browser target installs user-local Chromium; omit it when a compatible system
Chromium is available. CI installs its browser dependencies before running the
same check target. No Yocto task is executed during documentation extraction.

## 4. Edit, regenerate, and check

```sh
make -f docs/source/Makefile html
```

Expected result: strict Sphinx build exit status zero, matching native function
coverage, and `docs/site/index.html`. The build removes stale HTML and replaces
only generated reference sources under `contributing/.generated/`. Open the site
entry directly, copy the site elsewhere, and use its navigation and firmware
search with networking disabled.

Keep each authored subject in one source file. Policies stay at the repository
root. Update maintained-folder README inventories when adding or moving files.
Stage and commit documentation sources and generated output together, then run:

```sh
make -f docs/source/Makefile check
```

This checks independent function coverage, source navigation, and the copied site
in a headless offline browser, then rejects changed or untracked site output. The
[documentation workflow](../../../.github/workflows/documentation.yml) uses this
same entry point. Use `git commit -s` to apply the required sign-off.

## 5. Maintain native references

Shell functions use [shdoc annotations](https://github.com/reconquest/shdoc):
`@description`, typed `@arg` or `@noargs`, `@example`, and `@exitcode`, plus relevant
output/failure notes. Do not mark private helpers `@internal`, which hides output.
The generator compares shdoc entries against Bash syntax discovery; BitBake's
native parser discovers task blocks without evaluating statements or loading
includes. The reference includes the local shell tasks, not inherited functions.

Python tooling uses native docstrings with parameter/return types, an example,
and failure behaviour. Sphinx autodoc imports only the audited reference module,
whose work is protected by a main guard. Python AST discovery rejects additional
modules, nested definitions, or unsupported definitions until safe native
extraction is configured. Embedded Python definitions in BitBake and functions
inside workflow `run` blocks are detected and fail with a setup instruction;
current inline Python expressions define no functions. Never execute a recipe or
an unaudited Python module to generate documentation.

When changing tools, update the declared versions, regenerate the lock, rerun setup,
and rebuild. The Makefile owns shdoc and BitBake revision pins; the Python lock owns
Sphinx, MyST, bashlex, PyYAML, Playwright, and transitive package versions.

```sh
uv pip compile --python-version 3.12 docs/source/requirements.txt -o docs/source/requirements.lock
```

## 6. Update the nearby repository map

The root README map is exported independently of Sphinx. Follow the shared map's
[maintenance procedure](https://github.com/devdocsorg/qualcomm-repository-map/blob/main/data/README.md),
using its repository owners and pull-request route for relationship changes.
Access to that repository is required for regeneration. Audit this layer's
recipes, manifests, includes, and selected parent inputs, then use the existing
central checker and exporter with canonical identity `qualcomm-linux/meta-qcom-3rdparty`.
Do not copy the map generator, dataset, or map content into this documentation site.
