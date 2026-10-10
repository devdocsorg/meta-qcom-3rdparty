# Linux kernel

Machine-specific additions to the `linux-qcom-next` kernel recipe from
[`meta-qcom`](https://github.com/qualcomm-linux/meta-qcom).

## Folders

- [radxa-dragon-q6a/](radxa-dragon-q6a/) — Holds the Radxa Dragon Q6A's kernel configuration fragment, [`realtek-eth-8169.cfg`](radxa-dragon-q6a/realtek-eth-8169.cfg). The kernel recipe finds its files by name, so the folder takes no README.

## Files

- [README.md](README.md) — Lists the kernel additions.
- [linux-qcom-next_git.bbappend](linux-qcom-next_git.bbappend) — Adds the Realtek Ethernet configuration fragment for `radxa-dragon-q6a`.
