# Copyright (c) 2026 DevDocs
# SPDX-License-Identifier: BSD-3-Clause
"""Discover local definitions and build native shell and Python references safely.

Only this side-effect-free module is imported by autodoc. BitBake metadata is
parsed into statements, never evaluated, and shell code is never executed.
"""
from __future__ import annotations

import ast
import importlib
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from typing import Any

import bashlex
import yaml
from sphinx.application import Sphinx

ROOT = Path(__file__).resolve().parents[1]
BB_FORMATS = {'.bb', '.bbappend', '.bbclass', '.inc', '.conf'}
CODE_FORMATS = {'.js', '.ts', '.tsx', '.jsx', '.c', '.h', '.cpp', '.hpp', '.rs', '.go', '.java', '.rb', '.pl', '.lua', '.awk'}


def tracked(root: Path) -> list[Path]:
    """Return tracked source paths, including staged additions.

    :param root: Repository root directory.
    :returns: Existing tracked files outside generated site output.
    :raises subprocess.CalledProcessError: Git cannot read the index.
    :example: ``tracked(ROOT)`` includes ``ci/yocto-check-layer.sh``.
    """
    output = subprocess.check_output(['git', 'ls-files', '-z'], cwd=root, text=True)
    return [root / p for p in output.split('\0') if p and not p.startswith('docs/site/') and (root / p).is_file()]


def shell_nodes(code: str) -> list[Any]:
    """Find every shell function through bashlex, including nested definitions.

    :param code: Shell text with container substitutions already normalized.
    :returns: Function AST nodes with source offsets.
    :raises ValueError: Shell syntax requires parser support.
    :example: ``shell_nodes('helper() { :; }')[0].name.word`` is ``helper``.
    """
    found = []
    try:
        pending = list(bashlex.parse(code))
    except (bashlex.errors.ParsingError, NotImplementedError) as error:
        raise ValueError(f'Unsupported shell syntax; configure native parser support: {error}') from error
    while pending:
        node = pending.pop()
        if not isinstance(node, bashlex.ast.node):
            continue
        if node.kind == 'function':
            found.append(node)
        for value in vars(node).values():
            if isinstance(value, bashlex.ast.node):
                pending.append(value)
            elif isinstance(value, list):
                pending.extend(value)
    return sorted(found, key=lambda n: n.pos[0])


def comment_before(text: str, line: int) -> str:
    """Read the contiguous comment immediately before a definition.

    :param text: Complete source text.
    :param line: One-based definition line.
    :returns: Comment lines in source order.
    :example: ``comment_before('# @noargs\\nf() {}', 2)`` returns ``# @noargs``.
    """
    lines = text.splitlines()[:line - 1]
    comments = []
    for item in reversed(lines):
        if not item.lstrip().startswith('#'):
            break
        comments.append(item.lstrip())
    return '\n'.join(reversed(comments))


def require_shell_docs(comment: str, label: str) -> None:
    """Reject missing native shell fields before invoking shdoc.

    :param comment: Native shdoc comment preceding a function.
    :param label: Source path and function name for actionable diagnostics.
    :returns: None when the comment supplies purpose, arguments, status, and example.
    :raises ValueError: Required documentation is absent.
    :example: ``require_shell_docs('', 'ci/helper.sh:check')`` raises ``ValueError``.
    """
    for annotation in ('@description', '@example', '@exitcode'):
        if annotation not in comment:
            raise ValueError(f'{label}: missing {annotation} documentation')
    if '@arg ' not in comment and '@noargs' not in comment:
        raise ValueError(f'{label}: missing typed @arg or @noargs documentation')
    for argument in re.findall(r'@arg\s+([^\n]+)', comment):
        if len(argument.split()) < 3:
            raise ValueError(f'{label}: missing argument type or description')


def bitbake_units(path: Path) -> list[tuple[str, str, str]]:
    """Discover BitBake tasks using upstream statements without evaluating them.

    :param path: Metadata file in any maintained BitBake format.
    :returns: Tuples of task name, native comment, and normalized shell source.
    :raises ValueError: Embedded Python or a modified task needs extractor setup.
    :example: ``bitbake_units(ROOT / 'conf/layer.conf')`` returns an empty list.
    """
    sys.path.insert(0, str(ROOT / '.docs-tools/bitbake/lib'))
    handler = importlib.import_module('bb.parse.parse_py.BBHandler')
    bbast = importlib.import_module('bb.parse.ast')
    # get_statements expects the parser's transient state to be fresh per file.
    for name, value in [('__infunc__', []), ('__body__', []), ('__residue__', []), ('__inpython__', False), ('__classname__', '')]:
        setattr(handler, name, value)
    handler.cached_statements.clear()
    statements = handler.get_statements(str(path), str(path), path.name)
    source = path.read_text()
    units = []
    for statement in statements:
        if isinstance(statement, bbast.PythonMethodNode) or isinstance(statement, bbast.MethodNode) and statement.python:
            name = getattr(statement, 'func_name', getattr(statement, 'function', 'python'))
            raise ValueError(f'{path}:{name}: unsupported embedded Python definition; configure a static Python extractor')
        if not isinstance(statement, bbast.MethodNode):
            continue
        name = statement.func_name
        line = statement.lineno - len(statement.body)
        comment = comment_before(source, line)
        require_shell_docs(comment, f'{path}:{name}')
        if not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', name):
            raise ValueError(f'{path}:{name}: configure shdoc rendering for expanded or override task names')
        body = '\n'.join(statement.body)
        # BitBake substitutions are metadata, not shell parameter expressions.
        normalized = re.sub(r'\$\{[^}]*\}', 'BITBAKE_VALUE', body)
        units.append((name, comment, f'{name}() {{\n{normalized}\n}}\n'))
    return units


def workflow_units(path: Path) -> list[tuple[str, str]]:
    """Extract shell run values from parsed YAML, including inline values.

    :param path: GitHub Actions workflow path.
    :returns: Pairs of diagnostic labels and shell code.
    :raises ValueError: A run step uses an unsupported interpreter with definitions.
    :example: ``workflow_units(ROOT / '.github/workflows/push.yml')`` is empty.
    """
    document = yaml.safe_load(path.read_text())
    result = []
    for job_id, job in document.get('jobs', {}).items():
        for index, step in enumerate(job.get('steps', [])):
            if 'run' not in step:
                continue
            code = str(step['run'])
            interpreter = step.get('shell', job.get('defaults', {}).get('run', {}).get('shell', document.get('defaults', {}).get('run', {}).get('shell', 'bash')))
            label = f'{path}:jobs.{job_id}.steps.{index}'
            if interpreter not in ('bash', 'sh'):
                raise ValueError(f'{label}: unsupported {interpreter} source; configure its native extractor')
            result.append((label, re.sub(r'\$\{\{.*?\}\}', 'WORKFLOW_VALUE', code, flags=re.S)))
    return result


def inventory(root: Path) -> dict[str, list[str]]:
    """Independently discover and validate all maintained local definitions.

    :param root: Root of the Git checkout.
    :returns: Source-relative paths mapped to discovered function names.
    :raises ValueError: Documentation or supported extraction is missing.
    :example: ``inventory(ROOT)['ci/yocto-check-layer.sh']`` contains ``_is_dir``.
    """
    result = {}
    for path in tracked(root):
        relative = path.relative_to(root).as_posix()
        text = path.read_text()
        names = []
        if path.suffix == '.py':
            definitions = [n for n in ast.walk(ast.parse(text)) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
            for node in definitions:
                doc = ast.get_docstring(node)
                if not doc or ':example:' not in doc or ':returns:' not in doc:
                    raise ValueError(f'{relative}:{node.name}: missing native Python documentation (example/returns)')
                if node.returns is None or any(a.annotation is None for a in node.args.args if a.arg not in ('self', 'cls')):
                    raise ValueError(f'{relative}:{node.name}: missing parameter or return type')
                if relative != '.github/native_reference.py':
                    raise ValueError(f'{relative}:{node.name}: configure safe autodoc or a static Python extractor')
                names.append(node.name)
        elif path.suffix in BB_FORMATS:
            for name, comment, code in bitbake_units(path):
                names.append(name)
                for node in shell_nodes(code):
                    if node.name.word != name:
                        line = code[:node.pos[0]].count('\n') + 1
                        require_shell_docs(comment_before(code, line), f'{relative}:{node.name.word}')
                        raise ValueError(f'{relative}:{node.name.word}: configure nested BitBake shell reference rendering')
        elif path.suffix in ('.sh', '.bash') or text.startswith(('#!/bin/sh', '#!/bin/bash', '#!/usr/bin/env bash', '#!/usr/bin/env sh')):
            for node in shell_nodes(text):
                line = text[:node.pos[0]].count('\n') + 1
                require_shell_docs(comment_before(text, line), f'{relative}:{node.name.word}')
                names.append(node.name.word)
        elif relative.startswith('.github/workflows/') and path.suffix in ('.yml', '.yaml'):
            for label, code in workflow_units(path):
                for node in shell_nodes(code):
                    line = code[:node.pos[0]].count('\n') + 1
                    require_shell_docs(comment_before(code, line), f'{label}:{node.name.word}')
                    raise ValueError(f'{label}:{node.name.word}: configure embedded workflow function extraction')
        elif path.suffix in ('.yml', '.yaml'):
            document = yaml.safe_load(text)
            if isinstance(document, dict):
                for block, body in document.get('local_conf_header', {}).items():
                    # Parse embedded BitBake only after the YAML container is decoded.
                    with tempfile.TemporaryDirectory(prefix='native-kas-') as temporary:
                        metadata = Path(temporary) / path.with_suffix('.conf').name
                        metadata.write_text(str(body))
                        try:
                            units = bitbake_units(metadata)
                        except ValueError as error:
                            raise ValueError(f'{relative}:{block}: {error}') from error
                        if units:
                            raise ValueError(f'{relative}:{block}: configure embedded kas function extraction: {[unit[0] for unit in units]}')
        elif path.suffix in CODE_FORMATS:
            raise ValueError(f'{relative}: unsupported source format; configure its native extractor')
        if names:
            result[relative] = names
    return result


def generate(app: Sphinx) -> None:
    """Generate shdoc and safe Python autodoc pages before Sphinx reads sources.

    :param app: Active Sphinx application.
    :returns: None; writes ignored intermediate reference pages.
    :raises ValueError: Discovered definitions lack documentation or extraction.
    :example: Sphinx invokes ``generate(app)`` during ``builder-inited``.
    """
    entries = inventory(ROOT)
    destination = ROOT / 'docs/source/contributing/.generated'
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir()
    for relative, names in entries.items():
        path = ROOT / relative
        target = destination / (relative.replace('/', '-') + '.md')
        if path.suffix == '.py':
            target.write_text('# Documentation extension\n\n[Source](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/offline-guides-and-layer-map/.github/native_reference.py)\n\n```{eval-rst}\n.. automodule:: native_reference\n   :members:\n   :private-members:\n```\n')
            continue
        if path.suffix in BB_FORMATS:
            code = '\n\n'.join(comment + '\n' + source for _, comment, source in bitbake_units(path))
        else:
            code = path.read_text()
        # shdoc's @internal hides entries; coverage includes internal helpers.
        code = re.sub(r'^\s*#\s*@internal\s*$', '#', code, flags=re.M)
        rendered = subprocess.check_output(['gawk', '-f', str(ROOT / '.docs-tools/shdoc/shdoc')], input=code, text=True)
        for name in names:
            if f'## {name}' not in rendered:
                raise ValueError(f'{relative}:{name}: missing shdoc reference entry')
        title = "RUBIK Pi boot firmware" if path.suffix == ".bb" else path.name
        target.write_text(f'# {title}\n\n[Source](https://github.com/devdocsorg/meta-qcom-3rdparty/blob/docs/offline-guides-and-layer-map/{relative})\n\n' + rendered)


def check_rendered(root: Path) -> None:
    """Require real rendered native entries and correctly separated field sections.

    :param root: Checkout containing generated ``docs/site`` output.
    :returns: None when every discovered function has a rendered signature/heading.
    :raises ValueError: An entry or field is missing or annotations leaked as text.
    :example: ``check_rendered(ROOT)`` validates the current generated site.
    """
    for relative, names in inventory(root).items():
        page = root / 'docs/site/contributing/.generated' / (relative.replace('/', '-') + '.html')
        if not page.exists():
            raise ValueError(f'{relative}: missing rendered reference page')
        html = page.read_text()
        for name in names:
            anchor = f'native_reference.{name}' if relative.endswith('.py') else name.lstrip('_').replace('_', '-')
            if f'id="{anchor}"' not in html:
                raise ValueError(f'{relative}:{name}: missing rendered reference entry')
        if not relative.endswith('.py'):
            for heading in ('Example', 'Exit codes'):
                if f'>{heading}<' not in html:
                    raise ValueError(f'{relative}: missing rendered {heading} section')
            if re.search(r'@(arg|exitcode|description|noargs)\b', html):
                raise ValueError(f'{relative}: native annotations leaked into rendered reference')


def setup(app: Sphinx) -> dict[str, bool]:
    """Register native extraction with Sphinx.

    :param app: Sphinx application loading this extension.
    :returns: Parallel-safety metadata; generation runs serially.
    :example: Add ``native_reference`` to Sphinx's ``extensions`` list.
    """
    app.connect('builder-inited', generate)
    return {'parallel_read_safe': False, 'parallel_write_safe': False}
