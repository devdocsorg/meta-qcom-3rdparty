# Supported Machines

The machines this layer configures, one per `conf/machine/<machine>.conf`. Machine is the `MACHINE` value and the name of the kas fragment under `ci/`; Name and Description are the `#@NAME` and `#@DESCRIPTION` headers of that file. `ci/supported-machines.sh` writes this table from the headers and CI checks that they match, so a change starts in the machine file.

| Machine | Name | Description |
| --- | --- | --- |
| `radxa-dragon-q6a` | Radxa Dragon Q6A | Machine configuration for Radxa Dragon Q6A, with QCS6490 |
| `rubikpi3` | Thundercomm RUBIK Pi 3 (QCS6490) | Machine configuration for Thundercomm RUBIK Pi 3, with QCS6490. |
| `uno-q` | Arduino UNO Q | Machine configuration for Arduino UNO Q |
| `ventuno-q` | Arduino VENTUNO Q | Machine configuration for Arduino VENTUNO Q |

**SPDX-License-Identifier:** MIT
