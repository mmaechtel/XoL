# Official Nvidia Driver

Debian provides NVIDIA drivers through its package manager — the recommended method for most users. For those who need the very latest driver version, NVIDIA also offers a manual installer (`.run` file) as an alternative.

This page covers both approaches and includes notes for [Liquorix kernel](../glossary.md#liquorix-kernel) users.

## Prerequisites

- Compatible Nvidia graphics card
- Debian installed and updated
- Root or sudo rights
- For the package manager method: `non-free` and `non-free-firmware` components enabled in `/etc/apt/sources.list`
- Optional: Liquorix kernel (if used)

## Recommended: Package Manager

The simplest and most reliable method. Debian's packaged driver integrates with DKMS, initramfs, and Secure Boot automatically.

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install nvidia-driver
```

After installation, reboot the system. Verify with:

```bash
nvidia-smi
```

For details and troubleshooting, see the [Debian Wiki: NvidiaGraphicsDrivers](https://wiki.debian.org/NvidiaGraphicsDrivers/).

## Alternative: Manual Installation (.run File)

Use this method only if the Debian-packaged driver is too old or causes problems with specific hardware.

### System Preparation

The system is updated:

```bash
sudo apt update && sudo apt upgrade -y
```

For the standard Debian kernel, kernel headers and build tools are installed:

```bash
sudo apt install linux-headers-$(uname -r) build-essential dkms
```

**Note on [Liquorix kernel](../glossary.md#liquorix-kernel)**: The Liquorix kernel headers are a separate package that must be installed explicitly. [DKMS](../glossary.md#dkms-dynamic-kernel-module-support) is recommended so the NVIDIA module is automatically recompiled on kernel updates:

```bash
sudo apt install linux-headers-liquorix-amd64 dkms
```

Use `uname -r` to verify the active kernel — the output should contain `liquorix`.

### Driver Installation

1. Visit [https://www.nvidia.com/Download/index.aspx](https://www.nvidia.com/Download/index.aspx)
2. Select the graphics card, "Linux 64-bit", and the driver version
3. Download the `.run` file (e.g., `NVIDIA-Linux-x86_64-<VERSION>.run`) to the home directory

Switch to non-graphics mode using `systemctl`:

1. Change the default boot target:

```bash
sudo systemctl set-default multi-user.target
```

2. Restart the system:

```bash
sudo reboot
```

The system boots into a text console without a graphical interface.

Navigate to the `.run` file and make it executable:

```bash
chmod +x NVIDIA-Linux-x86_64-*.run
```

Start the installation:

```bash
sudo ./NVIDIA-Linux-x86_64-*.run
```

Follow the installation wizard:

- Accept the license
- Choose "Yes" for 32-bit compatibility libraries if needed
- Confirm disabling the [Nouveau](../glossary.md#nouveau) driver when asked
- When prompted about DKMS registration, accept the default ("Yes")

### Verify Installation

Check the driver:

```bash
nvidia-smi
```

An output with GPU details confirms successful installation.

### Return to Graphics Mode

Reset the default boot target:

```bash
sudo systemctl set-default graphical.target
```

Restart the system again:

```bash
sudo reboot
```

## Troubleshooting

- **Black Screen**: The `.run` installer automatically blacklists the Nouveau driver via `/etc/modprobe.d/`. If the graphical mode still does not start (e.g., because Nouveau is embedded in the initramfs), add `nouveau.modeset=0` to `/etc/default/grub` under `GRUB_CMDLINE_LINUX_DEFAULT` and run `sudo update-grub`.
- **Missing Dependencies**: For standard kernels, check `linux-headers-$(uname -r)`; for the Liquorix kernel, ensure both `linux-headers-liquorix-amd64` and `dkms` are installed.

## Performance Optimization

### Driver Settings (X11 Only)

On X11, the `nvidia-settings` tool offers composition options that can reduce screen [tearing](../glossary.md#tearing). These settings are **not available and not needed on [Wayland](../displayserver_wayland.md)**, where the compositor handles this natively.

```bash
nvidia-settings
```

Under "X Server Display Configuration" → "Advanced":

- **Force Full Composition Pipeline**: Prevents tearing by routing all display output through the GPU's composition engine. May increase input latency — test individually.
- **Force Composition Pipeline**: Similar but less aggressive. Prevents most tearing artifacts with less latency impact.

These settings are optional. Only enable them if tearing is actually visible during gameplay. They can be disabled at any time if performance issues occur.

### Kernel Parameters

When using the `.run` installer, `nvidia-drm.modeset=1` is **not** enabled by default and must be set manually. This parameter enables [kernel mode setting (KMS)](../glossary.md#drmkms-direct-rendering-manager-kernel-mode-setting) for NVIDIA, which is required for Wayland and improves display handling.

Add to `/etc/default/grub` under `GRUB_CMDLINE_LINUX_DEFAULT`:

```
nvidia-drm.modeset=1
```

Then update [GRUB](../glossary.md#grub-grand-unified-bootloader):

```bash
sudo update-grub
```

Verify the current setting:

```bash
cat /sys/module/nvidia_drm/parameters/modeset
```

A value of `Y` confirms KMS is active.

!!! note "Package manager installation"
    When installing via `apt install nvidia-driver`, Debian may configure modeset automatically through `/etc/modprobe.d/`. Check the current value before adding a GRUB parameter.

### MangoHud (Optional)

For advanced performance monitoring beyond X-Plane's built-in [FPS](../glossary.md#fps-frames-per-second) display (Ctrl+Shift+F):

```bash
sudo apt install mangohud
```

MangoHud provides detailed GPU/CPU metrics, frame time graphs, and [VRAM](../glossary.md#vram-video-ram) usage as an in-game overlay. See [System Tuning](../systemtuning.md) and [System Monitoring](../systemtools.md) for further performance analysis.

---

## Sources

- [Debian Wiki: NvidiaGraphicsDrivers](https://wiki.debian.org/NvidiaGraphicsDrivers/) — Official Debian NVIDIA installation guide
- [NVIDIA Driver Download](https://www.nvidia.com/Download/index.aspx) — Official driver download page
- [NVIDIA Driver README: KMS](https://download.nvidia.com/XFree86/Linux-x86_64/580.126.09/README/kms.html) — Kernel mode setting documentation
- [Arch Wiki: NVIDIA](https://wiki.archlinux.org/title/NVIDIA) — Comprehensive NVIDIA configuration reference
