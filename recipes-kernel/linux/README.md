# Linux kernel

## Folders

- [radxa-dragon-q6a/](radxa-dragon-q6a/) — Holds the Radxa Dragon Q6A kernel configuration fragment, [realtek-eth-8169.cfg](radxa-dragon-q6a/realtek-eth-8169.cfg), which enables its Realtek Ethernet. The kernel build reads this folder through `FILESEXTRAPATHS`, so it has no README.

## Files

- [README.md](README.md) — Lists the kernel append and its fragment folder.
- [linux-qcom-next_git.bbappend](linux-qcom-next_git.bbappend) — Adds the Radxa Dragon Q6A fragment to [meta-qcom](https://github.com/qualcomm-linux/meta-qcom)'s `linux-qcom-next` kernel for that board.
