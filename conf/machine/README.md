# Machines

Each file defines a board that `MACHINE` can select. Both boards use the QCS6490
SoC configuration from [meta-qcom](https://github.com/qualcomm-linux/meta-qcom).

## Files

- [README.md](README.md) — Lists the supported machines.
- [radxa-dragon-q6a.conf](radxa-dragon-q6a.conf) — Defines the Radxa Dragon Q6A, which boots firmware from its SPI NOR and an OS from an SD, UFS, or NVMe disk image.
- [rubikpi3.conf](rubikpi3.conf) — Defines the Thundercomm RUBIK Pi 3, flashed with the boot firmware and partitions in the `qcomflash` package.
