# Set up your development environment

This walkthrough installs the documentation tools, builds the site and function
reference, and runs the same check as CI. Layer builds and the checks required
before a pull request use kas-container; the [agent guide](AGENTS.md) owns that
procedure.

## Prerequisites

Tested on Linux with Git 2.55, GNU Make 4.4, GNU Awk 5.4 (shdoc runs on it),
curl 8, Python 3.12, and [uv](https://docs.astral.sh/uv/getting-started/installation/)
0.12. Setup needs network access. The browser check uses Chromium when it is
installed; otherwise run `make -f docs/source/Makefile browser` after setup to
install Playwright's copy. On Windows, use WSL.

## 1. Clone and create a branch

```sh
git clone https://github.com/qualcomm-linux/meta-qcom-3rdparty.git
cd meta-qcom-3rdparty
git switch -c docs/my-change
```

While this documentation is under review, clone
`https://github.com/devdocsorg/meta-qcom-3rdparty.git` with
`--branch docs/offline-layer-docs` instead. Contributions still go to `main` of
`qualcomm-linux/meta-qcom-3rdparty`.

## 2. Install the documentation tools

```sh
make -f docs/source/Makefile setup
```

This creates `.venv/` with the locked Sphinx, MyST, bashlex, and Playwright
packages, BitBake 2.16.0 (its parser reads recipe tasks), and shdoc 1.4.
Expected result: exit status 0 and an executable `.venv/bin/shdoc`.

## 3. Check your change

```sh
make -f docs/source/Makefile check
```

`check` rebuilds `docs/site/`, checks the function reference, opens a copy of
the site in headless Chromium with networking disabled, and compares the result
with the committed site. Expected result: exit status 0 after these lines:

```text
Reference coverage: 4 functions in 4 files documented and rendered
{"site": ".../docs/site", "pages": 14, "search": "rubikpi3", "result": "...", "network_requests": [], "browser_errors": []}
```

The check fails while regenerated output is uncommitted: commit the source and
`docs/site/` together, then run it again. `make -f docs/source/Makefile html`
only rebuilds; open `docs/site/index.html` directly in a browser to read it.

## Document a function

Shell functions in scripts, BitBake shell tasks, and workflow `run` steps use
[shdoc](https://github.com/reconquest/shdoc/tree/v1.4) comments:

```sh
# @description Say in one sentence what the function does.
# @arg $1 string What the first argument holds.
# @exitcode 0 When it succeeds.
# @example
#   my_function value
my_function() {
```

Use `# @noargs` instead of `@arg` when the function reads no positional
parameters. The build fails when a function has no such comment or no rendered
entry, when its documented arguments do not match the parameters it reads, and
for definitions no extractor covers, such as Python in BitBake files or a new
language. Configure an extractor for new languages in `docs/source/conf.py` and
`.github/test_reference_coverage.py`.

## Layer checks

Run the checks the agent guide lists
[before opening or updating a pull request](AGENTS.md#6-pull-request--contribution-workflow),
in the order given there. Pull requests also run markdownlint with
`.github/.markdownlint.yaml` and BitBake lint; the
[configuration reference](../user/CONFIGURATION.md#repository-automation)
lists every workflow.

## Update pinned tools

Python packages are pinned in `docs/source/requirements.txt`, and BitBake and
shdoc in `docs/source/Makefile`. After changing a package version, regenerate the
lock, then run setup and check again:

```sh
uv pip compile --python-version 3.12 docs/source/requirements.txt -o docs/source/requirements.lock
```

The repository map at the end of the root README is generated from the shared
[Qualcomm repository map](https://github.com/devdocsorg/qualcomm-repository-map);
updating it requires access to that repository.
