# ToLiss FlyWithLua Ecosystem

<div class="video-container" markdown>
<video controls width="100%" preload="metadata" poster="../../assets/video/en/toliss_flow_with_plugins/Beyond_the_Default_Cockpit.jpg">
  <source src="../../assets/video/en/toliss_flow_with_plugins/Beyond_the_Default_Cockpit.mp4" type="video/mp4">
</video>
</div>

The community has built an extensive ecosystem of [FlyWithLua](flywithlua.md) scripts around the ToLiss fleet (A319, A320 CEO/NEO, A321 CEO/NEO, A330neo, A340-600). These scripts extend the aircraft with callouts, cockpit automation, boarding simulation, and more. Additionally, several standalone plugins integrate with the ToLiss fleet.

Most scripts require the X-Airbus Library as a foundation. Start by installing that library, then pick the scripts that match your workflow — from callouts and cockpit initialization to full First Officer assistance.

## X-Airbus Library

The X-Airbus Library is a Lua library that serves as the foundation for many ToLiss scripts. It provides common functions and dataref access used by dependent scripts.

- **Developer:** FrankLFRS
- **Type:** FlyWithLua module
- **Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/92739-x-airbus-library/)
- **Compatible with:** A319, A320 CEO/NEO, A321 CEO/NEO, A330neo, A340-600

!!! warning "Installation"

    The X-Airbus Library goes into the FlyWithLua `Modules/` folder — not into `Scripts/`. Scripts that depend on X-Airbus will not work without the library.

## Callouts & Sound

### ToLiss V-Speeds

V-Speed callouts for takeoff and landing: Spoilers, Reverse Green, Brake Low/Medium, Decel, 70 Knots, plus Gear Down, Flaps, Speed Checked, and Go-Around Flaps. PF/PM voices and volumes are configurable per aircraft type.

- **Requires:** X-Airbus Library
- **Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/92767-toliss-v-speeds/)

### PMCO — Pilot Monitoring Callouts

FlyWithLua script by hotbso that speaks standard Pilot Monitoring callouts and reacts to pilot inputs (e.g., "Gear up"). Supports normal procedures and touch-and-go training. Multiple soundsets available (male/female, Airbus-compliant).

- **Requires:** FlyWithLua, ToLiss fleet only
- **Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/90074-pmco-pilot-monitoring-callouts-for-the-toliss-fleet/)

### ToLiss Announcements

Plays flight attendant and captain announcements and manages ECAM Cabin Ready. [X-Plane](../glossary.md#x-plane) 12 only.

- **Requires:** X-Airbus Library
- **Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/95101-toliss-announcements/)

!!! info "Linux: Airline-specific sound packs"

    ToLiss Announcements ships with a .exe switcher for airline-specific sound packs. Under Linux, this tool does not run — copy the desired sound files manually into the script's sound folder.

### DK Toliss Callout — FMA Callouts

FlyWithLua script that announces autopilot mode changes (CLB, OP CLB, SPEED, NAV, G/S) via text-to-speech. Reads the blue FMA values from the upper PFD box. On Linux, [XLinSpeak](xlinspeak.md) is required for audible output. [→ Detail page](dk_toliss_callout.md)

- **Developer:** cxn0026
- **Requires:** FlyWithLua
- **Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/91367-toliss-airbus-fma-callout-flywithlua-script/)

### Cockpit Rain Noise

Adds rain sounds to the cockpit. Volume scales with precipitation amount and fades with increasing speed. Volume configurable in dB, individual aircraft types can be excluded.

- **Requires:** X-Airbus Library
- **Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/94901-toliss-cockpit-rain-noise/)

## Cockpit Automation

### TOI Cabin Ready

Automatically sends the Cabin Ready call: at departure after 4–8 minutes (based on passenger count), on approach a few seconds after flaps and gear are extended. Handles edge cases like go-arounds safely. [→ Detail page](toicabrdy.md)

- **Developer:** cxn0026
- **Requires:** FlyWithLua
- **Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/91876-toliss-airbus-cabin-ready-automatic-flywithlua-script/)

### ToLiss Init

Initializes the cockpit according to personal preferences: ND mode, ND range, MKR beeps, external power status, CSTR light, and more. The script waits until BAT 1 + BAT 2 are switched on and applies the configuration after approximately 15 seconds.

- **Requires:** X-Airbus Library
- **Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/95194-toliss-init/)

### Speedy Copilot

Comprehensive FO/PM assistant that handles First Officer and Pilot Monitoring tasks from cockpit preparation through engine start to landing. Includes a PDF manual and multiple voice packs (US, British, French, Australian, Egyptian). Works with X-Plane 11 and 12.

- **Compatible with:** A319, A320 CEO/NEO, A321 CEO/NEO, A330neo, A340-600
- **Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/54069-speedy-copilot-for-toliss/)

### Windshield & Window Icing Mod

Lua-based mod that simulates icing on cockpit and cabin windows. Takes into account relative humidity, OAT, and spread. Ice clears only with active window heat / pitot heat and melts with realistic animation. Visual effects for A320 only; the Lua code also works with A346 and A339.

- **Requires:** FlyWithLua
- **Download:** [forums.x-plane.org](https://forums.x-plane.org/files/category/9-utilities/)

## Boarding & Ground

### TOBUS — Boarding/Deboarding

Simulates a realistic boarding and deboarding process with live payload adjustment. Passenger count can be set manually or imported via SimBrief. Three speed modes: Real, Fast, Instant. Front and rear door or front door only. An enhanced version by hotbso ([GitHub](https://github.com/hotbso/TOBUS/releases)) offers additional door options and A346 support.

- **Requires:** FlyWithLua, X-Airbus Library (in Modules folder)
- **Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/87996-tobus-your-toliss-boarding-lua-script/)

### ToLiss Ground Services

Automatic chock and external power management. At departure: APU available + PAX/cargo doors closed — chocks removed, external power disconnected. On arrival: parking brake + N1 < 10% — chocks set, external power connected.

- **Requires:** X-Airbus Library
- **Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/94691-toliss-ground-services/)

## Mods

### Easy Freighter — A321 P2F Cargo Door Mod

Simulates a cargo main door for the A321P2F/A321PCF with rigid cargo barrier and window plugs as a FlyWithLua object. Includes freight airline liveries. A separate version also exists for the A320. Not officially approved by ToLiss.

- **Developer:** XPJavelin
- **Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/92976-easy-freighter-conversion-kit-for-the-toliss-321/)

### Carda Realistic Engine Mods

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

## Related Plugins

The following standalone plugins integrate with the ToLiss fleet but are documented on separate pages:

- **[simbrief_hub](https://github.com/hotbso/simbrief_hub)** — provides SimBrief data as datarefs, used by [AutoDGS](autodgs.md), [openSAM](opensam.md), and other plugins
- **[XGS](xgs.md)** — Landing speed analysis with ToLiss-specific gear strut detection
- **[Follow the Greens](followthegreens.md)** — A-SMGCS taxiway guidance system
- **[openSAM](opensam.md)** — Jetways, VDGS, marshaller for custom sceneries
- **[AutoDGS](autodgs.md)** — Docking guidance for default airports
- **[AviTab](avitab.md)** — Cockpit tablet with PDF viewer and moving map
- **[KOSP Project](kosp_project.md)** — FMOD soundscape for A319, A320, A321 (all engine variants)
- **[Mango Studios](mango_studios.md)** — FMOD sound packs for the complete ToLiss fleet

