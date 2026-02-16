# ToLiss Mods

Aircraft modifications for the ToLiss fleet (A319, A320 CEO/NEO, A321 CEO/NEO) — 3D model replacements and conversions that go beyond scripting.

## Easy Freighter — A321 P2F Cargo Door Mod

Simulates a cargo main door for the A321P2F/A321PCF with rigid cargo barrier and window plugs as a FlyWithLua object. Includes freight airline liveries. A separate version also exists for the A320. Not officially approved by ToLiss.

- **Developer:** XPJavelin
- **Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/92976-easy-freighter-conversion-kit-for-the-toliss-321/)

## Carda Realistic Engine Mods

High-detail 3D engine replacements by Carda Jowol with 4K textures, animated thrust reversers, engine flex animations, and custom particle effects. Available for A319, A320 CEO/NEO, and A321 CEO/NEO. The engine models are free and platform-independent (OBJ files placed in the aircraft's `objects/` folder).

Available engines: CFM56-5A, CFM56-5B, IAE V2500 (CEO variants), CFM LEAP-1A, PW1100G (NEO variants).

Installation requires two steps: downloading the engine OBJ files from the Threshold Forums, then patching the `.acf` file to reference the new models. The **Carda Engine Installer** by Todaloo automates the `.acf` patching step. The separate **Carda Engines Mod Fix** by Travis is recommended to fix animation bugs.

- **Engine mod developer:** Carda Jowol
- **Installer developer:** Todaloo
- **Engine downloads:** [Threshold Forums](https://forum.thresholdx.net/files/category/36-mods/) (free)
- **Installer download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/94704-carda-engine-installer-for-toliss-a320-family/)
- **Mod Fix download:** [Threshold Forums](https://forum.thresholdx.net/files/file/3685-carda-engines-mod-fix-for-toliss-airbus/)

!!! warning "Linux: Installer is Windows-only"

    The Carda Engine Installer is a Windows `.exe`. On Linux, it can be run inside a [KVM](../kvm.md) Windows VM. The engine models themselves (OBJ/DDS) are platform-independent and work on Linux without modification. The installer must be re-run after every ToLiss aircraft update.
