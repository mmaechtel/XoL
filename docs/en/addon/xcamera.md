# XCamera

XCamera is a camera system for [X-Plane](../glossary.md#x-plane) 11/12 that replaces the default view system with a fully configurable, aircraft-specific camera framework.

## Background

- **Developer:** Stick and Rudder Studios
- **Website:** [stickandrudderstudios.com/x-camera](https://stickandrudderstudios.com/x-camera/)
- **License:** Commercial (closed source)
- **Platforms:** Windows, macOS, Linux (native binaries)
- **Compatibility:** X-Plane 11.3+ and X-Plane 12

XCamera is actively maintained. The [plugin](../glossary.md#plugin) is a standalone XPLM plugin and does not require FlyWithLua or any other scripting framework.

## Features

- **Custom views:** Multiple camera categories and views per aircraft, stored in aircraft-specific configuration files
- **Camera transitions:** Smooth and Bezier curve transitions between cameras, automatic sequences
- **Airport cameras:** Automatically generated cameras at gates, signs, runways, and tower positions
- **Walk mode / free camera:** Free movement via keyboard in and around the aircraft
- **G-Loaded Camera:** Replaces the earlier Cinema Verite function starting with X-Plane 12.4.1
- **External cameras:** Configurable external views with orbit and fly-by
- **AI aircraft views:** View from the perspective of AI aircraft
- **Mini control panel:** Color-coded dynamic panel for quick camera selection
- **Head tracking:** TrackIR (Windows), OpenTrack (Linux/macOS, recommended), [LinuxTrack](linuxtrack.md) (unmaintained), SimHat (iPhone)

### Free vs. Registered

- **Free:** All features are functional, but advanced settings are not saved. Airport camera generation is limited.
- **Registered ($18 USD):** Settings are saved, full airport camera generation. A 2.X key works for all 2.X versions.

## Value in Flight Simulation

XCamera offers hundreds of aircraft-specific camera positions that are shared through the community. The Bezier transitions between cameras create a cinematic effect that standard views lack. Airport cameras provide external views from gate, tower, or runway — useful for realistic approach observations. Walk mode allows free exploration of the aircraft and its surroundings.

## Installation

**Download:** [stickandrudderstudios.com/x-camera/download-x-camera](https://stickandrudderstudios.com/x-camera/download-x-camera/) (free version) or [X-Plane.Org Store](https://store.x-plane.org/X-Camera_p_889.html) (registered)

Extract the ZIP file to `Resources/plugins/`. This creates the `X-Camera/` folder with the Linux binary at `64/lin.xpl`.

No additional system packages are required. There are no known Linux-specific issues.

### Head Tracking on Linux

For head tracking on Linux, **OpenTrack** is recommended. LinuxTrack is no longer actively maintained.

**OpenTrack setup**

1. Install and configure OpenTrack (input: webcam with NeuralNet tracker, IR clip, etc.)
2. In OpenTrack: Set output to "UDP over network"
3. Place the OpenTrack X-Plane plugin (included in the OpenTrack build) in `Resources/plugins/` and enable "Track Head Motion" in X-Plane
4. In XCamera: Enable the "TrackIR" checkbox on the desired views — XCamera treats OpenTrack data the same as TrackIR data

**Installing OpenTrack on Debian/Ubuntu**

```bash
sudo apt install cmake qtbase5-dev libopencv-dev libprocps-dev
git clone https://github.com/opentrack/opentrack.git
cd opentrack && mkdir build && cd build
cmake .. && make -j$(nproc)
```

Alternatively, pre-built packages are available in some distributions.

## Sources

- [X-Camera — Stick and Rudder Studios](https://stickandrudderstudios.com/x-camera/)
- [X-Camera — forums.x-plane.org](https://forums.x-plane.org/files/file/24209-x-camera-linmacwin-32-64/)
- [OpenTrack — GitHub](https://github.com/opentrack/opentrack)
- [OpenTrack X-Plane Plugin — included in OpenTrack build](https://github.com/opentrack/opentrack/tree/master/x-plane-plugin)
