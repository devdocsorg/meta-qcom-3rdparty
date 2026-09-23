# Development setup

## Checkout and prerequisites

Use Linux (or WSL), Git, Make, curl, a C compiler, tar/xz, and
[uv 0.12.3](https://docs.astral.sh/uv/getting-started/installation/).
The documentation setup selects Python 3.12.13 and installs locked packages;
GNU Awk 5.4.1 is reused when installed, or built in `docs/.tools` by setup. Dependency installation needs network access.

This proposal’s runnable checkout contains the documentation commands below:

```sh
git clone --branch docs/offline-contributor-guides https://github.com/devdocsorg/meta-qcom-3rdparty.git
cd meta-qcom-3rdparty
git switch -c docs/my-change
make -f docs/source/Makefile setup
```

The setup recreates `.venv` and prepares GNU Awk 5.4.1 and shdoc v1.4 at fixed
versions with SHA-256 checks. Sphinx 9.1.0, MyST 5.1.0, Playwright 1.62.0, and bashlex 0.18
are pinned in the documentation requirements; the lock also pins transitive
packages. Tools and intermediate files stay outside the committed site.

For layer checks, use kas-container 4.8.2 and Docker or Podman. Inspect existing
installations first; the [kas installation guide](https://kas.readthedocs.io/en/4.8.2/userguide/getting-started.html#dependencies-installation)
provides the official container wrapper. Follow the
[agent guide’s runtime smoke test and environment setup](AGENTS.md#1-prerequisites)
in order: Docker first, then Podman when installed. Preserve existing cache
settings. The {download}`environment example <../../../.env.example>`
and [configuration reference](../user/CONFIGURATION.md) explain local controls.

## Edit and check

Edit `docs/source/` and keep folder indexes current. Shell functions use shdoc
comments with a purpose, typed arguments or `@noargs`, an example, and exit codes.
Python tooling uses native reStructuredText docstrings and safe module imports.
Sphinx calls the extractor; bashlex and Python’s AST independently discover
functions. Missing comments, missing rendered entries, or unsupported definitions
fail validation. [The generated reference](README.md#function-reference) includes
internal helpers. No BitBake task is executed by documentation extraction.

When the source edits are ready, generate the output once, then stage and commit
both source and site. The separate build-only command is:

```sh
make -f docs/source/Makefile html
```

Expected result: exit status 0 and `docs/site/index.html`. Open that file directly;
all local navigation and search work without a server. External source and policy
links still require a network connection.

After committing, run the shared check, which rebuilds automatically:

```sh
make -f docs/source/Makefile check
```

The check validates every reference, exercises coverage regressions, copies only
the site to a temporary directory, and opens it with networking disabled. It
checks links, anchors, assets, browser errors, and a search-result click. It also
rejects changed or untracked output. If system Chromium is unavailable, first run
`make -f docs/source/Makefile browser` to install Playwright’s user-local browser.
CI uses the same Makefile targets.

Before opening or updating **every pull request**, also follow
[the agent guide’s required checks](AGENTS.md):
run patchreview, then yocto-check-layer, using the helpers from the repository root.
Commit first: yocto-check-layer clones the current repository and tests committed
HEAD. Inspect the cloned revision when reporting results. Documentation checks do
not replace these checks. For functional board changes, the contribution guide
also requires an image build and hardware validation; report what was exercised.

The existing CI runs Markdown lint, advisory BitBake lint for changed metadata,
and Qualcomm preflight with the upstream repolinter rules. Its Yocto build matrix
runs on Qualcomm-owned runners; fork execution does not establish image coverage.

## Maintain the tools and map

After an intentional Python dependency change, regenerate the lock, rerun setup,
and commit the regenerated site:

```sh
uv pip compile --python-version 3.12 docs/source/requirements.txt -o docs/source/requirements.lock
make -f docs/source/Makefile setup
```

The [Makefile](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/offline-contributor-guides/docs/source/Makefile)
owns setup and checks. The versions and digests in `.github/setup_tools.sh` must change together after
reviewing the upstream release. The [documentation specification](https://github.com/devdocsorg/qli2-example-repo/blob/968509ed451e7f7241fdef6703b648a89fb50031/SPECIFICATION.md)
owns the scaffold requirements.

Repository map maintenance needs access to the private shared map repository.
Follow its [dataset procedure](https://github.com/devdocsorg/qualcomm-repository-map/blob/main/data/README.md),
audit build references, run both shared checks, and export the canonical identity
`qualcomm-linux/meta-qcom-3rdparty` into the root README from a committed revision.
Map export is separate from Sphinx; do not add map pages or copies to the site.
