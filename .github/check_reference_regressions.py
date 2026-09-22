# SPDX-License-Identifier: MIT
"""Exercise native coverage failures without executing any maintained build function."""
from pathlib import Path
import subprocess
import sys

from doc_reference import ROOT

source = ROOT / 'ci/yocto-patchreview.sh'
html = ROOT / 'docs/site/contributing/.generated/ci--yocto-patchreview-sh.html'
original_source = source.read_text()
original_html = html.read_text()
probe = ROOT / '.github/reference-probe.sh'
python_probe = ROOT / '.github/reference-probe.bbappend'
workflow_probe = ROOT / '.github/reference-probe.yml'
unsupported = ROOT / '.github/reference-probe.rs'
assert not any(path.exists() for path in (probe, python_probe, workflow_probe, unsupported))

cases = [
    (source, original_source.replace('# @description Validate', '# Validate'), 'generate', 'missing native comment'),
    (html, original_html.replace('id="is-dir"', 'id="removed-entry"'), 'check', 'missing native HTML reference'),
    (probe, 'undocumented() { :; }\n', 'generate', 'missing native comment'),
    (probe, "python3 -c 'def hidden(): pass'\n", 'generate', 'Inline Python definition'),
    (python_probe, 'python new_task() {\n    pass\n}\n', 'generate', 'embedded Python definition'),
    (workflow_probe, 'jobs:\n  check:\n    steps:\n      - run: |\n          helper() { :; }\n', 'generate', 'workflow shell definition'),
    (unsupported, 'fn new_function() {}\n', 'generate', 'unknown source format'),
]
try:
    for path, replacement, mode, diagnostic in cases:
        prior = path.read_text() if path.exists() else None
        try:
            path.write_text(replacement)
            result = subprocess.run([sys.executable, str(ROOT / '.github/doc_reference.py'), mode],
                                    cwd=ROOT, capture_output=True, text=True)
            assert result.returncode != 0, f'{path}: expected coverage failure'
            assert diagnostic in result.stderr, (diagnostic, result.stderr)
            print(f'Regression rejected: {diagnostic}')
        finally:
            if prior is None:
                path.unlink()
            else:
                path.write_text(prior)
    # A newly documented function must appear without editing an inventory/count.
    probe.write_text('''# @description Demonstrate automatic discovery of an added shell function.
# @noargs
# @example
#   new_documented_function
# @exitcode 0 The no-op completes with no output.
new_documented_function() { :; }
''')
    subprocess.run([sys.executable, str(ROOT / '.github/doc_reference.py'), 'generate'], cwd=ROOT, check=True)
    generated = ROOT / 'docs/source/contributing/.generated/-github--reference-probe-sh.md'
    assert '### new_documented_function' in generated.read_text()
    print('Regression accepted: new documented function discovered without a count change')
finally:
    source.write_text(original_source)
    html.write_text(original_html)
    for path in (probe, python_probe, workflow_probe, unsupported):
        path.unlink(missing_ok=True)
    subprocess.run([sys.executable, str(ROOT / '.github/doc_reference.py'), 'generate'], cwd=ROOT, check=True)
