# Layer configuration

[layer.conf](layer.conf) registers the layer with BitBake, and
[machine/](machine/README.md) holds the board definitions. The
[configuration reference](../docs/source/user/CONFIGURATION.md) explains each
setting.

## Folders

- [machine/](machine/README.md) — Contains one configuration per supported board.

## Files

- [README.md](README.md) — Describes the layer configuration.
- [layer.conf](layer.conf) — Registers the layer's recipes, collection, priority, dependencies, and supported release.
