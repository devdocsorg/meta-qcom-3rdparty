# Copyright (c) 2026 DevDocs
# SPDX-License-Identifier: BSD-3-Clause
"""Find every function definition and check its native reference.

Usage: test_reference_coverage.py generate | check

docs/source/conf.py runs "generate" before Sphinx reads its sources: it fails
on undocumented functions and on source formats without a configured
extractor, then writes one shdoc page per source file with functions to
docs/source/contributing/.generated/. The Makefile runs "check" after the HTML
build: it fails when a function has no rendered reference entry.

Functions are found in tracked and staged files, independently of shdoc.
BitBake's statement parser reads recipes and configuration without evaluating
them; bashlex parses shell scripts, workflow run steps, and Makefile recipes;
Python's ast module reads Python files. Nothing is executed.
"""
import ast
import html
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import bashlex
import yaml
from docutils.nodes import make_id

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / ".venv/bitbake/lib"))
from bb.parse.parse_py import BBHandler  # noqa: E402  (pinned by the Makefile's setup)

mode = sys.argv[1] if len(sys.argv) == 2 else ""
if mode not in ("generate", "check"):
    raise SystemExit(__doc__)
pages = root / "docs/source/contributing/.generated"
site = root / "docs/site/contributing/.generated"
source_url = "https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/layer-documentation/"
bitbake_suffixes = (".bb", ".bbappend", ".bbclass", ".inc", ".conf")
# Formats verified to hold no function definitions.
plain_suffixes = (".md", ".txt", ".lock", ".cfg")
plain_names = ("LICENSE", "NOTICE", "CODEOWNERS", ".gitignore", ".env.example")

functions, problems, shell_texts = [], [], []
# Tracked and staged files only: kas checkouts and build output can share this directory.
listed = subprocess.run(["git", "ls-files", "-z"], cwd=root, capture_output=True, text=True, check=True).stdout
for path in sorted(set(filter(None, listed.split("\0")))):
    full = root / path
    if path.startswith("docs/site/") or not full.is_file():
        continue  # Generated output derives from these sources; deleted files have no content.
    text = full.read_text(errors="replace")
    first_line = text.split("\n", 1)[0]
    if full.suffix == ".sh" or re.match(r"#!.*\b(ba)?sh\b", first_line):
        shell_texts.append((path, "", text, True))
    elif full.suffix in bitbake_suffixes:
        try:
            statements = BBHandler.get_statements(path, str(full), str(root))
        except Exception as error:
            problems.append(f"{path}: BitBake cannot parse this file ({error}); its definitions are unsupported")
            continue
        lines = text.splitlines()
        for node in statements:
            kind = type(node).__name__
            if kind == "PythonMethodNode" or (kind == "MethodNode" and node.python):
                name = getattr(node, "func_name", None) or getattr(node, "function", "")
                problems.append(f"{path}:{node.lineno}: Python function {name} is unsupported; "
                                "configure a Python extractor before adding BitBake Python functions")
            elif kind == "MethodNode":
                start = node.lineno - len(node.body) - 1
                if not (0 <= start < len(lines) and node.func_name in lines[start] and lines[start].rstrip().endswith("{")):
                    problems.append(f"{path}:{node.lineno}: cannot locate the definition of {node.func_name}")
                    continue
                comments = []
                while start - len(comments) > 0 and lines[start - len(comments) - 1].lstrip().startswith("#"):
                    comments.insert(0, lines[start - len(comments) - 1].strip())
                functions.append({"path": path, "name": node.func_name, "line": start + 1,
                                  "comments": comments, "whole_file": False})
    elif path.startswith(".github/workflows/") and full.suffix in (".yml", ".yaml"):
        workflow = yaml.safe_load(text) or {}
        default_shell = ((workflow.get("defaults") or {}).get("run") or {}).get("shell", "bash")
        for job_id, job in (workflow.get("jobs") or {}).items():
            job_shell = ((job.get("defaults") or {}).get("run") or {}).get("shell", default_shell)
            for number, step in enumerate(job.get("steps") or [], 1):
                if "run" not in step:
                    continue
                where = f" (job {job_id}, step {number})"
                if not re.match(r"(ba)?sh\b", str(step.get("shell", job_shell))):
                    problems.append(f"{path}{where}: shell {step['shell']!r} is unsupported; configure its extractor")
                    continue
                # GitHub substitutes expressions before the shell runs.
                shell_texts.append((path, where, re.sub(r"\$\{\{.*?\}\}", "GITHUB_EXPRESSION", str(step["run"])), False))
    elif full.suffix in (".yml", ".yaml"):
        # kas local_conf_header values are BitBake configuration; other YAML is data.
        headers = (yaml.safe_load(text) or {}).get("local_conf_header") or {}
        with tempfile.TemporaryDirectory() as temporary:
            for key, value in headers.items():
                fragment = Path(temporary) / f"{key}.conf"
                fragment.write_text(str(value))
                try:
                    statements = BBHandler.get_statements(f"{path}:{key}", str(fragment), temporary)
                except Exception as error:
                    problems.append(f"{path}: local_conf_header {key} cannot be parsed ({error}); unsupported")
                    continue
                for node in statements:
                    if type(node).__name__ in ("MethodNode", "PythonMethodNode"):
                        problems.append(f"{path}: local_conf_header {key} defines a function; "
                                        "BitBake configuration cannot hold functions and none is supported here")
    elif full.name == "Makefile":
        # Each recipe line runs in the shell after make turns $$ into $.
        recipes = [line[1:].lstrip("@-+").replace("$$", "$") for line in text.splitlines() if line.startswith("\t")]
        shell_texts.append((path, " (recipes)", "\n".join(recipes), False))
    elif full.suffix == ".py":
        tree = ast.parse(text, path)
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
                problems.append(f"{path}:{node.lineno}: Python functions are unsupported; "
                                "configure Python autodoc and its coverage before adding them")
    elif full.suffix == ".html" and "<script" not in text.lower():
        pass  # Templates without scripts define no functions.
    elif full.suffix not in plain_suffixes and full.name not in plain_names:
        problems.append(f"{path}: no function extractor is configured for this format; "
                        "add its extractor and coverage to .github/test_reference_coverage.py")

for path, where, text, whole_file in shell_texts:
    try:
        trees = bashlex.parse(text) if text.strip() else []
    except Exception as error:
        problems.append(f"{path}{where}: the shell parser cannot read it ({error}); functions cannot be checked")
        continue
    found = []
    stack = list(trees)
    while stack:
        node = stack.pop()
        if node.kind == "function":
            found.append((node.pos[0], node.name.word))
        for value in vars(node).values():
            children = value if isinstance(value, list) else [value]
            stack.extend(child for child in children if isinstance(child, bashlex.ast.node))
    lines = text.splitlines()
    for position, name in sorted(found):
        start = text.count("\n", 0, position)
        comments = []
        while start - len(comments) > 0 and lines[start - len(comments) - 1].lstrip().startswith("#"):
            comments.insert(0, lines[start - len(comments) - 1].strip())
        functions.append({"path": path, "where": where, "name": name, "line": start + 1,
                          "comments": comments, "whole_file": whole_file})

for function in functions:
    block = "\n".join(function["comments"])
    missing = [tag for tag in ("@description", "@example", "@exitcode") if tag not in block]
    if "@arg" not in block and "@noargs" not in block:
        missing.append("@arg or @noargs")
    location = f"{function['path']}:{function['line']}{function.get('where', '')}"
    if missing:
        problems.append(f"{location}: {function['name']} is undocumented; missing {', '.join(missing)}")
    if "@internal" in block:
        problems.append(f"{location}: {function['name']} is marked @internal, which omits it from the reference")
    if not re.fullmatch(r"[\w.:-]+", function["name"]):
        problems.append(f"{location}: shdoc cannot render the name {function['name']}; "
                        "this definition form is unsupported by the configured extractor")

if not problems and mode == "generate":
    pages.mkdir(parents=True, exist_ok=True)
    for path in sorted({function["path"] for function in functions}):
        defined = [function for function in functions if function["path"] == path]
        if defined[0]["whole_file"]:
            source = (root / path).read_text()
        else:
            # Embedded definitions: pass each documentation comment and name to shdoc.
            source = "".join("\n".join(function["comments"]) + f"\n{function['name']}() {{\n    :\n}}\n\n"
                             for function in defined)
        rendered = subprocess.run([str(root / ".venv/bin/shdoc")], input=source, capture_output=True,
                                  text=True, check=True).stdout
        (pages / (path.replace("/", "-") + ".md")).write_text(
            f"# {path}\n\nFunctions defined in [{path}]({source_url}{path}).\n\n{rendered.strip()}\n")
elif not problems:
    for function in functions:
        page = site / (function["path"].replace("/", "-") + ".html")
        content = page.read_text() if page.is_file() else ""
        anchor = content.find(f'<section id="{make_id(function["name"])}">')
        following = content.find("<h3", content.find("<h3", anchor) + 1)
        entry = content[anchor:following if following > 0 else None]
        heading = f">{html.escape(function['name'])}<a class=\"headerlink\""
        fields = ("Example", "Exit codes")
        if anchor < 0 or heading not in entry or not all(f">{field}<" in entry for field in fields):
            problems.append(f"{function['path']}:{function['line']}: {function['name']} has no complete rendered "
                            f"entry in {page.relative_to(root)} (missing reference coverage)")

for problem in problems:
    print(f"reference coverage: {problem}", file=sys.stderr)
if problems:
    raise SystemExit(f"Reference coverage failed with {len(problems)} problem(s).")
print(f"Reference coverage: {len(functions)} function(s) documented"
      + (" and rendered." if mode == "check" else "; pages generated."))
