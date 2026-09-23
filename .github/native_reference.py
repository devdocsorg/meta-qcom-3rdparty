# Copyright (c) 2026 DevDocs
# SPDX-License-Identifier: BSD-3-Clause
"""Extract shell and Python references without executing layer build tasks."""
import ast
from pathlib import Path
import re
import shutil
import subprocess
import sys

import bashlex

ROOT = Path(__file__).resolve().parents[1]
GENERATED = Path('docs/source/contributing/.generated')
SHDOC = Path('docs/.tools/shdoc')
SOURCE_URL = 'https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/offline-contributor-guides/'


def sources(root: Path) -> list[Path]:
    """Return tracked and new maintained source paths, excluding generated output.

    :param root: Repository root directory.
    :type root: pathlib.Path
    :returns: Sorted source paths relative to root.
    :rtype: list[pathlib.Path]
    :raises subprocess.CalledProcessError: Git cannot enumerate the checkout.

    Example::

        files = sources(ROOT)
    """
    names = subprocess.check_output(
        ['git', 'ls-files', '-z', '--cached', '--others', '--exclude-standard'], cwd=root
    ).decode().split('\0')
    return sorted({Path(p) for p in names if p and (root / p).is_file()
                   and not p.startswith(('docs/site/', 'docs/source/contributing/.generated/'))})


def shell_functions(text: str) -> list[tuple[str, int]]:
    """Find every shell function using bashlex, including nested definitions.

    :param text: Shell source text; never executed.
    :type text: str
    :returns: Function names and zero-based declaration offsets.
    :rtype: list[tuple[str, int]]
    :raises ValueError: The parser encounters unsupported shell syntax.

    Example::

        shell_functions('check() { test -d "$1"; }')
    """
    found = []
    pending = list(bashlex.parse(text))
    while pending:
        node = pending.pop()
        if node.kind == 'function':
            found.append((node.name.word, node.pos[0]))
        for value in vars(node).values():
            if isinstance(value, bashlex.ast.node):
                pending.append(value)
            elif isinstance(value, list):
                pending.extend(item for item in value if isinstance(item, bashlex.ast.node))
    return sorted(set(found), key=lambda item: item[1])


def inventory(root: Path) -> dict[Path, list[tuple[str, int]]]:
    """Discover definitions independently of shdoc and autodoc output.

    :param root: Repository root directory.
    :type root: pathlib.Path
    :returns: Source paths mapped to function names and declaration offsets.
    :rtype: dict[pathlib.Path, list[tuple[str, int]]]
    :raises ValueError: Documentation or supported extraction is missing.

    Example::

        definitions = inventory(ROOT)
    """
    result = {}
    for path in sources(root):
        text = (root / path).read_text() if path.suffix in {'.py', '.sh', '.bb', '.bbappend', '.bbclass', '.inc', '.yml', '.yaml'} else ''
        definitions = []
        if path.suffix == '.py':
            tree = ast.parse(text, filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if node not in tree.body:
                        raise ValueError(f'{path}:{node.lineno}: configure extraction for nested/class functions')
                    doc = ast.get_docstring(node) or ''
                    for marker in (':returns:', ':rtype:', 'Example::'):
                        if marker not in doc:
                            raise ValueError(f'{path}:{node.name}: missing native docstring field {marker}')
                    for arg in node.args.posonlyargs + node.args.args + node.args.kwonlyargs:
                        if f':param {arg.arg}:' not in doc or f':type {arg.arg}:' not in doc:
                            raise ValueError(f'{path}:{node.name}: document parameter {arg.arg}')
                    definitions.append((node.name, node.lineno))
            if definitions and path != Path('.github/native_reference.py'):
                raise ValueError(f'{path}: configure a safe-to-import autodoc module before adding functions')
        elif path.suffix == '.sh':
            definitions = shell_functions(text)
        elif path.suffix in {'.bb', '.bbappend', '.bbclass', '.inc'}:
            if re.search(r'^\s*(?:python\s*\w*\s*\(|def\s+)', text, re.M):
                raise ValueError(f'{path}: configure native extraction for embedded Python before adding definitions')
            # BitBake metadata is not shell syntax. Its task bodies use a closing
            # brace at column zero; parse each task with the existing shell parser.
            declarations = list(re.finditer(r'^([\w:+.-]+)\s*\(\)\s*\{', text, re.M))
            for match in declarations:
                end = re.search(r'^}', text[match.end():], re.M)
                if end is None:
                    raise ValueError(f'{path}: unterminated task {match[1]}')
                chunk = text[match.start():match.end() + end.end()]
                definitions.extend((name, offset + match.start()) for name, offset in shell_functions(chunk))
            if re.search(r'^(?:fakeroot|python)\b.*\{', text, re.M):
                raise ValueError(f'{path}: configure extraction for this BitBake function form')
        elif path.suffix in {'.yml', '.yaml'}:
            if re.search(r'^\s*(?:def\s+\w+|function\s+\w+|[\w-]+\s*\(\)\s*\{)', text, re.M):
                raise ValueError(f'{path}: configure extraction for embedded workflow functions')
        if definitions:
            if path.suffix != '.py':
                for name, offset in definitions:
                    before = text[:offset].splitlines()
                    comments = []
                    for line in reversed(before):
                        if line.startswith('#'):
                            comments.append(line)
                        else:
                            break
                    doc = '\n'.join(reversed(comments))
                    for marker in ('@description', '@example', '@exitcode'):
                        if marker not in doc:
                            raise ValueError(f'{path}:{name}: missing {marker}')
                    if '@arg ' not in doc and '@noargs' not in doc:
                        raise ValueError(f'{path}:{name}: document arguments or @noargs')
            result[path] = definitions
    return result


def generate(root: Path | None = None) -> None:
    """Generate shdoc Markdown and wrapped autodoc directives for the site.

    :param root: Repository root directory.
    :type root: pathlib.Path
    :returns: None; writes ignored reference intermediates.
    :rtype: None
    :raises ValueError: A function lacks comments or an extracted entry.
    :raises subprocess.CalledProcessError: shdoc fails.

    Example::

        generate(ROOT)
    """
    root = root or ROOT
    definitions = inventory(root)
    generated = root / GENERATED
    shutil.rmtree(generated, ignore_errors=True)
    generated.mkdir(parents=True)
    for path, functions in definitions.items():
        output = generated / (str(path).replace('/', '-') + '.md')
        if path.suffix == '.py':
            contents = ('# Reference tools\n\n```{eval-rst}\n'
                        '.. automodule:: native_reference\n'
                        '   :members:\n   :private-members:\n```\n')
        else:
            source = (root / path).read_text()
            contents = subprocess.check_output([str(root / 'docs/.tools/bin/gawk'), '-f', str(root / SHDOC)], input=source.encode()).decode()
            for name, _ in functions:
                if f'## {name}\n' not in contents and f'### {name}\n' not in contents:
                    raise ValueError(f'{path}:{name}: shdoc omitted a discovered function')
            # shdoc emits a function index above its headings; give each file a
            # concise page title while keeping the extracted fields untouched.
            title = 'RUBIK Pi boot firmware' if path.suffix == '.bb' else path.name
            contents = f'# {title}\n\n' + contents
        title, body = contents.split('\n', 1)
        contents = title + f'\n\n[Source: {path}]({SOURCE_URL}{path})\n' + body
        output.write_text(contents)


def check(root: Path | None = None) -> None:
    """Require a rendered HTML reference entry for every discovered function.

    :param root: Repository root directory.
    :type root: pathlib.Path
    :returns: None when all entries and rendered fields exist.
    :rtype: None
    :raises AssertionError: A page, entry, or rendered field is missing.

    Example::

        check(ROOT)
    """
    root = root or ROOT
    definitions = inventory(root)
    for path, functions in definitions.items():
        page = root / 'docs/site/contributing/.generated' / (str(path).replace('/', '-') + '.html')
        html = page.read_text()
        for name, _ in functions:
            anchor = f'native_reference.{name}' if path.suffix == '.py' else name.lower().lstrip('_').replace('_', '-')
            assert f'id="{anchor}"' in html, (path, name, 'missing rendered entry')
        assert '@exitcode' not in html and '@description' not in html and '.. automodule::' not in html, page
        if path.suffix == '.py':
            assert 'Parameters' in html and 'Return type' in html, page
        else:
            assert 'Exit codes' in html and 'Example' in html, page
    print(f'Native reference coverage: {sum(map(len, definitions.values()))} functions in {len(definitions)} files')


if __name__ == '__main__':
    check()
