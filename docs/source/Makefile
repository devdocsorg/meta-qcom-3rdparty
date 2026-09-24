# Run from the repository root: make -f docs/source/Makefile <target>.
# setup installs only the pinned documentation toolchain in the local .venv:
# the locked Python packages, BitBake's statement parser, and shdoc.
# html removes stale generated pages, builds the complete site strictly, and
# fails unless every function has a documented, rendered reference entry.
# check verifies output is committed and direct-file search avoids fetch().
.PHONY: setup html check browser

# BitBake yocto-6.0.3 (wrynose): conf.py reads recipes with its parser only.
BITBAKE_REVISION = fae9db3168dbff1b8c76fe9c6726a9687ff97514
# shdoc v1.4 renders shell documentation comments as Markdown.
SHDOC_REVISION = b3436134f08428f8bbe2e54bc4dc20da85cd300b
SHDOC_SHA256 = 856bdc62db15e4970c59f011e9a779d6a23e86f4f123707e25f5390d14c9b191

setup:
	uv venv --python 3.12 --clear .venv
	uv pip install --python .venv/bin/python -r docs/source/requirements.lock
	git init -q .venv/bitbake
	git -C .venv/bitbake fetch -q --depth 1 https://github.com/openembedded/bitbake $(BITBAKE_REVISION)
	git -C .venv/bitbake -c advice.detachedHead=false checkout -q FETCH_HEAD
	curl -sSfL -o .venv/bin/shdoc https://raw.githubusercontent.com/reconquest/shdoc/$(SHDOC_REVISION)/shdoc
	echo "$(SHDOC_SHA256)  .venv/bin/shdoc" | sha256sum -c --quiet
	chmod +x .venv/bin/shdoc

html:
	rm -rf docs/site docs/source/contributing/.generated
	.venv/bin/sphinx-build -W --keep-going -E -a -b html -d docs/.doctrees docs/source docs/site
	.venv/bin/python .github/finalise_site.py
	.venv/bin/python .github/test_reference_coverage.py check

# Install a user-local browser only when system Chromium is unavailable.
browser:
	.venv/bin/playwright install chromium

check: html
	.venv/bin/python .github/check_offline.py docs/site kas
	test -f docs/site/index.html
	grep -q 'SHOW_SEARCH_SUMMARY: false' docs/site/_static/documentation_options.js
	git diff --exit-code -- docs/site
	test -z "$$(git ls-files --others --exclude-standard docs/site)"
