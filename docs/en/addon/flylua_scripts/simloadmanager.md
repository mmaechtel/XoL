---
description: "SimLoad Manager for X-Plane 12 — FlyWithLua script simulating realistic passenger boarding, cargo loading, and fuel operations via SimBrief."
---
# SimLoad Manager

SimLoad Manager is a [FlyWithLua](../scripting/flywithlua.md) script that simulates realistic passenger boarding, cargo loading, and fuel loading for X-Plane 12. It integrates with SimBrief to import flight plan data (passenger count, cargo weight, fuel amounts) and provides real-time progress bars with dynamic time estimates.

## Background

- **Developer:** RackhamRPL
- **Download:** [X-Plane.org](https://forums.x-plane.org/files/file/93858-simload-manager-realistic-pax-cargo-fuel-ground-operations/)
- **Platforms:** Windows, macOS, Linux (pure Lua)
- **Compatibility:** X-Plane 12
- **Dependencies:** [FlyWithLua NG+](../scripting/flywithlua.md), SimBrief account (required), [SGES](https://forums.x-plane.org/files/file/62296-simple-ground-equipment-services-low-tech-services/) (optional, for visual ground equipment)

The script is actively maintained with frequent updates. It works with any aircraft — no aircraft-specific configuration needed.

## Features

- **Realistic loading simulation:** Passengers board dynamically based on cargo and fuel progress
- **SimBrief integration:** Auto-imports PAX count, cargo weight, fuel, and times from the latest flight plan
- **Multiple speed modes:** Realistic, Fast, Very Fast, or Custom (fully editable timing)
- **Progress visualization:** Real-time progress bars with dynamic time estimates for PAX, cargo, and fuel
- **Loadsheet generation:** Automatic realistic loadsheet (SLMLS system)
- **SGES integration:** When SGES is installed, visual ground equipment (stairs, belt loaders, fuel trucks, cones, passenger flow) accompanies the loading process
- **Sound effects:** Ambient sounds and AI-generated voice alerts during loading
- **AutoDGS compatibility:** Avoids jetway conflicts when AutoDGS is detected
- **API for external tools:** Exposed datarefs and FlyWithLua commands

## Value in Flight Simulation

Instant loading breaks immersion — real turnarounds take time and follow a sequence. SimLoad Manager adds a realistic ground operations phase to each flight: passengers board while cargo is loaded, fuel trucks arrive, and the loadsheet is generated when everything is complete. Combined with SGES, the ramp comes alive during turnaround.

## Installation

**Download:** [X-Plane.org](https://forums.x-plane.org/files/file/93858-simload-manager-realistic-pax-cargo-fuel-ground-operations/)

Place the script files into `Resources/plugins/FlyWithLua/Scripts/`:

- `SimLoadManager.lua` — main script
- `SimLoadManager_loadsheet.lua` — loadsheet module
- `SimLoad-Manager-Sounds/` — sound effects folder

Settings are stored in `FlyWithLua/Modules/simload_settings.txt` (auto-created on first run).

!!! warning "Updating from versions prior to v1.9.0"

    Delete `FlyWithLua/Modules/simload_settings.txt` before updating. It gets auto-recreated on launch. Failing to do so may cause incorrect timings or interface errors.

## Sources

- [SimLoad Manager — X-Plane.org](https://forums.x-plane.org/files/file/93858-simload-manager-realistic-pax-cargo-fuel-ground-operations/)
