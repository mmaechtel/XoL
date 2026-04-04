---
description: "SimLoad Manager for X-Plane 12 — FlyWithLua script simulating realistic passenger boarding, cargo loading, and fuel ground operations."
---
# SimLoad Manager

SimLoad Manager is a [FlyWithLua](../scripting/flywithlua.md) script that simulates realistic passenger boarding, cargo loading, and fuel loading for X-Plane 12. It integrates with SimBrief to import flight plan data (passenger count, cargo weight, fuel amounts) and provides real-time progress bars with dynamic time estimates.

## Background

- **Developer:** RackhamRPL
- **Download:** [X-Plane.org](https://forums.x-plane.org/files/file/93858-simload-manager-realistic-pax-cargo-fuel-ground-operations/)
- **Platforms:** Windows, macOS, Linux (pure Lua)
- **Compatibility:** X-Plane 12
- **Dependencies:** [FlyWithLua NG+](../scripting/flywithlua.md), [SGES](https://forums.x-plane.org/files/file/62296-simple-ground-equipment-services-low-tech-services/) (for ground equipment integration)
- **Optional:** SimBrief account (manual entry and Flight Sim Deck also supported as data sources)

The script is actively maintained with frequent updates. It supports Laminar default aircraft (B737-800, A330-300, MD-82), Zibo/Level Up B737 variants, ToLiss aircraft, X-Crafts E-Jets, Flight Factor 757/767, and FPS 747-800. Q4XP is excluded (uses its own tablet system).

## Features

- **Realistic loading simulation:** Passengers board dynamically based on cargo and fuel progress, with automatic unit detection (kg/lbs)
- **Multiple data sources:** SimBrief auto-import, manual entry, or Flight Sim Deck integration
- **Departure and Arrival modes:** Two distinct operational workflows, each with dedicated steps
- **Turnaround and RON:** Automatic new flight plan detection during turnaround, Remain Over Night handling
- **Ground handling stages:** Crew Briefing, Catering & Cleaning integrated into the workflow (Crew Briefing can be skipped via settings)
- **Multiple speed modes:** Realistic, Fast, Very Fast, or Custom (fully editable timing)
- **Progress visualization:** Real-time progress bars with dynamic time estimates for PAX, cargo, and fuel
- **Loadsheet generation:** Automatic realistic loadsheet (SLMLS system), adapts to data source
- **SGES integration:** Automatically triggers stairs, belt loaders, fuel trucks, cones, and passenger flow depending on stand type
- **Beacon-aware safety stops:** All operations halt when the rotating beacon is activated
- **Sound effects:** Ambient sounds and AI-generated voice alerts during loading
- **AutoDGS compatibility:** Jetway/stairs control with conflict avoidance
- **SimChecklist.eu integration:** Connects with the online checklist service
- **Flight save and resume:** Automatic state preservation during mode transitions — interrupted flights can be resumed via "Load Last Flight"
- **ACARS loadsheet uplink:** Loadsheet transmission to ToLiss aircraft via Hoppie network (ACARS)
- **API for external tools:** Custom X-Plane commands and exposed datarefs

## Value in Flight Simulation

Instant loading breaks immersion — real turnarounds take time and follow a sequence. SimLoad Manager adds a realistic ground operations phase to each flight: passengers board while cargo is loaded, fuel trucks arrive, and the loadsheet is generated when everything is complete. Combined with SGES, the ramp comes alive during turnaround.

## Installation

**Download:** [X-Plane.org](https://forums.x-plane.org/files/file/93858-simload-manager-realistic-pax-cargo-fuel-ground-operations/)

Place the following into `Resources/plugins/FlyWithLua/Scripts/`:

- `SimLoadManager.lua` — main script
- `SLM-Data/` — data folder (sounds, loadsheet module, settings)

Do not rename the `SLM-Data/` folder or its contents.

!!! warning "Updating from earlier versions"

    Delete all previous SimLoad Manager files from `FlyWithLua/Scripts/` before installing v3.x. The folder structure has changed — old files like `SimLoadManager_loadsheet.lua` and `SimLoad-Manager-Sounds/` are no longer used.

## Sources

- [SimLoad Manager — X-Plane.org](https://forums.x-plane.org/files/file/93858-simload-manager-realistic-pax-cargo-fuel-ground-operations/)
