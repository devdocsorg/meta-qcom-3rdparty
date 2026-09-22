"""Check reference coverage and regressions without executing build tasks.

Run after Sphinx. Mutations live only in a temporary clone and copied site.
"""
from pathlib import Path
import shutil
import subprocess
import tempfile

from reference import check_rendered, inventory

if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1]
    print(check_rendered(root, root / 'docs/site'))
    with tempfile.TemporaryDirectory(prefix='reference-coverage-') as directory:
        clone = Path(directory) / 'repo'
        subprocess.run(['git', 'clone', '--quiet', '--no-hardlinks', str(root), str(clone)], check=True)
        candidate = subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True).strip()
        tested = subprocess.check_output(['git', '-C', str(clone), 'rev-parse', 'HEAD'], text=True).strip()
        assert tested == candidate, (tested, candidate)
        print(f'Regression clone revision: {tested}')
        inventory(clone)
        product = clone / 'ci/yocto-buildstats.sh'
        original = product.read_text()
        mutations = [
            original.replace('@description', 'description'),
            original + '\nnew_helper() { :; }\n',
        ]
        for mutant in mutations:
            product.write_text(mutant)
            try:
                inventory(clone)
            except ValueError:
                pass
            else:
                raise AssertionError('Missing shell documentation was accepted')
        product.write_text(original)
        recipe = clone / 'recipes-bsp/unsupported.bb'
        recipe.write_text('python do_new_task() {\n    pass\n}\n')
        try:
            inventory(clone)
        except ValueError as error:
            assert 'embedded Python' in str(error), error
        else:
            raise AssertionError('Unsupported embedded Python was silently omitted')
        recipe.unlink()
        source = clone / '.github/reference.py'
        source.write_text(source.read_text().replace(':returns:', 'returns:'))
        try:
            inventory(clone)
        except ValueError:
            pass
        else:
            raise AssertionError('Missing Python documentation was accepted')
        site = Path(directory) / 'site'
        shutil.copytree(root / 'docs/site', site)
        for page, anchor in [
            ('contributing/.generated/ci-yocto-buildstats.sh.html', 'is-dir'),
            ('contributing/.generated/python-reference.html', 'reference.inventory'),
        ]:
            path = site / page
            text = path.read_text()
            path.write_text(text.replace(f'id="{anchor}"', 'id="removed-entry"'))
            try:
                check_rendered(root, site)
            except ValueError:
                pass
            else:
                raise AssertionError(f'Missing rendered entry was accepted: {anchor}')
            path.write_text(text)
    print('Reference coverage and missing-comment, missing-entry, new-function, and unsupported-language regressions passed.')
