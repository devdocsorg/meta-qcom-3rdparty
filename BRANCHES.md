# Branches

| Branch | Why it exists | Relationship to `main` |
| --- | --- | --- |
| `main` | Primary development branch, with focus on upstream support and the most recent Yocto Project release | Canonical branch |
| `wrynose` | LTS branch for Yocto Project 6.0, used by Qualcomm Linux 2.x | Maintained separately: it receives changes from `main` as cherry-picked backports, as [BACKPORTING.md on `wrynose`](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/wrynose/BACKPORTING.md) describes |
| `scarthgap` | Qualcomm Linux 1.4 and later, aligned with Yocto Project 5.0 | Not documented |
| `kirkstone` | Qualcomm Linux 1.3 and earlier, aligned with Yocto Project 4.0 | Not documented |
| `next` | Not documented | Not documented |

The [README](README.md#branches) gives each branch's status, build guidance, and
contribution destination.
