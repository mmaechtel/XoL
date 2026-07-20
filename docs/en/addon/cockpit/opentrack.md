---
description: "OpenTrack head tracking for X-Plane on Linux — 6DOF tracking with NeuralNet webcam tracker, IR devices, or SmoothTrack. Debian build guide and HeadTrack plugin setup."
---
# OpenTrack

OpenTrack is a head-tracking application for Linux, Windows, and macOS that translates head movements into X-Plane camera movements. Combined with the HeadTrack [plugin](../../glossary.md#plugin) by amyinorbit, it provides the recommended head-tracking stack for [X-Plane](../../glossary.md#x-plane) 12 on Linux.

## Background

- **Developer:** Stanisław Halik and contributors
- **Repository:** [github.com/opentrack/opentrack](https://github.com/opentrack/opentrack) (ISC license)
- **Platforms:** Windows, Linux (macOS currently unmaintained)
- **Compatibility:** X-Plane 10, 11, 12

OpenTrack is actively maintained and serves as the successor to FaceTrackNoIR. It supports a wide range of input trackers and output protocols. On Linux, the NeuralNet Tracker provides AI-based head tracking via a standard webcam — no special hardware required.

### HeadTrack Plugin

- **Developer:** amyinorbit
- **Repository:** [github.com/amyinorbit/headtrack](https://github.com/amyinorbit/headtrack) (MIT license)
- **Platforms:** Windows, Linux, macOS

HeadTrack is a lightweight X-Plane plugin that receives 6DOF tracking data over UDP port 4242. Its last release dates from October 2022 and development has stalled, but the Linux binary still works with X-Plane 12. It acts as the bridge between OpenTrack and X-Plane — the recommended connection method on Linux, because OpenTrack's own X-Plane plugin is not distributed as a binary.

## Features

- **6DOF head tracking:** Pitch, yaw, roll, and X/Y/Z translation
- **NeuralNet Tracker:** AI-based face tracking via webcam — no IR hardware needed, runs on CPU (requires ONNX Runtime, see installation)
- **PointTracker:** Classical tracking with 3 IR LEDs or reflective points and an IR camera
- **ArUco marker:** Printed paper marker in front of a webcam — zero-cost alternative to IR hardware
- **SmoothTrack input:** Receives tracking data from the [SmoothTrack](https://smoothtrack.app/) smartphone app (paid, iOS/Android) via WiFi/UDP
- **Filters and curves:** Accela filter, response curves, dead zones, and smoothing per axis
- **Hotkeys:** Start/stop, recenter, and zero via keyboard or joystick buttons

## Value in Flight Simulation

Head tracking on Windows typically relies on TrackIR with proprietary drivers. On Linux, OpenTrack provides an open-source alternative with native support for webcam-based AI tracking — the NeuralNet Tracker runs without any special hardware, making it the most accessible head-tracking solution for Linux flight simmers. The HeadTrack plugin ensures reliable data delivery to X-Plane 12 where the built-in OpenTrack plugin falls short.

## Recommended Setup

The recommended data flow on Linux:

```
Input (choose one):
  ├─ NeuralNet Tracker (webcam, no hardware)
  ├─ PointTracker (IR LEDs + camera)
  └─ SmoothTrack (smartphone app)
        │
        ▼
OpenTrack (Linux, built from source or package)
  ├─ Filter: Accela (default, recommended)
  ├─ Response curves per axis
  └─ Output: "UDP over network" → 127.0.0.1:4242
        │
        ▼
HeadTrack plugin (amyinorbit) in X-Plane
  └─ In-sim GUI for sensitivity and smoothing
```

!!! warning "Avoid the built-in OpenTrack X-Plane plugin"

    OpenTrack has its own X-Plane output protocol with a companion plugin (`opentrack.xpl`, POSIX shared memory). It is not shipped as a binary — it is only built when the X-Plane SDK path is passed via `-DSDK_XPLANE=`, and it is local-only. Use the HeadTrack plugin with UDP output instead.

## Installation

### OpenTrack on Debian/Ubuntu

```bash
sudo apt install build-essential cmake git libopencv-dev libproc2-dev qt6-base-private-dev qt6-tools-dev
git clone https://github.com/opentrack/opentrack.git
cd opentrack && cmake -B build && cmake --build build --parallel $(nproc)
```

!!! note "NeuralNet Tracker requires ONNX Runtime"

    The build commands above produce a working OpenTrack but without the NeuralNet tracker unless ONNX Runtime is installed. On Debian/Ubuntu, install `libonnxruntime-dev` if available, or download the [ONNX Runtime release](https://github.com/microsoft/onnxruntime/releases) and add `-DONNXRuntime_DIR=<path>` to the CMake command.

### HeadTrack Plugin

**Download:** [HeadTrack Releases](https://github.com/amyinorbit/headtrack/releases)

Extract the ZIP file to `Resources/plugins/`. This creates the `htrack/` folder with the Linux binary at `lin_x64/htrack.xpl`.

No additional system packages are required.

## Configuration

### OpenTrack Output

1. Launch OpenTrack
2. Select a tracker as input (e.g., "NeuralNet tracker" for webcam)
3. Set **Output** to "UDP over network"
4. In the output settings, set the target IP to `127.0.0.1` and port to `4242`
5. Configure the Accela filter (default settings work well as a starting point)
6. Adjust response curves per axis — reduce sensitivity for yaw/pitch to avoid jerky movements

### HeadTrack Plugin in X-Plane

After installing the plugin and starting X-Plane:

1. Open the HeadTrack settings via the plugin menu
2. Adjust sensitivity and smoothing — start with low values and increase gradually
3. Use the recenter hotkey in OpenTrack to reset the neutral head position before each flight

### NeuralNet Tracker

The NeuralNet Tracker uses a neural network model (ONNX Runtime) to detect face position from a standard webcam. ONNX Runtime must be installed separately before building — on Debian/Ubuntu, install `libonnxruntime-dev` if available, or download the [ONNX Runtime release](https://github.com/microsoft/onnxruntime/releases) and set `-DONNXRuntime_DIR=<path>` during the CMake step. It runs entirely on CPU and does not require a GPU.

- Works with most USB and built-in webcams
- Adequate lighting is important — avoid strong backlight
- Performance: typical CPU usage is low enough to run alongside X-Plane without impact

### SmoothTrack (Smartphone)

[SmoothTrack](https://smoothtrack.app/) is a paid smartphone app (iOS/Android) that provides head tracking via the front camera and sends data over WiFi.

- In OpenTrack: Set input to "UDP over network" to receive SmoothTrack data
- Alternatively: Send SmoothTrack directly to HeadTrack on port 4242, bypassing OpenTrack entirely

## Sources

- [OpenTrack — GitHub](https://github.com/opentrack/opentrack)
- [HeadTrack — GitHub](https://github.com/amyinorbit/headtrack)
- [SmoothTrack — Website](https://smoothtrack.app/)
- [LinuxTrack](linuxtrack.md) — Alternative head-tracking solution for Linux
- [XCamera](xcamera.md) — Camera plugin with OpenTrack integration
