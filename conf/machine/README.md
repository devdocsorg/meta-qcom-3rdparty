# Supported machines

Each file defines one board; build it with its kas file in [ci/](../../ci/README.md).

| Machine | Board | SoC | kas file |
| --- | --- | --- | --- |
| `radxa-dragon-q6a` | Radxa Dragon Q6A | QCS6490 | [radxa-dragon-q6a.yml](../../ci/radxa-dragon-q6a.yml) |
| `rubikpi3` | Thundercomm RUBIK Pi 3 | QCS6490 | [rubikpi3.yml](../../ci/rubikpi3.yml) |

## Files

- [radxa-dragon-q6a.conf](radxa-dragon-q6a.conf) — Defines the Radxa Dragon Q6A, which boots from Radxa's firmware in SPI NOR and gets an EFI disk image from this build.
- [README.md](README.md) — Lists the supported machines.
- [rubikpi3.conf](rubikpi3.conf) — Defines the Thundercomm RUBIK Pi 3, with this layer's boot firmware recipe and its partition layout.
