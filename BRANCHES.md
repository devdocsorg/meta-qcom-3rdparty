# Branches

Support status comes from the Yocto Project
[releases page](https://wiki.yoctoproject.org/wiki/Releases); each last update links
the branch's latest commit when this page was written. The
[contribution guide](docs/source/contributing/CONTRIBUTING.md) explains how to
send changes to each branch.

| Branch | Purpose | Status | Build from it | Changes and relationship to `main` |
| --- | --- | --- | --- | --- |
| `main` | Primary development branch, following the most recent Yocto Project release | Active | Yes: `rubikpi3` and `radxa-dragon-q6a` | Changes land here first. |
| `wrynose` | LTS branch on Yocto Project 6.0, used by Qualcomm Linux 2.x | Yocto Project LTS until April 2030 | Yes: the same machines as `main` | Does not merge back; receives backports of `main` changes. |
| `scarthgap` | Qualcomm Linux >= 1.4, on Yocto Project 5.0 | Yocto Project LTS until April 2028; last update [2025-09-03](https://github.com/qualcomm-linux/meta-qcom-3rdparty/commit/b411da79d08b3726eeba85df834627008b31fd7c) | No: it has no machine configurations, only `conf/layer.conf`, CI workflows, and policy files | Split from `main` in March 2025 and has not merged back; takes Qualcomm Linux 1.x changes. |
| `kirkstone` | Qualcomm Linux <= 1.3, on Yocto Project 4.0 | Yocto Project end of life; last update [2025-04-09](https://github.com/qualcomm-linux/meta-qcom-3rdparty/commit/d2f48af6ee98870294be24c16673dde7fa941543) | No: it has no machine configurations, only `conf/layer.conf`, CI workflows, and policy files | Split from `main` in March 2025 and has not merged back; whether it takes changes is not documented. |
| `next` | Not documented | Not documented; last update [2026-08-20](https://github.com/qualcomm-linux/meta-qcom-3rdparty/commit/9d6a08df6bf47047d359794155f315fae5c6b96d) | Not documented; it carries the `radxa-dragon-q6a`, `uno-q`, and `ventuno-q` machines | Not documented. |
