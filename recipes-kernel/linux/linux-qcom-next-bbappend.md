<!-- Generated from recipes-kernel/linux/linux-qcom-next_git.bbappend at wrynose @ e804c5eb (2026-09-08) by docsgen on 2026-09-08. Manual edits will be overwritten on regeneration; change the source, not this page. -->

# linux-qcom-next

Modifies the `linux-qcom-next` recipe. That recipe is not defined in this layer; another layer in the build provides it, and this repository pins no revision of it. This layer declares `LAYERDEPENDS_qcom-3rdparty = "core qcom"` in [conf/layer.conf](../../conf/layer.conf). Used by the [`linux-qcom-next`](https://github.com/qualcomm-linux/meta-qcom/blob/wrynose/recipes-kernel/linux/linux-qcom-next_git.bb) recipe in meta-qcom, which this file extends.

A bbappend extends a recipe that lives in another layer, adding settings and files to it while the recipe itself stays where it is ([bbappend](../../docs/glossary.md), [appending to another layer's metadata](https://docs.yoctoproject.org/dev-manual/layers.html#appending-other-layers-metadata-with-your-layer)). This one adds a Realtek Ethernet configuration fragment to the Radxa Dragon Q6A's kernel build.

Bbappend file: [recipes-kernel/linux/linux-qcom-next_git.bbappend](linux-qcom-next_git.bbappend).

## Configuration variables

| Variable | Effect |
| --- | --- |
| [`FILESEXTRAPATHS:prepend:radxa-dragon-q6a`](https://docs.yoctoproject.org/ref-manual/variables.html#term-FILESEXTRAPATHS) `:=` | Extends the search path used to resolve `file://` entries in `SRC_URI`. This file adds `${THISDIR}/radxa-dragon-q6a:`. Prepended to the value inherited from the target recipe. |
| [`SRC_URI:append:radxa-dragon-q6a`](https://docs.yoctoproject.org/ref-manual/variables.html#term-SRC_URI) `=` | Source locations the recipe fetches and unpacks. Appended to the value inherited from the target recipe. |

Override scopes:

- `FILESEXTRAPATHS:prepend:radxa-dragon-q6a`: `prepend`, machine scope [`radxa-dragon-q6a`](../../conf/machine/radxa-dragon-q6a.md)
- `SRC_URI:append:radxa-dragon-q6a`: `append`, machine scope [`radxa-dragon-q6a`](../../conf/machine/radxa-dragon-q6a.md)

## Configuration fragments

[recipes-kernel/linux/radxa-dragon-q6a/realtek-eth-8169.cfg](radxa-dragon-q6a/realtek-eth-8169.cfg), added through `SRC_URI`.

| Option | Value |
| --- | --- |
| `CONFIG_NET_SELFTESTS` | `y` |
| `CONFIG_R8169` | `y` |
| `CONFIG_MDIO_BUS` | `y` |
| `CONFIG_PHYLIB` | `y` |
| `CONFIG_FIXED_PHY` | `y` |
| `CONFIG_REALTEK_PHY` | `y` |
| `CONFIG_REALTEK_PHY_HWMON` | `not set` |
| `CONFIG_FWNODE_MDIO` | `y` |
| `CONFIG_OF_MDIO` | `y` |
| `CONFIG_ACPI_MDIO` | `y` |

## Compatibility

- Machine scopes: [`radxa-dragon-q6a`](../../conf/machine/radxa-dragon-q6a.md).
