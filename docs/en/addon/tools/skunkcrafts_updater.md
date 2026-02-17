# SkunkCrafts Updater

The SkunkCrafts Updater is the de facto standard update tool for [X-Plane](../../glossary.md#x-plane) addons. It scans an X-Plane installation for addons that ship with SkunkCrafts configuration files, compares versions against remote repositories, and downloads updates automatically.

## Background

- **Developer:** Lionel Zamouth (SkunkCrafts / Aerobask)
- **Forum:** [forums.x-plane.org](https://forums.x-plane.org/forums/forum/406-skunkcrafts-updater/)
- **License:** Freeware, closed source (the update protocol is open and documented)
- **Platforms:** Windows, macOS, Linux (native binaries)
- **Compatibility:** X-Plane 11 and 12

The current standalone version is a complete rewrite in Go with a Fyne UI. It replaces the legacy in-game [plugin](../../glossary.md#plugin) and runs independently of X-Plane — no running simulator required for updates.

## Features

- **Automatic discovery:** Scans all X-Plane subdirectories for `skunkcrafts_updater.cfg` files
- **Differential updates:** Only downloads files whose CRC32 checksum or size differs from the remote version
- **Concurrent downloads:** Up to 32 simultaneous downloads (configurable)
- **Beta channel:** Optional `skunkcrafts_updater_beta.cfg` for beta releases
- **Open protocol:** Any addon developer can integrate by shipping a cfg file pointing to their own repository — no coordination with the updater developer needed

## Value in Flight Simulation

Because dozens of commercial and freeware developers have adopted the SkunkCrafts protocol — including Aerobask, X-Crafts, SimCoders, VSKYLABS, Just Flight, FlyJSim, and Stick and Rudder Studios — installing the updater provides a single tool to keep most addons current. Each addon ships a `skunkcrafts_updater.cfg` that points to the developer's repository; the updater discovers these files automatically and handles the rest.

!!! info "Troubleshooting"

    The cfg files are plain text with pipe delimiters (`key|value`) — not INI, not JSON. When an addon does not appear in the updater, check that `skunkcrafts_updater.cfg` exists in the addon's root directory, that `disabled` is set to `false`, and that the `module` URL is reachable.

## Installation

**Download:** The standalone client is distributed via the [forums.x-plane.org release thread](https://forums.x-plane.org/forums/topic/292710-20250206-skunkcrafts-updater-standalone-client-v32d-available/). A free X-Plane.org account is required.

The Linux binary is a single file with the `.lin` extension. Place it in the X-Plane root directory (the folder containing `X-Plane-x86_64`) and make it executable:

```bash
chmod +x SkunkCrafts_Updater*.lin
./SkunkCrafts_Updater*.lin
```

The updater must be launched from the X-Plane root directory — it discovers addons by scanning subdirectories relative to its own location. A legacy in-game plugin version exists but is no longer actively developed.

### glibc Requirement

The Linux binary requires glibc 2.32 or higher. This is a consequence of the Go + Fyne build toolchain (CGo links against the build system's glibc).

| Distribution | glibc | Status |
|---|---|---|
| Debian 12 Bookworm | 2.36 | Works |
| Debian 11 Bullseye | 2.31 | May fail |
| Ubuntu 22.04+ | 2.35 | Works |
| Ubuntu 20.04 | 2.31 | Fails |

### Fyne UI and Wayland

The Fyne toolkit supports Wayland but may fall back to XWayland depending on the compositor. No SkunkCrafts-specific Wayland issues are documented.

## Sources

- [SkunkCrafts Updater — forums.x-plane.org](https://forums.x-plane.org/forums/forum/406-skunkcrafts-updater/)
- [Standalone Client v3.2d Release Thread — forums.x-plane.org](https://forums.x-plane.org/forums/topic/292710-20250206-skunkcrafts-updater-standalone-client-v32d-available/)
- [glibc Requirement Discussion — forums.x-plane.org](https://forums.x-plane.org/forums/topic/302313-linux-standalone-skunkcrafts-updater-requires-glibc-232-or-higher/)
- [openSAM SkunkCrafts Integration — GitHub](https://github.com/hotbso/openSAM)
