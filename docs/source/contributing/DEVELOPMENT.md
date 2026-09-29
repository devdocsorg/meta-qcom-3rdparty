# Set up your development environment

This walkthrough prepares a checkout, builds and checks the documentation, and
runs the layer checks that CI runs before a change is merged.

## Prerequisites

- Git, GNU Make, GNU Awk (for shdoc), curl, and
  [uv](https://docs.astral.sh/uv/getting-started/installation/) 0.12.3, which
  installs Python 3.12 for the documentation tools.
- Chromium for the offline site check, or run
  `make -f docs/source/Makefile browser` to install Playwright's copy.
- For layer builds and checks: the tools in the agent guide's
  [prerequisites](AGENTS.md#1-prerequisites), kas-container 4.8.2, and Docker
  or Podman.

Dependency installation needs network access; reading the built site does not.

## 1. Clone and create a branch

```sh
git clone --branch docs/layer-documentation https://github.com/devdocsorg/meta-qcom-3rdparty.git
cd meta-qcom-3rdparty
git switch -c my-change
```

This branch carries the documentation tools. Send the finished change where the
[contribution guide](CONTRIBUTING.md#28--branch-destinations) says.

## 2. Install the documentation tools

```sh
make -f docs/source/Makefile setup
```

The `setup` target recreates `.venv/` with the locked Python packages, the
pinned shdoc, and the pinned BitBake parser. Expected result: exit status 0 and
`.venv/bin/sphinx-build`. `.venv/` is ignored by Git.

## 3. Configure

The documentation build reads no settings. Layer builds and checks read the
optional paths in [.env.example](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/.env.example);
export them as the agent guide's [recommended environment](AGENTS.md#2-recommended-environment)
shows.

## 4. Build and check the documentation

```sh
make -f docs/source/Makefile check
```

`check` rebuilds the site with warnings as errors, fails when a shell function
or BitBake task lacks a documented and rendered reference entry, and opens a
copy of the site in headless Chromium with networking disabled. Expected
result: exit status 0 and a final JSON line with `"network_requests": []` and
`"browser_errors": []`. Open `docs/site/index.html` directly in a browser to
read the site; `make -f docs/source/Makefile html` rebuilds it without the
browser check.

Document a new shell function or BitBake task with shdoc's `@description`,
`@arg` or `@noargs`, `@exitcode`, and `@example` comments directly above its
definition, never inside a task body, where comments become part of the task
signature. Python helpers take Google-style docstrings with an `Example`
section. [test_reference_coverage.py](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/.github/test_reference_coverage.py)
finds the functions and stops the build on an undocumented function or an
unsupported format.

## 5. Run the layer checks

Run the CI helper checks in the order and at the times the agent guide's
[routine checks](AGENTS.md#4-run-routine-checks-via-ci-helper-scripts) give:
`yocto-patchreview` routinely, and `yocto-check-layer` before opening or
updating a pull request. Each exits with status 0 when the layer passes. The
[usage tutorial](../user/USAGE.md) builds an image.

## Update the tools

The [Makefile](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/docs/source/Makefile)
pins shdoc and BitBake. `docs/source/requirements.txt` declares the Python
packages and `docs/source/requirements.lock` pins them with their dependencies.
After changing a requirement, regenerate the lock, run `setup`, and rebuild:

```sh
uv pip compile --python-version 3.12 docs/source/requirements.txt -o docs/source/requirements.lock
```

## Repository map

The map at the end of the root README is exported from the
[Qualcomm repository map](https://github.com/devdocsorg/qualcomm-repository-map),
which records the evidence for each connection. Updating it needs access to that
repository; follow its
[update procedure](https://github.com/devdocsorg/qualcomm-repository-map/blob/main/data/README.md)
and regenerate the block with its exporter instead of editing it by hand.
