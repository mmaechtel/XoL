---
description: "LinuxTrack head tracking for X-Plane on Linux — 6DOF tracking with TrackIR, webcam, or Wiimote. Installation and X-IR fork guide."
---
# LinuxTrack

LinuxTrack is a head-tracking software suite for Linux and macOS that translates head movements into X-Plane camera movements via the xlinuxtrack [plugin](../../glossary.md#plugin). It supports TrackIR, webcams, and Wiimotes as input devices and provides 6DOF tracking (6 degrees of freedom).

## Background

- **Developer:** uglyDwarf (Michal), active fork: fwfa123 (LinuxTrack X-IR)
- **Repository:** [github.com/uglyDwarf/linuxtrack](https://github.com/uglyDwarf/linuxtrack) (MIT license)
- **Active fork:** [gitlab.com/fwfa123/linuxtrackx-ir](https://gitlab.com/fwfa123/linuxtrackx-ir) (canonical home; the [GitHub repo](https://github.com/fwfa123/linuxtrackx-ir) is a mirror)
- **Platforms:** Linux, macOS
- **Compatibility:** X-Plane 12

The original project has not had a regular release since 2016 and relies on an outdated Qt4 dependency. The active fork **LinuxTrack X-IR** addresses these issues: a Qt6/CMake-first rearchitecture, AppImage distribution, a MinGW-based Wine bridge, and a modernized X-Plane plugin.

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

**Download:** [LinuxTrack X-IR Releases](https://gitlab.com/fwfa123/linuxtrackx-ir/-/releases) (AppImages are published on GitLab)

1. Install LinuxTrack (AppImage or build from source)
2. Launch the LinuxTrack GUI (`ltr_gui`), configure the tracking device
3. In the "Gaming" tab, click "Install Xplane plugin...", then browse to the X-Plane executable and confirm with "Open"
4. Close the GUI — only the background daemon (`ltr_server1`) should run during flight

### Debian Dependencies (Build from Source)

```bash
sudo apt install build-essential git cmake pkg-config libusb-1.0-0-dev zlib1g-dev bison flex qt6-base-dev qt6-tools-dev qt6-tools-dev-tools libqt6opengl6-dev libmxml-dev libx11-dev libxrandr-dev libgl1-mesa-dev libglu1-mesa-dev
```

For webcam, face tracking, and Wiimote support, also install `libv4l-dev`, `libopencv-dev`, and `libcwiid-dev`.

### Notes

- TrackIR 4/5 requires firmware extraction on first launch
- Running the GUI (`ltr_gui`) during flight is possible but not recommended — tracking works with the daemon `ltr_server1` alone
- Alternative: [OpenTrack](opentrack.md) offers similar functionality with webcam-based AI tracking and broader platform support
- [XCamera](xcamera.md) supports LinuxTrack as one of its head tracking inputs

## Sources

- [LinuxTrack — GitHub](https://github.com/uglyDwarf/linuxtrack)
- [LinuxTrack X-IR — GitLab](https://gitlab.com/fwfa123/linuxtrackx-ir)
- [LinuxTrack — Wiki](https://github.com/uglyDwarf/linuxtrack/wiki)
