# Prepare a layer build with kas

This tutorial prepares the Dragon Q6A configuration, checks its metadata, and
shows where the resulting OS image is produced.

## Prerequisites

- A Linux build host with Git and a working Docker or Podman runtime.
- [kas-container](https://kas.readthedocs.io/en/latest/userguide/getting-started.html)
  on PATH, or an absolute executable path in `KAS_CONTAINER`.
- A checkout of this layer, network access, and writable work/cache directories.

## 1. Set up the workspace

From the layer checkout, load the optional host-path examples:

```sh
set -a
. ./.env.example
set +a
mkdir -p "$KAS_WORK_DIR" "$DL_DIR" "$SSTATE_DIR"
```

Existing environment values are retained. Keep these directories outside the
checkout. See [configuration](../user/configuration.md) for types and defaults.

## 2. Select and inspect the machine

```sh
"$KAS_CONTAINER" dump ci/radxa-dragon-q6a.yml
```

The merged YAML names `radxa-dragon-q6a`, the `nodistro` distro, and the
`core-image-base` target. It includes this layer, `meta-qcom`, OpenEmbedded Core,
and BitBake. Select release-compatible revisions when preparing a release build;
the development configuration follows the revisions selected by `meta-qcom`.

## 3. Check the layer configuration

```sh
"$KAS_CONTAINER" shell ci/radxa-dragon-q6a.yml --command 'bitbake-layers show-layers'
"$KAS_CONTAINER" shell ci/radxa-dragon-q6a.yml --command 'bitbake -p'
```

Expect the collections `core`, `qcom`, and `qcom-3rdparty` in the layer list.
A successful parse reports the recipe count and exits with status 0. An
incompatible-layer error means the selected revisions do not share a compatible
Yocto release. Parsing does not compile an image or test a board.

## 4. Build the image

```sh
"$KAS_CONTAINER" build ci/radxa-dragon-q6a.yml
```

A successful build produces `core-image-base` output under BitBake's `TMPDIR`,
in `deploy/images/radxa-dragon-q6a/`. This machine selects `wic`, `wic.gz`, and
`wic.bmap` disk-image formats. Compilation requires more disk space, downloads,
and time than the metadata checks above.

To use the Qualcomm distro, compose
`ci/radxa-dragon-q6a.yml:ci/qcom-distro.yml` and inspect its merged target before
building. The resulting OS image does not replace Dragon Q6A SPI boot firmware.
