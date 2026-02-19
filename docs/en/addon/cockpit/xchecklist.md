---
description: "Xchecklist for X-Plane on Linux — interactive checklists with text-to-speech via speech-dispatcher. Installation, TTS setup, and XLinSpeak integration."
---
# Xchecklist

Xchecklist is an open-source [plugin](../../glossary.md#plugin) for [X-Plane](../../glossary.md#x-plane) that provides interactive checklists with text-to-speech support. On Linux, speech output is handled via speech-dispatcher — the same stack used by [XLinSpeak](../tools/xlinspeak.md).

## Background

- **Developer:** sparker256 (William Good), uglyDwarf (Michal Navratil)
- **Repository:** [github.com/sparker256/xchecklist](https://github.com/sparker256/xchecklist) (MIT license)
- **Platforms:** Windows, macOS, Linux (native `lin.xpl`)
- **Compatibility:** X-Plane 10, 11, 12

Xchecklist is actively maintained and ships pre-built binaries for all three platforms. The plugin uses the XPLM SDK and does not require FlyWithLua or any other scripting framework.

## Features

- **Interactive checklists:** 2D window and VR overlay that tracks completed items during each flight phase
- **Text-to-speech:** Reads checklist items aloud via the `sw_remark:` command in checklist files
- **Aircraft-specific checklists:** Custom `clist.txt` files per aircraft — community checklists available for Zibo 737, ToLiss, and many others
- **Companion tools:** Simon (TTS helper process for Linux/macOS speech output) and Checker (validation tool for custom checklists)

## Value in Flight Simulation

On Windows and macOS, X-Plane plugins can use the platform's native speech engines for checklist callouts. On Linux, this integration is missing — Xchecklist fills the gap with native TTS via speech-dispatcher, providing audible readback without any Windows-only dependencies. Combined with interactive item tracking, it brings full checklist workflow to the Linux cockpit.

## Installation

**Download:** [Xchecklist — x-plane.org](https://forums.x-plane.org/files/file/20785-xchecklist-linwinmac/)

Extract the ZIP file to `Resources/plugins/`. This creates the `Xchecklist/` folder with the Linux binary at `64/lin.xpl`.

No additional system packages are required for basic operation. For TTS support, see the next section.

### Build from Source

Building from source is optional — pre-built binaries are included in each release.

```bash
sudo apt install build-essential cmake git freeglut3-dev libudev-dev libopenal-dev libspeechd-dev
git clone https://github.com/sparker256/xchecklist.git
cd xchecklist
cmake -S ./src -B ./build -DCMAKE_BUILD_TYPE=RelWithDebInfo
cmake --build ./build
cp ./build/lin.xpl ./Xchecklist/64/
```

## Text-to-Speech on Linux

Xchecklist spawns a companion process (`simon`) that connects to speech-dispatcher via `libspeechd`. This handles the `sw_remark:` commands in checklist files — the items that are read aloud as you work through the checklist. The plugin itself does not call `XPLMSpeakString()` on Linux — all speech is routed through the simon/speech-dispatcher mechanism.

!!! tip "Recommended setup"

    Install [XLinSpeak](../tools/xlinspeak.md) alongside Xchecklist. While Xchecklist handles its own speech via simon/speech-dispatcher, XLinSpeak catches `XPLMSpeakString()` calls from other plugins that would otherwise produce only silent text overlays on Linux.

### Prerequisites

```bash
sudo apt install speech-dispatcher
```

The default espeak-ng backend works reliably. Verify that speech-dispatcher is running:

```bash
spd-say "checklist test"
```

If no audio is heard, check that the speech-dispatcher service is active and the correct audio output is configured.

## Sources

- [Xchecklist — GitHub](https://github.com/sparker256/xchecklist)
- [Xchecklist — forums.x-plane.org](https://forums.x-plane.org/files/file/20785-xchecklist-linwinmac/)
- [XLinSpeak — GitHub](https://github.com/sparker256/XLinSpeak)
- [speech-dispatcher — GitHub](https://github.com/brailcom/speechd)
