# Contributor documentation

The contributor guide owns contribution rules and the worked board-integration
example. The agent guide owns CI-style build and check procedures. The development
walkthrough installs tools and links those procedures.

[Native function reference](.generated/index.rst) is generated from source comments,
including private shell helpers, the BitBake deploy task, and documentation tooling.
It is rebuilt automatically; do not maintain a second authored API manual.

```{toctree}
:hidden:

CONTRIBUTING
AGENTS
DEVELOPMENT
.generated/index
```

## Files

- [AGENTS.md](AGENTS.md) — Owns container checks, build commands, contribution routing, and commit rules for agents.
- [CONTRIBUTING.md](CONTRIBUTING.md) — Owns contribution standards and the worked RUBIK Pi board-integration example.
- [DEVELOPMENT.md](DEVELOPMENT.md) — Walks through checkout, tools, checks, and documentation maintenance.
- [README.md](README.md) — Introduces this folder and indexes its maintained contents.
