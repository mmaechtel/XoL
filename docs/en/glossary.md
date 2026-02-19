---
title: Glossary
description: "Glossary of X-Plane and Linux terms — CPU governor, Vulkan, VRAM, Wayland, Mesa, kernel parameters, scenery formats, and more explained."
tags:
  - reference
---
# Glossary

## A

### Airport Enhancement Package (AEP)

A scenery addon by X-Codr Designs for X-Plane that enhances default airports with more detailed models, higher resolution textures, and new technologies. It replaces airport buildings, facades, ground objects, static vehicles, as well as runway lights, beacons, and navigation aids with modern versions. [More details](addon/scenery_addons/aep.md)

### Airport Elements

The various components of an airport in X-Plane, such as buildings, facades, ground objects, static vehicles, runway lights, beacons, and navigation aids. The [Airport Enhancement Package (AEP)](addon/scenery_addons/aep.md) enhances these elements with more detailed models and higher resolution textures.

### Airport Vegetation

The 3D vegetation elements on airports in X-Plane. In the [Airport Enhancement Package (AEP)](addon/scenery_addons/aep.md), the default airport vegetation is replaced with new, more detailed 3D models for a more realistic representation.

### ALSA (Advanced Linux Sound Architecture)

The standard audio subsystem in the Linux kernel that provides the interface between audio hardware and applications. ALSA provides device drivers on which higher audio layers like PulseAudio or PipeWire build. X-Plane does not use ALSA directly but communicates through FMOD with PulseAudio/PipeWire.

### APST (Autonomous Power State Transitions)

An NVMe power-saving feature that automatically transitions SSDs into low-power states. Can cause micro-stutters when the SSD needs to wake from deep sleep to load scenery data. For X-Plane, disabling via the kernel parameter `nvme_core.default_ps_max_latency_us=0` is recommended.

### ANV

The open-source Vulkan driver for Intel GPUs within the Mesa driver stack. ANV is the default Vulkan driver on Linux systems with Intel Arc and integrated Intel graphics and is used directly by X-Plane 12.

### Autogen

Automatically generated 3D objects (buildings, vegetation) in X-Plane placed based on land use data. Autogen fills the landscape outside hand-modeled airports and cities. Density is controlled in X-Plane's graphics settings via "Objects".

### AutoOrtho

A tool for X-Plane that integrates orthophotos directly into the flight simulator. It enables streaming of high-resolution aerial imagery as ground textures without the need to download and convert them beforehand. The software can be installed either as a pre-built binary or from source code.

## B

### Binary

A pre-compiled, executable file of a program. Unlike installation from source code, a binary can be executed directly without requiring additional compilation steps.

### Blade Element Theory

A calculation method in aerodynamics where an aircraft is divided into many small segments to simulate airflow and forces in real-time.

### BORE (Burst-Oriented Response Enhancer)

A CPU scheduler that replaces the default EEVDF scheduler in the Liquorix kernel. BORE optimizes response time for interactive applications by prioritizing CPU-intensive burst phases. Relevant for X-Plane since the simulator generates high CPU load in irregular bursts. See [Liquorix](linux/optimizations/liquorix.md).

### Btrfs (B-tree Filesystem)

A copy-on-write filesystem for Linux with features like snapshots, transparent compression, and checksums. Offers more functionality than Ext4 but can be slower with fragmentation-sensitive workloads like loading large scenery files.

## C

### Compositor

A program that combines the contents of multiple windows into the final screen image. Under Wayland, the compositor also serves as the display server and window manager (e.g., Mutter for GNOME, KWin for KDE). Under X11, the compositor is a separate program that can be bypassed by fullscreen applications.

### CPU Affinity

The assignment of processes or threads to specific CPU cores. Through CPU affinity, X-Plane's main thread can run on a dedicated core while background processes and interrupts are moved to other cores. Configured via `taskset` or the kernel parameter `isolcpus`. See [System Tuning](linux/system/systemtuning.md).

### CPU Governor

The kernel's strategy for dynamically adjusting CPU clock frequency. `performance` maintains maximum frequency permanently, `ondemand` adjusts based on demand. For X-Plane, `performance` is recommended to avoid latency from frequency transitions. See [System Tuning](linux/system/systemtuning.md).

### C-States (CPU Idle States)

Power-saving idle states of modern CPUs. Higher C-States (C3, C6) save more power but take longer to wake up. For X-Plane, deep C-States can cause latency spikes. Can be limited via the kernel parameter `processor.max_cstate` or BIOS settings. See [System Tuning](linux/system/systemtuning.md).

### Custom Scenery

A directory in X-Plane where additional scenery files are stored. This is also where AutoOrtho's generated ortho textures are integrated.

## D

### DDS (DirectDraw Surface)

A texture format by Microsoft used in X-Plane for scenery and orthophoto textures. DDS files contain GPU-compressed image data (often in DXT/BC format) that can be loaded directly into VRAM without decompression. Ortho4XP generates DDS files from downloaded satellite imagery.

### Display Server

Software that manages graphics output and input devices for applications. X11 (Xorg) and Wayland are the two display server protocols on Linux. X-Plane 12 supports only X11. See [Display Server](linux/optimizations/displayserver.md).

### Docker

A platform for containerizing applications that enables packaging and running software in standardized units (containers). Docker simplifies the deployment and management of applications across different environments.

### DKMS (Dynamic Kernel Module Support)

A framework that enables automatic recompilation of kernel modules when kernel updates occur. Particularly important for drivers like Nvidia that are not included in the standard kernel.

### DRM/KMS (Direct Rendering Manager / Kernel Mode Setting)

The graphics subsystem in the Linux kernel that manages GPU access and display output. DRM provides the interface between userspace drivers (Mesa, Nvidia) and GPU hardware. KMS handles display resolution and mode switching directly in the kernel, enabling flicker-free booting and fast VT switching.

### DSF (Distribution Scenery Format)

X-Plane's native file format for scenery tiles. Each DSF file describes a one-degree-by-one-degree tile of the Earth's surface and contains terrain mesh, land use data, object placements, and road networks. Third-party orthophotos and meshes replace individual layers within this format.

### Dynamic Libraries

Also known as shared libraries, these are reusable collections of program code that can be loaded and shared by different programs at runtime. They typically have a .so (shared object) extension on Linux and allow for more efficient memory usage and easier updates.

## E

### EEVDF (Earliest Eligible Virtual Deadline First)

The default CPU scheduler in the Linux kernel since version 6.6, successor to CFS (Completely Fair Scheduler). EEVDF prioritizes tasks based on virtual deadlines and can improve latency for interactive applications. The Liquorix kernel uses the BORE scheduler instead.

### evdev

Event Device — the Linux kernel input interface that exposes input devices via `/dev/input/event*`. X-Plane uses SDL2 with the evdev backend for controller detection. Not to be confused with the older joystick interface (`/dev/input/js*`).

### Ext4 (Fourth Extended Filesystem)

The default filesystem of most Linux distributions. Ext4 is mature, stable, and offers good performance for both sequential and random access. Recommended for X-Plane due to its predictable I/O performance when loading scenery. See [Filesystem](linux/optimizations/filesystem.md).

## F

### FAA

Federal Aviation Administration - the US aviation authority that sets standards for flight simulations and training devices.

### FMOD

A proprietary audio engine by Firelight Technologies. X-Plane 12 uses FMOD Studio 2.02 for all audio output. On Linux, FMOD communicates with PulseAudio or PipeWire.

### FPS (Frames per Second)

The number of frames the simulator calculates and renders per second. Higher FPS means smoother display, though consistent frame times are more important than the raw FPS value. X-Plane shows current FPS through its built-in performance display. See [Performance](xplane/setup_diagnose/performance.md).

### Frame Time

The time in milliseconds the simulator needs to calculate and render a single frame. Consistent frame times are more important for a smooth simulation experience than a high framerate. Fluctuations (frame time spikes) manifest as stutters. See [Performance](xplane/setup_diagnose/performance.md).

### FUSE (Filesystem in Userspace)

An interface that allows implementing filesystems in user space rather than in the kernel. AutoOrtho uses FUSE to present streamed orthophotos as a virtual filesystem that X-Plane reads like a regular scenery directory.

## G

### Global Airports

The entry `*GLOBAL_AIRPORTS*` in X-Plane's scenery_packs.ini that contains the default airports, many of which are community-contributed via the X-Plane Gateway. In the load order, Global Airports should sit below custom airport sceneries but above autogen, orthophotos, and mesh layers. An incorrect position can cause floating airports or covered taxiways. See [Scenery Components](scenery/aufbau_quellen/scenery_components.md).

### Ground Markings

The markings and pavements on airports in X-Plane. In the [Airport Enhancement Package (AEP)](addon/scenery_addons/aep.md), these are replaced with new, high-resolution textures that support X-Plane 12's weather effects and create realistic patterns without repetition.

### GRUB (Grand Unified Bootloader)

The default bootloader for most Linux distributions. Kernel parameters for performance optimizations (C-States, NVMe settings, CPU isolation) are configured in GRUB's configuration at `/etc/default/grub` in the `GRUB_CMDLINE_LINUX_DEFAULT` parameter. See [System Tuning](linux/system/systemtuning.md).

### GUI (Graphical User Interface)

A graphical user interface that enables interaction with a program through graphical elements such as windows, buttons, and menus. In AutoOrtho, the GUI is used to configure the X-Plane directory and load ortho sets.

## H

### HDR

High Dynamic Range - a graphics technique that can display a particularly large brightness range, leading to more realistic lighting effects.

## I

### I/O Scheduler

The kernel algorithm that optimizes the order of read and write operations on storage devices. For NVMe SSDs, `none` (no-op) is recommended since the SSD's internal management is more efficient than software reordering. For SATA SSDs, `mq-deadline` is a good choice. See [Filesystem](linux/optimizations/filesystem.md).

### IRQ (Interrupt Request)

A signal used by hardware devices (GPU, NVMe SSD, USB controllers) to request the processor to handle data. Through targeted IRQ pinning, interrupts can be assigned to specific CPU cores to avoid disturbing X-Plane's main thread. See [System Tuning](linux/system/systemtuning.md).

### irqbalance

A userspace daemon that distributes hardware interrupts across CPU cores. irqbalance automatically adapts to new devices and respects kernel constraints for managed interrupts (MSI-X). The `IRQBALANCE_BANNED_CPULIST` setting in `/etc/default/irqbalance` excludes specific cores from interrupt distribution, keeping them free for the application. See [System Tuning](linux/system/systemtuning.md).

## K

### Kernel Module

A piece of code that can be loaded into the Linux kernel at runtime without restarting the system. Nvidia drivers, filesystem drivers, and hardware support are typically provided as kernel modules. DKMS ensures modules are automatically recompiled during kernel updates.

### Kernel Parameter

Configuration values passed to the kernel at boot time via the bootloader (GRUB). Parameters relevant to X-Plane include `processor.max_cstate` (C-States), `nvme_core.default_ps_max_latency_us` (NVMe power saving), and `isolcpus` (CPU isolation). Configured in `/etc/default/grub`. See [System Tuning](linux/system/systemtuning.md).

### KVM (Kernel-based Virtual Machine)

A virtualization solution integrated into the Linux kernel that enables running virtual machines with near-native performance. KVM utilizes hardware virtualization features of modern processors for efficient virtualization.

## L

### Latency

The delay between an action and its visible effect. Relevant in X-Plane as input latency (controller to control deflection), render latency (calculation to display), and I/O latency (scenery request to data availability). System tuning aims to minimize all three types of latency.

### ldd

A command-line program in Linux that displays all dynamic library dependencies of an executable file. It is an important diagnostic tool for identifying missing or incompatible libraries required for running a program like X-Plane.

### Linux

A free, open-source operating system known for its stability, security, and adaptability.

### Liquorix Kernel

An optimized version of the Linux kernel focused on performance. Often provides better response times and performance for desktop systems and gaming.

## M

### Mesa

The open-source graphics driver stack for Linux that provides OpenGL and Vulkan implementations for AMD (RADV), Intel, and other GPUs. Mesa also includes the Zink translation layer. The environment variable `MESA_LOADER_DRIVER_OVERRIDE` is only evaluated by Mesa drivers, not Nvidia.

### Mesh

The elevation model (terrain mesh) in X-Plane that defines the three-dimensional terrain shape — mountains, valleys, coastlines. The default mesh can be replaced with higher-resolution meshes from third parties. In scenery_packs.ini, the mesh is typically placed below the orthophoto layer.

## N

### noatime

A mount option for Linux filesystems that suppresses updating the access timestamp when reading files. Reduces unnecessary write operations on the SSD and improves I/O performance, especially when loading large scenery directories. See [Filesystem](linux/optimizations/filesystem.md).

### Nouveau

The default open-source driver for Nvidia graphics cards in Linux. Often disabled when installing the proprietary Nvidia driver.

### Nvidia Driver

Proprietary driver software from Nvidia for their graphics cards. Compared to the open-source Nouveau driver, it often provides better performance and more features, especially for 3D applications and gaming.

### NVMe (Non-Volatile Memory Express)

A protocol for accessing SSDs via the PCIe interface. NVMe SSDs offer significantly higher throughput and lower latency than SATA SSDs. Relevant for X-Plane due to faster scenery loading times. The power-saving feature APST should be disabled for optimal performance.

## O

### OpenGL

A cross-platform graphics interface that was superseded in X-Plane 12 by Vulkan as the primary rendering API. OpenGL is still used by some plugins for their rendering. The Zink translation layer in Mesa allows processing these OpenGL calls within the Vulkan pipeline.

### Ortho4XP

A tool for creating photorealistic landscape textures for X-Plane from various satellite image sources.

### Orthophotos

Orthophotos (or orthoimages) are geometrically corrected aerial photographs of the Earth's surface. In X-Plane, they are used as high-resolution ground textures to achieve a realistic representation of the landscape.

### Overlay (Scenery)

A scenery layer in X-Plane that sits above a base scenery and supplements or replaces it. Overlays typically contain airports, buildings, or roads, while the base layer provides terrain mesh and orthophotos. The order in scenery_packs.ini determines which overlays take precedence. See [Scenery Components](scenery/aufbau_quellen/scenery_components.md).

## P

### PBR

Physically Based Rendering - a graphics technique that simulates physical properties of materials and light to create realistic representations.

### PDS (Priority and Deadline based Skiplist)

The CPU scheduler used by the Liquorix kernel, replacing the mainline EEVDF scheduler. PDS uses a skiplist data structure for efficient task selection and prioritizes based on deadlines. Combined with shorter preemption windows and a 1000 Hz timer frequency, it provides lower latency for interactive applications. Unlike EEVDF, PDS does not provide the utilization signals that the `schedutil` governor relies on. See [System Tuning](linux/system/systemtuning.md).

### PipeWire

A modern audio and video framework for Linux designed to replace PulseAudio and JACK. PipeWire offers lower latency and better integration with professional audio workflows. FMOD in X-Plane communicates with PipeWire through its PulseAudio-compatible interface.

### Plugin

A software extension that adds additional functionality to X-Plane. Plugins can be developed by third parties.

### Preemption

The kernel's ability to interrupt running tasks to give CPU time to higher-priority tasks. More preemption means lower latency but also more overhead. The Liquorix kernel uses full preemption for minimal response times. See [System Tuning](linux/system/systemtuning.md).

### PulseAudio

An audio server for Linux that mixes audio streams from multiple applications and forwards them to the hardware. Increasingly being replaced by PipeWire but still in use on many systems. FMOD in X-Plane communicates via the PulseAudio interface — both with PulseAudio itself and with PipeWire through its compatibility layer.

### pyenv

A tool for managing multiple Python versions on a system. It allows installation and use of multiple Python versions side by side without affecting the system Python.

## R

### RADV

The open-source Vulkan driver for AMD GPUs within the Mesa driver stack. RADV is the default Vulkan driver on Linux systems with AMD graphics cards and is used directly by X-Plane 12.

## S

### scenery_packs.ini

A configuration file in X-Plane's Custom Scenery folder that determines the load order of installed scenery. AutoOrtho automatically adds entries with the prefix `z_ao_` here.

### SDL2 (Simple DirectMedia Layer)

A cross-platform multimedia library used by X-Plane 12 on Linux for window management, input devices, and joystick detection. SDL2 communicates with the display server (X11/XWayland) and the input subsystem (evdev).

### Shader Cache

A cache for compiled GPU shader programs. X-Plane compiles shaders when first loading a scene, which can cause stutters. The shader cache stores compiled results so subsequent loads are faster. On Linux, the cache is located in `~/.cache/`. See [Configuration](xplane/setup_diagnose/config.md).

### Single-CPU

A historical characterization of X-Plane's architecture. While single-core performance remains important, X-Plane 12 distributes substantial per-frame work across multiple cores since version 12.4.

### SimHeaven (X-World)

A scenery framework for X-Plane that generates 3D buildings, vegetation, and other autogen objects based on OpenStreetMap data. SimHeaven X-World complements orthophoto tools like AutoOrtho by adding the 3D layer that orthophotos alone cannot provide. When using SimHeaven, the yOrtho overlays included with AutoOrtho are not needed.

### SoftIRQ (Software Interrupt)

A deferred interrupt processing mechanism in the Linux kernel. Unlike hardware IRQs that are handled immediately, SoftIRQs are processed after the hardware interrupt handler returns, handling less time-critical work like network packet processing and block device completion. The `%soft` column in `mpstat` shows SoftIRQ time per core — relevant for verifying that interrupt shielding keeps both hardware IRQs and SoftIRQs off application cores. See [System Tools](linux/system/systemtools.md).

### sysctl

A tool for viewing and changing kernel parameters at runtime. Unlike GRUB kernel parameters that only take effect at boot, sysctl values can be adjusted at any time. Relevant settings for X-Plane include VM swappiness and network buffers. Configured via `/etc/sysctl.d/`.

### systemd

The init system and service management framework of most Linux distributions. systemd starts and manages system services, timers, and mount points. Relevant for X-Plane through timers like `fstrim.timer` (SSD TRIM), service units for irqbalance, and configuring CPU governor settings at boot.

## T

### Tearing

A visible display artifact where parts of two consecutive frames are shown simultaneously, appearing as a horizontal tear in the image. Occurs when the GPU delivers a new frame while the monitor is still displaying the previous one. V-Sync prevents tearing but can increase input latency. Under X11 in fullscreen mode, tearing is rarely an issue.

### Tick Rate (HZ)

The frequency at which the Linux kernel triggers its internal timer interrupt. A higher tick rate (e.g., 1000 Hz in the Liquorix kernel) enables finer scheduling granularity and lower latency but creates more overhead. The default kernel typically uses 250 Hz. See [Liquorix](linux/optimizations/liquorix.md).

### TRIM

A command that tells the SSD controller which data blocks are no longer needed. Regular TRIM (via `fstrim.timer` or the mount option `discard`) maintains SSD write speed and prevents performance degradation with large scenery installations. See [Filesystem](linux/optimizations/filesystem.md).

## V

### VRAM (Video RAM)

The memory on the graphics card that stores textures, shaders, framebuffers, and other graphics data. X-Plane with high-resolution orthophotos can occupy several gigabytes of VRAM. When VRAM is insufficient, textures must be swapped between GPU and system memory, causing stutters.

### Vulkan API

A modern, cross-platform graphics interface with low overhead used by X-Plane for graphics rendering. Compared to OpenGL, Vulkan often provides better performance through more efficient CPU usage and more direct GPU control.

## W

### Wayland

A modern display server protocol for Linux, successor to X11. The compositor handles both display server and window manager duties. Wayland offers better security and per-monitor refresh rates, but X-Plane 12 cannot speak Wayland natively and uses XWayland instead. See [Display Server](linux/optimizations/displayserver.md).

### Wine (Wine Is Not an Emulator)

A compatibility layer that enables running Windows programs on Linux. Wine translates Windows API calls to POSIX calls without emulating Windows itself.

## X

### X11 (Xorg)

The classic display server protocol for Linux, in use since 1984. A central X server manages all graphics and input. X-Plane speaks X11 natively. See [Display Server](linux/optimizations/displayserver.md).

### X-Plane

A highly realistic flight simulator available for various platforms (Windows, macOS, Linux).

### XWayland

A compatibility layer that runs a complete X11 server inside a Wayland session. When an X11 application (like X-Plane) starts on a Wayland desktop, XWayland handles the translation automatically. The extra translation adds latency. See [Wayland Session](linux/optimizations/displayserver_wayland.md).

### Xroads

A library for X-Plane 11 & 12 that optimizes the display of roads in Ortho4XP scenery.

## Z

### Zink

An OpenGL translation layer within Mesa that converts OpenGL commands into Vulkan commands. X-Plane 12 ships its own Zink driver so that plugins using OpenGL for rendering can work within the Vulkan render pipeline.

### ZL (Zoom Level)

The zoom level of orthophotos that determines their resolution. Higher ZL values mean more detailed images: ZL16 corresponds to roughly four meters per pixel, ZL17 two meters, ZL18 one meter. Higher zoom levels require significantly more storage space and bandwidth. See [Introduction to Orthophotography](scenery/orthophotography/orthophotography_intro.md).

## 3

### 32-Bit Compatibility

The ability of a 64-bit Linux system to run and support 32-bit applications and libraries. This may be necessary for some programs or plugins that have not yet been optimized for 64-bit architectures. In Debian, 32-bit support is activated by adding the i386 architecture and installing corresponding libraries.
