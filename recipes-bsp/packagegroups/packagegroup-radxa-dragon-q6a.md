<!-- Generated from recipes-bsp/packagegroups/packagegroup-radxa-dragon-q6a.bb at wrynose @ e804c5eb (2026-09-08) by docsgen on 2026-09-08. Manual edits will be overwritten on regeneration; change the source, not this page. -->

# packagegroup-radxa-dragon-q6a

Packages for the Radxa Dragon Q6A platform. Used by [conf/machine/radxa-dragon-q6a.conf](../../conf/machine/radxa-dragon-q6a.conf), which names `packagegroup-radxa-dragon-q6a-firmware` and `packagegroup-radxa-dragon-q6a-hexagon-dsp-binaries`.

A package group is a recipe that names a set of packages to install together, so a machine or an image pulls them in under one name ([package group](../../docs/glossary.md), [custom package groups](https://docs.yoctoproject.org/dev-manual/customizing-images.html#customizing-images-using-custom-package-groups)). This one bundles the firmware and Hexagon DSP packages the Radxa Dragon Q6A needs, each set under one installable name, and part of that firmware follows the distro's feature choices.

| Field | Detail |
| --- | --- |
| Recipe | [recipes-bsp/packagegroups/packagegroup-radxa-dragon-q6a.bb](packagegroup-radxa-dragon-q6a.bb) |

## Packages

This recipe produces `packagegroup-radxa-dragon-q6a-firmware` and `packagegroup-radxa-dragon-q6a-hexagon-dsp-binaries` (`${PN}` expands to `packagegroup-radxa-dragon-q6a`).

| Variable | Effect |
| --- | --- |
| [`PACKAGES`](https://docs.yoctoproject.org/ref-manual/variables.html#term-PACKAGES) `=` | The binary packages this recipe produces. This file sets it to `${PN}-firmware` and `${PN}-hexagon-dsp-binaries`. |
| [`RRECOMMENDS:${PN}-firmware`](https://docs.yoctoproject.org/ref-manual/variables.html#term-RRECOMMENDS) `=` | Runtime recommendations for the named package: installed by default, and removable without breaking the dependency graph. Sets the recommended packages to `${@bb.utils.contains_any('DISTRO_FEATURES', 'opencl opengl vulkan', 'linux-firmware-qcom-adreno-a660 linux-firmware-qcom-qcm6490-adreno', '', d)}`, `camxfirmware-kodiak`, `linux-firmware-lt9611uxc`, `linux-firmware-qcom-qcs6490-radxa-dragon-q6a-audio`, `linux-firmware-qcom-qcs6490-radxa-dragon-q6a-compute`, `linux-firmware-qcom-qcm6490-qupv3fw` and `linux-firmware-qcom-vpu`. |
| [`RDEPENDS:${PN}-hexagon-dsp-binaries`](https://docs.yoctoproject.org/ref-manual/variables.html#term-RDEPENDS) `=` | Runtime dependencies of the named package: they are installed alongside it. This file sets it to `hexagon-dsp-binaries-radxa-dragon-q6a-adsp` and `hexagon-dsp-binaries-radxa-dragon-q6a-cdsp`. |

## Compatibility

- `COMPATIBLE_MACHINE` is not set, so this recipe is not restricted to a machine by this file.
- Inherited classes: `packagegroup`, provided outside this layer.
