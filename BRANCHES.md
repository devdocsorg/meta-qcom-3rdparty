# Branches

| Branch | Purpose | Relationship to main |
| --- | --- | --- |
| `main` | Primary development branch, with focus on upstream support and compatibility with the most recent Yocto Project release. | Canonical branch; all new work lands here. |
| `wrynose` | LTS branch based on the Yocto Project 6.0 release, used by Qualcomm Linux 2.x. | Maintained separately. Changes land on `main` first and are backported, as the branch's [BACKPORTING.md](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/wrynose/BACKPORTING.md) describes; wrynose-only changes stay on the branch. |
| `scarthgap` | Qualcomm Linux >= 1.4, aligned with Yocto Project 5.0 (LTS). | Receives Qualcomm Linux 1.x contributions directly; the project does not document whether changes merge back. |
| `kirkstone` | Qualcomm Linux <= 1.3, aligned with Yocto Project 4.0 (LTS). | Not documented. [SECURITY.md](SECURITY.md) accepts patches only for current LTS releases and `main`, and Yocto Project 4.0 is end of life. |
| `next` | Not documented. | Not documented. |

The [README](README.md#branches) gives each branch's status and build guidance,
and the [contribution guide](docs/source/contributing/CONTRIBUTING.md#27--submitting-changes)
says where to send changes. Update both when a branch is added or deleted.
