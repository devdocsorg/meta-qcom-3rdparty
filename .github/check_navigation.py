# SPDX-License-Identifier: MIT
"""Check maintained-folder inventories and local Markdown destinations without networking."""
from pathlib import Path
from urllib.parse import unquote, urlsplit
import re

from markdown_it import MarkdownIt
from doc_reference import ROOT, source_files

files = source_files(ROOT)
folders = {ROOT}
for path in files:
    if any(part.startswith('.') for part in path.relative_to(ROOT).parts[:-1]):
        continue
    folders.update(parent for parent in path.parents if parent == ROOT or ROOT in parent.parents)
for folder in sorted(folders):
    readme = folder / 'README.md'
    assert readme.is_file(), f'Missing maintained-folder README: {folder}'
    text = readme.read_text()
    expected = {path.relative_to(folder).parts[0] for path in files if folder in path.parents}
    if folder == ROOT / 'docs':
        expected.add('site')
    indexed = set(re.findall(r'^- \[([^\]]+)\]\([^)]+\) — .+', text, re.M))
    assert expected <= indexed, f'{readme}: missing index items {expected - indexed}'
    assert indexed <= expected, f'{readme}: stale index items {indexed - expected}'

parser = MarkdownIt()
for path in files:
    if path.suffix != '.md':
        continue
    for token in parser.parse(path.read_text()):
        for child in token.children or []:
            if child.type not in {'link_open', 'image'}:
                continue
            link = child.attrGet('href') or child.attrGet('src')
            parsed = urlsplit(link)
            if parsed.scheme or parsed.netloc:
                continue
            target = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
            assert target.exists(), f'{path}: missing local link {link}'
            # Sphinx validates documentation heading references; the browser checks final IDs.
            if path.is_relative_to(ROOT / 'docs/source'):
                assert target != ROOT / 'README.md', f'{path}: Sphinx must not read the root map'
print(f'Navigation: {len(folders)} maintained folders; local Markdown destinations exist')
