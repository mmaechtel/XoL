---
description: "XGS displays landing quality data in X-Plane — sink rate, G-forces, centerline deviation, and touchdown distance with configurable rating scales."
---
# XGS

XGS (Landing Speed Plugin Reloaded) is a standalone [plugin](../../glossary.md#plugin) by hotbso that displays detailed landing quality data — from sink rate and G-forces to touchdown distance and centerline deviation.

## Background

- **Developer:** hotbso (Holger Teutsch)
- **Repository:** [github.com/hotbso/xgs](https://github.com/hotbso/xgs) (open source, GPL-2.0)
- **Platforms:** Windows, macOS, Linux (native binaries)
- **Compatibility:** [X-Plane](../../glossary.md#x-plane) 12

XGS is an evolution of the original Landing Speed Plugin. Development has stalled (last release June 2023, last commit October 2024), but the plugin remains functional.

## Features

- **Sink rate & G-forces:** Maximum sink rate (fpm) and maximum G-force on landing
- **Quality rating:** Textual landing quality assessment from a configurable file (e.g., "Smooth landing", "Hard landing, requires inspection")
- **Speed & pitch:** Indicated airspeed and pitch angle at touchdown
- **Threshold crossing:** Height above the threshold and distance from the threshold to touchdown
- **Centerline deviation:** Lateral and angular deviation from runway centerline
- **ToLiss detection:** For ToLiss models, XGS detects ground contact via main landing gear strut compression and additionally reports nosewheel touchdown distance

**Configurable Rating Scales**

XGS ships with a default rating scale and an aircraft-specific scale for Airbus types (based on real-world inspection thresholds). Custom scales can be placed as text files in the aircraft directory.

## Value in Flight Simulation

The built-in X-Plane instruments show no detailed landing quality data after touchdown. XGS fills this gap with immediate feedback — useful for training consistent landings. The ToLiss-specific gear detection provides more precise data than the generic method.

## Installation

**Download:** [GitHub Releases](https://github.com/hotbso/xgs/releases)

Extract the ZIP file to `Resources/plugins/`. This creates the `xgs/` folder with the Linux binary at `64/lin.xpl`.

No additional system packages are required. There are no known Linux-specific issues.

## Sources

- [XGS — GitHub](https://github.com/hotbso/xgs)
- [XGS — forums.x-plane.org](https://forums.x-plane.org/files/file/45734-landing-speed-plugin-xgs-reloaded/)
