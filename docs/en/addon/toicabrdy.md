# TOI Cabin Ready

TOI Cabin Ready is a [FlyWithLua](flywithlua.md) script that automatically sends the "Cabin Ready" ECAM notification for ToLiss Airbus aircraft, eliminating the need to manually press the FWD CALL button.

## Background

- **Developer:** cxn0026
- **Download:** [X-Plane.org](https://forums.x-plane.org/files/file/91876-toliss-airbus-cabin-ready-automatic-flywithlua-script/)
- **Platforms:** Windows, macOS, Linux (pure Lua)
- **Compatibility:** X-Plane 12
- **Price:** Free
- **Dependency:** [FlyWithLua NG+](flywithlua.md)

The script automates two cabin-ready triggers:

- **Departure:** Initiates a countdown (4–8 minutes, scaled by passenger count) when the beacon light is turned on
- **Approach:** Sends cabin ready a few seconds after both flaps and landing gear are in the down position

Edge cases like go-arounds and through-flights are handled — in worst case, the FWD CALL button may need to be pressed manually or an unnecessary chime may sound. The script never cancels an existing cabin ready state.

## Features

- **Automatic departure trigger:** Beacon-on starts a PAX-scaled countdown
- **Automatic approach trigger:** Flaps + gear down triggers cabin ready
- **Go-around safe:** Handles missed approaches without incorrect states
- **All ToLiss aircraft:** Works with the entire ToLiss Airbus family (A319, A320neo, A321/neo, A330neo, A340)

## Value in Flight Simulation

The FWD CALL for cabin ready is a routine task that interrupts cockpit flow — especially during busy departure and approach phases. This script automates the procedure realistically (timing scaled to passenger count), letting the pilot focus on flying.

## Installation

**Download:** [X-Plane.org](https://forums.x-plane.org/files/file/91876-toliss-airbus-cabin-ready-automatic-flywithlua-script/)

Place the `.lua` file into `Resources/plugins/FlyWithLua/Scripts/`.

### Linux Notes

No Linux-specific issues are known. The script is a plain Lua text file and runs identically on all platforms supported by FlyWithLua.

## Sources

- [Toliss Airbus Cabin Ready — X-Plane.org](https://forums.x-plane.org/files/file/91876-toliss-airbus-cabin-ready-automatic-flywithlua-script/)
