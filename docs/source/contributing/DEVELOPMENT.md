# Set up your development environment

This walkthrough prepares a checkout, installs the documentation tools, and
builds and checks the documentation site. The layer's own builds and checks run
in kas-container, as the [agent guide](AGENTS.md) describes.

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

The `check` target also needs Chromium, tested with Playwright 1.62's Chromium 151;
step 5 shows how to install it. Dependency installation needs network access;
reading the built site does not.

Building the layer and running its checks needs
[kas-container](https://kas.readthedocs.io/en/latest/userguide/kas-container.html)
and [Docker](https://docs.docker.com/engine/install/) or Podman, tested with
kas-container 4.8.2 and Docker 29.7.

## 1. Clone and create a branch

```sh
git clone -b docs/upgrade-test-1007a https://github.com/devdocsorg/meta-qcom-3rdparty.git
cd meta-qcom-3rdparty
git switch -c docs/my-change
```

This proposal branch holds the documentation tools. Contributions go to
[the upstream repository](https://github.com/qualcomm-linux/meta-qcom-3rdparty),
as the [contribution guide](CONTRIBUTING.md#21--pull-request-workflow) describes.

## 2. Install the documentation tools

```sh
make -f docs/source/Makefile setup
```

`setup` recreates `.venv` from `docs/source/requirements.lock`, downloads the
pinned shdoc and checks its SHA-256, and fetches the parser of
[BitBake](https://github.com/openembedded/bitbake) at the commit
the layer's builds use, which [meta-qcom](https://github.com/qualcomm-linux/meta-qcom) pins in its
[kas lock file](https://github.com/qualcomm-linux/meta-qcom/blob/9e35027ec5d241619a1b1e32b0aaf542a6886645/ci/base.lock.yml).
The `.venv` holds only the documentation tools; keep project dependencies and
custom tools in their own environments. The Makefile uses a POSIX shell; on
Windows, run the walkthrough in WSL.

## 3. Configure

The documentation build reads no settings. Layer builds take the optional
kas-container settings in
[.env.example](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1007a/.env.example),
which the [build tutorial](../user/USAGE.md#2-choose-the-work-and-cache-directories)
loads.

## 4. Build the site

Edit the Markdown under `docs/source/`. Keep policy files at the repository root
and link to them instead of copying a policy into the docs.

```sh
make -f docs/source/Makefile html
```

Expected result: exit status 0, a final line starting `Reference coverage:` that
reports every function documented and rendered, and `docs/site/index.html`, which
opens directly in a browser. `docs/site/` is generated and ignored by Git; each
build replaces it, removing stale pages.

## 5. Check the site

```sh
make -f docs/source/Makefile check
```

`check` rebuilds the site and opens a copy in headless Chromium with networking
disabled, checking links, anchors, resources, and a search. Expected result: exit
status 0 and a JSON line with `"network_requests": []` and `"browser_errors": []`.
Without system Chromium, run `make -f docs/source/Makefile browser`, and on Ubuntu
`sudo .venv/bin/playwright install-deps chromium`. The
[documentation workflow](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1007a/.github/workflows/documentation.yml)
runs the same targets on every pull request. External repository and policy
links still need network access.

## 6. Run the layer's checks

Before opening or updating a pull request, run the layer's checks in the order the
[agent guide](AGENTS.md#6-pull-request--contribution-workflow) gives.

## Document functions

[test_reference_coverage.py](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1007a/.github/test_reference_coverage.py)
finds every function in shell scripts, workflow `run` steps, Makefile recipes,
Python, BitBake files, and kas files' BitBake configuration. The build stops on a
function without a complete comment or rendered entry, and on unreadable formats.
Keep the comments authoritative; never edit the generated entries by hand.

- Shell functions and BitBake shell tasks take a shdoc block (`@description`,
  `@arg` or `@noargs`, `@exitcode`, and `@example`) directly above the definition.
  Never put it inside a task body: BitBake hashes the body, comments included.
- Python functions take a docstring with an `Example` section, rendered with
  autodoc and napoleon.
- BitBake Python functions stop the build until a renderer for them is added.
  A function defined inside a BitBake task also stops it: define it separately.

## Update the documentation tools

After changing `docs/source/requirements.txt`, regenerate the lock with
`uv pip compile --python-version 3.12 docs/source/requirements.txt -o docs/source/requirements.lock`,
then run `setup` and rebuild before committing the requirements and lock. The
[Makefile](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1007a/docs/source/Makefile)
pins the shdoc and BitBake revisions.
