# Copyright (c) 2026 DevDocs
# SPDX-License-Identifier: MIT
"""Check that every function in the repository has a documented, rendered reference entry.

Run from the repository root after sphinx-build; the html target does this.
Functions are discovered without shdoc: bashlex parses shell scripts, BitBake
shell task bodies, workflow run steps, and Makefile recipes; BitBake's statement
parser splits recipes, classes, includes, and configuration files; Python's ast
module parses Python files and python -c programs. Each function needs a
generated entry with a purpose, arguments, exit codes, and an example, and a
matching section in the generated HTML. Unsupported formats and definitions fail.
"""
import ast
from pathlib import Path
import re
import subprocess
import sys

import bashlex
from docutils.nodes import make_id
import yaml

sys.path.insert(0, str(Path(sys.prefix, "src/bitbake/lib")))
from bb.parse import ast as bitbake_ast  # noqa: E402
from bb.parse.parse_py import BBHandler  # noqa: E402

BITBAKE = (".bb", ".bbappend", ".bbclass", ".inc", ".conf")
# Formats that cannot define functions; anything else must be configured here.
DATA = (".md", ".yml", ".yaml", ".cfg", ".txt", ".lock", ".html")
DATA_NAMES = {"LICENSE", "NOTICE", "CODEOWNERS", ".gitignore", ".env.example"}
generated = Path("docs/source/contributing/.generated")
site = Path("docs/site/contributing/.generated")

errors, functions, shells = [], [], []
make_recipe = object()  # Marks shell lines taken from Makefile recipes.
tracked = subprocess.check_output(["git", "ls-files"], text=True).splitlines()
for path in (p for p in tracked if not p.startswith("docs/site/")):
    text = Path(path).read_text()
    first = text.partition("\n")[0]
    if path.endswith(".sh") or re.match(r"#!.*\b(ba|da)?sh\b", first):
        shells.append((path, text, None))
    elif path.endswith(BITBAKE):
        for node in BBHandler.get_statements(path, str(Path(path).resolve()), path):
            if isinstance(node, bitbake_ast.PythonMethodNode) or (
                    isinstance(node, bitbake_ast.MethodNode) and node.python):
                name = getattr(node, "function", None) or node.func_name
                errors.append(f"{path}: Python BitBake function {name} is unsupported; configure a Python extractor")
            elif isinstance(node, bitbake_ast.MethodNode):
                # BitBake names may hold ${...}; parse the body under a placeholder name.
                body = "\n".join(node.body)
                shells.append((path, f"bitbake_task() {{\n{body}\n}}", node.func_name))
    elif path.startswith(".github/") and path.endswith((".yml", ".yaml")):
        pending = [yaml.safe_load(text)]
        while pending:
            item = pending.pop()
            if isinstance(item, dict):
                if isinstance(item.get("run"), str):
                    if item.get("shell", "bash").split()[0] not in ("bash", "sh"):
                        errors.append(f"{path}: unsupported run shell {item['shell']}; configure its extractor")
                    shells.append((path, re.sub(r"\$\{\{.*?\}\}", "GITHUB_EXPRESSION", item["run"], flags=re.S), None))
                pending.extend(item.values())
            elif isinstance(item, list):
                pending.extend(item)
    elif path.endswith(".py") or re.match(r"#!.*python", first):
        for node in ast.walk(ast.parse(text, path)):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                errors.append(f"{path}: Python function {node.name} is unsupported; configure Python autodoc")
    elif Path(path).name == "Makefile":
        for line in text.splitlines():
            if line.startswith("\t"):
                shells.append((path, line[1:].replace("$$", "$"), make_recipe))
    elif not path.endswith(DATA) and Path(path).name not in DATA_NAMES:
        errors.append(f"{path}: unsupported source format; configure a native extractor for it")
    elif path.endswith(".html") and re.search(r"<script\b", text, re.I):
        errors.append(f"{path}: unsupported embedded script; configure a JavaScript extractor")

for path, text, task in shells:
    text = re.sub(r"\$\{@[^}]*\}", "BITBAKE_EXPRESSION", text)
    try:
        trees = bashlex.parse(text)
    except Exception as error:  # bashlex raises several parser error types
        errors.append(f"{path}: cannot parse shell ({error}); configure an extractor for this syntax")
        continue
    pending = [(tree, None) for tree in trees]
    while pending:
        node, current = pending.pop()
        if node.kind == "function":
            if task is make_recipe:
                errors.append(f"{path}: unsupported function {node.name.word} in a Makefile recipe; move it to a script")
            name = task if isinstance(task, str) and current is None else node.name.word
            functions.append({"path": path, "name": name, "arguments": False})
            current = functions[-1]
        elif node.kind == "parameter" and current is not None and re.fullmatch(r"[1-9@*#]", node.value):
            current["arguments"] = True
        elif node.kind == "command" and len(node.parts) > 2 and all(p.kind == "word" for p in node.parts[:3]) \
                and re.fullmatch(r"python3?", node.parts[0].word) and node.parts[1].word == "-c":
            try:
                definitions = [d.name for d in ast.walk(ast.parse(node.parts[2].word))
                               if isinstance(d, (ast.FunctionDef, ast.AsyncFunctionDef))]
            except SyntaxError as error:
                definitions = [f"(unparsed: {error})"]
            for name in definitions:
                errors.append(f"{path}: Python function {name} in python -c is unsupported; configure its extractor")
        for value in vars(node).values():
            for child in value if isinstance(value, list) else [value]:
                if isinstance(child, bashlex.ast.node):
                    pending.append((child, current))

pages = {}
for function in functions:
    page = function["path"].replace("/", "-")
    pages.setdefault(page, []).append(function)
for page in sorted({p.name[:-3] for p in generated.glob("*.md")} | set(pages)):
    markdown = (generated / f"{page}.md").read_text() if (generated / f"{page}.md").exists() else ""
    entries = re.findall(r"^### (.+)$", markdown, re.M)
    html = (site / f"{page}.html").read_text() if (site / f"{page}.html").exists() else ""
    names = [f["name"] for f in pages.get(page, [])]
    for name in set(entries) - set(names):
        errors.append(f"{page}: reference entry {name} has no discovered definition")
    anchors = sorted((html.find(f'id="{make_id(n)}"'), n) for n in names if f'id="{make_id(n)}"' in html)
    for function in pages.get(page, []):
        name, where = function["name"], f"{function['path']}: {function['name']}"
        block = markdown.partition(f"\n### {name}\n")[2].split("\n### ")[0]
        if not block:
            errors.append(f"{where} is missing its documentation comment or reference entry")
            continue
        no_arguments = "_Function has no arguments._" in block
        for field, present in (("an example", "#### Example" in block), ("exit codes", "#### Exit codes" in block),
                               ("arguments or @noargs", no_arguments or "#### Arguments" in block),
                               ("a purpose", bool(block.strip()) and not block.lstrip().startswith("#"))):
            if not present:
                errors.append(f"{where} documentation is missing {field}")
        if function["arguments"] == no_arguments:
            errors.append(f"{where} documents {'no ' if no_arguments else ''}arguments but "
                          f"{'reads' if function['arguments'] else 'never reads'} positional parameters")
        position = [i for i, (_, n) in enumerate(anchors) if n == name]
        if not position:
            errors.append(f"{where} is missing its rendered entry in {site / page}.html")
            continue
        start = anchors[position[0]][0]
        end = anchors[position[0] + 1][0] if position[0] + 1 < len(anchors) else len(html)
        if "Example" not in html[start:end] or "Exit codes" not in html[start:end]:
            errors.append(f"{where} rendered entry is missing its example or exit codes")

if errors:
    print("Reference coverage failed:", *errors, sep="\n  ", file=sys.stderr)
    sys.exit(1)
print(f"Reference coverage: {len(functions)} functions in {len(pages)} files documented and rendered")
