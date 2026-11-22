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

### 2026-11-22

- [SGES](addon/flylua_scripts/sges.md): development of the FlyWithLua script has ended; the page now covers its native successor SGES NG, currently in testing (X-Plane 12.4 or newer, no FlyWithLua needed)
- [X-ProTurb](addon/flylua_scripts/xproturb.md) updated: one-time calibration per aircraft, real-world weather data via LiveCAT, separate atmosphere and aircraft scales, and a revised installation section
- [SimLoad Manager](addon/traffic/simloadmanager.md) opens and closes aircraft doors automatically as ground vehicles arrive; [XP CabinState](addon/cockpit/xp_cabinstate.md) adds new service trolleys and updates inside the program
- [XEarthLayer](scenery/ortho_streaming/xearthlayer.md): the regional packages are built at ZL16, with ZL17 around ICAO airports

### 2026-11-02

- [XEarthLayer](scenery/ortho_streaming/xearthlayer.md) updated for version 0.5.0: macOS support, generated night lighting for ortho scenery, the rebuilt 17-region package library with its new package manager, a separate prefetch lane that never delays X-Plane's tile requests, and XDG paths under `~/.config` and `~/.cache`. A warning box covers the switch from the old package generation

### 2026-11-01

- New plugin pages: [AOC Datalink Center](addon/cockpit/aoc_datalink_center.md) brings ACARS/CPDLC dispatch via Hoppie as a native Linux plugin, [XP CabinState](addon/cockpit/xp_cabinstate.md) simulates cabin, crew, and passengers — officially Windows-only, documented with a tested Wine setup and the SimLoad Manager integration — [XP BirdState](addon/scenery_addons/xp_birdstate.md) adds bird flocks with an official Linux build, and [Night Sky Fix](addon/scenery_addons/night_sky_fix.md) replaces the star catalog for a visible Milky Way
- [SimLoad Manager](addon/traffic/simloadmanager.md) is now a native plugin with its own ground vehicles, passengers, and crew — no FlyWithLua or SGES required; the page moved to Traffic & Ground Ops
