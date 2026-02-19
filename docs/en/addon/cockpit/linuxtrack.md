---
description: "LinuxTrack head tracking for X-Plane on Linux — 6DOF tracking with TrackIR, webcam, or Wiimote. Installation and X-IR fork guide."
---
# LinuxTrack

LinuxTrack is a head-tracking software suite for Linux and macOS that translates head movements into X-Plane camera movements via the xlinuxtrack [plugin](../../glossary.md#plugin). It supports TrackIR, webcams, and Wiimotes as input devices and provides 6DOF tracking (6 degrees of freedom).

## Background

- **Developer:** uglyDwarf (Michal), active fork: fwfa123 (LinuxTrack X-IR)
- **Repository:** [github.com/uglyDwarf/linuxtrack](https://github.com/uglyDwarf/linuxtrack) (MIT license)
- **Active fork:** [github.com/fwfa123/linuxtrackx-ir](https://github.com/fwfa123/linuxtrackx-ir)
- **Platforms:** Linux, macOS
- **Compatibility:** X-Plane 12

The original project has not had a regular release since 2016 and relies on an outdated Qt4 dependency. The active fork **LinuxTrack X-IR** (v0.99.29, January 2026) addresses these issues: Qt5/Qt6 support, AppImage distribution, and a modernized X-Plane plugin.

## Features

- **6DOF head tracking:** Pitch, yaw, roll, and X/Y/Z translation
- **Supported hardware:** TrackIR 2–5, SmartNav 3/4, UVC webcams, PS3 Eye, Wiimote, generic HID joysticks
- **Configurable sensitivity:** Sensitivity curves, dead zones, and filters per axis
- **Joystick buttons:** Start/stop, recenter, and freeze via button press
- **Wine bridge:** Allows Windows games running under Proton/Wine to use LinuxTrack

## Value in Flight Simulation

Head tracking fundamentally changes the flight experience — natural head movements in the cockpit instead of mouse control. LinuxTrack is the native Linux solution for this, communicating directly with common tracking devices. Especially for TrackIR owners on Linux, there are few alternatives.

## Installation

**Recommended:** Use the X-IR fork as an AppImage.

**Download:** [LinuxTrack X-IR Releases](https://github.com/fwfa123/linuxtrackx-ir/releases)

1. Install LinuxTrack (AppImage or build from source)
2. Launch the LinuxTrack GUI (`ltr_gui`), configure the tracking device
3. In the "Misc." tab, click "Install XPlane plugin..." and select the X-Plane directory
4. Close the GUI — only the background daemon (`ltr_server1`) should run during flight

### Debian Dependencies (Build from Source)

```bash
sudo apt install build-essential git automake libmxml-dev libopencv-dev libtool libusb-1.0-0-dev zlib1g-dev libv4l-dev bison flex
```

For Qt5 support, also install `qtbase5-dev`.

### Notes

- TrackIR 4/5 requires firmware extraction on first launch
- The GUI (`ltr_gui`) must **not** be running while flying — only the daemon `ltr_server1`
- Alternative: [OpenTrack](opentrack.md) offers similar functionality with webcam-based AI tracking and broader platform support
- [XCamera](xcamera.md) supports LinuxTrack as one of its head tracking inputs

## Sources

- [LinuxTrack — GitHub](https://github.com/uglyDwarf/linuxtrack)
- [LinuxTrack X-IR — GitHub](https://github.com/fwfa123/linuxtrackx-ir)
- [LinuxTrack — Wiki](https://github.com/uglyDwarf/linuxtrack/wiki)
