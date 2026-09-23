# Branches

| Branch | Purpose | Status | Use and contributions | Relationship to main |
| --- | --- | --- | --- | --- |
| `main` | Development for the most recent Yocto Project release | Active | Build the latest board support; send changes here | Canonical branch |
| `wrynose` | Yocto Project 6.0 LTS, used by Qualcomm Linux 2.x | Active LTS | Build Qualcomm Linux 2.x; fixes arrive as backports of merged `main` pull requests labelled `backport wrynose` | Maintained separately |
| `scarthgap` | Yocto Project 5.0 LTS, Qualcomm Linux 1.4 and later | LTS; last changed September 2025 | Build Qualcomm Linux 1.4 or later; send Qualcomm Linux 1.x board support here, as the contribution guide describes | Maintained separately |
| `kirkstone` | Yocto Project 4.0 LTS, Qualcomm Linux 1.3 and earlier | LTS; last changed April 2025 | Build Qualcomm Linux 1.3 or earlier; send fixes for those releases here | Maintained separately |
| `next` | Staging branch for validating CI workflow changes | Last changed August 2026 | Do not build from it or send contributions to it | Its changes reach `main` through separate pull requests |

[SECURITY.md](SECURITY.md) accepts security patches for the LTS branches and
`main`. The [README](README.md#branches) lists every current branch, including
temporary ones.
