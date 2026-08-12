---
description: "Bay's Lighting Mod is a lighting overhaul for X-Plane 12 — reworked airport, beacon, night and cockpit lighting, cloud scattering and visibility."
---
# Bay's Lighting Mod

Bay's Lighting Mod replaces [X-Plane](../../glossary.md#x-plane) 12's lighting system with a reworked set of textures, sprites and parameters. It touches airport and beacon lights, night lighting, atmospheric scattering, cockpit illumination and visibility — with the stated goal of a better-looking sim that stays plausible rather than stylized.

## Background

- **Developer:** baylor703
- **Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/97497-bays-lighting-mod/)
- **Platforms:** No platform restriction stated — the package contains textures and a Lua script, no binary
- **Compatibility:** X-Plane 12
- **Dependency:** [FlyWithLua NG+](../scripting/flywithlua.md)
- **License:** Free download, donations via Patreon

The package is not compatible with other lighting mods — only one of them can be active at a time.

## Features

- **Airport and beacon lighting:** Reworked approach, taxiway and beacon lights, plus modified aircraft nav and beacon lights
- **Night lighting:** New sprites for the 3D lights and revised effects around them
- **Distant lighting:** The transition from the near "3D" lights to the distant baked-in light textures is matched to be nearly seamless — provided ortho scenery is switched off
- **Clouds and scattering:** Altered atmospheric scattering and cloud illumination
- **Cockpit lighting:** Enhanced interior illumination
- **Dawn and dusk:** Reworked color and light behavior in the twilight hours
- **Visibility:** Widened range between clear and obscured conditions — the same quantity [AutoHaze](../flylua_scripts/autohaze.md) recomputes from live data, so running both warrants an eye on the result

## Night Flying and Orthophotos

X-Plane draws night lighting in two layers: close to the aircraft as individual 3D lights, farther out as baked light textures lying on the ground. [Orthophoto](../../scenery/orthophotography/index.md) scenery replaces those ground textures. A terrain definition can declare a night overlay of its own via `LIT_TEX`, but ortho tiles generally ship without one — so the distant layer disappears, the 3D lights end abruptly a short distance from the aircraft and everything beyond is black. This happens with or without the mod installed; it follows from how X-Plane layers night lighting.

!!! tip "Disable ortho for night flights"

    The developer's recommendation is to switch ortho scenery off for night flying in general — ortho ground textures are barely visible in the dark anyway, while the distant light layer extends to the horizon. For [ortho streaming](../../scenery/ortho_streaming/index.md) setups that means disabling the streaming layer before departure rather than tuning the mod.

## Value in Flight Simulation

Default X-Plane 12 night lighting has a visible break where the 3D lights hand over to the ground textures, and the mod's main work goes into closing it. The treatment extends to dawn, dusk and cloud scattering, so the visual character changes across a whole flight instead of only after dark. How far the widened visibility range carries is a claim of the developer's and depends heavily on the rest of the scenery setup.

## Installation

**Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/97497-bays-lighting-mod/)

Two steps, both described in detail in the included readme:

1. Copy the `Resources` folder from the archive into the X-Plane 12 root directory and confirm the overwrite prompt — if no prompt appears, the folder landed in the wrong place.
2. Copy `bays_lighting.lua` into `Resources/plugins/FlyWithLua/Scripts/`.

The download also ships the default lighting files plus instructions for restoring them, so the change can be reverted without reinstalling the simulator.

!!! warning "Overwriting inside Resources"

    The mod writes over default files in `Resources`. Keep a copy of the original directory before installing. An X-Plane update replaces those files with the defaults again and thereby removes the mod — reinstalling it is part of the update routine.

## Sources

- [Bay's Lighting Mod — forums.x-plane.org](https://forums.x-plane.org/files/file/97497-bays-lighting-mod/)
