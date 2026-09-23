#!/bin/sh
# Copyright (c) 2026 DevDocs
# SPDX-License-Identifier: BSD-3-Clause
# Run from the repository root; installs only ignored documentation tools.
set -eu

# Required fixed versions/digests; update only after checking upstream releases.
GAWK_VERSION=5.4.1
GAWK_SHA256=07f6f7342b7febe4313fc2c2542ad93d64fe20ad8717200109f105a826f5fd37
SHDOC_REV=b3436134f08428f8bbe2e54bc4dc20da85cd300b
SHDOC_SHA256=856bdc62db15e4970c59f011e9a779d6a23e86f4f123707e25f5390d14c9b191
TOOLS="$(pwd)/docs/.tools"
mkdir -p "$TOOLS/bin"

# Reuse the exact installed runtime when available; otherwise build it locally.
if command -v gawk >/dev/null && gawk --version | head -n 1 | grep -q "GNU Awk $GAWK_VERSION,"; then
    ln -sf "$(command -v gawk)" "$TOOLS/bin/gawk"
elif ! "$TOOLS/bin/gawk" --version 2>/dev/null | head -n 1 | grep -q "GNU Awk $GAWK_VERSION,"; then
    curl --fail --location "https://ftp.gnu.org/gnu/gawk/gawk-$GAWK_VERSION.tar.xz" -o "$TOOLS/gawk.tar.xz"
    printf '%s  %s\n' "$GAWK_SHA256" "$TOOLS/gawk.tar.xz" | sha256sum --check
    tar -xf "$TOOLS/gawk.tar.xz" -C "$TOOLS"
    (
        cd "$TOOLS/gawk-$GAWK_VERSION"
        ./configure --prefix="$TOOLS" --without-mpfr --disable-nls
        make
        make install
    )
fi
curl --fail --location "https://raw.githubusercontent.com/reconquest/shdoc/$SHDOC_REV/shdoc" -o "$TOOLS/shdoc"
printf '%s  %s\n' "$SHDOC_SHA256" "$TOOLS/shdoc" | sha256sum --check
