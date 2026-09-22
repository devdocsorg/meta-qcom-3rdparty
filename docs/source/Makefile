# Run from the repository root: make -f docs/source/Makefile <target>.
# setup installs only the pinned documentation toolchain in the local .venv.
# html removes stale generated pages and builds the complete site strictly.
# check verifies output is committed and direct-file search avoids fetch().
.PHONY: setup html check browser

# Immutable shdoc source revision; gawk is its runtime.
SHDOC_REV = 52917b2f3471fe77c745ede115494d2d5c9168d1

setup:
	command -v gawk
	uv venv --python 3.12.13 --clear .venv
	uv pip install --python .venv/bin/python -r docs/source/requirements.lock

	mkdir -p .tools
	test -d .tools/shdoc/.git || git clone https://github.com/reconquest/shdoc.git .tools/shdoc
	git -C .tools/shdoc checkout --detach $(SHDOC_REV)

html:
	rm -rf docs/site
	.venv/bin/sphinx-build -W --keep-going -E -a -b html -d docs/.doctrees docs/source docs/site
	.venv/bin/python .github/finalise_site.py

# Install a user-local browser only when system Chromium is unavailable.
browser:
	.venv/bin/playwright install chromium

check: html
	.venv/bin/python .github/test_reference_coverage.py
	.venv/bin/python .github/check_offline.py docs/site firmware
	test -f docs/site/index.html
	grep -q 'SHOW_SEARCH_SUMMARY: false' docs/site/_static/documentation_options.js
	git diff --exit-code -- docs/site
	test -z "$$(git ls-files --others --exclude-standard docs/site)"
