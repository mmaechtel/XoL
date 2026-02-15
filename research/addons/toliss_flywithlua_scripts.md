# ToLiss FlyWithLua Scripts Ecosystem — Research

**Date:** 2026-02-15
**Sources:** forums.x-plane.org (file downloads), web search results
**Scope:** FlyWithLua scripts specifically for ToLiss aircraft in X-Plane 12

---

## Overview

A community member named **FrankLFRS** has built an ecosystem of FlyWithLua scripts for ToLiss aircraft, all sharing a common library called **X-Airbus**. The scripts are distributed exclusively through the X-Plane.org forum file downloads — no GitHub repository was found. All scripts are free.

In addition to FrankLFRS's ecosystem, a few independent scripts from other authors also target ToLiss aircraft.

---

## 1. X-Airbus Library

| Field | Detail |
|-------|--------|
| **Forum URL** | https://forums.x-plane.org/files/file/92739-x-airbus-library/ |
| **GitHub** | Not found — no public GitHub repository |
| **Author** | FrankLFRS |
| **Current version** | v1.11 (released 2026-02-15) |
| **Status** | Active (regularly updated) |
| **Type** | FlyWithLua module (placed in `Modules/`, not `Scripts/`) |

### What it provides

- Shared Lua functions for all FrankLFRS ToLiss scripts
- Aircraft detection and state functions (e.g., `OnGround()`, `Flying()`, `DetectAutoBrakeOff()`)
- Common dataref access layer for ToLiss-specific datarefs
- No user-facing documentation was created by the author ("intended for use by my own LUA scripts")

### Compatibility

- ToLiss A319, A320neo, A321(-neo), A330neo — confirmed
- ToLiss A340 and A320ceo — "should be OK" (author note)

### Installation

Copy `X-Airbus.lua` to:
```
X-Plane 12/Resources/plugins/FlyWithLua/Modules/
```

### Version requirements per script

| Script | Minimum X-Airbus version |
|--------|--------------------------|
| ToLiss Auto APU | v1.0+ |
| ToLiss Auto Lights | v1.6+ |
| ToLiss Cockpit Rain Noise | v1.6+ |
| ToLiss Auto ANTI ICE | v1.6+ |
| ToLiss NWS bound to Roll | v1.7+ |
| ToLiss Ground Services | requires X-Airbus (version unspecified) |
| ToLiss Init | v1.9+ |
| ToLiss V-Speeds | v1.10+ |
| ToLiss Announcements | v1.10+ |

### Dependent scripts (complete FrankLFRS ecosystem)

1. X-Airbus Library (foundation)
2. ToLiss More Commands
3. ToLiss Auto APU
4. ToLiss Auto Lights
5. ToLiss Auto ANTI ICE
6. ToLiss Cockpit Rain Noise
7. ToLiss NWS bound to Roll
8. ToLiss Ground Services
9. ToLiss V-Speeds
10. ToLiss Init
11. ToLiss Announcements
12. ToLiss Custom Cabin Announcements (add-on for Announcements)

---

## 2. ToLiss V-Speeds Callouts

| Field | Detail |
|-------|--------|
| **Forum URL** | https://forums.x-plane.org/files/file/92767-toliss-v-speeds/ |
| **Author** | FrankLFRS |
| **Current version** | v3.0 (released 2026-02-10) |
| **Status** | Active |
| **Requires** | FlyWithLua NG+, X-Airbus v1.10+ |

### What it does

Provides V-Speed callouts for takeoff and landing phases with separate PF (Pilot Flying) and PM (Pilot Monitoring) voices.

**Takeoff callouts:**
- SRS Autothrust blue, Thrust set, 100 Knots, V1, Rotate, Positive Climb, Gear Up, Nav

**Landing callouts:**
- Spoilers, Reverse green, Brake low/medium, Decel, 70 Knots, Gear down, Flaps 0/1/2/3/Full, Speed checked flaps, Go-around Flaps

### Configuration options

- Airbus voice instead of PM voice for V1 callout
- Autobrake Off callout (on/off)
- BRAKE LO/MEDIUM callouts (on/off)
- Separate voice selection for PF and PM (8 voices available)
- Sound samples from luvvoice.com, reworked with +12 dB compressor

### Compatibility

- ToLiss A319, A320(-neo), A321(-neo), A330neo — confirmed
- A340 — "should be OK"

---

## 3. ToLiss Announcements

| Field | Detail |
|-------|--------|
| **Forum URL** | https://forums.x-plane.org/files/file/95101-toliss-announcements/ |
| **Author** | FrankLFRS |
| **Current version** | v1.3.1 (released 2026-01-05) |
| **Status** | Active |
| **Requires** | FlyWithLua NG+, X-Airbus v1.10+ |

### What it does

- Plays flight attendant and captain announcements during various flight phases
- Manages ECAM Cabin Ready automatically (replaces standalone cabin ready scripts)
- Automatic cockpit door management (v1.3.1 feature)
- X-Plane 12 only

### Relation to Cabin Ready

This script **includes** automatic Cabin Ready management as a built-in feature. It supersedes the standalone "Toliss Airbus Cabin Ready" script (by cxn0026, see item 7) for users of this ecosystem.

### Add-on: ToLiss Custom Cabin Announcements

| Field | Detail |
|-------|--------|
| **Forum URL** | https://forums.x-plane.org/files/file/96029-toliss-custom-cabin-announcements/ |
| **Author** | FrankLFRS |

An extension package for ToLiss Announcements that provides:
- An executable for switching between airline-specific cabin announcement sound packs
- Multiple airline options included
- Credits to @fearlessfrog, @afterrfluff, @sjames1066 for cabin announcement contributions
- Linux note: The "exe" switcher is likely Windows-only; manual file copy should work on Linux

---

## 4. ToLiss Cockpit Rain Noise

| Field | Detail |
|-------|--------|
| **Forum URL** | https://forums.x-plane.org/files/file/94901-toliss-cockpit-rain-noise/ |
| **Author** | FrankLFRS |
| **Created** | 2025-03-30 |
| **Downloads** | ~960 |
| **Status** | Active |
| **Requires** | FlyWithLua NG+, X-Airbus v1.6+ |

### What it does

- Adds ambient rain sound in the cockpit
- Rain noise intensity varies with precipitation amount (increases/decreases dynamically)
- Customizable rain sound levels
- Option to exclude certain aircraft from the rain effect

### Installation

Copy `ToLiss_Rain` folder and lua file to:
```
X-Plane 12/Resources/plugins/FlyWithLua/Scripts/
```

---

## 5. ToLiss Init

| Field | Detail |
|-------|--------|
| **Forum URL** | https://forums.x-plane.org/files/file/95194-toliss-init/ |
| **Author** | FrankLFRS |
| **Created** | 2025-11-29 |
| **Status** | Active |
| **Requires** | FlyWithLua NG+, X-Airbus v1.9+ |

### What it configures

- ND rose mode (Captain and copilot): value 0-4 or 5 to set rotary switch position, or `nil` to skip
- ND range (Captain and copilot): configurable
- External power: plugged/unplugged at startup (`true`/`false`/`nil`)
- Waits until aircraft is powered on (BAT 1 + BAT 2 on at minimum)
- Settings applied approximately 15 seconds after power up

---

## 6. Windshield & Window Icing Mods

There are **two separate mods** from different authors addressing icing:

### 6a. TOLICE

| Field | Detail |
|-------|--------|
| **Forum URL** | https://forums.x-plane.org/files/file/98228-tolice/ |
| **Author** | Unknown (not FrankLFRS) |
| **Created** | 2026-01-12 |
| **Status** | Active |
| **Type** | Standalone Lua script (no X-Airbus dependency noted) |

- Small Lua script to make windshield icing visible on ToLiss planes
- Windows icing adjusted to Pitot-tube temperature
- Responds to Pitot-tube/windshield heat button
- Recommended to pair with "Icing Simulator" for enhanced icing math/visuals

### 6b. ToLiss A320 Windows Icing & Cabin Rain

| Field | Detail |
|-------|--------|
| **Forum URL** | https://forums.x-plane.org/files/file/98503-toliss-a320-windows-icing-cabin-rain/ |
| **Author** | ZoraBa |
| **Status** | Active |
| **Type** | Lua script + replacement OBJ files |

More comprehensive than TOLICE:
- Window icing appears when icing conditions are present
- Ice disappears only when window heat / pitot heat is ON
- Icing fades faster in window center, slower near edges (windshield frame as heat sink)
- Passenger cabin windows: both rain AND ice effects
- **Requires replacing aircraft OBJ files** (invasive: copies .acf and .obj files into ToLissA320 folder)
- A320-specific (not generic ToLiss fleet)

---

## 7. Cabin Ready (Standalone)

| Field | Detail |
|-------|--------|
| **Forum URL** | https://forums.x-plane.org/files/file/91876-toliss-airbus-cabin-ready-automatic-flywithlua-script/ |
| **Author** | cxn0026 |
| **Status** | Active but effectively superseded by ToLiss Announcements |
| **Type** | Standalone FlyWithLua script (no X-Airbus dependency) |

### What it does

- Automatically sends "Cabin Ready" (forward call button) for all ToLiss Airbus aircraft
- Departure: cabin ready 4-8 minutes after doors close (based on passenger count)
- Approach: cabin ready a few seconds after both flaps and gears are down
- Handles go-around and through-flight scenarios
- Tested under XP12, might work in XP11

### Relation to ToLiss Announcements

FrankLFRS's "ToLiss Announcements" (item 3) includes Cabin Ready management as a built-in feature. Users who install the full Announcements script do **not** need this standalone script. This script by cxn0026 predates the Announcements script and is useful for users who want Cabin Ready without the full announcement system.

---

## 8. A321 P2F Cargo Door Mod

There are **two separate P2F conversion mods** for the ToLiss A321:

### 8a. Easy Freighter (conversion kit)

| Field | Detail |
|-------|--------|
| **Forum URL** | https://forums.x-plane.org/files/file/92976-easy-freighter-conversion-kit-for-the-toliss-321/ |
| **Author** | XPJavelin |
| **Version** | v3.3 (2024-12-18) |
| **Status** | Active |

- Drag-and-drop object file placed in A321 objects folder
- Includes cargo door, removed passenger seats, reinforced floor, freight security systems
- Distributed with a demonstration livery
- Separate livery packs available (file 72821)
- Also has an A320 variant (file 96570)
- **Not a FlyWithLua script** — purely 3D object + ACF modification

### 8b. Passenger to Freighter conversion (P2F)

| Field | Detail |
|-------|--------|
| **Forum URL** | https://forums.x-plane.org/index.php?/files/file/66869-passenger-to-freighter-conversion-p2f-for-the-toliss-321/ |
| **Author** | Unknown |
| **Status** | Older mod |

- Main cargo door + window plugs as single 3D object
- Includes liveries: Minoan Airlines (fictional), Austria Post-Qantas Freight (real), Amazon Air (fictional)
- **Not a FlyWithLua script** — 3D object mod

---

## Additional FrankLFRS Scripts (not in original query)

These were discovered during research and are part of the X-Airbus ecosystem:

### ToLiss More Commands

| Field | Detail |
|-------|--------|
| **Forum URL** | https://forums.x-plane.org/files/file/92711-toliss-more-commands/ |
| **Author** | FrankLFRS |

Adds keyboard-assignable commands:
- Toggle Spoilers Armed, Toggle Dome Light, Toggle Autopilot
- Toggle External Power, Toggle Chocks, Toggle WX PWS
- Increase/Decrease SPD commands

### ToLiss Auto Lights

| Field | Detail |
|-------|--------|
| **Forum URL** | https://forums.x-plane.org/files/file/92762-toliss-auto-lights/ |
| **Author** | FrankLFRS |
| **Version** | v1.1 |
| **Downloads** | ~147 |
| **Requires** | X-Airbus v1.6+ |

Automated light management for flight phases (takeoff, climb, cruise, descent, landing). Supports spawn in midair.

### ToLiss Auto APU

| Field | Detail |
|-------|--------|
| **Forum URL** | https://forums.x-plane.org/files/file/92745-toliss-auto-apu-v12/ |
| **Author** | FrankLFRS |
| **Version** | v1.2 |
| **Requires** | X-Airbus v1.0+ |

APU off when engines ready, APU on after landing (at flaps up). Manual on/off for cold & dark and arrival at gate.

### ToLiss Auto ANTI ICE

| Field | Detail |
|-------|--------|
| **Author** | FrankLFRS |
| **Requires** | X-Airbus v1.6+ |

Automatically switches anti-ice (engines + wings) based on conditions. Configurable deicing duration.

### ToLiss NWS bound to Roll

| Field | Detail |
|-------|--------|
| **Forum URL** | https://forums.x-plane.org/files/file/93817-toliss-nws-bound-to-roll/ |
| **Author** | FrankLFRS |
| **Requires** | X-Airbus v1.7+ |

Binds roll axis to nosewheel steering (useful without rudder pedals). Keeps 6 deg NWS from yaw axis at slow speeds, full range on roll axis.

### ToLiss Ground Services

| Field | Detail |
|-------|--------|
| **Forum URL** | https://forums.x-plane.org/files/file/94691-toliss-ground-services/ |
| **Author** | FrankLFRS |
| **Requires** | X-Airbus (version unspecified) |

Automated ground services:
- Departure: APU available + PAX/Cargo doors closed -> chocks pulled, external power unplugged
- Arrival: park brake set + N1 below 10% -> chocks added, external power plugged

---

## Linux-Specific Notes

1. **FlyWithLua NG+** officially supports Linux (Win, Lin, Mac). GitHub: https://github.com/X-Friese/FlyWithLua
2. **Lua scripts are cross-platform** — no re-editing needed for Linux. The scripts themselves contain no OS-specific code.
3. **ToLiss Custom Cabin Announcements** includes a `.exe` switcher tool for selecting airline-specific sound packs. This will not run natively on Linux; manual file copy to the announcement directory is the workaround.
4. **ToLiss A320 Windows Icing & Cabin Rain** (by ZoraBa) replaces aircraft `.acf` and `.obj` files. This is platform-independent but invasive — will be overwritten by aircraft updates.
5. **No known Linux-specific bugs** were found for any of these scripts in forum discussions.

---

## Related Scripts (not FrankLFRS, not X-Airbus dependent)

| Script | URL | Author | Description |
|--------|-----|--------|-------------|
| PMCO: Pilot Monitoring Callouts | https://forums.x-plane.org/files/file/90074-pmco-pilot-monitoring-callouts-for-the-toliss-fleet/ | Unknown | Alternative to V-Speeds, ported to X-Plane for ToLiss fleet, "strictly by the books of Airbus" |
| Toliss Airbus FMA Callout | https://forums.x-plane.org/files/file/91367-toliss-airbus-fma-callout-flywithlua-script/ | Unknown | FMA callouts for ToLiss, verified on A319 and A320neo |
| TOBUS | https://forums.x-plane.org/files/file/87996-tobus-your-toliss-boarding-lua-script/ | Unknown | Boarding/deboarding process simulation for ToLiss |
| ToLoadHub | https://github.com/Butzy79/toloadhub | Butzy79 | Passenger and cargo management for ToLiss (on GitHub) |

---

## Summary Table

| # | Script | Author | X-Airbus? | Active? | Forum File ID |
|---|--------|--------|-----------|---------|---------------|
| 1 | X-Airbus Library | FrankLFRS | IS the library | Yes (v1.11) | 92739 |
| 2 | ToLiss V-Speeds | FrankLFRS | v1.10+ | Yes (v3.0) | 92767 |
| 3 | ToLiss Announcements | FrankLFRS | v1.10+ | Yes (v1.3.1) | 95101 |
| 4 | ToLiss Cockpit Rain Noise | FrankLFRS | v1.6+ | Yes | 94901 |
| 5 | ToLiss Init | FrankLFRS | v1.9+ | Yes | 95194 |
| 6a | TOLICE | Unknown | No | Yes | 98228 |
| 6b | A320 Windows Icing & Cabin Rain | ZoraBa | No | Yes | 98503 |
| 7 | Cabin Ready (standalone) | cxn0026 | No | Superseded | 91876 |
| 8a | Easy Freighter (A321 P2F) | XPJavelin | No | Yes (v3.3) | 92976 |
| 8b | P2F conversion (older) | Unknown | No | Older | 66869 |
| -- | ToLiss More Commands | FrankLFRS | No | Yes | 92711 |
| -- | ToLiss Auto Lights | FrankLFRS | v1.6+ | Yes | 92762 |
| -- | ToLiss Auto APU | FrankLFRS | v1.0+ | Yes (v1.2) | 92745 |
| -- | ToLiss Auto ANTI ICE | FrankLFRS | v1.6+ | Yes | -- |
| -- | ToLiss NWS bound to Roll | FrankLFRS | v1.7+ | Yes | 93817 |
| -- | ToLiss Ground Services | FrankLFRS | Yes | Yes | 94691 |
| -- | Custom Cabin Announcements | FrankLFRS | N/A (add-on) | Yes | 96029 |
