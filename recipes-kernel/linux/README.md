# Linux kernel appends

Board changes to the `linux-qcom-next` kernel recipe from
[`meta-qcom`](https://github.com/qualcomm-linux/meta-qcom).

## Folders

- [radxa-dragon-q6a/](radxa-dragon-q6a/) — Holds the Radxa Dragon Q6A kernel configuration fragment, [realtek-eth-8169.cfg](radxa-dragon-q6a/realtek-eth-8169.cfg), which enables its Realtek Ethernet. The recipe finds the fragment by name, so the folder holds only fragments and takes no README.

## Files

- [linux-qcom-next_git.bbappend](linux-qcom-next_git.bbappend) — Adds the Radxa Dragon Q6A fragment to the `linux-qcom-next` kernel for that machine only.
- [README.md](README.md) — Describes the kernel appends.
