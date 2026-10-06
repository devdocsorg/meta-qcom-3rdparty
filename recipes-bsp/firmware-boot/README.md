# Boot firmware recipes

Boot firmware that [`meta-qcom`](https://github.com/qualcomm-linux/meta-qcom)
does not provide; the machine's `QCOM_BOOT_FIRMWARE` setting selects the recipe.

## Files

- [firmware-qcom-boot-rubikpi3_20260915.bb](firmware-qcom-boot-rubikpi3_20260915.bb) — Fetches the RUBIK Pi 3 boot firmware and configuration data table from the vendor's [boot-assets](https://github.com/rubikpi-ai/boot-assets) repository and deploys them for the flashable image.
- [README.md](README.md) — Describes the boot firmware recipes.
