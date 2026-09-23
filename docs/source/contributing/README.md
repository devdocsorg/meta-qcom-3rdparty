# Contributor guides

Contribution policy, development setup, and native function references.

## Files

- [AGENTS.md](AGENTS.md) — Preserves the CI-aligned automation procedure.
- [CONTRIBUTING.md](CONTRIBUTING.md) — Owns the BSP contribution policy and upstream routing.
- [DEVELOPMENT.md](DEVELOPMENT.md) — Sets up the checkout and runs documentation and layer checks.
- [NOTICES.md](NOTICES.md) — Retains full notices for reused documentation material.
- [README.md](README.md) — Orients readers and indexes this folder.

## Function reference

The reference includes private CI helpers, the firmware deploy task, and the
documentation extension; it is generated from native source comments.

```{toctree}
:maxdepth: 1
:glob:

.generated/*
```

```{toctree}
:hidden:

CONTRIBUTING
DEVELOPMENT
AGENTS
NOTICES
```
