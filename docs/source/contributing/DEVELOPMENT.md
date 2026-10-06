# Set up your development environment

This walkthrough prepares a checkout, runs the layer checks that CI runs, and
builds and checks the documentation site.

## Prerequisites

The documentation build needs Git, Make, curl, `sha256sum`, GNU Awk (which runs
[shdoc](https://github.com/reconquest/shdoc) for shell functions), [uv](https://docs.astral.sh/uv/getting-started/installation/),
and Python 3.12, which uv uses when installed and otherwise downloads. Tested with
Git 2.43, GNU Make 4.3, curl 8.5, GNU coreutils 9.4 `sha256sum`, GNU Awk 5.2,
uv 0.12.3, and Python 3.12.13. Install them on Ubuntu:

```sh
sudo apt install git make curl gawk
curl -LsSf https://astral.sh/uv/0.12.3/install.sh | sh
```

On macOS 15 or newer, which includes `sha256sum`, with [Homebrew](https://brew.sh/):

```sh
xcode-select --install
brew install gawk
curl -LsSf https://astral.sh/uv/0.12.3/install.sh | sh
```

The `check` target also needs Chromium, tested with Playwright 1.62's Chromium 151;
step 4 shows how to install it. The layer checks and image builds need
[Docker](https://docs.docker.com/engine/install/), tested with 29.7, and
`kas-container` from [kas](https://github.com/siemens/kas), tested with 5.5
([installation](https://kas.readthedocs.io/en/latest/userguide/kas-container.html)). Dependency installation needs network access; reading the built
site does not.

## 1. Clone and create a branch

```sh
git clone -b docs/upgrade-test-1006d https://github.com/devdocsorg/meta-qcom-3rdparty.git
cd meta-qcom-3rdparty
git switch -c my-change
```

This branch is the runnable checkout of this documentation proposal. Submit
changes to [`qualcomm-linux/meta-qcom-3rdparty`](https://github.com/qualcomm-linux/meta-qcom-3rdparty)
as the [contribution guide](CONTRIBUTING.md) describes.

## 2. Run the layer checks

Set the kas work directories as in
[step 2 of the build tutorial](../user/USAGE.md#2-set-the-work-directories), then
run the CI-equivalent checks in the order the
[agent guide](AGENTS.md#4-run-routine-checks-via-ci-helper-scripts) gives:
`yocto-patchreview` routinely, and `yocto-check-layer` before opening or updating
a pull request. Both exit with status 0 when the layer passes. `yocto-check-layer`
ends with `meta-qcom-3rdparty ... PASS` and took 12 minutes on a 16-core host.

## 3. Install the documentation tools

```sh
make -f docs/source/Makefile setup
```

This recreates the documentation-only `.venv/` from the locked requirements,
downloads the pinned shdoc, and fetches [BitBake](https://github.com/openembedded/bitbake)
at a pinned revision for its statement parser; `.venv/` stays out of commits. The
[Makefile](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006d/docs/source/Makefile)
owns these commands for both local use and CI. It uses a POSIX shell; on Windows,
run the walkthrough in WSL.

## 4. Edit and check

Edit the Markdown under `docs/source/`, keeping policy files at the repository
root and linking to them. Then build and check the site:

```sh
make -f docs/source/Makefile check
```

The check builds `docs/site/` strictly, checks the function reference, then opens
a copy of the site with Playwright and networking disabled to check navigation,
anchors, resources, and a search-result click. It uses system Chromium when
available; otherwise run `make -f docs/source/Makefile browser` to install
Playwright's user-local browser. On Ubuntu, that browser also needs its system
libraries: `sudo .venv/bin/playwright install-deps chromium`. CI installs its
browser before running the same target.

Expected result: exit status 0, a `Reference coverage: … documented and rendered.`
line, and a JSON summary with no browser errors or network requests. `docs/site/`
is generated and ignored by Git; each build replaces it to remove stale pages.

`make -f docs/source/Makefile html` builds the site without the browser check.
Open `docs/site/index.html` directly in a browser, without a local HTTP server;
external repository and policy pages still need connectivity.

## Function reference

[test_reference_coverage.py](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006d/.github/test_reference_coverage.py)
finds every function in the tracked shell scripts, workflow `run` steps, Makefile
recipes, Python files, and BitBake files, using BitBake's own parser for the
BitBake files. The build fails on formats it cannot read, on functions without a
documentation comment or a configured renderer, and on missing rendered entries.
Shell functions and BitBake shell tasks take a shdoc comment block
(`@description`, `@arg` or `@noargs`, `@exitcode`, `@example`) directly above the
definition, never inside a task, whose body is part of its signature; a shell
function defined inside a task is reported as unsupported. Python
functions take Google-style docstrings with an `Example` section. BitBake Python
functions have no renderer configured, so adding one fails the build until the
script gains one.

Direct documentation dependencies are declared in `docs/source/requirements.txt`;
`docs/source/requirements.lock` also pins their transitive dependencies. After an
intentional tool update, regenerate the lock with
`uv pip compile --python-version 3.12 docs/source/requirements.txt -o docs/source/requirements.lock`,
run setup, and rebuild before committing the requirements and lock. Keep the
layer's own build tools in their own environments.
