# meta-qcom-3rdparty documentation

This OpenEmbedded / Yocto BSP layer extends the Qualcomm Linux ecosystem to
community and vendor boards not officially maintained by Qualcomm. These guides
serve developers, vendors, and contributors working with Qualcomm-based SoCs.
The layer provides common BSP enablement, upstream-aligned support through
`meta-qcom`, a shared structure for vendor contributions, and integration hooks
for Qualcomm Linux 1.x downstream and 2.x upstream releases.

Start with the [firmware deployment tutorial](user/USAGE.md), the
[supported machines](user/SUPPORTED_MACHINES.md), or the
[contributor environment walkthrough](contributing/DEVELOPMENT.md).
The configuration reference covers layer inclusion and validation; contributor
and agent guides own CI integration and maintainer procedures.

## Related layers and references

- [meta-qcom](https://github.com/qualcomm-linux/meta-qcom) supplies the upstream SoC baseline.
- [meta-qcom-hwe](https://github.com/qualcomm-linux/meta-qcom-hwe) supplies downstream enablement.
- [meta-qcom-distro](https://github.com/qualcomm-linux/meta-qcom-distro) supplies optional distribution settings.
- [OpenEmbedded Layer Index](https://layers.openembedded.org/layerindex/) catalogues layers.
- [Yocto documentation](https://docs.yoctoproject.org/) explains the build system.

**SPDX-License-Identifier:** MIT

```{toctree}
:hidden:

user/README
contributing/README
```

## Folders

- [.templates](.templates/index.html) — Contains the generated-site entry template.
- [contributing](contributing/README.md) — Owns contributor setup, policies, agent procedures, and native references.
- [user](user/README.md) — Explains the actual firmware output, supported machines, and configuration.

## Files

- [Makefile](Makefile) — Provides shared documentation setup, generation, and validation commands.
- [README.md](README.md) — Introduces this folder and indexes its maintained contents.
- [conf.py](conf.py) — Configures strict Sphinx, MyST, native autodoc, and offline search.
- [requirements.lock](requirements.lock) — Pins the full Python documentation dependency graph.
- [requirements.txt](requirements.txt) — Declares pinned direct documentation dependencies.
