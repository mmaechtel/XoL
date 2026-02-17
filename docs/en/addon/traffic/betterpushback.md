# Better Pushback

Better Pushback is a [plugin](../../glossary.md#plugin) for [X-Plane](../../glossary.md#x-plane) 11/12 that simulates realistic pushback operations with a route planner, 3D tug vehicle, and multilingual voice output.

## Background

- **Original:** [skiselkov/BetterPushbackC](https://github.com/skiselkov/BetterPushbackC) (archived since December 2025)
- **Recommended fork:** [olivierbutler/BetterPusbackMod](https://github.com/olivierbutler/BetterPusbackMod) (actively maintained)
- **License:** CDDL 1.0 (open source)
- **Platforms:** Windows, macOS, Linux (native binaries)
- **Compatibility:** X-Plane 11 and X-Plane 12

The original repository is no longer maintained. The olivierbutler fork (BetterPusbackMod) is the recommended download for X-Plane 12, with feature additions like manual push mode and Magic Squares shortcuts.

## Features

- **Overhead planning view:** Bird's-eye view of the apron, draw pushback route via mouse clicks (curves, straights, direction changes)
- **Fully automatic pushback:** After route planning, the pushback runs autonomously — the pilot can focus on the startup procedure
- **Manual mode:** Pushback without pre-planning, controlled via joystick buttons or keys (Mod fork only)
- **Forward towing:** Aircraft can also be towed forward
- **3D tug vehicle:** Animated tug model with correct physics simulation
- **Multilingual ground crew:** Voice output in various languages simulates local ground personnel
- **Magic Squares:** Quick-access buttons for frequent operations (Mod fork only)

## Value in Flight Simulation

Better Pushback replaces X-Plane's rudimentary default pushback function with a realistic alternative. Route planning via the overhead view enables precise pushback paths around obstacles. In automatic mode, the startup procedure can be completed in parallel with the pushback. Manual mode is suitable for quick repositioning without pre-planning.

## Installation

**Download:** [GitHub Releases (olivierbutler fork)](https://github.com/olivierbutler/BetterPusbackMod/releases) or [forums.x-plane.org](https://forums.x-plane.org/files/file/90556-better-pushback-for-x-plane-1112/)

Extract the ZIP file to `Resources/plugins/`. This creates the `BetterPushback/` folder with the Linux binary at `lin_x64/BetterPushback.xpl`.

All dependencies are statically linked — no additional system packages are required.

**Notes:**

- When updating, always replace the entire `BetterPushback/` folder (not just the binary)
- The plugin directory must not be a symlink — the plugin silently fails to load with symlinks

### ALSOFT Real-Time Priority Warning

The following message may appear in `Log.txt`:

```
[ALSOFT] (EE) Failed to set real-time priority for thread: Operation not permitted (1)
```

This warning is non-fatal and does not affect audio playback. The embedded openal-soft library attempts to set real-time scheduling for audio threads, which lacks permission by default. If the plugin is unresponsive despite this warning, check for other causes (e.g., conflicts with aircraft plugins).

## Sources

- [BetterPusbackMod — GitHub (olivierbutler fork)](https://github.com/olivierbutler/BetterPusbackMod)
- [BetterPushbackC — GitHub (original, archived)](https://github.com/skiselkov/BetterPushbackC)
- [Better Pushback — forums.x-plane.org](https://forums.x-plane.org/files/file/90556-better-pushback-for-x-plane-1112/)
