# Linux kernel appends

Appends to the `linux-qcom-next` kernel recipe from [meta-qcom](https://github.com/qualcomm-linux/meta-qcom).

## Folders

- [radxa-dragon-q6a/](radxa-dragon-q6a/) — Holds the Radxa Dragon Q6A kernel configuration fragment, [realtek-eth-8169.cfg](radxa-dragon-q6a/realtek-eth-8169.cfg). It takes no README: the kernel recipe finds its files by name through `FILESEXTRAPATHS`.

## Files

- [README.md](README.md) — Indexes the kernel appends.
- [linux-qcom-next_git.bbappend](linux-qcom-next_git.bbappend) — Adds the Ethernet configuration fragment for radxa-dragon-q6a.
