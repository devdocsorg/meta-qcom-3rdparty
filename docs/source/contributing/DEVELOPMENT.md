# Set up your development environment

This walkthrough installs the documentation tools, builds this site with its
function reference, and runs the documentation checks. Layer changes also need
the builds and checks in the [agent guide](AGENTS.md), described
[below](#check-layer-changes).

## Prerequisites

Git, GNU Make, GNU Awk (runs shdoc), curl, Python 3.12, and
[uv](https://docs.astral.sh/uv/getting-started/installation/) (tested with
0.12.3), plus Chromium for the browser check. Setup needs network access; reading
the built site does not. On Windows, use WSL.

## 1. Clone

```sh
git clone --branch docs/layer-documentation https://github.com/devdocsorg/meta-qcom-3rdparty.git
cd meta-qcom-3rdparty
```

This review branch carries the documentation tools. Send changes where the
[contribution guide](CONTRIBUTING.md) says.

## 2. Install the documentation tools

```sh
make -f docs/source/Makefile setup
```

This creates `.venv` with the locked Python packages from
[requirements.lock](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/docs/source/requirements.lock),
shdoc (checked against its SHA-256), and BitBake's parser at the commit the
[Makefile](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/docs/source/Makefile)
pins. The documentation build needs no other configuration; `.gitignore` keeps
`.venv` out of commits. If Chromium is not installed, also run
`make -f docs/source/Makefile browser`.

## 3. Edit and build

Edit the Markdown under `docs/source/`, or a function's documentation comment,
then build:

```sh
make -f docs/source/Makefile html
```

Expected result: exit status 0, `Reference coverage: ... documented and rendered.`,
and a regenerated `docs/site/`. The build fails on a function without a complete
comment, a function missing from the rendered reference, or a source format it
cannot read.

## 4. Check and commit

Stage the source and the regenerated site together, then run:

```sh
make -f docs/source/Makefile check
```

The check rebuilds the site, opens a copy of it in headless Chromium with
networking disabled, and then fails if `docs/site/` differs from what you staged.
Expected result: exit status 0 and a JSON summary with no `browser_errors` and
no `network_requests`. CI runs the same `setup` and `check` targets.

## Document functions

Shell scripts and BitBake shell tasks take a shdoc comment block directly above
the definition, with `@description`, `@arg` or `@noargs`, `@exitcode`, and
`@example`. In BitBake files, never put the block inside the task: the body,
comments included, is part of the task signature. Python helpers take
Google-style docstrings with an `Example` section, rendered by autodoc. The
build names BitBake Python functions and shell functions nested in a task and
fails, because no renderer is configured for them;
[test_reference_coverage.py](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/.github/test_reference_coverage.py)
is where to add one.

After an intentional tool update, regenerate the lock with
`uv pip compile --python-version 3.12 docs/source/requirements.txt -o docs/source/requirements.lock`,
run setup, and rebuild.

## Check layer changes

For changes to recipes, machines, or kas files, follow the agent guide:
[prerequisites](AGENTS.md#1-prerequisites) and
[environment](AGENTS.md#2-recommended-environment) (see
[environment settings](../user/CONFIGURATION.md#environment-settings)), a
[CI-style build](AGENTS.md#3-build-with-kas-container-ci-style), and
[the checks](AGENTS.md#4-run-routine-checks-via-ci-helper-scripts):
`yocto-patchreview` routinely, and `yocto-check-layer` before opening or updating
a pull request. CI runs both for pull requests to `main` that change more than
Markdown.
