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
- [Usage Guide](user/USAGE.md) — how to include and build the layer, add it to your workspace, and validate target builds.
- [Supported Machines](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/offline-layer-guides/conf/machine/README.md) — list of currently supported platforms, vendors, and hardware status.
- [Developer Notes](contributing/DEVELOPMENT.md) — additional details for maintainers, CI integration, and testing recommendations.

---

## Quick Start

To build a reference image using [kas](https://kas.readthedocs.io/):

```bash
kas build meta-qcom-3rdparty/ci/rubikpi3.yml
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
```

<!-- folder-index:start -->

## Folders

- [.templates](https://github.com/devdocsorg/meta-qcom-3rdparty/tree/docs/offline-layer-guides/docs/source/.templates) — Contains the generated site entry template.
- [contributing](contributing/README.md) — Explains contributor setup and provides generated function reference.
- [user](user/README.md) — Explains image use and configuration.

## Files

- [Makefile](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/offline-layer-guides/docs/source/Makefile) — Provides the shared setup, build, browser, and check commands.
- [README.md](README.md) — Introduces this folder and indexes its immediate contents.
- [conf.py](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/offline-layer-guides/docs/source/conf.py) — Configures Sphinx, MyST, autodoc, and native reference generation.
- [requirements.lock](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/offline-layer-guides/docs/source/requirements.lock) — Locks every Python documentation dependency version.
- [requirements.txt](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/offline-layer-guides/docs/source/requirements.txt) — Declares pinned documentation tools and the independent shell parser.

<!-- folder-index:end -->
