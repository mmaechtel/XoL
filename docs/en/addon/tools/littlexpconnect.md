# Little XpConnect

Little XpConnect is a [plugin](../../glossary.md#plugin) for [X-Plane](../../glossary.md#x-plane) 11/12 that serves as a bridge between X-Plane and the flight planning and navigation tool [Little Navmap](https://github.com/albar965/littlenavmap).

## Background

- **Developer:** Alexander Barthel (albar965)
- **Repository:** [github.com/albar965/littlexpconnect](https://github.com/albar965/littlexpconnect) (open source, GPL-3.0)
- **Platforms:** Windows, macOS, Linux (native binaries)
- **Compatibility:** X-Plane 11 and X-Plane 12

The plugin is actively maintained and is included in the Little Navmap download archive — it is not downloaded separately.

## Features

- **Flight data transfer:** Position, speed, heading, altitude, autopilot settings, fuel, weight
- **Weather data:** Temperature, pressure, visibility, wind, icing
- **AI/multiplayer aircraft:** Positions via TCAS interface
- **Ship positions:** Carrier and frigate
- **Shared memory IPC:** Communication via shared memory — no network port for local connections
- **Configurable fetch rate:** 50–500 ms interval for dataref queries

### Network Operation

To run Little Navmap on a different machine, start **Little Navconnect** (also included in the download) on the X-Plane machine. It reads the shared memory and forwards the data via TCP port **51968**.

## Value in Flight Simulation

Little Navmap is one of the most comprehensive free flight planning and navigation tools. Little XpConnect enables real-time display of the aircraft position on the Little Navmap map, moving map during flight, and monitoring of all flight parameters. The plugin uses shared memory instead of network communication, which means minimal latency and zero configuration effort for local setups.

## Installation

**Download:** Included in the [Little Navmap archive](https://github.com/albar965/littlenavmap/releases).

Copy the `Little Xpconnect` folder from the archive to `Resources/plugins/`. The plugin can also be installed/updated via the Little Navmap menu (`Tools`).

No additional system packages are required. There are no known Linux-specific issues.

**Configuration file:** `$HOME/.config/ABarthel/little_xpconnect.ini`

## Sources

- [Little XpConnect — GitHub](https://github.com/albar965/littlexpconnect)
- [Little Navmap — GitHub](https://github.com/albar965/littlenavmap)
- [Little Navmap — Documentation](https://www.littlenavmap.org/)
