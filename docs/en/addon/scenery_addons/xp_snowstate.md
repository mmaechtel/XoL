---
description: "XP SnowState for X-Plane 12 — native plugin that corrects X-Plane's snow with measured snow depths, separate for valley and mountain; beta with a Linux build."
---
# XP SnowState

XP SnowState is a native [plugin](../../glossary.md#plugin) for [X-Plane](../../glossary.md#x-plane) 12 that compares the snow X-Plane shows with the snow depth actually measured at that place, and corrects it only when X-Plane is clearly off. The package contains a native Linux build.

!!! note "Beta"
    XP SnowState is currently a time-limited beta that runs until 29 November 2026. There is no public download yet, so this page carries no download link. The description follows the README and manual of the beta package and may change until release.

## Background

- **Developer:** Isar Simworks (Munich)
- **Website:** [isarsimworks.de](https://isarsimworks.de/en/)
- **License:** Not yet announced (time-limited beta)
- **Platforms:** Windows 10/11 (64-bit), Linux (64-bit), macOS 11+
- **Compatibility:** X-Plane 12; 12.4.4+ recommended and required for the REGIONAL mode
- **Dependencies:** None (no XPPython3); an internet connection is required

Since 12.4.4, X-Plane draws its own regional snow with Real Weather from a GFS grid with cells about 28 km wide. On flat land that works, but in the mountains one cell averages valley and summit: valleys get too much snow, peaks too little. The developer's test example is Innsbruck, where X-Plane showed 9 cm at the airport while none was lying there.

## Modes

The mode decides how far the plugin intervenes. Only REGIONAL shows valley and mountain differently; in the other writing modes the value applies to the whole visible scene.

| Mode | Behaviour |
|---|---|
| AUTO | Corrects only on a clear deviation (from 3 cm and 50 %) and hands back to X-Plane once it matches again |
| REAL | Always sets the real snow depth |
| REGIONAL | Writes real snow depths into X-Plane's own snow file around the aircraft; X-Plane then spreads the snow itself. Originals are backed up and restored |
| MANUAL | Fixed value for testing |
| WATCH | Writes nothing, only compares |
| OFF | Plugin rests |

REGIONAL works only with X-Plane's Real Weather and corrects the grid points of the existing file — the grid itself stays at 0.25°.

## Features

- **Weather models:** Snow depth from Open-Meteo (DWD ICON, ECMWF, NOAA GFS, MeteoSwiss 1 km), chosen to match the real terrain height
- **Measuring stations:** Worldwide SYNOP reports plus national networks (SLF, GeoSphere Austria, DWD, SNOTEL, JMA, FMI, SMHI), weighted by distance, height difference, and age
- **Runway condition:** Snow, slush, or ice on the runways from the METAR runway state group, derived from the weather, or set manually
- **Controls:** In-sim window and a WebUI in any browser at `http://127.0.0.1:8797/`, in English and German
- **Diagnostics:** Nearby METAR in plain text, stations with height and distance, and X-Plane's own snow value side by side

## Value in Flight Simulation

For winter flights into valley airports such as Innsbruck, Samedan, or Bolzano, the snow at the airport decides how the approach looks and how the runway behaves. XP SnowState leaves X-Plane's regional snow untouched while it is right and steps in only where the coarse grid fails. Unlike plugins that set one value for the whole scene, the REGIONAL mode keeps X-Plane's own regional depiction.

!!! warning "Only one plugin may set the snow"
    The developer asks to remove [xa-snow](xa-snow.md), which sets the snow for the whole scene. [NOAA Weather](noaa_weather.md) writes the same X-Plane snow and runway friction controls: switch off its snow cover and runway friction, or run XP SnowState in WATCH mode.

## Installation

XP SnowState is a native plugin: the folder `XPSnowState` is copied to `Resources/plugins/`. On first start the plugin downloads the worldwide station list once (about 9 MB, a few minutes). The menu **Plugins → XP SnowState Beta** opens the window and the WebUI.

### Linux Notes

The Linux build of the beta depends only on the C library and needs glibc 2.38 or newer — available in Ubuntu 24.04 and Debian 13, but not in Ubuntu 22.04 or Debian 12. The plugin was not yet tested in the simulator for this page; the functional description follows the developer's specification.

## Sources

- [Isar Simworks](https://isarsimworks.de/en/)
- README and manual of the XP SnowState 1.0.0 beta package
