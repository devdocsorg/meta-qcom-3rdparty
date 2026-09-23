# Development environment

## Checkout and prerequisites

The runnable documentation proposal is in this fork and branch:

```sh
git clone --branch docs/offline-guides-and-layer-map https://github.com/devdocsorg/meta-qcom-3rdparty.git
cd meta-qcom-3rdparty
```

Contributions to the BSP still go to the upstream project through the
[contribution procedure](CONTRIBUTING.md). Use Linux, Git, Make, GNU Awk
(tested with 5.4.1), and [uv 0.12.3](https://docs.astral.sh/uv/getting-started/installation/).
The documentation setup installs Python 3.12.13 and the locked Python tools locally.
It fetches pinned shdoc and BitBake parsers into `.docs-tools/`; neither executes
build tasks. Internet access is needed for setup, not for browsing the built site.

For image builds and layer checks, use kas-container 4.8.2 and Docker or Podman.
Follow the [agent guide's prerequisites and runtime smoke tests](AGENTS.md#1-prerequisites)
in their stated order, then its [external work/cache directory setup](AGENTS.md#2-recommended-environment).
The environment settings are explained in [Configuration](../user/CONFIGURATION.md#environment).

## Documentation

From the checkout root:

```sh
make -f docs/source/Makefile setup
# Only when Chromium is not already installed:
make -f docs/source/Makefile browser
make -f docs/source/Makefile check
```

`check` rebuilds strictly, verifies native reference coverage, opens a copied site
with networking disabled, exercises search and navigation, and checks generated
output against Git. A clean checkout should finish without changes.
For documentation edits, build with `make -f docs/source/Makefile html`, inspect
`docs/site/index.html` directly in a browser, and commit sources and regenerated
output before running `check`. The browser test is headless and starts no server.

The shell comments use [shdoc annotations](https://github.com/reconquest/shdoc/tree/52917b2f3471fe77c745ede115494d2d5c9168d1#features).
Give each function a description, typed arguments or `@noargs`, exit status, and
example. Blank comment lines separate examples from subsequent annotations.
Python helpers use typed signatures and standard docstrings with examples;
Sphinx autodoc imports the safe documentation extension itself. New unsupported
source languages or embedded Python tasks stop the build with extractor setup
instructions. BitBake statement parsing covers `.bb`, `.bbappend`, `.bbclass`,
`.inc`, and `.conf`, including modified task names, without evaluating metadata.

## Layer checks

Run the [routine patch review](AGENTS.md#4-run-routine-checks-via-ci-helper-scripts).
Before opening or updating every pull request, run the
[two CI helpers in order](AGENTS.md#6-pull-request--contribution-workflow):
patch review, then layer checking. This also applies to documentation proposals.
Both return success on completion; the layer checker uses a temporary build and
clones the committed checkout, so commit changes before validating the candidate.
Full image and hardware validation remain necessary for BSP changes; the
[image tutorial](../user/USAGE.md) explains the output to inspect.

## Repository map

The map is maintained by DevDocs in the private
[shared repository](https://github.com/devdocsorg/qualcomm-repository-map).
Request access from its maintainers, follow `data/README.md` there, and run its
coverage and source checks before exporting the canonical
`qualcomm-linux/meta-qcom-3rdparty` view at a committed revision to the root README.
Map export is independent of Sphinx. The README export comment records the exact
revision and digest needed to reproduce it.
