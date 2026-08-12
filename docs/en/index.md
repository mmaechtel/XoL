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

### 2026-08-12

- New page [AutoHaze](addon/flylua_scripts/autohaze.md): a FlyWithLua script that replaces X-Plane's default haze with turbidity computed from satellite aerosol data, surface weather and the real boundary layer height — because above the METAR visibility cap the simulator has no data left and falls back to a fixed, usually excessive value. Linux support arrived with version 2.4; the page collects the helper-binary specifics, the SSL certificate fix and the log file
- New page [Bay's Lighting Mod](addon/scenery_addons/bays_lighting_mod.md): a complete overhaul of airport, night and cockpit lighting including cloud scattering and visibility. The page explains why night lighting and ortho scenery collide — ortho removes the distant baked light layer, which ends the lights abruptly around the aircraft, with or without the mod

### 2026-08-04
- Adversarial counter-check of the pages revised on 2026-08-03, with several corrections. [Scenery Sources](scenery/aufbau_quellen/scenery_sources.md): X-World Pro ships its own Linux installation script, so the manual symlink applies only to the free vegetation library — the previous instruction would have produced a broken Pro install. [XPME](scenery/ortho_streaming/xpme.md) does document a refund period. [Ortho4XP](scenery/orthophotography/ortho4xp.md): the "runways follow terrain contours" option disappeared with X-Plane 11, not 12, the Sonny mirror also carries 0.5″ tiles for the Alps, and the forum links now point at the Ortho4XP forum again
- Smaller precision fixes on the same pages: `masking_mode` selects a mask algorithm rather than a texture, `road_level=1` also includes trunk roads, `custom_dem` needs GDAL only for non-HGT rasters, and [XPAIS Marine Traffic](addon/traffic/xpais_marine_traffic.md) has the complete config and menu, the correct hull fallback and the two design decisions no longer listed as limitations

### 2026-08-03
- [Ortho4XP](scenery/orthophotography/ortho4xp.md) rebuilt as a parameter reference: every default verified against the source and corrected, the parameters grouped by topic and extended with `min_angle`, `water_tech`, airport coverage and the mask and elevation settings. New chapter **Building Packages for Ortho Streaming** — how `skip_downloads` and `skip_converts` produce mesh-and-terrain-only packages for a streaming layer, with a configuration profile of its own. The four profiles are now complete, paste-ready config fragments
- New page [XPME](scenery/ortho_streaming/xpme.md), a third ortho streaming solution alongside AutoOrtho and XEarthLayer — with an official Linux build, but closed source and freemium: high-resolution ground textures and preloading require a paid subscription, and it conflicts with existing Ortho4XP tiles
- [ToLiss Mods](addon/toliss/toliss_mods.md) extended by both wing mods: the **Durantula Wing Enhancement MOD** (new flaps and flap-track fairings, plus wingflex via X-Plane's native wing deflection) and **RealWings**, which replaces the wing outright with new geometry and 4K textures. Both have a native Linux installer; a note explains why the two should be treated as alternatives
- New page [XPAIS Marine Traffic](addon/traffic/xpais_marine_traffic.md): live AIS ship traffic from the AISStream feed, rendered at the vessels' real positions — a native Linux plugin, built from source, GPL-3.0. Its repository has been archived since July 2026, which the page states up front, and it explains why X-Plane's own ship traffic has to be switched off alongside it
- [Scenery Sources](scenery/aufbau_quellen/scenery_sources.md) now covers **X-World Pro**, SimHeaven's commercial VFR line for X-Plane 12 — what it adds over the free packages, which remain available. Includes the Linux pitfall of the vegetation libraries: the supplied Windows batch file does nothing here
