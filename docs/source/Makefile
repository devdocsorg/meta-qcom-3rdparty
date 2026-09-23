# Run from the repository root: make -f docs/source/Makefile <target>.
# setup installs only the pinned documentation toolchain in the local .venv.
# html removes stale generated pages and builds the complete site strictly.
# check verifies output is committed and direct-file search avoids fetch().
.PHONY: setup html check browser

setup:
	sh .github/setup_tools.sh
	uv venv --python 3.12.13 --clear .venv
	uv pip install --python .venv/bin/python -r docs/source/requirements.lock

html:
	rm -rf docs/site
	.venv/bin/sphinx-build -W --keep-going -E -a -b html -d docs/.doctrees docs/source docs/site
	.venv/bin/python .github/finalise_site.py

# Install a user-local browser only when system Chromium is unavailable.
browser:
	.venv/bin/playwright install chromium

check: html
	.venv/bin/python .github/native_reference.py
	.venv/bin/python .github/test_reference_coverage.py
	.venv/bin/python .github/check_offline.py docs/site firmware
	test -f docs/site/index.html
	grep -q 'SHOW_SEARCH_SUMMARY: false' docs/site/_static/documentation_options.js
	git diff --exit-code -- docs/site
	test -z "$$(git ls-files --others --exclude-standard docs/site)"
