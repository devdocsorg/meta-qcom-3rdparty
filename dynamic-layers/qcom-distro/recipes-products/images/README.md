<!-- Generated from dynamic-layers/qcom-distro/recipes-products/images/ at wrynose @ e804c5eb (2026-09-08) by docsgen on 2026-09-08. Manual edits will be overwritten on regeneration; change the source, not this page. -->

# dynamic-layers/qcom-distro/recipes-products/images/

A [bbappend](../../../../docs/glossary.md) extends a recipe another layer provides ([appending layer metadata](https://docs.yoctoproject.org/dev-manual/layers.html#appending-other-layers-metadata-with-your-layer)). This folder holds one for the Arduino UNO Q, parsed when the `qcom-distro` collection is in the build. Used by the `qcom-multimedia-image` recipe in meta-qcom-distro.

## Contents

| File | Description | Machine | Reference |
| --- | --- | --- | --- |
| [dynamic-layers/qcom-distro/recipes-products/images/qcom-multimedia-image.bbappend](qcom-multimedia-image.bbappend) | Modifies the `qcom-multimedia-image` recipe, which is provided outside this layer. Parsed only when the matching layer collection is present. | [`uno-q`](../../../../conf/machine/uno-q.md) | [qcom-multimedia-image bbappend](qcom-multimedia-image-bbappend.md) |

## Description

`dynamic-layers` is BitBake's mechanism for conditional cross-layer recipe integration. A layer exposes its recipes through `BBFILES`; `BBFILES_DYNAMIC` registers a further set of recipe and bbappend globs tagged with a named layer collection, and the parser includes that content when a layer providing the collection is present. This is deliberately weaker than `LAYERDEPENDS`, which is a hard requirement enforced on every build: a `BBFILES_DYNAMIC` entry whose gating collection is absent is skipped silently, which lets a layer ship integration content aimed at another layer while leaving that layer optional.

The path convention nests the conditional content under `dynamic-layers/<collection-name>/`, mirroring the layer's own `recipes-*` structure beneath that namespace. `qcom-distro` is the only such namespace in this repository, and `recipes-products/images/` occupies the same relative position an ordinary image-recipe directory would. It holds one bbappend targeting `qcom-multimedia-image`, which is not defined in this layer; another layer in the build provides both that recipe and the `qcom-distro` collection. [conf/layer.conf](../../../../conf/layer.conf) names `core` and `qcom` alone in `LAYERDEPENDS_qcom-3rdparty`, which is exactly why this content is gated rather than made a hard dependency.

When the gating collection is present, BitBake parses the bbappend and appends to `INCOMPATIBLE_LICENSE_EXCEPTIONS`, scoped to the `uno-q` machine override, the recipe and license pair covering this layer's boot firmware recipe. That exempts the firmware recipe's license from the active distro's incompatible-license filter for `uno-q` builds of the image, letting the image pull in the board's boot-firmware package where distro policy would otherwise exclude it.
