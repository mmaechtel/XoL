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

### 2026-08-03
- [Ortho4XP](scenery/orthophotography/ortho4xp.md) rebuilt as a parameter reference: every default verified against the source and corrected, the parameters grouped by topic and extended with `min_angle`, `water_tech`, airport coverage and the mask and elevation settings. New chapter **Building Packages for Ortho Streaming** — how `skip_downloads` and `skip_converts` produce mesh-and-terrain-only packages for a streaming layer, with a configuration profile of its own. The four profiles are now complete, paste-ready config fragments
- New page [XPME](scenery/ortho_streaming/xpme.md), a third ortho streaming solution alongside AutoOrtho and XEarthLayer — with an official Linux build, but closed source and freemium: high-resolution ground textures and preloading require a paid subscription, and it conflicts with existing Ortho4XP tiles
- [ToLiss Mods](addon/toliss/toliss_mods.md) extended by both wing mods: the **Durantula Wing Enhancement MOD** (new flaps and flap-track fairings, plus wingflex via X-Plane's native wing deflection) and **RealWings**, which replaces the wing outright with new geometry and 4K textures. Both have a native Linux installer; a note explains why the two should be treated as alternatives
- New page [XPAIS Marine Traffic](addon/traffic/xpais_marine_traffic.md): live AIS ship traffic from the AISStream feed, rendered at the vessels' real positions — a native Linux plugin, built from source, GPL-3.0. Its repository has been archived since July 2026, which the page states up front, and it explains why X-Plane's own ship traffic has to be switched off alongside it
- [Scenery Sources](scenery/aufbau_quellen/scenery_sources.md) now covers **X-World Pro**, SimHeaven's commercial VFR line for X-Plane 12 — what it adds over the free packages, which remain available. Includes the Linux pitfall of the vegetation library: the supplied Windows batch file does nothing here, and without a manually created symlink X-Plane aborts loading

### 2026-07-27
- Fact-check across all 46 [addon pages](addon/index.md): every claim verified against current primary sources. Highlights: AviTab now documents the maintained TeamAvitab fork, LST's developer tooling is a browser-based Web Editor that also runs on Linux, XOrganizer is now sold via the X-Plane.org Store, XPPython3 points to its maintained successor fork, and stagnant projects (XGS, XLinSpeak, TerrainRadar and others) are marked with their last release date

### 2026-07-26
- [Ortho4XP](scenery/orthophotography/ortho4xp.md) now covers [OrthoForge](https://xpconnect.me/orthoforge.html): an independently developed successor with a native Linux setup script, separate land/seabed elevation sources and pre-baked OpenStreetMap data

