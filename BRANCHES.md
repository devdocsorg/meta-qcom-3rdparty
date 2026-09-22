# Branches

[qualcomm-linux/meta-qcom-3rdparty](https://github.com/qualcomm-linux/meta-qcom-3rdparty)
owns the layer and its contribution routes. The `devdocsorg` fork hosts
integration work and documentation review. The default branch is `main` in both
repositories; their contents can differ. This proposal's branch guide is linked
relatively because its files are available on `docs/contributor-reference`. After
adoption, the canonical guide belongs on `main`.

## Upstream maintenance

| Branch | Purpose and use | Contribution and merge relationship |
| --- | --- | --- |
| `main` | Active upstream development with the latest supported Yocto baseline; use for new board support. | Default target for upstream PRs. |
| `next` | Upstream integration branch; use only when following a maintainer's integration work. | Propose ordinary changes to `main`; integration work may feed `main`. |
| `wrynose` | Yocto 6.0 LTS for Qualcomm Linux 2.x; use for that release. | Maintained separately; the backport workflow selects it from `main` with the `backport wrynose` label. |
| `scarthgap` | Yocto 5.0 LTS for Qualcomm Linux 1.4 and later 1.x releases; use for that release. | Separately maintained release branch; target release-specific fixes here. |
| `kirkstone` | Yocto 4.0 LTS for Qualcomm Linux 1.3 and earlier; use for that release. | Separately maintained release branch; confirm security support through the upstream release policy. |

The fork's `main`, `next`, `scarthgap`, and `kirkstone` retain the corresponding
baseline roles. Its `upstream` branch is the raw baseline used for documentation
review and is maintained separately from the fork's integration branches.
Do not submit layer changes to that mirror branch. The upstream `wrynose` branch
is available from the Qualcomm repository.

## Fork topic branches

The [root README](README.md#fork-topic-branches) inventories all fork topic branches.
These are integration or review topics, not independently supported releases;
build one only for its named work. Their presence does not establish acceptance
or a promise to merge. Send layer changes to the appropriate upstream branch above,
and review a fork topic with its author before depending on it.
