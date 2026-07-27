---
description: "XLinSpeak adds text-to-speech for X-Plane plugins on Linux via speech-dispatcher. Plus Piper TTS Manager for high-quality neural speech synthesis."
---
# XLinSpeak

XLinSpeak is a Linux-only [plugin](../../glossary.md#plugin) that adds text-to-speech (TTS) support for [X-Plane](../../glossary.md#x-plane) plugins. On Windows and macOS, X-Plane uses the platform's native speech engines — on Linux, this integration is missing. XLinSpeak fills this gap via speech-dispatcher.

## Background

- **Developer:** uglyDwarf (Michal), XP12 fork: sparker256 (William Good)
- **Repository:** [github.com/sparker256/XLinSpeak](https://github.com/sparker256/XLinSpeak) (XP12)
- **Original:** [github.com/uglyDwarf/x-plane_plugins](https://github.com/uglyDwarf/x-plane_plugins/tree/master/XLinSpeak)
- **Platform:** Linux only
- **Compatibility:** X-Plane 12 (sparker256 fork; last commit February 2023, no releases since)

X-Plane 12 uses pre-generated audio files for its built-in ATC, which work on Linux without any TTS engine. XLinSpeak is primarily needed for **plugin-generated speech** — such as [Xchecklist](../cockpit/xchecklist.md) announcements, 124thATC, or other plugins calling `XPLMSpeakString()`.

## Features

- **Binary hooking:** Intercepts X-Plane's internal speech functions at the machine code level and routes text to speech-dispatcher
- **Transparent integration:** Works automatically with any plugin that uses X-Plane's speech output
- **No configuration:** Fully automatic after installation — no UI needed

## Value in Flight Simulation

Without XLinSpeak, Linux users only get a text overlay on screen when plugins request speech output — no audio. This plugin restores parity with Windows and macOS, so that checklist callouts, ATC plugins, and other speech-enabled extensions are audible on Linux.

## Installation

**Download:** [sparker256/XLinSpeak](https://github.com/sparker256/XLinSpeak)

The pre-compiled binary is in the repository at `XLinSpeak/lin_x64/XLinSpeak.xpl`. Copy the `XLinSpeak` folder to `Resources/plugins/`.

### Prerequisite: speech-dispatcher

```bash
sudo apt install speech-dispatcher
```

The default espeak-ng backend works reliably. No dedicated Piper module for speech-dispatcher exists — Piper can only be integrated manually via GenericExecuteSynth, which is different from the Piper TTS Manager described below.

### Build from Source

```bash
sudo apt install libspeechd-dev nasm gcc
cd XLinSpeak/src
make
```

---

## Alternative: Piper TTS Manager

Piper TTS Manager (PTTSM) is a FlyWithLua script that provides high-quality neural text-to-speech for X-Plane. While XLinSpeak intercepts `XPLMSpeakString()` calls and routes them through espeak-ng (functional but robotic), PTTSM uses Piper neural voice models — producing speech quality comparable to cloud-based TTS services.

- **Developer:** JT8D-17 (BK)
- **Repository:** [github.com/JT8D-17/Piper-TTS-Manager-for-X-Plane](https://github.com/JT8D-17/Piper-TTS-Manager-for-X-Plane) (EUPL-1.2)
- **Status:** No versioned releases
- **Platform:** All (FlyWithLua-based)

PTTSM monitors a text input file and generates WAV audio via Piper whenever new text appears. It was developed for X-ATC-Chatter's SimpleATC module and supports multiple voice models assigned to different actors.

### Dependencies

- [FlyWithLua](../scripting/flywithlua.md) NG+ for X-Plane 12
- Piper TTS binary — use [TheLouisHong/piper](https://github.com/TheLouisHong/piper/releases) fork (piper_linux_x86_64.tar.gz); the OHF-Voice/piper1-gpl upstream provides only Python wheels
- Voice models (`.onnx` + `.onnx.json`) from [Hugging Face piper-voices](https://huggingface.co/rhasspy/piper-voices/tree/main)


!!! note "XLinSpeak and PTTSM solve different problems"

    XLinSpeak intercepts X-Plane's internal speech functions — needed for plugins that call `XPLMSpeakString()`. PTTSM provides its own TTS pipeline for plugins that write text to a file (like X-ATC-Chatter). Both can run side by side without conflict.

### TTS Options on Linux

| Solution | Mechanism | Quality | Use case |
|----------|-----------|---------|----------|
| XLinSpeak + espeak-ng | Hooks `XPLMSpeakString()` → speech-dispatcher | Functional (robotic) | Plugin speech ([Xchecklist](../cockpit/xchecklist.md), 124thATC) |
| Piper TTS Manager | FlyWithLua + Piper neural models | High (natural) | X-ATC-Chatter, custom TTS |
| X-Plane 12 built-in ATC | Pre-generated audio files | Good | Standard ATC (works on all platforms) |

## Sources

- [XLinSpeak XP12 — GitHub](https://github.com/sparker256/XLinSpeak)
- [XLinSpeak Original — GitHub](https://github.com/uglyDwarf/x-plane_plugins/tree/master/XLinSpeak)
- [Native Speech Synthesis for Linux — X-Plane.org Forum](https://forums.x-plane.org/forums/topic/114358-native-speech-synthesis-for-linux/)
- [Piper TTS Manager — GitHub](https://github.com/JT8D-17/Piper-TTS-Manager-for-X-Plane)
- [Piper TTS — GitHub](https://github.com/OHF-Voice/piper1-gpl) (successor to archived rhasspy/piper)
