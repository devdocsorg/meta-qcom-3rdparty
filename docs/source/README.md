# meta-qcom-3rdparty Documentation

Welcome to the documentation for **meta-qcom-3rdparty**, an OpenEmbedded / Yocto layer that extends the Qualcomm Linux ecosystem by supporting community and vendor hardware platforms not officially maintained by Qualcomm.

This documentation is intended for developers, vendors, and contributors working with Qualcomm-based SoCs using the Yocto Project build system.

---

## Overview

The `meta-qcom-3rdparty` layer provides:

- Common BSP enablement for **third-party and community boards**
- **Upstream-aligned** machine support based on [`meta-qcom`](https://github.com/qualcomm-linux/meta-qcom)
- Clean, maintainable structure to avoid fragmentation across vendors
- Integration hooks for both **Qualcomm Linux 1.x** (downstream) and future **Qualcomm Linux 2.x** (upstream) releases

---

## Documentation Index

- [Contribution Guidelines](contributing/CONTRIBUTING.md) — how to contribute patches, follow Yocto conventions, and structure vendor-specific code.
- [Usage Guide](user/USAGE.md) — how to build an image for a supported board with kas.
- [Configuration Reference](user/CONFIGURATION.md) — the settings in the layer, machine, kas, and kernel files.
- [Supported Machines](https://github.com/devdocsorg/meta-qcom-3rdparty/tree/docs/upgrade-test-1006d/conf/machine) — list of currently supported platforms.
- [Developer Notes](contributing/DEVELOPMENT.md) — development setup, the layer checks CI runs, and the documentation build.
- [Agent Guide](contributing/AGENTS.md) — how automation agents run builds and checks the same way CI does.

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

```{toctree}
:hidden:

user/README
contributing/README
```

## Folders

- [user/](user/README.md) — Holds the build tutorial and the configuration reference.
- [contributing/](contributing/README.md) — Holds the contribution, development, and agent guides and the function reference.
- [.templates/](https://github.com/devdocsorg/meta-qcom-3rdparty/tree/docs/upgrade-test-1006d/docs/source/.templates) — Supplies the generated site's entry-point redirect.

## Files

- [Makefile](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006d/docs/source/Makefile) — Provides the shared local and CI setup, build, and check commands.
- [README.md](README.md) — Introduces the documentation and supplies the site's homepage.
- [conf.py](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006d/docs/source/conf.py) — Configures Markdown rendering, the function reference, local navigation, and search.
- [requirements.txt](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006d/docs/source/requirements.txt) — Pins the documentation packages.
- [requirements.lock](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/upgrade-test-1006d/docs/source/requirements.lock) — Locks direct and transitive documentation dependencies for reproducible builds.

---

**SPDX-License-Identifier:** MIT
