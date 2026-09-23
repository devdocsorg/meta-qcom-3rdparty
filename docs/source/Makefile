# Run from the repository root: make -f docs/source/Makefile <target>.
# setup installs the pinned documentation toolchain in the local .venv: the
# locked Python packages, shdoc, and BitBake, whose parser reads the metadata.
# html removes stale output, builds the site strictly, and checks that every
# function has a documentation comment and a rendered reference entry.
# check also opens a copied site offline and rejects uncommitted output.
.PHONY: setup html check browser

# shdoc 1.4 renders shell documentation comments (commit and script SHA-256).
SHDOC_COMMIT = b3436134f08428f8bbe2e54bc4dc20da85cd300b
SHDOC_SHA256 = 856bdc62db15e4970c59f011e9a779d6a23e86f4f123707e25f5390d14c9b191
# BitBake tag yocto-6.0.3, from the wrynose series named by conf/layer.conf.
BITBAKE_COMMIT = fae9db3168dbff1b8c76fe9c6726a9687ff97514

setup:
	uv venv --python 3.12 --clear .venv
	uv pip install --python .venv/bin/python -r docs/source/requirements.lock
	curl -fsSL -o .venv/bin/shdoc https://raw.githubusercontent.com/reconquest/shdoc/$(SHDOC_COMMIT)/shdoc
	echo "$(SHDOC_SHA256)  .venv/bin/shdoc" | sha256sum -c -
	chmod +x .venv/bin/shdoc
	git init --quiet .venv/bitbake
	git -C .venv/bitbake fetch --quiet --depth 1 https://github.com/openembedded/bitbake.git $(BITBAKE_COMMIT)
	git -C .venv/bitbake -c advice.detachedHead=false checkout --quiet FETCH_HEAD

html:
	rm -rf docs/site
	.venv/bin/sphinx-build -W --keep-going -E -a -b html -d docs/.doctrees docs/source docs/site
	.venv/bin/python .github/finalise_site.py
	.venv/bin/python .github/test_reference_coverage.py docs/site

# Install a user-local browser only when system Chromium is unavailable.
browser:
	.venv/bin/playwright install chromium

check: html
	.venv/bin/python .github/check_offline.py docs/site rubikpi3
	test -f docs/site/index.html
	grep -q 'SHOW_SEARCH_SUMMARY: false' docs/site/_static/documentation_options.js
	git diff --exit-code -- docs/site
	test -z "$$(git ls-files --others --exclude-standard docs/site)"
