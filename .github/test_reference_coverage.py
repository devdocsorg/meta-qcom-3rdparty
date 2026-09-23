# Copyright (c) 2026 DevDocs
# SPDX-License-Identifier: BSD-3-Clause
"""Find the repository's functions and check their generated reference.

``docs/source/conf.py`` uses this module to pass shell code to shdoc and Python
modules to autodoc. After the HTML build, run it with the site directory to
compare every discovered function with its documentation comment and its
rendered reference entry; any gap or unsupported source fails the build::

    .venv/bin/python .github/test_reference_coverage.py docs/site

Shell scripts and workflow ``run`` steps are parsed with tree-sitter-bash,
BitBake metadata with BitBake's own statement and shell parsers, and Python
with ``ast``. Nothing is executed.
"""
import ast
import html
import logging
import re
import subprocess
import sys
from pathlib import Path

import tree_sitter_bash
import yaml
from tree_sitter import Language, Parser

ROOT = Path(__file__).resolve().parents[1]
BITBAKE_LIB = ROOT / ".venv/bitbake/lib"
BITBAKE_SUFFIXES = {".bb", ".bbappend", ".bbclass", ".inc", ".conf"}
YAML_SUFFIXES = {".yml", ".yaml"}
# Formats without function definitions. A new format fails until it is listed
# here or given an extractor.
DATA_SUFFIXES = {".md", ".txt", ".lock", ".cfg", ".html"}
DATA_NAMES = {"LICENSE", "NOTICE", "CODEOWNERS", "Makefile", ".gitignore", ".env.example"}
SHELL_TAGS = ("@description", "@exitcode", "@example")


def tracked_files(root: Path = ROOT) -> list[str]:
    """List tracked files outside the generated site.

    :param root: Repository checkout.
    :returns: Repository-relative paths from ``git ls-files``.
    :raises subprocess.CalledProcessError: If ``root`` is not a Git checkout.

    Example::

        tracked_files()  # ['.env.example', '.github/CODEOWNERS', ...]
    """
    listing = subprocess.run(["git", "ls-files"], cwd=root, check=True,
                             capture_output=True, text=True).stdout
    return [path for path in listing.splitlines()
            if not path.startswith("docs/site/") and not (root / path).is_symlink()]


def shell_units(path: str, root: Path = ROOT) -> list[str]:
    """Return the shell code in a tracked file, one unit per script or step.

    :param path: Repository-relative file path.
    :param root: Repository checkout.
    :returns: Shell scripts, BitBake shell functions with their comments, or
        workflow ``run`` scripts; an empty list for formats without code.
    :raises ValueError: For an unsupported source format or embedded language.

    Example::

        shell_units("ci/yocto-patchreview.sh")  # [whole script]
    """
    file = root / path
    suffix = file.suffix
    if suffix == ".sh":
        return [file.read_text()]
    if suffix in BITBAKE_SUFFIXES:
        return bitbake_units(path, root)
    if suffix in YAML_SUFFIXES:
        return run_steps(path, root)
    if suffix == ".html" and "<script" in file.read_text():
        raise ValueError(f"{path}: unsupported embedded script; configure an extractor")
    if suffix == ".py" or suffix in DATA_SUFFIXES or file.name in DATA_NAMES:
        return []
    raise ValueError(f"{path}: unsupported source format; configure its native "
                     "extractor in .github/test_reference_coverage.py and docs/source/conf.py")


def bitbake_units(path: str, root: Path = ROOT) -> list[str]:
    """Split BitBake metadata into shell functions with their comment blocks.

    BitBake's statement parser finds each definition, including ``fakeroot``
    tasks and names containing variables, without evaluating the metadata.

    :param path: Repository-relative ``.bb``, ``.bbappend``, ``.bbclass``,
        ``.inc``, or ``.conf`` file.
    :param root: Repository checkout.
    :returns: One ``name() { ... }`` unit per shell function.
    :raises ValueError: For a Python function, which has no configured extractor.

    Example::

        bitbake_units("recipes-bsp/firmware-boot/firmware-qcom-boot-rubikpi3_20260621.bb")
    """
    if str(BITBAKE_LIB) not in sys.path:
        sys.path.insert(0, str(BITBAKE_LIB))
    from bb.parse import ast as bbast
    from bb.parse.parse_py import BBHandler

    lines = (root / path).read_text().splitlines()
    units = []
    for node in BBHandler.get_statements(path, str(root / path), ""):
        if isinstance(node, bbast.PythonMethodNode) or getattr(node, "python", False):
            name = getattr(node, "func_name", None) or node.function
            raise ValueError(f"{path}:{node.lineno}: unsupported BitBake Python function "
                             f"{name}; configure a Python extractor for BitBake")
        if isinstance(node, bbast.MethodNode):
            start = node.lineno - len(node.body)  # node.lineno is the closing brace.
            first = start
            while first > 1 and lines[first - 2].lstrip().startswith("#"):
                first -= 1
            header = f"{node.func_name}() {{"  # Drop task modifiers such as fakeroot.
            units.append("\n".join(lines[first - 1:start - 1] + [header] + lines[start:node.lineno]) + "\n")
    return units


def run_steps(path: str, root: Path = ROOT) -> list[str]:
    """Return the shell scripts of GitHub workflow or action ``run`` steps.

    :param path: Repository-relative YAML file.
    :param root: Repository checkout.
    :returns: Each ``run`` value, inline or block, in document order.
    :raises ValueError: For a step whose ``shell`` is not bash or sh.

    Example::

        run_steps(".github/workflows/bitbake-lint.yml")  # ['rel=$(awk ...']
    """
    scripts, pending = [], [yaml.safe_load((root / path).read_text())]
    while pending:
        node = pending.pop(0)
        if isinstance(node, dict):
            if isinstance(node.get("run"), str):
                if node.get("shell", "bash") not in ("bash", "sh"):
                    raise ValueError(f"{path}: unsupported {node['shell']} run step; configure an extractor")
                scripts.append(node["run"])
            pending.extend(node.values())
        elif isinstance(node, list):
            pending.extend(node)
    return scripts


def shell_functions(unit: str, bitbake: bool = False) -> list[tuple[str, int]]:
    """Find the functions a shell unit defines, with their zero-based lines.

    :param unit: Shell code from :func:`shell_units`.
    :param bitbake: Parse with BitBake's shell parser, as BitBake does for tasks.
    :returns: ``(name, line)`` pairs.
    :raises ValueError: If the unit is not valid shell.

    Example::

        shell_functions('_is_dir(){\\n  test -d "$1"\\n}\\n')  # [('_is_dir', 0)]
    """
    if bitbake:
        from bb.codeparser import ShellParser
        parser = ShellParser("reference", logging.getLogger("reference"))
        try:
            parser.parse_shell(unit)
        except Exception as error:
            raise ValueError(f"BitBake cannot parse shell function: {error}") from error
        lines = unit.splitlines()
        return [(name, next(i for i, text in enumerate(lines)
                            if re.match(rf"\s*{re.escape(name)}\s*\(\s*\)", text)))
                for name in sorted(parser.funcdefs)]
    # GitHub substitutes ${{ }} expressions before the shell runs.
    code = re.sub(r"\$\{\{.*?\}\}", "GITHUB_EXPRESSION", unit, flags=re.S)
    tree = Parser(Language(tree_sitter_bash.language())).parse(code.encode())
    if tree.root_node.has_error:
        raise ValueError("tree-sitter-bash cannot parse the shell code")
    found, pending = [], [tree.root_node]
    while pending:
        node = pending.pop()
        if node.type == "function_definition":
            found.append((node.child_by_field_name("name").text.decode(), node.start_point[0]))
        pending.extend(node.children)
    return sorted(found, key=lambda item: item[1])


def comment_block(unit: str, line: int) -> str:
    """Return the comment lines directly above a line.

    :param unit: Shell code.
    :param line: Zero-based line of a function definition.
    :returns: The contiguous ``#`` lines before it, joined by newlines.

    Example::

        comment_block("# Say hello.\\nf() { :; }\\n", 1)  # '# Say hello.'
    """
    block = []
    for text in reversed(unit.splitlines()[:line]):
        if not text.lstrip().startswith("#"):
            break
        block.insert(0, text.strip())
    return "\n".join(block)


def python_definitions(path: str, root: Path = ROOT) -> tuple[str, list[tuple[str, int, bool]]]:
    """Return a Python file's module name and its documented definitions.

    Modules with definitions must be safe for autodoc to import: only imports,
    definitions, assignments, and a ``__main__`` guard may run at import time.

    :param path: Repository-relative ``.py`` file.
    :param root: Repository checkout.
    :returns: Module name and ``(qualified name, line, has docstring)`` entries
        for every function, class, and method.
    :raises ValueError: If the module has definitions but runs code on import.

    Example::

        python_definitions(".github/test_reference_coverage.py")
    """
    tree = ast.parse((root / path).read_text())
    found, pending = [], [(tree, "")]
    while pending:
        node, prefix = pending.pop(0)
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                found.append((prefix + child.name, child.lineno, ast.get_docstring(child) is not None))
                pending.append((child, prefix + child.name + "."))
    allowed = (ast.Import, ast.ImportFrom, ast.FunctionDef, ast.AsyncFunctionDef,
               ast.ClassDef, ast.Assign, ast.AnnAssign)
    for statement in tree.body[1 if ast.get_docstring(tree) is not None else 0:]:
        guard = isinstance(statement, ast.If) and "__main__" in ast.unparse(statement.test)
        if found and not (isinstance(statement, allowed) or guard):
            raise ValueError(f"{path}:{statement.lineno}: code runs on import; add a __main__ "
                             "guard so autodoc can import the module")
    return Path(path).stem, found


def check(site: Path, root: Path = ROOT) -> list[str]:
    """Compare discovered functions with their comments and rendered entries.

    :param site: Generated HTML site.
    :param root: Repository checkout.
    :returns: One message per undocumented function or missing reference entry.
    :raises ValueError: For unsupported sources, from :func:`shell_units`.

    Example::

        check(Path("docs/site"))  # [] when the reference is complete
    """
    problems = []
    for path in tracked_files(root):
        page = site / "contributing/.generated" / (path.replace("/", "-") + ".html")
        rendered = page.read_text() if page.is_file() else ""
        if path.endswith(".py"):
            module, definitions = python_definitions(path, root)
            for name, line, documented in definitions:
                if not documented:
                    problems.append(f"{path}:{line}: {name} is missing its docstring")
                elif f'id="{module}.{name}"' not in rendered:
                    problems.append(f"{path}:{line}: {name} is missing its reference entry in {page}")
            continue
        headings = {html.unescape(re.sub(r"<[^>]+>", "", heading))
                    for heading in re.findall(r"<h3>(.*?)<a class=\"headerlink\"", rendered)}
        bitbake = Path(path).suffix in BITBAKE_SUFFIXES
        for unit in shell_units(path, root):
            try:
                functions = shell_functions(unit, bitbake)
            except ValueError as error:
                raise ValueError(f"{path}: {error}") from error
            for name, line in functions:
                block = comment_block(unit, line)
                missing = [tag for tag in SHELL_TAGS if tag not in block]
                if "@arg" not in block and "@noargs" not in block:
                    missing.append("@arg or @noargs")
                if missing:
                    problems.append(f"{path}: {name} is missing documentation comment tags: {', '.join(missing)}")
                elif name not in headings:
                    problems.append(f"{path}: {name} is missing its reference entry in {page}")
    return problems


if __name__ == "__main__":
    try:
        failures = check(Path(sys.argv[1]).resolve())
    except ValueError as error:
        failures = [str(error)]
    for failure in failures:
        print(f"Reference coverage: {failure}", file=sys.stderr)
    sys.exit(1 if failures else 0)
