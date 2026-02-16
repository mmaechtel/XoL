# XoL — Offene Dokumentationsthemen

Workflow und Phasen-Beschreibung: siehe `CLAUDE.md` → Dokumentations-Workflow.

---

## Übersicht

| Prio  | Datei               | Status      | Thema                                               |
| ----- | ------------------- | ----------- | --------------------------------------------------- |
| 1     | `xplane/config.md`  | **geprüft** | X-Plane Konfiguration (Linux-Spezifika)             |
| **!** | `systemtuning.md`   | **geprüft** | **Governor/Liquorix korrigiert + Erklärungen ergänzt** |
| 1b    | `systemtuning.md`   | umgesetzt   | Kernel-Wechsel (Debian, Standard ↔ Liquorix)        |
| 1c    | `systemtools.md`    | **umgesetzt** | Linux-Systemtools (htop, glances, iotop)            |
| 2     | `mesa.md`           | offen       | AMD/Intel GPU-Treiber (Mesa, RADV, Vulkan)          |
| 3     | `input_devices.md`  | offen       | Joystick, Throttle, Ruderpedal unter Linux          |
| 4     | `displayserver*.md` | **geprüft** | Display-Server-Wahl für X-Plane |
| 5     | `audio.md`          | offen       | PipeWire/PulseAudio für X-Plane                     |
| 6     | `multi_monitor.md`  | offen       | Multi-Monitor und Netzwerk-Rendering                |
| 7     | `xplane/plugins.md` | offen       | Plugin-Verwaltung unter Linux                       |
| 8     | `kvm.md`            | offen       | WiP-Abschnitt ausbauen oder entfernen               |

| 11 | `addon/xorganizer.md` | offen | Wine-Installation und Workflow-Hinweise |

---

## Abgeschlossene Themen

### 1. `xplane/config.md` — X-Plane Konfiguration (Überarbeitung)

**Status:** geprüft

**Ergebnis:** Komplett neu geschrieben mit Fokus auf Linux-Spezifika. Vulkan/Zink, Shader-Cache, Mesa-Umgebungsvariablen, Display-Server, Audio, Controller, szenariobasierte CLI-Fehlerbehebung, GPU-Debugging. Akademische Hintergrundtexte (AA, PBR) als klappbare Blöcke. Faktencheck gegen Primärquellen durchgeführt, versionsspezifische Informationen bereinigt.

**Research-Papers:**

- `research/xplane-config/XPlane12_Konfiguration_Linux_Spezifika.md`
- `research/xplane-config/LEKTORAT_config_md.md`
- `research/xplane-config/xplane-help.out` (X-Plane CLI-Referenz)

---

### 4. Display-Server (displayserver.md, displayserver_wayland.md, displayserver_x11.md)

**Status:** geprüft

**Ergebnis:** Drei Seiten (Übersicht, X11-Session, Wayland-Session) in DE + EN. Latenz-Messungen (Justo + Hugl), GPU-spezifische Empfehlungen, Szenario-Tabellen. Faktencheck mit 6 Korrekturen eingearbeitet.

**Research-Papers:**

- `research/display-server/wayland_display_server.md` (konsolidiert)
- `research/display-server/wayland_vs_x11.md` (Rohdaten: X-Plane-Kompatibilität)
- `research/display-server/wayland_vs_x11_gaming.md` (Rohdaten: Performance/Latenz)
- `research/display-server/LEKTORAT_wayland.md`
- `research/display-server/FAKTENCHECK_displayserver.md`

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

## Strukturbereinigung: Dateien in Unterverzeichnisse verschieben

Konvention: Jede Nav-Section hat ein eigenes Unterverzeichnis mit `index.md`.
Folgende Dateien liegen noch im Root und müssen verschoben werden:

### "Übersicht"-Section — bleibt im Root

- `intro.md`, `begin.md`, `performance_overview.md`, `videos.md` bleiben im Root
- Der Section Index der "Übersicht" ist die Homepage (`index.md`)
- Ein eigenes Verzeichnis würde zwei Tiefen innerhalb einer Section erzeugen

### "Szenerien"-Section → neues Verzeichnis (z.B. `scenery/`)

- `scenery.md`, `scenery_components.md`
- `addon/xorganizer.md` bleibt in `addon/` (nur in der Nav unter Szenerien eingehängt)

### Ablauf (analog zur system/optimizations/extensions-Migration)

1. `git mv` der Dateien (DE + EN)
2. `mkdocs.yml` Nav-Pfade anpassen
3. Neue `index.md` Section-Index-Seiten erstellen
4. Links in verschobenen Dateien anpassen
5. Externe Verweise auf verschobene Dateien anpassen (glossary, andere Seiten)
6. `mkdocs build --strict` Verifikation

---

## Korrekturen: Bestehende Seiten

### systemtuning.md — CPU-Governor / Liquorix ~~falsch~~ erledigt

**Status:** erledigt (Commit e7a201a, 2026-02-14)

- ✅ Profil B: `schedutil` → `ondemand` (Governor-Empfehlung + GRUB-Parameter)
- ✅ Vergleichstabelle: `schedutil` → `ondemand`
- ✅ Temporärer Terminal-Befehl zum Governor-Wechsel ergänzt
- ✅ Erklärbox: Warum `ondemand` statt `schedutil` (PDS-Scheduler)

### systemtuning.md — Fehlende Erklärungen — erledigt

**Status:** erledigt (Commit e7a201a, 2026-02-14)

- ✅ `IRQBALANCE_BANNED_CPULIST`: Pfad `/etc/default/irqbalance` dokumentiert
- ✅ `nvme_core.default_ps_max_latency_us=0`: sysfs-Limitierung erklärt + PM-QOS-Workaround ergänzt

---

## Neue Kapitel

### systemtuning.md — Kernel-Wechsel (Debian)

**Status:** offen
**Nav-Position:** Hinter die beiden Kernel-Optimierungs-Profile

Anleitung: Wie man unter Debian zwischen zwei installierten Kerneln (Standard + Liquorix) on-the-fly wechselt. Ergänzendes Kapitel zu den bestehenden Profilen.

### systemtools.md — Linux-Systemtools

**Status:** umgesetzt
**Nav-Position:** Linux > Optimierungen (nach Systemtuning, vor Dateisystem)

**Research-Papers:**

- `research/systemtools/cpu_monitoring_tools.md`
- `research/systemtools/io_monitoring_tools.md`
- `research/systemtools/interrupt_monitoring_tools.md`
- `research/systemtools/Linux_Monitoring_Tools_Combined.md`
- `research/systemtools/LEKTORAT_systemtools.md`

**Plan:** Companion-Seite zu systemtuning.md — Tools zur Verifikation der dort beschriebenen Einstellungen.

**Gliederung:**

1. Einleitung + Installation (alle Pakete)
2. CPU-Monitoring: htop, btop, cpupower, s-tui, turbostat, mpstat
3. IO-Monitoring: iotop, iostat, ioping, nvme-cli
4. Interrupt-Analyse: /proc/interrupts, irqtop/lsirq, mpstat -I, Shielding-Verifikation
5. System-Dashboards: glances (Web-UI), powertop (C-States)
6. Szenario-Tabelle: Frage → Tool → Befehl
7. Klappbare Blöcke: nmon, fatrace, perf/ftrace (Fortgeschrittene)
8. Quellenabschnitt

**Querverweise:** Jedes Tool-Kapitel verweist auf den relevanten systemtuning.md-Abschnitt.

### addon/xorganizer.md — Wine-Installation und Workflow

**Status:** offen

**Ergänzungen:**

- **Workflow-Hinweis:** XOrganizer kann X-Plane unter Linux nicht selbst starten (Windows-Programm). Ablauf: scenery.ini schreiben lassen → XOrganizer beenden → X-Plane starten
- **Wine-Installationsanleitung:** Binary in Wine-App-Ordner anlegen, `winetricks` für .NET, ggf. ältere + neuere .NET-Version übereinander installieren
- **Font-Anpassungen** bei hoher Auflösung (HiDPI)
- Querverweis auf Wine-Seite

---

## Notizen: Bestehende Seiten

### nvidia.md — Ergänzungen

- **NVIDIA Smooth Motion** (`NVPRESENT_ENABLE_SMOOTH_MOTION=1`): AI-Frame-Generierung (Vulkan-Layer). Nur RTX 40/50, ab Treiber 580.82.07. Kompatibel mit X-Plane 12, aber Stabilitätsprobleme (Flickering, Crashes). Offizielle Doku: [NVIDIA Linux README Ch. 39](https://download.nvidia.com/XFree86/Linux-x86_64/575.57.08/README/nvpresent.html)

---

## Querverweise (geplant)

| Von                | Nach                                      | Grund                            |
| ------------------ | ----------------------------------------- | -------------------------------- |
| `config.md`        | `audio.md`, `input_devices.md`, `mesa.md` | Themen-Vertiefung                |
| `input_devices.md` | `systemtuning.md`                         | USB-Energiemanagement            |
| `audio.md`         | `flight_operations/vatsim.md`             | VATSIM-Funk                      |
| `displayserver.md` | `multi_monitor.md`                        | Display-Server bei Multi-Monitor |
| `mesa.md`          | `systemtuning.md`                         | GPU Power Profile + Governor     |
| `plugins.md`       | `addon/xorganizer.md`                     | Profil-basierte Verwaltung       |
| `linux.md`         | Alle neuen Seiten                         | Übersichtsseite erweitern        |

## Nach Abschluss aller Seiten

- `linux.md` (DE + EN) — Übersichtsseite erweitern
- `glossary.md` (DE + EN) — Neue Einträge: Mesa, RADV, Wayland, PipeWire
- `mkdocs.yml` — Nav-Einträge in beiden Sprachbäumen
- `index.md` (DE + EN) — Changelog
