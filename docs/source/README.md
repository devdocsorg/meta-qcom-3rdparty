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
- [Supported Machines](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/offline-layer-documentation/conf/machine/README.md) — list of currently supported platforms, vendors, and hardware status.
- [Developer Notes](contributing/DEVELOPMENT.md) — development environment, documentation checks, and CI integration.
- [Configuration Reference](user/CONFIGURATION.md) — layer, machine, kas, and workflow settings.
- [Agent Guide](contributing/AGENTS.md) — kas-container builds and the checks to run before a pull request.
- [Function Reference](contributing/README.md#function-reference) — generated from the documentation comments in scripts and recipes.

---

## Quick Start

Follow the [usage tutorial](user/USAGE.md) to build an image with kas or add
the layer to an existing Yocto environment.

---

## Related Layers and References

- [meta-qcom](https://github.com/qualcomm-linux/meta-qcom)
- [meta-qcom-hwe](https://github.com/qualcomm-linux/meta-qcom-hwe)
- [meta-qcom-distro](https://github.com/qualcomm-linux/meta-qcom-distro)
- [OpenEmbedded Layer Index](https://layers.openembedded.org/layerindex/)
- [Yocto Project Documentation](https://docs.yoctoproject.org/)

```{toctree}
:hidden:

user/README
contributing/README
```

## Folders

- [user/](user/README.md) — Holds the usage tutorial and the configuration reference.
- [contributing/](contributing/README.md) — Holds the contribution, development, and agent guides and the function reference.
- [.templates/](https://github.com/devdocsorg/meta-qcom-3rdparty/tree/docs/offline-layer-documentation/docs/source/.templates) — Supplies the generated site's entry-point redirect.

## Files

- [README.md](README.md) — Introduces the layer documentation and supplies the site's homepage.
- [conf.py](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/offline-layer-documentation/docs/source/conf.py) — Configures Sphinx and MyST and generates the function reference pages.
- [Makefile](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/offline-layer-documentation/docs/source/Makefile) — Provides the shared local and CI setup, build, and check targets.
- [requirements.txt](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/offline-layer-documentation/docs/source/requirements.txt) — Declares the documentation packages at exact versions.
- [requirements.lock](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/offline-layer-documentation/docs/source/requirements.lock) — Locks direct and transitive documentation packages.

---

**SPDX-License-Identifier:** MIT
