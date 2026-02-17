# Dynamic Rain Rate

Dynamic Rain Rate is a [FlyWithLua](../scripting/flywithlua.md) script that dynamically adjusts X-Plane 12's rain intensity based on the aircraft's true airspeed. Instead of a static rain rate, the script continuously scales the effect to produce more realistic precipitation at different flight speeds.

## Background

- **Developer:** GusRodrigues
- **Download:** [X-Plane.org](https://forums.x-plane.org/files/file/97500-dynamic-rain-rate/)
- **Platforms:** Windows, macOS, Linux (pure Lua)
- **Compatibility:** X-Plane 12
- **Dependency:** [FlyWithLua NG+](../scripting/flywithlua.md)

## Features

- **Speed-proportional rain:** Rain intensity scales continuously with true airspeed (updated every 0.5 seconds)
- **No manual interaction:** Fully automatic — runs in the background without user input
- **Lightweight:** Minimal performance impact due to low update frequency

## Value in Flight Simulation

X-Plane 12 uses a fixed rain rate regardless of aircraft speed, which looks unrealistic — slow taxi appears the same as fast cruise. Dynamic Rain Rate addresses this by making rain intensity respond to speed, creating a more immersive weather experience especially during speed transitions (approach, acceleration, descent).

## Installation

**Download:** [X-Plane.org](https://forums.x-plane.org/files/file/97500-dynamic-rain-rate/)

Place the `.lua` file into `Resources/plugins/FlyWithLua/Scripts/`.

## Sources

- [Dynamic Rain Rate — X-Plane.org](https://forums.x-plane.org/files/file/97500-dynamic-rain-rate/)
