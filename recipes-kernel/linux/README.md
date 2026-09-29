# Linux kernel appends

## Folders

- [radxa-dragon-q6a/](radxa-dragon-q6a/) — Holds the Radxa Dragon Q6A kernel configuration fragment, `realtek-eth-8169.cfg`, which enables its Realtek Ethernet controller. The kernel build reads this folder by name, so it has no README.

## Files

- [README.md](README.md) — Describes this folder and indexes its contents.
- [linux-qcom-next_git.bbappend](linux-qcom-next_git.bbappend) — Adds the Radxa Dragon Q6A configuration fragment to the `linux-qcom-next` kernel.
