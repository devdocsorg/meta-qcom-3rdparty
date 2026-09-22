# Dragon Q6A kernel configuration

The [kernel configuration fragment](realtek-eth-8169.cfg) requests the Realtek Ethernet driver and its PHY dependencies.
`m` requests a module and `y` built-in support; the selected kernel determines
each symbol's permitted type, dependencies, and effective value. Omitted symbols
keep the kernel defconfig or earlier fragment's setting.

| Symbol | Purpose | Requested value |
| --- | --- | --- |
| `CONFIG_NET_SELFTESTS` | Network device self-tests. | `y` |
| `CONFIG_R8169` | Realtek RTL8169-family Ethernet driver. | `y` |
| `CONFIG_MDIO_BUS` | MDIO bus support. | `y` |
| `CONFIG_PHYLIB` | Ethernet PHY library. | `y` |
| `CONFIG_FIXED_PHY` | Fixed-link PHY support. | `y` |
| `CONFIG_REALTEK_PHY` | Realtek Ethernet PHY drivers. | `y` |
| `CONFIG_REALTEK_PHY_HWMON` | Realtek PHY hardware monitoring. | `n` |
| `CONFIG_FWNODE_MDIO` | Firmware-node MDIO registration. | `y` |
| `CONFIG_OF_MDIO` | Device-tree MDIO registration. | `y` |
| `CONFIG_ACPI_MDIO` | ACPI MDIO registration. | `y` |

## Files

- [README.md](README.md): Introduces this directory and lists its contents.
- [realtek-eth-8169.cfg](realtek-eth-8169.cfg): Requests Dragon Q6A Realtek Ethernet and PHY support.
