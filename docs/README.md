# meta-qcom-3rdparty Documentation

Use the [tutorial](usage.md) to prepare a build, and the
[contribution guidelines](contributing.md) when adding board support.
The generated website includes a reference extracted from the function comments.

```{toctree}
:maxdepth: 1

usage
contributing
configuration
```

```{toctree}
:caption: Function reference
:maxdepth: 2
:glob:

.generated/*
```

## Build the documentation

Use Python 3.12 or newer, `uv`, GNU awk (`gawk`), and `curl`. From the repository root:

```sh
uv venv .venv
uv pip install --python .venv/bin/python -r docs/requirements.txt
curl --fail --location https://raw.githubusercontent.com/reconquest/shdoc/b3436134f08428f8bbe2e54bc4dc20da85cd300b/shdoc --output .venv/bin/shdoc
chmod +x .venv/bin/shdoc
.venv/bin/sphinx-build -W --keep-going -b html docs docs/_build/html
```

Open `docs/_build/html/README.html`. Each build extracts the shell and BitBake
function annotations with shdoc v1.4 and renders them with Sphinx. Generated
reference pages and HTML are build output; edit the source comments to change
the reference.

## Files

- [README.md](README.md): Introduces this directory and lists its contents.
- [conf.py](conf.py): Extracts function comments with shdoc and configures Sphinx.
- [configuration.md](configuration.md): Documents configuration types, defaults, and examples.
- [contributing.md](contributing.md): Explains BSP contribution guidelines and the board example.
- [index.md](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/main/docs/index.md): Contains the original documentation overview and planned guide links.
- [requirements.txt](requirements.txt): Pins documentation-only Python dependencies.
- [usage.md](usage.md): Walks through kas setup, configuration inspection, parsing, and image output.
