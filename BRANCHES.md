# Branches

| Branch | Why it exists | Status | Relationship to `main` |
| --- | --- | --- | --- |
| `main` | Primary development branch, with focus on upstream support and compatibility with the most recent Yocto Project release. | Active development | Default branch; changes land here first. |
| `wrynose` | LTS branch based on the Yocto Project 6.0 release, used by Qualcomm Linux 2.x. | Maintained LTS release branch; Yocto Project 6.0 is supported until April 2030 ([releases](https://wiki.yoctoproject.org/wiki/Releases)) | Maintained separately: merged `main` changes are backported to it with `git cherry-pick -x`, and changes specific to it go to it directly ([backporting guide](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/a06d0c7ca08f701093e4373760ea913e61ae59ee/BACKPORTING.md)). |
| `scarthgap` | Qualcomm Linux >= 1.4, aligned with Yocto Project 5.0 (LTS). | Not documented; Yocto Project 5.0 is supported until April 2028 ([releases](https://wiki.yoctoproject.org/wiki/Releases)); last change on 2025-09-03 ([b411da7](https://github.com/qualcomm-linux/meta-qcom-3rdparty/commit/b411da79d08b3726eeba85df834627008b31fd7c)) | Diverged from `main` at [9a3d05c](https://github.com/qualcomm-linux/meta-qcom-3rdparty/commit/9a3d05c30a18a3c65ec7ed222c75f4436aa26cda); it holds only the layer configuration, policies, and CI. Whether it merges with `main` is not documented. |
| `kirkstone` | Qualcomm Linux <= 1.3, aligned with Yocto Project 4.0 (LTS). | Not documented; Yocto Project 4.0 is end of life ([releases](https://wiki.yoctoproject.org/wiki/Releases)); last change on 2025-04-09 ([d2f48af](https://github.com/qualcomm-linux/meta-qcom-3rdparty/commit/d2f48af6ee98870294be24c16673dde7fa941543)) | Diverged from `main` at [9a3d05c](https://github.com/qualcomm-linux/meta-qcom-3rdparty/commit/9a3d05c30a18a3c65ec7ed222c75f4436aa26cda); it holds only the layer configuration, policies, and CI. Whether it merges with `main` is not documented. |
| `next` | Not documented. The commit that adds it to the push build gives it CI coverage so it can validate workflow changes before they land on `main` ([9d6a08d](https://github.com/qualcomm-linux/meta-qcom-3rdparty/commit/9d6a08df6bf47047d359794155f315fae5c6b96d)). | Not documented; declares Yocto Project 6.0 (`wrynose`) compatibility; last change on 2026-08-20 ([9d6a08d](https://github.com/qualcomm-linux/meta-qcom-3rdparty/commit/9d6a08df6bf47047d359794155f315fae5c6b96d)) | Branched from `main` at [cad0b2b](https://github.com/qualcomm-linux/meta-qcom-3rdparty/commit/cad0b2b7ab58a89ff449f7ec77597b6f4b466262) and carries one commit that `main` does not; it holds the `uno-q` and `ventuno-q` machines, which `main` does not. Whether it merges back is not documented. |

Document each long-lived branch's purpose, support status, and whether changes
merge back into `main`. List every branch, including temporary branches, in the
[README](README.md#branches) with its build guidance and contribution
destination; remove entries when their branches are deleted.
[SECURITY.md](SECURITY.md#branches-maintained-with-security-fixes) states which
branches receive security fixes.
