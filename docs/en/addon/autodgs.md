# AutoDGS

AutoDGS automatically provides a Docking Guidance System (VDGS or marshaller) at over 5,000 gateway airports — without requiring any scenery modifications.

## Background

- **Developer:** hotbso (also developer of [openSAM](opensam.md) and the [Better Pushback](betterpushback.md) Mod fork)
- **Repository:** [github.com/hotbso/AutoDGS](https://github.com/hotbso/AutoDGS) (open source, LGPL-2.1)
- **Platforms:** Windows, macOS, Linux (native binaries)
- **Compatibility:** [X-Plane](../glossary.md#x-plane) 12

AutoDGS is actively maintained with regular updates. The [plugin](../glossary.md#plugin) is standalone and does not require any other plugins.

## Features

- **Automatic DGS:** Activates after landing (beacon on, airtime required) and searches for suitable stands in taxi direction
- **Two DGS types:** Animated marshaller (ground crew) or electronic VDGS (Safedock-style with azimuth and distance guidance)
- **Preselect mode:** Manual stand selection while on the ground
- **SimBrief integration:** Displays flight number, destination, and timing data on the VDGS (requires the optional [simbrief_hub](toliss_ecosystem.md#simbrief_hub) plugin)
- **Jetway docking:** Automatic X-Plane 12 jetway animation on arrival
- **Per-airport configuration:** GUI settings are saved locally

## Value in Flight Simulation

Default airports without custom scenery have no docking guidance system. AutoDGS fills this gap by providing a VDGS or marshaller at every gateway airport with a tower and stands. The plugin complements [openSAM](opensam.md): AutoDGS handles default airports, openSAM takes care of SAM-enabled custom sceneries. Both plugins can run in parallel — AutoDGS automatically skips airports with a `sam.xml`.

## Installation

**Download:** [GitHub Releases](https://github.com/hotbso/AutoDGS/releases)

Extract the ZIP file to `Resources/plugins/`. This creates the `AutoDGS/` folder with the Linux binary at `lin_x64/AutoDGS.xpl`.

No additional system packages are required. There are no known Linux-specific issues. Automatic updates via the [SkunkCrafts Updater](skunkcrafts_updater.md) are supported.

## Sources

- [AutoDGS — GitHub](https://github.com/hotbso/AutoDGS)
- [AutoDGS — forums.x-plane.org](https://forums.x-plane.org/forums/topic/290222-autodgs-dgs-marshaller-or-vdgs-for-every-gateway-airport/)
