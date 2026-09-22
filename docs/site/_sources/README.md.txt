# meta-qcom-3rdparty Documentation

Welcome to the documentation for **meta-qcom-3rdparty**, an OpenEmbedded / Yocto layer that extends the Qualcomm Linux ecosystem by supporting community and vendor hardware platforms not officially maintained by Qualcomm.

This documentation is intended for developers, vendors, and contributors working with Qualcomm-based SoCs using the Yocto Project build system.

Use the [contributor guides](contributing/README.md) to build or extend the layer,
and the [user guides](user/README.md) to understand its configuration.

```{toctree}
:hidden:

contributing/README
user/README
```

## Overview

The `meta-qcom-3rdparty` layer provides:

- Common BSP enablement for **third-party and community boards**
- **Upstream-aligned** machine support based on `meta-qcom`
- Clean, maintainable structure to avoid fragmentation across vendors
- Integration hooks for both **Qualcomm Linux 1.x** (downstream) and future **Qualcomm Linux 2.x** (upstream) releases

## Related Layers and References

- [meta-qcom](https://github.com/qualcomm-linux/meta-qcom)
- [meta-qcom-hwe](https://github.com/qualcomm-linux/meta-qcom-hwe)
- [meta-qcom-distro](https://github.com/qualcomm-linux/meta-qcom-distro)
- [OpenEmbedded Layer Index](https://layers.openembedded.org/layerindex/)
- [Yocto Project Documentation](https://docs.yoctoproject.org/)

## Folders

- [.templates/](.templates/index.html): Supplies the generated local-browser entry point.

- [contributing/](contributing/README.md): Contribution guidelines, the usage tutorial, agent instructions, and generated function reference.
- [user/](user/README.md): User-facing configuration documentation.

## Files

- [Makefile](Makefile): Provides the shared local and CI setup, build, and reproducibility commands.

- [README.md](README.md): Introduces the documentation and lists its contents.
- [conf.py](conf.py): Extracts function comments with shdoc and configures Sphinx.
- [requirements.txt](requirements.txt): Pins the Python documentation dependencies.

- [requirements.lock](requirements.lock) — Locks direct and transitive documentation dependencies for reproducible builds.

**SPDX-License-Identifier:** MIT
