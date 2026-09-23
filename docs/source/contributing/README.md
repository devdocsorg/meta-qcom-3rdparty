# Contributing

Start with [development setup](DEVELOPMENT.md), follow the
[contribution guidelines](CONTRIBUTING.md), and retain the
[agent instructions](AGENTS.md) when using automation.

```{toctree}
:hidden:

DEVELOPMENT
CONTRIBUTING
AGENTS
```

## Function reference

The shell pages extract local functions, including internal CI helpers, with shdoc.
Python documentation tooling uses Sphinx autodoc. Each page links to its source.

```{toctree}
:maxdepth: 1
:glob:

.generated/*
```

## Files

- [AGENTS.md](AGENTS.md) — Preserves the CI build, check-order, and signed-off commit rules for automation.
- [CONTRIBUTING.md](CONTRIBUTING.md) — Defines upstream contribution routing and board integration standards.
- [DEVELOPMENT.md](DEVELOPMENT.md) — Walks through checkout, tool installation, builds, and required checks.
- [README.md](README.md) — Describes this folder and indexes its immediate contents.
