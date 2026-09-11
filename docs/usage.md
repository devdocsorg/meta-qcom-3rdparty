# Usage Guide

`meta-qcom-3rdparty` is an OpenEmbedded / Yocto Project BSP layer for third-party maintained Qualcomm based platforms. `conf/layer.conf` registers it as the BitBake collection `qcom-3rdparty` at priority 5, declares `LAYERDEPENDS_qcom-3rdparty = "core qcom"` and sets `LAYERSERIES_COMPAT_qcom-3rdparty = "wrynose"`: a build needs [OpenEmbedded-Core](https://github.com/openembedded/openembedded-core) and [meta-qcom](https://github.com/qualcomm-linux/meta-qcom) alongside it, on that Yocto Project series. The kas fragments under `ci/` pin `meta-qcom` to its `master` branch (`ci/meta-qcom.yml`).

---

## Prerequisites

Sections 1 and 2 of [AGENTS.md](../AGENTS.md) cover what every command below expects: `kas-container` on `PATH`, a working container runtime, and build and cache directories outside the checkout.

---

## Building with kas

[kas](https://kas.readthedocs.io/en/latest/userguide/project-configuration.html) composes small YAML fragments into one build configuration, and `ci/` holds this layer's. The fragments a local build composes:

- `base.yml` includes meta-qcom's `ci/base.yml`, pins the `meta-qcom` repository to `master`, and declares this layer itself, which kas resolves to the checkout it runs from.
- `<machine>.yml` includes `base.yml` and sets `machine` to one board. There is one fragment per machine, named after it.
- `qcom-distro.yml` includes meta-qcom's fragment of the same name, which selects the `qcom-distro` distribution policy and adds the layers it needs. Without it a build uses `nodistro`; the build matrix in `.github/workflows/build-yocto.yml` runs `nodistro` and `qcom-distro`.
- `linux-qcom-next.yml` sets `PREFERRED_PROVIDER_virtual/kernel` to `linux-qcom-next` with a hard assignment, overriding the weak default a machine configuration sets.
- `mirror.yml` includes meta-qcom's `ci/mirror.yml`, which adds meta-qcom's sstate mirror to a build that names it on the kas command line.
- `world.yml` sets `EXCLUDE_FROM_WORLD` to `1` for every layer and back to `0` for `layer-qcom` and `layer-qcom-3rdparty`, and names `world` as the target, so a world build covers the recipes those layers provide.

Fragments compose on the kas command line, separated by colons, in the `:ci/<machine>.yml[:distro.yml]` composition pattern that section 3 of [AGENTS.md](../AGENTS.md) documents: a machine fragment first and a distro fragment after it when one is wanted. Building the Thundercomm RUBIK Pi 3 (QCS6490), machine `rubikpi3`, with the Qualcomm distro:

```bash
kas-container build ci/rubikpi3.yml:ci/qcom-distro.yml
```

To run kas natively on the host instead of in a container, install kas and use `kas build` in place of `kas-container build`.

The world build section 3 of [AGENTS.md](../AGENTS.md) documents, "World build (all machines in this layer)", takes the base fragment rather than a machine one:

```bash
kas-container build ci/base.yml:ci/world.yml
```

---

## Adding the Layer to an Existing Build

An existing Yocto build takes the layer the way the Quick Start in [index.md](index.md) shows:

```bash
git clone https://github.com/qualcomm-linux/meta-qcom-3rdparty.git
bitbake-layers add-layer ../meta-qcom-3rdparty
```

Two entries in `conf/layer.conf` decide whether that build then parses. `LAYERDEPENDS_qcom-3rdparty` names `core` and `qcom`, so OpenEmbedded-Core and `meta-qcom` have to be in `bblayers.conf` already, and `LAYERSERIES_COMPAT_qcom-3rdparty` limits the layer to the `wrynose` series.

A project that already builds with kas has a shorter route: declare this layer under `repos:` in its own kas file and include `ci/base.yml` through that entry, which brings `meta-qcom` in with it; a bare `ci/base.yml` path would resolve inside the including repository instead.

```yaml
header:
  includes:
    - repo: meta-qcom-3rdparty
      file: ci/base.yml
```

---

## Choosing a Machine

[supported-machines.md](supported-machines.md) is the list. A board's `MACHINE` value is the basename of its `conf/machine/<machine>.conf` file, and its kas fragment `ci/<machine>.yml` carries the same name, so one string identifies the board on either route. The direct kas shell example in section 5 of [AGENTS.md](../AGENTS.md) builds `core-image-base`. What a board needs beyond the SoC baseline, and why, is in the comments of its own machine configuration.

---

## Flashing

Images built from this layer are flashed with the tools meta-qcom documents. Its [flashing guide](https://github.com/qualcomm-linux/meta-qcom/blob/master/docs/flashing.md) covers building the QDL tool, preparing the board, and flashing images over USB in EDL mode.

---

## Validating a Build

The checks to run before opening a pull request, and the local commands that match what CI runs, are in [developer.md](developer.md).

---

**SPDX-License-Identifier:** MIT
