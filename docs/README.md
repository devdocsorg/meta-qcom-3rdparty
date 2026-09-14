# Documentation

Edit the guides in [source/](source/README.md) and rebuild the Sphinx website in
[site/](site/). Commit the updated source and generated site together.

## Build the documentation

Use Python 3.12 or newer, `uv`, GNU awk (`gawk`), and `curl`. From the repository root:

```sh
uv venv .venv
uv pip install --python .venv/bin/python -r docs/source/requirements.txt
curl --fail --location https://raw.githubusercontent.com/reconquest/shdoc/b3436134f08428f8bbe2e54bc4dc20da85cd300b/shdoc --output .venv/bin/shdoc
chmod +x .venv/bin/shdoc
rm -rf docs/site
.venv/bin/sphinx-build -W --keep-going -E -b html -d docs/.doctrees docs/source docs/site
```

Open `docs/site/README.html`. The function reference is extracted from source
comments with shdoc v1.4 during the build. Edit the comments to change the reference.
The site contains generated HTML and assets; build caches and intermediate
Markdown stay outside it.

## Folders

- [source/](source/README.md): Contributor and user documentation, dependencies, and Sphinx configuration.
- [site/](site/): The generated Sphinx website stored with its source.

## Files

- [README.md](README.md): Explains the documentation layout and build command.
