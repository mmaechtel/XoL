---
description: "SimBrief Simple OFP for X-Plane — FlyWithLua script that downloads and displays your SimBrief flight plan as an in-simulator overlay."
---
# SimBrief Simple OFP

SimBrief Simple OFP is a [FlyWithLua](../scripting/flywithlua.md) script that downloads the latest flight plan from SimBrief and displays it as a readable Operational Flight Plan (OFP) directly inside X-Plane.

## Background

- **Developer:** HurricanetwistR
- **Download:** [X-Plane.org](https://forums.x-plane.org/files/file/75422-simbrief-simple-operational-flight-plan-ofp-xp1112/)
- **Platforms:** Windows, macOS, Linux (pure Lua)
- **Compatibility:** X-Plane 11/12
- **Dependencies:** [FlyWithLua NG+](../scripting/flywithlua.md), SimBrief account (free), xml2lua library (included in download)

The script connects to the SimBrief API using the user's SimBrief username, downloads the flight plan in XML format, and parses it into a formatted OFP display. Two layout options are available. Accessible via `Plugins > FlyWithLua > FlyWithLua Macros`.

## Features

- **SimBrief API integration:** Automatic download of the latest generated flight plan
- **Two OFP layouts:** Different display formats to choose from
- **METAR abbreviations:** Decoded weather information in the OFP
- **SELCAL codes:** Aircraft SELCAL code displayed in layout 1
- **Local times:** Local time conversion for departure and arrival
- **Multiple alternates:** Support for flight plans with multiple alternate airports

## Value in Flight Simulation

Viewing the OFP normally requires switching to a browser or second monitor. SimBrief Simple OFP brings the essential flight plan data into X-Plane as an overlay — useful for quick reference to fuel figures, route information, and weather data without leaving the simulator.

## Installation

**Download:** [X-Plane.org](https://forums.x-plane.org/files/file/75422-simbrief-simple-operational-flight-plan-ofp-xp1112/)

The download contains:

- `SIMBRIEF_SIMPLE_OFP.lua` and `SIMBRIEF_SIMPLE_OFP_Lib.lua` — place both in `Resources/plugins/FlyWithLua/Scripts/`
- `xml2lua` module — place in `Resources/plugins/FlyWithLua/Modules/`

Enter the SimBrief username in the script configuration before first use.

## Sources

- [SimBrief Simple OFP — X-Plane.org](https://forums.x-plane.org/files/file/75422-simbrief-simple-operational-flight-plan-ofp-xp1112/)
