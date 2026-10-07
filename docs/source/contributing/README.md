# Contributor documentation

Follow [development setup](DEVELOPMENT.md) to prepare and check a change, then
use the [contribution guide](CONTRIBUTING.md) to submit it. Automation agents
follow the [agent guide](AGENTS.md).

```{toctree}
:hidden:

CONTRIBUTING
DEVELOPMENT
AGENTS
```

## Function reference

Generated from the documentation comments in the layer's shell scripts, BitBake
recipes, and Python documentation tools.

```{toctree}
:glob:
:titlesonly:

.generated/*
```

## Files

- [README.md](README.md) — Introduces the contributor guides and lists the function reference.
- [CONTRIBUTING.md](CONTRIBUTING.md) — Defines the contribution workflow, layer scope rules, and commit requirements.
- [DEVELOPMENT.md](DEVELOPMENT.md) — Installs the documentation tools, builds and checks the site, and explains function comments.
- [AGENTS.md](AGENTS.md) — Guides automation agents through CI-style builds, checks, and backports.
