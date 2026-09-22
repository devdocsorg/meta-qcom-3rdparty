# Copyright (c) 2026 DevDocs
# SPDX-License-Identifier: MIT
"""Generate and check native shell and Python references without running BSP tasks."""
from __future__ import annotations

import ast
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

import bashlex
import yaml

ROOT = Path(__file__).resolve().parents[1]
GENERATED = ROOT / 'docs/source/contributing/.generated'


def source_files(root: Path) -> list[Path]:
    """List maintained tracked and unignored new files below a checkout.

    :param root: Absolute checkout path.
    :return: Sorted paths, excluding dependencies and generated documentation.
    :raises subprocess.CalledProcessError: If root is not a Git checkout.

    Example: ``source_files(ROOT)`` includes hidden workflow sources.
    """
    paths = subprocess.check_output(
        ['git', 'ls-files', '-z', '--cached', '--others', '--exclude-standard'],
        cwd=root, text=True).split('\0')
    return sorted({root / name for name in paths if name and
                   not name.startswith(('docs/site/', 'docs/source/contributing/.generated/'))
                   and (root / name).is_file()})


def shell_functions(text: str) -> list[tuple[str, int]]:
    """Discover shell definitions through Bash syntax nodes, including nested helpers.

    :param text: Shell source string; no commands are executed.
    :return: Function name and zero-based character offset pairs.
    :raises ValueError: If shell syntax is unsupported by the pinned parser.

    Example: ``shell_functions('f() { :; }')`` returns ``[('f', 0)]``.
    """
    try:
        pending = list(bashlex.parse(text))
    except (NotImplementedError, bashlex.errors.ParsingError) as error:
        raise ValueError(f'Unsupported shell syntax: extend the native inventory parser: {error}') from error
    found = []
    while pending:
        node = pending.pop()
        if node.kind == 'command':
            words = [part.word for part in node.parts if part.kind == 'word']
            if words and re.fullmatch(r'(?:.*/)?python(?:[23](?:\.\d+)?)?', words[0]) and '-c' in words:
                code_index = words.index('-c') + 1
                if code_index < len(words):
                    embedded = ast.parse(words[code_index])
                    if any(isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)) for item in ast.walk(embedded)):
                        raise ValueError('Inline Python definition: configure safe native Python extraction for the shell command')
        if node.kind == 'function':
            name = next(part.word for part in node.parts if part.kind == 'word')
            found.append((name, node.pos[0]))
        for value in vars(node).values():
            if isinstance(value, bashlex.ast.node):
                pending.append(value)
            elif isinstance(value, list):
                pending.extend(part for part in value if isinstance(part, bashlex.ast.node))
    return sorted(set(found))


def comment_before(text: str, offset: int) -> str:
    """Read the contiguous native comment immediately preceding a definition.

    :param text: Original source string.
    :param offset: Zero-based definition start offset.
    :return: Comment text including its hash prefixes.
    :raises ValueError: If the offset is outside the source.

    Example: ``comment_before('# @noargs\\nf() { :; }', 10)`` reads the annotation.
    """
    if not 0 <= offset <= len(text):
        raise ValueError('Definition offset outside source')
    lines = text[:offset].rstrip().splitlines()
    block = []
    for line in reversed(lines):
        if not line.lstrip().startswith('#'):
            break
        block.append(line)
    return '\n'.join(reversed(block))


def bitbake_functions(path: Path) -> list[tuple[str, int]]:
    """Inventory BitBake task definitions through its native parse-only statement API.

    :param path: Recipe, append, class, include, or configuration path.
    :return: Shell task names and source offsets; inherited tasks are excluded.
    :raises ValueError: For embedded Python or shell forms requiring extractor setup.
    :raises RuntimeError: If the pinned BitBake parser is missing.

    Example: ``bitbake_functions(ROOT / 'recipes-bsp/firmware-boot/firmware-qcom-boot-rubikpi3_20260621.bb')``.
    No statements are evaluated, no includes loaded, and no tasks run.
    """
    parser_path = ROOT / '.doc-tools/bitbake/lib'
    if not parser_path.is_dir():
        raise RuntimeError('Run make -f docs/source/Makefile setup to install the BitBake parser')
    sys.path.insert(0, str(parser_path))
    from bb.parse.parse_py import BBHandler
    from bb.parse import ast as bbast
    text = path.read_text()
    if re.search(r'\$\{@[^}]*\blambda\b', text):
        raise ValueError(f'{path}: inline Python definition needs safe native extraction')
    # The upstream parser keeps state for one file. Reset it without calling eval().
    BBHandler.__infunc__ = []
    BBHandler.__inpython__ = False
    BBHandler.__body__ = []
    BBHandler.__residue__ = []
    BBHandler.cached_statements.clear()
    statements = BBHandler.get_statements(str(path), str(path), path.name)
    result = []
    for statement in statements:
        if isinstance(statement, bbast.PythonMethodNode) or (
                isinstance(statement, bbast.MethodNode) and statement.python):
            raise ValueError(f'{path}: embedded Python definition: configure safe native Python extraction before adding this definition')
        if isinstance(statement, bbast.MethodNode):
            name = statement.func_name
            start = statement.lineno - len(statement.body)
            offset = sum(len(line) for line in text.splitlines(keepends=True)[:start - 1])
            header = text[offset:text.find('\n', offset)]
            if not re.fullmatch(r'[A-Za-z_]\w*\s*\(\s*\)\s*\{', header):
                raise ValueError(f'{path}:{start}: extend shdoc adaptation for BitBake definition {name}')
            # Bash parses only the task body; BitBake assignments are not shell syntax.
            body = '\n'.join(statement.body)
            if shell_functions(body):
                raise ValueError(f'{path}:{start}: nested task functions need a shdoc extraction adapter')
            result.append((name, offset))
    return result


def inventory(root: Path) -> tuple[dict[str, list[tuple[str, int]]], list[str]]:
    """Independently discover functions across maintained source and mixed-language files.

    :param root: Absolute checkout path.
    :return: Shell definitions keyed by relative path and Python callable names.
    :raises ValueError: For undocumented Python or unsupported language definitions.

    Example: ``shell, python = inventory(ROOT)`` includes private helpers.
    """
    shell = {}
    python = []
    known = {'.md', '.txt', '.rst', '.html', '.css', '.cfg', '.lock', '.json', '.MIT', ''}
    for path in source_files(root):
        relative = path.relative_to(root).as_posix()
        text = path.read_text()
        if path.suffix == '.py':
            tree = ast.parse(text, filename=relative)
            definitions = [node for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda))]
            for node in definitions:
                if not isinstance(node, ast.FunctionDef) or node not in tree.body or relative != '.github/doc_reference.py':
                    raise ValueError(f'{relative}:{node.lineno}: configure safe native autodoc extraction for this Python definition')
                doc = ast.get_docstring(node) or ''
                for required in (':param ', ':return:', ':raises ', 'Example:'):
                    if required not in doc:
                        raise ValueError(f'{relative}:{node.lineno}: missing Python documentation {required}')
                python.append(node.name)
        elif path.suffix in {'.bb', '.bbappend', '.bbclass', '.inc', '.conf'}:
            functions = bitbake_functions(path)
            if functions:
                shell[relative] = functions
        elif path.suffix in {'.sh', '.bash'} or text.startswith(('#!/bin/sh', '#!/bin/bash', '#!/usr/bin/env bash')):
            functions = shell_functions(text)
            if functions:
                shell[relative] = functions
        elif path.suffix in {'.yml', '.yaml'}:
            # Discover executable workflow blocks without evaluating Actions expressions.
            pending = [yaml.safe_load(text)]
            while pending:
                item = pending.pop()
                if isinstance(item, dict):
                    for key, value in item.items():
                        if key == 'run' and isinstance(value, str):
                            cleaned = re.sub(r'\$\{\{.*?\}\}', 'expression', value, flags=re.S)
                            if shell_functions(cleaned):
                                raise ValueError(f'{relative}: workflow shell definition needs a shdoc extraction adapter')
                        else:
                            pending.append(value)
                elif isinstance(item, list):
                    pending.extend(item)
        elif path.suffix not in known and path.name not in {'Makefile', '.gitignore', '.env.example', 'CODEOWNERS'}:
            raise ValueError(f'{relative}: unknown source format; configure its native extractor or document why it contains no definitions')
    return shell, sorted(python)


def generate(root: Path) -> None:
    """Extract annotated shell functions with shdoc and create native autodoc navigation.

    :param root: Absolute checkout path.
    :return: None; replaces only ignored generated reference sources.
    :raises ValueError: If comments or shdoc entries omit any discovered definition.
    :raises subprocess.CalledProcessError: If the pinned extractor fails.

    Example: ``generate(ROOT)`` prepares sources for the strict Sphinx build.
    """
    shell, python = inventory(root)
    shutil.rmtree(GENERATED, ignore_errors=True)
    GENERATED.mkdir(parents=True)
    pages = []
    entries = {}
    for relative, functions in shell.items():
        text = (root / relative).read_text()
        for name, offset in functions:
            block = comment_before(text, offset)
            for required in ('@description', '@example', '@exitcode'):
                if required not in block:
                    raise ValueError(f'{relative}:{name}: missing native comment {required}')
            if '@arg ' not in block and '@noargs' not in block:
                raise ValueError(f'{relative}:{name}: document argument types or @noargs')
            if '@internal' in block:
                raise ValueError(f'{relative}:{name}: internal functions must remain in the reference')
        output = subprocess.check_output(
            ['gawk', '-f', str(root / '.doc-tools/shdoc/shdoc')], input=text, text=True)
        output = re.sub(r'\n{3,}', '\n\n', output)
        extracted = re.findall(r'^### (\S+)\s*$', output, re.M)
        expected = [name for name, _ in functions]
        if sorted(extracted) != sorted(expected):
            raise ValueError(f'{relative}: shdoc coverage differs: discovered {expected}, extracted {extracted}')
        slug = relative.replace('/', '--').replace('.', '-')
        (GENERATED / f'{slug}.md').write_text(f'# {relative}\n\n' + output)
        pages.append(slug)
        entries[slug] = expected
    pytext = 'Documentation tooling\n=====================\n\n'
    for name in python:
        pytext += f'.. autofunction:: doc_reference.{name}\n\n'
    (GENERATED / 'python.rst').write_text(pytext)
    pages.append('python')
    (GENERATED / 'index.rst').write_text('Native function reference\n=========================\n\n'
        'Generated from native comments; private helpers are included.\n\n'
        '.. toctree::\n   :maxdepth: 2\n\n' + ''.join(f'   {page}\n' for page in pages))
    (GENERATED / 'inventory.json').write_text(json.dumps({'shell': entries, 'python': python}, indent=2) + '\n')
    print(f'Native inventory: {sum(map(len, shell.values()))} shell definitions, {len(python)} Python definitions')


def check_output(root: Path) -> None:
    """Compare independently discovered functions with final generated HTML anchors.

    :param root: Absolute checkout path.
    :return: None when every native entry is present.
    :raises ValueError: If a function or reference anchor is missing.

    Example: ``check_output(ROOT)`` fails if an extractor omits an internal helper.
    """
    shell, python = inventory(root)
    base = root / 'docs/site/contributing/.generated'
    for relative, functions in shell.items():
        slug = relative.replace('/', '--').replace('.', '-')
        page = (base / f'{slug}.html').read_text()
        for name, _ in functions:
            # MyST heading IDs replace underscores with hyphens and strip leading ones.
            anchor = name.replace('_', '-').strip('-')
            if f'id="{anchor}"' not in page:
                raise ValueError(f'{relative}:{name}: missing native HTML reference entry')
    page = (base / 'python.html').read_text()
    for name in python:
        if f'id="doc_reference.{name}"' not in page:
            raise ValueError(f'Python {name}: missing native HTML reference entry')
    print('Native HTML coverage matches the independent source inventory')


if __name__ == '__main__':
    if len(sys.argv) != 2 or sys.argv[1] not in {'generate', 'check'}:
        raise SystemExit('Usage: doc_reference.py generate|check')
    if sys.argv[1] == 'generate':
        generate(ROOT)
    else:
        check_output(ROOT)
