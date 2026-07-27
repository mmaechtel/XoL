---
description: "ToLiss aircraft mods for X-Plane 12: Easy Freighter A321 P2F cargo door conversion and Carda high-detail 3D engine replacements with 4K textures."
---
# ToLiss Mods

Aircraft modifications for the ToLiss fleet (A319, A320 CEO/NEO, A321 CEO/NEO) — 3D model replacements and conversions that go beyond scripting.

## Easy Freighter — A321 P2F Cargo Door Mod

Simulates an A321 freighter conversion (A321P2F/A321PCF). The kit is a drag-and-drop object for the aircraft's `objects/` folder; the cargo livery must contain `external_Extras = YES` and `custom_Cabin = F` in its `livery.tlscfg`. A demonstration livery is included. A separate version also exists for the A320. Not officially approved by ToLiss.

- **Developer:** XPJavelin
- **Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/92976-easy-freighter-conversion-kit-for-the-toliss-321/)

## Carda Realistic Engine Mods

High-detail 3D engine replacements by Carda Jowol with 4K textures, animated thrust reversers, engine flex animations, and custom particle effects. Available for A319, A320 CEO/NEO, and A321 CEO/NEO. The engine models are free and platform-independent (OBJ files placed in the aircraft's `objects/` folder).

Available engines: CFM56-5A, CFM56-5B, IAE V2500 (CEO variants), CFM LEAP-1A, PW1100G (NEO variants).

Installation requires two steps: downloading the engine OBJ files from the Threshold Forums, then patching the `.acf` file to reference the new models. The **Carda Engine Installer** by Todaloo automates the `.acf` patching step. The separate **Carda Engines Mod Fix** by Travis is recommended to fix animation bugs.

- **Engine mod developer:** Carda Jowol
- **Installer developer:** iy4vet
- **Engine downloads:** [Threshold Forums](https://forum.thresholdx.net/files/category/36-mods/) (free)
- **Installer download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/99205-carda-engine-mod-installer-for-toliss-a319-a320-a321/)

!!! note "Linux: native installer binary"

    The installer ships a native Linux binary (`install-carda-linux-x64`, also ARM64). Make it executable with `chmod +x` and run it from the aircraft folder. Alternatively, `install_carda.py` runs directly with Python 3.10+ and needs no external dependencies. The engine models themselves (OBJ/DDS) are platform-independent. The installer must be re-run after every ToLiss aircraft update.
