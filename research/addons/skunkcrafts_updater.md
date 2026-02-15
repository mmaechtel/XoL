# SkunkCrafts Updater — Research Paper

**Date:** 2026-02-15
**Status:** Recherche abgeschlossen
**Sources:** Primary sources only (GitHub repos, forums.x-plane.org, developer sites)

---

## 1. What It Is

The SkunkCrafts Updater is a free, closed-source update management tool for X-Plane addons. It scans the user's X-Plane installation for addons that ship with SkunkCrafts configuration files, checks their versions against remote repositories, and downloads/applies updates automatically.

**Developer:** Lionel Zamouth, founder of SkunkCrafts. Zamouth also works at Aerobask (aircraft systems and avionics). SkunkCrafts was originally started as a side venture for addon projects Aerobask was not interested in developing.

**License:** Freeware / closed-source. The updater is available as a free download. No public source code repository exists for the updater itself. The protocol and file format are open (documented on forums, reverse-engineered by third parties).

**Official website:** https://skunkcrafts.com/ (currently shows "Fine aircrafts for X-Plane 11", appears to be under construction/outdated)

**Forum home:** https://forums.x-plane.org/forums/forum/406-skunkcrafts-updater/

### Sources

- Developer identity: [Threshold interview with Lionel Zamouth](https://www.thresholdx.net/article/intlio)
- Forum section: [forums.x-plane.org/forums/forum/406-skunkcrafts-updater/](https://forums.x-plane.org/forums/forum/406-skunkcrafts-updater/)
- Standalone announcement: [Threshold article](https://www.thresholdx.net/news/skwrks)

---

## 2. Current Status (2025/2026)

### Latest Version: Standalone Client v3.2d

- **Release date:** 2025-02-06
- **Forum thread:** https://forums.x-plane.org/forums/topic/292710-20250206-skunkcrafts-updater-standalone-client-v32d-available/
- The thread has 500+ replies and 149k+ views, indicating active community usage.
- As of 2026-02-15, no v3.3 or newer version has been found in search results. v3.2d appears to be the current release.

### Version History

| Version | Date | Notes |
|---------|------|-------|
| v2.x | pre-2023 | Original in-game plugin (X-Plane plugin, .xpl format) |
| v3.0 | 2023-08 | Complete rewrite as standalone desktop app (Go + Fyne UI) |
| v3.2d | 2025-02-06 | Latest known release |

### Development Status

- **Actively maintained** as of early 2025.
- All future development focuses on the standalone version; the in-game plugin is legacy.
- The standalone client is fully backward-compatible with existing v2.x addon repositories.

### Sources

- v3.2d release: [forums.x-plane.org thread](https://forums.x-plane.org/forums/topic/292710-20250206-skunkcrafts-updater-standalone-client-v32d-available/)
- v3.0 announcement: [XPlaneReviews forum](https://xplanereviews.com/forums/topic/12385-new-skunkcrafts-standalone-updater-client-v30/)

---

## 3. How It Works — Technical Mechanism

### Architecture

The standalone v3.x client is:

- **Written in Go** with the **Fyne** UI library (cross-platform GUI toolkit)
- Concurrent download engine supporting up to **32 simultaneous downloads** (configurable)
- Runs as an independent desktop application outside X-Plane (no X-Plane SDK dependency)

### Update Protocol (Reconstructed from Open Repositories)

The update mechanism is file-based and uses a set of plain-text control files with a pipe-delimited format (`key|value`). The system works as follows:

#### Client-Side Files (shipped with each addon)

Each addon that supports SkunkCrafts Updater includes a `skunkcrafts_updater.cfg` file in its root directory. Example:

```ini
zone|custom
liveries|false
module|https://raw.githubusercontent.com/hotbso/openSAM/refs/heads/release/release/XP12/openSAM/
version|v1.2.3
disabled|false
name|openSAM XP12
locked|false
```

**Fields:**

| Field | Purpose |
|-------|---------|
| `zone` | `custom` = use `module` as full URL; otherwise, a directory name on a default server |
| `module` | Base URL of the remote repository containing update files |
| `name` | Display name shown in the updater UI |
| `version` | Currently installed version string |
| `disabled` | `true`/`false` — whether this entry is active |
| `locked` | `true`/`false` — whether updates are locked (maintenance mode) |
| `liveries` | `true`/`false` — whether this module includes liveries |

A second file `skunkcrafts_updater_beta.cfg` can optionally provide a separate beta channel with the same format but pointing to a different branch/URL.

#### Server-Side Files (hosted by the addon developer)

The remote repository (pointed to by `module` URL) contains these control files:

| File | Format | Purpose |
|------|--------|---------|
| `skunkcrafts_updater_config.txt` | `key\|value` | Remote version info (zone, module, name, version, locked) |
| `skunkcrafts_updater_whitelist.txt` | `filename\|crc32` | CRC32 checksums (unsigned 32-bit decimal) for all distributed files |
| `skunkcrafts_updater_sizeslist.txt` | `filename\|bytes` | File sizes in bytes for all distributed files |
| `skunkcrafts_updater_blacklist.txt` | `filename` | Files to delete on the client (one per line) |
| `skunkcrafts_updater_oncelist.txt` | `filename` | Files to download only once (never overwrite user modifications) |
| `skunkcrafts_updater_ignorelist.txt` | `filename` | Files to ignore during update checking |

#### Update Process

1. **Discovery:** The updater scans all directories under the X-Plane root for `skunkcrafts_updater.cfg` files
2. **Version check:** For each discovered addon, the updater fetches `skunkcrafts_updater_config.txt` from the remote `module` URL and compares the `version` field
3. **Integrity check:** If versions differ, the updater downloads the remote `skunkcrafts_updater_whitelist.txt` and `skunkcrafts_updater_sizeslist.txt`, then compares CRC32 checksums and file sizes against local files
4. **Differential download:** Only files that differ (wrong CRC32, wrong size, or missing) are downloaded
5. **Cleanup:** Files listed in `skunkcrafts_updater_blacklist.txt` are deleted locally
6. **Protection:** Files in `skunkcrafts_updater_ignorelist.txt` are skipped; files in `skunkcrafts_updater_oncelist.txt` are only downloaded if they do not already exist locally

### Developer Integration

Addon developers integrate by:

1. Creating a remote repository (GitHub, own web server, etc.) hosting the addon files and control files
2. Shipping a `skunkcrafts_updater.cfg` in the addon's root directory pointing to that repository
3. Generating the whitelist (CRC32) and sizeslist on each release

Several open-source tools exist for generating the server-side files:

- **Parcel** (Python, Apache 2.0): https://github.com/slimit75/Parcel — "UNOFFICIAL file generator for the Skunkcrafts Updater"
- **skunkcrafts_file_generator.py** in [FollowTheGreens](https://github.com/devleaks/followthegreens) — generates whitelist, sizeslist, and cfg
- **GitHub Actions integration** — multiple projects automate SkunkCrafts file generation in CI/CD (openSAM, XTouchDownRecorder, Magknight B787)

#### Hosting Patterns

Common hosting approaches found in real-world repos:

| Pattern | Example |
|---------|---------|
| GitHub raw content from release branch | `https://raw.githubusercontent.com/hotbso/openSAM/refs/heads/release/...` |
| GitHub raw content from main branch | `https://raw.githubusercontent.com/devleaks/followthegreens/refs/heads/main` |
| Gitee (for Chinese mirror) | `https://gitee.com/cpuwolf/XTouchDownRecorder/raw/release/release` |
| Custom web server | `https://ramonster.nl/winctrl-plugin` |
| Developer's own server | `http://updates.simcoders.com/release/PA18/` |

### Sources

- openSAM cfg template + CI: [github.com/hotbso/openSAM release.yaml](https://github.com/hotbso/openSAM/blob/main/.github/workflows/release.yaml)
- SGES update repo (complete file set): [github.com/GitHubJavelin/sges-updates](https://github.com/GitHubJavelin/sges-updates)
- Mission-X cfg templates: [github.com/snagar/mx-random-scenery](https://github.com/snagar/mx-random-scenery)
- XTouchDownRecorder CI: [github.com/cpuwolf/XTouchDownRecorder release.yml](https://github.com/cpuwolf/XTouchDownRecorder/blob/main/.github/workflows/release.yml)
- Parcel tool: [github.com/slimit75/Parcel](https://github.com/slimit75/Parcel)
- FollowTheGreens generator: [github.com/devleaks/followthegreens skunkcrafts_file_generator.py](https://github.com/devleaks/followthegreens)
- Magknight acf-action: [github.com/magknight/acf-action](https://github.com/magknight/acf-action)
- WINCTRL build script: [github.com/rswilem/winctrl-xplane-plugin](https://github.com/rswilem/winctrl-xplane-plugin)

---

## 4. Installation on Linux

### Standalone Client (v3.x)

The standalone client is distributed as a single executable file per platform:

| Platform | File Extension | Notes |
|----------|---------------|-------|
| Windows 10/11 | `.exe` | |
| macOS (Intel + Apple Silicon) | `.app` | Universal binary |
| GNU/Linux | `.lin` | Tested on Ubuntu 22.04 |

**Installation steps (Linux):**

1. Download the zip archive from the X-Plane.org forum thread
2. Extract the `.lin` executable file
3. Place it in the **X-Plane root folder** (the directory containing `X-Plane-x86_64`)
4. Make it executable: `chmod +x SkunkCrafts_Updater*.lin` (exact filename may vary)
5. Run it from the X-Plane root folder

**Important:** The updater must be launched from the X-Plane root directory. It scans subdirectories relative to its own location to discover addon cfg files.

### Legacy Plugin (v2.x)

The original plugin was an X-Plane plugin (`.xpl` format) placed in `Resources/plugins/SkunkCraftsUpdater/`. It ran within X-Plane and required X-Plane to be running for updates. This version is legacy and no longer actively developed.

### glibc Requirement

The standalone Linux binary requires **glibc 2.32 or higher**. This is a known issue documented on the forums:

- **Forum thread:** https://forums.x-plane.org/forums/topic/302313-linux-standalone-skunkcrafts-updater-requires-glibc-232-or-higher/
- **Affected distros:** Ubuntu 20.04 (glibc 2.31), Debian 10 Buster (glibc 2.28)
- **Not affected:** Ubuntu 22.04+ (glibc 2.35), Debian 11 Bullseye+ (glibc 2.31 — borderline), Debian 12 Bookworm (glibc 2.36)

This is a consequence of the Go + Fyne build environment; Go binaries with CGo dependencies (Fyne uses CGo for GUI rendering) link against the build system's glibc.

**Note:** The openSAM project explicitly uses `ubuntu-22.04` as their CI build runner with the comment "use oldest possible ubuntu version in order to avoid compatibility errors with libc" — this is a known pattern for X-Plane Linux builds.

### Sources

- glibc issue: [forums.x-plane.org/forums/topic/302313](https://forums.x-plane.org/forums/topic/302313-linux-standalone-skunkcrafts-updater-requires-glibc-232-or-higher/)
- Installation guide: [X-Crafts guide](https://www.xcrafts.com/how-to-update-download-new-version)
- openSAM CI glibc note: [github.com/hotbso/openSAM release.yaml](https://github.com/hotbso/openSAM/blob/main/.github/workflows/release.yaml)

---

## 5. Addons That Use SkunkCrafts Updater

### Confirmed Users (from primary sources)

| Developer | Products | Source |
|-----------|----------|--------|
| **Aerobask** | Various aircraft (Phenom 300, etc.) | Developed alongside Aerobask ([Threshold](https://www.thresholdx.net/news/skwrks)) |
| **X-Crafts** | E-Jets Family, ERJ Family | [xcrafts.com](https://www.xcrafts.com/how-to-update-download-new-version) |
| **SimCoders** | Reality Expansion Pack (REP) for multiple aircraft | [simcoders.com](https://www.simcoders.com/faqs/how-do-i-update-my-rep-using-the-skunkcrafts-updater-plugin/) |
| **VSKYLABS** | Various aircraft (DC-3, etc.) | [vskylabs.com](https://www.vskylabs.com/install-and-update/) |
| **JetStream FS** | CIS Seneca II | [jetstreamfs.com](https://www.jetstreamfs.com/skunkcrafts-updater/) |
| **Stick and Rudder Studios** | X-Camera, X-ATC-Chatter, X-KeyPad | [stickandrudderstudios.com](https://stickandrudderstudios.com/updating-with-the-skunkcrafts-standalone-updater/) |
| **Magknight** | 787 Aviator's Edition | [docs.magknight.org](https://docs.magknight.org/faq/) |
| **Just Flight** | 146 Professional, Pilatus PC-6 Turbo Porter, others | [community.justflight.com](https://community.justflight.com/topic/8162/146-professional-xp12-not-showing-on-skunkcrafts-updater), [support.justflight.com](https://support.justflight.com/support/solutions/articles/17000116042-how-will-future-updates-be-managed-for-this-aircraft-) |
| **FlyJSim** | 737-200 (732) | [flyjsim.com](https://www.flyjsim.com/patch-notes-732) |
| **Rotate** | MD-80 (v1.50+) | [forums.x-plane.org](https://forums.x-plane.org/forums/topic/288666-skunkcrafts-updater-configuration-files-for-rotate-md-80v150-and-up/) |
| **hotbso (open source)** | openSAM | [github.com/hotbso/openSAM](https://github.com/hotbso/openSAM) |
| **devleaks (open source)** | FollowTheGreens | [github.com/devleaks/followthegreens](https://github.com/devleaks/followthegreens) |
| **cpuwolf (open source)** | XTouchDownRecorder | [github.com/cpuwolf/XTouchDownRecorder](https://github.com/cpuwolf/XTouchDownRecorder) |
| **GitHubJavelin (open source)** | Simple Ground Equipment & Services | [github.com/GitHubJavelin/sges-updates](https://github.com/GitHubJavelin/sges-updates) |
| **rswilem (open source)** | WINCTRL | [github.com/rswilem/winctrl-xplane-plugin](https://github.com/rswilem/winctrl-xplane-plugin) |
| **X-Aerodynamics** | Cessna-172, B58 Baron | [forums.x-plane.org](https://forums.x-plane.org/forums/topic/324915-new-updates-and-features-for-cessna-172-and-b58-baron-january-2025/) |

This is not an exhaustive list. The SkunkCrafts Updater is the de facto standard update mechanism in the X-Plane addon ecosystem. Dozens of commercial and freeware addons use it.

---

## 6. Configuration Reference

### Main Config: `skunkcrafts_updater.cfg`

Placed in the addon's root directory. Pipe-delimited key-value format.

```
zone|custom
liveries|false
module|https://example.com/path/to/repo/
version|1.2.3
disabled|false
name|My Addon Name
locked|false
```

### Beta Config: `skunkcrafts_updater_beta.cfg`

Same format as above, typically pointing to a different branch or URL for beta releases.

### Server-Side Control Files

All placed at the `module` URL root:

| File | Format | Description |
|------|--------|-------------|
| `skunkcrafts_updater_config.txt` | `key\|value` | Authoritative version + metadata (server-side mirror of cfg) |
| `skunkcrafts_updater_whitelist.txt` | `path\|crc32_decimal` | CRC32 checksums for integrity verification |
| `skunkcrafts_updater_sizeslist.txt` | `path\|size_bytes` | File sizes for download progress |
| `skunkcrafts_updater_blacklist.txt` | `path` | Files to remove from client on update |
| `skunkcrafts_updater_oncelist.txt` | `path` | Files to install only once (preserve user modifications) |
| `skunkcrafts_updater_ignorelist.txt` | `path` | Files to ignore during update checking |

### CRC32 Format

The CRC32 values are **unsigned 32-bit integers in decimal representation**. Example from the FollowTheGreens generator:

```python
crc = binascii.crc32(buf) & 0xFFFFFFFF  # ensure unsigned
files[f] = {"crc32": f"{crc:d}"}         # decimal string
```

From shell scripts (openSAM, XTouchDownRecorder):

```bash
checksum_hex=$(crc32 "$file")
checksum_decimal=$((16#${checksum_hex}))  # hex to decimal
echo "$filename|$checksum_decimal"
```

### Standalone Client Settings

The standalone client has its own settings (separate from per-addon cfg files):

- Concurrent downloads: 1-32 (configurable in UI)
- Text size: configurable in UI
- Beta mode: toggle in UI (switches between release/beta repositories)

---

## 7. Known Issues on Linux

### glibc 2.32+ Requirement

**Impact:** The standalone client binary does not run on systems with glibc < 2.32.

- **Debian 11 Bullseye:** glibc 2.31 — may fail (borderline)
- **Debian 12 Bookworm:** glibc 2.36 — works
- **Ubuntu 20.04:** glibc 2.31 — fails
- **Ubuntu 22.04:** glibc 2.35 — works (officially tested platform)

**Source:** https://forums.x-plane.org/forums/topic/302313-linux-standalone-skunkcrafts-updater-requires-glibc-232-or-higher/

### File Permissions

The downloaded `.lin` binary may not have the execute bit set after extraction. Users need to run `chmod +x` before first launch. This is a standard Linux issue not specific to SkunkCrafts.

### Fyne UI on Wayland

The Fyne UI toolkit (used by the standalone client) has varying support for Wayland. Fyne supports Wayland through its Go bindings but may fall back to XWayland. No specific bug reports were found for SkunkCrafts on Wayland, but this is worth noting for Wayland-only setups.

### No GUI Dependencies Documented

The official documentation does not list required GUI libraries. As a Fyne/Go application, it likely requires:

- OpenGL support (Fyne uses OpenGL for rendering)
- Standard X11 or Wayland libraries
- The exact dependencies are not documented by the developer

### X-Plane Must Be Closed (Legacy Plugin Only)

The legacy v2.x plugin version required X-Plane to be closed when updating the currently loaded aircraft. The standalone v3.x version eliminates this restriction — users no longer need to close X-Plane or unload aircraft.

---

## 8. Alternatives

### FlightFactor X-Updater

- **URL:** https://x-updater.com/ / https://x-updater.readthedocs.io/
- **Developer:** StepToSky (used by FlightFactor)
- **Technology:** Java-based (requires Java 8 runtime)
- **Scope:** Primarily for FlightFactor aircraft (A320 Ultimate, 757, 767, 777)
- **Launch:** 2018 — the first major addon updater in the X-Plane ecosystem
- **Mechanism:** Scans local files, compares with developer file list, downloads missing/changed files
- **Status:** Still in use for FlightFactor products
- **Source:** [forums.x-plane.org](https://forums.x-plane.org/forums/topic/274482-x-updater-tutorial-how-to-install-and-update-your-ff-aircraft/), [x-updater.readthedocs.io](https://x-updater.readthedocs.io/)

### inSim Plugin Updater

- **URL:** https://x-plane.joanpc.com/plugins/insim-plugin-updater
- **Developer:** joanpc
- **Technology:** X-Plane plugin (runs inside X-Plane)
- **Scope:** General plugin updater, accessible via Plugins menu
- **Mechanism:** In-game menu for discovering, installing, and updating plugins
- **Limitation:** Runs inside X-Plane (not standalone)

### Developer-Specific Update Systems

Some developers maintain their own update mechanisms:

- **ToLiss:** Uses its own SimBrief-integrated updater system
- **X-Plane.org Store:** Manual re-download from the store for purchased products
- **Steam Workshop:** For Steam-distributed addons (limited X-Plane support)

### Addon Managers (Broader Scope)

These are addon management tools, not update-only tools:

- **XFast-Manager** (https://github.com/CCA3370/XFast-Manager): Tauri-based (Rust + Web), modern addon installer/manager with scenery management, livery management, and DSF overlap detection. Actively developed (v0.8.11 as of 2026-02-13). Mentions SkunkCrafts Updater compatibility in its changelog.
- **XAddonManager** (https://forums.x-plane.org/files/file/4886-xaddonmanager/): Utility for managing X-Plane addons (scenery, plugins, aircraft, CSLs). Focuses on installation and organization rather than updates.

### Key Comparison

| Tool | Type | Platform | Standalone | Open Protocol |
|------|------|----------|------------|---------------|
| SkunkCrafts Updater | Addon updater | Win/Mac/Linux | Yes (v3.x) | Yes |
| FlightFactor X-Updater | Addon updater | Win/Mac/Linux (Java) | Yes | No |
| inSim | Plugin updater | Inside X-Plane | No | Unknown |
| XFast-Manager | Addon manager | Win/Mac/Linux | Yes | N/A |

SkunkCrafts Updater has the widest adoption by far. Its open protocol allows any developer to integrate without coordination with the updater developer.

---

## 9. Summary and Assessment for Documentation

### Relevance for XoL (X-Plane on Linux)

**High relevance.** The SkunkCrafts Updater is the most widely used addon update mechanism in the X-Plane ecosystem. Linux users need to know:

1. How to install and run the standalone client on Linux
2. The glibc requirement and which distros are compatible
3. That `chmod +x` is needed after download
4. That no specific Linux configuration is needed — the cfg files are platform-independent

### Documentation Approach

The addon page should cover:

- What it is and why it matters (de facto standard for addon updates)
- Linux installation (standalone only, not the legacy plugin)
- Known Linux issues (glibc, permissions)
- Brief explanation of the cfg format (useful for troubleshooting)
- Link to the forum for downloads

### Information Stability

- The update protocol is stable and has been backward-compatible across v2.x to v3.x
- The cfg format is well-established with no changes expected
- The glibc requirement may change with future builds
- Version numbers will change but the mechanism will not

### What NOT to Include

- Detailed developer integration guide (not relevant for end users)
- Complete list of supported addons (changes constantly)
- FlightFactor X-Updater details (separate ecosystem, not broadly relevant)
