# Copyright (c) 2026 DevDocs
# SPDX-License-Identifier: BSD-3-Clause
"""Check native coverage and prove missing or unsupported definitions fail."""
from pathlib import Path
import shutil
import tempfile

from native_reference import inventory, verify

root = Path.cwd()
verify(root)
with tempfile.TemporaryDirectory(prefix='reference-regressions-') as temporary:
    candidate = Path(temporary)
    shutil.copytree(root / 'ci', candidate / 'ci')
    shutil.copytree(root / 'recipes-bsp', candidate / 'recipes-bsp')
    shutil.copytree(root / 'docs/site', candidate / 'docs/site')
    source = candidate / 'ci/yocto-check-layer.sh'
    original = source.read_text()
    source.write_text(original.replace('@description', 'description'))
    try:
        inventory(candidate)
    except ValueError as error:
        assert 'missing shdoc' in str(error), error
    else:
        raise AssertionError('Missing function comment was accepted')
    source.write_text(original)
    page = candidate / 'docs/site/contributing/.generated/ci-yocto-check-layer.sh.html'
    saved = page.read_text()
    page.write_text(saved.replace('id="is-dir"', 'id="removed-entry"'))
    try:
        verify(candidate)
    except ValueError as error:
        assert 'missing rendered reference' in str(error), error
    else:
        raise AssertionError('Missing function reference was accepted')
    page.write_text(saved)
    source = candidate / 'recipes-bsp/new.bb'
    source.write_text('python do_new() {\n    pass\n}\n')
    try:
        inventory(candidate)
    except ValueError as error:
        assert 'embedded Python' in str(error), error
    else:
        raise AssertionError('Unsupported embedded definition was accepted')
print('Missing comments, missing entries, and unsupported-definition regressions passed')
