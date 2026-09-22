# Copyright (c) 2026 DevDocs
# SPDX-License-Identifier: MIT
"""Prove that missing native reference coverage fails in isolated source copies.

Run from the repository root after installing the documentation toolchain.
The tests alter only temporary copies and never execute recipes or shell tasks.
"""
from pathlib import Path
import shutil
import subprocess
import tempfile

root = Path.cwd()
cases = (
    ('ci/yocto-patchreview.sh', '\nundocumented_helper() {\n    :\n}\n',
     'undocumented_helper'),
    ('recipes-bsp/firmware-boot/firmware-qcom-boot-rubikpi3_20260621.bb',
     '\npython do_example() {\n    pass\n}\n', 'Configure BitBake Python extraction'),
)
for source, addition, expected in cases:
    with tempfile.TemporaryDirectory(prefix='reference-coverage-') as temp:
        copied = Path(temp) / 'repo'
        shutil.copytree(root, copied, ignore=shutil.ignore_patterns(
            '.git', '.venv', 'site', '.doctrees', '.generated', '__pycache__'))
        target = copied / source
        target.write_text(target.read_text() + addition)
        result = subprocess.run(
            [str(root / '.venv/bin/sphinx-build'), '-W', '-E', '-b', 'html',
             str(copied / 'docs/source'), str(copied / 'site')],
            capture_output=True, text=True,
        )
        assert result.returncode != 0 and expected in result.stderr, result.stdout + result.stderr
        print(f'Coverage failure verified: {expected}')
