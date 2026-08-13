# Install Qualcomm Linux on the Radxa Dragon Q6A

Build Qualcomm Linux from source, flash it to a microSD card, and boot a Radxa Dragon Q6A board to a root shell over a serial console, all from one Windows PC.

This tutorial is for a developer with a Radxa Dragon Q6A board and a Windows 10 or 11 PC. No prior Yocto or embedded Linux experience is assumed. You are done when you can run a command in a root shell on the board.

This tutorial covers only a Windows host using WSL2. If your host runs native Linux or macOS, the build steps are similar but the flashing and serial steps differ; those hosts are not covered here. If you want to run Radxa OS (the board's default Debian-based OS) instead of Qualcomm Linux, follow [Radxa's install guide](https://docs.radxa.com/en/dragon/q6a/getting-started/install-system) instead.

> Info: Provenance and validation status. This tutorial was reconstructed from recorded bring-up sessions (June and July 2026) and cross-checked against the current [`meta-qcom-3rdparty`](https://github.com/qualcomm-linux/meta-qcom-3rdparty) repository (commit `dea38dcd9b1e`, 2026-07-09) and Radxa's published documentation. It has not yet been validated end to end on hardware. Steps marked "pending validation" are the ones whose exact values or outputs still need confirmation on a real board; see the accompanying validation plan before treating this page as tested.

## Contents

- [Background](#background)
- [How to read this tutorial](#how-to-read-this-tutorial)
- [What you need](#what-you-need)
- [Part 1: Set up the Windows build host](#part-1-set-up-the-windows-build-host)
- [Part 2: Get the build tool and the board's layer](#part-2-get-the-build-tool-and-the-boards-layer)
- [Part 3: Build the image](#part-3-build-the-image)
- [Part 4: Flash the microSD card](#part-4-flash-the-microsd-card)
- [Part 5: Connect the serial console](#part-5-connect-the-serial-console)
- [Part 6: Boot the board](#part-6-boot-the-board)
- [Final Check](#final-check)
- [Part 7 (optional): Log in over SSH](#part-7-optional-log-in-over-ssh)
- [Next steps](#next-steps)

## Background

There is no prebuilt Qualcomm Linux image for this board. Qualcomm publishes prebuilt images only for its own reference devices (such as the RB3 Gen 2), so for the Dragon Q6A you build the image from source. The board is supported by the community-maintained [`meta-qcom-3rdparty`](https://github.com/qualcomm-linux/meta-qcom-3rdparty) Yocto layer, and this tutorial builds that layer's own board configuration with the [kas](https://kas.readthedocs.io/en/latest/) tool. Expect roughly 50 GB of disk use and one to two hours of build time.

The work splits across two worlds on one PC: building happens inside WSL2 (Ubuntu), while flashing the card and sharing USB devices happen from Windows. Each part below says which side you are on.

## How to read this tutorial

Steps that can be checked end with a PASS line: the exact output that means the step worked, followed by what to do when it did not. Warning callouts mark mistakes that are expensive to recover from; Info callouts explain what you are seeing. Do the parts in order; each part assumes the previous one passed.

## What you need

Hardware:

- A Radxa Dragon Q6A board.
- A USB-C power adapter that supports 12 V USB-PD output. A basic 5 V phone charger is not sufficient.
- A microSD card, 16 GB or larger (minimum size pending validation).
- A USB microSD card reader that plugs into your Windows PC.
- A USB-to-UART serial adapter with 3.3 V logic (this guide was worked out with a CP210x-based adapter), plus three female-to-female jumper wires.
- Only if you ever need low-level recovery: a USB A-to-A data cable (male Type-A on both ends). A USB C-to-A cable does not work for recovery mode.

Host PC:

- Windows 10 or 11, with at least 100 GB of free disk space (the logged build used roughly 50 GB; exact requirement pending validation) and administrator rights to install software.

Expectations worth correcting before you start:

- Unlike an Arduino-class board, one USB cable cannot both power and program this board. Power, flashing, and console access are three separate connections.
- You do not need an HDMI monitor. With this image, an attached screen shows about one second of boot logs and then goes black; the serial console is the only reliable way to see and use the system.

## Part 1: Set up the Windows build host

You will build inside WSL2 (Ubuntu) using a containerized build tool, flash from Windows, and talk to the board from Windows. This part makes sure all four host tools are ready.

1. Open PowerShell.

2. Check whether WSL2 with Ubuntu is installed.

   ```powershell
   wsl -l -v
   ```

   PASS: the output lists `Ubuntu` with `VERSION` `2`.

   If it does not, install it by following [Microsoft's WSL installation guide](https://learn.microsoft.com/en-us/windows/wsl/install), then run the check again. Return here when `Ubuntu` shows `VERSION` `2`.

3. Open an Ubuntu (WSL) terminal.

4. Check whether Docker is available inside WSL.

   ```bash
   docker run --rm hello-world
   ```

   PASS: the output contains `Hello from Docker!`.

   If the command is not found or fails, install [Docker Desktop for Windows](https://docs.docker.com/desktop/setup/install/windows-install/) and enable its WSL integration for Ubuntu under `Settings` > `Resources` > `WSL integration`, then run the check again.

   > Warning: Docker Desktop's WSL integration can silently drop after updates or reboots. If `docker` stops being found inside WSL later, re-enable the integration in Docker Desktop settings.

5. On Windows, install [balenaEtcher](https://etcher.balena.io/), the tool that writes the built image to the microSD card.

6. On Windows, install [usbipd-win](https://github.com/dorssel/usbipd-win), the tool that shares USB devices with WSL. In a PowerShell window, run:

   ```powershell
   winget install --interactive --exact dorssel.usbipd-win
   ```

   PASS: after the install finishes, a new PowerShell window recognizes the `usbipd` command.

7. In the Ubuntu (WSL) terminal, install [picocom](https://github.com/npat-efault/picocom), the terminal you will use for the serial console.

   ```bash
   sudo apt install -y picocom
   ```

## Part 2: Get the build tool and the board's layer

The board is supported by the community-maintained [`meta-qcom-3rdparty`](https://github.com/qualcomm-linux/meta-qcom-3rdparty) Yocto layer, built with the [kas](https://kas.readthedocs.io/en/latest/) tool through its `kas-container` wrapper. Everything in this part happens inside the Ubuntu (WSL) terminal.

1. Create the workspace directory and enter it.

   ```bash
   mkdir -p ~/qli && cd ~/qli
   ```

   > Info: Keep the workspace inside the WSL filesystem (under `~`), not under `/mnt/c`. Building on the Windows-mounted filesystem is much slower.

2. Download the `kas-container` wrapper script, pinned to kas 5.4.

   ```bash
   wget https://raw.githubusercontent.com/siemens/kas/refs/tags/5.4/kas-container && chmod +x kas-container
   ```

3. Verify that the script runs.

   ```bash
   ./kas-container --help
   ```

   PASS: the output shows usage text that includes a `build` command.

   If it fails with a Python or shell error, delete the file and repeat the download step.

4. Clone the board-support layer and enter it.

   ```bash
   git clone https://github.com/qualcomm-linux/meta-qcom-3rdparty.git && cd meta-qcom-3rdparty
   ```

   > Info: This tutorial was written against commit `dea38dcd9b1e` of the `main` branch. If a later `main` breaks the build, you can reproduce the state this page describes with `git checkout dea38dcd9b1e`.

5. Verify that the board's build configuration exists.

   ```bash
   ls ci/radxa-dragon-q6a.yml ci/qcom-distro.yml
   ```

   PASS: both file names are printed with no `No such file or directory` error.

   If either file is missing, you are on the wrong branch or in the wrong directory; run `pwd` (expect `/home/<user>/qli/meta-qcom-3rdparty`) and `git branch --show-current` (expect `main`).

## Part 3: Build the image

You will build `qcom-multimedia-image` for the `radxa-dragon-q6a` machine, with SSH login enabled at build time. SSH is off by default in this image and cannot be turned on afterwards without rebuilding, which is why it is added now.

1. Confirm you are in the layer's root directory.

   ```bash
   pwd
   ```

   PASS: the output is `/home/<your user>/qli/meta-qcom-3rdparty`.

   > Warning: `kas-container` resolves configuration paths relative to the directory you run it from. If you later see `configuration file not found`, you ran it from the wrong directory, not a broken checkout. Return to this directory and try again.

2. Create a kas overlay file that enables the SSH server in the image.

   ```bash
   cat > ssh.yml << 'EOF'
   header:
     version: 14

   local_conf_header:
     enable-ssh: |
       EXTRA_IMAGE_FEATURES += "ssh-server-openssh"
   EOF
   ```

3. Verify the overlay file contents.

   ```bash
   cat ssh.yml
   ```

   PASS: the output matches the block you pasted, including the `ssh-server-openssh` line.

4. Start the build. (Command pending validation; the configuration chain is the same one this repository's own CI builds for this board.)

   ```bash
   ../kas-container build ci/radxa-dragon-q6a.yml:ci/qcom-distro.yml:ssh.yml --target qcom-multimedia-image
   ```

   > Warning: If the container image pull is denied, run `docker logout` and retry. A logged-in Docker session has been observed to fail registry membership checks that anonymous pulls pass. Also, if you ever override the container image, the `KAS_CONTAINER_IMAGE` variable takes a full image path (for example `ghcr.io/siemens/kas/kas:5.4`), not a bare version tag.

5. Wait for the build to finish.

   > Info: What to expect while it runs. The first build fetches several other layer repositories automatically, takes roughly 80 minutes on a fast machine (pending validation), and will heavily load your CPU and disk. The task counter counts tasks as they are discovered, so the total grows while the build runs (for example `6000` growing toward `15000`); that is normal, not a restart. Do not start a second build in parallel. To check that a build is alive, run `pgrep -f bitbake` in another WSL terminal; a live build shows one or more process IDs.

   > Warning: Do not run `git pull` inside the layer directories that the build fetched (they appear next to `build/`). kas pins them to exact revisions; pulling mid-build corrupts the checkout. If the build fails partway, rerun the same build command; it resumes from cached state instead of starting over.

   PASS: the command exits without an error message. A red `ERROR:` block naming a failed task means the build failed; rerun the build command once, and if the same task fails again, report it on the [layer's issue tracker](https://github.com/qualcomm-linux/meta-qcom-3rdparty/issues) with the log file it names.

6. Verify that the build produced a compressed disk image.

   ```bash
   ls -lh build/tmp/deploy/images/radxa-dragon-q6a/*.wic.gz
   ```

   PASS: at least one `.wic.gz` file is listed, expected to be named like `qcom-multimedia-image-radxa-dragon-q6a.rootfs.wic.gz` (exact name pending validation).

   If the directory does not exist, list `build/tmp/deploy/images/` to see which machine directory was created, and confirm the build command used `ci/radxa-dragon-q6a.yml`. A build without that file produces an image for a different board that will not boot on the Dragon Q6A.

## Part 4: Flash the microSD card

The image is written to the microSD card from Windows with balenaEtcher. WSL cannot see USB SD-card readers, so do not try to flash from inside WSL.

1. In the Ubuntu (WSL) terminal, copy the image to a Windows-visible folder.

   ```bash
   mkdir -p /mnt/c/qli && cp build/tmp/deploy/images/radxa-dragon-q6a/*.wic.gz /mnt/c/qli/
   ```

2. Verify the copy.

   ```bash
   ls -lh /mnt/c/qli/
   ```

   PASS: the `.wic.gz` file is listed with the same size as in Part 3, step 6.

3. Plug the microSD card into the USB card reader, and the reader into the Windows PC.

4. Open balenaEtcher on Windows.

5. Click `Flash from file` and select the `.wic.gz` file in `C:\qli`.

   Etcher decompresses `.gz` images itself; do not extract the file first.

6. Click `Select target` and choose the entry whose size matches your microSD card.

   > Warning: Double-check the target. Etcher writes over the selected drive completely.

7. Click `Flash!` and wait until Etcher reports the flash and its validation as complete.

   PASS: Etcher shows a completed flash with no validation error.

   If validation fails, reseat the card in the reader and flash again; if it fails twice, try a different card or reader.

   > Info: After flashing, Windows may pop up dialogs asking to format the drive. Close them without formatting; Windows simply cannot read the Linux partitions it now sees.

8. Remove the card reader, and take the microSD card out of it.

## Part 5: Connect the serial console

You wire the serial console before first boot so you can see the boot logs from the first second. The board's debug UART is on the 40-pin header; details are on [Radxa's serial login page](https://docs.radxa.com/en/dragon/q6a/system-config/uart-debug).

1. With the board unpowered, connect three jumper wires from the 40-pin header to the USB-UART adapter: pin 6 (`GND`) to the adapter's `GND`, pin 8 (`TX`) to the adapter's `RXD`, and pin 10 (`RX`) to the adapter's `TXD`.

   TX and RX cross over: the board transmits into the adapter's receive line. Do not connect the adapter's `VCC` (red) wire to anything.

2. Plug the USB-UART adapter into the Windows PC.

3. Open PowerShell as administrator and list the USB devices to find the adapter's bus ID: the value in the `BUSID` column, such as `4-4`, on the row describing a USB serial device.

   ```powershell
   usbipd list
   ```

   Write the bus ID down; you will use it in the next two steps. If no serial device appears in the list, the adapter may need its driver installed; check the adapter vendor's driver page.

4. In the same administrator PowerShell window, share the adapter so WSL can use it (replace `<busid>` with the bus ID you wrote down). This is needed once per device.

   ```powershell
   usbipd bind --busid <busid>
   ```

   PASS: running `usbipd list` again shows the device's `STATE` as `Shared`.

5. Make sure the Ubuntu (WSL) terminal is open (attaching only works while WSL is running), then attach the adapter to WSL. This step no longer needs the administrator window.

   ```powershell
   usbipd attach --wsl --busid <busid>
   ```

   > Info: While attached, the adapter is invisible to Windows. If you unplug the adapter or reboot, run this attach command again before using the serial console. `usbipd detach --busid <busid>` hands the adapter back to Windows.

6. In the Ubuntu terminal, confirm the adapter arrived in WSL.

   ```bash
   ls /dev/ttyUSB*
   ```

   PASS: `/dev/ttyUSB0` is listed.

   If `ls` finds no `/dev/ttyUSB*` device, the attach did not take: run `usbipd list` in PowerShell and check the device state, then repeat the attach step.

## Part 6: Boot the board

1. In the Ubuntu terminal, open the serial console.

   ```bash
   sudo picocom -b 115200 /dev/ttyUSB0
   ```

   PASS: picocom prints `Terminal ready`. The console stays blank until the board powers on; that is expected. (When you want to leave picocom later, press `Ctrl-A` then `Ctrl-X`.)

2. Insert the microSD card into the microSD slot on the board itself.

   > Warning: The onboard microSD slot is the only boot medium that works for Qualcomm Linux on this board. A USB flash drive, or the microSD card inside a USB adapter, will not boot this image (Radxa OS boots from USB; Qualcomm Linux does not). Days were lost discovering this by elimination; do not repeat that experiment.

3. Connect the USB-C power adapter to the board's power port.

4. Watch the picocom terminal while the board boots.

   PASS: boot log lines stream in the picocom terminal within a few seconds of power-on.

   > Info: If a monitor is attached over HDMI, it shows about one second of logs and then goes black. That is the known behavior of this image, not a boot failure; the serial console keeps working.

   > Warning: If nothing at all appears in picocom: first check that the adapter is still attached to WSL (`usbipd list` in PowerShell; the attach drops on unplug or reboot), then swap the pin 8 and pin 10 wires (crossed TX/RX is the most common mistake), then re-check the device path and the `115200` speed. If the board still shows no serial output on a known-good wiring and a known-good image, the boot firmware may need recovery: follow Radxa's [Entering EDL Mode](https://docs.radxa.com/en/dragon/q6a/low-level-dev/edl-mode) page (hold the EDL button, power on, connect the USB A-to-A cable to the board's blue USB 3 Type-A port; a correctly entered device shows USB ID `05c6:9008`) and then [Flashing SPI Boot Firmware](https://docs.radxa.com/en/dragon/q6a/low-level-dev/spi-fw). Return here and boot again when the SPI firmware is restored.

5. Wait until the log stream ends in a login prompt.

   The prompt is expected to look like the following (exact text pending validation):

   ```text
   radxa-dragon-q6a login:
   ```

   If the log stream stalls for more than five minutes with no login prompt, power-cycle the board once. If it stalls at the same point again, the image is suspect: reflash the card (Part 4) and, if that does not help, rebuild (Part 3) before suspecting the hardware.

## Final Check

1. At the login prompt in picocom, type `root` and press `Enter`.

   This image is built with an empty root password, so no password prompt is expected; if one appears, press `Enter` at it.

2. Verify that you have a working shell on the board.

   ```bash
   uname -a
   ```

   PASS: the output starts with `Linux` and contains `aarch64`.

3. Confirm what you are running.

   ```bash
   cat /etc/os-release
   ```

   PASS: the file prints distribution fields including a `BUILD_ID` (exact contents pending validation).

   > Info: Do not be alarmed if the OS identifies itself with OpenEmbedded rather than a "Qualcomm Linux" brand string. Qualcomm Linux images are OpenEmbedded/Yocto builds, and the branding in `/etc/os-release` does not mean you installed the wrong OS.

You now have Qualcomm Linux, built from source for the Radxa Dragon Q6A, booting from microSD with a root shell over the serial console.

> Warning: This image allows root login with no password, and you enabled the SSH server at build time. Do not connect the board to an untrusted network in this state.

## Part 7 (optional): Log in over SSH

Follow this part when you want a network shell instead of the serial console, and the board is connected to your network with an Ethernet cable. Otherwise skip it; the serial console from the Final Check is complete on its own. (This whole part is pending validation.)

1. In the serial console, read the board's IP address.

   ```bash
   ip -4 addr show eth0
   ```

   Write down the address after `inet` (for example `192.168.1.42`). If there is no `inet` line, check the Ethernet cable and your router's DHCP.

2. In the Ubuntu (WSL) terminal on the PC, connect to the address you wrote down (replace it in the command before running).

   ```bash
   ssh root@192.168.1.42
   ```

   PASS: you get a shell prompt on the board.

   If the connection is refused, the running image was built without the `ssh.yml` overlay from Part 3, step 2; rebuild and reflash with it. If the connection times out, the PC and board are not on the same network.

## Next steps

- The [`meta-qcom-3rdparty` layer](https://github.com/qualcomm-linux/meta-qcom-3rdparty) is where this board's machine configuration lives; use its issue tracker for build problems.
- [Radxa's Dragon Q6A documentation](https://docs.radxa.com/en/dragon/q6a) covers the board hardware: pinouts, EDL recovery, and SPI boot firmware.
- To change what is in the image (packages, features, other image targets such as `qcom-console-image`), start from the [Yocto Project documentation on images and IMAGE_FEATURES](https://docs.yoctoproject.org/ref-manual/features.html#image-features).
