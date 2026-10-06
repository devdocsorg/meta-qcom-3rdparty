# Set up your development environment

This walkthrough prepares a checkout, runs the checks CI runs on every pull
request, and builds this documentation with its function reference.

## Prerequisites

The layer checks and image builds run in kas-container; install it and a
container runtime as the [agent guide](AGENTS.md#1-prerequisites) describes.

The documentation build needs Git, Make, curl, `sha256sum`, GNU Awk (which runs
shdoc for shell functions), and [uv](https://docs.astral.sh/uv/getting-started/installation/),
which installs Python 3.12 for the documentation tools. Tested with Git 2.43,
GNU Make 4.3, curl 8.5, GNU coreutils 9.4 `sha256sum`, GNU Awk 5.2, and
uv 0.12.3. Install them on Ubuntu:

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

The documentation check in step 5 also needs a Chromium browser, tested with
Playwright's Chromium 151; step 5 shows how to install it.

## 1. Clone and create a branch

This proposal's runnable checkout is the
[docs/build-prerequisites-test branch](https://github.com/devdocsorg/meta-qcom-3rdparty/tree/docs/build-prerequisites-test);
send changes where the [contribution guide](CONTRIBUTING.md) says:

```sh
git clone -b docs/build-prerequisites-test https://github.com/devdocsorg/meta-qcom-3rdparty.git
cd meta-qcom-3rdparty
git switch -c my-change
```

## 2. Configure

The checks read the settings in
[.env.example](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/build-prerequisites-test/.env.example).
Export the work and cache directories outside the checkout, as the
[agent guide](AGENTS.md#2-recommended-environment) shows.

## 3. Run the layer checks

Run `yocto-patchreview` and then `yocto-check-layer` in the order the
[agent guide](AGENTS.md#4-run-routine-checks-via-ci-helper-scripts) gives; CI runs
both for pull requests to `main`. Expected result: each helper exits with status 0, and
`yocto-check-layer` ends with `meta-qcom-3rdparty ... PASS`. Build an image
with the [image tutorial](../user/USAGE.md) when a change affects a machine.

## 4. Build the documentation

```sh
make -f docs/source/Makefile setup html
```

`setup` creates `.venv` with the locked Python packages, shdoc, and BitBake's
parser. `html` writes the function reference pages, builds the site with warnings
treated as errors, and checks that every function has a rendered entry.
Expected result: exit status 0, `Reference coverage: N function(s) documented and
rendered.`, and `docs/site/index.html`, which opens directly in a browser; Git
ignores the site and `.venv`.

Every shell function and BitBake shell task needs an shdoc comment block directly
above its definition, with `@description`, `@arg` or `@noargs`, `@exitcode`, and
`@example`. Never put the comment inside a task body: BitBake includes the body in
the task signature. Python helpers take Google-style docstrings with an `Example`
section. The build names any function that lacks them and any source format it
cannot read.

## 5. Check the site

`check` rebuilds the site and opens a copy offline in Playwright, checking every
link, anchor, and resource and a search for `environment`. It uses system
Chromium when available; otherwise the commands below install Playwright's
browser. The first installs its system libraries on Ubuntu; skip it on macOS.

```sh
sudo .venv/bin/playwright install-deps chromium
make -f docs/source/Makefile browser
make -f docs/source/Makefile check
```

Expected result: exit status 0 and a JSON line with the number of pages checked,
no network requests, and no browser errors. The
[documentation workflow](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/build-prerequisites-test/.github/workflows/documentation.yml)
runs the same `setup` and `check` targets.

After changing `docs/source/requirements.txt`, regenerate the lock with
`uv pip compile --python-version 3.12 docs/source/requirements.txt -o docs/source/requirements.lock`,
then run `setup` and `check` before committing both files.
