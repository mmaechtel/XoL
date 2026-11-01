---
description: "XP CabinState for X-Plane 12 — cabin, crew and passenger simulation with SimLoad Manager integration; tested on Linux via Wine in headless mode."
---
# XP CabinState

XP CabinState simulates cabin, crew, and passengers alongside [X-Plane](../../glossary.md#x-plane) 12: boarding, safety demonstration, trolley service, and announcements matched to the phase of flight, altitude, and cabin signs. It is a standalone Windows program that reads X-Plane through the built-in Web API and is operated through a browser WebUI. Linux is not officially supported, but the program runs headless under [Wine](../../glossary.md#wine-wine-is-not-an-emulator).

## Background

- **Developer:** Vito Jackson (Isar Simworks, Munich)
- **Website:** [isarsimworks.de](https://isarsimworks.de/en/shop.php?p=xp-cabinstate)
- **License:** Free edition at no cost, Pro edition paid (licence key, checked offline)
- **Platforms:** Officially Windows 10/11 only — macOS and Linux are not supported
- **Compatibility:** X-Plane 12.1.1 or newer (built-in Web API, enabled by default)
- **Aircraft:** 12 cabins — ToLiss A319 to A340-600, Zibo/LevelUp 737-600 to 900ER, DeltaWing ATR 72-600
- **Companion plugin:** XP CabinState Link (figures, cabin signs, and cabin sound inside X-Plane) — Windows build only

## Features

- **Complete flight flow:** Boarding, safety demonstration, trolley service, landing, deboarding, and cleaning; the crew answers call buttons
- **Announcements:** Crew announcements in German and English, gate announcements with terminal sound, boarding music and chime
- **In-flight screen:** Safety video and cabin map with route and position
- **3D cabin:** Cabin view with crew and seat occupancy in the WebUI
- **Flight setup:** From SimBrief or driven by SimLoad Manager
- **Tablet and second PC:** The WebUI runs in any browser on the same network

**Free vs. Pro**

| Feature | Free | Pro |
|---|---|---|
| Flight flow in all 12 cabins, announcements, IFE screen | Yes | Yes |
| Tablets and second devices at once | 1 | Unlimited |
| Logbook | Last 5 flights | Complete, with flight report |
| Airline mode (fleet, bank, staff, contracts, billing) | — | Yes |
| Own media and seat maps | — | Yes |

## Value in Flight Simulation

In most simulator setups the cabin behind the cockpit door stays empty and silent. XP CabinState fills that gap with a crew that reacts to what happens in the cockpit — the captain's welcome follows pushback, service is interrupted in stronger turbulence, and announcements follow the flight phase. Together with a loading tool, the turnaround at the gate and the life in the cabin form one continuous sequence.

## SimLoad Manager Integration

Under **Settings → Flight flow**, [SimLoad Manager](../traffic/simloadmanager.md) can be selected as the loading source. SimLoad Manager then drives boarding, crew, catering, and deboarding; the matching CabinState options are hidden. The passenger count is taken from SimLoad Manager when the flight is created and updated until boarding starts. The option is only selectable while SimLoad Manager is running in X-Plane.

## Linux Setup (Wine)

!!! warning "Workaround, not official support"

    The developer supports Windows only. The following setup was tested at the time of testing with the ToLiss A320: flight flow, announcements, and the WebUI 3D cabin view work. Program versions and command-line options may change.

Extract the complete `XP CabinState` folder and keep `XPCabinState.exe`, `xpcabinstate.dat`, and the bundled runtime files together; move only the whole folder, never single files. Run the commands below from inside that folder. A dedicated Wine prefix is sufficient; Mono and Gecko are not needed and can be skipped when creating it:

```bash
WINEPREFIX="$HOME/.wine-xpcabinstate" WINEDLLOVERRIDES="mscoree,mshtml=" wineboot -i
WINEPREFIX="$HOME/.wine-xpcabinstate" wine XPCabinState.exe --headless --run-seconds=86400
```

- **`--headless`** is required — the program window needs WebView2/.NET, which is not available under Wine
- **`--run-seconds`** is required — without it the program crashes with `OverflowError: timestamp out of range`; the value is the runtime in seconds and can be generous (86400 is 24 hours)
- **WebUI:** Port 8130 on all interfaces by default; if it is taken, the program uses the next free port (the address is in the log `Documents/XP-CabinState/XP CabinState.log` inside the Wine prefix). Open `http://127.0.0.1:8130/?k=<key>` once with the access key from `Documents/XP-CabinState/Spielstand/ui_key.txt`, adjusting the port if necessary — the browser remembers access via cookie
- **Sound:** Comes from the browser (toggle in the WebUI); enable it in one browser only, otherwise announcements play twice
- **IFE screen:** Available at `/?ife=1`, for example in the [AviTab](avitab.md) browser

Since XP CabinState Link has no Linux build, the figures in the X-Plane cabin, sound inside the sim, the X-Plane menu, and the cabin camera are missing. Everything else runs in the WebUI.

## Sources

- [XP CabinState — Isar Simworks Shop](https://isarsimworks.de/en/shop.php?p=xp-cabinstate)
- [Isar Simworks — Installation](https://isarsimworks.de/en/installation.php)
