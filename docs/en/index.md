# **XoL**: Running **X**-Plane **o**n **L**inux

This documentation covers setup and optimization of X-Plane 12 (Laminar Research) under Linux. It is aimed at experienced Linux users — a working installation is assumed. The examples are based on Debian but transfer to other distributions with minor adjustments.

## Where to Start

- **Why Linux?** [Introduction](intro.md) explains what makes X-Plane on Linux different.
- **New to X-Plane on Linux?** [Getting Started](begin.md) covers system requirements, installation, and first launch.
- **X-Plane already running?** [Performance Fundamentals](performance_overview.md) explains the three load dimensions (CPU, I/O, network) before diving into [System Tuning](systemtuning.md).

## About This Documentation

The core focus is on Linux system tuning — kernel parameters, CPU governor, GPU drivers, display server selection, and filesystem optimization — complemented by performance analysis using both X-Plane's built-in tools and Linux monitoring utilities. Additional sections cover scenery management with orthophoto streaming, flight operations including ATC procedures, and a reference catalog of Linux-compatible addons and plugins. The guides are modular — individual topics can be implemented independently or combined as needed.

## Contributing

This documentation is an open project. Improvements or additions can be contributed via GitHub:

- Create issues for bugs or suggestions
- Submit pull requests for changes
- Share experiences in the discussions in the footer of this website (e.g., via the Discord link)

## Featured Video: X-Plane: Display Server Choice

<div class="video-container" style="max-width: 640px;" markdown>
<video controls width="100%" preload="metadata" aria-label="Video: X-Plane — Display Server Choice" poster="../assets/video/en/X-Plane__Display_Server_Choice/X-Plane__Display_Server_Choice.jpg">
  <source src="../assets/video/en/X-Plane__Display_Server_Choice/X-Plane__Display_Server_Choice.mp4" type="video/mp4">
</video>
</div>

[All Videos →](videos.md)

## Recent Changes

### 2026-02-16
- Accessibility improved: larger fonts, keyboard focus indicators, skip link, video ARIA labels
- Source sections revised: Arch Wiki links replaced with distro-independent sources
- [Scenery Components](scenery_components.md) audited: priority direction corrected, DDS format, OSM clarification, tone aligned
- New video: [Display Server](displayserver.md) — X11 vs Wayland decision guide
- New videos: [Introduction](intro.md) — guided tour through XoL (DE + EN)
- [Scenery Components](scenery_components.md): key terms linked to [Glossary](glossary.md), new entry Global Airports
- [Scenery Components](scenery_components.md) restructured: load order as table, admonition boxes instead of nested lists
- [ToLiss Ecosystem](addon/toliss_ecosystem.md) restructured: simbrief_hub section added, Mods split to [own page](addon/toliss_mods.md)

### 2026-02-15
- New addon pages: [SGES](addon/sges.md), [KabinXP](addon/kabinxp.md), [LST](addon/lst.md), [LinuxTrack](addon/linuxtrack.md), [XLinSpeak](addon/xlinspeak.md), [WINCTRL](addon/winctrl.md), [TerrainRadar](addon/terrainradar.md), [NOAA Weather](addon/noaa_weather.md), [MobiFlight](addon/mobiflight.md), [SayIntentions.AI](addon/sayintentions.md)
- New Sounds category: [KOSP Project](addon/kosp_project.md), [Mango Studios](addon/mango_studios.md)
- New page [Performance Fundamentals](performance_overview.md)
- ATC section: 6 flight phase pages ([Pushback & Taxi](flight_operations/pushback_taxi.md), [Takeoff](flight_operations/takeoff.md), [Departure & Climb](flight_operations/departure.md), [En Route](flight_operations/enroute.md), [Approach](flight_operations/approach.md), [Landing & Taxi In](flight_operations/landing.md))
- [ToLiss Ecosystem](addon/toliss_ecosystem.md) restructured, videos embedded
- Existing addon pages revised: cross-references, corrections, prices and redundant Linux notes removed
- Navigation: categories flattened, Sounds category added
- [FlyWithLua](addon/flywithlua.md): general script installation guide added
- [Performance](xplane/performance.md) revised: flowing text instead of nested lists, reference and Microprofiler tables, diagnostic workflows, sources section

### 2026-02-14
- New page [System Tuning Introduction](systemtuning_intro.md), videos embedded (DE + EN)
- [Liquorix Kernel](liquorix.md) audited: scheduler description corrected, quick install method added, page rewritten
- [Nvidia Driver](nvidia.md), [System Tuning](systemtuning.md), [System Tools](systemtools.md), [X-Plane Configuration](xplane/config.md) audited and fact-checked
- [Getting Started](begin.md) revised, [Glossary](glossary.md) expanded
- Navigation: System Monitoring grouped under System Tuning


