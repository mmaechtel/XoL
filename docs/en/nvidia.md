## Official Nvidia Driver

The installation of [Nvidia drivers](../glossary.md#nvidia-driver) directly from the official Nvidia website is another option to support Nvidia graphics cards under Debian – especially for the latest driver version. This chapter describes the process precisely, uses `systemctl set-default` for switching between non-graphics and graphics mode, and covers the use of the [Liquorix kernel](../glossary.md#liquorix-kernel).

## Prerequisites

- Compatible Nvidia graphics card
- Debian installed and updated
- Optional: Liquorix kernel (if used)
- Root or sudo rights

## Installation

### System Preparation

The system is updated:
```bash
sudo apt update && sudo apt upgrade -y
```

For the standard Debian kernel, kernel headers and build tools are installed:
```bash
sudo apt install linux-headers-$(uname -r) build-essential dkms
```

**Note on [Liquorix kernel](../glossary.md#liquorix-kernel)**: When using the Liquorix kernel (an optimized kernel variant for performance), the kernel headers are already available through the Liquorix package sources after the kernel is installed. Use `uname -r` to check if the Liquorix kernel is active (e.g., `6.6.0-1-liquorix-amd64`). In this case, only ensure that [DKMS](../glossary.md#dkms-dynamic-kernel-module-support) is installed, as the Nvidia driver needs it to compile the kernel module dynamically:
```bash
sudo apt install dkms
```

### Driver Installation

1. Visit [https://www.nvidia.com/Download/index.aspx](https://www.nvidia.com/Download/index.aspx)
2. Select the graphics card, "Linux 64-bit", and the driver version
3. Download the `.run` file (e.g., `NVIDIA-Linux-x86_64-550.54.14.run`) to the home directory (`/home/user`)

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

Navigate to the `.run` file:
```bash
cd /home/user
```

Make the file executable:
```bash
chmod +x NVIDIA-Linux-x86_64-550.54.14.run
```

Start the installation:
```bash
sudo ./NVIDIA-Linux-x86_64-550.54.14.run
```

Follow the installation wizard:
- Accept the license
- Choose "Yes" for 32-bit compatibility libraries if needed
- Confirm disabling the [Nouveau](../glossary.md#nouveau) driver when asked

**Liquorix kernel**: Thanks to `dkms`, the Nvidia module is automatically compiled for the Liquorix kernel and updated with kernel updates.

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

- **Black Screen**: If the graphics mode doesn't start, add `nouveau.modeset=0` to `/etc/default/grub` under `GRUB_CMDLINE_LINUX_DEFAULT` and run `sudo update-grub`.
- **Missing Dependencies**: For standard kernels, check `linux-headers-$(uname -r)`; for the Liquorix kernel, ensure `dkms` is present.

## Performance Optimization

### Driver Settings

Start the NVIDIA settings program:
```bash
nvidia-settings
```

The program offers the following optional settings that can be tested as needed:
- Under "X Server Display Configuration" → "Advanced" → "Force Full Composition Pipeline":
    - This setting prevents tearing in games
    - May cause slightly increased latency
    - Recommended for games suffering from tearing
- Under "X Server Display Configuration" → "Advanced" → "Force Composition Pipeline":
    - Improves image quality and stability
    - May slightly increase GPU usage
    - Helps with screen refresh issues

**Note**: These settings are optional and may have different effects depending on the game and system configuration. It's recommended to test the settings individually and only enable those that actually provide improvement. If performance issues occur, the settings can be disabled at any time.

### Performance Modes

The performance mode can be optionally activated via the command line:
```bash
sudo nvidia-smi -pm 1
```

This setting keeps the GPU in a higher performance state, which improves response time but also increases power consumption. It can be particularly useful for:
- Games with high FPS requirements
- Applications that benefit from constant GPU performance
- Systems where GPU performance fluctuates

**Note**: The performance mode is not mandatory and should only be activated if performance fluctuations are actually noticed. For X-Plane, it can help if GPU performance is irregular or if FPS drops occur in certain situations.

### Kernel Parameters

In Debian 12, most NVIDIA optimizations are already enabled by default. If manual adjustments are still desired, the following parameters can be added to `/etc/default/grub` under `GRUB_CMDLINE_LINUX_DEFAULT`:
```bash
nvidia-drm.modeset=1
```

This parameter enables the Direct Rendering Manager (DRM) for NVIDIA. It enables:
- Better integration with the Linux graphics stack
- Improved Wayland support
- Optimized screen refresh
- Better handling of multi-monitor setups

Then update GRUB:
```bash
sudo update-grub
```

**Note**: Most of these parameters are already configured by default in Debian 12. Manual adjustment is only necessary in rare cases, e.g., for specific performance issues or if screen refresh problems occur.

### Additional Optimizations

**MangoHud** (optional): For advanced performance monitoring features:
```bash
sudo apt install mangohud
```

**Note**: X-Plane already offers a built-in FPS display (Ctrl+Shift+F). MangoHud is only necessary if additional monitoring features are needed.

### Important Notes

- Performance may vary depending on system configuration
- Regular driver updates can improve performance
- Settings in the NVIDIA settings program (`nvidia-settings`) may vary depending on driver version and system configuration 