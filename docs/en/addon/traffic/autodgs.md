---
description: "AutoDGS provides automatic docking guidance with VDGS or marshaller at over 5,000 X-Plane gateway airports — no scenery modifications required."
---
# AutoDGS

AutoDGS automatically provides a Docking Guidance System (VDGS or marshaller) at over 5,000 gateway airports — without requiring any scenery modifications.

## Background

- **Developer:** hotbso (also developer of [openSAM](opensam.md) and the [Better Pushback](betterpushback.md) Mod fork)
- **Repository:** [github.com/hotbso/AutoDGS](https://github.com/hotbso/AutoDGS) (open source; code LGPL-2.1, 3D objects/textures CC-BY, Safedock-T2-24 VDGS CC BY-NC-SA)
- **Platforms:** Windows, macOS, Linux (native binaries)
- **Compatibility:** [X-Plane](../../glossary.md#x-plane) 11 and 12 — but on X-Plane 12 the maintained path is [openSAM](opensam.md) v5.x, into which AutoDGS has been merged. The standalone AutoDGS is the legacy line (XP11 via the frozen 4.x release)

!!! warning "Deprecated — merged into openSAM"

    AutoDGS functionality has been folded into [openSAM](opensam.md) v5.x. The standalone plugin is deprecated and no longer supported (support is Discord-only). On X-Plane 12, openSAM v5.x replaces standalone AutoDGS.

The [plugin](../../glossary.md#plugin) is standalone and does not require any other plugins.

## Features

- **Automatic DGS:** Activates after landing (beacon must be on) and searches for suitable stands in taxi direction
- **Two DGS types:** Animated marshaller (ground crew) or electronic VDGS (Safedock-style with azimuth and distance guidance)
- **Preselect mode:** Manual stand selection while on the ground
- **SimBrief integration:** Displays flight number, destination, and timing data on the VDGS (requires the optional [simbrief_hub](../toliss/toliss_ecosystem.md#simbrief_hub) plugin)
- **Jetway docking:** Automatic X-Plane 12 jetway animation on arrival
- **Per-airport configuration:** GUI settings are saved locally

## Value in Flight Simulation

Default airports without custom scenery have no docking guidance system. AutoDGS fills this gap by providing a VDGS or marshaller at every gateway airport with a tower and stands. On X-Plane 12 this functionality now lives in [openSAM](opensam.md) v5.x, which covers both default/gateway airports and SAM-enabled custom sceneries from a single plugin. The earlier model of running standalone AutoDGS in parallel with openSAM — with AutoDGS skipping airports that have a `sam.xml` — is legacy.

## Installation

**Download:** [GitHub Releases](https://github.com/hotbso/AutoDGS/releases)

Extract the ZIP file to `Resources/plugins/`. This creates the `AutoDGS/` folder with the Linux binary at `lin_x64/AutoDGS.xpl`.

No additional system packages are required. There are no known Linux-specific issues. Automatic updates via the [SkunkCrafts Updater](../tools/skunkcrafts_updater.md) are supported.

## Sources

- [AutoDGS — GitHub](https://github.com/hotbso/AutoDGS)
- [AutoDGS — forums.x-plane.org](https://forums.x-plane.org/forums/topic/290222-autodgs-dgs-marshaller-or-vdgs-for-every-gateway-airport/)
