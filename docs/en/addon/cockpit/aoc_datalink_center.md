---
description: "AOC Datalink Center for X-Plane 12 — free native plugin for ToLiss: Hoppie ACARS, CPDLC, PDC, SimBrief OFP, OOOI and weather monitors in a browser WebUI."
---
# AOC Datalink Center

AOC Datalink Center brings airline operations-centre work into [X-Plane](../../glossary.md#x-plane) 12: weather packages as ACARS uplinks, free-text telex, CPDLC and PDC via the Hoppie network, automatic OOOI reports, and background monitors along the route. It is designed for the ToLiss Airbus and runs as a native [plugin](../../glossary.md#plugin) with a browser-based WebUI — also usable from a tablet in the home cockpit.

## Background

- **Developer:** Vito Jackson (Isar Simworks, Munich)
- **Website:** [isarsimworks.de](https://isarsimworks.de/en/)
- **License:** Free, private use only, no redistribution
- **Platforms:** Windows x64, Linux x64 (native plugin)
- **Compatibility:** X-Plane 12, ToLiss Airbus
- **Dependencies:** None (no XPPython3); on Linux the system libcurl and glibc 2.17 or newer
- **Accounts:** Hoppie logon code (free at hoppie.nl), SimBrief username

The developer also offers a standalone Windows desktop program under the same name. It is a separate package — this page covers the plugin.

## Features

- **Weather packages:** METAR, TAF, SIGMET/AIRMET, and D-ATIS as ACARS uplinks into the aircraft
- **SimBrief integration:** LOAD OFP fills in callsign, stations, flow routes, ATIS station, and planned gate; loadsheet, OFP summary, and PDC go out as uplinks
- **Telex and CPDLC:** Free-text messages with templates and automatic segmentation, CPDLC and PDC via Hoppie
- **OOOI reports:** Automatic OUT/OFF/ON/IN reports with gate detection, schedule, and delay
- **Monitors:** Weather changes at destination and alternate, SIGMET along the corridor, new ATIS letters, ECFMP flow measures
- **Route ATC monitor:** Derives the FIRs crossed by the SimBrief route and reports VATSIM or IVAO controllers coming online or going offline, sector-aware based on the aircraft position
- **Interfaces:** WebUI in two layouts (Classic and Cockpit Rail), EFB view for tablets, and an in-sim panel inside X-Plane
- **Self-test:** Checks every data source and names the cause of timeouts or DNS blocking

## Value in Flight Simulation

Datalink in the cockpit only comes alive with a counterpart on the ground. AOC Datalink Center acts as that dispatch office: weather, clearances, and loadsheets arrive in the cockpit as they would from a real airline OPS centre, while the monitors keep watch during cruise. On VATSIM, the route ATC monitor shows which sectors ahead are staffed.

## Installation

**Download:** [isarsimworks.de](https://isarsimworks.de/en/)

Copy the `plugins` folder from the package into `Resources/`. The result is `Resources/plugins/AOCDatalinkCenter/` with the platform folders `win_x64/` and `lin_x64/` and the file `AOCDatalinkCenter.dat`, which holds the WebUI and must stay next to the platform folders. X-Plane loads the matching build automatically.

On Linux, the plugin uses the system libcurl for HTTPS. If it is missing, install it via the package manager, for example on Debian/Ubuntu:

```bash
sudo apt install libcurl4
```

Afterwards, open the WebUI via **Plugins → AOC Datalink Center → Open WebUI** or at `http://localhost:8785/` (from a tablet, use the sim PC's IP address). On the SETUP tab, enter the Hoppie logon code and press Enter to save. On the SIMBRIEF tab, enter the SimBrief username or pilot ID, then click LOAD OFP. Settings and learned gates are stored in `Output/preferences/AOCDatalinkCenter/`.

!!! note "Port 8785 and older versions"

    The plugin, the older XPPython3 version, the desktop program, and the former FlyWithLua script all use port 8785 — run only one of them, or set a different port in SETUP. Before switching, remove the old XPPython3 copy (`PythonPlugins/PI_AOC_Datalink_Center.py` and the folder `PythonPlugins/AOCDatalinkCenter`) and the former FlyWithLua script. On first start the plugin copies the settings and learned gates to `Output/preferences/AOCDatalinkCenter/`; the originals stay in place. The WebUI has no password, so do not forward the port to the internet.

### Linux Notes

This setup has been successfully tested on Linux: the X-Plane log reports the libcurl network backend, the native initialisation, and the WebUI listening on port 8785.

## Sources

- [Isar Simworks — Official Website](https://isarsimworks.de/en/)
- [AOC Datalink Center — Manual (PDF)](https://isarsimworks.de/dl.php?f=AOC_Datalink_Center_Manual_EN.pdf)
- [Hoppie ACARS](https://www.hoppie.nl/acars/)
