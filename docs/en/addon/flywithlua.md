# FlyWithLua

FlyWithLua NG+ is a Lua scripting engine for [X-Plane](../glossary.md#x-plane) 12 that serves as the foundation for numerous community plugins and custom automations.

## Background

- **Developer:** X-Friese (Florian Schmid), maintainers sparker256 / smoothchat
- **Repository:** [github.com/X-Friese/FlyWithLua](https://github.com/X-Friese/FlyWithLua) (open source, MIT license)
- **Platforms:** Windows, macOS, Linux (native binaries)
- **Compatibility:** X-Plane 12 (NG+ Edition), X-Plane 11 (older NG Edition)
- **Price:** Free

The [plugin](../glossary.md#plugin) has been in development since X-Plane 9 and is one of the most widely used X-Plane plugins. Many other plugins such as 3jFPS or AutoATC require FlyWithLua as a dependency.

## Features

- **Lua scripting via LuaJIT:** Read and write datarefs, create custom commands, build menus
- **ImGui integration:** Native Dear ImGui windows for custom user interfaces
- **[FMOD](../glossary.md#fmod) audio:** Access to the X-Plane FMOD sound system (COM1, interior, UI, master buses)
- **HID device access:** Direct USB HID communication for custom controllers
- **Script quarantine:** Faulty scripts are automatically moved to the `Scripts (Quarantine)/` folder and can be reloaded via the Plugins menu after fixing
- **Scripts (disabled):** Scripts in this folder are skipped at startup without needing to delete them

## Value in Flight Simulation

FlyWithLua enables automation of recurring cockpit tasks — from simple checklist helpers to complex custom UIs with ImGui. Via HID access, you can also interface with unusual controllers that X-Plane does not natively support. Since many community plugins require FlyWithLua as a dependency, it belongs to the basic equipment of any X-Plane installation.

## Installation

**Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/82888-flywithlua-ng-next-generation-plus-edition-for-x-plane-12-win-lin-mac/) (free X-Plane.Org account required)

Extract the ZIP file to `Resources/plugins/`. This creates the following directory structure:

```
Resources/plugins/FlyWithLua/
    lin_x64/FlyWithLua.xpl
    Scripts/
    Scripts (disabled)/
    Scripts (Quarantine)/
    Internals/
    Modules/
```

**Dependencies on Debian/Ubuntu:**

```bash
sudo apt install libglut3.12 libopenal1
```

### Missing libglut Symlink on Debian Bookworm

On Debian Bookworm (Stable), the `libglut3.12` package does not include a `libglut.so.3` symlink. FlyWithLua links against `libglut.so.3` and silently fails to load without it — no error message appears in `Log.txt`.

**Workaround:**

```bash
sudo ln -s /usr/lib/x86_64-linux-gnu/libglut.so.3.12 /usr/lib/x86_64-linux-gnu/libglut.so.3
```

On Debian Trixie (Testing) and Ubuntu 24.04+, the symlink is already included in the package.

### FMOD Error with Certain Aircraft

When loading aircraft with FMOD sound packages (e.g., ToLiss A321), the following error may appear in `Log.txt`:

```
FlyWithLua Error: Error in ../Fmod/FmodIntegration.cpp, line 732: An invalid parameter was passed to this function.
```

The error is non-fatal — the plugin continues to function. A fix is pending.

## Sources

- [FlyWithLua — GitHub](https://github.com/X-Friese/FlyWithLua)
- [FlyWithLua NG+ for X-Plane 12 — forums.x-plane.org](https://forums.x-plane.org/files/file/82888-flywithlua-ng-next-generation-plus-edition-for-x-plane-12-win-lin-mac/)
- [Issue #111 — libglut.so.3 symlink missing on Debian](https://github.com/X-Friese/FlyWithLua/issues/111)
- [Issue #126 — FMOD error on Linux](https://github.com/X-Friese/FlyWithLua/issues/126)
