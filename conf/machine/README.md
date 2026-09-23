# Supported machines

Each file defines one board, built with the matching kas fragment in
[ci/](../../ci/README.md) as the [usage tutorial](../../docs/source/user/USAGE.md)
shows. The [configuration reference](../../docs/source/user/CONFIGURATION.md#machines)
compares their settings.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [radxa-dragon-q6a.conf](radxa-dragon-q6a.conf) — Radxa Dragon Q6A (QCS6490): an SD, UFS, or NVMe disk image booted by the Radxa-provided SPI NOR firmware.
- [rubikpi3.conf](rubikpi3.conf) — Thundercomm RUBIK Pi 3 (QCS6490): a QDL-flashable UFS image with its boot firmware, without Wi-Fi and Bluetooth firmware so far.
