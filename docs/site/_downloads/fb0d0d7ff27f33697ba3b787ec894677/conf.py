# SPDX-License-Identifier: MIT
"""Configure strict Markdown and native Python reference generation for file browsing."""
from pathlib import Path
import sys

# Required module search path for the audited, side-effect-free native reference module.
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / '.github'))
# Optional string; Sphinx default is 'Project name not set'.
project = 'meta-qcom-3rdparty'
# Optional list; default []. MyST reads Markdown; autodoc reads Python docstrings.
extensions = ['myst_parser', 'sphinx.ext.autodoc']
# Optional string; default 'index'. The documentation README owns site orientation.
root_doc = 'README'
# Optional integer; default 0. Preserve links to Markdown headings at all used depths.
myst_heading_anchors = 6
# Optional boolean; default False. Missing references fail the strict build.
nitpicky = True
# Optional list; default []. Build templates and Python caches are not source pages.
exclude_patterns = ['.templates/**', '**/__pycache__/**']
# Optional list; default []. Find the local direct-file entry template.
templates_path = ['.templates']
# Optional mapping; default {}. Generate index.html with a relative redirect/fallback.
html_additional_pages = {'index': 'index.html'}
# Optional boolean; default True. Search titles without fetching local-file excerpts.
html_show_search_summary = False
# Optional string; default 'signature'. Retain annotated parameter and return types.
autodoc_typehints = 'signature'
# Optional list; default []. Path is displayed locally without a remote inventory.
nitpick_ignore = [('py:class', 'pathlib.Path'), ('py:exc', 'subprocess.CalledProcessError')]
