# **XoL**: Running **X**-Plane **o**n **L**inux

This documentation covers setup and optimization of X-Plane 12 (Laminar Research) under Linux. It is aimed at experienced Linux users — a working installation is assumed. The examples are based on Debian but transfer to other distributions with minor adjustments.

## Where to Start

- **Why Linux?** [Introduction](intro.md) explains what makes X-Plane on Linux different.
- **New to X-Plane on Linux?** [Getting Started](begin.md) covers system requirements, installation, and first launch.
- **X-Plane already running?** [Performance Fundamentals](performance_overview.md) explains the three load dimensions (CPU, I/O, network) before diving into [System Tuning](system/systemtuning.md).

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
- New video: [Display Server](optimizations/displayserver.md) — X11 vs Wayland decision guide
- New videos: [Introduction](intro.md) — guided tour through XoL (DE + EN)
- [ToLiss Ecosystem](addon/toliss/toliss_ecosystem.md): simbrief_hub section added, new page [ToLiss Mods](addon/toliss/toliss_mods.md)

### 2026-02-15
- New addon pages: [SGES](addon/flylua_scripts/sges.md), [KabinXP](addon/cockpit/kabinxp.md), [LST](addon/scenery_addons/lst.md), [LinuxTrack](addon/cockpit/linuxtrack.md), [XLinSpeak](addon/tools/xlinspeak.md), [WINCTRL](addon/tools/winctrl.md), [TerrainRadar](addon/cockpit/terrainradar.md), [NOAA Weather](addon/scenery_addons/noaa_weather.md), [MobiFlight](addon/kvm/mobiflight.md), [SayIntentions.AI](addon/kvm/sayintentions.md)
- New Sounds category: [KOSP Project](addon/sounds/kosp_project.md), [Mango Studios](addon/sounds/mango_studios.md)
- New page [Performance Fundamentals](performance_overview.md)
- ATC section: 6 flight phase pages ([Pushback & Taxi](flight_operations/atc/pushback_taxi.md), [Takeoff](flight_operations/atc/takeoff.md), [Departure & Climb](flight_operations/atc/departure.md), [En Route](flight_operations/atc/enroute.md), [Approach](flight_operations/atc/approach.md), [Landing & Taxi In](flight_operations/atc/landing.md))
- [FlyWithLua](addon/scripting/flywithlua.md): general script installation guide added

### 2026-02-14
- New page [System Tuning Introduction](system/index.md), videos embedded (DE + EN)
- [Glossary](glossary.md) expanded


