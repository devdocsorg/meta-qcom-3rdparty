# Contributor documentation

Follow the [contribution guidelines](CONTRIBUTING.md) when adding board support,
or start with the [usage tutorial](USAGE.md) to prepare a layer build.
[Development setup](DEVELOPMENT.md) covers the contributor environment, and the
[agent instructions](AGENTS.md) describe the automated build and validation workflow.
Skill documentation lives alongside these guides.

```{toctree}
:hidden:

CONTRIBUTING
DEVELOPMENT
USAGE
AGENTS
```

## Function reference

```{toctree}
:maxdepth: 2
:glob:

.generated/*
```

## Files

- [DEVELOPMENT.md](DEVELOPMENT.md): Walks through contributor setup, documentation extraction, offline validation, and layer-check entry points.

- [README.md](README.md): Introduces the contributor guides and generated function reference.
- [CONTRIBUTING.md](CONTRIBUTING.md): Explains BSP contribution guidelines and the board example.
- [USAGE.md](USAGE.md): Walks through kas setup, configuration inspection, parsing, and image output.
- [AGENTS.md](AGENTS.md): Defines the agent build, validation, and contribution workflow.
