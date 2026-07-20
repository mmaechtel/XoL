---
description: "XP Walkaround for X-Plane 12 — first-person walkaround with flashlight, campsite system, and mouse look. Native Linux plugin with SimpleWalkaround as free alternative."
---
# XP Walkaround

XP Walkaround is a commercial [plugin](../../glossary.md#plugin) for [X-Plane](../../glossary.md#x-plane) 12 that adds first-person movement outside the cockpit — walking around the aircraft, exploring the airport environment, and inspecting the ramp at night with a built-in flashlight. The plugin runs natively on Linux and is currently distributed as a beta release.

## Background

- **Developer:** clemacamelc
- **Store:** [Gumroad](https://clemacamelc.gumroad.com/l/xpwalkaround) (commercial)
- **Platforms:** Windows, macOS, Linux
- **Compatibility:** X-Plane 12

The plugin ships native binaries for all three platforms — no additional system packages or dependencies required on Linux.

## Features

- **Walk Mode:** Leave the cockpit and move freely around the aircraft and airport. Enter or exit via the plugin window, Plugins menu, or ESC key.
- **First/third-person view:** Switch between first-person and third-person perspective
- **Mouse Look:** Toggle with M key for natural look-around while walking. Optional inverted Y axis. When disabled, X-Plane's default right-click camera remains intact.
- **Flashlight:** Toggle with F key for dark cockpits, cabins, and nighttime ramp inspections. Volume adjustable via plugin settings.
- **Skydiving:** Above 500 ft a "Skydive!" button appears in the plugin window. Freefall with body-position control, parachute deploy via F key (auto-deploy at 500 ft), steerable ram-air canopy, and a seamless transition into Walk Mode on touchdown.
- **Campsite System:** Spawn a campsite with campfire in front of the current view (requires X-Plane 12.04+). Build, cancel, or tear down from the UI. Designed for bush flying and remote operations.
- **Movement controls:** WASD movement, Q/E lean, C crouch, Backspace jump, ESC exit Walk Mode
- **Plugin window:** Floating, resizable ImGui window accessible via Plugins menu. Optional automatic display on startup.
- **Persistent settings:** View height, sound volume, mouse invert, and window preferences saved between sessions

## Value in Flight Simulation

Instead of being locked to the cockpit camera, pilots can step outside, walk around the aircraft, and explore the airport surroundings. The flashlight enables night inspections of cockpits and cargo areas. The campsite system adds atmosphere for bush flying at remote strips. Unlike many commercial X-Plane addons, the plugin includes a native Linux binary and works without compatibility layers or workarounds.

## Installation

**Download:** [Gumroad](https://clemacamelc.gumroad.com/l/xpwalkaround)

Install as a standalone plugin into `Resources/plugins/`. Activate the Gumroad license key in the plugin window after first launch. No additional system packages or configuration required on Linux.

!!! tip "Linux compatibility"

    XP Walkaround works without restrictions on Linux. No additional configuration or workarounds required.

## Free Alternative: SimpleWalkaround

[SimpleWalkaround](https://forums.x-plane.org/files/file/96508-simplewalkaround/) is a free plugin that provides basic walkaround movement outside the cockpit. It uses WASD movement controls, sprint (C), and crouch (X) but lacks the extended features of XP Walkaround such as flashlight, campsite system, mouse look, and persistent settings. The developer tests on Windows only and does not guarantee behaviour on other platforms, so Linux use is untested.

## Sources

- [XP Walkaround — Gumroad](https://clemacamelc.gumroad.com/l/xpwalkaround)
- [SimpleWalkaround — forums.x-plane.org](https://forums.x-plane.org/files/file/96508-simplewalkaround/)
