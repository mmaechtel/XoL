---
description: "openSAM is a free open-source replacement for the SAM plugin — controlling animated jetways, VDGS, and marshallers in X-Plane custom sceneries."
---
# openSAM

openSAM is an open-source replacement for the commercial SAM [plugin](../../glossary.md#plugin) (Scenery Animation Manager) by Stairport. It controls animated jetways, VDGS, marshallers, and custom animations in SAM-enabled custom sceneries.

## Background

- **Developer:** hotbso (also developer of [AutoDGS](autodgs.md))
- **Repository:** [github.com/hotbso/openSAM](https://github.com/hotbso/openSAM) (open source; code LGPL-2.1, assets/VDGS CC-BY and CC BY-NC-SA)
- **Platforms:** Windows, macOS, Linux (native binaries)
- **Compatibility:** [X-Plane](../../glossary.md#x-plane) 12 only — the current openSAM (v5.x) runs on XP12 exclusively. XP11 users must stick to a legacy 4.x release, which is no longer actively developed

openSAM is actively maintained and is the recommended successor to the commercial SAM plugin, which is no longer loaded starting with X-Plane 12.4. openSAM reads the original `sam.xml` configuration files from sceneries and serves as a drop-in replacement.

## Features

- **Animated jetways:** Scans SAM-enabled sceneries at startup and operates their jetways; falls back to X-Plane 12 native jetways
- **VDGS:** Activates after landing (beacon on), shows azimuth and distance guidance to the stand
- **Marshallers:** Animated ground crew guidance
- **Custom animations:** Support for SAM custom animations
- **SAM Seasons emulator:** Built-in (separate SAM Seasons plugin should be removed)
- **SimBrief integration:** Via the companion plugin [simbrief_hub](../toliss/toliss_ecosystem.md#simbrief_hub)
- **Multiplayer support:** Compatible with xPilot, Traffic Global XP, and [LiveTraffic](livetraffic.md)
- **Zero-configuration mode:** Scenery developers can place openSAM library assets in WED without writing custom config files

## Value in Flight Simulation

Many high-quality custom sceneries were developed for the commercial SAM plugin. Since SAM no longer works with X-Plane 12.4, openSAM takes over this role as a free open-source replacement. As of v5.x, openSAM also incorporates [AutoDGS](autodgs.md), so it covers default gateway airports as well as SAM-enabled custom sceneries from a single plugin — a separate AutoDGS installation is no longer needed on X-Plane 12.

## Installation

**Download:** [GitHub Releases](https://github.com/hotbso/openSAM/releases)

The ZIP file contains two components:

- `openSAM` → extract to `Resources/plugins/`
- `openSAM_Library` → extract to `Custom Scenery/`

In `scenery_packs.ini`, `openSAM_Library` must be placed above `SAM_Library`. Before starting X-Plane, remove any existing installations of the commercial SAM plugin, [AutoDGS](autodgs.md), or the standalone SAM Seasons emulator — openSAM includes both AutoDGS and Seasons emulation.

No additional system packages are required. There are no known Linux-specific issues. Automatic updates via the [SkunkCrafts Updater](../tools/skunkcrafts_updater.md) are supported.

## Sources

- [openSAM — GitHub](https://github.com/hotbso/openSAM)
- [openSAM — forums.x-plane.org](https://forums.x-plane.org/index.php?/files/file/90865-opensam-an-open-source-replacement-for-sam-on-xp12/)
