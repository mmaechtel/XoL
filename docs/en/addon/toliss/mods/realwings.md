---
description: "RealWings replaces the wing of the ToLiss A319, A320 and A321 outright — new geometry, 4K textures and window frames, with a Linux installer."
---
# RealWings

Where the [Durantula mod](durantula_wing_mod.md) reworks parts of the stock wing, RealWings replaces it outright: fully re-modelled wing geometry including the flaps, with new 4K textures, a Substance 3D Painter paint kit for repainters, and new cabin window frames as an optional extra. The mod is purely visual — it ships no original ToLiss files and does not touch the aircraft's systems code. It is built to sit alongside the Carda CFM/IAE engines.

## Background

- **Mod developer:** GeoBuilds, together with Durantula2405
- **Installer developer:** iy4vet (based on earlier auto-installers by alexvor20)
- **Downloads:** [RealWings319](https://forums.x-plane.org/files/file/99042-realwings319-wing-replacement-mod-for-toliss-a319/) · [RealWings320](https://forums.x-plane.org/files/file/99352-realwings320-wing-replacement-mod-for-toliss-a320neo/) · [RealWings321](https://forums.x-plane.org/files/file/99442-realwings321-wing-replacement-mod-for-toliss-a321neoceo/)
- **Installer:** [github.com/iy4vet](https://github.com/iy4vet/xplane-toliss-realwings-installer)
- **Platforms:** The mod itself is OBJ and texture data and platform-independent; the installer ships native binaries for Linux, macOS and Windows
- **Compatibility:** X-Plane 12, ToLiss A319, A320 and A321
- **License:** Mods as free forum downloads, installer under GPL-3.0

## Coverage

There is one download per narrowbody type, each covering the relevant wingtip variants. Only one variant is active at a time; re-running the installer switches between them. A RealWings340 for the ToLiss A340-600 exists as well, outside the scope of this page.

| Download | Aircraft | Variants |
|----------|----------|----------|
| RealWings319 | A319 | CEO |
| RealWings320 | A320 | NEO, CEO with sharklets, CEO with wingtips |
| RealWings321 | A321 | NEO, CEO with sharklets, CEO with wingtips |

## Value in Flight Simulation

The wing is the largest single surface in every external view and in most cabin views, and the stock ToLiss geometry shows its age against the rest of the model. Because the replacement is complete rather than partial, the result is consistent across all wingtip variants instead of mixing new and old detail on one surface. The cost is the tighter coupling to everything else that touches the wing OBJs — engine mods, lighting mods, and any other wing mod.

## Installation

**Downloads:** see above · **Installer:** [GitHub Releases](https://github.com/iy4vet/xplane-toliss-realwings-installer/releases)

1. Unzip the RealWings download into the aircraft folder. The installer finds the `RealWings3XX/` source folders there and copies them into `objects/RealWings3XX/` itself. For the A320 and A321 the download nests its assets in `CEO/` and `NEO/` subfolders, which the installer merges on its own.
2. Place the installer in the same folder and run it. It asks for the aircraft, the wingtip variant and whether to install the optional cabin window frames.

The installer swaps the stock wing OBJs for the RealWings versions at the correct positions, with matching shadow modes and lighting flags, removes the geometry blocks that become obsolete (`LIGHT_PARAM` blocks in the lighting OBJ, stale `TRIS` in `Decals.obj` and, on an A319 without the Carda mod, in `engines.obj`) and corrects the engine coordinates if it finds the Carda mod installed. Backups are written as `*.bak` before any change, and `.acf` files that do not belong to X-Plane 12 are skipped. There is no uninstall option — going back means restoring those backups by hand, and because the installer never overwrites an existing `.bak`, a backup left behind by another wing mod is not necessarily the stock state.

One step stays manual: if a livery brings its own RealWings textures, its `objects/RealWings3XX/` folder has to be copied into the matching livery folder.

!!! note "Linux: native installer binary"

    Native Linux binaries are available (`install-realwings-linux-x64` and `-arm64`); `chmod +x`, then run from the aircraft folder. `install_realwings.py` works directly with Python 3.10+ without external dependencies. Non-interactive via `--aircraft`, `--variant`, `--frames` and `--aircraft-dir`; the variant keys are `ceo` (A319 only), `ceo-wingtips`, `ceo-sharklets` and `neo`.

!!! warning "A ToLiss update removes the mod"

    As with every mod that edits the aircraft's own files, an update via SkunkCraftsUpdater restores the stock state and the installer has to be re-run afterwards.

!!! warning "RealWings and the Durantula mod overlap"

    RealWings does not rewrite the stock wing OBJs but removes them from the `.acf` outright, which silently voids the [Durantula mod](durantula_wing_mod.md)'s in-place edits. Beyond that, both also edit `Decals.obj`, the lighting OBJ and the Carda engine OBJs. Neither installer knows about the other — they detect only the Carda mod — and RealWings deletes the obsolete Carda "kit" geometry by line number, which a previous Durantula run has already shifted. Treat the two as alternatives, not a stack.

    Switching from Durantula to RealWings therefore means restoring the `*.durantula.bak` backups **first** — above all those of the Carda engine OBJs. Durantula has already deleted a `TRIS` line there, while RealWings looks for the obsolete Carda geometry at fixed line numbers, so it would silently delete the wrong block from a file that is one line shorter than it expects.

!!! note "Lighting mod goes last"

    [ToLiss Photon](toliss_photon.md) patches the RealWings light objects so its light positions match the new geometry. Its installer therefore has to run after this one — and again after every re-run.

## Sources

- [RealWings320](https://forums.x-plane.org/files/file/99352-realwings320-wing-replacement-mod-for-toliss-a320neo/) — wing replacement mod by GeoBuilds (A319 and A321 versions linked above)
- [xplane-toliss-realwings-installer](https://github.com/iy4vet/xplane-toliss-realwings-installer) — installer source, binaries and documentation
