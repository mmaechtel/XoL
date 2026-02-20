# XoL — Offene Dokumentationsthemen

Workflow und Phasen-Beschreibung: siehe `CLAUDE.md` → Dokumentations-Workflow.

---

## Übersicht

| Prio  | Datei               | Status      | Thema                                               |
| ----- | ------------------- | ----------- | --------------------------------------------------- |
| 1b    | `systemtuning.md`   | offen       | Kernel-Wechsel (Debian, Standard ↔ Liquorix)        |
| 2     | `mesa.md`           | offen       | AMD/Intel GPU-Treiber (Mesa, RADV, Vulkan)          |
| 3     | `input_devices.md`  | offen       | Joystick, Throttle, Ruderpedal unter Linux          |
| 5     | `audio.md`          | offen       | PipeWire/PulseAudio für X-Plane                     |
| 6     | `multi_monitor.md`  | offen       | Multi-Monitor und Netzwerk-Rendering                |
| 7     | `xplane/plugins.md` | offen       | Plugin-Verwaltung unter Linux                       |
| 8     | `kvm.md`            | offen       | WiP-Abschnitt ausbauen oder entfernen               |
| 11    | `addon/xorganizer.md` | offen     | Wine-Installation und Workflow-Hinweise             |
| 12    | Verzeichnisnamen    | offen       | DE-Verzeichnisnamen in EN-Pfaden (`systemfehler/`, `aufbau_quellen/`, `setup_diagnose/`) auf englische Namen migrieren |
| 13    | `addon/cockpit/xchecklist.md` | geprüft | Xchecklist: Interaktive Checklisten mit Linux-TTS |
| 14    | `addon/cockpit/opentrack.md` | geprüft | OpenTrack: Headtracking unter Linux |
| 15    | `addon/tools/xlinspeak.md` | geprüft | XLinSpeak ergänzen: Piper TTS Manager |
| 16    | `addon/cockpit/xpwalkaround.md` | geprüft | XP Walkaround: First-Person-Walkaround |

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

### 1c. `systemtools.md` — Linux-Systemtools

**Status:** geprüft (Audit abgeschlossen)
**Nav-Position:** Linux > System > Monitoring

**Ergebnis:** Companion-Seite zu systemtuning.md — Tools zur Verifikation der dort beschriebenen Einstellungen. CPU-Monitoring, IO-Monitoring, Interrupt-Analyse, System-Dashboards, Szenario-Tabelle.

**Research-Papers:**

- `research/systemtools/cpu_monitoring_tools.md`
- `research/systemtools/io_monitoring_tools.md`
- `research/systemtools/interrupt_monitoring_tools.md`
- `research/systemtools/Linux_Monitoring_Tools_Combined.md`
- `research/systemtools/LEKTORAT_systemtools.md`
- `research/systemtools/AUDIT_systemtools.md`

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

### systemtuning.md — Governor/Liquorix-Korrektur

**Status:** erledigt (Commit e7a201a, 2026-02-14)

- Profil B: `schedutil` → `ondemand` (Governor-Empfehlung + GRUB-Parameter)
- Vergleichstabelle: `schedutil` → `ondemand`
- Temporärer Terminal-Befehl zum Governor-Wechsel ergänzt
- Erklärbox: Warum `ondemand` statt `schedutil` (PDS-Scheduler)
- `IRQBALANCE_BANNED_CPULIST`: Pfad `/etc/default/irqbalance` dokumentiert
- `nvme_core.default_ps_max_latency_us=0`: sysfs-Limitierung erklärt + PM-QOS-Workaround ergänzt

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

## Neue Kapitel

### systemtuning.md — Kernel-Wechsel (Debian)

**Status:** offen
**Nav-Position:** Hinter die beiden Kernel-Optimierungs-Profile

Anleitung: Wie man unter Debian zwischen zwei installierten Kerneln (Standard + Liquorix) on-the-fly wechselt. Ergänzendes Kapitel zu den bestehenden Profilen.

### addon/xorganizer.md — Wine-Installation und Workflow

**Status:** offen

**Ergänzungen:**

- **Workflow-Hinweis:** XOrganizer kann X-Plane unter Linux nicht selbst starten (Windows-Programm). Ablauf: scenery.ini schreiben lassen → XOrganizer beenden → X-Plane starten
- **Wine-Installationsanleitung:** Binary in Wine-App-Ordner anlegen, `winetricks` für .NET, ggf. ältere + neuere .NET-Version übereinander installieren
- **Font-Anpassungen** bei hoher Auflösung (HiDPI)
- Querverweis auf Wine-Seite

---

### 13. `addon/cockpit/xchecklist.md` — Xchecklist

**Status:** geprüft
**Nav-Position:** Addon > Cockpit

Interaktive Checklisten mit TTS unter Linux. Nativ (lin.xpl), Open Source (MIT), v1.53. Linux-Spezifikum: TTS via libspeechd/speech-dispatcher. Querverweis auf XLinSpeak.

**Gliederung:** Background, Features, Value, Installation, TTS on Linux, Sources

**Research-Papers:**

- `research/addons/xplane_addon_plugins_linux.md` (Abschnitt 1)
- `research/addons/LEKTORAT_xplane_addon_plugins_linux.md`

---

### 14. `addon/cockpit/opentrack.md` — OpenTrack Headtracking

**Status:** geprüft
**Nav-Position:** Addon > Cockpit

OpenTrack als Hauptlösung für Headtracking unter Linux. NeuralNet Tracker (Webcam, kein Hardware nötig), HeadTrack-Plugin (amyinorbit) als empfohlene X-Plane-Bridge via UDP:4242. Build-Anleitung für Debian. Querverweis von linuxtrack.md.

**Gliederung:** Background, Features, Value, Recommended Linux Setup, Installation, Configuration, NeuralNet Tracker, SmoothTrack, Sources

**Research-Papers:**

- `research/addons/xplane_addon_plugins_linux.md` (Abschnitt 5)
- `research/addons/LEKTORAT_xplane_addon_plugins_linux.md`

---

### 15. XLinSpeak ergänzen — Piper TTS Manager

**Status:** geprüft

Bestehende XLinSpeak-Seite um Abschnitt zu Piper TTS Manager (PTTSM) ergänzt. Hochwertige neuronale Sprachsynthese via FlyWithLua + Piper.

**Research-Papers:**

- `research/addons/xplane_addon_plugins_linux.md` (Abschnitt 6)
- `research/addons/LEKTORAT_xplane_addon_plugins_linux.md`

---

### 16. `addon/cockpit/xpwalkaround.md` — XP Walkaround

**Status:** geprüft

**Ergebnis:** First-Person-Walkaround mit Flashlight, Campsite-System und Mouse Look. Faktencheck gegen Gumroad-Produktseite, 10 falsche Claims korrigiert (stammten von VFRScenery's WalkAround), Glossar-Check sauber.

**Research-Papers:**

- `research/addons/FAKTENCHECK_xpwalkaround.md`

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
| `audio.md`         | `flight_operations/vatsim/vatsim.md`      | VATSIM-Funk                      |
| `displayserver.md` | `multi_monitor.md`                        | Display-Server bei Multi-Monitor |
| `mesa.md`          | `systemtuning.md`                         | GPU Power Profile + Governor     |
| `plugins.md`       | `addon/xorganizer.md`                     | Profil-basierte Verwaltung       |
| `linux/index.md`   | Alle neuen Seiten                         | Übersichtsseite erweitern        |

## Nach Abschluss aller Seiten

- `linux/index.md` (DE + EN) — Übersichtsseite erweitern
- `glossary.md` (DE + EN) — Neue Einträge: Mesa, RADV, Wayland, PipeWire
- `mkdocs.yml` — Nav-Einträge in beiden Sprachbäumen
- `index.md` (DE + EN) — Changelog
