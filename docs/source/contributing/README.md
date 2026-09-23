# Contributor documentation

Use the [contribution guide](CONTRIBUTING.md) to prepare and submit a change,
the [agent guide](AGENTS.md) to build and check the layer, and
[development setup](DEVELOPMENT.md) to build and check this documentation.

```{toctree}
:hidden:

CONTRIBUTING
DEVELOPMENT
AGENTS
```

## Function reference

Generated from the documentation comments in the layer's scripts, recipes, and
documentation tools.

```{toctree}
:glob:
:maxdepth: 1

.generated/*
```

## Files

- [README.md](README.md) — Introduces the contributor guides and lists the function reference.
- [CONTRIBUTING.md](CONTRIBUTING.md) — Defines contribution scope, target branches, review, and submission.
- [DEVELOPMENT.md](DEVELOPMENT.md) — Sets up the documentation tools and runs the local checks.
- [AGENTS.md](AGENTS.md) — Describes kas-container builds and the checks CI runs, for people and automation agents.
