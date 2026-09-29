# Set up your development environment

This walkthrough prepares a checkout, runs the layer checks that CI runs, and
builds this documentation with its function reference.

## Prerequisites

- Git, GNU Make, curl, and GNU Awk, which runs
  [shdoc](https://github.com/reconquest/shdoc).
- For the layer checks: kas-container with Docker or Podman, as listed in the
  agent guide's [prerequisites](AGENTS.md#1-prerequisites).
- For the documentation: Python 3.12 or newer and
  [uv](https://docs.astral.sh/uv/getting-started/installation/) (tested with uv
  0.12.3), and Chromium for the offline check. Setup needs network access;
  reading the built site does not.

## 1. Clone and create a branch

```sh
git clone -b docs/layer-documentation https://github.com/devdocsorg/meta-qcom-3rdparty.git
cd meta-qcom-3rdparty
git switch -c my-change
```

This branch holds the proposed documentation tools. Once they reach the
project, clone [meta-qcom-3rdparty](https://github.com/qualcomm-linux/meta-qcom-3rdparty)
`main` instead. The [contribution guide](CONTRIBUTING.md#27--submitting-changes)
says where to send changes.

## 2. Configure the environment

Export the kas settings you need from
[.env.example](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/.env.example),
keeping the work, download, and shared-state directories outside the checkout.
All of them are optional.

## 3. Check the layer

Follow the agent guide to
[build with kas-container](AGENTS.md#3-build-with-kas-container-ci-style) and to
[run the checks](AGENTS.md#4-run-routine-checks-via-ci-helper-scripts) through
the CI helper scripts. Run `yocto-patchreview` routinely. Before opening or
updating a pull request, run `yocto-patchreview` and then `yocto-check-layer`,
in that order, as CI does.

Expected result: each helper exits with status 0. `yocto-patchreview` fails when
a patch has a malformed `Signed-off-by` or `Upstream-Status`.

## 4. Build and check the documentation

```sh
make -f docs/source/Makefile setup
make -f docs/source/Makefile check
```

`setup` creates `.venv` with the locked Python packages, the pinned shdoc, and
the pinned BitBake parser. `check` rebuilds the site with warnings treated as
errors, checks the function reference, and opens a copied site in headless
Chromium with networking disabled. Without a system Chromium, run
`make -f docs/source/Makefile browser` once first.

Expected result: exit status 0, a `Reference coverage:` line saying every
function is documented and rendered, and a JSON line from the offline check
with empty `network_requests` and `browser_errors`. Open `docs/site/index.html`
directly in a browser; `docs/site/` is ignored by Git. The
[documentation workflow](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/.github/workflows/documentation.yml)
runs the same targets, and
[markdownlint](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/.github/workflows/markdownlint.yml)
checks every Markdown file.

## Document functions

[test_reference_coverage.py](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/.github/test_reference_coverage.py)
finds every function with parsers, without running anything, and stops the build
when one lacks documentation or a rendered entry, or when a file format has no
configured extractor.

- Shell functions and BitBake shell tasks take a shdoc comment block directly
  above the definition: `@description`, `@arg` or `@noargs`, `@exitcode`, and
  `@example`. Never put it inside a task body: body text is part of the task
  signature.
- Python functions take Google-style docstrings with an `Example` section.
- BitBake Python functions and nested shell functions in tasks have no
  configured renderer yet; the build names them until one is added.

After an intentional documentation-tool update, regenerate the lock with
`uv pip compile --python-version 3.12 docs/source/requirements.txt -o docs/source/requirements.lock`,
run setup, and rebuild before committing the requirements and lock.
