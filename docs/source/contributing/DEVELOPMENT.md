# Set up your development environment

This walkthrough builds and checks the documentation site and runs the layer
checks required before a pull request.

## Prerequisites

The site build needs Git, Make, curl, `sha256sum`, GNU Awk (which runs
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

The `check` target also needs Chromium, tested with [Playwright](https://github.com/microsoft/playwright) 1.62's Chromium 151;
step 4 shows how to install it. Building images and running the layer checks
needs Docker (tested with 29.7) or Podman and [kas-container](https://github.com/siemens/kas) 5.5, installed as the
[build tutorial's prerequisites](../user/USAGE.md#prerequisites) describe.
Dependency installation needs network access; reading the built site does not.

## 1. Clone and create a branch

This proposal's runnable checkout is its review branch:

```sh
git clone -b docs/upgrade-test-1010a https://github.com/devdocsorg/meta-qcom-3rdparty.git
cd meta-qcom-3rdparty
git switch -c my-change
```

Submit the change as the [contribution guide](CONTRIBUTING.md) describes.

## 2. Install the documentation tools

```sh
make -f docs/source/Makefile setup
```

This recreates the documentation-only `.venv` from the lockfile and installs
shdoc and [BitBake](https://github.com/openembedded/bitbake)'s parser at pinned versions in it. The Makefile uses a
POSIX shell; on Windows, use WSL.

## 3. Build the site

Edit the Markdown under `docs/source/`, then build:

```sh
make -f docs/source/Makefile html
```

Expected result: exit status 0, `docs/site/index.html`, and a final line saying
every function is documented and rendered. `docs/site/` is generated and ignored
by Git; the build replaces it to remove stale pages after a source deletion or
rename. The build stops when a function lacks its documentation comment:

- Shell functions, BitBake shell tasks, and shell code in workflow steps take a
  shdoc block directly above the definition, with `@description`, `@arg` or
  `@noargs`, `@exitcode`, and `@example`. In a recipe, keep the block outside
  every task body: text inside a body changes the task's signature.
- Python functions take a docstring with an `Example` section.
- BitBake Python functions, functions nested in a BitBake task, and formats
  without an extractor stop the build until
  [`test_reference_coverage.py`](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1010a/.github/test_reference_coverage.py) supports them.

## 4. Check the site

```sh
make -f docs/source/Makefile check
```

This rebuilds the site and opens a copy with networking disabled to check its
links, anchors, and a search for `environment`. It uses system Chromium when
available; otherwise run `make -f docs/source/Makefile browser` first, and on
Ubuntu also `sudo .venv/bin/playwright install-deps chromium`. The
documentation CI job installs its browser and runs the same strict build and
check.

Expected result: exit status 0, the coverage line from step 3, and a JSON line
whose `network_requests` and `browser_errors` are empty.

To check by hand, open `docs/site/index.html` directly in a browser, without a
local HTTP server. Navigate to the tutorial, the contribution guide, and this
page, use a heading link, return home, and search for `environment`. Repeat with
networking disabled; a copy of `docs/site/` alone must also work.

## 5. Run the layer checks

Run `yocto-patchreview` routinely and `yocto-check-layer` before opening or
updating a pull request, in that order, with the commands in the
[agent guide's routine checks](AGENTS.md#4-run-routine-checks-via-ci-helper-scripts).
They run in kas-container; load `.env` first, as in the
[build tutorial](../user/USAGE.md#2-choose-the-work-directories). Each command
exits with status 0 when its check passes.

## Update the documentation tools

After changing `docs/source/requirements.txt`, regenerate the lock with
`uv pip compile --python-version 3.12 docs/source/requirements.txt -o docs/source/requirements.lock`,
run setup, and rebuild before committing both files. The
[Makefile](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1010a/docs/source/Makefile)
pins shdoc and BitBake.

## Update the repository map

The README's repository map is exported from the
[Qualcomm repository map](https://github.com/devdocsorg/qualcomm-repository-map)
dataset; its source comment records the map revision and dataset digest.
Updating it needs access to that repository. Record new connections there as its
[maintenance guide](https://github.com/devdocsorg/qualcomm-repository-map/blob/main/data/README.md)
describes, then export from a map checkout beside this one:

```sh
python3 tools/map_build.py --export qualcomm-linux/meta-qcom-3rdparty \
  --readme ../meta-qcom-3rdparty/README.md --revision "$(git rev-parse HEAD)"
```
