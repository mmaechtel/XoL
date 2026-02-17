# XLinSpeak

XLinSpeak is a Linux-only [plugin](../../glossary.md#plugin) that adds text-to-speech (TTS) support for X-Plane plugins. On Windows and macOS, X-Plane uses the platform's native speech engines — on Linux, this integration is missing. XLinSpeak fills this gap via speech-dispatcher.

## Background

- **Developer:** uglyDwarf (Michal), XP12 fork: sparker256 (William Good)
- **Repository:** [github.com/sparker256/XLinSpeak](https://github.com/sparker256/XLinSpeak) (XP12)
- **Original:** [github.com/uglyDwarf/x-plane_plugins](https://github.com/uglyDwarf/x-plane_plugins/tree/master/XLinSpeak)
- **Platform:** Linux only
- **Compatibility:** X-Plane 12 (sparker256 fork)

X-Plane 12 uses pre-recorded audio files for its built-in ATC, which work on Linux without any TTS engine. XLinSpeak is primarily needed for **plugin-generated speech** — such as XChecklist announcements, 124thATC, or other plugins calling `XPLMSpeakString()`.

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

The default espeak-ng backend works reliably. Piper as an alternative TTS backend currently causes a crash.

### Build from Source

```bash
sudo apt install libspeechd-dev nasm gcc
cd XLinSpeak/src
make
```

## Sources

- [XLinSpeak XP12 — GitHub](https://github.com/sparker256/XLinSpeak)
- [XLinSpeak Original — GitHub](https://github.com/uglyDwarf/x-plane_plugins/tree/master/XLinSpeak)
- [Native Speech Synthesis for Linux — X-Plane.org Forum](https://forums.x-plane.org/forums/topic/114358-native-speech-synthesis-for-linux/)
