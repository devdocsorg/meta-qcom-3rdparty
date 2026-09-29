# Contributor documentation

Follow [development setup](DEVELOPMENT.md) to prepare and validate a change, then
use the [contribution guidelines](CONTRIBUTING.md) to submit it. Automation
agents follow the [agent guide](AGENTS.md).

```{toctree}
:hidden:

CONTRIBUTING
DEVELOPMENT
AGENTS
```

## Function reference

Generated from the documentation comments in the repository's shell scripts,
BitBake recipes, and Python tools.

```{toctree}
:glob:
:titlesonly:

.generated/*
```

## Files

- [README.md](README.md) — Introduces the contributor guides and lists the function reference.
- [CONTRIBUTING.md](CONTRIBUTING.md) — Defines the layer's contribution standards and where to submit changes.
- [DEVELOPMENT.md](DEVELOPMENT.md) — Sets up a checkout, runs the layer checks, and builds the documentation.
- [AGENTS.md](AGENTS.md) — Tells automation agents how to build, check, and commit like CI.
