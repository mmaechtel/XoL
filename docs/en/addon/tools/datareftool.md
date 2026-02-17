---
description: "DataRefTool (DRT) for X-Plane 12: browse, search, watch, and edit datarefs in real time. Essential for plugin development and debugging on Linux."
---
# DataRefTool

DataRefTool (DRT) is a development and debugging tool for [X-Plane](../../glossary.md#x-plane) 12 that allows browsing, watching, and editing datarefs as well as triggering commands.

## Background

- **Developer:** Lee C. Baker
- **Website:** [datareftool.com](https://datareftool.com)
- **License:** v1 was open source (MIT, [GitHub](https://github.com/leecbaker/datareftool)); v2 is closed source
- **Platforms:** Windows, macOS, Linux (native binaries)
- **Compatibility:** X-Plane 12.1+ (v2); X-Plane 10/11 (v1)

The [plugin](../../glossary.md#plugin) has existed since X-Plane 10. Version 2 was released as a closed-source rewrite for X-Plane 12 and uses the dataref enumeration API (XPLM400) introduced in X-Plane 12.04.

## Features

- **Dataref browser:** Read, write, and search all datarefs (including arrays)
- **Command browser:** Search for and execute commands directly
- **Change detection:** Highlight datarefs that have changed recently
- **Watch window:** Monitor specific dataref values in a separate panel
- **Regex search:** Multiple search terms, regular expressions, optional case sensitivity
- **Plugin/scenery reload:** Trigger reloads directly from DRT
- **Multi-window:** Multiple DRT windows can be open simultaneously
- **Ignore list:** `drt_ignore.txt` in the `Resources/plugins/` directory to exclude problematic datarefs

## Value in Flight Simulation

DRT is the standard tool for plugin development and troubleshooting in X-Plane. It enables real-time observation of all datarefs, which is invaluable for analyzing plugin conflicts or developing custom FlyWithLua scripts. With windows open, DRT reads all datarefs every frame, which can reduce [FPS](../../glossary.md#fps-frames-per-second) — with windows closed, the performance impact is zero.

## Installation

**Download:** [datareftool.com/download](https://datareftool.com/download)

Extract the ZIP file to `Resources/plugins/`. Minimum system requirement on Linux: Ubuntu 20.04+ (or equivalent glibc version). No additional system packages are required. There are no known Linux-specific issues.

## Sources

- [DataRefTool — Website](https://datareftool.com)
- [DataRefTool v1 — GitHub (archived)](https://github.com/leecbaker/datareftool)
