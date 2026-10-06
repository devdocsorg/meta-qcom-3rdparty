# Machines

Set `MACHINE` to a file name below, without `.conf`, or use the matching kas
fragment in [ci/](../../ci/README.md). Both boards use the QCS6490 SoC and are
built by CI with and without the Qualcomm distribution.

## Files

- [README.md](README.md) — Lists the supported machines.
- [radxa-dragon-q6a.conf](radxa-dragon-q6a.conf) — Defines the Radxa Dragon Q6A, which boots an EFI disk image from its own SPI NOR firmware.
- [rubikpi3.conf](rubikpi3.conf) — Defines the Thundercomm RUBIK Pi 3, flashed with Qualcomm boot firmware from this layer.
