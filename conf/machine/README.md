# Machines

Each file here is a BitBake machine configuration; set `MACHINE`, or use the
matching `ci/<machine>.yml` fragment, to build for that board. The
[build tutorial](../../docs/source/user/USAGE.md) builds one of them.

## Files

- [README.md](README.md) — Lists the supported machines.
- [radxa-dragon-q6a.conf](radxa-dragon-q6a.conf) — Configures the Radxa Dragon Q6A (QCS6490), which boots from vendor firmware in SPI NOR.
- [rubikpi3.conf](rubikpi3.conf) — Configures the Thundercomm RUBIK Pi 3 (QCS6490), including its boot firmware and partition layout.
