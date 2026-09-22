# Branch maintenance

[qualcomm-linux/meta-qcom-3rdparty](https://github.com/qualcomm-linux/meta-qcom-3rdparty)
is the upstream project. The DevDocs fork carries documentation and development
review branches; it does not replace upstream maintainers or release support.
Use the [root README](README.md#branches) for the complete branch inventory.
This file's adopted home is `main`; review branches carry the proposed copy.

## Long-lived upstream branches

| Branch | Purpose and status | Build, contribution, and merge policy |
| --- | --- | --- |
| `main` | Primary development, upstream support, and current Yocto compatibility. | Build using that checkout's machine fragments and `LAYERSERIES_COMPAT`; submit normal product contributions here. Approved development changes land here. |
| `wrynose` | Yocto 6.0 LTS / Qualcomm Linux 2.x. | Build with matching release layers; maintained separately. Main changes labelled `backport (wrynose)` can create reviewable backport PRs. |
| `scarthgap` | Yocto 5.0 LTS / Qualcomm Linux 1.4 and later 1.x. | Build matching downstream layers; send release-specific fixes to that branch. Maintained separately from main. |
| `kirkstone` | Yocto 4.0 LTS / Qualcomm Linux 1.3 and earlier. | Retained older baseline; check the security policy and upstream release support before choosing it. Release fixes target that branch, not a wholesale merge into main. |
| `next` | Upstream staging branch. | Use only for development evaluation after checking its contents; normal contributions target main unless maintainers direct otherwise. Presence does not promise a release or merge schedule. |

## Fork branches

The fork's `main` is its default integration branch; it can differ from upstream
`main`. `upstream` is the fork's named review baseline for upstream-derived work.
Neither name guarantees that the branch is current: compare remote commits before
rebasing. Use matching layers when building either branch. Documentation proposals
may target the explicitly requested fork branch; product patches still go upstream.

The fork retains `kirkstone`, `scarthgap`, and `next` alongside its topic branches.
Release names carry the upstream compatibility intent, but verify the fork's
actual commit before using them. Fork topic branches are review/development work,
not supported release baselines. Their presence does not establish approval or
an intended merge destination. Review proposals against their stated base; do not
merge a topic branch merely because its name resembles a release.
