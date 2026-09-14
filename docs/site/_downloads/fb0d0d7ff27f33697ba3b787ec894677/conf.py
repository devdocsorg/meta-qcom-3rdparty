# SPDX-License-Identifier: MIT
"""Build the guides and extract function documentation without running recipes."""

from pathlib import Path
import subprocess
import sys

# Optional string; default 'Project name not set'.
project = "meta-qcom-3rdparty"
# Optional list; default []. Parse the existing Markdown guides.
extensions = ["myst_parser"]
# Optional string; default 'index'. Use the folder guide as the site homepage.
root_doc = "README"
# Optional pattern list; default []. The existing overview contains planned
# guides and remains available on GitHub.
exclude_patterns = ["user/index.md"]
# Optional integer; default 0. Support heading links in generated Markdown.
myst_heading_anchors = 4
# Optional boolean; default False. Check unresolved cross-references.
nitpicky = True

# Build paths are derived from this file; no host-specific configuration.
source_dir = Path(__file__).resolve().parent
root = source_dir.parents[1]
generated = source_dir / "contributing" / ".generated"
shdoc = Path(sys.executable).with_name("shdoc")
generated.mkdir(exist_ok=True)
# Replace generated pages on every build, including after source-file removal.
for stale in generated.glob("*.md"):
    stale.unlink()
for source in sorted([*root.glob("ci/*.sh"), *root.glob("recipes-*/**/*.bb*")]):
    with source.open() as script:
        result = subprocess.run([str(shdoc)], stdin=script, text=True,
                                capture_output=True, check=True)
    if result.stdout.strip():
        name = str(source.relative_to(root)).replace("/", "-")
        (generated / (name + ".md")).write_text(result.stdout)
