---
description: "SimLoad Manager for X-Plane 12 — native plugin for boarding, cargo, fuel and animated ground ops with Ground Planner; runs on Linux without SGES."
---
# SimLoad Manager

SimLoad Manager is a native [plugin](../../glossary.md#plugin) for [X-Plane](../../glossary.md#x-plane) 12 that simulates realistic passenger boarding, cargo loading, and fueling, and brings its own ground handling: animated vehicles, passengers, and crew, laid out per aircraft in the built-in Ground Planner. It works without SGES or any other plugin.

## Background

- **Developer:** RackhamRPL
- **Download:** [X-Plane.org](https://forums.x-plane.org/files/file/93858-simload-manager-realistic-pax-cargo-fuel-ground-operations/)
- **Platforms:** Windows, macOS, Linux (native `lin_x64` build)
- **Compatibility:** X-Plane 12.4.4 or newer
- **Dependencies:** None — [SGES](../flylua_scripts/sges.md) is optional and only then requires [FlyWithLua NG+](../scripting/flywithlua.md)
- **Optional:** SimBrief account (an enriched manual flight plan is also supported)

Supported aircraft include the Laminar default fleet (737-800, A330-300, MD-82, C750 and most smaller Laminar aircraft), Zibo/LevelUp 737-600 to 900ER, all ToLiss aircraft, X-Crafts E-Jets and ERJ, Flight Factor 757/767 and A320, FPS 747-800, Rotate MD80, FlyJSim 732, and the Colimata Concorde FXP. For the Q4XP, SimLoad Manager automatically disables its weight and fuel integration.

## Features

- **Loading simulation:** Loading and unloading of passengers, cargo, and fuel, with automatic kg/lbs detection
- **Load variation:** No-shows, standbys, fuel top-up, tankering, a low-cost mode, and random events
- **Ground Ops:** All vehicles are managed by SimLoad Manager itself — animated X-Plane vehicles plus 3D models by Isar Simworks (stairs, ULD loaders, fresh and waste water trucks); every vehicle is optional per profile
- **Passengers and crew:** Animated passengers and crew
- **Ground Planner:** Editor for per-aircraft ground profiles — vehicle positions, forward and reverse routes, wait times, height adjustment, and in-sim testing of single vehicles or whole stages
- **Vehicle beacons:** On, while driving, or off
- **Ground handling details:** GPU management per aircraft type, a checklist, buses and stairs arriving after catering
- **Data sources:** SimBrief import or an enriched manual flight plan; automatic flight plan detection
- **Workflows:** Departure and Arrival modes, Turnaround and RON, Crew Briefing, Catering and Cleaning
- **Speed modes:** Realistic, Fast, Very Fast, or Custom
- **Safety stops:** Beacon-aware halt of all operations, plus a "Don't touch the chocks" rule
- **Loadsheet:** SLMLS loadsheet, also as ACARS uplink via Hoppie or SayIntentions.ai (addressed to the flight number or SimBrief callsign)
- **Sound:** Ambient sounds, AI voice alerts, and boarding music (custom WAV files supported)
- **Web server:** The UI can be opened on a second screen, a tablet, or the AviTab browser
- **Integrations:** Custom commands, Flight Sim Deck, SimChecklist.eu, auto-save; UI languages EN/FR/IT/ES/DE

## Value in Flight Simulation

A turnaround takes time and follows a sequence. SimLoad Manager adds this phase to every flight: vehicles drive up to the aircraft, passengers board while cargo is loaded and fuel is pumped, and the loadsheet arrives when everything is complete. The ground vehicles are part of the plugin, so a separate ground-service add-on is not required. With [XP CabinState](../cockpit/xp_cabinstate.md), SimLoad Manager can also drive crew and boarding inside the cabin simulation.

## Installation

**Download:** [X-Plane.org](https://forums.x-plane.org/files/file/93858-simload-manager-realistic-pax-cargo-fuel-ground-operations/)

Extract the archive and copy the complete `SimLoadManager/` folder into `Resources/plugins/` — do not rename it. After starting X-Plane, the plugin is available under **Plugins → SimLoad Manager**.

- **Settings:** Stored in `Output/preferences/simload_settings.txt` — deleting the plugin folder during an update does not reset them
- **Ground profiles:** Stored in `Resources/plugins/SimLoadManager/profiles/` and can be shared; the builds ship without profiles; the developer links default profiles and a guide
- **Updates:** Via the [SkunkCrafts Updater](../tools/skunkcrafts_updater.md)

!!! warning "Switching from the FlyWithLua version"

    Remove the previous FlyWithLua version of SimLoad Manager from `FlyWithLua/Scripts/` before installing the plugin. The package contains an optional SGES bridge (`FlyWithLua_Scripts/SimLoadManager_SGES_bridge.lua` and `lua/slm5_sges.lua`). It is only needed when SGES is used.

### Linux Notes

The package contains a native `lin_x64/SimLoadManager.xpl`. This setup has been successfully tested on Linux — the X-Plane log shows the plugin loading from the `lin_x64` folder. For the SimBrief import, the Linux build uses the system libcurl (`libcurl.so.4`), which most distributions ship by default.

## Sources

- [SimLoad Manager — X-Plane.org](https://forums.x-plane.org/files/file/93858-simload-manager-realistic-pax-cargo-fuel-ground-operations/)
