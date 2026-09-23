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
- [Usage Guide](user/USAGE.md) — build a board image and locate the output.
- [Supported Machines](user/USAGE.md#other-machines-and-existing-workspaces) — board choices and firmware boundaries.
- [Development Setup](contributing/DEVELOPMENT.md) — prepare tools and run the required checks.

---

## Quick Start

After [development setup](contributing/DEVELOPMENT.md), build a reference image
from the checkout root using [kas](https://kas.readthedocs.io/):

```bash
kas-container build ci/rubikpi3.yml
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

user/README
contributing/README
NOTICES
```

## Folders

- [.templates](https://github.com/devdocsorg/meta-qcom-3rdparty/tree/docs/offline-contributor-guides/docs/source/.templates) — Contains documentation entry templates.
- [contributing](contributing/README.md) — Explains contribution procedures, setup, and native function references.
- [user](user/README.md) — Explains image builds and local configuration choices.

## Files

- [Makefile](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/offline-contributor-guides/docs/source/Makefile) — Provides the shared setup, build, browser, and validation targets.
- [NOTICES.md](NOTICES.md) — Preserves the reused scaffold’s full licence notices.
- [README.md](README.md) — Describes this folder and indexes its immediate contents.
- [conf.py](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/offline-contributor-guides/docs/source/conf.py) — Configures Sphinx, MyST, autodoc, and shell reference extraction.
- [requirements.lock](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/offline-contributor-guides/docs/source/requirements.lock) — Pins the resolved Python documentation toolchain.
- [requirements.txt](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/offline-contributor-guides/docs/source/requirements.txt) — Declares exact direct documentation dependencies.
