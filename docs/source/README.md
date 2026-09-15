# meta-qcom-3rdparty Documentation

Use the contributor guides to build or extend the layer, and the user guides
to understand its configuration.

```{toctree}
:hidden:

contributing/README
user/README
```

## Folders

- [.templates/](.templates/index.html): Supplies the generated local-browser entry point.

- [contributing/](contributing/README.md): Contribution guidelines, the usage tutorial, agent instructions, and generated function reference.
- [user/](user/README.md): User-facing configuration documentation.

## Files

- [Makefile](Makefile): Provides the shared local and CI setup, build, and reproducibility commands.

- [README.md](README.md): Introduces the documentation and lists its contents.
- [conf.py](conf.py): Extracts function comments with shdoc and configures Sphinx.
- [requirements.txt](requirements.txt): Pins the Python documentation dependencies.

- [requirements.lock](requirements.lock) — Locks direct and transitive documentation dependencies for reproducible builds.
