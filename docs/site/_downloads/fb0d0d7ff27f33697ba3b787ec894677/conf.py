# Copyright (c) 2026 DevDocs
# SPDX-License-Identifier: MIT
"""Build the guides and extract function documentation without running recipes."""

from pathlib import Path
import ast
import re
import subprocess
import sys

# Optional string; default 'Project name not set'.
project = "meta-qcom-3rdparty"
# Optional list; default []. Parse the existing Markdown guides.
extensions = ["myst_parser"]
# Optional string; default 'index'. Use the folder guide as the site homepage.
root_doc = "README"
# Optional integer; default 0. Support heading links in generated Markdown.
myst_heading_anchors = 4
# Optional boolean; default False. Check unresolved cross-references.
nitpicky = True

# Optional list; default []. Exclude the entry-point template from source discovery.
exclude_patterns = [".templates/**"]
# Optional list; default []. Resolve bundled HTML templates locally.
templates_path = [".templates"]
# Optional mapping; default {}. Keep README as the sole homepage source.
html_additional_pages = {"index": "index.html"}
# Optional boolean; default True. Avoid fetch() of local files for search excerpts.
html_show_search_summary = False

# Build paths are derived from this file; no host-specific configuration.
source_dir = Path(__file__).resolve().parent
root = source_dir.parents[1]
# Derive the README map from the shared-map snapshot already used by this site.
# Only the marked block is replaced; all other README content stays authored there.
readme_path = root / "README.md"
readme_text = readme_path.read_text()
map_start = "<!-- repository-map:start -->"
map_end = "<!-- repository-map:end -->"
if readme_text.count(map_start) != 1 or readme_text.count(map_end) != 1:
    raise RuntimeError("README must contain exactly one repository-map marker pair")
readme_before, readme_map = readme_text.split(map_start)
map_previous, readme_after = readme_map.split(map_end)
map_snapshot = (source_dir / "user" / "REPOSITORY_MAP.md").read_text()
map_section = "## Repository map\n" + re.sub(r"(?m)^(#{1,5}) ", r"#\1 ", map_snapshot.split("\n", 1)[1])
readme_path.write_text(readme_before + map_start + "\n\n" + map_section.rstrip()
                       + "\n\n" + map_end + readme_after)

generated = source_dir / "contributing" / ".generated"
shdoc = Path(sys.executable).with_name("shdoc")
generated.mkdir(exist_ok=True)
# Replace generated pages on every build, including after source-file removal.
for stale in generated.glob("*.md"):
    stale.unlink()
# Reject Python functions until their native extraction/coverage path is configured.
for python_source in sorted([*root.glob("ci/*.py"), *source_dir.glob("*.py"),
                             *(root / ".github").rglob("*.py")]):
    python_tree = ast.parse(python_source.read_text())
    if any(isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda))
           for node in ast.walk(python_tree)):
        raise RuntimeError(f"Configure Python API extraction for {python_source.relative_to(root)}")

reference_count = 0
for source in sorted([*root.glob("ci/*.sh"), *root.glob("recipes-*/**/*.bb*")]):
    source_text = source.read_text()
    if re.search(r"(?m)^\s*(?:fakeroot\s+)?python\s*(?:[\w:.-]+\s*)?\(\s*\)\s*\{|^\s*(?:async\s+)?def\s+", source_text):
        raise RuntimeError(f"Configure BitBake Python extraction for {source.relative_to(root)}")
    declared = set(re.findall(r"(?m)^\s*(?:function\s+)?([\w:.-]+)\s*\(\s*\)\s*\{", source_text))
    declared.update(re.findall(r"(?m)^\s*function\s+([\w:.-]+)\s*\{", source_text))
    with source.open() as script:
        result = subprocess.run([str(shdoc)], stdin=script, text=True,
                                capture_output=True, check=True)
    documented = set(re.findall(r"(?m)^### ([\w:.-]+)\s*$", result.stdout))
    if declared != documented:
        raise RuntimeError(f"Reference coverage mismatch in {source.relative_to(root)}: "
                           f"missing={sorted(declared - documented)}, extra={sorted(documented - declared)}")
    reference_count += len(declared)
    if result.stdout.strip():
        name = str(source.relative_to(root)).replace("/", "-")
        (generated / (name + ".md")).write_text(result.stdout)

print(f"Verified language-specific reference coverage: {reference_count} shell functions/tasks")

# Optional mapping; theme defaults to 940px. Give diagrams and evidence tables room.
html_theme_options = {"page_width": "1280px", "sidebar_width": "220px"}
