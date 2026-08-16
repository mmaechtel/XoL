---
description: "The Durantula Wing Enhancement MOD reworks flaps, flap-track fairings and wingflex on the ToLiss A319, A320 and A321 — with a Linux installer."
---
# Durantula Wing Enhancement MOD

The Durantula Wing Enhancement MOD reworks parts of the ToLiss wing on the A319, A320 and A321: new flap and flap-track-fairing geometry, and a wingflex built on [X-Plane](../../../glossary.md#x-plane)'s own wing deflection instead of the animation ToLiss ships. Both parts are independent and can be installed separately or together.

## Background

- **Mod developer:** Durantula2405 (3D modelling and animation: Giorgi_Z4)
- **Installer developer:** iy4vet
- **Mod download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/88518-toliss-a319-a320-and-a321-wing-enhancement-mod/)
- **Installer:** [github.com/iy4vet](https://github.com/iy4vet/xplane-toliss-durantula-installer)
- **Platforms:** The mod itself is OBJ and texture data and platform-independent; the installer ships native binaries for Linux, macOS and Windows
- **Compatibility:** X-Plane 12, ToLiss A319, A320 and A321
- **License:** Mod as a free forum download, installer under GPL-3.0

The mod is purely visual — it changes geometry, textures and animations, not the aircraft's systems.

## Features

- **Flaps:** Replaces the stock flaps and flap-track fairings in the wing OBJs with new meshes and their own textures. On CEO airframes the obsolete engine "kit" geometry overlapping the new fairings is removed as well: from the Carda engine OBJs if those are installed, otherwise from the stock `engines.obj`
- **Wingflex:** Replaces ToLiss's own winglet-flex animations in the wing, glass, decal, light and particle OBJs with X-Plane's native `wing_tip_deflection_deg` animation, and sets the wing damping properties in the `.acf`
- **Paint kit:** An optional "New Wing Textures" set is included; the finished livery goes into the aircraft's `liveries/` folder by hand

The two parts are coupled more tightly than their separate installation suggests: the new flap mesh is modelled flat and only bends onto the wing through the wingflex animation. The installer therefore picks the flexing mesh whenever the wingflex is installed as well, and the static one otherwise.

## Value in Flight Simulation

Flaps and flap-track fairings sit where the eye goes during approach and after landing, and the stock geometry is the coarsest part of the ToLiss exterior model. The wingflex is the wider change: X-Plane's native deflection reacts to load and turbulence instead of running a fixed animation, so the wing moves differently on a rough approach than on a smooth one. Neither part changes how the aircraft flies.

## Installation

**Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/88518-toliss-a319-a320-and-a321-wing-enhancement-mod/) · **Installer:** [GitHub Releases](https://github.com/iy4vet/xplane-toliss-durantula-installer/releases)

Installing the mod by hand means editing OBJ files in a text editor and the `.acf` in Plane Maker. The installer automates every one of those edits:

1. Unpack the mod download — it produces folders named `Durantula_ToLiss_New_Flaps_*`, `Durantula_ToLiss_Wingflex_*` and a manual.
2. Put those folders **and** the installer into the aircraft folder, next to the `.acf` file. Nothing is copied by hand; the installer pulls the OBJs and textures out of the mod folders itself. `--mod-dir` points it at another location.
3. Run the installer from that folder. It asks for the aircraft, the parts to install and — on an A319 or A320 carrying both engine families — which flap mesh to use.

The engine family is read from the `.acf` automatically. Every edit matches on geometry and animation content instead of line numbers, so it still works when other mods — the Carda engines or a lighting mod — have shifted the line numbering, and it is safe to re-run. Backups are written as `*.durantula.bak` before any file is touched. If the stock flap geometry cannot be removed, the installer aborts rather than stack the new flaps on top of it.

!!! note "Linux: native installer binary"

    Native Linux binaries are available (`install-durantula-linux-x64`, also ARM64). Make the binary executable with `chmod +x` and run it from the aircraft folder, or run `install_durantula.py` directly with Python 3.10+ — no external dependencies. Both accept `--aircraft`, `--parts`, `--flaps-engine`, `--textures`, `--mod-dir` and `--aircraft-dir` for a fully non-interactive install, which is worth setting up because the mod has to be reinstalled regularly.

!!! warning "A ToLiss update removes the mod"

    An update via SkunkCraftsUpdater restores the stock files, so the installer has to be re-run after every one. Repeated runs are harmless — the installer detects work already done and neither duplicates objects nor over-deletes geometry. The `*.durantula.bak` backups allow a rollback at any time; the suffix is mod-specific, so it never collides with another mod's or SkunkCrafts' own `.bak` files. There is no uninstall option — restoring those backups is the way back.

!!! warning "RealWings and the Durantula mod overlap"

    Both mods target the same files, and [RealWings](realwings.md) removes the stock wing OBJs from the `.acf` outright, which silently voids this mod's in-place edits. Beyond that, both also edit `Decals.obj`, the lighting OBJ and the Carda engine OBJs, and neither installer knows about the other — they detect only the Carda mod. Treat the two as alternatives, not a stack.

    Coming from RealWings, restore its `*.bak` backups **first** — in particular the `.acf`. RealWings shifts the Carda engine coordinates to match its own wing, and this installer does not set them back.

!!! note "Lighting mod goes last"

    [ToLiss Photon](toliss_photon.md) installs a light variant built for the wing that is actually drawing, so its installer has to run after this one — and again after every re-run.

## Sources

- [Toliss A319, A320 and A321 — Wing Enhancement MOD](https://forums.x-plane.org/files/file/88518-toliss-a319-a320-and-a321-wing-enhancement-mod/) — mod by Durantula2405
- [xplane-toliss-durantula-installer](https://github.com/iy4vet/xplane-toliss-durantula-installer) — installer source, binaries and documentation
