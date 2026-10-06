# Branches

| Branch | Purpose | Status | Use and contributions | Relationship to main |
| --- | --- | --- | --- | --- |
| `main` | Primary development branch, aligned with the most recent Yocto Project release | Active; CI builds every push and runs a nightly build | Build `rubikpi3` and `radxa-dragon-q6a` from it; [new work goes here](docs/source/contributing/CONTRIBUTING.md#29--target-branches) | Canonical branch |
| `wrynose` | LTS branch for Qualcomm Linux 2.x, on Yocto Project 6.0 | LTS; a scheduled workflow on `main` starts its nightly build; the [Yocto Project](https://wiki.yoctoproject.org/wiki/Releases) supports 6.0 until April 2030 | Build `rubikpi3` and `radxa-dragon-q6a` from it; [receives backports](docs/source/contributing/CONTRIBUTING.md#29--target-branches) | Fixes land on `main` first and are backported, as the [agent guide](docs/source/contributing/AGENTS.md#8-backporting-to-a-release-branch) describes |
| `scarthgap` | Downstream baseline for Qualcomm Linux 1.x (>= 1.4), on Yocto Project 5.0 | Not documented; the Yocto Project supports 5.0 until April 2028; [last commit](https://github.com/qualcomm-linux/meta-qcom-3rdparty/commits/scarthgap) 2025-09-03 | No machines to build; [Qualcomm Linux 1.x boards](docs/source/contributing/CONTRIBUTING.md#29--target-branches) | Not documented |
| `kirkstone` | Qualcomm Linux <= 1.3, on Yocto Project 4.0 | Not documented; the Yocto Project lists 4.0 as end of life; [last commit](https://github.com/qualcomm-linux/meta-qcom-3rdparty/commits/kirkstone) 2025-04-09 | No machines to build; [destination not documented](docs/source/contributing/CONTRIBUTING.md#29--target-branches) | Not documented |
| `next` | Not documented | Not documented; [last commit](https://github.com/qualcomm-linux/meta-qcom-3rdparty/commits/next) 2026-08-20 | Holds the `radxa-dragon-q6a`, `uno-q`, and `ventuno-q` machines; whether to build from it and its destination are [not documented](docs/source/contributing/CONTRIBUTING.md#29--target-branches) | Not documented |

Create a long-lived branch only when the project has a maintenance need for it.
Document its purpose, support status, and whether changes merge back into `main`.
List every branch, including temporary branches, in the
[README](README.md#branches); remove entries when their branches are deleted.
