# XTextureExtractor

XTextureExtractor extracts cockpit instrument textures from [X-Plane](../glossary.md#x-plane) and streams them over the network to external displays — tablets, monitors, or Raspberry Pis.

## Background

- **Developer:** Wayne Piekarski
- **Repository:** [github.com/waynepiekarski/XTextureExtractor](https://github.com/waynepiekarski/XTextureExtractor) (open source, GPL-3.0)
- **Platforms:** Windows, macOS, Linux (native binaries)
- **Compatibility:** X-Plane 11 and X-Plane 12 ([Vulkan](../glossary.md#vulkan-api) and OpenGL)
- **Price:** Free

The [plugin](../glossary.md#plugin) is maintained and supports over 35 preconfigured aircraft, including Zibo 737, ToLiss A320/A321, Flight Factor 757/767/777, and many Laminar default aircraft.

## Features

- **Texture extraction:** Automatically detects the panel texture of the current aircraft and extracts individual instruments (HSI, ND, EICAS, CDU, etc.)
- **Local windows:** Display instruments in separate X-Plane windows, move to external monitors, save positions
- **Network streaming:** Streams PNG-encoded instrument frames over TCP to connected clients
- **Aircraft definitions:** Simple `.tex` text files define instrument regions — custom aircraft can be added easily
- **Android app:** [Google Play](https://play.google.com/store/apps/details?id=net.waynepiekarski.xtextureextractor) — displays 2 panels simultaneously, automatic X-Plane discovery
- **Java desktop client:** Cross-platform (Windows, Linux, macOS, Raspberry Pi), included in the download

### Limitations

- The cockpit must be rendered (internal view required)
- The default Laminar G1000 (C172, etc.) uses a non-standard texture mechanism and cannot be captured

## Value in Flight Simulation

XTextureExtractor enables multi-monitor setups without special hardware. Cockpit instruments can be offloaded to a tablet next to the main screen — particularly useful for navigation displays, EICAS, or CDUs that are hard to read in the full-screen cockpit. Via network streaming, remote devices can also serve as instrument displays.

## Installation

**Download:** [GitHub](https://github.com/waynepiekarski/XTextureExtractor) — download the ZIP file from the `Uploads/` directory.

Extract the `Plugin-XTextureExtractor-x64-Release` folder to `Resources/plugins/`. The Linux binary is at `64/lin.xpl`.

No additional system packages are required. There are no known Linux-specific issues.

### Network Streaming

The plugin server listens on TCP port **52500**. To receive data on external devices, this port must be opened in the firewall. Automatic discovery by the Android app uses the X-Plane beacon on UDP multicast **239.255.1.1:49707**.

## Sources

- [XTextureExtractor — GitHub](https://github.com/waynepiekarski/XTextureExtractor)
- [XTextureExtractor — Google Play](https://play.google.com/store/apps/details?id=net.waynepiekarski.xtextureextractor)
