# AviTab

AviTab is an open-source [plugin](../glossary.md#plugin) for [X-Plane](../glossary.md#x-plane) 12 that displays a tablet in the cockpit — featuring a PDF viewer, moving map, and chart integration. It was primarily designed for VR but works equally well in 2D mode.

## Background

- **Developer:** Folke Will (fpw), contributors dave6502, mjh65
- **Repository:** [github.com/fpw/avitab](https://github.com/fpw/avitab) (open source, AGPL-3.0)
- **Platforms:** Windows, macOS, Linux (native binaries)
- **Compatibility:** X-Plane 11.20+ and X-Plane 12
- **Price:** Free

Development activity is low — the last commit and the latest release (v0.7.1) date from September 2024. The repository is not archived, but there are no signs of upcoming updates.

## Features

- **PDF viewer:** Displays PDF charts and checklists from the `charts/` subdirectory
- **Moving map:** Online maps (OpenTopoMap, OpenStreetMap) and offline maps with configurable tile servers
- **Navigraph integration:** IFR/VFR charts in the cockpit (requires Navigraph subscription, not available in self-compiled builds)
- **ChartFox integration:** Free charts via Vatsim login
- **Airport app:** Airport information, runway data, local charts
- **Route overlay:** FMS files as overlay on the moving map
- **Aircraft integration:** Some aircraft (e.g., Zibo 737) have a 3D tablet model with AviTab integration
- **Standalone mode:** Can also run as a standalone application outside of X-Plane

### AviTab Browser (Companion Plugin)

The [AviTab Browser](https://github.com/rswilem/avitab-browser) plugin by rswilem adds a full web browser to AviTab. It uses the Chromium Embedded Framework built into X-Plane 12.

- **License:** GPL-3.0
- **Features:** Configurable homepage, hotkey websites, SimBrief flight plan download
- **Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/93812-avitab-browser-a-web-browser-addon-for-the-avitab-plugin/)

## Value in Flight Simulation

AviTab solves the problem of needing to look up charts, checklists, or manuals during flight — especially in VR, where you would otherwise need to remove the headset to read external screens. Via custom maps, you can integrate your own tile servers (e.g., a local TileServer-GL). Aircraft integration provides a tablet built directly into the 3D cockpit for supported aircraft.

## Installation

**Download:** [github.com/fpw/avitab/releases](https://github.com/fpw/avitab/releases/tag/v0.7.1) or [forums.x-plane.org](https://forums.x-plane.org/files/file/44825-avitab-vr-compatible-tablet-with-pdf-viewer-moving-maps-and-more/)

Extract the ZIP file to `Resources/plugins/`. This creates the `AviTab/` folder with the Linux binary at `lin_x64/AviTab.xpl`.

All dependencies are statically linked — no additional system packages are required.

**Placing PDF charts:**

```bash
cp my_charts/*.pdf /path/to/X-Plane\ 12/Resources/plugins/AviTab/charts/
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

### PDF Crash on Linux

!!! warning "PDF viewer unusable on certain distributions"

    AviTab crashes when opening PDF files on Linux systems with newer `lcms2` library versions (SIGSEGV in `cmsSignalError`). The statically linked MuPDF library conflicts with the system-wide `lcms2` version.

    **Affected distributions (confirmed):**

    - Arch Linux / EndeavourOS
    - Ubuntu 24.04 / Kubuntu 24.10

    **Debian Bookworm** (lcms2 2.14) is likely unaffected. Debian Trixie (lcms2 2.16) needs testing.

    **Workaround:** A community member fixed the crash by recompiling AviTab with a newer MuPDF version (1.26.11). This requires self-compilation — an official update is pending. Moving map and other apps work normally regardless.

## Sources

- [AviTab — GitHub](https://github.com/fpw/avitab)
- [AviTab v0.7.1 — Release Notes](https://github.com/fpw/avitab/releases/tag/v0.7.1)
- [AviTab Browser — GitHub](https://github.com/rswilem/avitab-browser)
- [Issue #232 — PDF crash on Linux](https://github.com/fpw/avitab/issues/232)
- [AviTab — forums.x-plane.org](https://forums.x-plane.org/files/file/44825-avitab-vr-compatible-tablet-with-pdf-viewer-moving-maps-and-more/)
