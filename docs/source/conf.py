# Copyright (c) 2026 DevDocs
# SPDX-License-Identifier: BSD-3-Clause
"""Configure the skeleton's Markdown site for hosted and direct-file browsing."""

# Optional string; default 'Project name not set'.
project = "meta-qcom-3rdparty"
# Optional list; default []. Render Markdown with MyST.
extensions = ["myst_parser", "sphinx.ext.autodoc", "sphinx.ext.napoleon"]
# Optional string; default 'index'. README owns the homepage content.
root_doc = "README"
# Optional integer; default 0. Preserve links to Markdown headings.
myst_heading_anchors = 4
# Optional boolean; default False. Reject unresolved cross-references.
nitpicky = True
# Optional list; default []. Do not parse build templates as documentation.
exclude_patterns = [".templates/**"]
# Optional list; default []. Resolve the additional HTML template locally.
templates_path = [".templates"]
# Optional mapping; default {}. Generate an entry point without a second source index.
html_additional_pages = {"index": "index.html"}
# Optional boolean; default True. Avoid fetch() of local files for search excerpts.
html_show_search_summary = False

# Optional list; default []. Show bundled file notices without remote assets.
html_extra_path = []
# Optional list; default []. Standard-library types are described without intersphinx.
nitpick_ignore = [("py:class", "pathlib.Path"), ("py:class", "Path")]
# Import only the safe documentation helper; never import or execute layer tasks.
from pathlib import Path
import sys

repository = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(repository / ".github"))
from native_reference import generate

generate(repository)
