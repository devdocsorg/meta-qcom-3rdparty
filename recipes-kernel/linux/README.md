# Linux kernel appends

The [configuration reference](../../docs/source/user/CONFIGURATION.md#kernel-configuration-fragment)
explains the append and the fragment it adds.

## Folders

- [radxa-dragon-q6a/](radxa-dragon-q6a/) — Holds [realtek-eth-8169.cfg](radxa-dragon-q6a/realtek-eth-8169.cfg), the Radxa Dragon Q6A kernel configuration fragment; it has no README because BitBake finds its files by name.

## Files

- [README.md](README.md) — Describes the kernel appends.
- [linux-qcom-next_git.bbappend](linux-qcom-next_git.bbappend) — Adds the board's configuration fragment to the `linux-qcom-next` kernel from [meta-qcom](https://github.com/qualcomm-linux/meta-qcom).
