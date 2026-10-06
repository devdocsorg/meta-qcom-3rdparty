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
- [Usage Guide](user/USAGE.md) — how to build an image with the layer and find its output.
- [Supported Machines](https://github.com/devdocsorg/meta-qcom-3rdparty/tree/docs/build-prerequisites-test/conf/machine) — list of currently supported platforms and vendors.
- [Developer Notes](contributing/DEVELOPMENT.md) — development setup, the CI-equivalent layer checks, and the documentation build.
- [Configuration Reference](user/CONFIGURATION.md) — every setting in the layer, machine, recipe, kas, and workflow files.

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

- [user/](user/README.md) — Contains the image build tutorial and the configuration reference.
- [contributing/](contributing/README.md) — Contains the contribution, agent, and development guides and the function reference.
- [.templates/](https://github.com/devdocsorg/meta-qcom-3rdparty/tree/docs/build-prerequisites-test/docs/source/.templates) — Supplies the generated site's entry-point redirect.

## Files

- [README.md](README.md) — Introduces the layer documentation and supplies the site's homepage.
- [Makefile](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/build-prerequisites-test/docs/source/Makefile) — Provides the shared local and CI setup, build, and check commands.
- [conf.py](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/build-prerequisites-test/docs/source/conf.py) — Configures Markdown rendering, the function reference, local navigation, and search.
- [requirements.txt](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/build-prerequisites-test/docs/source/requirements.txt) — Pins the documentation packages.
- [requirements.lock](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/build-prerequisites-test/docs/source/requirements.lock) — Locks direct and transitive documentation dependencies for reproducible builds.

---

**SPDX-License-Identifier:** MIT
