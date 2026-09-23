# Set up your development environment

This walkthrough builds the documentation site and its function reference and
runs the same check as CI. To build the layer and run the checks CI requires
before a pull request, follow the [agent guide](AGENTS.md).

## Prerequisites

Tested with the versions shown; newer releases should also work.

- Git, GNU Make, curl, and GNU Awk (`gawk` 5.4), which runs shdoc.
- [uv](https://docs.astral.sh/uv/getting-started/installation/) 0.12. It
  installs Python 3.12 when the host has none.
- Chromium, or Playwright's browser installed by the `browser` target below.
- Network access during setup. Reading the built site needs none.

## 1. Clone and create a branch

```sh
git clone -b docs/offline-layer-documentation https://github.com/devdocsorg/meta-qcom-3rdparty.git
cd meta-qcom-3rdparty
git switch -c docs/my-change
```

This branch carries the documentation tools. Submit changes to
`qualcomm-linux/meta-qcom-3rdparty` as the [contribution guide](CONTRIBUTING.md)
describes.

## 2. Install the documentation tools

```sh
make -f docs/source/Makefile setup
```

`setup` recreates `.venv` from `docs/source/requirements.lock`, downloads
shdoc 1.4 and checks its SHA-256, and clones BitBake `yocto-6.0.3`, whose
parsers read the recipes without running them. Run
`make -f docs/source/Makefile browser` as well if Chromium is not installed.
The build needs no configuration.

## 3. Build and check

```sh
make -f docs/source/Makefile check
```

`check` rebuilds `docs/site/` with warnings as errors, checks the function
reference, opens a copy of the site offline in headless Chromium, and fails if
`docs/site/` differs from the last commit. Expected result: exit status 0, with
a final JSON line reporting the pages visited, a search for `rubikpi3`, and
empty `network_requests` and `browser_errors` lists.

After editing, run `make -f docs/source/Makefile html`, commit the sources and
`docs/site/` together, and run `check` again. The
[documentation workflow](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/offline-layer-documentation/.github/workflows/documentation.yml)
runs `setup` and `check` for every pull request and every push to `main`.

## 4. Document functions

Each shell function, BitBake shell task, and workflow `run` function needs a
shdoc comment directly above it with `@description`, `@arg` for each argument
or `@noargs`, `@exitcode`, and `@example`:

```sh
# @description Stop the script unless a path is an existing directory.
# @arg $1 string Directory path to test.
# @exitcode 0 The path is a directory.
# @example
#   _is_dir "$REPO_DIR"
```

Python functions need docstrings with parameters, return values, and an
example. The `html` target fails with a `Reference coverage:` message naming
any function without a comment or rendered entry, and any source format or
embedded language that has no configured extractor.

## Update the repository map

The map at the end of the root `README.md` is generated from the shared
[Qualcomm repository map](https://github.com/devdocsorg/qualcomm-repository-map),
which needs access to that private repository. Record new build relationships
there, then export the map into this README with the commands in its
[maintenance guide](https://github.com/devdocsorg/qualcomm-repository-map/blob/main/data/README.md).
Sphinx never reads the map.

## Update the tools

Update `docs/source/requirements.txt`, then regenerate the lock:

```sh
uv pip compile --python-version 3.12 docs/source/requirements.txt -o docs/source/requirements.lock
```

The shdoc and BitBake pins are variables at the top of the
[Makefile](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/offline-layer-documentation/docs/source/Makefile).
Run `setup` and `check` after any update.
