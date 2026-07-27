---
description: "AutoGate provides animated jetways and docking guidance for older X-Plane sceneries built with the AutoGate toolkit. Legacy plugin, maintained for XP12."
---
# AutoGate

AutoGate is a [plugin](../../glossary.md#plugin) for [X-Plane](../../glossary.md#x-plane) that provides animated jetways and docking guidance systems for sceneries built with the AutoGate toolkit.

## Background

- **Original:** [Marginal/AutoGate](https://github.com/Marginal/AutoGate) by Jonathan Harris (2006–2017, no longer maintained)
- **XP12 fork:** [hotbso/AutoGate](https://github.com/hotbso/AutoGate) (X-Plane 12 compatible)
- **License:** Plugin code LGPL-2.1, 3D objects/textures CC-BY 3.0
- **Platforms:** Windows and Linux (the XP12 fork ships native binaries for both; no macOS binary is provided)
- **Compatibility:** X-Plane 12 (hotbso fork)

!!! warning "Legacy plugin"

    AutoGate is in maintenance mode. For new sceneries, **[openSAM](opensam.md)** is recommended. AutoGate is only relevant for older scenery packages built with the AutoGate toolkit.

## Features

- **Jetways and DGS:** Two jetway types (glass, steel) and four DGS types (Safedock, standalone DGS, and marshaller)
- **Docking on beacon off:** Jetway docks when the beacon is switched off with the aircraft at the stop position

## Value in Flight Simulation

AutoGate was the first open-source jetway system for X-Plane and laid the foundation for openSAM. Some older custom sceneries use AutoGate assets. For these sceneries, the hotbso fork remains the only X-Plane 12 compatible option. AutoGate can run alongside [openSAM](opensam.md) and [AutoDGS](autodgs.md).

## Installation

**Download:** [GitHub Releases (hotbso fork)](https://github.com/hotbso/AutoGate/releases)

Extract the ZIP file to `Resources/plugins/`. The Linux binary links against OpenAL; ensure that libopenal1 is installed.

## Sources

- [AutoGate — GitHub (hotbso fork for XP12)](https://github.com/hotbso/AutoGate)
- [AutoGate — GitHub (original by Marginal)](https://github.com/Marginal/AutoGate)
