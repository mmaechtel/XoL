---
description: "AnyAirline for X-Plane 12 — AI cabin announcements, route-aware passenger manifest, boarding ambience, and IFE map, with a Linux connector."
---
# AnyAirline

AnyAirline is a passenger cabin immersion tool for [X-Plane](../../glossary.md#x-plane) 12 (and Microsoft Flight Simulator 2020/2024). Instead of treating the cabin as a generic soundboard, it turns the route, aircraft and airline into a passenger manifest and layers route-aware cabin announcements, boarding ambience and a passenger IFE map on top of the flight. A desktop connector bridges the simulator; the cabin flow is prepared in an online workspace.

## Background

- **Developer:** AnyAirline
- **Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/100112-anyairline-ai-cabin-crew-passenger-ife-airline-immersion) · [anyairline.app](https://anyairline.app)
- **Platforms:** Windows, Linux, macOS (desktop connector, packaged runtime included)
- **Compatibility:** X-Plane 12, MSFS 2020/2024 (open beta)
- **Account:** Free AnyAirline account required (online workspace for sync, workshop and credits)
- **Pricing:** Freemium — local English voice and passenger IFE map are free

## Features

- **Passenger manifest pipeline:** Turns route, aircraft and airline into named passengers, cabin crew roles, a real seat-map layout and passenger context — reused by both announcements and the IFE view
- **AI cabin announcements:** Route-aware gate, welcome, safety and service announcements; a free local English voice runs offline with no credits, while paid cloud AI adds richer airline-style generation and multilingual output (74 languages)
- **Three voice modes:** Local AI (free, English, offline), AI Lite and Full AI (cloud, credit-based)
- **Cabin ambience:** Boarding and deboarding music plus gate and PA chimes layered around announcements
- **Passenger IFE map (free):** Shows route, aircraft position, ETA and live-style flight data while the connector follows the simulator
- **Workshop asset library:** Shared boarding/deboarding music, airport chimes, safety media, cabin layouts and reusable flight templates (including cargo-style flows)
- **SimBrief integration:** Imports an OFP and uses route, fleet, flight number, schedule and airport context to prepare the cabin flow

## Value in Flight Simulation

AnyAirline fills the silent-cabin gap that most aircraft leave behind. The manifest approach means announcements and the IFE map reference the actual route, airline and seat layout rather than a generic preset. It is **not** a virtual-airline management, ACARS, dispatch or logbook system — it adds a passenger cabin layer on top of those tools and complements cabin-sound plugins like [KabinXP](kabinxp.md). Crucially for Linux setups, the connector ships an official Linux build, so the immersion layer works without a Windows host.

## Installation

**Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/100112-anyairline-ai-cabin-crew-passenger-ife-airline-immersion) · [anyairline.app](https://anyairline.app)

Create a free AnyAirline account, then install the desktop connector — the local bridge that handles simulator telemetry and audio playback. Start the connector alongside X-Plane and prepare announcements, ambience, workshop media and the IFE map in the web workspace. The free tier covers the local English cabin voice, workshop access and the passenger IFE map; paid AI credits unlock cloud voices, multilingual generation and advanced templates.

### Linux Notes

The connector officially supports Linux with a packaged Python runtime included (8 GB RAM minimum, Ubuntu 22.04/24.04 LTS or a compatible x64 desktop). Unlike the Windows build it does not bundle FFmpeg — install `ffmpeg`, `ffprobe` and `espeak-ng` from the distribution repositories for the local voice fallback. The cloud features run in the browser-based workspace and are platform-independent.

## Sources

- [AnyAirline — forums.x-plane.org](https://forums.x-plane.org/files/file/100112-anyairline-ai-cabin-crew-passenger-ife-airline-immersion)
- [AnyAirline — official website](https://anyairline.app)
