---
description: "XPPython3 Python 3 plugin framework for X-Plane 12 on Linux: full SDK access, built-in pip, Dear ImGui UI, and Debian dependency setup."
---
# XPPython3

XPPython3 is a Python 3 scripting engine for [X-Plane](../../glossary.md#x-plane) 12 that wraps the complete X-Plane SDK into Python, enabling plugins written in Python to run alongside native C/C++ plugins.

## Background

- **Developer:** Peter Buckner (AvnWx.com), initial Python 3 port by Michal (uglyDwarf)
- **Documentation:** [xppython3.readthedocs.io](https://xppython3.readthedocs.io/en/latest/)
- **Repository:** [github.com/uglyDwarf/x-plane_plugins](https://github.com/uglyDwarf/x-plane_plugins) (GPL)
- **Platforms:** Windows, macOS, Linux (native binaries)
- **Compatibility:** X-Plane 12 (v4.x); X-Plane 11 (legacy v3.1.5)

XPPython3 is the successor to Sandy Barbour's PythonInterface (Python 2 only). The current v4.x line bundles Python 3.12 internally — no system Python installation is needed. A major C-to-C++ rewrite in v4.6 brought approximately 20% performance improvement.

## Features

- **Full SDK coverage:** All X-Plane SDK modules accessible from Python (datarefs, commands, display, menus, camera, navigation, scenery, sound, weather)
- **Dear ImGui integration:** Modern UI windows via the `xp_imgui` module
- **Built-in pip:** Install third-party Python packages (numpy, Pillow, requests) directly from X-Plane
- **Plugin types:** Global, aircraft-specific, and scenery-specific Python plugins
- **Hot reload:** Reload all Python plugins without restarting X-Plane
- **Built-in updater:** Checks for new XPPython3 versions from the Plugins menu
- **Compiled plugins:** Support for `.pyc` and encrypted `.xpyce` files for commercial distribution

## Value in Flight Simulation

XPPython3 opens the X-Plane SDK to the Python ecosystem — developers can use standard Python libraries, pip packages, and familiar debugging tools. Plugins like [Follow the Greens](../traffic/followthegreens.md) and XP-NOAA-Weather depend on it. The plugin ecosystem is smaller than [FlyWithLua](flywithlua.md)'s Lua-based one, but XPPython3 serves developers who prefer Python and projects that benefit from Python's library ecosystem.

## Installation

**Download:** [xppython3.readthedocs.io](https://xppython3.readthedocs.io/en/latest/usage/installation_plugin.html) — download `xp3-linux.zip` (stable) or `xp3-linuxb.zip` (beta).

Extract the ZIP file to `Resources/plugins/`. This creates the following directory structure:

```
Resources/plugins/XPPython3/
    lin_x64/
        XPPython3.xpl
        python3.12/
```

On first launch, the [plugin](../../glossary.md#plugin) auto-creates `Resources/plugins/PythonPlugins/` where third-party Python plugins are placed.

### Dependencies on Debian/Ubuntu

```bash
sudo apt install libexpat1 libbsd0
```

The `zlib1g` and `libc6` packages are part of every standard installation. On Arch Linux, `libbsd` must be installed separately (`pacman -S libbsd`).

### Plugin Not Loading

If XPPython3 does not appear in the Plugins menu and produces no output in `Log.txt`, a missing shared library is the most common cause. Diagnose with:

```bash
ldd Resources/plugins/XPPython3/lin_x64/XPPython3.xpl
```

Any line showing `not found` indicates a missing dependency.

## Sources

- [XPPython3 Documentation — xppython3.readthedocs.io](https://xppython3.readthedocs.io/en/latest/)
- [XPPython3 — GitHub](https://github.com/uglyDwarf/x-plane_plugins)
- [XPPython3 v4.6.1 Released — forums.x-plane.org](https://forums.x-plane.org/forums/topic/338833-xppython3-v461-released/)
