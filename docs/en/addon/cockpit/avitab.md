---
title: "AviTab on Linux: Setup, Charts, Tile Servers"
description: "AviTab for X-Plane on Linux — open-source cockpit tablet with PDF viewer, moving map, Navigraph charts, and custom tile server support."
---
# AviTab

AviTab is an open-source [plugin](../../glossary.md#plugin) for [X-Plane](../../glossary.md#x-plane) 12 that displays a tablet in the cockpit — featuring a PDF viewer, moving map, and chart integration. It was primarily designed for VR but works equally well in 2D mode.

## Background

- **Developer:** Folke Will (fpw), contributors dave6502, mjh65
- **Repository:** [github.com/TeamAvitab/avitab](https://github.com/TeamAvitab/avitab) (open source, AGPL-3.0; maintained fork of the archived fpw/avitab)
- **Platforms:** Windows, macOS, Linux (native binaries)
- **Compatibility:** X-Plane 11.20+ and X-Plane 12

The original [fpw/avitab](https://github.com/fpw/avitab) repository is archived (read-only, issue tracker disabled) after Folke Will stepped back from maintenance. Development continues under [TeamAvitab/avitab](https://github.com/TeamAvitab/avitab), which took over the project and publishes releases regularly.

## Features

- **PDF viewer:** Displays PDF charts and checklists from the `charts/` subdirectory
- **Moving map:** Online maps (OpenTopoMap, OpenStreetMap) and offline maps with configurable tile servers
- **Navigraph integration:** IFR/VFR charts in the cockpit (requires Navigraph subscription, not available in self-compiled builds)
- **ChartFox integration:** Free charts via Vatsim login
- **Airport app:** Airport information, runway data, local charts
- **Route overlay:** FMS files as overlay on the moving map
- **Aircraft integration:** Some aircraft (e.g., Zibo 737) have a 3D tablet model with AviTab integration; panel integration for X-Plane 12 requires the aircraft to opt into the current integration mode
- **Standalone mode:** Can also run as a standalone application outside of X-Plane

### AviTab Browser (Companion Plugin)

The [AviTab Browser](https://github.com/rswilem/avitab-browser) plugin by rswilem adds a full web browser to AviTab. It uses the Chromium Embedded Framework built into X-Plane 12.

- **License:** GPL-3.0
- **Features:** Configurable homepage, hotkey websites, SimBrief flight plan download
- **Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/93812-avitab-browser-a-web-browser-addon-for-the-avitab-plugin/)

!!! tip "Little Navmap as a moving map in the AviTab Browser"
    [Little Navmap](../tools/littlexpconnect.md) has a built-in web server (`Tools > Run Web Server`, default port 8965). Its map page shows the aircraft position delivered by Little XpConnect and can keep the aircraft centered (`Center on aircraft` plus auto refresh) — a moving map with the full Little Navmap map, including the flight plan, without any extra tile server. Point the AviTab Browser at that page and it appears on the cockpit tablet.

    Configuration in `Resources/plugins/avitab-browser/config.ini` (the file is created with defaults on first start); a working Linux example:

    ```ini
    [browser]
    homepage=http://localhost:8965
    hide_addressbar=yes

    [statusbar]
    icon_1=navigation
    url_1=http://localhost:8965
    ```

    `homepage` opens the map directly, the `statusbar` bookmark brings it back with one tap after browsing elsewhere. If Little Navmap runs on a different machine, replace `localhost` with that machine's address — the web server is reachable from any device in the local network.

## Value in Flight Simulation

AviTab solves the problem of needing to look up charts, checklists, or manuals during flight — especially in VR, where you would otherwise need to remove the headset to read external screens. Via custom maps, you can integrate your own tile servers (e.g., a local TileServer-GL). Aircraft integration provides a tablet built directly into the 3D cockpit for supported aircraft.

## Installation

**Download:** [github.com/TeamAvitab/avitab/releases](https://github.com/TeamAvitab/avitab/releases/latest) or [forums.x-plane.org](https://forums.x-plane.org/files/file/44825-avitab-vr-compatible-tablet-with-pdf-viewer-moving-maps-and-more/)

Extract the ZIP file and copy the `Avitab/` folder it contains into `Resources/plugins/`. The Linux binary is at `Avitab/lin_x64/Avitab.xpl`.

All dependencies are statically linked — no additional system packages are required.

**Placing PDF charts:**

```bash
cp my_charts/*.pdf /path/to/X-Plane\ 12/Resources/plugins/Avitab/charts/
```

Subdirectories are supported and displayed as a folder structure in the plugin.

### Configuring Custom Maps

Custom map sources are defined in the `online-maps/mapconfig.json` file in the plugin directory:

```json
[
    {
        "name": "OpenTopoMap",
        "servers": ["a.tile.opentopomap.org", "b.tile.opentopomap.org"],
        "protocol": "https",
        "url": "{z}/{x}/{y}.png",
        "min_zoom_level": 1,
        "max_zoom_level": 17,
        "tile_width_px": 256,
        "tile_height_px": 256,
        "enabled": true
    }
]
```

## Sources

- [AviTab — GitHub (TeamAvitab fork)](https://github.com/TeamAvitab/avitab)
- [AviTab — Release Notes](https://github.com/TeamAvitab/avitab/releases)
- [AviTab Browser — GitHub](https://github.com/rswilem/avitab-browser)
- [AviTab — forums.x-plane.org](https://forums.x-plane.org/files/file/44825-avitab-vr-compatible-tablet-with-pdf-viewer-moving-maps-and-more/)
