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

### 2026-07-26
- [Ortho4XP](scenery/orthophotography/ortho4xp.md) now covers [OrthoForge](https://xpconnect.me/orthoforge.html): an independently developed successor with a native Linux setup script, separate land/seabed elevation sources and pre-baked OpenStreetMap data

### 2026-06-30
- [WorldMap of Scenery](Maps.md) now shows each scenery's last update date and adds a **Scenery since** year filter — show only sceneries updated since a chosen year. The map now covers over 1800 X-Plane 12 sceneries

### 2026-06-24
- New page [X-ProTurb](addon/flylua_scripts/xproturb.md): physics-based turbulence engine for X-Plane 12, modelling the atmosphere from MIL-F-8785C, FAR 25.341 and ICAO 9625 Level-D standards with per-airframe 6-DOF response, von Kármán/Dryden spectra, CAT, mountain-wave and CB/storm modelling
- New page [AnyAirline](addon/cockpit/anyairline.md): passenger cabin immersion with AI cabin announcements, a route-aware passenger manifest, boarding ambience and a free passenger IFE map — the desktop connector ships an official Linux build
- [XEarthLayer](scenery/ortho_streaming/xearthlayer.md) updated for v0.4.6: four-step setup wizard with dynamic disk-cache sizing (25% of free space) and RAM-based memory cache, GPU adapter selection step, and a cache fix so tiles from failed downloads are no longer stored
- [AutoOrtho](scenery/ortho_streaming/autoortho.md) expanded with the latest ProgrammingDinosaur-fork features: unified single-process architecture across all OS, VRAM optimization via dynamic DDS sizing, and a lightweight map UI that drops the bundled Chromium browser






