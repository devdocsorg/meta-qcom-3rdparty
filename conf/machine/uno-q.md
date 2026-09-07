<!-- Generated from conf/machine/uno-q.conf at wrynose @ 7649ae51 (2026-08-31) by docsgen on 2026-09-07. Manual edits will be overwritten on regeneration; change the source, not this page. -->

# uno-q

Machine configuration for Arduino UNO Q. Source: [conf/machine/uno-q.conf](uno-q.conf).

## Selection

```text
MACHINE = "uno-q"
```

Used by the kas fragment [ci/uno-q.yml](../../ci/uno-q.yml), the machine matrix in [.github/workflows/build-yocto.yml](../../.github/workflows/build-yocto.yml) and meta-qcom's compile action.

## Configuration variables

| Variable | Effect |
| --- | --- |
| [`MACHINEOVERRIDES`](https://docs.yoctoproject.org/ref-manual/variables.html#term-MACHINEOVERRIDES) `=.` | Extends the machine's override tokens, so assignments scoped to an added token apply to this machine. This machine adds `arduino:`. |
| [`PREFERRED_PROVIDER_virtual/kernel`](https://docs.yoctoproject.org/ref-manual/variables.html#term-PREFERRED_PROVIDER) `?=` | Selects the recipe that provides `virtual/kernel` for this machine. This machine uses [`linux-arduino`](../../recipes-kernel/linux/linux-arduino.md). |
| [`MACHINE_FEATURES`](https://docs.yoctoproject.org/ref-manual/variables.html#term-MACHINE_FEATURES) `=` | Hardware capability flags for the board. Distro policy and recipes test them to decide which support packages and configuration to include. Sets the machine features to `efi`, `usbhost`, `usbgadget`, `alsa`, `wifi` and `bluetooth`. |
| [`PREFERRED_PROVIDER_virtual/bootloader`](https://docs.yoctoproject.org/ref-manual/variables.html#term-PREFERRED_PROVIDER) `?=` | Selects the recipe that provides `virtual/bootloader` for this machine. This machine uses [`u-boot-arduino`](../../recipes-bsp/u-boot/u-boot-arduino.md). |
| [`UBOOT_CONFIG`](https://docs.yoctoproject.org/ref-manual/variables.html#term-UBOOT_CONFIG) `=` | The U-Boot configuration to build. This machine uses `qrb2210-arduino-imola`. |
| [`UBOOT_CONFIG[qrb2210-arduino-imola]`](https://docs.yoctoproject.org/ref-manual/variables.html#term-UBOOT_CONFIG) `=` | Maps a U-Boot configuration name to the defconfig that builds it. This machine uses `qcom_defconfig`. |
| `UBOOT_INITIAL_ENV =` | Names the initial environment file that OpenEmbedded's `u-boot` class embeds. Set empty, no initial environment is embedded. |
| `QCOM_DTB_DEFAULT ?=` | Names the device tree, without the `.dtb` suffix, whose vfat image the flash package carries as the default; the value `multi-dtb` selects a combined multi-device-tree image instead. This machine uses `qrb2210-arduino-imola`. Empty skips the default image. |
| [`KERNEL_DEVICETREE`](https://docs.yoctoproject.org/ref-manual/variables.html#term-KERNEL_DEVICETREE) `?=` | Device tree blobs the kernel recipe builds and deploys for this machine. This machine uses `qcom/qrb2210-arduino-imola.dtb`. |
| `KERNEL_CMDLINE_EXTRA +=` | Adds kernel command-line arguments to all three boot paths: the Android-style boot image, the U-Boot FIT script and the unified kernel image. This machine adds `deferred_probe_timeout=30`. |
| [`MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS`](https://docs.yoctoproject.org/ref-manual/variables.html#term-MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS) `+=` (2 assignments, accumulated) | Packages recommended into images built on `packagegroup-core-boot` for this machine. Recommendations are installed by default, though distro policy can filter them out. This machine adds [`packagegroup-uno-q-firmware`](../../recipes-bsp/packagegroups/packagegroup-uno-q.md), [`packagegroup-uno-q-hexagon-dsp-binaries`](../../recipes-bsp/packagegroups/packagegroup-uno-q.md) and `qbootctl` (external). The file notes: "Helper util to tell the android bootloader to mark the boot as successfull. The boot firmware will switch to slot B and fail to boot otherwise." |
| `QCOM_CDT_FILE =` | Names the configuration data table binary, without its `.bin` suffix, that the flash package carries as `cdt.bin`. This machine uses `cdt`. Empty leaves the flash package without a configuration data table. |
| `QCOM_BOOT_FILES_SUBDIR =` | Names the deploy subdirectory the flash package takes its boot firmware, configuration data table and SPI NOR files from. This machine uses `qrb2210-arduino-imola`. Empty leaves them out of the flash package. |
| `QCOM_PARTITION_FILES_SUBDIR ?=` | Names the deploy subdirectory whose GPT and rawprogram partition files are copied into the flash package. This machine uses `partitions/qrb2210-unoq/emmc-16GB`. Empty skips the copy. |
| `QCOM_BOOT_FIRMWARE =` | Names the recipe providing the vendor boot-firmware bundle; the flash image is built from its output. This machine uses [`firmware-qcom-boot-qrb2210-arduino-imola`](../../recipes-bsp/firmware-boot/firmware-qcom-boot-qrb2210-arduino-imola.md). Empty skips the step. |

Names marked (external) are not provided by this layer.

## Compatibility

- `require conf/machine/include/qcom-qcm2290.inc`: this file is not in this layer; BitBake resolves it through `BBPATH` from another layer in the build.
- Layer dependencies: `LAYERDEPENDS_qcom-3rdparty = "core qcom"` in [conf/layer.conf](../layer.conf). This repository pins no revision of those layers; the build supplies them, and `LAYERSERIES_COMPAT_qcom-3rdparty = "wrynose"` records the Yocto release series they must match.
- [firmware-qcom-boot-qrb2210-arduino-imola recipe](../../recipes-bsp/firmware-boot/firmware-qcom-boot-qrb2210-arduino-imola.md) declares `COMPATIBLE_MACHINE` for this machine.
- [linux-arduino recipe](../../recipes-kernel/linux/linux-arduino.md) declares `COMPATIBLE_MACHINE` for this machine.
- [u-boot-arduino recipe](../../recipes-bsp/u-boot/u-boot-arduino.md) declares `COMPATIBLE_MACHINE` for this machine.
- [esp-qcom-image bbappend](../../recipes-kernel/images/esp-qcom-image-bbappend.md) carries changes scoped to this machine.
- [qcom-multimedia-image bbappend](../../dynamic-layers/qcom-distro/recipes-products/images/qcom-multimedia-image-bbappend.md) carries changes scoped to this machine.
- Build configuration [ci/uno-q.yml](../../ci/uno-q.yml) selects this machine; see the [ci/ folder index](../../ci/README.md).
