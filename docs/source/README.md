# meta-qcom-3rdparty Documentation

Welcome to the documentation for **meta-qcom-3rdparty**, an OpenEmbedded / Yocto layer that extends the Qualcomm Linux ecosystem by supporting community and vendor hardware platforms not officially maintained by Qualcomm.

This documentation is intended for developers, vendors, and contributors working with Qualcomm-based SoCs using the Yocto Project build system.

---

## Overview

The `meta-qcom-3rdparty` layer provides:

- Common BSP enablement for **third-party and community boards**
- **Upstream-aligned** machine support based on `meta-qcom`
- Clean, maintainable structure to avoid fragmentation across vendors
- Integration hooks for both **Qualcomm Linux 1.x** (downstream) and future **Qualcomm Linux 2.x** (upstream) releases

---

## Documentation Index

- [Contribution Guidelines](contributing/CONTRIBUTING.md) — how to contribute patches, follow Yocto conventions, and structure vendor-specific code.
- [Usage Guide](user/USAGE.md) — how to include and build the layer, add it to your workspace, and inspect target builds.
- [Supported Machines](https://github.com/devdocsorg/meta-qcom-3rdparty/tree/docs/contributor-reference/conf/machine) — machine configurations and board-specific settings.
- [Developer Notes](contributing/DEVELOPMENT.md) — development setup, CI integration, and required checks.

---

## Quick Start

To build a reference image using [kas](https://kas.readthedocs.io/):

```bash
kas-container build meta-qcom-3rdparty/ci/rubikpi3.yml
```

Otherwise add this layer to your existing Yocto environment:

```bash
git clone https://github.com/qualcomm-linux/meta-qcom-3rdparty.git
bitbake-layers add-layer ../meta-qcom-3rdparty
```

---

## Related Layers and References

- [meta-qcom](https://github.com/qualcomm-linux/meta-qcom)
- [meta-qcom-hwe](https://github.com/qualcomm-linux/meta-qcom-hwe)
- [meta-qcom-distro](https://github.com/qualcomm-linux/meta-qcom-distro)
- [OpenEmbedded Layer Index](https://layers.openembedded.org/layerindex/)
- [Yocto Project Documentation](https://docs.yoctoproject.org/)

---

**SPDX-License-Identifier:** MIT

```{toctree}
:hidden:

contributing/README
user/README
```

## Folders

- [.templates/](https://github.com/devdocsorg/meta-qcom-3rdparty/tree/docs/contributor-reference/docs/source/.templates) — Contains the generated offline site entry template.
- [contributing/](contributing/README.md) — Contribution procedures, development setup, agent instructions, and generated native reference.
- [user/](user/README.md) — User tutorial and configuration reference.

## Files

- [Makefile](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/contributor-reference/docs/source/Makefile) — Provides shared documentation setup, build, browser, and check targets.
- [README.md](README.md) — Describes this folder and indexes its contents.
- [conf.py](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/contributor-reference/docs/source/conf.py) — Configures Sphinx, offline browsing, and native extraction.
- [requirements.lock](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/contributor-reference/docs/source/requirements.lock) — Locks all resolved Python documentation dependencies.
- [requirements.txt](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/contributor-reference/docs/source/requirements.txt) — Declares pinned documentation dependencies.
