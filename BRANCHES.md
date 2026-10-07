# Branches

The [README](README.md#branches) gives each branch's status, build guidance, and
contribution destination. This page records why each branch exists and how it
relates to `main`.

| Branch | Why it exists | Relationship to `main` |
| --- | --- | --- |
| `main` | Primary development branch, with focus on upstream support and compatibility with the most recent Yocto Project release. | Changes land here first ([release branches](docs/source/contributing/CONTRIBUTING.md#29--release-branches)). |
| `wrynose` | LTS branch based on the Yocto Project 6.0 release, used by Qualcomm Linux 2.x. | Receives backports of changes merged on `main`, and changes that apply only to `wrynose`. |
| `scarthgap` | Qualcomm Linux >= 1.4, aligned with Yocto Project 5.0 (LTS). | Separate downstream baseline for Qualcomm Linux 1.x ([contribution guide](docs/source/contributing/CONTRIBUTING.md#4--downstream-baseline--qualcomm-linux-1x)). Whether its changes merge back into `main` is not documented. |
| `kirkstone` | Qualcomm Linux <= 1.3, aligned with Yocto Project 4.0 (LTS). | Not documented. |
| `next` | Not documented. | Not documented, including whether the branch is long-lived. |

Create a long-lived branch only when the project has a maintenance need for it.
Document its purpose, support status, and whether changes merge back into `main`.
List every branch, including temporary branches, in the
[README](README.md#branches); remove entries when their branches are deleted.
