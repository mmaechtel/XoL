---
description: "XPAIS Marine Traffic renders live AIS ship traffic in X-Plane 12 from the AISStream feed — a native Linux plugin, open source but archived since July 2026."
---
# XPAIS Marine Traffic

XPAIS Marine Traffic puts real ships on the water. The plugin subscribes to the [AISStream](https://aisstream.io/) feed, receives the position reports that vessels broadcast via AIS (Automatic Identification System), and renders them in [X-Plane](../../glossary.md#x-plane) 12 at their actual positions — where [LiveTraffic](livetraffic.md) does this for aircraft, XPAIS does it for maritime traffic.

## Background

- **Developer:** CheckCanopy (xbard)
- **Repository:** [codeberg.org/xbard/XPAIS-Marine-Traffic](https://codeberg.org/xbard/XPAIS-Marine-Traffic) (open source, GPL-3.0)
- **Platform:** Linux (built from source)
- **Compatibility:** X-Plane 12
- **Requirement:** free AISStream API key

!!! warning "Archived — no further development"

    The repository was set to read-only on 2026-07-07; the last commit dates from 2026-06-16. The code remains available and buildable, but there will be no fixes or new features. Anyone using it is on their own.

    Not to be confused with the similarly named **XP AIS-Traffic** by nestasko on the X-Plane.org forums: a separate project that names X-Plane 12 and Windows 64-bit as its supported platform. Its author calls Linux and macOS support "definitely on the roadmap" with no ETA — as of August 2026 no Linux build exists.

## How It Works

Two threads with a clean split of responsibilities: `ais_client` owns the WebSocket connection over TLS and never touches the X-Plane API, while everything sim-facing runs on the flight-loop thread. That is the correct design for a plugin — X-Plane's SDK is not thread-safe, and network jitter never reaches the frame loop.

Vessels are rendered **60 seconds behind real time**. That sounds like a flaw and is in fact the more honest approach: in steady state the plugin interpolates between two known AIS fixes instead of extrapolating a guessed position forward. It only extrapolates briefly, and capped, at the leading edge — right after a vessel appears or when its feed stalls. Ships move smoothly and never have to jump when the next report contradicts a prediction.

The hulls come from X-Plane's own default ship objects, selected by AIS type code and by the vessel's reported length and beam. [OpenSceneryX](https://www.opensceneryx.com/) is optional but worth having: X-Plane 12 ships no passenger vessel models, so without it liners and ferries fall back to a generic cargo hull, and small passenger craft to a yacht model.

## Installation

The plugin is built from source. Required are `cmake`, a C++17 compiler and the OpenSSL development libraries — on Debian:

```bash
sudo apt install cmake g++ libssl-dev
```

The X-Plane SDK is vendored in the repository, so it needs no separate download — but the build fetches IXWebSocket and nlohmann/json at configure time, so it does need network access:

```bash
./build.sh            # builds into dist/XPAISTraffic/
./build.sh install    # copies into the X-Plane installation
```

The target is `X-Plane 12/Resources/plugins/XPAISTraffic/`. An AISStream API key is mandatory — registration is free — and goes into `config.ini`:

```ini
[AIS]
ApiKey=<your key>

[Logging]
Debug=true

[Display]
ShowTraffic=true
Labels=false
Wakes=false
HideNoHeading=false
OpenSceneryX=true
```

Without a valid key no vessels appear. The plugin logs to `logs/xpaistraffic.log`, which is the first place to look when the contact count stays at zero.

## Operation

The **Plugins → XP AIS Traffic** menu exposes the live settings, including the current contact count. Around busy ports that number gets large — testers reported roughly 3,000 contacts near EHAM.

| Menu item | Effect |
|-----------|--------|
| Show traffic | Master switch |
| Show labels | Vessel name, heading and speed above the ship |
| Show wakes | Unfinished, off by default |
| Hide vessels w/o heading (HDG 000) | Suppresses vessels that report no heading |
| Use OpenSceneryX ships (if installed) | Prefer the better hulls when available |
| Contacts: N | Live count of tracked vessels — `Contacts: (off)` while traffic is switched off |

The HDG-000 filter addresses a quirk of the data: anchored and stationary vessels frequently transmit neither true heading nor course over ground, so they all end up pointing due north. The filter is off by default, and the developer names its limitation plainly — AIS offers no way to distinguish "reported no heading" from "genuinely steaming north", so a real northbound ship is hidden along with the rest.

Wakes exist but default to off, as they were never finished. They reference X-Plane's own `wake.png` rather than copying it.

!!! note "Turn off \"Draw boats and balloons\""

    X-Plane's own ship traffic is positionally closed. The only writable position datarefs are `sim/world/boat/*` under `override_boats`, and those cover just the carrier and the frigate — the ambient boats cannot be placed from outside, which is also why AIS vessels cannot inherit their procedural wake.

    Leaving X-Plane's own traffic on is actively harmful: its synthetic boats have nothing to do with real traffic and duplicate as ghosts right next to the AIS vessels. The plugin's ships are instanced independently and render regardless of the setting.

    The repository README says the opposite — keep the setting on. The developer corrected this in the forum thread afterwards; the correction is the newer statement.

## Limitations

Two things the project lists as deliberate design choices rather than shortcomings, because they do not apply to a renderer driven by live AIS:

- **No collision avoidance:** vessels render exactly where AIS places them, including in each other
- **No berth or port scripting:** everything comes from the live feed, nothing is choreographed

The gaps the project does name as gaps are different: passenger vessels need OpenSceneryX to look right, the car-carrier hulls are a deliberate mix, and the visuals were never tuned in the simulator.

Two further limits come from the data rather than the plugin:

- **Coverage varies:** AIS quality depends on transponders, shore stations and satellite reception. Parts of the world are simply empty — testers found no data at all in the Strait of Hormuz
- **Data quality:** spoofed or duplicated AIS entries occur and cannot be corrected by the plugin

## Sources

- [XPAIS-Marine-Traffic](https://codeberg.org/xbard/XPAIS-Marine-Traffic) — repository, README and build instructions (archived)
- [XPAIS Marine Traffic — Linux build](https://forums.x-plane.org/forums/topic/348448-xpais-marine-traffic-linux-build/) — development thread with the developer's explanations
- [AISStream](https://aisstream.io/) — AIS data source, API key registration
