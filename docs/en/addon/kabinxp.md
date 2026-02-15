# KabinXP

KabinXP is a lightweight cabin announcement plugin for [X-Plane](../glossary.md#x-plane) 12. It plays custom audio files (captain announcements, safety briefings, boarding sounds) with a single click during flight. The plugin ships with an empty sound library — users supply their own audio files and organize them per airline or livery.

## Background

- **Developer:** Kadikoy34
- **Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/98298-kabinxp/)
- **Platforms:** Windows, macOS, Linux
- **Compatibility:** X-Plane 12
- **Price:** Free (freeware)

## Features

- **Custom audio library:** Ships empty — users add WAV, MP3, or FLAC files
- **Per-livery sound packs:** Each livery can have its own announcement folder, auto-detected on load
- **3D Spatial Audio:** Sounds are positionally attached inside the aircraft cabin
- **Custom subfolders:** Up to 10 subfolders per announcement folder, UI buttons update automatically
- **Drag-and-arrange buttons:** Reorder announcement buttons via drag-and-drop
- **Persistent layouts:** Button order is saved per livery and restored on next flight
- **Live indicator:** Shows which announcement is currently playing

## Value in Flight Simulation

KabinXP adds cabin atmosphere without requiring a specific aircraft or preset library. Since users supply their own audio files, it works with any airline livery and any language. The per-livery auto-detection means switching from a Lufthansa to a Ryanair livery automatically loads the matching announcements — no manual configuration needed.

## Installation

**Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/98298-kabinxp/)

Install as a standalone plugin into `Resources/plugins/KabinXP/`. Create a sound folder within each livery directory and add audio files (WAV, MP3, or FLAC). KabinXP detects the livery on aircraft load and presents the available announcements in its UI.

### Linux Notes

KabinXP is a compiled plugin. Verify that the download includes a `lin.xpl` binary. If only Windows and macOS binaries are present, the plugin does not support Linux natively.

## Sources

- [KabinXP — forums.x-plane.org](https://forums.x-plane.org/files/file/98298-kabinxp/)
- [KabinXP — x-plane.to](https://x-plane.to/file/2078/kabinxp)
