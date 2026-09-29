SUMMARY = "Boot firmware for Thundercomm RUBIK Pi 3"
DESCRIPTION = "Qualcomm-signed SoC boot firmware and Rubik Pi 3-specific LUN 6 \
payloads from rubikpi-ai/boot-assets."

LICENSE = "LicenseRef-LICENSE.qcom-2"
LIC_FILES_CHKSUM = "file://LICENSE.txt;md5=165287851294f2fb8ac8cbc5e24b02b0"

SRC_URI = "git://github.com/rubikpi-ai/boot-assets;protocol=https;branch=main;destsuffix=${BP}"
SRCREV = "10b868574aa4d06fb3836399d10eb5c792765504"

INHIBIT_DEFAULT_DEPS = "1"
do_configure[noexec] = "1"
do_compile[noexec] = "1"

inherit allarch deploy

QCOM_BOOT_IMG_SUBDIR = "rubikpi3"

COMPATIBLE_MACHINE = "(rubikpi3)"

# @description Install the boot binaries and the CDT into the deploy directory
#   under QCOM_BOOT_IMG_SUBDIR, where the qcomflash image type collects them.
# @noargs
# @exitcode 0 The files are deployed.
# @exitcode 1 An install command failed, for example because RubikPi3_CDT.bin is missing.
# @example
#   bitbake firmware-qcom-boot-rubikpi3 -c deploy
do_deploy() {
    install -d ${DEPLOYDIR}/${QCOM_BOOT_IMG_SUBDIR}

    for ext in elf mbn fv img; do
        find "${S}" -maxdepth 1 -name "*.${ext}" \
            -exec install -m 0644 {} ${DEPLOYDIR}/${QCOM_BOOT_IMG_SUBDIR}/ \;
    done

    # qcomflash consumes the CDT as cdt.bin via QCOM_CDT_FILE.
    install -m 0644 "${S}/RubikPi3_CDT.bin" ${DEPLOYDIR}/${QCOM_BOOT_IMG_SUBDIR}/
}
addtask deploy before do_build after do_install
