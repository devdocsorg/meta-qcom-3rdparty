"""Inventory definitions independently, then generate and check native references.

Shell and BitBake task comments are rendered by pinned shdoc. Python modules use
Sphinx autodoc; AST parsing never imports product code or executes build tasks.
"""
import ast
from pathlib import Path
import re
import shutil
import subprocess

import bashlex
from docutils.nodes import make_id

def source_files(root: Path) -> list[Path]:
    """Return maintained source paths using Git's tracked and unignored inventory.

    :param root: Repository root (Path), for example ``Path.cwd()``.
    :returns: Sorted list of repository-relative Paths, excluding generated HTML.
    :raises subprocess.CalledProcessError: Git cannot enumerate the repository.

    Example: ``source_files(Path.cwd())`` includes ``Path('ci/yocto-check-layer.sh')``.
    """
    output = subprocess.check_output(
        ['git', '-C', str(root), 'ls-files', '-z', '--cached', '--others', '--exclude-standard'],
        text=True,
    )
    return sorted({Path(name) for name in output.split('\0') if name
                   and not name.startswith('docs/site/') and (root / name).is_file()})


def shell_functions(text: str) -> list[tuple[str, int]]:
    """Discover shell function names and positions with bashlex's independent AST.

    :param text: Shell source string, such as ``'f() { :; }'``.
    :returns: List of (name string, character offset integer) pairs, including helpers.
    :raises ValueError: Shell syntax cannot be parsed; update parser support explicitly.

    Example: ``shell_functions('f() { :; }')`` returns ``[('f', 0)]``.
    """
    try:
        pending = list(bashlex.parse(text))
    except (NotImplementedError, bashlex.errors.ParsingError) as error:
        raise ValueError(f'Unsupported shell syntax; configure the parser: {error}') from error
    found = []
    while pending:
        node = pending.pop()
        if node.kind == 'function':
            found.append((node.name.word, node.pos[0]))
        for value in vars(node).values():
            if isinstance(value, bashlex.ast.node):
                pending.append(value)
            elif isinstance(value, list):
                pending.extend(item for item in value if isinstance(item, bashlex.ast.node))
    return sorted(set(found))


def inventory(root: Path) -> dict[Path, list[str]]:
    """Validate native comments and discover all shell, BitBake, and Python definitions.

    :param root: Repository root Path, for example ``Path.cwd()``.
    :returns: Mapping from relative source Path to discovered qualified function names.
    :raises ValueError: Documentation is missing or a definition needs extractor support.

    Example: ``inventory(Path.cwd())[Path('ci/yocto-buildstats.sh')]`` is ``['_is_dir']``.
    """
    found = {}
    for path in source_files(root):
        text = (root / path).read_text() if path.suffix in {'.sh', '.bb', '.bbappend', '.bbclass', '.inc', '.conf', '.py'} else ''
        if path.suffix == '.py':
            tree = ast.parse(text)
            definitions = [node for node in ast.walk(tree)
                           if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]
            names = []
            for node in definitions:
                parents = [parent for parent in ast.walk(tree)
                           if isinstance(parent, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef))
                           and parent is not node and node in ast.walk(parent)]
                if any(isinstance(parent, (ast.FunctionDef, ast.AsyncFunctionDef)) for parent in parents):
                    raise ValueError(f'{path}:{node.name}: nested function needs native extractor support')
                name = '.'.join([parent.name for parent in parents] + [node.name])
                doc = ast.get_docstring(node) or ''
                if not all(field in doc for field in (':returns:', 'Example:')):
                    raise ValueError(f'{path}:{name}: missing native purpose, return, or example documentation')
                args = node.args.posonlyargs + node.args.args + node.args.kwonlyargs
                if any(arg.arg not in {'self', 'cls'} and f':param {arg.arg}:' not in doc for arg in args):
                    raise ValueError(f'{path}:{name}: missing parameter documentation')
                names.append(name)
            if names:
                found[path] = names
            continue
        if path.suffix == '.sh':
            functions = shell_functions(text)
        elif path.suffix in {'.bb', '.bbappend', '.bbclass', '.inc', '.conf'}:
            if re.search(r'^\s*(?:python\s|python\(|def\s|async\s+def\s)', text, re.M):
                raise ValueError(f'{path}: embedded Python definitions need a safe native extractor; configure one before building')
            functions = []
            # BitBake metadata outside task blocks is not shell. Identify its task
            # delimiters, then let bashlex parse each shell body independently.
            starts = list(re.finditer(r'^([^#\n]*?\(\)\s*\{)', text, re.M))
            for start in starts:
                if not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*\s*\(\)\s*\{', start[1]):
                    raise ValueError(f'{path}: unsupported task signature {start[1]!r}; configure native extraction')
                end = re.search(r'^\}', text[start.end():], re.M)
                if end is None:
                    raise ValueError(f'{path}: unterminated BitBake task')
                task = text[start.start():start.end() + end.end()]
                functions.extend((name, offset + start.start()) for name, offset in shell_functions(task))
        else:
            continue
        for name, offset in functions:
            lines = text[:offset].rstrip('\n').splitlines()
            comments = []
            for line in reversed(lines):
                if not line.lstrip().startswith('#'):
                    break
                comments.append(line)
            comment = '\n'.join(reversed(comments))
            if not all(tag in comment for tag in ('@description', '@example', '@exitcode')):
                raise ValueError(f'{path}:{name}: missing shdoc purpose, example, or exit-code documentation')
            if re.search(r'\$[1-9]', text[offset:]) and '@arg' not in comment:
                raise ValueError(f'{path}:{name}: missing shdoc argument documentation')
        if functions:
            found[path] = [name for name, offset in functions]
    return found


def generate(root: Path) -> None:
    """Generate native-reference source pages without executing product functions.

    :param root: Repository root Path; ``generate(Path.cwd())`` is used by Sphinx.
    :returns: None; writes ignored intermediate Markdown under the contributor area.
    :raises ValueError: Inventory or extraction misses documented definitions.
    :raises subprocess.CalledProcessError: Pinned shdoc fails.

    Example: ``generate(Path.cwd())`` creates the shell task and Python reference pages.
    """
    functions = inventory(root)
    destination = root / 'docs/source/contributing/.generated'
    shutil.rmtree(destination, ignore_errors=True)
    destination.mkdir(parents=True)
    python_pages = ['# Python documentation tools\n\nNative docstrings are rendered by Sphinx autodoc.\n']
    for path, names in functions.items():
        if path.suffix == '.py':
            python_pages.append(f'\n## {path.as_posix()}\n\n```{{eval-rst}}\n.. automodule:: {path.stem}\n   :members:\n   :private-members:\n   :undoc-members:\n```\n')
            continue
        rendered = subprocess.check_output(
            ['gawk', '-f', str(root / '.tools/shdoc/shdoc')],
            input=f'# @file {path.as_posix()}\n' + (root / path).read_text(), text=True,
        )
        for name in names:
            if f'## {name}\n' not in rendered and f'### {name}\n' not in rendered:
                raise ValueError(f'{path}:{name}: shdoc omitted a discovered function')
        (destination / (path.as_posix().replace('/', '-') + '.md')).write_text(rendered)
    (destination / 'python-reference.md').write_text(''.join(python_pages))


def check_rendered(root: Path, site: Path) -> dict[str, list[str]]:
    """Require actual native-domain HTML entries for every discovered function.

    :param root: Repository root Path, for example ``Path.cwd()``.
    :param site: Generated site Path, for example ``root / 'docs/site'``.
    :returns: Source-path strings mapped to documented function-name lists.
    :raises ValueError: A rendered reference entry is missing or documentation is invalid.

    Example: ``check_rendered(Path.cwd(), Path('docs/site'))`` validates the built reference.
    """
    discovered = inventory(root)
    for path, names in discovered.items():
        if path.suffix == '.py':
            page = site / 'contributing/.generated/python-reference.html'
            ids = [path.stem + '.' + name for name in names]
        else:
            page = site / 'contributing/.generated' / (path.as_posix().replace('/', '-') + '.html')
            ids = [make_id(name) for name in names]
        html = page.read_text() if page.exists() else ''
        for name in ids:
            if f'id="{name}"' not in html:
                raise ValueError(f'{path}:{name}: missing rendered native reference entry')
    return {path.as_posix(): names for path, names in discovered.items()}
