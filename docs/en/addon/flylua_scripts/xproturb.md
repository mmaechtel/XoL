---
description: "X-ProTurb — FlyWithLua turbulence engine for X-Plane 12 with physics-based atmospheric models (MIL-F-8785C, ICAO 9625) and 6-DOF response."
---
# X-ProTurb — Professional Turbulence Engine

X-ProTurb is a [FlyWithLua](../scripting/flywithlua.md) script that replaces the simplistic turbulence model of [X-Plane](../../glossary.md#x-plane) 12 with a physics-based engine. Instead of a random "shake" driven by a 0–10 intensity slider, it computes turbulence from the same certification standards used to qualify full-motion Level-D airline simulators — and lets each airframe react to it individually.

## Background

- **Developer:** sfkcyl (Safak Cayli, a Level-D simulator developer)
- **Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/100195-x-proturb-professional-turbulence-engine/)
- **Platforms:** Windows, macOS, Linux (via FlyWithLua)
- **Compatibility:** X-Plane 12
- **Dependency:** [FlyWithLua NG+](../scripting/flywithlua.md)
- **License:** Free for personal use

## The Core Idea — Two Separate Systems

The engine cleanly separates "what is happening in the air?" from "how does my aircraft react to it?":

- The **atmosphere** carries its own physically modelled turbulence field.
- The **aircraft** responds according to its type — mass, wing, speed and structure are read automatically.

A light Cessna gets thrown around in the same gust that a wide-body barely notices — with no per-aircraft setup and no arbitrary intensity multiplier to guess at.

## Standards

Turbulence is derived from recognised aviation norms rather than tuned curves:

- **MIL-F-8785C** — US military standard for flying qualities; the engine calibrates each aircraft's felt response to its certified target
- **FAR 25.341 (Pratt)** — FAA gust-load requirement transport aircraft are designed against
- **ICAO 9625 Level-D** — the highest fidelity tier for full-flight simulators used in airline pilot training

## Features

- **6-DOF response:** The aircraft moves in all six degrees of freedom — including true vertical *heave* (the sink-and-lift you feel in the seat) plus sway and surge
- **Load factor Δn:** Per-type variation of the g-loads via the FAR 25.341 Pratt formula, read automatically from each aircraft's geometry
- **von Kármán / Dryden spectra:** Two established gust models that distribute turbulence energy across realistic wavelengths instead of flat random noise
- **CAT:** Clear Air Turbulence using a Richardson-number model, a tropopause-locked CAT profile and Kelvin–Helmholtz billows — the insidious turbulence that strikes without visual warning
- **Mountain-Wave suite:** Queney lee waves, rotor zones, wave breaking, hydraulic jump (Boulder/Bora downslope windstorms) and the Scorer parameter for trapped vs. propagating waves
- **CB / storm modelling:** Cumulonimbus cores, hail and heavy-rain turbulence scaled to the official FAA severity bands (light → extreme), with a turbulence-ahead warning
- **Weather integration:** The engine reads X-Plane's own 3D weather grid and compensates for double-counting, or takes over turbulence entirely in its own mode
- **Fly-by-wire detection:** On Airbus-style aircraft the engine recognises the electronic flight-control system and lets its control laws set the ride, the way the real aircraft would

## Value in Flight Simulation

Default X-Plane turbulence is essentially a single random jitter with an intensity dial. X-ProTurb turns that into a true physics engine: the atmosphere is modelled on certification-grade standards, and every aircraft in your fleet reacts to it according to its own characteristics — no per-aircraft tuning required. A professional UI with five colour-coded tabs shows in real time what the engine is computing, including a live aircraft-recognition chip (type plus fly-by-wire or conventional) and honest readouts of every source driving the ride.

## Installation

**Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/100195-x-proturb-professional-turbulence-engine/)

Place the script files into `Resources/plugins/FlyWithLua/Scripts/`. The engine runs automatically across your whole fleet — from a glider to a heavy twin, default, freeware or study-level — with zero per-aircraft configuration.

## Sources

- [X-ProTurb — forums.x-plane.org](https://forums.x-plane.org/files/file/100195-x-proturb-professional-turbulence-engine/)
