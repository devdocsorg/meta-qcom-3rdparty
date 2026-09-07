<!-- Generated from conf/machine/radxa-dragon-q6a.conf at wrynose @ 7649ae51 (2026-08-31) by docsgen on 2026-09-07. Manual edits will be overwritten on regeneration; change the source, not this page. -->

# radxa-dragon-q6a

Machine configuration for Radxa Dragon Q6A, with QCS6490. Source: [conf/machine/radxa-dragon-q6a.conf](radxa-dragon-q6a.conf).

```text
Boot architecture:
  SPI NOR (Radxa-managed):  PBL -> XBL -> UEFI/EDK2 -> discovers ESP
  SD/UFS/NVMe (Yocto-built): ESP (systemd-boot + UKI) + rootfs

SPI NOR firmware is flashed separately via Radxa's edl-ng package.
This machine conf only produces the OS disk image (ESP + rootfs).
```

Bootloader: Radxa EDK2 in SPI NOR; no U-Boot needed

Do NOT set PREFERRED_PROVIDER_virtual/bootloader. The qcomflash class defaults to uefi.elf from QCOM_BOOT_FILES_SUBDIR, which is empty, so it's a no-op.

## Selection

```text
MACHINE = "radxa-dragon-q6a"
```

Used by the kas fragment [ci/radxa-dragon-q6a.yml](../../ci/radxa-dragon-q6a.yml), the machine matrix in [.github/workflows/build-yocto.yml](../../.github/workflows/build-yocto.yml) and meta-qcom's compile action.

## Configuration variables

| Variable | Effect |
| --- | --- |
| [`MACHINE_FEATURES`](https://docs.yoctoproject.org/ref-manual/variables.html#term-MACHINE_FEATURES) `+=` | Hardware capability flags for the board. Distro policy and recipes test them to decide which support packages and configuration to include. Adds the `efi` and `pci` machine features. |
| [`KERNEL_DEVICETREE`](https://docs.yoctoproject.org/ref-manual/variables.html#term-KERNEL_DEVICETREE) `=` | Device tree blobs the kernel recipe builds and deploys for this machine. This machine uses `qcom/qcs6490-radxa-dragon-q6a.dtb`. Grouped in the file under "Kernel / Device Tree". |
| [`PREFERRED_PROVIDER_virtual/kernel`](https://docs.yoctoproject.org/ref-manual/variables.html#term-PREFERRED_PROVIDER) `?=` | Selects the recipe that provides `virtual/kernel` for this machine. This machine uses `linux-qcom-next` (external). |
| `QCOM_BOOT_FIRMWARE =` | Names the recipe providing the vendor boot-firmware bundle; the flash image is built from its output. Empty skips the step. Grouped in the file under "Boot firmware: NOT managed by Yocto". The file notes: "SPI NOR contents (XBL, UEFI, TZ, HYP, DEVCFG, AOP, CDT) are provided by Radxa and flashed independently. Blank these out so the qcomflash class doesn't try to package or depend on Qualcomm boot firmware." |
| `QCOM_BOOT_FILES_SUBDIR =` | Names the deploy subdirectory the flash package takes its boot firmware, configuration data table and SPI NOR files from. Empty leaves them out of the flash package. |
| `QCOM_PARTITION_FILES_SUBDIR =` | Names the deploy subdirectory whose GPT and rawprogram partition files are copied into the flash package. Empty skips the copy. |
| `QCOM_PARTITION_FILES_SUBDIR_SPINOR =` | The same, for the partition files placed under the flash package's `spinor` directory. Empty skips the copy. |
| `QCOM_PARTITION_CONF =` | Names the recipe providing the partition configuration; the flash image is built after its deploy step. Empty skips the step. |
| `QCOM_CDT_FILE =` | Names the configuration data table binary, without its `.bin` suffix, that the flash package carries as `cdt.bin`. Empty leaves the flash package without a configuration data table. |
| [`WKS_FILE`](https://docs.yoctoproject.org/ref-manual/variables.html#term-WKS_FILE) `=` | The wic kickstart file describing the partition layout of the generated disk image. This machine uses `efi-uki-bootdisk.wks.in`. Grouped in the file under "EFI System Partition + UKI boot". The file notes: "Use the canned UEFI UKI WKS; it creates the ESP inline via the bootimg_efi plugin (systemd-boot + UKI) with correct GPT type GUID. No need for the standalone esp-qcom-image recipe." |
| `QCOM_ESP_IMAGE =` | Names the recipe that builds the EFI system partition image the flash image includes; the flash-image class picks `esp-qcom-image` on its own when `MACHINE_FEATURES` contains `efi`. Empty skips the ESP image. |
| `QCOM_VFAT_SECTOR_SIZE ?=` | Sets the sector size, passed to `mkfs.vfat -S`, of the device tree and EFI system partition vfat images; it has to match the storage medium. This machine uses `512`. The file notes: "SD card uses 512-byte sectors; override to 4096 for UFS targets". |
| `QCOM_BOOTIMG_ROOTFS ?=` | Sets the `root=` argument on the kernel command line of the Android-style boot image, the U-Boot FIT script and the unified kernel image. Required: the build fails when it is unset. This machine uses `PARTLABEL=root`. The file notes: "Root device identifier for the UKI kernel cmdline". |
| `QCOM_DTB_DEFAULT ?=` | Names the device tree, without the `.dtb` suffix, whose vfat image the flash package carries as the default; the value `multi-dtb` selects a combined multi-device-tree image instead. This machine uses `qcs6490-radxa-dragon-q6a`. Empty skips the default image. |
| [`IMAGE_FSTYPES`](https://docs.yoctoproject.org/ref-manual/variables.html#term-IMAGE_FSTYPES) `+=` | Image formats produced for this machine. This machine adds `wic`, `wic.gz` and `wic.bmap`. Grouped in the file under "Image output". |
| [`MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS`](https://docs.yoctoproject.org/ref-manual/variables.html#term-MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS) `+=` | Packages recommended into images built on `packagegroup-core-boot` for this machine. Recommendations are installed by default, though distro policy can filter them out. This machine adds `packagegroup-qcom-boot-essential` (external), `packagegroup-machine-essential-qcom-qcs6490-soc` (external), [`packagegroup-radxa-dragon-q6a-firmware`](../../recipes-bsp/packagegroups/packagegroup-radxa-dragon-q6a.md), [`packagegroup-radxa-dragon-q6a-hexagon-dsp-binaries`](../../recipes-bsp/packagegroups/packagegroup-radxa-dragon-q6a.md) and `qairt-sdk-hexagon-v68` (external). Grouped in the file under "Firmware packages". |

Names marked (external) are not provided by this layer.

## Compatibility

- `require conf/machine/include/qcom-qcs6490.inc`: this file is not in this layer; BitBake resolves it through `BBPATH` from another layer in the build.
- Layer dependencies: `LAYERDEPENDS_qcom-3rdparty = "core qcom"` in [conf/layer.conf](../layer.conf). This repository pins no revision of those layers; the build supplies them, and `LAYERSERIES_COMPAT_qcom-3rdparty = "wrynose"` records the Yocto release series they must match.
- [linux-qcom-next bbappend](../../recipes-kernel/linux/linux-qcom-next-bbappend.md) carries changes scoped to this machine.
- Build configuration [ci/radxa-dragon-q6a.yml](../../ci/radxa-dragon-q6a.yml) selects this machine; see the [ci/ folder index](../../ci/README.md).
