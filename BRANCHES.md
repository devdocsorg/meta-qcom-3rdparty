# Branches

| Branch | Purpose | Status | Relationship to `main` |
| --- | --- | --- | --- |
| `main` | Primary development, aligned with the most recent Yocto Project release | Active | Canonical branch |
| `wrynose` | Long-term support for Qualcomm Linux 2.x on Yocto Project 6.0 | Active | Maintained separately; fixes land on `main` first and are backported |
| `scarthgap` | Qualcomm Linux 1.4 and later on Yocto Project 5.0 | Maintenance policy not documented | Diverged from `main` in March 2025; its commits are not merged back |
| `kirkstone` | Qualcomm Linux 1.3 and earlier on Yocto Project 4.0 | Maintenance policy not documented; Yocto Project 4.0 is end of life | Diverged from `main` in March 2025; its commits are not merged back |
| `next` | Validating workflow changes before they land on `main`, per [9d6a08d](https://github.com/qualcomm-linux/meta-qcom-3rdparty/commit/9d6a08df6bf47047d359794155f315fae5c6b96d) | Maintenance policy not documented | Branched from `main` on 2026-08-20 and adds one commit; whether it merges back is not documented |

Merged pull requests to `main` that carry the `backport wrynose` label are
backported automatically by the
[backport workflow](.github/workflows/backport.yml); the
[agent guide](docs/source/contributing/AGENTS.md#8-backporting-to-a-release-branch)
describes manual backports. Pull requests target the branches named in the
[contribution guide](docs/source/contributing/CONTRIBUTING.md).

[SECURITY.md](SECURITY.md) accepts patches only for the LTS releases and `main`;
the [Yocto Project releases page](https://wiki.yoctoproject.org/wiki/Releases)
lists which releases are supported. The [README](README.md#branches) lists every
branch with its status and whether to build from it.
