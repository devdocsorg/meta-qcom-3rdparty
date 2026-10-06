# Branches

| Branch | Purpose | Status | Use and contributions | Relationship to main |
| --- | --- | --- | --- | --- |
| `main` | Primary development branch, with focus on upstream support and compatibility with the most recent Yocto Project release | Development, compatible with the `blacksail` release series | Build `radxa-dragon-q6a` and `rubikpi3`; changes land here first | Canonical branch |
| `wrynose` | LTS branch based on the Yocto Project 6.0 release, used by Qualcomm Linux 2.x | Long-term support until April 2030 | Build `radxa-dragon-q6a` and `rubikpi3`; receives backports of changes merged on `main` | Maintained separately: merged pull requests labelled `backport wrynose` are cherry-picked from `main` by [backport.yml](.github/workflows/backport.yml) |
| `scarthgap` | Qualcomm Linux >= 1.4, aligned with Yocto Project 5.0 (LTS) | Yocto Project 5.0 is supported until April 2028; last commit 2025-09-03 | Holds only `conf/layer.conf` and CI configuration, so there is no board support to build; the contribution guide names it as the target for Qualcomm Linux 1.x changes | Maintained separately; its history is not merged into `main` |
| `kirkstone` | Qualcomm Linux <= 1.3, aligned with Yocto Project 4.0 (LTS) | Yocto Project 4.0 is end of life; last commit 2025-04-09 | Holds only `conf/layer.conf` and CI configuration, so there is no board support to build; [SECURITY.md](SECURITY.md) accepts patches only for LTS releases and `main` | Not documented; its history is not merged into `main` |
| `next` | Not documented | Not documented; last commit 2026-08-20 | Holds the `radxa-dragon-q6a`, `uno-q`, and `ventuno-q` machines for the `wrynose` release series; whether to build from it or contribute to it is not documented | Not documented; it branched from `main` and adds one CI commit |

Support periods come from the [Yocto Project releases page](https://wiki.yoctoproject.org/wiki/Releases).
The [contribution guide](docs/source/contributing/CONTRIBUTING.md#branches-and-backports)
explains where changes for each branch go.

Create a long-lived branch only when the project has a maintenance need for it.
Document its purpose, support status, and whether changes merge back into `main`.
List every branch, including temporary branches, in the
[README](README.md#branches); remove entries when their branches are deleted.
