---
description: "Smoke & Steam for SimHeaven adds particle-based smoke and steam effects to industrial chimneys and cooling towers in SimHeaven X-World scenery."
---
# Smoke & Steam for SimHeaven

Smoke & Steam for SimHeaven is a scenery extension for [X-Plane](../../glossary.md#x-plane) that adds particle-based smoke and steam effects to industrial chimneys and cooling towers placed by [SimHeaven X-World](../../glossary.md#simheaven-x-world). The effects cover X-World objects worldwide and use the native X-Plane 12 particle system.

## Background

- **Type:** Scenery extension (particle library, no plugin dependency)
- **Author:** Günther Kremp (particle effects by Helfried Miersch)
- **Distribution:** [X-Plane.org Forums](https://forums.x-plane.org/files/file/94841-smoke-steam-for-chimneys-coolingtowers-for-simheaven-10-xp12/) (Freeware, non-commercial use only)
- **Platforms:** Windows, macOS, Linux (standard scenery folder, platform-independent)
- **Compatibility:** X-Plane 12 only
- **Dependency:** [SimHeaven X-World](../../glossary.md#simheaven-x-world) must be installed

The extension installs as a standalone particle library (`simHeaven_X-World_Particles_Library`) that references existing X-World chimney and cooling tower objects. X-World itself is developed by Armin "PilotBalu" (SimHeaven) and available as freeware from [simheaven.com](https://simheaven.com).

??? abstract "Technical Background: X-Plane 12 Particle System"

    X-Plane 12 supports particle emitters in scenery objects (DSF). Each OBJ file can reference a `.pss` particle system definition via the `PARTICLE_SYSTEM` directive and place `EMITTER` sources at specific positions. Emitters run continuously — ideal for persistent effects like chimney smoke — while *effects* are time-limited sequences (e.g., explosions). The particle appearance (texture, opacity, scale, lifetime) is defined per particle type in the `.pss` file.

## Features

- **Smoke** on industrial chimneys from SimHeaven X-World
- **Steam** on cooling towers from SimHeaven X-World
- Worldwide coverage — effects appear wherever X-World places matching objects
- Smaller chimneys and cooling towers are intentionally excluded to preserve frame rates on lower-end hardware

## Value in Flight Simulation

X-Plane's default scenery does not animate industrial structures — chimneys and cooling towers remain static objects without visual activity. This extension adds a visual layer that makes industrial areas identifiable from a distance during VFR flight: rising smoke columns and steam plumes serve as orientation points and increase the perceived realism of the ground environment. On Linux, the package installs as a standard scenery folder without plugin dependencies.

## Installation

**Download:** [X-Plane.org Forums](https://forums.x-plane.org/files/file/94841-smoke-steam-for-chimneys-coolingtowers-for-simheaven-10-xp12/) | [SimHeaven](https://simheaven.com)

1. Extract the ZIP into a directory **outside** of X-Plane
2. Copy the folder `simHeaven_X-World_Particles_Library` to `X-Plane 12/`[Custom Scenery](../../glossary.md#custom-scenery)`/`
3. Register the folder in [scenery_packs.ini](../../glossary.md#scenery_packsini) **above** X-World

**Load order in scenery_packs.ini**

```
SCENERY_PACK Custom Scenery/simHeaven_X-World_Particles_Library/
SCENERY_PACK Custom Scenery/simHeaven_X-World_Europe_.../
SCENERY_PACK Custom Scenery/simHeaven_X-World_Vegetation_Library/
```

---

## Further Reading

| Topic | Page | Focus |
|---|---|---|
| Scenery Components | [How X-Plane Builds the World](../aufbau_quellen/scenery_components.md) | scenery_packs.ini load order and layer interaction |
| Scenery Sources | [Sources](../aufbau_quellen/scenery_sources.md) | Overview of scenery providers and databases |

---

## Sources

- [Smoke & Steam for Chimneys & Coolingtowers — X-Plane.org Forums](https://forums.x-plane.org/files/file/94841-smoke-steam-for-chimneys-coolingtowers-for-simheaven-10-xp12/)
- [SimHeaven — X-World Downloads](https://simheaven.com/xp12-sceneries/)
- [X-Plane 12 Particle System — Laminar Research Developer Docs](https://developer.x-plane.com/article/x-plane-11-particle-system/)
