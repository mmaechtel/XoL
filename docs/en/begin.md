# Getting Started with X-Plane on Linux

This guide will walk you through the first steps to optimally set up X-Plane on Linux. It is aimed at Linux-experienced users and builds on an existing Linux installation.

## System Requirements

X-Plane 12 is a demanding flight simulator that requires significant system resources, especially for realistic simulations at high resolutions. While single-core performance remains important, X-Plane 12 distributes substantial per-frame work across multiple cores. A fast CPU with good single-core *and* multi-core performance is ideal.

### Recommended Requirements

- **CPU**: Current generation with high single-core and multi-core performance (Intel Core i7/i9 or AMD Ryzen 7/9)
    - *Why?* X-Plane benefits from fast single-core speed and distributes rendering work across multiple cores. These recommendations target addon-heavy setups with [orthophotos](../glossary.md#orthophotos) — Laminar Research's official minimum is lower (e.g., Intel i5-12600K).
  
- **RAM**: 32 GB or more
    - *Why?* Memory-hungry addons, detailed scenery, and orthophotos can dramatically increase RAM usage.
  
- **Graphics Card**: High-performance GPU with at least 8 GB [VRAM](../glossary.md#vram-video-ram) (e.g., NVIDIA RTX 3080/4080 or higher)
    - *Why?* Especially for 4K resolution or multi-monitor setups, you need substantial graphics power and VRAM. High-resolution textures and complex lighting effects challenge even high-end GPUs.
  
- **Storage Space**: 250 GB or more SSD storage ([NVMe](../glossary.md#nvme-non-volatile-memory-express) recommended)
    - *Why?* The base installation requires about 25 GB, a full install with all scenery regions around 75–80 GB. Orthophotos can quickly add hundreds of GB on top. SSD speed reduces loading times during flight.
  
- **Network**: Fast internet connection for ortho streaming and map updates
    - *Why?* Real-time data such as weather and air traffic, as well as streaming orthophotos, require a reliable connection.

### Hardware Optimizations

- SSD/NVMe drive for operating system and X-Plane installation
- Dedicated graphics card with current drivers
- Multiple monitors for extended cockpit setup
- Good cooling system, as X-Plane heavily loads CPU and GPU

*Note: Even with high-end hardware, X-Plane can be demanding. The recommended optimizations in this documentation help to get the most out of your existing system.*

## Installing Debian Linux

This documentation assumes that you have already installed Debian Linux in the current Stable version and are working with a functional graphical user interface. If you still need to install Debian, here are the most important resources:

### Official Installation Sources

- [Debian Main Server](https://www.debian.org/) — Here you'll always find the current Stable version
- [Worldwide Debian Mirror Servers](https://www.debian.org/mirror/list) — Choose a server near you for faster downloads
- [Debian Network Installation](https://www.debian.org/distrib/netinst) — Minimal ISO for network installation (recommended)

### Choosing the Right Version

- Always use the current **Stable** version of Debian for maximum stability
- The Stable version is prominently displayed on the [Debian main page](https://www.debian.org/)
- For X-Plane performance, always choose the 64-bit version (amd64)

### Installation Tips

- Any major desktop environment works with X-Plane. "GNOME" or "KDE Plasma" are recommended for newcomers due to large community support and mature [Wayland](../glossary.md#wayland) integration
- When partitioning, configure swap space: approximately 4 GB is sufficient without hibernation, or equal to your RAM size if you plan to use hibernation
- Set up separate partitions for `/` (root, at least 30 GB) and `/home` (remaining space)
- Install the [GRUB](../glossary.md#grub-grand-unified-bootloader) bootloader on the main drive

### After Installation

After successful installation and login to the graphical user interface, the following steps are recommended:

1. Fully update the system:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. Install important base packages:
   ```bash
   sudo apt install build-essential dkms git curl wget nano
   ```

The following chapters of this documentation assume a working Debian installation and focus on optimization for X-Plane.

## Installing X-Plane 12 on Linux

X-Plane 12 is available both through Steam and directly from developer Laminar Research. While the Steam version may be convenient for beginners, in this documentation we focus on the standalone version, which offers more control and flexibility.

### Installation Methods

#### Standalone Version (direct download from Laminar Research)

Direct installation of X-Plane offers numerous advantages for experienced users:

1. **Download X-Plane**
    - Visit the [official X-Plane website](https://www.x-plane.com/)
    - Purchase X-Plane 12 (or download the demo version)
    - Download the Linux installer (`X-Plane12InstallerLinux.zip`, approximately 25 MB)

2. **Prepare the installer**
    - Navigate to the download folder and extract:
        ```bash
        cd ~/Downloads
        unzip X-Plane12InstallerLinux.zip
        ```
    - Make the installer executable (if needed):
        ```bash
        chmod +x "X-Plane 12 Installer Linux"
        ```

3. **Start installation**
    - Run the installer:
        ```bash
        ./"X-Plane 12 Installer Linux"
        ```
    - In the graphical installer, you can select:
        - Installation directory (recommended: `/home/[username]/X-Plane 12/`)
        - Scenery packages to load
        - World coverage (select at least your main flying area)

4. **Download process**
    - The installer downloads the selected content (25–80 GB depending on scenery selection)
    - This process can take several hours
    - The download can be interrupted and resumed later

**Advantages of the standalone version**

- Full control over installation directory and options
- Direct updates via the X-Plane updater without third parties
- Often faster updates for new versions
- Easy backups and migration to other computers
- Unrestricted access to files for modifications

### After Installation

After successful installation, you should perform the following steps:

1. **First launch**: Start X-Plane once and close it again so that configuration files are created

2. **Optimize performance settings**: Adjust graphics settings according to your hardware. See the [X-Plane Configuration](xplane/config.md) page for detailed Linux-specific guidance.

3. **Check the performance** with the built-in [FPS](../glossary.md#fps-frames-per-second) display (activate with `Shift+Ctrl+F`)

### Checking Library Dependencies

If X-Plane doesn't start or crashes unexpectedly, it might be due to missing libraries. Linux provides a simple way to check dependencies with the [ldd](../glossary.md#ldd) tool:

#### Checking Dependencies with ldd

1. **Open a terminal** and navigate to the X-Plane directory:
   ```bash
   cd ~/X-Plane\ 12/
   ```

2. **Apply [ldd](../glossary.md#ldd) to the X-Plane executable**:
   ```bash
   ldd X-Plane-x86_64
   ```

3. **Analyze the output**:
    - Normal dependencies appear in the format: `libname.so => /path/to/libname.so`
    - Problematic dependencies show `not found` or are missing completely:
     ```
     libvulkan.so.1 => not found
     ```

#### Interpreting ldd Output

The [ldd](../glossary.md#ldd) output shows all [dynamic libraries](../glossary.md#dynamic-libraries) that X-Plane needs:

```
linux-vdso.so.1 (0x00007ffcb9192000)
libdl.so.2 => /lib/x86_64-linux-gnu/libdl.so.2 (0x00007f040d8e5000)
libpthread.so.0 => /lib/x86_64-linux-gnu/libpthread.so.0 (0x00007f040d8c6000)
libGL.so.1 => /usr/lib/x86_64-linux-gnu/libGL.so.1 (0x00007f040d83a000)
libvulkan.so.1 => not found
...
```

- **Found libraries**: Listed with complete path
- **Missing libraries**: Marked with `not found`
- **Dependencies of dependencies**: Also displayed

#### Resolving Missing Dependencies

1. **Example: Missing [Vulkan API](../glossary.md#vulkan-api) library**:
   ```bash
   sudo apt install libvulkan1 mesa-vulkan-drivers vulkan-tools
   ```

2. **Example: Missing audio libraries**:
   ```bash
   sudo apt install libasound2 libasound2-plugins libpulse0
   ```

3. **Example: Missing OpenGL libraries**:
   ```bash
   sudo apt install libgl1 libgl1-mesa-dri
   ```

4. **Example: [32-Bit Compatibility](../glossary.md#32-bit-compatibility) (rarely needed — only for certain third-party plugins or Wine-based tools)**:
   ```bash
   sudo dpkg --add-architecture i386
   sudo apt update
   sudo apt install libgl1:i386 libvulkan1:i386
   ```

#### Common Missing Dependencies

| Library | Package | Installation Command |
|---------|---------|----------------------|
| libvulkan.so.1 | libvulkan1 | `sudo apt install libvulkan1` |
| libGL.so.1 | libgl1 | `sudo apt install libgl1` |
| libX11.so.6 | libx11-6 | `sudo apt install libx11-6` |
| libasound.so.2 | libasound2 | `sudo apt install libasound2` |
| libpulse.so.0 | libpulse0 | `sudo apt install libpulse0` |

After installing missing libraries, you should restart X-Plane. In most cases, this will resolve startup issues caused by missing dependencies.

### Troubleshooting

If problems occur:

- **X-Plane doesn't start**: Check the log file at `~/X-Plane 12/Log.txt`
- **Poor performance**: Update graphics drivers and reduce graphics settings
- **Crashes**: Ensure all X-Plane files were downloaded correctly
- **Input devices not recognized**: Install `jstest-gtk` for diagnosis and calibration
- **General issues**: Check GPU driver compatibility, make sure all Linux packages are up to date, and verify X-Plane system requirements on the [official website](https://www.x-plane.com/)

Depending on the hardware and Linux distribution you use, specific adjustments may be necessary. The examples shown here have been tested with Debian but work with minor changes on other distributions. For technical terms, consult the [Glossary](glossary.md).

## Next Steps

After a successful installation, continue with the following topics:

- [NVIDIA Drivers](nvidia.md) — Install and configure proprietary NVIDIA drivers
- [Liquorix Kernel](liquorix.md) — Low-latency kernel optimized for desktop workloads
- [System Tuning](systemtuning.md) — CPU governor, interrupt shielding, and kernel parameters
- [Display Server](displayserver.md) — Wayland vs. X11 for X-Plane
- [X-Plane Configuration](xplane/config.md) — Linux-specific graphics and performance settings