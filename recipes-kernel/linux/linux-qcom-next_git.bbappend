# Board-specific kernel configuration for meta-qcom's linux-qcom-next recipe.
# radxa-dragon-q6a adds realtek-eth-8169.cfg, which builds in the Realtek
# RTL8169 Ethernet driver and PHY support.
FILESEXTRAPATHS:prepend := "${THISDIR}/${BPN}:"

FILESEXTRAPATHS:prepend:radxa-dragon-q6a := "${THISDIR}/radxa-dragon-q6a:"

SRC_URI:append:radxa-dragon-q6a = " \
			file://realtek-eth-8169.cfg \
"
