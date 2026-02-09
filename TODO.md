# XoL — Offene Dokumentationsthemen

Workflow und Phasen-Beschreibung: siehe `CLAUDE.md` → Dokumentations-Workflow.

---

## Übersicht

| Prio | Datei | Status | Thema |
|------|-------|--------|-------|
| 1 | `xplane/config.md` | **geprüft** | X-Plane Konfiguration (Linux-Spezifika) |
| 2 | `mesa.md` | offen | AMD/Intel GPU-Treiber (Mesa, RADV, Vulkan) |
| 3 | `input_devices.md` | offen | Joystick, Throttle, Ruderpedal unter Linux |
| 4 | `wayland.md` | offen | Display-Server-Wahl für X-Plane |
| 5 | `audio.md` | offen | PipeWire/PulseAudio für X-Plane |
| 6 | `multi_monitor.md` | offen | Multi-Monitor und Netzwerk-Rendering |
| 7 | `xplane/plugins.md` | offen | Plugin-Verwaltung unter Linux |
| 8 | `kvm.md` | offen | WiP-Abschnitt ausbauen oder entfernen |

---

## Abgeschlossene Themen

### 1. `xplane/config.md` — X-Plane Konfiguration (Überarbeitung)

**Status:** geprüft

**Ergebnis:** Komplett neu geschrieben mit Fokus auf Linux-Spezifika. Vulkan/Zink, Shader-Cache, Mesa-Umgebungsvariablen, Display-Server, Audio, Controller, szenariobasierte CLI-Fehlerbehebung, GPU-Debugging. Akademische Hintergrundtexte (AA, PBR) als klappbare Blöcke. Faktencheck gegen Primärquellen durchgeführt, versionsspezifische Informationen bereinigt.

**Research-Papers:**

- `research/XPlane12_Konfiguration_Linux_Spezifika.md`
- `research/LEKTORAT_config_md.md`
- `research/xplane-help.out` (X-Plane CLI-Referenz)

---

## Offene Themen

### 2. `mesa.md` — Mesa/AMD/Intel Grafiktreiber

**Nav-Position:** Linux > Optimierungen (nach nvidia.md)

**Unterthemen:** Mesa als Open-Source-Grafikstack, RADV/ANV Vulkan-Treiber, Treiberversionen (Debian Stable vs. Backports vs. kisak-mesa), Vulkan ICD-Auswahl, RADV vs. AMDVLK, AMD Power Profile/Undervolting, Intel Arc Support, Performance-Monitoring (radeontop, intel_gpu_top), Fehlerbehebung

---

### 3. `input_devices.md` — Eingabegeräte unter Linux

**Nav-Position:** Linux > Erweiterungen

**Unterthemen:** evdev/udev-System, SDL2 Game Controller API, Geräteerkennung (lsusb, evtest, jstest-gtk), Linux-seitige Kalibrierung, udev-Regeln für persistente Zuordnung, bekannte Hardware (Thrustmaster, VKB, Virpil), USB-Autosuspend, Fehlerbehebung

---

### 4. `wayland.md` — Display-Server für X-Plane

**Nav-Position:** Linux > Erweiterungen

**Unterthemen:** X11 vs. Wayland Überblick, XWayland als Kompatibilitätsbrücke, Performance-Vergleich (Compositor-Overhead, Latenz), bekannte X-Plane-Probleme, Empfehlung (X11 für X-Plane), Wechsel zwischen Sessions, Fehlerbehebung

---

### 5. `audio.md` — Audio-Konfiguration

**Nav-Position:** Linux > Erweiterungen

**Unterthemen:** PulseAudio/PipeWire/ALSA, FMOD Audio-Engine, Grundkonfiguration, mehrere Audioausgänge (Headset + Lautsprecher), VATSIM-spezifisch (AFV, Mikrofon, PTT), Fehlerbehebung

---

### 6. `multi_monitor.md` — Multi-Monitor-Setup

**Nav-Position:** X-Plane

**Unterthemen:** X-Plane Visual Offsets, Nvidia Mosaic/AMD xrandr, Bezel Correction, Netzwerk-Rendering (Master/Slave), Performance-Überlegungen, Fehlerbehebung

---

### 7. `xplane/plugins.md` — Plugin-Verwaltung

**Nav-Position:** X-Plane

**Unterthemen:** XPLM Plugin-Architektur, native Linux-Plugins (FlyWithLua, Avitab), Windows-Only-Erkennung, Plugin-Verwaltung und -Debugging (ldd, Log.txt), empfohlene Linux-Plugins

---

### 8. `kvm.md` — WiP-Abschnitt aufräumen

**Optionen:** Ausbauen (Streamdeck USB-Passthrough, Windows-Plugins in KVM) oder WiP entfernen

---

## Notizen: Bestehende Seiten

### nvidia.md — Ergänzungen

- **NVIDIA Smooth Motion** (`NVPRESENT_ENABLE_SMOOTH_MOTION=1`): AI-Frame-Generierung (Vulkan-Layer). Nur RTX 40/50, ab Treiber 580.82.07. Kompatibel mit X-Plane 12, aber Stabilitätsprobleme (Flickering, Crashes). Offizielle Doku: [NVIDIA Linux README Ch. 39](https://download.nvidia.com/XFree86/Linux-x86_64/575.57.08/README/nvpresent.html)

---

## Querverweise (geplant)

| Von | Nach | Grund |
|-----|------|-------|
| `config.md` | `audio.md`, `input_devices.md`, `mesa.md` | Themen-Vertiefung |
| `input_devices.md` | `systemtuning.md` | USB-Energiemanagement |
| `audio.md` | `flight_operations/vatsim.md` | VATSIM-Funk |
| `wayland.md` | `multi_monitor.md` | Display-Server bei Multi-Monitor |
| `mesa.md` | `systemtuning.md` | GPU Power Profile + Governor |
| `plugins.md` | `addon/xorganizer.md` | Profil-basierte Verwaltung |
| `linux.md` | Alle neuen Seiten | Übersichtsseite erweitern |

## Nach Abschluss aller Seiten

- `linux.md` (DE + EN) — Übersichtsseite erweitern
- `glossary.md` (DE + EN) — Neue Einträge: Mesa, RADV, Wayland, PipeWire
- `mkdocs.yml` — Nav-Einträge in beiden Sprachbäumen
- `index.md` (DE + EN) — Changelog
