# Contributor documentation

Follow [development setup](DEVELOPMENT.md) to prepare and check a change, then
use the [contribution guidelines](CONTRIBUTING.md) to submit it. The
[agent guide](AGENTS.md) describes how to run layer builds and CI checks with
kas-container.

```{toctree}
:hidden:

CONTRIBUTING
DEVELOPMENT
AGENTS
```

## Function reference

Each page lists the functions defined in one source file, generated from their
shdoc comments.

```{toctree}
:glob:
:maxdepth: 1

.generated/*
```

## Files

- [README.md](README.md) — Introduces the contributor guides and the function reference.
- [CONTRIBUTING.md](CONTRIBUTING.md) — Defines contribution scope, board integration, and submission.
- [DEVELOPMENT.md](DEVELOPMENT.md) — Sets up the documentation tools and runs the local checks.
- [AGENTS.md](AGENTS.md) — Guides automation agents through CI-style builds, checks, and commits.
