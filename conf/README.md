# Layer configuration

BitBake reads `layer.conf` to add the layer, and a machine file when `MACHINE`
names it. The [configuration reference](../docs/source/user/CONFIGURATION.md)
explains each setting.

## Folders

- [machine/](machine/README.md) — Holds the machine definitions for the supported boards.

## Files

- [README.md](README.md) — Introduces the layer configuration.
- [layer.conf](layer.conf) — Registers the layer, its recipe paths, dependencies, and compatible release series.
