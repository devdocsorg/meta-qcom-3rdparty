# Copyright (c) 2026 DevDocs
# SPDX-License-Identifier: BSD-3-Clause
"""Configure the layer's Markdown site for hosted and direct-file browsing."""

# Optional string; default 'Project name not set'.
project = "meta-qcom-3rdparty"
# Optional list; default []. Render Markdown with MyST.
extensions = ["myst_parser", "sphinx.ext.autodoc", "sphinx.ext.viewcode"]
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

# Use safe tooling modules; product scripts and BitBake tasks are never imported.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".github"))
from native_reference import generate
# Build-local reference intermediates are regenerated before Sphinx discovers pages.
generate()
# Optional mapping; default {}. Include documented internal Python helpers.
autodoc_default_options = {"members": True, "private-members": True}

# Optional pairs; default []. Standard-library types are displayed without cross-links.
nitpick_ignore = [("py:class", "pathlib.Path"), ("py:exc", "subprocess.CalledProcessError")]
# Optional mapping; default {}. Keep sidebar navigation at page level.
html_theme_options = {"globaltoc_maxdepth": 1}
