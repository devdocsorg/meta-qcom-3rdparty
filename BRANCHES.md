# Branches

Select a branch together with the matching `meta-qcom` and OpenEmbedded Core
versions. The layer's `LAYERSERIES_COMPAT` setting records Yocto compatibility.

| Branch | Purpose | Contributions and maintenance |
| --- | --- | --- |
| `main` | Primary development, with focus on upstream support and the most recent Yocto release | Submit new development here. |
| `next` | CI and workflow validation before changes land on `main` | Use for integration testing; submit changes through the normal `main` review process. |
| `wrynose` | Yocto 6.0 LTS, used by Qualcomm Linux 2.x | Maintained separately; backport applicable fixes from `main`. |
| `scarthgap` | Yocto 5.0 LTS, used by Qualcomm Linux 1.4 and later 1.x releases | Maintained separately for the matching release. |
| `kirkstone` | Yocto 4.0 LTS, used by Qualcomm Linux 1.3 and earlier | Maintained separately for the matching release. |

In the `devdocsorg` fork, `devdocs/main` is a separately maintained integration
branch. Product changes are submitted to upstream `main` through the normal
review process. The fork's `upstream` branch records the upstream baseline for
review; it is refreshed from upstream and carries no independent product changes.
The [root branch inventory](README.md#branches) describes the fork's topic work.

Use the [security policy](SECURITY.md) for supported security-fix branches and
[contribution guidelines](docs/source/contributing/CONTRIBUTING.md) for submission requirements.
