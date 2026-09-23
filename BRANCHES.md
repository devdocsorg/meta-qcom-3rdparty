# Branches

| Branch | Purpose and status | Build and contribution route | Merge relationship |
| --- | --- | --- | --- |
| `main` | Active upstream development, following current Yocto support. | Start new upstream work here and submit pull requests to `main`. | Receives reviewed topic changes. |
| `next` | Integration branch for validating changes, including workflows. | Use only to test changes under integration; propose normal contributions to `main`. | Integration work is intended for `main`. |
| `wrynose` | Yocto 6.0 LTS, used by Qualcomm Linux 2.x. | Build this release with matching layers; submit release fixes to this branch. | Maintained separately; selected `main` fixes are backported. |
| `scarthgap` | Yocto 5.0 LTS, Qualcomm Linux 1.4 and later 1.x releases. | Use for the downstream baseline described in the contribution guide. | Maintained separately from upstream development. |
| `kirkstone` | Yocto 4.0 LTS baseline for Qualcomm Linux 1.3 and earlier. | Use only for those older releases; check upstream security support before deployment. | Maintained separately; not a route for new upstream development. |

The [security policy](SECURITY.md) accepts security patches for current LTS
releases and `main`. See [contributing](CONTRIBUTING.md) for BSP contribution rules.
The fork's `upstream` branch preserves the imported upstream baseline;
`docs/offline-guides-and-layer-map` proposes documentation against it and is a
review branch, not a separate product release.
