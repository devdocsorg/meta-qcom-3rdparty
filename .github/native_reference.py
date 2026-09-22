# Copyright (c) 2026 DevDocs
# SPDX-License-Identifier: BSD-3-Clause
"""Discover local definitions independently and generate their native reference."""
import ast
from pathlib import Path
import re
import subprocess

import bashlex
import yaml
from docutils.nodes import make_id


def inventory(root: Path) -> dict[str, list[tuple[str, str]]]:
    """Discover functions in maintained Python, shell, and BitBake sources.

    Args:
        root (Path): Repository root, for example ``Path.cwd()``.

    Returns:
        dict[str, list[tuple[str, str]]]: Relative paths mapped to function names
        and their native documentation comments or docstrings.

    Raises:
        ValueError: A definition lacks documentation or uses unsupported syntax.

    Example:
        ``definitions = inventory(Path.cwd())`` discovers internal helpers too.
    """
    found = {}
    ignored = {'.git', '.venv', '.tools', '__pycache__', '.doctrees', '.generated'}
    for path in sorted(root.rglob('*')):
        relative = path.relative_to(root)
        if (not path.is_file() or any(p in ignored for p in relative.parts)
                or relative.parts[:2] == ('docs', 'site')):
            continue
        text = path.read_text(errors='replace')
        definitions = []
        if path.suffix == '.py':
            tree = ast.parse(text, filename=str(relative))
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    doc = ast.get_docstring(node) or ''
                    if not all(part in doc for part in ('Args:', 'Returns:', 'Example:')):
                        raise ValueError(f'{relative}:{node.name}: document purpose, types, return, and example')
                    if relative.as_posix() != '.github/native_reference.py':
                        raise ValueError(f'{relative}:{node.name}: configure safe Python autodoc for this module')
                    definitions.append((node.name, doc))
        elif path.suffix in {'.sh', '.bb', '.bbappend', '.bbclass', '.inc', '.conf'}:
            if re.search(r'^\s*(?:python\s+\w*\s*\(|(?:async\s+)?def\s+)', text, re.M):
                raise ValueError(f'{relative}: configure safe native extraction for embedded Python definitions')
            chunks = [text] if path.suffix == '.sh' else re.findall(
                r'(?m)^[ \t]*[\w:+.-]+[ \t]*\(\)[ \t]*\{[\s\S]*?^\}', text)
            for chunk in chunks:
                nodes = list(bashlex.parse(chunk))
                while nodes:
                    node = nodes.pop()
                    if node.kind == 'function':
                        name = node.name.word
                        declaration = chunk[node.pos[0]:node.pos[1]]
                        start = text.index(declaration)
                        prefix = text[:start].splitlines()
                        comments = []
                        for line in reversed(prefix):
                            if not line.strip().startswith('#'):
                                break
                            comments.append(line)
                        doc = '\n'.join(reversed(comments))
                        if not all(tag in doc for tag in ('@description', '@example', '@exitcode')):
                            raise ValueError(f'{relative}:{name}: missing shdoc purpose, example, or exit status')
                        if '@arg' not in doc and 'No positional arguments' not in doc:
                            raise ValueError(f'{relative}:{name}: document argument types or no arguments')
                        definitions.append((name, doc))
                    for value in vars(node).values():
                        if isinstance(value, bashlex.ast.node):
                            nodes.append(value)
                        elif isinstance(value, list):
                            nodes.extend(v for v in value if isinstance(v, bashlex.ast.node))
            # BitBake supports task modifiers; do not let an unhandled form vanish.
            declarations = re.findall(r'(?m)^\s*(?:(?:fakeroot|python)\s+)?([\w:+.-]+)\s*\(\s*\)\s*\{', text)
            if len(declarations) != len(definitions):
                raise ValueError(f'{relative}: unsupported shell/task definition; extend native extraction')
        elif relative.parts[:2] == ('.github', 'workflows') and path.suffix in {'.yml', '.yaml'}:
            pending = [yaml.safe_load(text)]
            while pending:
                value = pending.pop()
                if isinstance(value, dict):
                    run = value.get('run', '')
                    if isinstance(run, str) and re.search(
                            r'(?m)^\s*(?:(?:async\s+)?def\s+|function\s+|[\w.-]+\s*\(\s*\)\s*\{)', run):
                        raise ValueError(f'{relative}: configure native extraction for workflow definitions')
                    pending.extend(value.values())
                elif isinstance(value, list):
                    pending.extend(value)
        elif path.suffix in {'.js', '.ts', '.c', '.h', '.cpp', '.rs', '.go', '.java'}:
            raise ValueError(f'{relative}: configure the language native extractor before adding source')
        if definitions:
            found[relative.as_posix()] = definitions
    return found


def generate(root: Path) -> None:
    """Generate shdoc and autodoc source pages without running layer code.

    Args:
        root (Path): Repository root, for example ``Path.cwd()``.

    Returns:
        None: Writes ignored Markdown intermediates below the contributor area.

    Raises:
        RuntimeError: shdoc omits a discovered definition.

    Example:
        ``generate(Path.cwd())`` is called by Sphinx configuration.
    """
    target = root / 'docs/source/contributing/.generated'
    target.mkdir(exist_ok=True)
    for old in target.glob('*.md'):
        old.unlink()
    for relative, definitions in inventory(root).items():
        output = target / (relative.replace('/', '-') + '.md')
        if relative.endswith('.py'):
            output.write_text('# Documentation reference tools\n\n```{eval-rst}\n'
                              '.. automodule:: native_reference\n'
                              '   :members:\n   :private-members:\n```\n')
        else:
            result = subprocess.run(['gawk', '-f', str(root / '.tools/shdoc/shdoc')],
                                    input=(root / relative).read_text(), text=True,
                                    capture_output=True, check=True)
            for name, _ in definitions:
                if f'### {name}\n' not in result.stdout:
                    raise RuntimeError(f'{relative}:{name}: shdoc omitted definition')
            output.write_text(result.stdout)


def verify(root: Path) -> None:
    """Compare independently discovered functions with rendered native entries.

    Args:
        root (Path): Built repository root, for example ``Path.cwd()``.

    Returns:
        None: Prints the number of verified reference entries.

    Raises:
        ValueError: A discovered function has no rendered native heading or ID.

    Example:
        ``verify(Path.cwd())`` checks a completed ``make html`` build.
    """
    count = 0
    for relative, definitions in inventory(root).items():
        page = root / 'docs/site/contributing/.generated' / (relative.replace('/', '-') + '.html')
        html = page.read_text() if page.exists() else ''
        for name, _ in definitions:
            identifier = 'native_reference.' + name if relative.endswith('.py') else make_id(name)
            if f'id="{identifier}"' not in html:
                raise ValueError(f'{relative}:{name}: missing rendered reference entry {identifier}')
            count += 1
    print(f'{count} native function entries verified')
