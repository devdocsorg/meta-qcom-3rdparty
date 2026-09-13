# Branches

This is the DevDocs fork of
[qualcomm-linux/meta-qcom-3rdparty](https://github.com/qualcomm-linux/meta-qcom-3rdparty).
The branches below are development or release-line snapshots; their presence
in this fork is not a hardware-validation or security-support commitment.

## Long-lived branches

- `main` integrates upstream development. Submit generally useful BSP changes
  upstream, then bring accepted changes into the fork.
- `scarthgap` and `kirkstone` remain separate release lines. Do not merge their
  complete histories into `main`; port applicable fixes through upstream's
  release process.
- `devdocs/main` integrates DevDocs experiments separately. Move only reviewed,
  generally applicable changes toward upstream and `main`.
- `next` tracks staging work separately; it is not a stable release target.

## Branch inventory

| Branch | Purpose and status | Use and contributions |
| --- | --- | --- |
| `main` | Upstream integration snapshot for development | Use for current fork development; BSP submissions go upstream |
| `scarthgap` | Separate Yocto 5.0 / Qualcomm Linux 1.4+ line | Use with matching release dependencies; upstream release fixes only |
| `kirkstone` | Separate Yocto 4.0 / Qualcomm Linux 1.3 and earlier line | Use for that release only; check upstream security support |
| `next` | Upstream staging snapshot | Integration testing; not a release build target |
| `devdocs/main` | DevDocs integration development | DevDocs integration work; not an upstream release |
| `devdocs/build` | Local build resource settings | Development experiment; not a release target |
| `devdocs/s3-cache-backup` | DevDocs cache/integration backup snapshot | Reference snapshot; do not target new contributions |
| `devdocs/imx219-cam2` | IMX219 camera integration work | Board-specific development; coordinate changes with the branch owner |
| `devdocs/vscode` | Runtime support for development tooling | Development experiment; not a release target |
| `devdocs/docs-v3` | Documentation development snapshot | Reference prior documentation work; use the Sphinx branch for this update |
| `devdocs/generated-tutorials` | Generated tutorial work | Reference tutorial sources; use the Sphinx branch for this update |
| `devdocs/wrynose/docs` | Wrynose documentation development | Reference release-specific documentation work; not a release branch |
| `devdocs/wrynose/docs-v2` | Wrynose documentation revision | Reference release-specific documentation work; not a release branch |
| `docs/qli-2-tutorials` | QLI 2.0 tutorial development | Reference tutorial work; not a release build target |
| `njjetha` | Preflight workflow development snapshot | Reference CI work; not a release target |
| `radxa-dragon-q6a-hdmi` | Dragon Q6A HDMI/deferred-probe experiment | Board-specific development; not a release target |
| `radxa-dragon-q6a-hdmi-cmdline-extra` | Deferred-probe kernel command-line experiment | Board-specific development; not a release target |
| `radxa-dragon-q6a-hdmi-deferred-config` | Deferred-probe kernel configuration experiment | Board-specific development; not a release target |
| `radxa-dragon-q6a-hdmi-uki-cmdline` | Deferred-probe UKI command-line experiment | Board-specific development; not a release target |
| `devdocs/required-files-sphinx` | DevDocs checklist and Sphinx documentation development | Use to review this documentation update; target related contributions here |

The remaining branches are topic work or reference snapshots. Their names do
not establish an active maintenance commitment. Keep them separate until their
owners select changes for integration; do not merge experiments wholesale.
`devdocs/required-files-sphinx` is intended to merge into the DevDocs `main`
after the documentation approach is accepted, with upstream submission handled
separately.

Upstream also has a `wrynose` release branch for Qualcomm Linux 2.x. This fork
has no branch named `wrynose`; the `devdocs/wrynose/*` documentation branches
are not substitutes. Use the upstream release branch and matching release
manifest for release builds. Update this inventory when a branch is added,
removed, or changes purpose.
