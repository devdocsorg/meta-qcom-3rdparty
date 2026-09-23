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
- [Usage Guide](user/USAGE.md) — how to include and build the layer and inspect its image output.
- [Supported Machines](user/CONFIGURATION.md#machines) — board configurations and boot differences.
- [Developer Notes](contributing/DEVELOPMENT.md) — setup, CI checks, and generated reference.

---

## Quick Start

To build a reference image using [kas](https://kas.readthedocs.io/), run this
from the checkout’s parent directory and replace `<machine.yml>` with a board
fragment such as `rubikpi3.yml`:

```bash
kas build meta-qcom-3rdparty/ci/<machine.yml>
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

## Folders

- [.templates](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/offline-guides-and-layer-map/docs/source/.templates) — Contains the generated-site entry template.
- [contributing](contributing/README.md) — Provides contribution procedures, setup, and native references.
- [user](user/README.md) — Explains image use and configuration.

## Files

- [Makefile](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/offline-guides-and-layer-map/docs/source/Makefile) — Provides shared setup, build, browser, and check targets.
- [README.md](README.md) — Orients readers and indexes this folder.
- [conf.py](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/offline-guides-and-layer-map/docs/source/conf.py) — Configures strict Sphinx, MyST, and native extraction.
- [requirements.lock](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/offline-guides-and-layer-map/docs/source/requirements.lock) — Pins the resolved documentation environment.
- [requirements.txt](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/offline-guides-and-layer-map/docs/source/requirements.txt) — Pins direct Python documentation dependencies.

```{toctree}
:hidden:

user/README
contributing/README
```
