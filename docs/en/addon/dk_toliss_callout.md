# DK Toliss Callout

DK Toliss Callout is a [FlyWithLua](flywithlua.md) script that provides automated voice callouts of the Flight Mode Annunciator (FMA) for ToLiss Airbus aircraft. When autopilot modes change (CLB, OP CLB, SPEED, NAV, G/S), the script announces the new mode via text-to-speech.

## Background

- **Developer:** cxn0026
- **Download:** [X-Plane.org](https://forums.x-plane.org/files/file/91367-toliss-airbus-fma-callout-flywithlua-script/)
- **Platforms:** Windows, macOS, Linux (pure Lua)
- **Compatibility:** X-Plane 12
- **Dependency:** [FlyWithLua NG+](flywithlua.md)

The script reads the blue FMA values from the upper FMA box on the PFD. Magenta values are not yet implemented. Due to the complexity of extracting FMA data from ToLiss aircraft, callouts may occasionally fail depending on variable changes. Verified on the A319 and A320neo — should work with other ToLiss Airbus types.

## Features

- **Automated FMA callouts:** Announces autopilot mode changes via TTS
- **Customizable TTS text:** Users can edit what the speech engine pronounces
- **Real-time monitoring:** Detects FMA changes as they occur

## Value in Flight Simulation

FMA callouts are standard operating procedure in real Airbus cockpits — the pilot monitoring announces mode changes to maintain shared awareness. This script automates that procedure for single-pilot operation, adding realism to ToLiss Airbus flights and helping pilots track autopilot mode transitions without constantly scanning the FMA.

## Installation

**Download:** [X-Plane.org](https://forums.x-plane.org/files/file/91367-toliss-airbus-fma-callout-flywithlua-script/)

Place the `.lua` file into `Resources/plugins/FlyWithLua/Scripts/`.

### Linux Notes

No Linux-specific issues are known. The script uses X-Plane's built-in TTS via `XPLMSpeakString()`. For audible output on Linux, [XLinSpeak](xlinspeak.md) is required.

## Sources

- [Toliss Airbus FMA Callout — X-Plane.org](https://forums.x-plane.org/files/file/91367-toliss-airbus-fma-callout-flywithlua-script/)
