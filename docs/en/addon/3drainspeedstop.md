# 3D Rain Stop

3D Rain Stop is a [FlyWithLua](flywithlua.md) script package that automatically disables the 3D rain particle effect at higher speeds or altitudes. X-Plane 12's falling rain particles create a distracting "Star Wars warp speed" visual at high speeds — the scripts remove this effect while preserving the windshield rain rendering.

## Background

- **Developer:** domvc10
- **Download:** [X-Plane.org](https://forums.x-plane.org/files/file/88602-3d-rain-stop-lua-script-xp12/)
- **Platforms:** Windows, macOS, Linux (pure Lua)
- **Compatibility:** X-Plane 12
- **Price:** Free
- **Dependency:** [FlyWithLua NG+](flywithlua.md)

The download contains two scripts — only one should be active at a time:

- **3drainspeedstop.lua** — Disables 3D rain above 100 knots, re-enables below 99 knots
- **3drainheightstop.lua** — Disables 3D rain above 7,000 ft AGL, re-enables below that altitude

Both thresholds can be adjusted by editing the values in the `.lua` file.

## Features

- **Speed-based rain control:** Automatic on/off based on indicated airspeed
- **Altitude-based rain control:** Alternative variant using AGL altitude as trigger
- **Windshield unaffected:** Only disables the falling 3D rain particles — the rain effect on the aircraft windshield remains active
- **Editable thresholds:** Speed and altitude values are configurable in the script source

## Value in Flight Simulation

At cruise speed, X-Plane 12's 3D rain particles streak across the screen unrealistically. The effect is purely cosmetic at altitude and distracts from the instruments. 3D Rain Stop removes this visual artifact during fast flight while keeping the atmospheric rain effect intact during slower phases like approach and taxi.

## Installation

**Download:** [X-Plane.org](https://forums.x-plane.org/files/file/88602-3d-rain-stop-lua-script-xp12/)

Place **one** of the two `.lua` files into `Resources/plugins/FlyWithLua/Scripts/`. Do not use both scripts simultaneously.

### Linux Notes

No Linux-specific issues are known. The script is a plain Lua text file and runs identically on all platforms supported by FlyWithLua.

## Sources

- [3D Rain Stop — X-Plane.org](https://forums.x-plane.org/files/file/88602-3d-rain-stop-lua-script-xp12/)
