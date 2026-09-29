# Documentation

Build the site from the repository root, then open `docs/site/index.html`
directly in a browser; no HTTP server is needed:

```sh
make -f docs/source/Makefile setup html
```

The site is generated and not committed. Edit the [source](source/README.md) and
follow the [development environment walkthrough](source/contributing/DEVELOPMENT.md)
to check it.

The build writes `site/THIRD_PARTY_LICENSES.txt`, which preserves the licences
of the locked documentation packages, and attaches the upstream notices to the
JavaScript it redistributes.

## Folders

- [source/](source/README.md) — Contains the authoritative guides and the documentation build configuration.

## Files

- [README.md](README.md) — Explains how to build and open the site, and holds the documentation tooling's licence notices.

## Documentation tooling licence

The documentation helpers `.github/check_offline.py`, `.github/finalise_site.py`,
and `.github/test_reference_coverage.py`, the documentation workflow, the build
files in `docs/source/`, the issue and pull request templates, and parts of the
new guides adapt the [QLI 2.0 repository skeleton](https://github.com/devdocsorg/qli2-example-repo).
The following notices apply to that material; the layer itself remains under
the [MIT licence](../LICENSE).

```text
BSD 3-Clause License

Copyright (c) 2026, DevDocs

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```

The skeleton's issue and pull request templates adapt the
[Qualcomm Linux pkg-fastrpc templates](https://github.com/qualcomm-linux/pkg-fastrpc/tree/9b1a916be3d29fa184feb16995a4db403d91aa59/.github),
under this notice:

```text
Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:
* Redistributions of source code must retain the above copyright
  notice, this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above
  copyright notice, this list of conditions and the following
  disclaimer in the documentation and/or other materials provided
  with the distribution.
* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived
  from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED "AS IS" AND ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT
ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS
BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```
