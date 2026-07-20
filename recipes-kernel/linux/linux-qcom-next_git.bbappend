FILESEXTRAPATHS:prepend:radxa-dragon-q6a := "${THISDIR}/radxa-dragon-q6a:"

SRC_URI:append:radxa-dragon-q6a = " \
			file://realtek-eth-8169.cfg \
			file://camera.cfg \
			file://0001-arm64-dts-qcom-dragon-q6a-add-cam2-imx219.patch \
"
