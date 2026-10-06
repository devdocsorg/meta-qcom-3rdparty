# Set up your development environment

This walkthrough prepares a checkout, builds the documentation site with its
function reference, and checks it the way CI does. To build images and run the
layer checks, follow the [agent guide](AGENTS.md), which gives the CI-style
kas-container commands.

## Prerequisites

The site build needs Git, Make, curl, `sha256sum`, GNU Awk (which runs shdoc),
[uv](https://docs.astral.sh/uv/getting-started/installation/), and Python 3.12,
which uv downloads when it is not installed. Tested with Git 2.43, GNU Make 4.3,
curl 8.5, GNU coreutils 9.4 `sha256sum`, GNU Awk 5.2, uv 0.12.3, and Python
3.12.13. Install them on Ubuntu:

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

The `check` target also needs Chromium, tested with Playwright 1.62's Chromium;
step 3 shows how to install it. Dependency installation needs network access;
reading the built site does not.

## 1. Clone and create a branch

The documentation tools are on the `docs/upgrade-test-1006b` review branch of
this proposal:

```sh
git clone -b docs/upgrade-test-1006b https://github.com/devdocsorg/meta-qcom-3rdparty.git
cd meta-qcom-3rdparty
git switch -c docs/my-change
```

Send changes where the [contribution guide](CONTRIBUTING.md) says.

## 2. Install the documentation tools

```sh
make -f docs/source/Makefile setup
```

This creates `.venv/` with the locked Python packages, the pinned shdoc, and a
pinned BitBake checkout whose parser finds the functions in recipes. On Windows,
run the walkthrough in WSL.

## 3. Install the test browser

On Ubuntu, install Chromium's system libraries, then the user-local browser:

```sh
sudo .venv/bin/playwright install-deps chromium
make -f docs/source/Makefile browser
```

On macOS, run only the `make` command. A system `chromium` on `PATH` is used
instead when present.

## 4. Edit and check

Edit the Markdown under `docs/source/`, then build and check the site:

```sh
make -f docs/source/Makefile check
```

Expected result: exit status 0, a line starting `Reference coverage:` and ending
`documented and rendered.`, `docs/site/index.html`, and a JSON line with
`"network_requests": []` and `"browser_errors": []`. The check opens every page
of a copied site through `file://` with networking disabled, follows local
links and anchors, and clicks a search result. The documentation CI job runs
the same targets. `make -f docs/source/Makefile html` builds the ignored
`docs/site/` without the browser check.

## Function reference

[test_reference_coverage.py](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006b/.github/test_reference_coverage.py)
stops the build on an undocumented function, a missing rendered entry, or a
format it cannot read. It parses shell scripts and workflow `run` steps with
tree-sitter-bash, Python with `ast`, and recipes, appends, classes, and include
files with BitBake's parser; BitBake and kas configuration must hold no
function definitions.

Document a shell function or BitBake shell task with shdoc's `@description`,
`@arg` or `@noargs`, `@exitcode`, and `@example` tags in the comment block
directly above its definition. Never put the comment inside a task body:
BitBake counts the body, comments included, in the task signature. A BitBake
Python function has no configured renderer yet, so the build stops until one is
added. Python helpers take docstrings with an `Example` section.

## Update the documentation tools

`docs/source/requirements.txt` declares the documentation packages, and
`docs/source/requirements.lock` pins them with their dependencies. After an
intentional update, regenerate the lock with
`uv pip compile --python-version 3.12 docs/source/requirements.txt -o docs/source/requirements.lock`,
run `setup`, and rebuild before committing both files. The
[Makefile](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006b/docs/source/Makefile)
pins shdoc and BitBake by commit.
