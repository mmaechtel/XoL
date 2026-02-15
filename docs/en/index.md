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

The documentation covers the most important areas of X-Plane configuration under Linux. The focus is on optimal settings for X-Plane, performance optimization through kernel, drivers, and system settings, as well as the installation and configuration of important extensions like AutoOrtho. Additionally, common problems and their solutions are thoroughly addressed. A special emphasis is placed on performance analysis using integrated and external tools, filesystem optimization for fast loading times, and hardware-specific adjustments for maximum performance.

## Guide Structure

The technical guides are modular in design and enable flexible implementation. You can implement individual components as needed or adapt the entire system according to your requirements. Each guide describes the goal and benefit of the change, shows the necessary steps, explains important configuration options, and provides troubleshooting tips. The guides are organized into logical sections: Basic system optimization, performance monitoring and analysis, hardware-specific adjustments, and advanced configurations for special use cases.

## Contributing

This documentation is an open project. Improvements or additions can be contributed via GitHub:

- Create issues for bugs or suggestions
- Submit pull requests for changes
- Share experiences in the discussions in the footer of this website (e.g., via the Discord link)

## Recent Changes

### 2026-02-15
- New page [SGES](addon/sges.md) — Ground equipment services (GPU, fuel truck, chocks, animated passengers) as FlyWithLua script
- New page [KabinXP](addon/kabinxp.md) — Cabin announcement plugin with custom audio files and per-livery sound packs
- [ToLiss Ecosystem](addon/toliss_ecosystem.md): SGES and KabinXP moved to standalone pages
- [FlyWithLua](addon/flywithlua.md) expanded: General script installation guide (Scripts, Modules, sound folders)
- Navigation: Ortho Streaming and FlyWithLua Scripts as standalone categories
- New addon pages: [LST](addon/lst.md) (animated ground traffic for sceneries), [LinuxTrack](addon/linuxtrack.md) (head tracking for Linux), [XLinSpeak](addon/xlinspeak.md) (TTS for plugin speech output on Linux), [WINCTRL](addon/winctrl.md) (Winwing hardware integration without SimAppPro), [TerrainRadar](addon/terrainradar.md) (EGPWS terrain display and VSD)
- New addon pages (Via KVM): [MobiFlight](addon/mobiflight.md) (open-source cockpit hardware middleware, network split setup) and [SayIntentions.AI](addon/sayintentions.md) (AI-based air traffic control with voice recognition, VM setup with UDP forwarding)
- New page [NOAA Weather](addon/noaa_weather.md) — Python plugin for real-world snow coverage and METAR monitoring as a supplement to X-Plane's Real Weather
- [ToLiss Ecosystem](addon/toliss_ecosystem.md) and [Videos](videos.md): "Beyond the Default Cockpit" video embedded (EN)
- [ToLiss Ecosystem](addon/toliss_ecosystem.md) and [Videos](videos.md): "Vom Briefing zum Gate" video embedded (DE)
- ATC section expanded: 6 new flight phase pages — [Pushback & Taxi](flight_operations/pushback_taxi.md), [Takeoff](flight_operations/takeoff.md), [Departure & Climb](flight_operations/departure.md), [En Route](flight_operations/enroute.md), [Approach](flight_operations/approach.md), [Landing & Taxi In](flight_operations/landing.md) — complete gate-to-gate ATC communication guide
- New addon pages: [SkunkCrafts Updater](addon/skunkcrafts_updater.md) (update tool with glibc requirement and Wayland notes), [XPPython3](addon/xppython3.md) (Python 3 scripting engine with Debian dependencies)
- Navigation restructured: Addon categories flattened (removed Miscellaneous wrapper), [ToLiss Ecosystem](addon/toliss_ecosystem.md) as standalone menu item, Ortho Streaming as subcategory
- ToLiss SimBrief Connector removed (obsolete), [simbrief_hub](https://github.com/hotbso/simbrief_hub) reference added to [ToLiss Ecosystem](addon/toliss_ecosystem.md)
- [XRoad](addon/xroad.md): GitHub repository link added
- Addon pages revised: Fact corrections ([Follow the Greens](addon/followthegreens.md), [XGS](addon/xgs.md), [AutoGate](addon/autogate.md)), Linux notes added ([ToLiss Ecosystem](addon/toliss_ecosystem.md)), intro rewrite ([XTextureExtractor](addon/xtextureextractor.md))
- [ToLiss Ecosystem](addon/toliss_ecosystem.md) restructured: Overview paragraph, `###` headings instead of bold for better navigation
- New addon pages: [ToLiss Ecosystem](addon/toliss_ecosystem.md) (callouts, automation, boarding, ground services), [XGS](addon/xgs.md) (landing speed analysis), [Follow the Greens](addon/followthegreens.md) (A-SMGCS taxi guidance)
- Addon section expanded: [AutoDGS](addon/autodgs.md), [openSAM](addon/opensam.md), [AutoGate](addon/autogate.md), [DataRefTool](addon/datareftool.md), [Little XpConnect](addon/littlexpconnect.md), [XTextureExtractor](addon/xtextureextractor.md) — new Tools category and expanded Traffic & Ground Ops
- Addon section expanded: New pages [FlyWithLua](addon/flywithlua.md), [AviTab](addon/avitab.md), [XCamera](addon/xcamera.md), [LiveTraffic](addon/livetraffic.md), [Better Pushback](addon/betterpushback.md) — each with background, Linux installation, known issues, and sources
- Existing pages [XRoad](addon/xroad.md) and [AEP](addon/aep.md) revised to follow unified template
- Navigation: Miscellaneous section with categories (Scripting, Cockpit & Camera, Traffic & Ground Ops, Scenery)
- New page [Performance Fundamentals](performance_overview.md): CPU, I/O, and network load dimensions, interactions, frame time as a metric, optimization approaches overview
- [Orthophotography](addon/orthophotography_intro.md), [Performance Fundamentals](performance_overview.md), and [Videos](videos.md): Ortho streaming and performance videos embedded (DE + EN)
- [Performance Fundamentals](performance_overview.md) corrected: SSD latencies, DDR5 bandwidth, and TCP congestion wording refined

### 2026-02-14
- [X-Plane Configuration](xplane/config.md) expanded: Comprehensive udev rules for controllers (identify device IDs, rule examples, distinguish identical devices by USB port)
- [Nvidia Driver](nvidia.md) audited: Added package manager method as recommended approach, corrected persistence mode and modeset claims, marked composition pipeline settings as X11-only, added sources section
- [X-Plane Configuration](xplane/config.md) corrected: Differentiated `__GL_*` variables (`__GL_SYNC_TO_VBLANK` affects Vulkan), added NVIDIA Smooth Motion as experimental option
- [System Tools](systemtools.md) verified: Added missing `sudo` to ioping commands (direct device access requires root)
- [System Tools](systemtools.md) audited: Fixed btop hotkey, clarified cpupower/turbostat/mpstat descriptions, improved glances and fatrace notation, bold table captions
- [System Tuning](systemtuning.md) fact-checked: Corrected scheduler references, removed non-functional kernel parameter, clarified NVMe notes, added sources section
- [Getting Started](begin.md) revised: Merged troubleshooting sections, clarified 32-bit note, added display server link
- Language revision (DE): [Getting Started](begin.md) and [Docker](docker.md) converted to impersonal style
- [Glossary](glossary.md) expanded: New terms PDS and irqbalance
- [System Tuning](systemtuning.md) glossary links added: FPS, Frame Time, Latency, Preemption, NVMe, C-States, EEVDF, PDS, irqbalance
- [System Tuning](systemtuning.md) and [Videos](videos.md): System tuning video embedded (DE + EN)
- [Glossary](glossary.md) expanded: New term SoftIRQ
- [System Tools](systemtools.md) glossary links added: NVMe, C-States, IRQ, CPU Governor, Latency, APST
- New page [System Tuning Introduction](systemtuning_intro.md): Video intro bridging tuning and monitoring topics
- Navigation: System Tools renamed to System Monitoring, grouped under System Tuning


