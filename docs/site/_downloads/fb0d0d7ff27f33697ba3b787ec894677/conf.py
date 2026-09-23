# Copyright (c) 2026 DevDocs
# SPDX-License-Identifier: BSD-3-Clause
"""Configure the layer's Markdown site and generate its shell function reference.

Loading this file runs the pinned shdoc over every shell script, BitBake shell
task, and GitHub Actions ``run`` step, writing one Markdown page per source file
to ``contributing/.generated/``. BitBake files are split into statements with
BitBake's own parser; no metadata is evaluated and no task is executed.
"""
from pathlib import Path
import re
import shutil
import subprocess
import sys

import yaml

# Optional string; default 'Project name not set'.
project = "meta-qcom-3rdparty"
# Optional list; default []. Render Markdown with MyST.
extensions = ["myst_parser"]
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
# Optional boolean; default True. Keep intermediate reference Markdown out of the site.
html_copy_source = False

# setup installs BitBake's parser and shdoc inside the documentation environment.
sys.path.insert(0, str(Path(sys.prefix, "src/bitbake/lib")))
from bb.parse import ast as bitbake_ast  # noqa: E402
from bb.parse.parse_py import BBHandler  # noqa: E402

root = Path(__file__).resolve().parents[2]
generated = Path(__file__).resolve().parent / "contributing/.generated"
shutil.rmtree(generated, ignore_errors=True)
generated.mkdir(parents=True)
tracked = subprocess.check_output(["git", "ls-files"], cwd=root, text=True).splitlines()
for path in tracked:
    source = root / path
    chunks = []
    if path.endswith(".sh"):
        chunks.append(source.read_text())
    elif path.endswith((".bb", ".bbappend", ".bbclass", ".inc", ".conf")):
        lines = source.read_text().splitlines()
        for node in BBHandler.get_statements(path, str(source), path):
            if isinstance(node, bitbake_ast.MethodNode) and not node.python:
                # The node records its closing line; its body ends with an empty entry.
                header = node.lineno - len(node.body) - 1
                start = header
                while start > 0 and lines[start - 1].lstrip().startswith("#"):
                    start -= 1
                chunks.append("\n".join(lines[start:header] + [f"{node.func_name}() {{", *node.body[:-1], "}"]))
    elif path.startswith(".github/") and path.endswith((".yml", ".yaml")):
        pending = [yaml.safe_load(source.read_text())]
        while pending:
            item = pending.pop()
            if isinstance(item, dict):
                if isinstance(item.get("run"), str):
                    chunks.append(item["run"])
                pending.extend(item.values())
            elif isinstance(item, list):
                pending.extend(item)
    if not chunks:
        continue
    # A command line between chunks stops a comment from attaching to the next chunk.
    reference = subprocess.run([Path(sys.prefix, "bin/shdoc")], input="\n:\n".join(chunks),
                               capture_output=True, text=True, check=True).stdout
    if reference.strip():
        # The page heading and navigation already list the functions; drop shdoc's index.
        reference = re.sub(r"## Index\n\n(\* .*\n)+", "## Functions\n", reference, count=1)
        link = f"https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/main/{path}"
        page = generated / (path.replace("/", "-") + ".md")
        page.write_text(f"# {path}\n\nSource: [{path}]({link})\n\n{reference.strip()}\n")
