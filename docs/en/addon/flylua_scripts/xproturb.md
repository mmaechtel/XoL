---
description: "X-ProTurb — FlyWithLua turbulence engine for X-Plane 12 with physics-based atmospheric models (MIL-F-8785C, ICAO 9625) and an aircraft-specific gust response."
---
# X-ProTurb — Professional Turbulence Engine

X-ProTurb is a [FlyWithLua](../scripting/flywithlua.md) script that replaces the simplistic turbulence model of [X-Plane](../../glossary.md#x-plane) 12 with a physics-based engine. Instead of a random "shake" driven by a 0–10 intensity slider, it computes turbulence from the same certification standards used to qualify full-motion Level-D airline simulators — and lets each airframe react to it individually.

## Background

- **Developer:** sfkcyl (Safak Cayli, a Level-D simulator developer)
- **Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/100195-x-proturb-professional-turbulence-engine/)
- **Platforms:** Windows, macOS (Intel and Apple Silicon), Linux — native libraries, falling back automatically to an equivalent Lua implementation
- **Compatibility:** X-Plane 12
- **Dependency:** [FlyWithLua NG+](../scripting/flywithlua.md) 2.8.13 or newer; on Linux and macOS, Python 3 for the optional LiveCAT helper
- **License:** Free for personal use

## The Core Idea — Two Separate Systems

The engine cleanly separates "what is happening in the air?" from "how does my aircraft react to it?":

- The **atmosphere** carries its own physically modelled turbulence field.
- The **aircraft** responds according to its type — mass, wing, speed and structure are read automatically.

A light Cessna gets thrown around in the same gust that a wide-body barely notices — with no hand-tuned settings per aircraft and no arbitrary intensity multiplier to guess at.

## Standards

Turbulence is derived from recognised aviation norms rather than tuned curves:

- **MIL-F-8785C** — US military standard for flying qualities; the engine scales each aircraft's felt response to its certified target
- **FAR 25.341 (Pratt)** — FAA gust-load requirement transport aircraft are designed against
- **ICAO 9625 Level-D** — the highest fidelity tier for full-flight simulators used in airline pilot training

## Features

- **Gusts on the airframe:** Vertical and side gusts act on X-Plane's own wing, tail and fin elements, so the aircraft's airfoil data, flaps, Mach number and wing loading shape the response; the gust travels from nose to tail with the correct delays
- **Calibration:** A one-time measurement per aircraft captures how fuselage, nacelles and other bodies respond to gusts (see [Calibration](#calibration)). Calibration is optional; without it, these bodies do not respond to gusts
- **Load factor Δn:** Per-type variation of the g-loads via the FAR 25.341 Pratt formula, read automatically from each aircraft's geometry
- **von Kármán / Dryden spectra:** Two established gust models that distribute turbulence energy across realistic wavelengths instead of flat random noise
- **CAT:** Clear Air Turbulence using a Richardson-number model, a tropopause-locked CAT profile and Kelvin–Helmholtz billows — the insidious turbulence that strikes without visual warning
- **Mountain-Wave suite:** Queney lee waves, rotor zones, wave breaking, hydraulic jump (Boulder/Bora downslope windstorms) and the Scorer parameter for trapped vs. propagating waves
- **CB / storm modelling:** Cumulonimbus cores, hail and heavy-rain turbulence scaled to the official FAA severity bands (light → extreme), with a turbulence-ahead warning
- **Weather integration:** The engine reads X-Plane's own 3D weather grid, measures in flight how much turbulence X-Plane's weather actually puts on the aircraft, and adds only the energy above it — nothing is counted twice
- **Surface roughness:** Low-level turbulence follows the terrain upwind, taken from the ESA WorldCover 10 m map (forest, city, cropland, water); runways and aprons count as open ground
- **LiveCAT:** Optional helper for real-world data (GFS boundary layer, surface heat flux, CAT/SIGMET/PIREP advisories); without internet, the engine runs in full
- **Two scales:** ATMOSPHERE grades the turbulence in the air on the ICAO EDR scale, AIRCRAFT shows what is felt at the pilot's seat — a widebody rides atmospheric "moderate" as light chop
- **Fly-by-wire friendly:** The engine never touches controls, autopilot, fly-by-wire laws or yaw damper
- **Panel:** Five tabs (Status, Weather, Phenomena, Aircraft, Settings) with a bar per turbulence source, EDR readouts, a PIREP in AIM format and a nowcast about 25 nm ahead

## Value in Flight Simulation

Default X-Plane turbulence is essentially a single random jitter with an intensity dial. X-ProTurb turns that into a true physics engine: the atmosphere is modelled on certification-grade standards, and every aircraft in your fleet reacts to it according to its own characteristics — without hand-tuning per aircraft. Typical cost is under 1 ms per frame.

## Installation

**Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/100195-x-proturb-professional-turbulence-engine/)

Copy the complete package into `Resources/plugins/FlyWithLua/Scripts/`:

- the `X-ProTurb_*.lua` script
- the `XPT_Runtime` folder (complete)
- `xproturb_livecat.py` (Linux and macOS; Windows uses `xproturb_livecat.exe`)
- the six `albedo_*.csv` files

When upgrading, delete the old `X-ProTurb_*.lua` first; the included changelog says whether the settings file `X-ProTurb.txt` can be kept. Step-by-step instructions per platform are in `KURULUM_INSTALL.txt`. The panel opens via `Plugins > FlyWithLua > FlyWithLua Macros > X-ProTurb`.

### Calibration

Calibration is started once per aircraft with a button on the panel's top bar and takes about 1.5 minutes. Before starting, set the weather manually to Clear and have the engines running. The aircraft is lifted about 300 m above the ground, runs through its tests for every flap position, and is then put back where it started. A sim restart is not needed — set up the flight again and continue.

## Sources

- [X-ProTurb — forums.x-plane.org](https://forums.x-plane.org/files/file/100195-x-proturb-professional-turbulence-engine/)
