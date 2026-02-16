# **XoL**: Running **X**-Plane **o**n **L**inux

This documentation is aimed at experienced Linux users who want to run X-Plane on Linux. A working Linux installation is assumed.

The examples shown here are based on Debian Linux but can be easily adapted to other distributions. The basic concepts and approaches remain the same - only the specific package manager commands or repository configurations need to be adjusted accordingly.

## Featured Video

<div class="video-container" markdown>
<video controls width="100%" preload="metadata" poster="../assets/video/en/toliss_flow_with_plugins/Beyond_the_Default_Cockpit.jpg">
  <source src="../assets/video/en/toliss_flow_with_plugins/Beyond_the_Default_Cockpit.mp4" type="video/mp4">
</video>
</div>

[All Videos →](videos.md)

## Documentation Content

The documentation covers X-Plane configuration and optimization under Linux. The core focus is on system tuning — kernel parameters, CPU governor, GPU drivers, display server selection, and filesystem optimization — complemented by performance analysis using both X-Plane's built-in tools and Linux monitoring utilities. Additional sections cover scenery management with orthophoto streaming, flight operations including ATC procedures across all flight phases, and a reference catalog of Linux-compatible addons and plugins.

## Guide Structure

The guides are modular — individual topics can be implemented independently or combined as needed. Each guide explains the goal, shows the necessary steps, and provides troubleshooting tips. The content is organized into sections covering Linux system optimization, X-Plane configuration and performance, scenery management, addons and plugins, and flight operations.

## Contributing

This documentation is an open project. Improvements or additions can be contributed via GitHub:

- Create issues for bugs or suggestions
- Submit pull requests for changes
- Share experiences in the discussions in the footer of this website (e.g., via the Discord link)

## Recent Changes

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


