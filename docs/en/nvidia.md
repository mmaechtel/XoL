## [Nvidia Driver](../glossary.md#nvidia-driver) Installation on Debian from the Official Website

Installing [Nvidia Driver](../glossary.md#nvidia-driver) directly from the official Nvidia website is another option to support Nvidia graphics cards on Debian - especially for the latest driver version. This article describes the process precisely, uses `systemctl set-default` for switching between non-graphical and graphical mode, and addresses the use of the [Liquorix Kernel](../glossary.md#liquorix-kernel).

## Prerequisites
- Compatible Nvidia graphics card
- Debian installed and updated
- Optional: Liquorix kernel (if used)
- Root or sudo rights

## Step 1: Update System
Update the system:
```bash
sudo apt update && sudo apt upgrade -y
```

## Step 2: Install Dependencies
For the standard Debian kernel, install kernel headers and build tools:
```bash
sudo apt install linux-headers-$(uname -r) build-essential dkms
```
**Note on [Liquorix Kernel](../glossary.md#liquorix-kernel)**: If you're using the Liquorix kernel (an optimized kernel variant for performance), the kernel headers are already available through the Liquorix package sources after installing the kernel. Check with `uname -r` if the Liquorix kernel is active (e.g., `6.6.0-1-liquorix-amd64`). In this case, you only need to ensure that [DKMS](../glossary.md#dkms-dynamic-kernel-module-support) is installed, as the Nvidia driver needs it to dynamically compile the kernel module:
```bash
sudo apt install dkms
```

## Step 3: Download Nvidia Driver
1. Visit [https://www.nvidia.com/Download/index.aspx](https://www.nvidia.com/Download/index.aspx).
2. Select your graphics card, "Linux 64-bit" and the driver version.
3. Download the `.run` file (e.g., `NVIDIA-Linux-x86_64-550.54.14.run`) to your home directory (`/home/user`).

## Step 4: Switch to Non-Graphical Mode
Switch to non-graphical mode using `systemctl`:
1. Change the default boot target:
```bash
sudo systemctl set-default multi-user.target
```
2. Reboot the system:
```bash
sudo reboot
```
The system boots into a text console without graphical interface.

## Step 5: Perform Driver Installation
1. Navigate to the `.run` file:
```bash
cd /home/user
```
2. Make the file executable:
```bash
chmod +x NVIDIA-Linux-x86_64-550.54.14.run
```
3. Start the installation:
```bash
sudo ./NVIDIA-Linux-x86_64-550.54.14.run
```
4. Follow the installation wizard:
   - Accept the license.
   - Choose "Yes" for 32-bit compatibility libraries if needed.
   - Confirm disabling the [Nouveau](../glossary.md#nouveau) driver when asked.
**Liquorix Kernel**: Thanks to `dkms`, the Nvidia module is automatically compiled for the Liquorix kernel and updated during kernel updates.

## Step 6: Verify Installation
Check the driver:
```bash
nvidia-smi
```
An output with GPU details confirms successful installation.

## Step 7: Switch Back to Graphical Mode
Reset the default boot target:
```bash
sudo systemctl set-default graphical.target
```
Reboot again:
```bash
sudo reboot
```

## Troubleshooting
- **Black Screen**: If graphical mode doesn't start, add `nouveau.modeset=0` in `/etc/default/grub` under `GRUB_CMDLINE_LINUX_DEFAULT` and run `sudo update-grub`.
- **Missing Dependencies**: For standard kernels, check `linux-headers-$(uname -r)`; for Liquorix kernel, ensure `dkms` is present. 