# Set up your development environment

This walkthrough prepares a contributor checkout, installs the documentation
extractors, and connects to the existing kas build tutorial and CI checks.

## 1. Prepare a checkout

Use Git and a Linux host. For documentation changes, you need the documentation
tools below; image builds also need the container runtime and kas setup in the
[usage tutorial](USAGE.md#prerequisites).

```sh
git clone https://github.com/qualcomm-linux/meta-qcom-3rdparty.git
cd meta-qcom-3rdparty
git switch -c docs/my-change
```

For this documentation proposal, use your checkout of the PR branch in
`devdocsorg/meta-qcom-3rdparty`. The upstream clone acquires these documentation
files when the proposal is adopted. Keep contribution routing in the
[contribution guide](CONTRIBUTING.md).

## 2. Build the documentation

Use Make, Python 3.12 or newer, `uv`, GNU awk (`gawk`), and `curl`. From the repository root:

```sh
make -f docs/source/Makefile setup
make -f docs/source/Makefile html
```

Open `docs/site/index.html` directly in a browser, without an HTTP server. The function reference is extracted from source
comments with shdoc v1.4 during the build. Edit the comments to change the reference.
The site contains generated HTML and assets; build caches and intermediate
Markdown stay outside it.

## 3. Check the site without a server

Open `docs/site/index.html`, navigate into contributor and user pages, follow a
heading link, and return home. Search for `_is_dir` and open a function result.
Repeat with the network disabled and with `docs/site/` copied outside the checkout.
Navigation, styling, and search must still work. External
repository and upstream documentation links require connectivity.

Search shows result titles without fetching page excerpts, which browsers block
under `file://`. The site entry point redirects to the homepage generated from
`docs/source/README.md`; there is only one maintained homepage.

## 4. Prepare and validate a layer change

Follow [Prepare a layer build with kas](USAGE.md) for workspace defaults, machine
selection, metadata parsing, and image output. This is the authoritative setup
procedure for those operations; existing environment settings take precedence.

Follow the [agent and CI guide](AGENTS.md#4-run-routine-checks-via-ci-helper-scripts)
for the required patch review and layer checks. The guide also owns container
smoke tests, cache placement, and the submission check order.

## Documentation language coverage

| Maintained source | Extractor and output | Validation |
| --- | --- | --- |
| Shell functions in `ci/*.sh` | shdoc v1.4 extracts standard shell documentation comments into the contributor function reference. | The Sphinx build compares declared function names with shdoc entries and fails on missing entries. |
| Shell tasks in BitBake recipes and appends | The same shdoc extractor reads the task comments without executing BitBake or firmware tasks. | Task names must appear in the extracted reference; shell syntax and BitBake metadata remain validated by the existing CI checks. |
| Python documentation build configuration and checks | `conf.py` and the documentation checks in `.github/` currently define no Python functions or classes needing an API reference. | Adding Python functions requires a Python extractor and coverage check before the build can pass. |
| kas YAML and BitBake configuration | MyST renders the [configuration reference](../user/CONFIGURATION.md). | These are configuration settings, not function definitions; their types, defaults, and examples belong in that reference. |

Sphinx/MyST renders the prose and generated Markdown. shdoc is the language-specific
extractor. Both are installed by the build setup above. Inline calls such as
`${@bb.utils.contains_any(...)}` use upstream functions; they do not define local
Python functions. The build rejects Python function definitions in recipes until
an appropriate Python extraction path is configured, rather than silently omitting
them. New languages must add their native extractor, pinned dependencies, reference
navigation, and coverage validation together.

Edit comments beside each function to change its reference. Generated intermediate
Markdown and rendered pages are derived output, not independently maintained API
prose. The documentation CI job rebuilds from scratch, checks reference coverage,
rejects stale committed output, and tests that temporary undocumented shell
functions and unsupported Python tasks cause a build failure.

The [Makefile](../Makefile) owns dependency installation and build commands for
both local use and CI. After committing regenerated output, run
`make -f docs/source/Makefile check` to verify it reproduces.

The shared `check` target also opens a copied site with Playwright and networking
disabled. It checks navigation, anchors, resources, and a search-result click.
It uses system Chromium when available; otherwise run
`make -f docs/source/Makefile browser` to install Playwright's user-local browser.
CI installs its browser before invoking the same check target.

Direct documentation dependencies are declared in `docs/source/requirements.txt`;
`docs/source/requirements.lock` also pins their transitive dependencies. After an
intentional tool update, regenerate the lock with
`uv pip compile --python-version 3.12 docs/source/requirements.txt -o docs/source/requirements.lock`,
run setup, and rebuild before committing both source and output.

## Nearby map updates

The [nearby map at the bottom of the root README](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/devdocs/required-files-sphinx/README.md#repository-map)
shows the recorded build/component connections, including incoming links,
optional integrations, and indirect paths through their providers. Its source comment records the
central map commit and dataset digest. The
[Qualcomm repository map](https://github.com/devdocsorg/qualcomm-repository-map)
owns the relationship facts and full view. Follow its
[README export procedure](https://github.com/devdocsorg/qualcomm-repository-map/blob/main/data/README.md)
to audit build references, run the source and coverage checks, and regenerate the
marked block directly from a reviewed commit. Use `--check` to
verify that the block matches the recorded source. Access to the private map
repository is required for updates. Do not maintain a second copy of relationship
facts here.

The map lives only in the root README. Map export is independent of Sphinx;
the documentation build does not read, copy, or write the map.

The setup target recreates the documentation-only `.venv` from the lockfile.
Keep project dependencies and custom tools in their own environments.
