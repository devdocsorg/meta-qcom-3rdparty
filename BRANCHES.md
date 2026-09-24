# Branches

| Branch | Purpose | Maintenance | Relationship to `main` |
| --- | --- | --- | --- |
| `main` | Primary development branch, with focus on upstream support and compatibility with the most recent Yocto Project release. | Active; CI builds every push and runs nightly. | Canonical branch. |
| `wrynose` | LTS branch based on the Yocto Project 6.0 release, used by Qualcomm Linux 2.x. | Maintained separately; CI builds every push and runs nightly. | Receives backports of merged `main` changes; changes do not merge back. |
| `scarthgap` | Qualcomm Linux >= 1.4, aligned with Yocto Project 5.0 (LTS). | Maintained separately; holds layer and CI configuration only. | Does not merge back; depends on Qualcomm Linux 1.x layers. |
| `kirkstone` | Qualcomm Linux <= 1.3, aligned with Yocto Project 4.0 (LTS). | Maintained separately; holds layer and CI configuration only. | Does not merge back; depends on Qualcomm Linux 1.x layers. |

The [README](README.md#branches) also lists the staging and temporary backport
branches, and the [contribution guide](docs/source/contributing/CONTRIBUTING.md#27--branches-and-pull-requests)
explains where each change goes.
