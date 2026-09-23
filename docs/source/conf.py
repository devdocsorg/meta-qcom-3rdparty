# Copyright (c) 2026 DevDocs
# SPDX-License-Identifier: BSD-3-Clause
"""Configure the layer's Markdown site and its generated function reference.

Loading this file regenerates contributing/.generated: shdoc renders every
shell script, BitBake shell function, and workflow run step that defines
functions, and autodoc renders each Python module with definitions.
"""
import shutil
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(root / ".github"))
import test_reference_coverage as reference  # noqa: E402

# Required string. Repository page that source links open: the review branch
# while this documentation is proposed, main once it is adopted.
source_url = "https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/offline-layer-documentation"
generated = Path(__file__).parent / "contributing/.generated"
shutil.rmtree(generated, ignore_errors=True)
generated.mkdir()
for path in reference.tracked_files(root):
    page = generated / (path.replace("/", "-") + ".md")
    heading = f"# {Path(path).name}\n\nSource: [{path}]({source_url}/{path}).\n\n"
    if path.endswith(".py"):
        module, definitions = reference.python_definitions(path, root)
        if definitions:
            sys.path.insert(0, str((root / path).parent))
            page.write_text(heading + "```{eval-rst}\n.. automodule:: " + module
                            + "\n   :members:\n   :private-members:\n```\n")
        continue
    units = reference.shell_units(path, root)
    bitbake = Path(path).suffix in reference.BITBAKE_SUFFIXES
    if any(reference.shell_functions(unit, bitbake) for unit in units):
        shdoc = subprocess.run([root / ".venv/bin/shdoc"], input="\n".join(units),
                               capture_output=True, text=True, check=True)
        page.write_text(heading + shdoc.stdout)

# Optional string; default 'Project name not set'.
project = "meta-qcom-3rdparty"
# Optional list; default []. Render Markdown with MyST and Python docstrings with autodoc.
extensions = ["myst_parser", "sphinx.ext.autodoc"]
# Optional string; default 'index'. README owns the homepage content.
root_doc = "README"
# Optional integer; default 0. Preserve links to Markdown headings.
myst_heading_anchors = 4
# Optional boolean; default False. Reject unresolved cross-references.
nitpicky = True
# Optional list; default []. Standard-library types in signatures have no local target.
nitpick_ignore = [("py:class", "pathlib.Path"), ("py:exc", "subprocess.CalledProcessError")]
# Optional list; default []. Do not parse build templates as documentation.
exclude_patterns = [".templates/**"]
# Optional list; default []. Resolve the additional HTML template locally.
templates_path = [".templates"]
# Optional mapping; default {}. Generate an entry point without a second source index.
html_additional_pages = {"index": "index.html"}
# Optional boolean; default True. Avoid fetch() of local files for search excerpts.
html_show_search_summary = False
# Optional boolean; default False. Show defaults as written, not as local absolute paths.
autodoc_preserve_defaults = True
# Optional boolean; default True. Page sources stay in the repository, not the site.
html_copy_source = False
# Optional boolean; default True. No copyright holder is configured, so omit the empty notice.
html_show_copyright = False
