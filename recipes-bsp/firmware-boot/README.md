# Boot firmware

## Files

- [README.md](README.md) — Describes the boot firmware recipes.
- [firmware-qcom-boot-rubikpi3_20260621.bb](firmware-qcom-boot-rubikpi3_20260621.bb) — Fetches the RUBIK Pi 3 boot binaries and CDT from `rubikpi-ai/boot-assets` and deploys them for the `qcomflash` package; its `do_deploy` task is in the [function reference](../../docs/source/contributing/README.md#function-reference).
