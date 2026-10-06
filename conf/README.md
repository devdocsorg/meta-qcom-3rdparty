# Layer configuration

BitBake reads [layer.conf](layer.conf) to register the layer, and finds each board's
definition in [machine/](machine/README.md) by its `MACHINE` name.

## Folders

- [machine/](machine/README.md) — Holds one configuration file per supported board.

## Files

- [README.md](README.md) — Describes the layer configuration folder.
- [layer.conf](layer.conf) — Registers the layer, its recipe paths, dependencies, and compatible Yocto Project release.
