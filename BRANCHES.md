# Branches

## Upstream maintenance

[Qualcomm Linux](https://github.com/qualcomm-linux/meta-qcom-3rdparty) owns the layer.
Its `main` branch is the primary development and contribution destination.
Release branches are maintained separately for their Yocto baselines; relevant
fixes can be backported rather than merging a whole release branch into `main`.

| Branch | Purpose, status, and use | Contribution destination |
| --- | --- | --- |
| `main` | Active upstream development, tracking the most recent Yocto release; use for upstream work. | Upstream `main`. |
| `next` | Upstream integration branch; the repository provides no supported release contract for it. Use only when maintainers request it. | Upstream `main` unless maintainers direct otherwise. |
| `wrynose` | Separately maintained Yocto 6.0 LTS / Qualcomm Linux 2.x baseline. | Upstream `main` with the existing wrynose backport process, or maintainer-directed release fixes. |
| `scarthgap` | Separately maintained Yocto 5.0 LTS / Qualcomm Linux >= 1.4 baseline. | Upstream `scarthgap` for downstream changes described in the contribution guide. |
| `kirkstone` | Separately maintained Yocto 4.0 LTS / Qualcomm Linux <= 1.3 baseline; check the security policy for supported fixes. | Consult upstream maintainers for release support. |

## Documentation fork

This checkout is the [DevDocs fork](https://github.com/devdocsorg/meta-qcom-3rdparty).
Its `upstream` branch supplies the raw source base for this proposal and is a
tracking branch, not the upstream project's contribution destination. Fork `main`
and the retained `next`, `scarthgap`, and `kirkstone` branches are fork snapshots;
do not assume that a fork branch matches upstream HEAD. `devdocs/main` and
`devdocs/build` are separately named fork integration/build work; their names alone
do not establish release support or an upstream merge commitment.

`docs/offline-layer-guides` is the runnable documentation review branch. It targets
the fork's `upstream` base for review and remains a proposal until approved.
`BRANCHES.md` is maintained at the repository root; its canonical home on adoption
is `main`. Use [this proposal's copy](BRANCHES.md) while reviewing these files.

The root [README](README.md#branches) inventories the remaining temporary fork
branches. No supported build or merge commitment is inferred for a topic branch.
Upstream contribution routing remains the [project procedure](CONTRIBUTING.md).
