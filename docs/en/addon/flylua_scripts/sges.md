# SGES — Simple Ground Equipment & Services

SGES is a [FlyWithLua](../scripting/flywithlua.md) script that adds comprehensive ground handling equipment to [X-Plane](../../glossary.md#x-plane) 12. It places and animates static and moving objects around the aircraft on the apron — from GPU and fuel truck to animated passengers and a simplified marshaller.

## Background

- **Developer:** XPJavelin
- **Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/62296-simple-ground-equipment-services-low-tech-services/)
- **Platforms:** Windows, macOS, Linux (pure Lua)
- **Compatibility:** X-Plane 12
- **Dependency:** [FlyWithLua NG+](../scripting/flywithlua.md)
- **Updates:** Via [SkunkCrafts Updater](../tools/skunkcrafts_updater.md)

## Features

- **Ramp vehicles:** GPU, ASU, fuel truck, belt loader, ULD loaders, catering vehicle, bus, baggage carts, follow-me car
- **Static equipment:** Cones, functional chocks (prevent rolling on sloped aprons), airstairs with maintenance stair variant
- **Animated elements:** Animated passengers, moving vehicles (follow-me car, EMS, fuel truck, baggage carts, passenger bus), simplified marshaller
- **Pushback:** Simple pushback with pushback truck, compatible with aircraft carriers
- **Deicing:** Active deicing that protects the airframe from X-Plane ice for a configurable time period (activates only in low temperatures)
- **Adaptive ground kit:** Automatically adjusts equipment for freighter, passenger, regional, business jet, or GA aircraft
- **Military variant:** Green-painted vehicles for military ramp scenarios
- **Arresting systems:** Cable, net barrier, EMAS (Engineered Material Arresting System)
- **Emergency scenarios:** Accidents, fires, shipwrecks, industrial/wildfire effects (extinguishable by X-Plane water bombers)

All equipment is toggleable via a non-intrusive popup menu. Compatible with X-Plane 12.2+ native chocks.

## Value in Flight Simulation

SGES fills the gap between static default ramps and paid ground service solutions. The adaptive ground kit automatically matches equipment to the aircraft type — no manual configuration needed. The functional chocks and animated ground traffic add immersion without requiring other ground service plugins. SGES complements [Better Pushback](../traffic/betterpushback.md) (for realistic pushback) and [openSAM](../traffic/opensam.md) (for jetways and VDGS).

## Installation

**Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/62296-simple-ground-equipment-services-low-tech-services/)

Place the SGES files into `Resources/plugins/FlyWithLua/Scripts/`. The included `skunkcrafts_updater.cfg` goes into `Resources/plugins/FlyWithLua/` (root, not Scripts).

After first launch, assign a keyboard key to toggle the SGES menu via `Settings > Keyboard`. Generate the airport cache via `Plugins > FlyWithLua > Macros > SGES refresh`.

SGES ships with five PDF manuals covering general use, animated passengers, arresting systems, and marshaller functions.

## Sources

- [SGES — forums.x-plane.org](https://forums.x-plane.org/files/file/62296-simple-ground-equipment-services-low-tech-services/)
- [SGES — x-plane.to](https://x-plane.to/file/176/simple-ground-equipment-services-low-tech-ground-services)
