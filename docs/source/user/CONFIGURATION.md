# Configuration reference

This page explains the settings this layer chooses. Standard variable meanings
come from the [Yocto Project variable glossary](https://docs.yoctoproject.org/wrynose/ref-manual/variables.html)
for the wrynose release, [BitBake assignment syntax](https://docs.yoctoproject.org/bitbake/2.16/bitbake-user-manual/bitbake-user-manual-metadata.html),
and the [kas project configuration format](https://kas.readthedocs.io/en/4.8/userguide/project-configuration.html).

## Loading and precedence

kas reads a chain of fragments from `ci/`, checks out the listed layers, and
writes `local.conf` and `bblayers.conf` in its build directory. BitBake then
parses `local.conf`, each layer's `conf/layer.conf`, the machine file named by
`MACHINE`, and recipes with their `.bbappend` files. A `?=` assignment only sets
a default when nothing earlier set the variable, so a later `?=` has no effect;
`=` and `+=` apply in parse order; `:append` is applied last. A `:rubikpi3` or
`:radxa-dragon-q6a` override applies only when that machine is selected.

## Environment

kas-container and the CI helper read these variables from the environment.
[.env.example](../../../.env.example) lists them with safe values; nothing loads
it automatically. Copy it to `.env`, edit it, and run `set -a; . ./.env; set +a`
before the kas commands. Sourcing the file replaces values already exported in
your shell.

| Variable | Purpose | Type and default | Example |
| --- | --- | --- | --- |
| `KAS_CONTAINER` | kas-container script used by `ci/kas-container-shell-helper.sh` | Optional path; default is `kas-container` on `PATH` | `/opt/kas/kas-container` |
| `KAS_WORK_DIR` | Directory holding layer checkouts and the `build/` directory | Optional path; default is the current directory | `$HOME/kas-work` |
| `DL_DIR` | Download cache shared between builds ([DL_DIR](https://docs.yoctoproject.org/wrynose/ref-manual/variables.html#term-DL_DIR)) | Optional path; default is `build/downloads` | `$HOME/yocto-cache/downloads` |
| `SSTATE_DIR` | Shared state cache ([SSTATE_DIR](https://docs.yoctoproject.org/wrynose/ref-manual/variables.html#term-SSTATE_DIR)) | Optional path; default is `build/sstate-cache` | `$HOME/yocto-cache/sstate-cache` |

kas documents how it forwards these in its
[environment variables](https://kas.readthedocs.io/en/4.8/command-line.html#environment-variables) list.

## Layer configuration

[conf/layer.conf](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/main/conf/layer.conf)
registers the layer with BitBake. All values are required for the layer to load.

| Variable | Local value and purpose |
| --- | --- |
| `BBPATH` | Appends the layer directory so BitBake finds `conf/machine/*.conf`. |
| `BBFILES` | Parses `recipes-*/*/*.bb` and `recipes-*/*/*.bbappend`. |
| `BBFILE_COLLECTIONS`, `BBFILE_PATTERN_qcom-3rdparty` | Names the layer `qcom-3rdparty` and matches every file under it. |
| `BBFILE_PRIORITY_qcom-3rdparty` | `5`: the priority used when two layers provide the same recipe. |
| `LAYERDEPENDS_qcom-3rdparty` | `core qcom`: OE-Core and meta-qcom must be in the build. |
| `LAYERSERIES_COMPAT_qcom-3rdparty` | `wrynose`: the Yocto Project release this branch supports. |
| `BBFILES_DYNAMIC` | Parses `dynamic-layers/qcom-distro/` only when meta-qcom-distro (`qcom-distro`) is present. |

## Machine configuration

Each file in [conf/machine/](https://github.com/qualcomm-linux/meta-qcom-3rdparty/tree/main/conf/machine)
starts with `#@TYPE`, `#@NAME`, and `#@DESCRIPTION` comments that name the board,
then requires meta-qcom's
[qcom-qcs6490.inc](https://github.com/qualcomm-linux/meta-qcom/blob/master/conf/machine/include/qcom-qcs6490.inc),
which supplies the QCS6490 defaults referred to below.

| Machine | Board | Output |
| --- | --- | --- |
| `rubikpi3` | Thundercomm RUBIK Pi 3 (QCS6490) | `qcomflash` package with boot firmware, partitions, ESP, and root filesystem |
| `radxa-dragon-q6a` | Radxa Dragon Q6A (QCS6490) | `wic` disk image (ESP and root filesystem); SPI NOR boot firmware is flashed separately with Radxa's tools |

| Setting | Purpose | Type and default | `rubikpi3` | `radxa-dragon-q6a` |
| --- | --- | --- | --- | --- |
| `PREFERRED_PROVIDER_virtual/kernel ?=` | Kernel recipe | Recipe name; the SoC include defaults to `linux-qcom-next` | `linux-qcom-next`, set before the SoC include so it takes effect | `linux-qcom-next`, after the include, so the matching SoC default applies |
| `MACHINE_FEATURES +=` | Hardware features recipes may use | Word list; SoC default `alsa bluetooth usbgadget usbhost wifi` | `efi pci` | `efi pci` |
| `KERNEL_CMDLINE_EXTRA:append` | Extra kernel arguments in the unified kernel image | String; unset | `deferred_probe_timeout=30`, so the display driver waits for the HDMI bridge | Not set |
| `KERNEL_DEVICETREE` | Device tree built by the kernel | Path list; required | `qcom/qcs6490-thundercomm-rubikpi3.dtb` | `qcom/qcs6490-radxa-dragon-q6a.dtb` |
| `QCOM_DTB_DEFAULT ?=` | Device tree the boot firmware selects | Name; default `multi-dtb` | `qcs6490-thundercomm-rubikpi3` | `qcs6490-radxa-dragon-q6a` |
| `QCOM_BOOT_FIRMWARE` | Recipe deploying boot firmware into `qcomflash` | Recipe name; default empty | `firmware-qcom-boot-rubikpi3` | Empty: firmware is not built |
| `QCOM_BOOT_FILES_SUBDIR` | Deploy subdirectory holding the boot files | Path; default empty | `rubikpi3` | Empty |
| `QCOM_PARTITION_FILES_SUBDIR` | qcom-ptool partition layout to package | Path; defaults to the boot files subdirectory | `partitions/qcs6490-thundercomm-rubikpi3/ufs` (weak default) | Empty |
| `QCOM_PARTITION_FILES_SUBDIR_SPINOR`, `QCOM_PARTITION_CONF` | SPI NOR layout and partition recipe | Path and recipe name; defaults empty and `qcom-partition-conf` | Defaults | Empty: no partition package |
| `QCOM_CDT_FILE` | Board configuration data table packaged as `cdt.bin` | File name without extension; default empty | `RubikPi3_CDT` | Empty |
| `WKS_FILE` | Partition layout of the `wic` image | File name; unset | Not set | `efi-uki-bootdisk.wks.in`: ESP with systemd-boot and the kernel image, then root |
| `QCOM_ESP_IMAGE` | Separate ESP image recipe | Recipe name; `esp-qcom-image` when `efi` is set | Default | Empty: the `wic` layout creates the ESP |
| `QCOM_VFAT_SECTOR_SIZE ?=` | ESP sector size in bytes | Integer; default `4096` for UFS | Default | `512` for SD cards; use `4096` for UFS |
| `QCOM_BOOTIMG_ROOTFS ?=` | `root=` kernel argument | Device identifier; default `PARTLABEL=rootfs` | Default | `PARTLABEL=root` |
| `IMAGE_FSTYPES +=` | Image formats written | Word list; SoC default `ext4 qcomflash` | Default | `wic wic.gz wic.bmap` |
| `MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS +=` | Packages installed in every image | Package list | SoC boot and module groups, `packagegroup-rubikpi3-firmware` | SoC groups, `packagegroup-radxa-dragon-q6a-firmware`, `packagegroup-radxa-dragon-q6a-hexagon-dsp-binaries`, `qairt-sdk-hexagon-v68` |

The Radxa file notes that `PREFERRED_PROVIDER_virtual/bootloader` stays unset:
the board boots from EDK2 in its SPI NOR, so no U-Boot is built.

## Kernel and image additions

[linux-qcom-next_git.bbappend](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/main/recipes-kernel/linux/linux-qcom-next_git.bbappend)
adds `recipes-kernel/linux/linux-qcom-next/` to the file search path, which has no
effect while that folder does not exist, and for `radxa-dragon-q6a` adds the
`radxa-dragon-q6a/` folder and merges its
[realtek-eth-8169.cfg](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/main/recipes-kernel/linux/radxa-dragon-q6a/realtek-eth-8169.cfg)
[configuration fragment](https://docs.yoctoproject.org/wrynose/kernel-dev/common.html#creating-configuration-fragments)
into the kernel configuration.

| Kconfig option | Value | Purpose |
| --- | --- | --- |
| `CONFIG_R8169`, `CONFIG_REALTEK_PHY` | `y` | Build the Realtek RTL8169 Ethernet driver and its PHY driver into the kernel. |
| `CONFIG_PHYLIB`, `CONFIG_MDIO_BUS`, `CONFIG_FWNODE_MDIO`, `CONFIG_OF_MDIO`, `CONFIG_ACPI_MDIO`, `CONFIG_FIXED_PHY` | `y` | Build the PHY and MDIO support the driver needs, instead of loading modules. |
| `CONFIG_NET_SELFTESTS` | `y` | Build the network self-tests that the driver selects. |
| `CONFIG_REALTEK_PHY_HWMON` | Not set | Leave out the PHY temperature sensor. |

Options set to `y` are built in; an option not listed keeps the value from the
kernel's default configuration.

[qcom-multimedia-image.bbappend](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/main/dynamic-layers/qcom-distro/recipes-products/images/qcom-multimedia-image.bbappend)
applies only with meta-qcom-distro. For `rubikpi3` it adds
`firmware-qcom-boot-rubikpi3:LicenseRef-LICENSE.qcom-2` to
[INCOMPATIBLE_LICENSE_EXCEPTIONS](https://docs.yoctoproject.org/wrynose/ref-manual/variables.html#term-INCOMPATIBLE_LICENSE_EXCEPTIONS),
so that image can ship the board's boot firmware under the distribution's licence policy.

## kas fragments

Every file in [ci/](https://github.com/qualcomm-linux/meta-qcom-3rdparty/tree/main/ci)
uses kas format `header.version: 14`; the first-line
`yaml-language-server` comment only enables editor schema checks. Combine
fragments with colons, for example `ci/rubikpi3.yml:ci/qcom-distro.yml`; later
fragments override earlier ones.

| File | Settings and purpose |
| --- | --- |
| `base.yml` | Includes meta-qcom's `ci/base.yml` (OE-Core, BitBake, `nodistro`, target `core-image-base`), takes meta-qcom from its `master` branch, and adds this checkout as `meta-qcom-3rdparty`. |
| `rubikpi3.yml`, `radxa-dragon-q6a.yml` | Include `base.yml` and set `machine`. |
| `meta-qcom.yml` | Declares the meta-qcom repository for the fragments below. |
| `qcom-distro.yml` | Includes meta-qcom's `ci/qcom-distro.yml`: the `qcom-distro` distribution, its layers, and its image targets. |
| `ci.yml`, `mirror.yml` | Include meta-qcom's CI settings and its Yocto Project shared state mirror. |
| `linux-qcom-next.yml` | Forces `PREFERRED_PROVIDER_virtual/kernel = "linux-qcom-next"` in `local.conf`, overriding the machine default. |
| `world.yml` | Builds target `world`, limited by `EXCLUDE_FROM_WORLD` to recipes from meta-qcom (`layer-qcom`) and this layer (`layer-qcom-3rdparty`). |

## Repository automation

[CODEOWNERS](https://github.com/qualcomm-linux/meta-qcom-3rdparty/blob/main/.github/CODEOWNERS)
assigns every path to the layer maintainers. The markdownlint rules and the
documentation build settings are explained by comments in
`.github/.markdownlint.yaml`, `docs/source/conf.py`, `docs/source/Makefile`, and
`docs/source/requirements.txt`. Each workflow in
[.github/workflows/](https://github.com/qualcomm-linux/meta-qcom-3rdparty/tree/main/.github/workflows):

- `pr.yml`: pull requests to `main` that change more than Markdown; builds both machines through `build-yocto.yml`.
- `push.yml`: pushes to `main`; runs the same build.
- `nightly-build.yml`, `nightly-build-wrynose.yml`: daily build of `main` and `wrynose`, skipped when the same inputs already built successfully.
- `build-yocto.yml`: reusable build; locks the layers with kas, runs `yocto-patchreview` and `yocto-check-layer`, and builds each machine with `nodistro` and `qcom-distro` (a `world` build only with `nodistro`).
- `bitbake-lint.yml`: pull requests changing BitBake files; reports oelint-adv findings on the changed lines without failing.
- `markdownlint.yml`: pushes to `main` and pull requests changing Markdown; lints every `*.md` file.
- `qcom-preflight-checks.yml`: pull requests and pushes to `main`; runs Qualcomm's preflight workflow with only the Repolinter check enabled.
- `documentation.yml`: pull requests and pushes to `main`; runs `make -f docs/source/Makefile check`.
- `backport.yml`: merged pull requests to `main` labelled `backport wrynose`; opens the backport pull request.
- `stales.yml`: daily; marks issues and pull requests inactive for 30 days as stale and closes stale pull requests 5 days later.
- `test-pr.yml`, `test.yml`, `test-distro.yml`, `publish-results.yml`: LAVA boot tests and result publishing; disabled until a machine in this layer has a lab device.
