# Set up your development environment

This walkthrough prepares a checkout, builds the documentation site with its
function reference, and lists the checks to run before a pull request. Building
images is covered by the [build tutorial](../user/USAGE.md).

## Prerequisites

The site build needs Git, Make, curl, `sha256sum`, GNU Awk (which runs shdoc
for shell functions), [uv](https://docs.astral.sh/uv/getting-started/installation/),
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
step 5 shows how to install it. Dependency installation needs network access;
reading the built site does not.

The layer checks in step 6 need `kas-container` from [kas](https://github.com/siemens/kas)
and Docker, as the [agent guide](AGENTS.md#1-prerequisites) lists; tested with
kas-container 5.5 and Docker 29.7. Install Docker with `sudo apt install docker.io`
on Ubuntu or `brew install --cask docker` on macOS, and `kas-container` as the
[build tutorial](../user/USAGE.md#1-install-kas-container) shows.

## 1. Clone and create a branch

The documentation tooling is proposed on the `docs/upgrade-test-1006c` branch of
a fork; clone that branch until it reaches `main`, and submit changes as the
[contribution guide](CONTRIBUTING.md#21--pull-request-workflow) describes:

```sh
git clone -b docs/upgrade-test-1006c https://github.com/devdocsorg/meta-qcom-3rdparty.git
cd meta-qcom-3rdparty
git switch -c docs/my-change
```

## 2. Configure layer builds

kas-container checks out the layers and builds in `KAS_WORK_DIR`, which defaults
to the current folder. Keep it, and the download and shared-state caches,
outside the checkout: copy `.env.example` to `.env`, adjust the paths that the
[configuration reference](../user/CONFIGURATION.md#environment) explains, then:

```sh
set -a; . ./.env; set +a
mkdir -p "$KAS_WORK_DIR"
```

## 3. Install the documentation tools

```sh
make -f docs/source/Makefile setup
```

This creates `.venv/` with the locked Python packages, shdoc, and the pinned
BitBake whose parser finds functions in the layer metadata. On Windows, use WSL.

## 4. Build the site

Edit the Markdown under `docs/source/`. Keep policy files at the repository root
and link to them instead of copying them into the docs.

```sh
make -f docs/source/Makefile html
```

Expected result: exit status 0, `docs/site/index.html`, which opens directly in
a browser, and a final line `Reference coverage: … function(s) documented and
rendered.` `docs/site/` is generated and ignored by Git.

## 5. Check the site

```sh
make -f docs/source/Makefile check
```

`check` rebuilds the site, opens a copy with Playwright and networking disabled,
and checks navigation, anchors, assets, and a search for `environment`. It uses
system Chromium when available; otherwise run
`make -f docs/source/Makefile browser` first, and on Ubuntu install that
browser's system libraries with `sudo .venv/bin/playwright install-deps chromium`.
Expected result: exit status 0 and
a JSON summary with empty `network_requests` and `browser_errors`. The
[documentation workflow](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006c/.github/workflows/documentation.yml)
runs the same targets on every pull request.

## 6. Run the layer checks

Run `yocto-patchreview` and then `yocto-check-layer` through the CI helper
scripts before opening or updating a pull request, as the
[agent guide](AGENTS.md#6-pull-request--contribution-workflow) shows. Both
exit with status 0 when the layer passes.

## Document functions

The build fails when a function lacks its documentation comment or reference
entry. Shell functions and BitBake shell tasks take a comment block directly
above the definition with `@description`, `@arg` or `@noargs`, `@exitcode`, and
`@example`; shdoc renders it. Keep BitBake comments outside task bodies: body
text is part of the task signature. Python functions take docstrings with an
`Example` section, rendered by autodoc. A source format without an extractor, or
a BitBake Python function, stops the build until
[test_reference_coverage.py](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006c/.github/test_reference_coverage.py)
supports it.

After an intentional documentation-tool update, regenerate the lock with
`uv pip compile --python-version 3.12 docs/source/requirements.txt -o docs/source/requirements.lock`,
run setup, and rebuild before committing the requirements and lock.

## Update the repository map

The `repository-map` block at the end of the root README is generated from the
shared [Qualcomm repository map](https://github.com/devdocsorg/qualcomm-repository-map),
whose comment records the source revision and dataset digest. Do not edit it by
hand. With access to that repository, follow its update procedure, then export
the block from the map checkout; add `--check` to verify an existing export:

```sh
python3 tools/map_build.py --export qualcomm-linux/meta-qcom-3rdparty \
  --readme ../meta-qcom-3rdparty/README.md --revision "$(git rev-parse HEAD)"
```
