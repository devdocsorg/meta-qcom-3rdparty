# Linux kernel appends

Machine-specific additions to the `linux-qcom-next` kernel recipe.

## Folders

- [radxa-dragon-q6a/](radxa-dragon-q6a/realtek-eth-8169.cfg) — Holds the Radxa Dragon Q6A kernel configuration fragment `realtek-eth-8169.cfg`; the recipe adds this folder to `FILESEXTRAPATHS`, so it takes no README.

## Files

- [README.md](README.md) — Describes the kernel appends.
- [linux-qcom-next_git.bbappend](linux-qcom-next_git.bbappend) — Adds the Realtek Ethernet fragment for the Radxa Dragon Q6A.
