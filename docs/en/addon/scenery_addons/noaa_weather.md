---
description: "NOAA Weather adds snow cover, treated-runway friction and a METAR window (NOAA, IVAO, VATSIM) to X-Plane 12 on Linux. Requires XPPython3."
---
# NOAA Weather

NOAA Weather is a Python-based [plugin](../../glossary.md#plugin) that adds snow cover, a runway friction adjustment, and METAR monitoring to X-Plane 12. It works alongside X-Plane's built-in Real Weather engine rather than replacing it.

## Background

- **Developer:** Antonio Golfari (biuti), originally by Joan Perez i Cauhe
- **Repository:** [github.com/biuti/XplaneNoaaWeather](https://github.com/biuti/XplaneNoaaWeather) (open source, GPLv2 or later)
- **Platforms:** Windows, macOS, Linux
- **Compatibility:** X-Plane 12.4.4+ for the current pre-releases; NOAA Weather 12.4 remains for X-Plane 12.4 before 12.4.4
- **Prerequisite:** [XPPython3](../scripting/xppython3.md) 4.8.0+ for the current pre-releases, 4.6.0+ for NOAA Weather 12.4

Since X-Plane 12 already uses NOAA GFS data for its own weather engine, the plugin does not act as a weather replacement — according to the developer it mostly monitors what Real Weather is doing. From X-Plane 12.4.4 on, the Real Weather files contain snow depth, so the plugin no longer downloads GFS data itself. The plugin is actively maintained.

## Features

- **Snow cover:** Reads the snow depth from X-Plane's Real Weather files at the aircraft position and sets the snow cover from it — according to the developer, X-Plane 12.4.4 does not yet interpret this data correctly on its own
- **Snow value retention:** Reuses the last valid snow depth within a 70 nm radius when no value is available at the position, for example over water
- **Runway friction:** Simulates tarmac treatment in cold weather by reducing the slipperiness X-Plane derives from icing conditions
- **METAR window:** Displays the X-Plane 12 Real Weather METAR alongside an external source (NOAA, IVAO, or VATSIM) for any airport
- **Real Weather monitoring:** Shows in real time what X-Plane's internal weather engine is actually producing

## Settings

The settings are in the menu **Plugins → XP NOAA Weather → Configuration**. Only two of them change the simulator; the METAR settings affect the display only.

| Setting | Default | Effect |
|---|---|---|
| Accumulated Snow | on | Sets the snow cover for the whole visible scene |
| Adjusted Runway Friction | on | Lowers the runway friction value as on a treated runway |
| METAR Source | NOAA | Source shown in the METAR window: NOAA, IVAO, or VATSIM |
| METAR Decoding | off | Adds a decoded text to the raw METAR |

!!! tip "Online flying"
    For flights on VATSIM or IVAO, set the METAR source to the network. The window then shows the report the controllers work with; the weather in the simulator still comes from X-Plane's Real Weather. The developer points out that Real Weather can differ from what ATC, ATIS, and other pilots see.

## Limits of the Snow Cover

The plugin sets a single snow value for the whole visible scene, taken from the GFS grid cell at the aircraft position. Such a cell is roughly 28 km wide and averages valley and summit, so mountains and valleys always show the same amount of snow. [XP SnowState](xp_snowstate.md) addresses this case with height-aware data.

!!! warning "Only one plugin may set the snow"
    NOAA Weather and XP SnowState write the same X-Plane snow and runway friction controls. When both are active, switch off **Accumulated Snow** and **Adjusted Runway Friction** in NOAA Weather; the METAR window keeps working.

## Value in Flight Simulation

X-Plane 12 sources its weather from NOAA and has shipped snow depth with Real Weather since 12.4.4, but the depiction is not yet reliable. NOAA Weather turns this data into a consistent snow cover, tames the runway friction, and adds a METAR comparison that is particularly useful for online flying on IVAO or VATSIM. Since commercial weather alternatives like Active Sky and xEnviro do not support Linux, NOAA Weather is one of the few options available to Linux users. A related addon is [AutoHaze](../flylua_scripts/autohaze.md), which recomputes the atmospheric haze from measured aerosol data.

## Installation

**Download:** [GitHub Releases](https://github.com/biuti/XplaneNoaaWeather/releases)

[XPPython3](../scripting/xppython3.md) must already be installed. The current pre-releases come as a single folder that is copied to `Resources/plugins/PythonPlugins/`:

```
Resources/plugins/PythonPlugins/
└── PI_NOAAWeather/
    ├── PI_NOAAWeather.py
    ├── bin/
    ├── scripts/
    └── version.txt
```

Before installing, completely remove any previous version (do not overwrite) — in particular the old layout with `PI_noaaWeather.py` and the folder `noaaweather/`.

### Linux Notes

The plugin ships a pre-compiled `linux-wgrib2` binary (built on Ubuntu 20.04 LTS) for decoding GRIB2 files. It is compatible with most current distributions. If the bundled binary does not work on your system, wgrib2 can be compiled from source.

XPPython3 loads plugins packaged as a folder only from version 4.8.0 on. [XOrganizer](../tools/xorganizer.md) lists only `PI_*.py` files directly in `PythonPlugins/` and therefore does not show the plugin.

## Sources

- [NOAA Weather — GitHub](https://github.com/biuti/XplaneNoaaWeather)
- [NOAA Weather — X-Plane.org Forum](https://forums.x-plane.org/forums/topic/72313-noaa-weather-plugin/)
- [XPPython3 — Documentation](https://xppython3.readthedocs.io/en/latest/index.html)
