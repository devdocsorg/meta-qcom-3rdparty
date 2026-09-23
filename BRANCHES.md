# Branches

| Branch | Purpose | Status | Build from it | Changes go to | Relationship to `main` |
| --- | --- | --- | --- | --- | --- |
| `main` | Development against the most recent Yocto Project release | Active; the default branch | Yes | `main` | Canonical branch |
| `wrynose` | LTS branch for Yocto Project 6.0, used by Qualcomm Linux 2.x | Maintained | Yes, for Qualcomm Linux 2.x | `main`, then backported | Maintained separately; receives changes from `main` as cherry-picked backports and never merges back |
| `scarthgap` | Qualcomm Linux 1.4 and later, on Yocto Project 5.0 LTS | Maintenance | No: only the layer configuration and CI, no machines | `scarthgap` | Maintained separately |
| `kirkstone` | Qualcomm Linux 1.3 and earlier, on Yocto Project 4.0 LTS | End of life, like Yocto Project 4.0 | No: only the layer configuration and CI, no machines | None | Maintained separately; no longer updated |
| `next` | Maintainer branch for trying CI workflow changes before they reach `main` | Behind `main`; still carries the `uno-q` and `ventuno-q` machines that moved to meta-qcom-arduino | No | `main` | Not merged; changes reach `main` through pull requests |

The [contribution guide](docs/source/contributing/CONTRIBUTING.md#27--target-branches-and-submission)
explains each route.
