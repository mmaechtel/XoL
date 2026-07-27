---
description: "xa-snow overlays real-world NOAA snow depth data on X-Plane 12 scenery, replacing uniform regional snow with location-specific coverage on Linux."
---
# xa-snow

xa-snow is a standalone [plugin](../../glossary.md#plugin) by hotbso that overlays real-world snow coverage on X-Plane 12 scenery. It downloads accumulated snow depth data from NOAA and applies it to the simulation in real time.

## Background

- **Developer:** hotbso (Holger Teutsch), originally by zodiac1214
- **Repository:** [github.com/hotbso/xa-snow](https://github.com/hotbso/xa-snow) (open source, GPL-3.0; libspng component BSD-2-Clause)
- **Platforms:** Windows, macOS, Linux (native binaries)
- **Compatibility:** [X-Plane](../../glossary.md#x-plane) 12

xa-snow replaces X-Plane's uniform regional snow with location-specific coverage based on actual weather data. The plugin is actively maintained with regular releases.

## Features

- **NOAA snow data:** Downloads 6-hour accumulated snow depth forecasts covering the entire globe
- **Spatial interpolation:** Overcomes X-Plane's limitation of uniform regional snow coverage at 0.25° lat/lon resolution
- **Shoreline handling:** Extrapolates inland snow to coastlines that NOAA's IR imagery misses, with optional temperature correction that melts extended coastal snow when ground temperature is high
- **Historical snow:** Optionally loads archived snow data for a past date, set before starting the flight — the archive covers roughly a year but has gaps
- **Auto update:** Optionally refreshes snow depth data during long flights — resource-heavy and flagged upstream as potentially unstable
- **Runway friction:** Adjustable runway ice behavior via "Lock Elsa Up" option (reduces runway friction in X-Plane 12.4.x+)
- **Manual weather override:** Forces snow downloads even when using manual weather (default: skips download to preserve summer scenery)

**Per-Scenery Configuration**

Legacy (mostly XP11) sceneries show excessive snow on runways and taxiways. Copying `xa-snow.cfg-sample` from the plugin directory into a scenery directory as `xa-snow.cfg` caps the snow depth for that airport.

## Value in Flight Simulation

X-Plane's built-in snow is applied uniformly across large regions — either everything is covered or nothing is. xa-snow brings seasonal realism by showing snow where it actually exists: snow-covered Alps next to green valleys, realistic treeline transitions, and accurate coastal snow boundaries. Combined with real weather, this creates convincing winter operations.

## Installation

**Download:** [GitHub Releases](https://github.com/hotbso/xa-snow/releases)

Extract the ZIP file to `Resources/plugins/`. After the initial installation, [SkunkCrafts Updater](../tools/skunkcrafts_updater.md) handles automatic updates (PROD or BETA channel).

### Linux Notes

The Linux binary links against `libcurl-gnutls.so.4` for better compatibility with Steam/Proton environments. On Debian Trixie and later:

```bash
sudo apt install libcurl3t64-gnutls
```

No other Linux-specific issues are known.

## Sources

- [xa-snow — GitHub](https://github.com/hotbso/xa-snow)
- [Accumulated Snow — Threshold Forum](https://forum.thresholdx.net/files/file/3871-accumulated-snow/)
