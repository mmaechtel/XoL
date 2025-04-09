# Getting Started with X-Plane on Linux

This guide will walk you through the first steps to optimally set up X-Plane on Linux. It is aimed at Linux-experienced users and builds on an existing Linux installation.

## System Requirements

X-Plane 12 is a demanding flight simulator that requires significant system resources, especially for realistic simulations at high resolutions. Unlike many other applications, X-Plane heavily utilizes single-core performance and places high demands on the graphics card.

### Recommended Requirements
- **CPU**: Current generation with high single-core performance (Intel Core i7/i9 or AMD Ryzen 7/9)
    - *Why?* X-Plane primarily uses one CPU core for flight physics calculations. High single-core speed is crucial for smooth framerates.
  
- **RAM**: 32 GB or more
    - *Why?* Memory-hungry addons, detailed scenery, and orthophotos can dramatically increase RAM usage.
  
- **Graphics Card**: High-performance GPU with at least 8 GB VRAM (e.g., NVIDIA RTX 3080/4080 or higher)
    - *Why?* Especially for 4K resolution or multi-monitor setups, you need substantial graphics power and VRAM. High-resolution textures and complex lighting effects challenge even high-end GPUs.
  
- **Storage Space**: 250 GB or more SSD storage (NVMe recommended)
    - *Why?* The base installation already requires about 70 GB, and orthophotos can quickly occupy hundreds of GB. SSD speed reduces loading times during flight.
  
- **Network**: Fast internet connection for ortho streaming and map updates
    - *Why?* Real-time data such as weather and air traffic, as well as streaming orthophotos, require a reliable connection.

### Hardware Optimizations
- SSD/NVMe drive for operating system and X-Plane installation
- Dedicated graphics card with current drivers
- Multiple monitors for extended cockpit setup
- Good cooling system, as X-Plane heavily loads CPU and GPU

*Note: Even when following these recommendations, be aware that due to its single-core limitation, X-Plane may have performance constraints even on high-end hardware. The recommended optimizations in this documentation help to get the most out of your existing hardware.*

## Installing Debian Linux

This documentation assumes that you have already installed Debian Linux in the current Stable version and are working with a functional graphical user interface. If you still need to install Debian, here are the most important resources:

### Official Installation Sources
- [Debian Main Server](https://www.debian.org/) - Here you'll always find the current Stable version
- [Worldwide Debian Mirror Servers](https://www.debian.org/mirror/list) - Choose a server near you for faster downloads
- [Debian Network Installation](https://www.debian.org/distrib/netinst) - Minimal ISO for network installation (recommended)

### Choosing the Right Version
- Always use the current **Stable** version of Debian for maximum stability
- The Stable version is prominently displayed on the [Debian main page](https://www.debian.org/)
- For X-Plane performance, always choose the 64-bit version (amd64)

### Installation Tips
- During installation, choose the desktop environment "GNOME" or "KDE Plasma" for best compatibility
- When partitioning, activate swap space of at least half your RAM size (e.g., 16 GB swap for 32 GB RAM)
- Set up separate partitions for `/` (root, at least 100 GB) and `/home` (remaining space)
- Install the GRUB bootloader on the main drive

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

X-Plane 12 runs natively on Linux and, unlike many other games and simulators, doesn't require a compatibility layer like Wine or Proton. Here are the steps for installation:

### Preparations
Before installing X-Plane 12, you should make the following preparations:

1. **Update graphics drivers** - For Nvidia GPUs, install the current proprietary driver:
   ```bash
   sudo apt install nvidia-driver
   ```
   *For more details, see the chapter [Nvidia Drivers](nvidia.md).*

2. **Install OpenGL libraries**:
   ```bash
   sudo apt install libgl1-mesa-glx libgl1-mesa-dri
   ```

3. **Ensure audio components**:
   ```bash
   sudo apt install pulseaudio pavucontrol
   ```

### Installation Methods

X-Plane 12 is available both through Steam and directly from developer Laminar Research. While the Steam version may be convenient for beginners, in this documentation we focus on the standalone version, which offers more control and flexibility.

#### Standalone Version (direct download from Laminar Research)

Direct installation of X-Plane offers numerous advantages for experienced users:

1. **Download X-Plane**
   - Visit the [official X-Plane website](https://www.x-plane.com/)
   - Purchase X-Plane 12 (or download the demo version)
   - Download the installer (approximately 1 GB)

2. **Prepare the installer**
   - Navigate to the download folder:
     ```bash
     cd ~/Downloads
     ```
   - Make the installer executable:
     ```bash
     chmod +x X-Plane-installer.run
     ```

3. **Start installation**
   - Run the installer:
     ```bash
     ./X-Plane-installer.run
     ```
   - In the graphical installer, you can select:
     - Installation directory (recommended: `/home/[username]/X-Plane 12/`)
     - Scenery packages to load
     - World coverage (select at least your main flying area)

4. **Download process**
   - The installer downloads the selected content (70-150 GB depending on selection)
   - This process can take several hours
   - The download can be interrupted and resumed later

**Advantages of the standalone version:**
- Full control over installation directory and options
- Direct updates via the X-Plane updater without third parties
- Often faster updates for new versions
- Easy backups and migration to other computers
- Unrestricted access to files for modifications

### After Installation

After successful installation, you should perform the following steps:

1. **First launch**: Start X-Plane once and close it again so that configuration files are created

2. **Optimize performance settings**:
   - Start X-Plane
   - Go to "Settings" > "Graphics"
   - Adjust settings according to your hardware:
     - For higher FPS: Reduce visibility and object details
     - For better quality: Increase texture quality and anti-aliasing
     - Activate the Vulkan rendering API for better performance

3. **Save a custom graphics profile** for different scenarios (flight training, photography, etc.)

4. **Check the performance** with the built-in FPS display (activate with `Shift+Ctrl+F`)

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
   sudo apt install libvulkan1 mesa-vulkan-drivers vulkan-utils
   ```

2. **Example: Missing audio libraries**:
   ```bash
   sudo apt install libasound2 libasound2-plugins libpulse0
   ```

3. **Example: Missing OpenGL libraries**:
   ```bash
   sudo apt install libgl1-mesa-glx libgl1-mesa-dri
   ```

4. **Example: [32-Bit Compatibility](../glossary.md#32-bit-compatibility) (if necessary)**:
   ```bash
   sudo dpkg --add-architecture i386
   sudo apt update
   sudo apt install libgl1-mesa-glx:i386 libvulkan1:i386
   ```

#### Common Missing Dependencies

| Library | Package | Installation Command |
|---------|---------|----------------------|
| libvulkan.so.1 | libvulkan1 | `sudo apt install libvulkan1` |
| libGL.so.1 | libgl1-mesa-glx | `sudo apt install libgl1-mesa-glx` |
| libX11.so.6 | libx11-6 | `sudo apt install libx11-6` |
| libasound.so.2 | libasound2 | `sudo apt install libasound2` |
| libpulse.so.0 | libpulse0 | `sudo apt install libpulse0` |

After installing missing libraries, you should restart X-Plane. In most cases, this will resolve startup issues caused by missing dependencies.

### Troubleshooting X-Plane Installation

If problems occur:

- **X-Plane doesn't start**: Check the log file at `~/X-Plane 12/Log.txt`
- **Poor performance**: Update graphics drivers and reduce graphics settings
- **Crashes**: Ensure all X-Plane files were downloaded correctly
- **Input devices not recognized**: Install `jstest-gtk` for diagnosis and calibration

## Installation Issues

If you encounter problems, the following steps may help:

- Check GPU driver compatibility
- Make sure all Linux packages are up to date
- Verify X-Plane system requirements on the official website
- Consult the [Glossary](glossary.md) for technical terms

Depending on the hardware and Linux distribution you use, specific adjustments may be necessary. The examples shown here have been tested with Debian but work with minor changes on other distributions. 