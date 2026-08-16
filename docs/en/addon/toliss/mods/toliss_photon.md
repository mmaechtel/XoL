---
description: "ToLiss Photon reworks exterior and cockpit lighting on the ToLiss A319, A320, A321 and A330-900 — native plugin, own Linux installer, GPLv3."
---
# ToLiss Photon

ToLiss Photon reworks the lighting of the ToLiss Airbus fleet in [X-Plane](../../../glossary.md#x-plane) 12. Every exterior light is re-authored in the aircraft's OBJ files, a native plugin takes over the beacon and strobe flashing, and an optional cockpit lighting set by Gus Rodrigues is installed alongside it. Which lamp technology the aircraft uses — halogen and Xenon, LED, or a mix — is switchable in the simulator and saved per livery.

## Background

- **Developer:** schmal (cockpit lighting: Gus Rodrigues, integrated with permission)
- **Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/100717-toliss-photon-complete-lighting-mod-for-toliss-a330a319a320a321/)
- **Source:** [github.com/ischmal](https://github.com/ischmal/toliss-photon-lighting)
- **Platforms:** Windows, macOS, Linux (installer and plugin built per platform, Linux as x86_64)
- **Compatibility:** X-Plane 12, ToLiss A319, A320 (CEO/NEO), A321 (CEO/NEO) and A330-900
- **Dependency:** None — compiled native plugin, neither [FlyWithLua](../../scripting/flywithlua.md) nor [XPPython3](../../scripting/xppython3.md) is required
- **License:** GPL-3.0, free download

## How It Works

X-Plane draws two kinds of light: billboards, the 2D sprites that give a light its on-screen glow, and spill lights, which actually illuminate the surroundings. A billboard needs a direction to look convincing — brightest when faced head-on, fading out as the camera pans away. Many of the stock ToLiss billboards omit that direction and stay equally bright through all 360 degrees, which is the main reason for their flat appearance.

Photon rewrites every light in the OBJ files, gives each one a direction (except the upper and lower beacons, which really are visible from all sides) and reads custom datarefs so the same light can appear as halogen or as LED. The flashing itself comes from the plugin: every frame it overwrites the sim's beacon and strobe brightness datarefs — the ones ToLiss drives itself — replacing the stock sine-wave fade with the behavior of the actual lamp type.

## Features

- **Exterior lighting:** All exterior lights re-authored, excessive default intensity reduced, individual lights switchable between halogen and LED
- **Beacon and strobe:** LED beacons blink instead of fading; Xenon flash tubes fire instantly with an imperceptible decay
- **Color characteristics:** Halogen runs visibly warmer with desaturated navigation lights; white LEDs appear cool-white with strongly saturated red and green; the Xenon beacon trends slightly pink through the red glass
- **Cockpit lighting:** Optional during installation, switchable between old halogen, new halogen and LED
- **Screen glow:** Display units, MCDUs and DCDUs get a backlight effect of their own — independent of the cockpit lighting and available on the A330-900 as well
- **In-sim adjustment:** Lighting options can be changed with the aircraft loaded, no restart and no reinstall
- **Per livery:** Preferences are saved separately for each livery

## Light Profiles

Instead of a single look, the mod ships profiles that group the lamp technology by aircraft generation.

| Profile | Exterior lighting |
| --- | --- |
| Classic | Halogen throughout, Xenon flash tubes for strobes and beacons |
| Hybrid LED | LED for navigation and anti-collision lights, halogen for illumination |
| Full LED | All exterior lights LED |
| Auto | Profile selected automatically from the aircraft's equipment |
| Custom | Taxi, takeoff, runway turnoff, landing, wing inspection, navigation, beacon, strobe and logo lights set individually |

The cockpit lighting offers three looks of its own — warm orange, a lighter amber, and cool white — and is not available for the A330-900. Its light design, placement and textures are Gus Rodrigues' work; Photon only makes them switchable in the simulator.

## Value in Flight Simulation

The stock beacon fades in and out like a warming filament, which no beacon does — it is either a Xenon flash tube or an LED. That mismatch is what the project started with, and the correction is visible on every ground movement and every external view. The lamp-technology profiles add a second layer: the same airframe can be given halogen and Xenon or an all-LED set, matched to the livery it wears. How much this is worth depends on how often the aircraft is seen from outside or at night, and the cockpit lighting only pays off for those who fly the ToLiss at night.

## Installation

**Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/100717-toliss-photon-complete-lighting-mod-for-toliss-a330a319a320a321/) or [GitHub Releases](https://github.com/ischmal/toliss-photon-lighting/releases)

The Linux download is a `.tar.gz` containing the installer, the `data/` folder with the light objects, cockpit textures and plugin, plus a `README.txt`. No files are moved by hand — the archive can stay in the download folder:

1. Unpack the entire archive and leave the installer and `data/` together; the installer reads `data/` from beside itself.
2. Open a terminal in that folder and run `./photon-installer` — `chmod +x photon-installer` first if the executable bit did not survive unpacking.
3. Follow the steps: the installer detects X-Plane 12 on its own, then asks for the aircraft, the wing variant and whether the cockpit lighting should be installed.

The same installer also uninstalls and restores the original ToLiss files.

!!! note "Linux specifics"

    The installer window is drawn on the GPU. If it comes up black or blank — VM, remote session, old drivers — `./photon-installer --software` renders it on the CPU, and `./photon-installer-console` is the identical installer as a text-mode program. The Browse button for the X-Plane path calls `zenity` or `kdialog`; on a minimal desktop with neither installed, the path can be typed in directly. The Linux bundle is built for x86_64 only, no ARM build is offered.

!!! warning "Install after the wing mods"

    On the A319, A320 and A321 the light positions depend on the wing geometry. Both the [Durantula mod](durantula_wing_mod.md) and [RealWings](realwings.md) are supported, but Photon has to match the wing that is actually drawing — on RealWings it patches the mod's own light objects, on Durantula it installs a variant built for that wing — so it has to run **after** the wing mod. Re-running a wing installer afterwards means running the Photon installer again as well.

!!! warning "A ToLiss update removes the mod"

    The lighting lives in the aircraft's OBJ files, and a ToLiss update via SkunkCraftsUpdater restores them to stock. The installer detects this — it writes a version marker into the OBJ and checks whether that marker is still there — but the mod has to be reinstalled after every aircraft update. The original files are kept in `Photon Backup Files/` inside the aircraft folder.

Gus Rodrigues' [A320 Family Light Mod](https://forums.x-plane.org/files/file/93337-a320-light-mod/) does not need to be installed separately for the cockpit — that part comes with Photon. Installing his package by hand afterwards overwrites Photon's exterior lights, since it ships its own light object; for the exterior lighting the two mods are alternatives, not a stack.

!!! tip "Performance"

    The plugin brings its own performance analysis tool, reachable from the Settings tab of its window. It times the cockpit with each of Photon's effects switched off in turn, so what a feature costs in frames can be measured on the machine that actually has to render it — rather than taken from someone else's numbers.

## Sources

- [ToLiss Photon — forums.x-plane.org](https://forums.x-plane.org/files/file/100717-toliss-photon-complete-lighting-mod-for-toliss-a330a319a320a321/)
- [toliss-photon-lighting — GitHub](https://github.com/ischmal/toliss-photon-lighting) — source, readme and releases
