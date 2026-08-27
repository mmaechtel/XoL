---
description: "X-Plane 12 on Linux — setup guides, kernel tuning, GPU drivers, filesystem optimization, scenery management, and addon catalog."
---
# **XoL**: Running **X**-Plane **o**n **L**inux

This documentation covers setup and optimization of X-Plane 12 (Laminar Research) under Linux. It is aimed at experienced Linux users — a working installation is assumed. The examples are based on Debian but transfer to other distributions with minor adjustments.

## Where to Start

- **Why Linux?** [Introduction](intro.md) explains what makes X-Plane on Linux different.
- **New to X-Plane on Linux?** [Getting Started](begin.md) covers system requirements, installation, and first launch.
- **X-Plane already running?** [Performance](fundamentals/performance/performance_overview.md) explains the three load dimensions (CPU, I/O, network) before diving into [System Tuning](linux/system/systemtuning.md).

## About This Documentation

The core focus is on Linux system tuning — kernel parameters, CPU governor, GPU drivers, display server selection, and filesystem optimization — complemented by performance analysis using both X-Plane's built-in tools and Linux monitoring utilities. Additional sections cover scenery management with orthophoto streaming, flight operations including ATC procedures, and a reference catalog of Linux-compatible addons and plugins. The guides are modular — individual topics can be implemented independently or combined as needed.

## Contributing

This documentation is an open project. Improvements or additions can be contributed via GitHub:

- Create issues for bugs or suggestions
- Submit pull requests for changes
- Share experiences in the discussions in the footer of this website (e.g., via the Discord link)

## Featured Video: X-Plane 12 Performance

<div class="video-container" style="max-width: 640px;" markdown>
<video controls width="100%" preload="metadata" aria-label="Video: X-Plane 12 Performance" poster="../assets/video/en/X-Plane_12_Performance/X-Plane_12_Performance.jpg">
  <source src="../assets/video/en/X-Plane_12_Performance/X-Plane_12_Performance.mp4" type="video/mp4">
</video>
</div>

[All Videos →](videos.md)

## Recent Changes

### 2026-08-27

- The section overview pages now carry real orientation text instead of a one-liner — what the section covers, for whom, and in which order to read: [Fundamentals](fundamentals/index.md), [Utilities](linux/extensions/index.md), [Structure & Sources](scenery/aufbau_quellen/index.md), [Orthophotography](scenery/orthophotography/index.md), [Autogen](scenery/autogen/index.md), [Scripting](addon/scripting/index.md), [ToLiss Mods](addon/toliss/mods/index.md), [Sounds](addon/sounds/index.md), [Tools](addon/tools/index.md), [Traffic & Ground Ops](addon/traffic/index.md), [Scenery Plugins](addon/scenery_addons/index.md), [Via KVM](addon/kvm/index.md), [Weather](flight_operations/weather/index.md), [Online](flight_operations/vatsim/index.md) and [Videos](videos.md). Along the way a few summaries were corrected against their detail pages — XRoads hides road polygons on ortho tiles rather than adding traffic, XOrganizer is Windows-only, and on X-Plane 12 openSAM v5 replaces standalone AutoDGS
- [Easy Freighter](addon/toliss/mods/easy_freighter.md) now explains how the cargo door is switched per livery and lists the setup steps
- The [Videos](videos.md) pages describe each video with duration and upload date in machine-readable form, so search engines can show them as video results
- The sidebar shows only the active section, which cuts page weight by roughly 40 %; the retired airport blog posts were removed

### 2026-08-21

- The [X-Plane WINCTRL Plugin](addon/tools/winctrl.md) page was reworked. The vendor now trades as WINCTRL, so "Winwing" is gone from the documentation; **WINCTRL** means the hardware, the software is the **X-Plane WINCTRL plugin**. The udev section now recommends Debian's `uaccess` tag over `MODE="0666"` — including the trap that the rule file must be named `70-winctrl.rules`, because `99-*` sorts after `73-seat-late.rules` and the tag then does nothing. The vendor ID `4098` is a hexadecimal string (0x4098); the previous note claiming otherwise was wrong. New: custom FMC display fonts as `.xpwwf` files, and the rule that buttons assigned in X-Plane take precedence over the plugin. Supported hardware and the SimAppPro comparison were corrected
- [X-Plane Configuration](xplane/setup_diagnose/config.md#controllers): new table separating the two device classes — joysticks, yokes and throttle quadrants are handled by the kernel and configured entirely inside X-Plane, while cockpit panels expose a root-only raw HID node and need a udev rule plus a plugin

### 2026-08-17

- [AviTab](addon/cockpit/avitab.md): new tip on using Little Navmap as a moving map in the AviTab Browser — Little Navmap's built-in web server delivers the map with the live aircraft position to the cockpit tablet, with a working `config.ini` example for Linux; the [Little XpConnect](addon/tools/littlexpconnect.md) page links to it
