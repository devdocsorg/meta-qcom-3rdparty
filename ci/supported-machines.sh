#!/bin/sh -e
# Copyright (c) 2026 Qualcomm Innovation Center, Inc. All rights reserved.
# SPDX-License-Identifier: MIT

# Writes docs/supported-machines.md from the #@TYPE, #@NAME and #@DESCRIPTION
# headers of every conf/machine/*.conf.

# Fix the collation, so the row order does not depend on the caller's locale.
LC_ALL=C
export LC_ALL

# Work from the repository root whatever the caller's working directory is.
cd "$(dirname "$0")/.."

PAGE="docs/supported-machines.md"

fail() {
    printf '%s\n' "ci/supported-machines.sh: $1: $2" >&2
    exit 1
}

# The value after "#@<key>:" on the first line starting with that prefix,
# whitespace trimmed. Empty when the file has no such line.
header() {
    awk -v prefix="#@$1:" '
        index($0, prefix) == 1 {
            value = substr($0, length(prefix) + 1)
            sub(/^[ \t]+/, "", value)
            sub(/[ \t]+$/, "", value)
            print value
            exit
        }
    ' "$2"
}

# A pipe in a value would end the table cell.
escape() {
    printf '%s' "$1" | sed 's/|/\\|/g'
}

TMP="$(mktemp)"
trap 'rm -f "$TMP"' EXIT

printf '%s\n' \
    "# Supported Machines" \
    "" \
    'The machines this layer configures, one per `conf/machine/<machine>.conf`. Machine is the `MACHINE` value and the name of the kas fragment under `ci/`; Name and Description are the `#@NAME` and `#@DESCRIPTION` headers of that file. `ci/supported-machines.sh` writes this table from the headers and CI checks that they match, so a change starts in the machine file.' \
    "" \
    "| Machine | Name | Description |" \
    "| --- | --- | --- |" > "$TMP"

# Pathname expansion sorts on the collation set above, so the rows follow the
# byte order of the file names.
for conf in conf/machine/*.conf; do
    type="$(header TYPE "$conf")"
    name="$(header NAME "$conf")"
    description="$(header DESCRIPTION "$conf")"

    [ -n "$type" ] || fail "$conf" "missing #@TYPE"
    [ "$type" = "Machine" ] || fail "$conf" "#@TYPE is not Machine"
    [ -n "$name" ] || fail "$conf" "missing #@NAME"
    [ -n "$description" ] || fail "$conf" "missing #@DESCRIPTION"

    machine="${conf##*/}"
    machine="${machine%.conf}"

    printf '| `%s` | %s | %s |\n' \
        "$machine" "$(escape "$name")" "$(escape "$description")" >> "$TMP"
done

printf '%s\n' "" "**SPDX-License-Identifier:** MIT" >> "$TMP"

# mktemp creates the file private; the page is a repository file.
chmod 644 "$TMP"
mv "$TMP" "$PAGE"
