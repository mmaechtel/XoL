# X-Plane 12 Interfaces & APIs — Research Summary

**Datum:** 2026-02-21
**Scope:** All programmatic and file-based interfaces for X-Plane 12 (Stand: SDK 4.2.0, X-Plane 12.4.0)
**Verwendung:** Hintergrund für intro.md, künftige API/SDK-Doku, Addon-Seiten

---

## 1. XPLM Plugin SDK

X-Plane's Plugin SDK is the primary extension mechanism. Plugins are compiled shared libraries (`.xpl` = renamed `.so`/`.dll`/`.dylib`) loaded in-process.

**SDK 4.2.0** (October 2025, requires X-Plane 12.3.0+) — 21 API modules:

| Module | Purpose |
|--------|---------|
| XPLMCamera | Custom camera control |
| XPLMDataAccess | DataRef read/write/creation |
| XPLMDisplay | Windows, drawing callbacks, key sniffing |
| XPLMGraphics | OpenGL state, texture loading, coordinate conversion |
| XPLMInstance | GPU-instanced object placement |
| XPLMMap | Map layer rendering |
| XPLMMenus | Plugin menus in X-Plane menubar |
| XPLMNavigation | Navaid database queries, FMS manipulation |
| XPLMPlanes | Aircraft loading, positioning, TCAS |
| XPLMPlugin | Plugin lifecycle, inter-plugin messaging |
| XPLMProcessing | Flight loop callbacks at configurable intervals |
| XPLMScenery | Terrain probing, object loading, library lookup |
| XPLMSound | FMOD-based 3D audio (SDK 4.0+) |
| XPLMUtilities | Commands, file paths, system info, error reporting |
| XPLMWeather | Weather data queries (experimental, SDK 4.0+) |
| XPLMAvionics | Custom avionics devices (SDK 4.1+) |
| XPWidgets | UI widget system (legacy) |
| XPWidgetDefs | Widget type definitions |
| XPWidgetUtils | Widget helper functions |
| XPStandardWidgets | Pre-built UI widgets |
| XPLMUI | Plugin preferences dialogs |

**Key constraints:**
- In-process only — no external process access via SDK
- Plugins run on X-Plane's main thread (flight loop callbacks)
- SDK 4.0+ (XP 12.0): XPLMSound (FMOD), XPLMWeather
- SDK 4.1 (XP 12.1): XPLMAvionics (custom avionics devices)
- SDK 4.2 (XP 12.3): DataRef introspection (XPLM400)

Sources:
- [X-Plane Developer — SDK Documentation](https://developer.x-plane.com/sdk/)
- [X-Plane Developer — Developing Plugins](https://developer.x-plane.com/article/developing-plugins/)

---

## 2. DataRefs

Callback-driven shared variable system — the central interface for reading and controlling simulator state.

- **~5,225** built-in `sim/` DataRefs, **~7,000** at runtime (including plugin-defined)
- Types: int, float, double, int array, float array, byte array
- Callback-based: reading/writing triggers getter/setter functions, not direct memory access
- Accessible by path string (e.g., `sim/cockpit2/gauges/indicators/airspeed_kts_pilot`)

**XPLM400 introspection** (SDK 4.2, XP 12.3+):
```c
int XPLMCountDataRefs(void);
XPLMDataRef XPLMGetDataRefsByIndex(int offset);
XPLMGetDataRefInfo(XPLMDataRef ref, ...);  // returns name, type, writable, owner plugin
```
Enables runtime enumeration of all DataRefs without a lookup file.

**Discovery tools:**
- DataRefTool (plugin): Interactive browser with search, filtering, type display
- DataRefEditor: Older alternative
- `DataRefs.txt` in aircraft folders: Documents custom aircraft DataRefs

Sources:
- [X-Plane Developer — DataRef documentation](https://developer.x-plane.com/datarefs/)
- [X-Plane Developer — XPLMDataAccess SDK](https://developer.x-plane.com/sdk/XPLMDataAccess/)
- [DataRefTool — GitHub](https://github.com/leecbaker/datareftool)

---

## 3. Commands

Action/event system for triggering simulator operations.

- **~2,816** built-in commands
- Three-phase model: Begin → Continue → End
- Plugins can create custom commands and intercept existing ones
- Preferred over writable DataRefs for triggering actions

```c
XPLMCommandRef XPLMFindCommand(const char *inName);
void XPLMCommandOnce(XPLMCommandRef inCommand);
void XPLMCommandBegin(XPLMCommandRef inCommand);
void XPLMCommandEnd(XPLMCommandRef inCommand);
```

Sources:
- [X-Plane Developer — Commands documentation](https://developer.x-plane.com/datarefs/)
- [X-Plane Developer — XPLMUtilities SDK](https://developer.x-plane.com/sdk/XPLMUtilities/)

---

## 4. Built-in Web API (since 12.1.1)

HTTP/WebSocket server on `localhost:8086`. First official mechanism for external process access without plugins.

**API versions:**

| Version | X-Plane | Capabilities |
|---------|---------|-------------|
| v1 | 12.1.1 (Jul 2024) | DataRef read/write, listing, filtering |
| v2 | ~12.2 | + Command listing and activation |
| v3 | 12.4.0 (Dec 2025) | + Flight initialization, config updates |

**REST:** `http://localhost:8086/api/v3` — JSON, requires `Accept: application/json`
**WebSocket:** `ws://localhost:8086/api/v3` — JSON messages with `req_id`, `type`, `params`. 10 Hz DataRef streaming.

**Critical limitation:** Localhost only — no LAN access. Laminar plans authorization model for future remote access.

**Configuration:** Port configurable via `--web_server_port=`. Disable with `--no_web_server`.

Sources:
- [X-Plane Developer — X-Plane Web API](https://developer.x-plane.com/article/x-plane-web-api/) (updated January 2026)
- [X-Plane Developer Blog — Webservers, Documentation, and Terrible Titles (July 2024)](https://developer.x-plane.com/2024/07/webservers-documentation-and-terrible-titles/)

---

## 5. UDP Protocol

Legacy binary protocol, oldest external interface. **Disabled by default in XP12** (must enable in Settings > Network).

**Ports (hard-coded):**
- 49000 — receive (inbound)
- 49001 — send (outbound)
- 49707 — multicast beacon (LAN discovery)

**Packet format:** 5-byte header (4 ASCII chars + 1 index byte), little-endian, 4-byte aligned.

**Key message types:** DATA (flight data rows), DREF (set DataRef), RREF (subscribe to DataRef), CMND (execute command), RPOS (position updates), CHAR (simulate keypress), VEH1/VEHA (aircraft control).

**Also used for:** Network rendering (external visuals, master/slave multi-computer setups).

Sources:
- [Nuclear Projects — X-Plane UDP Reference](http://www.nuclearprojects.com/xplane/xplaneref.html)
- [X-Plane Support — Using Networked Multiplayer, External Visuals & Apps](https://x-plane.helpscoutdocs.com/article/34-using-networked-multiplayer-external-visuals-apps)

---

## 6. Scripting Frameworks

In-process scripting via embedded interpreters (all wrap the XPLM SDK):

| Framework | Language | Developer | License | Scope |
|-----------|----------|-----------|---------|-------|
| FlyWithLua NG+ | Lua (LuaJIT) | X-Friese | Open source | User scripts, global |
| XPPython3 | Python 3 | pbuckner | Open source | Full SDK access from Python |
| XLua | Lua 5.1 | Laminar Research | MIT | Aircraft-scoped, minimal |
| SASL v3 | Lua | 1-sim.com | Commercial | Aircraft avionics framework |

**FlyWithLua** is the most widely used. Scripts in `Resources/plugins/FlyWithLua/Scripts/`. Full DataRef/command access, OpenGL drawing, floating windows.

**XLua** is Laminar's own minimal scripting. Designed for art-team use. Independent modules per aircraft.

**SASL** is a commercial aircraft development framework with UI components, sound, particles, DRM.

Sources:
- [GitHub — X-Friese/FlyWithLua](https://github.com/X-Friese/FlyWithLua)
- [GitHub — X-Plane/XLua](https://github.com/X-Plane/XLua)
- [1-sim.com — SASL](https://1-sim.com/)

---

## 7. Third-Party Bridge Tools

Bridge plugins expose SDK functionality to external processes:

| Tool | Protocol | Port | Plugin Required | XP12 Status |
|------|----------|------|-----------------|-------------|
| ExtPlane | Text TCP | 51000 | Yes | Likely compatible |
| NASA XPlaneConnect | Binary UDP | Dynamic | Yes | Known issues |
| XPlaneConnectX | UDP | 49000/01 | No (uses built-in UDP) | Built for XP12 |
| SPAD.neXt | Proprietary | — | Yes | Supported |

**ExtPlane** is the simplest: connect to TCP 51000, text commands (`sub`, `set`, `get`, `cmd`).

**XPlaneConnectX** (Stanford SISL) requires no plugin — uses X-Plane's native UDP. Python 3 and Julia libraries. Tested on XP 12.1 across Win/Mac/Ubuntu.

Sources:
- [GitHub — vranki/ExtPlane](https://github.com/vranki/ExtPlane)
- [GitHub — nasa/XPlaneConnect](https://github.com/nasa/XPlaneConnect)
- [GitHub — sisl/XPlaneConnectX](https://github.com/sisl/XPlaneConnectX)

---

## 8. Scenery File Formats

### Core Formats

| Format | Extension | Purpose |
|--------|-----------|---------|
| DSF | `.dsf` | 1°×1° terrain tiles (binary, chunked) |
| OBJ8 | `.obj` | 3D scenery objects (text-based) |
| apt.dat | `apt.dat` | Airport infrastructure (text, spec 1200) |
| library.txt | `library.txt` | Virtual path mapping for shared resources |
| scenery_packs.ini | `scenery_packs.ini` | Scenery load order (top = highest priority) |
| Terrain Type | `.ter` | Texture mapping + physical terrain properties |
| Facade | `.fac` | Extruded building definitions |
| Forest | `.for` | Vegetation placement rules |
| Draped Polygon | `.pol` | Flat polygons on terrain |
| Painted Line | `.lin` | Taxiway/road markings |
| Vector Network | `.net` | Road/path rendering |
| Autogen Block | `.agb` | Procedural building blocks |
| Autogen String | `.ags` | Procedural building strings |

### DSF Structure

- 12-byte header (`XPLNEDSF` + version), chunked atoms, MD5 footer
- Two types: Base Mesh (terrain foundation) and Overlay (`sim/overlay: 1`, objects/polygons)
- XP12 additions: seasonal raster layers, polygonal exclusion zones, bathymetric depth, `WATER_COLOR_MASK`

### OBJ8

- Right-handed coordinate system (+Y up, +X east, +Z south), meters
- LOD: selective (one at a time) or additive (progressive)
- Animation: DataRef-driven (`ANIM_rotate`, `ANIM_trans`, `ANIM_hide/show`)
- XP12: PBR material model (Disney/UE4 standard), rain/wiper/thermal textures

### Navigation Data

| File | Content | Spec Version |
|------|---------|-------------|
| earth_nav.dat | VORs, NDBs, ILS | XPNAV1150/1200 |
| earth_fix.dat | Enroute/terminal fixes | XPFIX1200 |
| earth_awy.dat | Airway segments | XPAWY1101 |
| earth_hold.dat | Holding patterns | XPHOLD1140 |
| CIFP/*.dat | Instrument procedures | ARINC 424 |

**Override hierarchy:** Resources/default data → Custom Data → Global Airports → user_fix.dat/user_nav.dat

### Scenery Library System

`library.txt` maps local files to virtual paths:
- `EXPORT` — replacement (blocks lower priority)
- `EXPORT_EXTEND` — additive (merges)
- `EXPORT_BACKUP` — fallback only
- `EXPORT_SEASON` — seasonal variants (XP 1200+)
- Regional filtering: `REGION_RECT`, `REGION_BITMAP`, `REGION_DREF`

### XPLMScenery API (Plugin Access)

- `XPLMProbeTerrainXYZ()` — terrain probing (height, normal, is_wet)
- `XPLMLoadObject()` / `XPLMLoadObjectAsync()` — object loading
- `XPLMLookupObjects()` — library query by virtual path + location
- No public API for texture loading — reason why streaming tools use FUSE

### Scenery Streaming (Third-Party)

X-Plane has no native scenery streaming. AutoOrtho and XEarthLayer use FUSE virtual filesystems to intercept DDS texture reads and stream satellite imagery on-demand. DDS mipmaps enable progressive resolution loading.

**Laminar's direction:** Transition to raster-based meshes (announced 2024), which would make streaming architecturally more natural. No timeline.

Sources:
- [DSF File Format Specification](https://developer.x-plane.com/article/dsf-file-format-specification/)
- [OBJ8 File Format Specification](https://developer.x-plane.com/article/obj8-file-format-specification/)
- [Airport Data (apt.dat) 12.00 Specification](https://developer.x-plane.com/article/airport-data-apt-dat-12-00-file-format-specification/)
- [Library (library.txt) File Format Specification](https://developer.x-plane.com/article/library-library-txt-file-format-specification/)
- [Terrain Type (.ter) File Format Specification](https://developer.x-plane.com/article/terrain-type-ter-file-format-specification/)
- [XPLMScenery API Reference](https://developer.x-plane.com/sdk/XPLMScenery/)
- [Navdata in X-Plane 11 and 12](https://developer.x-plane.com/article/navdata-in-x-plane-11/)

---

## 9. Input & Tracking

### Joystick/HID
- USB HID directly, no separate API
- `.joy` config files: plain text, device mapping by name or VID:PID
- Linux: joystick/evdev subsystem, udev rules often needed

### Head Tracking
- Windows: native TrackIR (proprietary)
- Linux: OpenTrack → UDP port 4242 → HeadTrack plugin (6DOF data)
- VR: separate OpenXR/SteamVR pipeline

Sources:
- [X-Plane Developer — Joystick Configuration (.joy) File Specification](https://developer.x-plane.com/article/creating-joystick-configuration-joy-files/)

---

## 10. Replay / FDR

- `.rep` — native replay (binary, undocumented)
- `.fdr` — Flight Data Recorder (plain text, semi-documented, 88+ columns)
- `.sit` — situation snapshots (minimal docs)
- No public replay API; plugins can read `sim/operation/replay/*` DataRefs

Sources:
- [X-Plane KB — Creating FDR Files](https://www.x-plane.com/kb/creating-fdr-files/)

---

## Interface Summary Table

| Interface | Type | Protocol | Access | XP12 Status |
|-----------|------|----------|--------|-------------|
| XPLM SDK | In-process | C API | Plugin only | SDK 4.2.0 |
| DataRefs | In-process | Callback | Plugin/scripting | ~5,225 built-in |
| Commands | In-process | Event | Plugin/scripting | ~2,816 built-in |
| Web API | Built-in | HTTP/WS/JSON | External (localhost) | Since 12.1.1 |
| UDP | Built-in | Binary UDP | External (LAN) | Disabled by default |
| FlyWithLua | Plugin | Lua | Scripts | NG+ for XP12 |
| XPPython3 | Plugin | Python | Scripts | Full SDK binding |
| ExtPlane | Plugin | Text TCP:51000 | External | Compatible |
| DSF/OBJ8/apt.dat | File | Binary/text | Tools | Spec 1200 |
| scenery_packs.ini | File | Text | User config | Standard |
| .joy | File | Text | User config | Standard |
