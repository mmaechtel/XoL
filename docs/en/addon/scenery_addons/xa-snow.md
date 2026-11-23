---
description: "xa-snow overlays real-world NOAA snow depth data on X-Plane 12 scenery — discontinued since X-Plane 12.4.4 draws accumulated snow itself; native Linux build."
---
# xa-snow

xa-snow is a standalone [plugin](../../glossary.md#plugin) by hotbso that sets X-Plane 12's snow cover from real-world NOAA snow depth data. It downloads accumulated snow depth data from NOAA and applies it to the simulation in real time.

!!! warning "Discontinued"

    The developer has declared xa-snow obsolete and archived the repository: X-Plane 12.4.4 supports accumulated snow natively. The last release remains available, but there will be no further updates. Laminar Research asks users to remove xa-snow before using X-Plane 12.4.4, because it overrides X-Plane's global snow parameters. The developer of [XP SnowState](xp_snowstate.md) (beta) asks for the same.

## Background

- **Developer:** hotbso (Holger Teutsch), originally by zodiac1214
- **Repository:** [github.com/hotbso/xa-snow](https://github.com/hotbso/xa-snow) (open source, GPL-3.0; libspng component BSD-2-Clause)
- **Platforms:** Windows, macOS, Linux (native binaries)
- **Compatibility:** [X-Plane](../../glossary.md#x-plane) 12
- **Status:** Discontinued, repository archived

Before X-Plane 12.4.4, xa-snow set X-Plane's snow cover from the NOAA snow depth at the aircraft position.

## Features

- **NOAA snow data:** Downloads 6-hour accumulated snow depth forecasts covering the entire globe
- **Interpolation:** Tries to smooth changes in snow depth by interpolating in time and space between the NOAA grid points (0.25° lat/lon)
- **Shoreline handling:** Extrapolates inland snow to coastlines that NOAA's IR imagery misses, with optional temperature correction that melts extended coastal snow when ground temperature is high
- **Historical snow:** Optionally tries to load archived snow data for a past date and time, set before starting the flight — the archive covers roughly a year but has gaps
- **Auto update:** Optionally refreshes snow depth data during long flights — resource-heavy and flagged upstream as potentially unstable
- **Runway ice:** The “Lock Elsa Up” option reduces ice on runways and taxiways; on X-Plane 12.4.x it also limits the runway friction to the “puddly” level
- **Manual weather override:** Forces snow downloads even when using manual weather (default: skips download to preserve summer scenery)

**Per-Scenery Configuration**

Legacy (mostly XP11) sceneries show excessive snow on runways and taxiways. Copying `xa-snow.cfg-sample` from the plugin directory into a scenery directory as `xa-snow.cfg` caps the snow depth for that airport.

## Value in Flight Simulation

Before 12.4.4, X-Plane showed the same snow cover everywhere in the scene. xa-snow tied that cover to the NOAA snow depth below the aircraft. Because the whole scene showed that one value, snow could still appear or vanish suddenly despite the smoothing, for example when overflying an isolated snowy peak.

## Installation

**Download:** [GitHub Releases](https://github.com/hotbso/xa-snow/releases)

Extract the ZIP file to `Resources/plugins/`. Updates were delivered through [SkunkCrafts Updater](../tools/skunkcrafts_updater.md) until the project was archived.

### Linux Notes

The Linux binary links against `libcurl-gnutls.so.4` for better compatibility with Steam/Proton environments. On Debian Trixie and later:

```bash
sudo apt install libcurl3t64-gnutls
```

No other Linux-specific issues are known.

## Sources

- [xa-snow — GitHub](https://github.com/hotbso/xa-snow)
- [X-Plane 12.4.4 Release Notes — Laminar Research](https://www.x-plane.com/kb/x-plane-12-4-4-release-notes/)
- [Accumulated Snow — Threshold Forum](https://forum.thresholdx.net/files/file/3871-accumulated-snow/)
