---
description: "TOI Cabin Ready: FlyWithLua script that automates the Cabin Ready ECAM call for ToLiss Airbus aircraft in X-Plane 12 during departure and approach."
---
# TOI Cabin Ready

TOI Cabin Ready is a [FlyWithLua](../scripting/flywithlua.md) script that automatically sends the "Cabin Ready" ECAM notification for ToLiss Airbus aircraft, eliminating the need to manually press the FWD CALL button.

## Background

- **Developer:** cxn0026
- **Download:** [X-Plane.org](https://forums.x-plane.org/files/file/91876-toliss-airbus-cabin-ready-automatic-flywithlua-script/)
- **Platforms:** Windows, macOS, Linux (pure Lua)
- **Compatibility:** X-Plane 12
- **Dependency:** [FlyWithLua NG+](../scripting/flywithlua.md)

The script automates two cabin-ready triggers:

- **Departure:** Cabin ready follows about 4–8 minutes after the start of the departure phase, scaled by passenger count
- **Approach:** Sends cabin ready a few seconds after both flaps and landing gear are in the down position

Edge cases like go-arounds and through-flights are handled — in worst case, the FWD CALL button may need to be pressed manually or an unnecessary chime may sound. The script never cancels an existing cabin ready state.

## Features

- **Automatic departure trigger:** Beacon-on starts a PAX-scaled countdown
- **Automatic approach trigger:** Flaps + gear down triggers cabin ready
- **Go-around safe:** Handles missed approaches without incorrect states
- **All ToLiss aircraft:** Works with the entire ToLiss Airbus family (A319, A320 CEO/NEO, A321 CEO/NEO, A330-900, A340-600)

## Value in Flight Simulation

The FWD CALL for cabin ready is a routine task that interrupts cockpit flow — especially during busy departure and approach phases. This script automates the procedure realistically (timing scaled to passenger count), letting the pilot focus on flying.

## Installation

**Download:** [X-Plane.org](https://forums.x-plane.org/files/file/91876-toliss-airbus-cabin-ready-automatic-flywithlua-script/)

Place the `.lua` file into `Resources/plugins/FlyWithLua/Scripts/`.

## Sources

- [Toliss Airbus Cabin Ready — X-Plane.org](https://forums.x-plane.org/files/file/91876-toliss-airbus-cabin-ready-automatic-flywithlua-script/)
