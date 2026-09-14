SUMMARY = "Packages for the Thundercomm RUBIK Pi 3 platform"
DESCRIPTION = "Thundercomm RUBIK Pi 3 firmware. The -firmware package recommends \
GPU firmware when DISTRO_FEATURES has opencl, opengl or vulkan, plus QUPv3, video, \
audio and compute firmware."

inherit packagegroup

PACKAGES = " \
    ${PN}-firmware \
"

# Wifi (brcmfmac43456) and Bluetooth (BCM4345C5) firmware are not yet in
# upstream linux-firmware, so they are omitted; the board boots without them.
RRECOMMENDS:${PN}-firmware = " \
    ${@bb.utils.contains_any('DISTRO_FEATURES', 'opencl opengl vulkan', 'linux-firmware-qcom-adreno-a660 linux-firmware-qcom-qcm6490-adreno', '', d)} \
    linux-firmware-qcom-qcm6490-qupv3fw \
    linux-firmware-qcom-vpu \
    linux-firmware-qcom-qcs6490-thundercomm-rubikpi3-audio \
    linux-firmware-qcom-qcs6490-compute \
"
