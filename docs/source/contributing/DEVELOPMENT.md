# Set up your development environment

This walkthrough prepares a checkout, installs the documentation tools, and runs
the documentation check that CI runs. Layer builds and the Yocto checks use the
container workflow in the [agent guide](AGENTS.md).

## Prerequisites

- Git, GNU Make, curl, and GNU Awk, which runs shdoc. Tested with Git 2.55,
  Make 4.4.1, curl 8.21, and GNU Awk 5.4.1.
- [uv](https://docs.astral.sh/uv/getting-started/installation/) 0.12.3; it
  installs Python 3.12 for the documentation tools.
- Chromium for the offline browser check; tested with Chromium 151.
- For layer builds and checks, the container runtime and kas-container listed
  in the agent guide's [prerequisites](AGENTS.md#1-prerequisites).

## 1. Clone and create a branch

This proposal's runnable checkout is the `docs/layer-documentation` branch of
the [devdocsorg/meta-qcom-3rdparty](https://github.com/devdocsorg/meta-qcom-3rdparty)
fork:

```sh
git clone -b docs/layer-documentation https://github.com/devdocsorg/meta-qcom-3rdparty.git
cd meta-qcom-3rdparty
git switch -c my-change
```

Submit changes where the [contribution guide](CONTRIBUTING.md#27--branches-and-pull-requests) says.

## 2. Install the documentation tools

```sh
make -f docs/source/Makefile setup
```

This creates `.venv/` with the locked Python packages, the BitBake statement
parser from `yocto-6.0.3`, and shdoc v1.4. Expected result: exit status 0 and
an executable `.venv/bin/shdoc`. No environment settings are needed; the
build helpers' variables are documented in
[.env.example](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/.env.example).

## 3. Build and check the documentation

Edit the Markdown under `docs/source/`, then rebuild the site:

```sh
make -f docs/source/Makefile html
```

Expected result: exit status 0, a regenerated `docs/site/`, and a final line
reporting that every function is documented and rendered. Commit the source and
the regenerated site together, then run the check that CI runs:

```sh
make -f docs/source/Makefile check
```

`check` rebuilds the site, opens a copy through `file://` in headless Chromium
with networking disabled, and fails if the committed site differs from the
rebuild. Expected result: exit status 0 and a JSON line with
`"network_requests": []`. Without system Chromium, run
`make -f docs/source/Makefile browser` once to install Playwright's browser.
Open `docs/site/index.html` directly in a browser to read the result.

## 4. Document functions

Each shell function in `ci/` and each shell task in a recipe needs shdoc
comments directly above it: `@description`, `@arg` for each argument (or
`@noargs`), `@exitcode`, and an indented `@example`. The build checks tracked
and staged files: it lists every function that lacks them, and it fails on
Python functions or other languages
until their extractor is configured in
[test_reference_coverage.py](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/.github/test_reference_coverage.py).
The [function reference](README.md#function-reference) shows the result.

## 5. Run the layer checks

Run `yocto-patchreview` routinely and `yocto-check-layer` before opening or
updating a pull request, in the order the agent guide's
[routine checks](AGENTS.md#4-run-routine-checks-via-ci-helper-scripts) give.
Build a board with the agent guide's [kas-container commands](AGENTS.md#3-build-with-kas-container-ci-style).
The [configuration reference](../user/CONFIGURATION.md#ci-workflows) lists
the other checks CI runs on a pull request.

## Update the tools

Direct documentation dependencies are declared in `docs/source/requirements.txt`.
After changing one, regenerate the lock and rebuild:

```sh
uv pip compile --python-version 3.12 docs/source/requirements.txt -o docs/source/requirements.lock
make -f docs/source/Makefile setup html
```

The [Makefile](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/docs/source/Makefile)
pins the BitBake and shdoc revisions. The layout follows the
[repository documentation specification](https://github.com/devdocsorg/qli2-example-repo/blob/main/SPECIFICATION.md).
