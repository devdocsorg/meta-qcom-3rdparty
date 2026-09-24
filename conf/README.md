# Layer configuration

BitBake reads [layer.conf](layer.conf) to register the layer and the files in
[machine/](machine/README.md) to configure each board. The
[configuration reference](../docs/source/user/CONFIGURATION.md) explains every setting.

## Folders

- [machine/](machine/README.md) — Contains one configuration file per supported board.

## Files

- [README.md](README.md) — Describes the layer configuration.
- [layer.conf](layer.conf) — Registers the layer, its recipes, dependencies, and compatible release.
