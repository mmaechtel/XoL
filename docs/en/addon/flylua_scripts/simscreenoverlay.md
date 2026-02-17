# SimScreen Overlay

SimScreen Overlay is a [FlyWithLua](../scripting/flywithlua.md) script that adds a clean flight information overlay to X-Plane 12 screenshots. The overlay appears only during the screenshot capture — no visual clutter while flying.

## Background

- **Developer:** RackhamRPL
- **Download:** [x-plane.to](https://x-plane.to/file/1910/simscreen-overlay)
- **Platforms:** Windows, macOS, Linux (pure Lua)
- **Compatibility:** X-Plane 12
- **Dependencies:** [FlyWithLua NG+](../scripting/flywithlua.md), SimBrief account (optional, for automatic flight data import)

## Features

- **Screenshot overlay:** Flight information (aircraft type, departure, arrival) displayed at the bottom-left of screenshots
- **SimBrief integration:** Automatic import of flight plan data via Pilot ID
- **Editable fields:** Aircraft type, departure ICAO, and arrival ICAO can be entered manually for VFR or non-SimBrief flights
- **Capture-only display:** Overlay activates only during the screenshot moment
- **Settings UI:** Configurable via `FlyWithLua Macros > SimScreen Overlay: Settings`

## Value in Flight Simulation

Screenshots without context lose their story — aircraft type, route, and conditions are not visible. SimScreen Overlay automatically stamps this information onto screenshots without requiring post-processing. Since the overlay only appears during capture, it does not affect normal flying.

## Installation

**Download:** [x-plane.to](https://x-plane.to/file/1910/simscreen-overlay)

Place `SimScreenOverlay.lua` into `Resources/plugins/FlyWithLua/Scripts/`.

After installation, assign a key to the command `FlyWithLua / SimScreen_Overlay / Screenshot` in X-Plane's keyboard settings.

## Sources

- [SimScreen Overlay — x-plane.to](https://x-plane.to/file/1910/simscreen-overlay)
