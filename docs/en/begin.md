# Getting Started with X-Plane on Linux

This guide covers system requirements, X-Plane installation, and initial setup. For background on why Linux is a strong platform for X-Plane, see [Introduction](intro.md).

## System Requirements

X-Plane 12 requires significant system resources, especially for realistic simulations at high resolutions. A fast CPU with good single-core *and* multi-core performance is ideal.

### Recommended Requirements

- **CPU**: Current generation with high single-core and multi-core performance (Intel Core i7/i9 or AMD Ryzen 7/9)
- **RAM**: 32 GB or more
- **Graphics Card**: High-performance GPU with at least 8 GB [VRAM](../glossary.md#vram-video-ram) (e.g., NVIDIA RTX 3080/4080 or higher)
- **Storage Space**: 250 GB or more SSD storage ([NVMe](../glossary.md#nvme-non-volatile-memory-express) recommended)
- **Network**: Fast internet connection for ortho streaming and map updates

??? info "Why these specifications?"

    - **CPU**: X-Plane benefits from fast single-core speed and distributes rendering work across multiple cores. These recommendations target addon-heavy setups with [orthophotos](../glossary.md#orthophotos) — Laminar Research's official minimum is lower (e.g., Intel i5-12600K).
    - **RAM**: Memory-hungry addons, detailed scenery, and orthophotos can dramatically increase RAM usage.
    - **GPU**: Especially for 4K resolution or multi-monitor setups, high-resolution textures and complex lighting effects challenge even high-end GPUs.
    - **Storage**: The base installation requires about 25 GB, a full install with all scenery regions around 75–80 GB. Orthophotos can quickly add hundreds of GB on top. SSD speed reduces loading times during flight.
    - **Network**: Real-time data such as weather and air traffic, as well as streaming orthophotos, require a reliable connection.

### Hardware Optimizations

- SSD/NVMe drive for operating system and X-Plane installation
- Dedicated graphics card with current drivers
- Multiple monitors for extended cockpit setup
- Good cooling system, as X-Plane heavily loads CPU and GPU

??? tip "Debian Linux Installation"

    This documentation assumes a working Debian installation in the current Stable version with a functional graphical user interface. If Debian still needs to be installed:

    **Official Installation Sources**

    - [Debian Main Server](https://www.debian.org/) — Always the current Stable version
    - [Worldwide Debian Mirror Servers](https://www.debian.org/mirror/list) — Choose a server near you for faster downloads
    - [Debian Network Installation](https://www.debian.org/distrib/netinst) — Minimal ISO for network installation (recommended)

    **Choosing the Right Version**

    - Always use the current **Stable** version of Debian for maximum stability
    - The Stable version is prominently displayed on the [Debian main page](https://www.debian.org/)
    - For X-Plane performance, always choose the 64-bit version (amd64)

    **Installation Tips**

    - Any major desktop environment works with X-Plane. "GNOME" or "KDE Plasma" are recommended for newcomers due to large community support and mature [Wayland](../glossary.md#wayland) integration
    - When partitioning, configure swap space: approximately 4 GB is sufficient without hibernation, or equal to your RAM size if you plan to use hibernation
    - Set up separate partitions for `/` (root, at least 30 GB) and `/home` (remaining space)
    - Install the [GRUB](../glossary.md#grub-grand-unified-bootloader) bootloader on the main drive

    **After Installation**

    1. Fully update the system:
        ```bash
        sudo apt update && sudo apt upgrade -y
        ```

    2. Install important base packages:
        ```bash
        sudo apt install build-essential dkms git curl wget nano
        ```

## Installing X-Plane 12 on Linux

X-Plane 12 is available both through Steam and directly from Laminar Research.

### Steam

This documentation focuses on the standalone installation. All described optimizations can be applied 1:1 to a Steam installation — only the paths need to be adjusted to match Steam's directory structure (typically `~/.steam/steam/steamapps/common/X-Plane 12/`).

### Standalone Version (Laminar Research)

The standalone version provides:

- Full control over installation directory and options
- Direct updates via the X-Plane updater without third parties
- Easy backups and migration to other computers
- Unrestricted access to files for modifications

**Installation steps:**

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
    - In the graphical installer, select:
        - Installation directory (recommended: `/home/[username]/X-Plane 12/`)
        - Scenery packages to load
        - World coverage (select at least your main flying area)

4. **Download process**
    - The installer downloads the selected content (25–80 GB depending on scenery selection)
    - This process can take several hours
    - The download can be interrupted and resumed later

### After Installation

1. **First launch**: Start X-Plane once and close it again so that configuration files are created

2. **Optimize performance settings**: Adjust graphics settings according to your hardware. See [X-Plane Configuration](xplane/config.md) for Linux-specific guidance.

3. **Check the performance** with the built-in [FPS](../glossary.md#fps-frames-per-second) display (activate with `Shift+Ctrl+F`)

??? note "Troubleshooting: Library Dependencies (ldd)"

    If X-Plane doesn't start or crashes unexpectedly, it might be due to missing libraries. Check dependencies with [ldd](../glossary.md#ldd):

    ```bash
    cd ~/X-Plane\ 12/
    ldd X-Plane-x86_64
    ```

    Look for lines marked `not found`:

    ```
    libvulkan.so.1 => not found
    ```

    **Common Missing Dependencies**

    | Library | Package | Installation Command |
    |---------|---------|----------------------|
    | libvulkan.so.1 | libvulkan1 | `sudo apt install libvulkan1` |
    | libGL.so.1 | libgl1 | `sudo apt install libgl1` |
    | libX11.so.6 | libx11-6 | `sudo apt install libx11-6` |
    | libasound.so.2 | libasound2 | `sudo apt install libasound2` |
    | libpulse.so.0 | libpulse0 | `sudo apt install libpulse0` |

    For full Vulkan support (required):

    ```bash
    sudo apt install libvulkan1 mesa-vulkan-drivers vulkan-tools
    ```

    For audio support:

    ```bash
    sudo apt install libasound2 libasound2-plugins libpulse0
    ```

    After installing missing libraries, restart X-Plane.

### Troubleshooting

If problems occur:

- **X-Plane doesn't start**: Check the log file at `~/X-Plane 12/Log.txt`
- **Poor performance**: Update graphics drivers and reduce graphics settings
- **Crashes**: Ensure all X-Plane files were downloaded correctly
- **Input devices not recognized**: Install `jstest-gtk` for diagnosis and calibration

For technical terms, consult the [Glossary](glossary.md).

## Next Steps

After a successful installation, continue with:

1. [Performance Fundamentals](performance_overview.md) — Understand the three load dimensions (CPU, I/O, network)
2. [NVIDIA Drivers](optimizations/nvidia.md) — Install and configure proprietary NVIDIA drivers
3. [Liquorix Kernel](optimizations/liquorix.md) — Low-latency kernel optimized for desktop workloads
4. [System Tuning](system/systemtuning.md) — CPU governor, interrupt shielding, and kernel parameters
5. [Display Server](optimizations/displayserver.md) — Wayland vs. X11 for X-Plane
6. [X-Plane Configuration](xplane/config.md) — Linux-specific graphics and performance settings
