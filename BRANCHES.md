# Branch maintenance

Qualcomm maintains the [upstream repository](https://github.com/qualcomm-linux/meta-qcom-3rdparty).
The root [README](README.md#branches) accounts for release, mirror, and review topics.

| Branch | Status and purpose | Build and contribution route | Merge relationship |
| --- | --- | --- | --- |
| `main` | Primary upstream development for current Yocto support. | Build current enablement; submit new upstream patches here. | Common development base. |
| `wrynose` | Yocto 6.0 LTS and Qualcomm Linux 2.x. | Build this release with matching layers; propose applicable maintenance fixes. | Maintained separately; the main-branch backport workflow accepts the `backport wrynose` label. |
| `scarthgap` | Yocto 5.0 LTS and Qualcomm Linux 1.4 or later. | Use for those products; send applicable LTS fixes to this branch. | Maintained separately from main. |
| `kirkstone` | Yocto 4.0 LTS and Qualcomm Linux through 1.3. | Use only for the matching legacy product; check the security policy for supported releases. | Maintained separately from main. |
| `next` | Upstream integration branch with no release guarantee described in this layer. | Use main unless a maintainer directs testing here. | Maintainer-controlled integration; no automatic merge promise. |
| `upstream` | The fork’s raw upstream mirror. | Comparison and documentation review base; product patches still go upstream. | Synchronised mirror, not an independent product release. |

The documentation proposal is intended for upstream review. Its topic checkout
is documented in [development setup](docs/source/contributing/DEVELOPMENT.md).
