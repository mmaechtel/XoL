---
description: "XP SnowState for X-Plane 12 — native plugin that corrects X-Plane's snow with real snow depths from measuring stations and weather models; beta with a Linux build."
---
# XP SnowState

XP SnowState is a native [plugin](../../glossary.md#plugin) for [X-Plane](../../glossary.md#x-plane) 12 that compares the snow X-Plane shows with real snow depths from measuring stations and weather models, and corrects it only when X-Plane is clearly off. The plugin is currently in beta and includes a native Linux build.

## Background

- **Developer:** Isar Simworks (Munich)
- **Website:** [isarsimworks.de](https://isarsimworks.de/en/)
- **License:** Not yet announced
- **Status:** Beta, available through the developer's Discord channel
- **Platforms:** Windows 10/11 (64-bit), Linux (64-bit), macOS 11+
- **Compatibility:** X-Plane 12; 12.4.4+ recommended and required for the REGIONAL mode
- **Dependencies:** None (no XPPython3); an internet connection is required

Since 12.4.4, X-Plane draws its own regional snow with Real Weather from a GFS grid of 0.25° (cells about 28 km wide). On flat land that works, but in the mountains one cell averages valley and summit: valleys get too much snow, peaks too little. The developer's test example is Innsbruck, where X-Plane showed 9 cm at the airport although there was no snow on the ground.

## Features

- **Weather models:** Snow depth from Open-Meteo (DWD ICON, ECMWF, NOAA GFS, MeteoSwiss 1 km), chosen to match the real terrain height
- **Measuring stations:** Worldwide SYNOP reports plus national networks (SLF, GeoSphere Austria, DWD, SNOTEL, JMA, FMI, SMHI), weighted by distance, height difference, and age
- **Runway condition:** Snow, slush, or ice on the runways from the METAR runway state group, derived from the weather, or set manually
- **Controls:** In-sim window and a WebUI in any browser at `http://127.0.0.1:8797/`, in English and German
- **Diagnostics:** Nearby METAR in plain text, stations with height and distance, and X-Plane's own snow value side by side

## Modes

The mode decides how far the plugin intervenes. The default is AUTO.

| Mode | Behaviour |
|---|---|
| AUTO | Corrects only on a clear deviation (at least 3 cm and 50 % off) and hands back to X-Plane once it matches again |
| REAL | Always sets the real snow depth |
| REGIONAL | Writes real snow depths into X-Plane's own snow file around the aircraft; X-Plane then spreads the snow itself. Originals are backed up and restored |
| MANUAL | Fixed value for testing |
| WATCH | Writes nothing, only compares |
| OFF | Plugin inactive |

In AUTO, REAL, and MANUAL the snow value applies to the whole visible scene. REGIONAL works only with X-Plane's Real Weather: it gives every grid point of X-Plane's snow file the depth that fits its terrain height and, on the ground and on approach, sets the exact value at the aircraft position. The grid stays at 0.25°, so the snow differs from region to region, but not between a valley and the summit right above it.

## Value in Flight Simulation

For winter flights into valley airports such as Innsbruck, Samedan, or Bolzano, the snow at the airport decides how the approach looks and how the runway behaves. In AUTO mode XP SnowState leaves X-Plane's snow alone as long as it is correct and corrects it when it is clearly off. The REGIONAL mode goes further: instead of one value for the whole scene it corrects X-Plane's regional snow, and on the ground and on approach the value at the aircraft is exact. The developer recommends it for mountains and valley airports.

!!! warning "Only one plugin may set the snow"

    The developer asks to remove [xa-snow](xa-snow.md), which interferes with X-Plane's own snow and with XP SnowState. [NOAA Weather](noaa_weather.md) writes the same X-Plane datarefs for snow and runway friction: switch off **Accumulated Snow** there. For the runway friction there are two ways: switch off **Adjusted Runway Friction** in NOAA Weather as well, or set **Set runway condition** to off in XP SnowState and leave the friction to NOAA Weather.

## Installation

**Download:** During the beta through the developer's Discord channel

XP SnowState is a native plugin: the folder `XPSnowState` is copied to `Resources/plugins/`. On first start the plugin downloads the worldwide station list once (about 9 MB, a few minutes). The menu **Plugins → XP SnowState Beta** opens the window and the WebUI.

### Linux Notes

The Linux build of the beta depends only on the C library and needs glibc 2.38 or newer — available in Ubuntu 24.04 and Debian 13, but not in Ubuntu 22.04 or Debian 12. The plugin has not been tested in the simulator for this page; the description follows the README and manual of the beta package.

## Sources

- [Isar Simworks](https://isarsimworks.de/en/)
- README and manual of the XP SnowState 1.0.0 beta package
