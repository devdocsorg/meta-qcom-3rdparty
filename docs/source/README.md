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
- [Supported Machines](user/CONFIGURATION.md#machine-configuration) — list of currently supported platforms, vendors, and their machine settings.
- [Developer Notes](contributing/DEVELOPMENT.md) — additional details for maintainers, CI integration, and testing recommendations.
- [Configuration Reference](user/CONFIGURATION.md) — what each layer, machine, kas, and environment setting does.
- [Function Reference](contributing/README.md#function-reference) — shell functions and BitBake tasks, generated from their source comments.
- [Agent Guide](contributing/AGENTS.md) — how automation agents build and check the layer the way CI does.

The repository [README](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/main/README.md)
remains the project entry point, with branches, maintainers, and the repository map.

```{toctree}
:hidden:

user/README
contributing/README
```

---

## Quick Start

To build a reference image using [kas](https://kas.readthedocs.io/):

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

## Folders

- [user/](user/README.md) — Contains the usage tutorial and configuration reference.
- [contributing/](contributing/README.md) — Contains contributor, development, and agent guides and the function reference.
- [.templates/](.templates/index.html) — Supplies the generated site's entry-point redirect.

## Files

- [README.md](README.md) — Introduces the layer documentation and supplies the site homepage.
- [conf.py](conf.py) — Configures Markdown rendering, local navigation, search, and function reference generation.
- [Makefile](Makefile) — Provides the shared local and CI setup, build, and check commands.
- [requirements.txt](requirements.txt) — Declares the pinned documentation packages.
- [requirements.lock](requirements.lock) — Locks direct and transitive documentation dependencies for reproducible builds.

---

**SPDX-License-Identifier:** MIT
