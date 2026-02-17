---
description: "LST (Living Scenery Technology) brings animated ground traffic to X-Plane 12 airports: vehicles, pedestrians, and ground equipment on defined routes."
---
# LST (Living Scenery Technology)

LST is a native [plugin](../../glossary.md#plugin) that brings airport scenery to life with animated ground traffic. Vehicles, pedestrians, ground service equipment, and trains move along defined routes — with realistic traffic jams, acceleration, and deceleration.

## Background

- **Developer:** X-Codr Designs
- **Website:** [x-codrdesigns.com](https://www.x-codrdesigns.com/living-scenery-technology)
- **Download:** [X-Plane.org](https://forums.x-plane.org/files/file/82876-living-scenery-technology/)
- **Platforms:** Windows, macOS, Linux (native binaries)
- **Compatibility:** X-Plane 12

LST is the modern successor to the older GroundTraffic plugin. Where GroundTraffic required a separate plugin instance per scenery (limited to ~30–40), LST operates as a global plugin that serves any number of sceneries simultaneously. The plugin is actively maintained.

## Features

- **Route-based animation:** Objects move along developer-defined paths with realistic acceleration and deceleration
- **Branching:** Objects randomly transition between routes for natural traffic flow — no sudden pop-in at unnatural locations
- **Minimum spacing:** Vehicles automatically maintain distance and decelerate gradually (traffic jam simulation)
- **Particle system:** Access to X-Plane 12's particle effects (exhaust, smoke) on scenery objects
- **FMOD sound:** Directional, distance-attenuated sounds on moving and static objects
- **Location triggers:** Trigger events at specific positions (e.g., door opening on vehicle arrival)
- **Performance:** Thousands of animated objects with less than 5–10% frame rate impact

## Value in Flight Simulation

Without LST, airport sceneries feel static — ramp vehicles sit motionless, roads remain empty. LST brings movement to the scenery: buses shuttle between terminals, baggage carts drive to the aircraft, cars flow on access roads. An increasing number of scenery developers integrate LST into their products, making the benefit grow with each new scenery.

## Installation

**Download:** [X-Plane.org](https://forums.x-plane.org/files/file/82876-living-scenery-technology/)

Copy the `Living Scenery Technology` folder to `Resources/plugins/`. The plugin activates automatically when an LST-enabled scenery is loaded.

### Linux Notes

The Linux binary is included in the download. No Linux-specific issues are known.

The official developer tools (converter, generator) are Windows-only. For Linux, the community alternative [lst-utils](https://github.com/devleaks/lst-utils) (Python, MIT license) is available.

## Sources

- [LST — X-Plane.org](https://forums.x-plane.org/files/file/82876-living-scenery-technology/)
- [LST — X-Codr Designs](https://www.x-codrdesigns.com/living-scenery-technology)
