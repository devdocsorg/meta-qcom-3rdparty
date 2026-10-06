# Linux kernel

Appends board-specific configuration to the `linux-qcom-next` kernel from
[meta-qcom](https://github.com/qualcomm-linux/meta-qcom).

## Folders

- [radxa-dragon-q6a/](radxa-dragon-q6a/) — Holds the Radxa Dragon Q6A kernel configuration fragments, which the append finds by name through `FILESEXTRAPATHS`, so the folder takes no README.

## Files

- [README.md](README.md) — Describes the kernel append.
- [linux-qcom-next_git.bbappend](linux-qcom-next_git.bbappend) — Adds the Radxa Dragon Q6A Ethernet configuration fragment to the kernel.
