# Copyright (c) 2026 DevDocs
# SPDX-License-Identifier: BSD-3-Clause
"""Check rendered coverage and prove missing comments and entries are rejected."""
import tempfile
from pathlib import Path
import native_reference as reference

reference.check_rendered(reference.ROOT)
try:
    reference.require_shell_docs('', 'regression:missing-comment')
except ValueError:
    pass
else:
    raise AssertionError('Missing comments passed')

# Preserve the actual file while checking that the coverage validator rejects loss.
page = reference.ROOT / 'docs/site/contributing/.generated/ci-yocto-check-layer.sh.html'
original = page.read_text()
try:
    page.write_text(original.replace('id="is-dir"', 'id="removed-entry"'))
    try:
        reference.check_rendered(reference.ROOT)
    except ValueError as error:
        assert 'missing rendered reference entry' in str(error), error
    else:
        raise AssertionError('Missing rendered entry passed')
finally:
    page.write_text(original)
print('Native comments, discovered functions, and rendered entries agree; negative checks passed.')
