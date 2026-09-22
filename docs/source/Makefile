# Run from the repository root: make -f docs/source/Makefile TARGET.
# Optional path string; defaults to .venv/bin/python. Example: PYTHON=.venv/bin/python.
PYTHON ?= .venv/bin/python
# Required immutable extractor revisions; change only with validation and a rebuild.
SHDOC_REV := 52917b2f3471fe77c745ede115494d2d5c9168d1
BITBAKE_REV := 18cca50ba3da5ce27bc674478957bb08e7536b9a

.PHONY: setup html check browser references
setup:
	uv venv --python 3.12 --clear .venv
	uv pip install --python $(PYTHON) -r docs/source/requirements.lock
	mkdir -p .doc-tools/shdoc .doc-tools/bitbake
	git -C .doc-tools/shdoc init -q
	git -C .doc-tools/shdoc fetch -q --depth=1 https://github.com/reconquest/shdoc.git $(SHDOC_REV)
	git -C .doc-tools/shdoc checkout -q --detach FETCH_HEAD
	git -C .doc-tools/bitbake init -q
	git -C .doc-tools/bitbake fetch -q --depth=1 https://github.com/openembedded/bitbake.git $(BITBAKE_REV)
	git -C .doc-tools/bitbake checkout -q --detach FETCH_HEAD
	command -v gawk

references:
	test "$$(git -C .doc-tools/shdoc rev-parse HEAD)" = "$(SHDOC_REV)"
	test "$$(git -C .doc-tools/bitbake rev-parse HEAD)" = "$(BITBAKE_REV)"
	$(PYTHON) .github/doc_reference.py generate

html: references
	rm -rf docs/site
	.venv/bin/sphinx-build -W --keep-going -E -a -b html -d docs/.doctrees docs/source docs/site
	$(PYTHON) .github/finalise_site.py
	$(PYTHON) .github/doc_reference.py check

browser:
	.venv/bin/playwright install chromium

check: html
	$(PYTHON) .github/check_reference_regressions.py
	$(PYTHON) .github/check_navigation.py
	$(PYTHON) .github/check_offline.py docs/site firmware
	git diff --exit-code -- docs/site
	test -z "$$(git ls-files --others --exclude-standard docs/site)"
