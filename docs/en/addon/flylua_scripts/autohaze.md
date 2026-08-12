---
description: "AutoHaze is a FlyWithLua script for X-Plane 12 that replaces the default haze with turbidity derived from real satellite aerosol and weather data."
---
# AutoHaze — Real-World Haze Correction

AutoHaze is a [FlyWithLua](../scripting/flywithlua.md) script that addresses the uniform haze [X-Plane](../../glossary.md#x-plane) 12 shows on clear days. Instead of a fixed default turbidity, it derives the haze from measured atmospheric data for the aircraft's actual position — satellite aerosol values, surface weather and boundary layer height.

## Background

- **Developer:** MrBitsy
- **Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/99665-autohaze/)
- **Platforms:** Windows, macOS, Linux (one helper binary per platform)
- **Compatibility:** X-Plane 12
- **Dependency:** [FlyWithLua NG+](../scripting/flywithlua.md), free API keys for the online data queries
- **License:** Free download, donation link on the download page

## The Problem

According to the developer, X-Plane 12 derives its haze primarily from METAR visibility. A METAR caps that figure — at 9999 m under ICAO, at 10 statute miles in the US — so whenever conditions are better than the cap, the simulator receives no usable visibility value and falls back to a default turbidity. The result is the same milky sky over the Mojave Desert as over the Indo-Gangetic Plain, and it does not thin out with altitude: the view at FL300 looks as murky as it does at low level.

## Data Sources

AutoHaze queries several services and converts their readings into a turbidity value:

| Source | Delivers | Effect |
| --- | --- | --- |
| CAMS (Copernicus) | Satellite-measured aerosol optical depth at the aircraft position | Regional variation — clear air over California vs. dense haze over northern India |
| VisualCrossing / OpenWeatherMap | Surface visibility, humidity, temperature, dew point, wind | Fine-tuning for near-surface conditions |
| Open-Meteo | Real boundary layer height | Haze thins out during climb |

The conversion uses the Koschmieder and Linke turbidity equations rather than an empirical lookup table.

## Features

- **Position-based haze:** Turbidity follows the aircraft, not a global default value
- **Altitude scaling:** Above the real boundary layer the haze recedes into clean air
- **Rain coupling:** Visibility changes with the amount of rain hitting the aircraft instead of staying fixed during a shower
- **Gradual transitions:** Turbidity changes are always blended, never instant
- **Background helper:** All HTTP queries run in a separate helper process, so no console window flashes and the simulator does not pause
- **Persistent settings:** CAMS preference and query interval are restored on startup from the last manual save
- **Hotkey window:** The AutoHaze window can be bound to a key combination under *Settings → AutoHaze*

## Value in Flight Simulation

Haze is a primary distance cue, and X-Plane 12 handles it worst in the situation that occurs most often — visibility better than the METAR cap. In practice the correction usually goes one way: on genuinely clear days the default haze veil disappears and the view opens up. Over regions with high aerosol load, or in humid air near the surface, it goes the other way and turns denser than the default. Climbing out of the murk into clean air becomes a visible event rather than a constant backdrop. AutoHaze acts on the haze; the weather situation itself comes from X-Plane or from a source such as [NOAA Weather](../scenery_addons/noaa_weather.md). Neither source documents how the two behave together, and both write to visibility-related values — worth watching when running them side by side. [X-ProTurb](xproturb.md) follows the same idea of driving an effect from real atmospheric data, but acts on turbulence and does not overlap.

## Installation

**Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/99665-autohaze/)

The package ships as a ZIP archive holding the script, the installation guide and the helper for each of the three platforms. Unpack it and copy the contents into `Resources/plugins/FlyWithLua/Scripts/` — all files can stay in place, AutoHaze loads the helper matching the operating system.

!!! warning "Unpack the ZIP, do not download single files"

    The ZIP package exists precisely to preserve the macOS and Linux helper filenames. Downloading the files individually can alter them, and AutoHaze then fails to find the helper for the running system.

!!! note "Linux specifics"

    Official Linux and macOS support starts at version 2.4; the developer states outright that they own neither system and rely on user feedback for both. Two later fixes matter on Linux: the helper now detaches cleanly from X-Plane, so a simulator crash no longer leaves parts of it unable to unload, and the helper binaries bundle CA certificates, which fixes the SSL errors some distributions produced during the API queries. The helper writes its log to `AutoHaze-helper.log` inside the FlyWithLua directory — the first place to look when no data arrives.

Live mode needs free API keys for the weather services. The developer notes that the HTTP requests run through Python and that no additional software is required on Windows 10 and later; the source makes no equivalent statement for Linux, so whether the Linux helper brings its own runtime or expects a system Python is not documented. Any distribution used for X-Plane ships Python anyway.

## Sources

- [AutoHaze — forums.x-plane.org](https://forums.x-plane.org/files/file/99665-autohaze/)
