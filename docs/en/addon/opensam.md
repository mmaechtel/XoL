# openSAM

openSAM is an open-source replacement for the commercial SAM [plugin](../glossary.md#plugin) (Scenery Animation Manager) by Stairport. It controls animated jetways, VDGS, marshallers, and custom animations in SAM-enabled custom sceneries.

## Background

- **Developer:** hotbso (also developer of [AutoDGS](autodgs.md))
- **Repository:** [github.com/hotbso/openSAM](https://github.com/hotbso/openSAM) (open source, LGPL-2.1)
- **Platforms:** Windows, macOS, Linux (native binaries)
- **Compatibility:** [X-Plane](../glossary.md#x-plane) 11 and X-Plane 12 (separate builds)

openSAM is actively maintained and is the recommended successor to the commercial SAM plugin, which is no longer loaded starting with X-Plane 12.4. openSAM reads the original `sam.xml` configuration files from sceneries and serves as a drop-in replacement.

## Features

- **Animated jetways:** Scans SAM-enabled sceneries at startup and operates their jetways; falls back to X-Plane 12 native jetways
- **VDGS:** Activates after landing (beacon on), shows azimuth and distance guidance to the stand
- **Marshallers:** Animated ground crew guidance
- **Custom animations:** Support for SAM custom animations
- **SAM Seasons emulator:** Built-in (separate SAM Seasons plugin should be removed)
- **SimBrief integration:** Via the companion plugin [simbrief_hub](https://github.com/hotbso/simbrief_hub)
- **Multiplayer support:** Compatible with xPilot, Traffic Global XP, and [LiveTraffic](livetraffic.md)
- **Zero-configuration mode:** Scenery developers can place openSAM library assets in WED without writing custom config files

## Value in Flight Simulation

Many high-quality custom sceneries were developed for the commercial SAM plugin. Since SAM no longer works with X-Plane 12.4, openSAM takes over this role as a free open-source replacement. Combined with [AutoDGS](autodgs.md) (for default airports), this provides full coverage: openSAM for custom sceneries, AutoDGS for all other airports.

## Installation

**Download:** [GitHub Releases](https://github.com/hotbso/openSAM/releases)

The ZIP file contains two components:

- `openSAM` → extract to `Resources/plugins/`
- `openSAM_Library` → extract to `Custom Scenery/`

In `scenery_packs.ini`, `openSAM_Library` must be placed above `SAM_Library`. If the commercial SAM plugin is still installed, it should be removed (the `SAM_Library` can remain if needed by sceneries).

No additional system packages are required. There are no known Linux-specific issues. Automatic updates via the [SkunkCrafts Updater](skunkcrafts_updater.md) are supported.

## Sources

- [openSAM — GitHub](https://github.com/hotbso/openSAM)
- [openSAM — forums.x-plane.org](https://forums.x-plane.org/index.php?/files/file/90865-opensam-an-open-source-replacement-for-sam-on-xp12/)
