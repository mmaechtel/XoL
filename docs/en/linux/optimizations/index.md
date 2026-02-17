---
description: "Linux optimization layers for X-Plane: NVIDIA driver, Liquorix kernel, X11 vs. Wayland display server, and filesystem I/O tuning."
---
# Optimizations

Between kernel and application lie several layers that affect X-Plane's rendering pipeline: GPU driver, scheduler, display server, and filesystem. The NVIDIA driver provides Vulkan support and kernel mode setting — with separate header packages on Liquorix. The Liquorix kernel itself replaces the mainline scheduler with PDS at 1000 Hz timer frequency and full preemption, responding four times faster to load changes than the stock kernel. X-Plane has no native Wayland support; in a Wayland session it runs through XWayland, which doubles input latency compared to a direct X11 session. At the filesystem level, X-Plane benefits from NVMe SSDs with disabled power saving and optimized mount options.

- **[Nvidia Drivers](nvidia.md)** — Installation and configuration for Vulkan performance
- **[Liquorix Kernel](liquorix.md)** — Low-latency kernel for real-time workloads
- **[Display Server](displayserver.md)** — X11 vs. Wayland for X-Plane
- **[X11 Session](displayserver_x11.md)** — X11-specific configuration
- **[Wayland Session](displayserver_wayland.md)** — Wayland-specific configuration
- **[Filesystem](filesystem.md)** — Storage structure and I/O optimization
