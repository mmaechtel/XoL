---
description: "The X-Plane WINCTRL plugin connects WINCTRL cockpit panels to X-Plane on Linux and macOS via USB HID — replacing the Windows-only SimAppPro with full LCD, LED, and button support."
---
# X-Plane WINCTRL Plugin

The X-Plane WINCTRL plugin is a native [plugin](../../glossary.md#plugin) that connects WINCTRL cockpit panels (MCDU, FCU, EFIS) directly to X-Plane via USB HID — without the Windows-only SimAppPro software. For Linux and macOS users, it is the only way to fully utilize WINCTRL hardware.

## Background

- **Developer:** Ramon (rswilem), community contributions
- **Repository:** [github.com/rswilem/winctrl-xplane-plugin](https://github.com/rswilem/winctrl-xplane-plugin) (GPL-3.0)
- **Download:** [X-Plane.org](https://forums.x-plane.org/files/file/95987-winctrl-plugin-for-x-plane-mac-linux-windows/)
- **Platforms:** Linux, macOS, Windows
- **Compatibility:** X-Plane 11 and 12

!!! note "Hardware and plugin share a name"

    WINCTRL is both the hardware vendor and the name of this plugin. On this page, **WINCTRL** on its own refers to the hardware; the software is called the **X-Plane WINCTRL plugin**, or simply the plugin.

The plugin communicates directly with the hardware via USB HID: it reads button presses, knob rotations, and switch states while driving LCD screens, LED backlighting, and annunciator lights in return. Axes (throttle levers, joystick) are deliberately left to X-Plane's built-in joystick configuration — calibration, dead zones, and response curves are handled better there. The same precedence applies to buttons: anything assigned under **Settings → Joystick** wins, and the plugin then withholds its own command for that button. Development is very active with frequent releases.

## Features

- **Automatic device detection:** No manual configuration needed
- **LCD/display driving:** MCDU screens, PDC displays, FCU number displays
- **LED/annunciator control:** Button illumination, backlighting, warning lights in sync with aircraft state
- **Multi-aircraft profiles:** Different dataref mappings per aircraft type
- **Self-test emulation:** MCDU/FMC power-up self-test on ToLiss aircraft
- **Custom FMC fonts:** Own display fonts as `.xpwwf` files
- **SkunkCrafts Updater:** Automatic updates after initial installation

**Supported hardware:** MCDU-32, PFP 3N/4/7, FCU (optionally with EFIS L/R), 32 ECAM, 32 AGP, 32 TCAS, 32 RMP, 32 NWS, 3N PAP MCP, 3N/3M PDC, URSA MINOR Airline and Fighter joysticks, URSA MINOR 32 Throttle (optionally with 32 PAC), ORION Joystick Base II and Throttle Base II

**Supported aircraft:** ToLiss A3XX family, Laminar A330/737, Zibo/LevelUp 737, FlightFactor 767/777/A350, JustFlight BAe 146, and others

### Custom FMC Fonts

The FMC display font can be replaced. Fonts are built in the upstream font editor, downloaded as an `.xpwwf` file and placed in:

```
X-Plane 12/Resources/plugins/winctrl/fonts/
```

Selection happens in the simulator under **Plugins → WINCTRL → FMC → Display font**. Since the August 2026 release the bundled fonts live in that same directory rather than inside the binary, which shortens load times.

## Value in Flight Simulation

Without the plugin, WINCTRL hardware on Linux offers only basic joystick functionality — the actual cockpit panel features (displays, LEDs, button feedback) remain unused, since SimAppPro is not available for Linux. The plugin replaces the part of SimAppPro that matters in flight: the runtime link that drives displays and lights from the simulator. Firmware updates, calibration, and the hardware self-test still require SimAppPro on a Windows machine.

## Installation

**Download:** [GitHub Releases](https://github.com/rswilem/winctrl-xplane-plugin/releases)

Copy the `winctrl` folder to `Resources/plugins/`. The plugin auto-detects connected hardware.

### Linux Notes: udev Rules

Raw HID nodes carry no default ACL, so a udev rule is what gets the panels within reach of the plugin — [Controllers](../../xplane/setup_diagnose/config.md#controllers) explains why standard joysticks need no such rule and these panels do.

Debian recommends the udev `uaccess` tag, which grants an ACL to whoever is logged in at the seat rather than opening the device to everyone. Create `/etc/udev/rules.d/70-winctrl.rules`:

```
# WINCTRL HID devices (USB vendor ID 0x4098)
SUBSYSTEM=="hidraw", ATTRS{idVendor}=="4098", TAG+="uaccess"
```

udev matches `idVendor` against the sysfs value, which the kernel writes as a hexadecimal string — `4098` in the rule therefore means USB vendor ID **0x4098**, the value the plugin hardcodes as `WINCTRL_VENDOR_ID`. Do not convert it to decimal.

!!! warning "The file name decides whether `uaccess` works"

    The tag is only acted upon by `73-seat-late.rules`. A rule file named `99-winctrl.rules` sorts *after* that and the tag silently does nothing — the file must sort before 73, hence `70-winctrl.rules`.

The README instead uses `MODE="0666"`, which opens the device to every local user, with device-specific rules in this form:

```
KERNEL=="hidraw*", ATTRS{idProduct}=="...", ATTRS{idVendor}=="4098", MODE="0666", SYMLINK+="..."
```

That form works regardless of file name and is the right choice when the symlinks are needed. `GROUP="plugdev", MODE="0660"` is the older middle ground, limiting access to members of that group.

Reloading the rules does not touch devices that are already attached — either replug the panel, or re-emit the events for what is currently connected:

```bash
sudo udevadm control --reload-rules && sudo udevadm trigger
```

The complete rule set with device-specific product IDs and symlinks is documented in the [repository README](https://github.com/rswilem/winctrl-xplane-plugin#linux-udev-rules) — use it as the authoritative source.

## Sources

- [WINCTRL — GitHub](https://github.com/rswilem/winctrl-xplane-plugin)
- [WINCTRL — X-Plane.org](https://forums.x-plane.org/files/file/95987-winctrl-plugin-for-x-plane-mac-linux-windows/)
