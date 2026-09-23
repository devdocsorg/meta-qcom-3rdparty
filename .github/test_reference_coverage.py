# Copyright (c) 2026 DevDocs
# SPDX-License-Identifier: BSD-3-Clause
"""Prove missing comments, rendered entries, and unsupported definitions fail."""
from pathlib import Path
import shutil
import subprocess
import tempfile

import native_reference as reference

with tempfile.TemporaryDirectory(prefix='reference-regression-') as directory:
    root = Path(directory)
    subprocess.run(['git', 'init', '-q', directory], check=True)
    for path in reference.sources(reference.ROOT):
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(reference.ROOT / path, target)
    shutil.copytree(reference.ROOT / 'docs/site', root / 'docs/site')
    reference.check(root)
    source = root / 'ci/yocto-patchreview.sh'
    original = source.read_text()
    source.write_text(original.replace('@description', 'description'))
    try:
        reference.inventory(root)
    except ValueError as error:
        assert 'missing @description' in str(error), error
    else:
        raise AssertionError('Missing shell comments were accepted')
    source.write_text(original)
    page = root / 'docs/site/contributing/.generated/ci-yocto-patchreview.sh.html'
    original_html = page.read_text()
    page.write_text(original_html.replace('id="is-dir"', 'id="removed"').replace('id="is_dir"', 'id="removed"'))
    try:
        reference.check(root)
    except AssertionError as error:
        assert 'missing rendered entry' in str(error), error
    else:
        raise AssertionError('Missing rendered entry was accepted')
    page.write_text(original_html)
    fixture = root / 'recipes-bsp/fixture.bb'
    fixture.write_text('python do_new_task() {\n    pass\n}\n')
    try:
        reference.inventory(root)
    except ValueError as error:
        assert 'embedded Python' in str(error), error
    else:
        raise AssertionError('Unsupported embedded definition was accepted')
    fixture.unlink()
    # A new shell function must be found independently of current entry count.
    source.write_text(original + '\nnew_helper() { true; }\n')
    try:
        reference.inventory(root)
    except ValueError as error:
        assert 'new_helper' in str(error), error
    else:
        raise AssertionError('New undocumented function was accepted')
print('Reference regressions: missing comments, entries, and unsupported/new functions rejected')
