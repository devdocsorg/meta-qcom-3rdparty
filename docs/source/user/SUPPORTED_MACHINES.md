# Supported machines

The {download}`machine configurations <../../../conf/machine/README.md>` are the authoritative
list for this checkout. Both machines use Qualcomm QCS6490 and inherit the SoC
baseline from `meta-qcom`.

| Machine | Configuration and output | Firmware and limits |
| --- | --- | --- |
| `rubikpi3` | [Thundercomm RUBIK Pi 3](../../../conf/machine/rubikpi3.conf), DTB `qcom/qcs6490-thundercomm-rubikpi3.dtb`, `linux-qcom-next` selected before the SoC include. | Vendor boot assets and board CDT are deployed by this layer; partition assets come from `qcom-ptool` through `meta-qcom`. Wi-Fi/Bluetooth blobs are omitted because the packagegroup does not yet select upstream firmware for those devices. |
| `radxa-dragon-q6a` | [Radxa Dragon Q6A](../../../conf/machine/radxa-dragon-q6a.conf), DTB `qcom/qcs6490-radxa-dragon-q6a.dtb`, EFI UKI disk output in `wic`, `wic.gz`, and `wic.bmap` formats. | Radxa-managed SPI NOR firmware is flashed separately using Radxa's tools. This layer builds ESP/rootfs disk images and deliberately leaves the Qualcomm boot-firmware packaging settings empty. |

The Radxa kernel provider assignment follows the SoC include, so the first
upstream `?=` can win. Confirm the resolved provider with BitBake when changing
parent revisions; the [configuration reference](CONFIGURATION.md) explains
assignment precedence. Recipe presence is not a hardware-validation claim.
Neither machine currently has an enabled LAVA boot job in this repository.

The [RUBIK Pi tutorial](USAGE.md) demonstrates firmware output. The
[contributor machine example](../contributing/CONTRIBUTING.md#6--machine-example--thundercomm-rubik-pi-3)
explains how to add machine configurations, packagegroups, firmware, kernel
appends, and CI registration.
