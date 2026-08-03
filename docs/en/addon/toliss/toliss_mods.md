---
description: "ToLiss aircraft mods for X-Plane 12: Easy Freighter A321 P2F cargo door conversion, Carda 3D engine replacements, the Durantula wing mod with new flaps and native wingflex, and the RealWings wing replacement."
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

Installation requires two steps: downloading the engine OBJ files from the Threshold Forums, then patching the `.acf` file to reference the new models. The **Carda Engine Mod Installer** by iy4vet automates the `.acf` patching step; an older, separate installer by Todaloo covers the same ground. The separate **Carda Engines Mod Fix** by Travis is recommended to fix animation bugs.

- **Engine mod developer:** Carda Jowol
- **Installer developer:** iy4vet
- **Engine downloads:** [Threshold Forums](https://forum.thresholdx.net/files/category/36-mods/) (free)
- **Installer download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/99205-carda-engine-mod-installer-for-toliss-a319-a320-a321/)

!!! note "Linux: native installer binary"

    The installer ships a native Linux binary (`install-carda-linux-x64`, also ARM64). Make it executable with `chmod +x` and run it from the aircraft folder. Alternatively, `install_carda.py` runs directly with Python 3.10+ and needs no external dependencies. The engine models themselves (OBJ/DDS) are platform-independent. The installer must be re-run after every ToLiss aircraft update.

## Durantula Wing Enhancement MOD

New flap and flap-track-fairing geometry plus a native wingflex for the A319, A320 and A321. The mod consists of two independent parts that can be installed separately or together:

- **Flaps** — replaces the stock flaps and flap-track fairings in the wing OBJs with new meshes and their own textures. On CEO airframes the obsolete engine "kit" geometry overlapping the new fairings is removed as well: from the Carda engine OBJs if those are installed, otherwise from the stock `engines.obj`
- **Wingflex** — replaces ToLiss's own winglet-flex animations in the wing, glass, decal, light and particle OBJs with X-Plane's native `wing_tip_deflection_deg` animation, and sets the wing damping properties in the `.acf`

An optional "New Wing Textures" paint kit is included; the finished livery goes into the aircraft's `liveries/` folder manually.

Installed by hand, the mod means editing OBJ files in a text editor and the `.acf` in Plane Maker. The **Durantula Wing Mod Installer** by iy4vet automates every one of those edits. It matches on geometry and animation content instead of line numbers, so it still works when other mods — the Carda engines or a lighting mod — have shifted the line numbering, and it is safe to re-run. Backups are written as `*.durantula.bak` before any file is touched, and the engine family is read from the `.acf` automatically.

- **Mod developer:** Durantula2405 (3D modelling and animation: Giorgi_Z4)
- **Installer developer:** iy4vet
- **Mod download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/88518-toliss-a319-a320-and-a321-wing-enhancement-mod/)
- **Installer:** [github.com/iy4vet](https://github.com/iy4vet/xplane-toliss-durantula-installer) (GPL-3.0, with pre-built binaries)

!!! note "Linux: native installer binary"

    A native Linux binary is available (`install-durantula-linux-x64`, also ARM64). Make it executable with `chmod +x` and run it from the aircraft folder, or run `install_durantula.py` directly with Python 3.10+ — no external dependencies. Both accept `--aircraft`, `--parts`, `--flaps-engine` and `--textures` for a fully non-interactive install. A ToLiss update via SkunkCraftsUpdater restores the stock files, so the installer has to be re-run afterwards.

## RealWings

Where the Durantula mod reworks parts of the stock wing, RealWings replaces it outright: fully re-modelled wing geometry with new 4K textures, a Substance 3D Painter paintkit for repainters, and new window frames as a bonus. The mod is purely visual — it ships no original ToLiss files and does not touch the aircraft's systems code. It is built to sit alongside the Carda CFM/IAE engines.

There is one download per narrowbody type, each covering the relevant wingtip variants (a RealWings340 for the ToLiss A340-600 exists as well, outside the scope of this page):

| Download | Aircraft | Variants |
|----------|----------|----------|
| RealWings319 | A319 | CEO |
| RealWings320 | A320 | NEO, CEO with sharklets, CEO with wingtips |
| RealWings321 | A321 | NEO, CEO with sharklets, CEO with wingtips |

The installer — again by iy4vet — swaps the stock wing OBJs for the RealWings versions at the correct positions, removes the geometry blocks that become obsolete, and corrects the engine coordinates if it finds the Carda mod installed. Only one wingtip variant is active at a time; re-running the installer switches between them. For the A320 and A321 the download contains nested `CEO/` and `NEO/` folders, which the installer merges on its own. One step stays manual: if a livery brings its own RealWings textures, its `objects/RealWings3XX/` folder has to be copied into the matching livery folder.

- **Mod developer:** GeoBuilds, together with Durantula2405
- **Installer developer:** iy4vet
- **Downloads:** [RealWings319](https://forums.x-plane.org/files/file/99042-realwings319-wing-replacement-mod-for-toliss-a319/) · [RealWings320](https://forums.x-plane.org/files/file/99352-realwings320-wing-replacement-mod-for-toliss-a320neo/) · [RealWings321](https://forums.x-plane.org/files/file/99442-realwings321-wing-replacement-mod-for-toliss-a321neoceo/)
- **Installer:** [github.com/iy4vet](https://github.com/iy4vet/xplane-toliss-realwings-installer) (GPL-3.0, with pre-built binaries)

!!! note "Linux: native installer binary"

    As with the other two installers, native Linux binaries are available (`install-realwings-linux-x64` and `-arm64`); `chmod +x`, then run from the aircraft folder. `install_realwings.py` works directly with Python 3.10+ without external dependencies. Non-interactive via `--aircraft`, `--variant`, `--frames` and `--aircraft-dir`.

!!! warning "RealWings and the Durantula mod overlap"

    Both mods target the same files. RealWings does not rewrite the stock wing OBJs but removes them from the `.acf` outright, which silently voids the Durantula mod's in-place edits; beyond that, both also edit `Decals.obj`, the lighting OBJ and the Carda engine OBJs. Neither installer knows about the other — they detect only the Carda mod — and RealWings deletes the obsolete Carda "kit" geometry by line number, which a previous Durantula run has already shifted. Treat the two as alternatives, not a stack.

## Sources

- [Toliss A319, A320 and A321 — Wing Enhancement MOD](https://forums.x-plane.org/files/file/88518-toliss-a319-a320-and-a321-wing-enhancement-mod/) — mod by Durantula2405
- [RealWings320](https://forums.x-plane.org/files/file/99352-realwings320-wing-replacement-mod-for-toliss-a320neo/) — wing replacement mod by GeoBuilds (A319 and A321 versions linked above)
- [xplane-toliss-realwings-installer](https://github.com/iy4vet/xplane-toliss-realwings-installer) — installer source, binaries and documentation
- [xplane-toliss-durantula-installer](https://github.com/iy4vet/xplane-toliss-durantula-installer) — installer source, binaries and documentation
- [Carda Engine Mod Installer](https://forums.x-plane.org/files/file/99205-carda-engine-mod-installer-for-toliss-a319-a320-a321/) — installer for the Carda engine mods
- [Easy Freighter Conversion Kit](https://forums.x-plane.org/files/file/92976-easy-freighter-conversion-kit-for-the-toliss-321/) — A321 P2F cargo door mod
