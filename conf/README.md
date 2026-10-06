# Layer configuration

BitBake reads [layer.conf](layer.conf) when the layer is added to a build, and
finds each machine in [machine/](machine/README.md) by its `MACHINE` name. The
[configuration reference](../docs/source/user/CONFIGURATION.md) explains each
setting.

## Folders

- [machine/](machine/README.md) — Contains one configuration file per supported board.

## Files

- [README.md](README.md) — Describes the layer configuration.
- [layer.conf](layer.conf) — Registers the layer's recipes, priority, dependencies, and compatible release.
