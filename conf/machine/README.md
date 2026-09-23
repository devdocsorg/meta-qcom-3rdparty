# Machines

Each file defines a supported board; select it with `MACHINE` or a kas machine
fragment in [ci/](../../ci/README.md). The
[configuration reference](../../docs/source/user/CONFIGURATION.md#machine-configuration)
compares their settings.

## Files

- [README.md](README.md) — Lists the supported machines.
- [radxa-dragon-q6a.conf](radxa-dragon-q6a.conf) — Defines the Radxa Dragon Q6A (QCS6490), which boots a `wic` disk image from its SPI NOR firmware.
- [rubikpi3.conf](rubikpi3.conf) — Defines the Thundercomm RUBIK Pi 3 (QCS6490), flashed with a `qcomflash` package.
