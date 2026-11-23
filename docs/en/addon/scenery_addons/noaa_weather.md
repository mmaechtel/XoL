---
description: "NOAA Weather adds snow cover, treated-runway friction and a METAR window (NOAA, IVAO, VATSIM) to X-Plane 12 on Linux. Requires XPPython3."
---
# NOAA Weather

NOAA Weather is a Python-based [plugin](../../glossary.md#plugin) that adds snow cover, a runway friction adjustment, and METAR monitoring to X-Plane 12. It works alongside X-Plane's built-in Real Weather engine rather than replacing it.

## Background

- **Developer:** Antonio Golfari (biuti), originally by Joan Perez i Cauhe
- **Repository:** [github.com/biuti/XplaneNoaaWeather](https://github.com/biuti/XplaneNoaaWeather) (open source, GPLv2 or later)
- **Platforms:** Windows, macOS, Linux
- **Compatibility:** X-Plane 12.4.4 or newer (current pre-releases); for X-Plane 12.4.0–12.4.3 use the release NOAA Weather 12.4
- **Prerequisite:** [XPPython3](../scripting/xppython3.md) 4.8.0+ for the current pre-releases, 4.6.0+ for NOAA Weather 12.4

X-Plane 12 already builds its weather on NOAA GFS data, so the plugin does not generate weather of its own; according to the developer it mostly monitors what Real Weather is doing. From X-Plane 12.4.4 on, the Real Weather files contain snow depth, and the plugin no longer downloads GFS data itself.

## Features

- **Snow cover:** Reads the snow depth from X-Plane's Real Weather files at the aircraft position and sets the snow cover from it — according to the developer, X-Plane 12.4.4 does not yet interpret this data correctly on its own
- **Last snow value:** Keeps the last valid snow depth for up to 70 nm when no value is available at the position, for example over water
- **Runway friction:** Simulates runway treatment in cold weather by reducing the slipperiness X-Plane derives from icing conditions
- **METAR window:** Displays the METAR from X-Plane's Real Weather alongside an external source (NOAA, IVAO, or VATSIM) for any airport
- **Weather info window:** Shows the live Real Weather values at the aircraft position: wind, visibility, temperature, pressure, and runway friction

## Settings

The settings are in the menu **Plugins → XP NOAA Weather → Configuration**. Only two of them change the simulator; the METAR settings affect the display only.

| Setting | Default | Effect |
|---|---|---|
| Accumulated Snow | on | Sets the snow cover for the whole visible scene |
| Adjusted Runway Friction | on | Reduces the slipperiness, as on a treated runway |
| METAR Source | NOAA | Source shown in the METAR window: NOAA, IVAO, or VATSIM |
| METAR Decoding | off | Adds a decoded text to the raw METAR |

!!! tip "Online flying"

    On VATSIM or IVAO, controllers and ATIS work with the network METAR, which can differ from X-Plane's Real Weather. Set the METAR source to the network to see that report; the weather in the simulator still comes from Real Weather.

## Limits of the Snow Cover

The plugin applies one snow value to the whole visible scene, taken from the GFS grid cell at the aircraft position. That cell is roughly 28 km wide and averages valley and summit. Mountains and valleys therefore show the same snow, and in mountainous terrain the value fits neither. [XP SnowState](xp_snowstate.md) (beta) corrects the snow with data that takes the terrain height into account.

!!! warning "Only one plugin may set the snow"

    NOAA Weather and XP SnowState write the same X-Plane datarefs for snow and runway friction. When both are active, switch off **Accumulated Snow** and **Adjusted Runway Friction** in NOAA Weather, or run XP SnowState in WATCH mode. The METAR window keeps working either way.

## Value in Flight Simulation

X-Plane's own snow depiction is not yet reliable. NOAA Weather applies the Real Weather snow depth as snow cover around the aircraft, reduces runway slipperiness in icing conditions, and adds a METAR comparison. Commercial weather engines such as Active Sky and xEnviro do not run on Linux; NOAA Weather does not replace them. A related addon is [AutoHaze](../flylua_scripts/autohaze.md), which recomputes the atmospheric haze from measured aerosol data.

## Installation

**Download:** [GitHub Releases](https://github.com/biuti/XplaneNoaaWeather/releases)

[XPPython3](../scripting/xppython3.md) must already be installed. On X-Plane 12.4.4 or newer, pick the latest release marked *Pre-release*. It comes as a single folder that is copied to `Resources/plugins/PythonPlugins/`:

```
Resources/plugins/PythonPlugins/
└── PI_NOAAWeather/
    ├── PI_NOAAWeather.py
    ├── bin/
    ├── scripts/
    └── version.txt
```

Before installing, completely remove any previous version (do not overwrite) — in particular the old layout with `PI_noaaWeather.py` and the folder `noaaweather/`. [XOrganizer](../tools/xorganizer.md) lists only `PI_*.py` files directly in `PythonPlugins/` and does not show the plugin; it still loads.

### Linux Notes

The plugin ships a pre-compiled `linux-wgrib2` binary (built on Ubuntu 20.04 LTS) for reading the Real Weather GRIB2 files. It is compatible with most current distributions. If it does not run on a system, a self-compiled wgrib2 can replace `bin/linux-wgrib2` in the plugin folder.

No other Linux-specific issues are known.

## Sources

- [NOAA Weather — GitHub](https://github.com/biuti/XplaneNoaaWeather)
- [NOAA Weather — X-Plane.org Forum](https://forums.x-plane.org/forums/topic/72313-noaa-weather-plugin/)
- [XPPython3 — Documentation](https://xppython3.readthedocs.io/en/latest/index.html)
