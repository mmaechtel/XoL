# xa-snow

xa-snow is a standalone [plugin](../glossary.md#plugin) by hotbso that overlays real-world snow coverage on X-Plane 12 scenery. It downloads accumulated snow depth data from NOAA and applies it to the simulation in real time.

## Background

- **Developer:** hotbso (Holger Teutsch), originally by zodiac1214
- **Repository:** [github.com/hotbso/xa-snow](https://github.com/hotbso/xa-snow) (open source, LGPL-2.1)
- **Platforms:** Windows, macOS, Linux (native binaries)
- **Compatibility:** [X-Plane](../glossary.md#x-plane) 12

xa-snow replaces X-Plane's uniform regional snow with location-specific coverage based on actual weather data. The plugin is actively maintained with regular releases.

## Features

- **NOAA snow data:** Downloads 6-hour accumulated snow depth forecasts covering the entire globe
- **Spatial interpolation:** Overcomes X-Plane's limitation of uniform regional snow coverage at 0.25° lat/lon resolution
- **Historical snow:** Access archived snow data for specific dates (365-day archive)
- **Auto update:** Optionally updates snow coverage during flight as you move across regions
- **Runway friction:** Adjustable runway ice behavior via "Lock Elsa Up" option (reduces runway friction in X-Plane 12.4.x+)
- **Manual weather override:** Forces snow downloads even when using manual weather (default: skips download to preserve summer scenery)

**Per-Scenery Configuration**

Scenery developers can include `xa-snow.cfg` files to fine-tune snow behavior for specific airports or regions.

## Value in Flight Simulation

X-Plane's built-in snow is applied uniformly across large regions — either everything is covered or nothing is. xa-snow brings seasonal realism by showing snow where it actually exists: snow-covered Alps next to green valleys, realistic treeline transitions, and accurate coastal snow boundaries. Combined with real weather, this creates convincing winter operations.

## Installation

**Download:** [GitHub Releases](https://github.com/hotbso/xa-snow/releases)

Extract the ZIP file to `Resources/plugins/`. After the initial installation, [SkunkCrafts Updater](skunkcrafts_updater.md) handles automatic updates (PROD or BETA channel).

### Linux Notes

Since v2.3.1, the Linux binary links against `libcurl4-gnutls` for better compatibility with Steam/Proton environments. On Debian-based systems:

```bash
sudo apt install libcurl4-gnutls-dev
```

No other Linux-specific issues are known.

## Sources

- [xa-snow — GitHub](https://github.com/hotbso/xa-snow)
- [Accumulated Snow — Threshold Forum](https://forum.thresholdx.net/files/file/3871-accumulated-snow/)
