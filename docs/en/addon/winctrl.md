# WINCTRL

WINCTRL is a native [plugin](../glossary.md#plugin) that connects Winwing cockpit panels (MCDU, FCU, EFIS, pedals) directly to X-Plane via USB HID — without the Windows-only SimAppPro software. For Linux and macOS users, it is the only way to fully utilize Winwing hardware.

## Background

- **Developer:** Ramon (rswilem), community contributions
- **Repository:** [github.com/rswilem/winctrl-xplane-plugin](https://github.com/rswilem/winctrl-xplane-plugin) (GPL-3.0)
- **Download:** [X-Plane.org](https://forums.x-plane.org/files/file/95987-winctrl-plugin-for-x-plane-mac-linux-windows/)
- **Platforms:** Linux, macOS, Windows
- **Compatibility:** X-Plane 12
- **Price:** Free (open source)

The plugin communicates directly with the hardware via USB HID: it reads button presses, knob rotations, and switch states while driving LCD screens, LED backlighting, and annunciator lights in return. Axes (throttle levers, joystick) are deliberately left to X-Plane's built-in joystick configuration. Development is very active (32 releases since July 2025).

## Features

- **Automatic device detection:** No manual configuration needed
- **LCD/display driving:** MCDU screens, PDC displays, FCU number displays
- **LED/annunciator control:** Button illumination, backlighting, warning lights in sync with aircraft state
- **Multi-aircraft profiles:** Different dataref mappings per aircraft type
- **Self-test emulation:** MCDU/FMC power-up self-test on ToLiss aircraft
- **SkunkCrafts Updater:** Automatic updates after initial installation

**Supported hardware:** MCDU-32, PFP 3N/4/7, FCU, EFIS, ECAM32, PAP3, AGP, URSA MINOR Joystick/Throttle, 3N/3M PDC

**Supported aircraft:** ToLiss A3XX family, Laminar A330/737, Zibo/LevelUp 737, FlightFactor 767/777/A350, iniSimulations A300/A310, JustFlight BAe 146, and others

## Value in Flight Simulation

Without WINCTRL, Winwing hardware on Linux offers only basic joystick functionality — the actual cockpit panel features (displays, LEDs, button feedback) remain unused, since SimAppPro is not available for Linux. WINCTRL unlocks the full hardware capabilities on all platforms.

## Installation

**Download:** [GitHub Releases](https://github.com/rswilem/winctrl-xplane-plugin/releases)

Copy the `winctrl` folder to `Resources/plugins/`. The plugin auto-detects connected hardware.

### Linux Notes: udev Rules

udev rules are required for non-root HID access. Create `/etc/udev/rules.d/99-winctrl.rules`:

```bash
# Winwing/WINCTRL HID devices
SUBSYSTEM=="hidraw", ATTRS{idVendor}=="1002", MODE="0666"
```

Then reload udev rules:

```bash
sudo udevadm control --reload-rules && sudo udevadm trigger
```

The complete rule file with device-specific symlinks is documented in the [repository README](https://github.com/rswilem/winctrl-xplane-plugin#linux).

## Sources

- [WINCTRL — GitHub](https://github.com/rswilem/winctrl-xplane-plugin)
- [WINCTRL — X-Plane.org](https://forums.x-plane.org/files/file/95987-winctrl-plugin-for-x-plane-mac-linux-windows/)
