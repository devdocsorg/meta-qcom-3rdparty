# Linux kernel appends

Appends and configuration fragments for the `linux-qcom-next` kernel, explained in the
[configuration reference](../../docs/source/user/CONFIGURATION.md#kernel).

## Folders

- [radxa-dragon-q6a/](radxa-dragon-q6a/) — Holds the Radxa Dragon Q6A kernel configuration fragment, [realtek-eth-8169.cfg](radxa-dragon-q6a/realtek-eth-8169.cfg). The kernel build finds its files by name, so it has no README.

## Files

- [README.md](README.md) — Lists the kernel appends.
- [linux-qcom-next_git.bbappend](linux-qcom-next_git.bbappend) — Adds the Radxa Dragon Q6A Ethernet fragment to `linux-qcom-next`.
