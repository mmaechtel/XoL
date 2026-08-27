---
title: "X-Plane Scripting: FlyWithLua, XPPython3"
description: "FlyWithLua and XPPython3: the two scripting frameworks for X-Plane 12 on Linux. Lua for lightweight scripts, Python 3 for complex plugins."
---
# Scripting

FlyWithLua and XPPython3 are the two scripting frameworks for X-Plane, and both run natively on Linux. FlyWithLua uses Lua for fast, lightweight scripts with direct DataRef access, Dear ImGui windows, and FMOD audio — the foundation for most community scripts, including the [FlyWithLua Scripts](../flylua_scripts/index.md) collected in this documentation. XPPython3 wraps the complete X-Plane SDK in Python 3, bundles its own interpreter, ships pip for third-party packages, and is the better fit for complex plugins that lean on Python libraries.

Start with [FlyWithLua](flywithlua.md) — it covers installation, the missing libglut symlink on Debian Bookworm, and the FMOD error message with certain aircraft that looks alarming but leaves the plugin running. [XPPython3](xppython3.md) follows with the Debian dependency setup and the plugins that depend on it, such as Follow the Greens. Both frameworks coexist in one X-Plane installation.

- **[FlyWithLua](flywithlua.md)** — Lua-based scripting framework
- **[XPPython3](xppython3.md)** — Python 3 plugin framework
