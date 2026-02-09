# XoL — Offene Dokumentationsthemen

## Arbeitsablauf pro Thema

Jedes Thema durchläuft drei Phasen — **keine Phase darf übersprungen werden.**

### Phase 1: Recherche

- Umfangreiche, hochaktuelle, tiefgehende Recherche zum Thema
- Primärquellen: GitHub-Repos (README, Releases, Code, Issues), offizielle Dokumentation, Kernel-Docs
- Keine Foren, keine Drittanbieter-Links die nur auf GitHub verweisen — direkt zur Quelle
- Ergebnis wird als strukturiertes Research-Paper in `research/` abgelegt
- Dateiname: beschreibend, z.B. `research/Mesa_Grafiktreiber_Linux.md`
- Das Paper dient als verifizierte Wissensbasis für die Dokumentation

### Phase 2: Analyse und Planung

- Bestehende Dokumentation analysieren: Was gibt es schon? Was muss sich ändern?
- Konkreten Plan erstellen: Was kommt neu wohin, was wird geändert, welche Querverweise
- Plan wird hier in der TODO.md oder als Kommentar beim jeweiligen Thema festgehalten
- Erst wenn der Plan steht und abgestimmt ist → weiter zu Phase 3

### Phase 3: Umsetzung

- Subagents schreiben die DE- und EN-Seiten parallel
- Bestehende Seiten werden angepasst (Querverweise, Nav, Glossar)
- Abschluss: `mkdocs serve` Prüfung, MARKDOWN_RULES Check, Changelog

---

## Übersicht

| Prio | Dateiname | Nav-Position | Typ | Thema |
|------|-----------|-------------|-----|-------|
| **1** | `xplane/config.md` | X-Plane > Konfiguration | Überarbeitung | X-Plane Grafikeinstellungen, Rendering, Vulkan |
| **2** | `mesa.md` | Linux > Optimierungen (nach nvidia.md) | Neue Seite | AMD/Intel GPU-Treiber (Mesa, RADV, Vulkan) |
| **3** | `input_devices.md` | Linux > Erweiterungen | Neue Seite | Joystick, Throttle, Ruderpedal unter Linux |
| **4** | `wayland.md` | Linux > Erweiterungen | Neue Seite | Display-Server-Wahl für X-Plane |
| **5** | `audio.md` | Linux > Erweiterungen | Neue Seite | PipeWire/PulseAudio für X-Plane |
| **6** | `multi_monitor.md` | X-Plane | Neue Seite | Multi-Monitor und Netzwerk-Rendering |
| **7** | `xplane/plugins.md` | X-Plane | Neue Seite | Plugin-Verwaltung unter Linux |
| **8** | `kvm.md` | Linux > Erweiterungen | Aufräumen | WiP-Abschnitt ausbauen oder entfernen |

---

## 1. `xplane/config.md` — X-Plane Konfiguration unter Linux (Überarbeitung)

**Status:** Recherche abgeschlossen, Plan erstellt

**Fokus-Entscheidung:** Allgemeine X-Plane-Einstellungen (Texture Quality, Shadows, Clouds etc.) sind plattformunabhängig und von Laminar Research dokumentiert. Die config.md wird ausschließlich auf **Linux-Spezifika** fokussiert.

### Research-Papers

- `research/XPlane12_Konfiguration_Linux_Spezifika.md` (konsolidiert)
- `research/Grafikeinstellungen_XPlane12_Technische_Grundlagen.md` (Agent A)
- `research/XPlane12_Einstellungsprofile_Linux_Performance.md` (Agent B)
- `research/Audio_Controller_Debugging_XPlane12.md` (Agent C)

### Umsetzungsplan

**Bestehender Inhalt wird ersetzt.** Die AA/PBR-Theorie und die Aufzählungs-Stichpunkte werden entfernt. Neuer Inhalt: nur Linux-Spezifika.

**Neue Gliederung (DE + EN parallel):**

- **Vulkan unter Linux**
    - Vulkan als einzige API (kein OpenGL-Fallback)
    - Treiber-Anforderungen: NVIDIA proprietär 510+, Mesa RADV 22.0+, Intel ANV ab 12.3.0
    - Zink für Plugin-Kompatibilität (30 FPS Gewinn, AMD-Hauptnutznießer)
    - Verweis auf nvidia.md und (zukünftig) mesa.md
- **Shader-Cache**
    - X-Plane-eigener Cache (`Output/shadercache/vulkan/`)
    - Mesa Shader-Cache (`~/.cache/mesa_shader_cache/`)
    - Cache löschen bei Problemen
- **Umgebungsvariablen**
    - Mesa/RADV: `MESA_SHADER_CACHE_*`, `MESA_VK_WSI_PRESENT_MODE`, `RADV_FORCE_VRS`
    - NVIDIA: `__GL_*` irrelevant für Vulkan
    - Tabelle mit Variablen, Werten und X-Plane-Relevanz
- **Display-Server**
    - X11 empfohlen (Compositor-Bypass)
    - Wayland/XWayland: funktional, aber Overhead
    - Verweis auf (zukünftig) wayland.md
- **Audio**
    - FMOD + PipeWire/PulseAudio-Integration
    - PipeWire-Workaround (Symlink, pipewire-pulse)
    - Verweis auf (zukünftig) audio.md
- **Controller**
    - SDL2/evdev-Erkennung, udev-Regeln (Pflicht)
    - Konfigurationsdateien (Linux-Pfade)
    - Bekannte Probleme (Autosuspend, Phantomachsen)
    - Verweis auf (zukünftig) input_devices.md
- **Log-Dateien und Debugging**
    - Log.txt Pfad und Rotation (ab 12.2.0)
    - Kommandozeilenparameter (Tabelle)
    - Vulkan Validation Layers
    - GPU-Crash-Analyse (`--aftermath`)
    - GDB für Crashes
- **Bekannte Linux-spezifische Probleme**
    - Tabelle: Bug / Version / Status (aus Release Notes)

### Änderungen an bestehenden Seiten

- `glossary.md` (DE + EN): Neue Einträge — FMOD, Zink, RADV, ACO, evdev
- `index.md` (DE + EN): Changelog-Eintrag
- Keine Änderungen an `mkdocs.yml` (Position bleibt: X-Plane > Konfiguration)

### Was NICHT übernommen wird

- Allgemeine Grafikeinstellungen (plattformunabhängig)
- GPU-klassenspezifische Profile (zu spekulativ, keine offiziellen Daten)
- VRAM-Verbrauchszahlen (variieren zu stark)
- FSR-Details (plattformunabhängig)
- .joy-Dateiformat im Detail (gehört in zukünftige input_devices.md)
- DataRef-Debugging im Detail (gehört in performance.md)

---

## Notizen: nvidia.md — Ergänzungen

- **NVIDIA Smooth Motion** (`NVPRESENT_ENABLE_SMOOTH_MOTION=1`): AI-basierte Frame-Generierung auf Treiberebene (Vulkan-Layer `VK_LAYER_NV_present`). Nur RTX 40/50, ab Treiber 580.82.07. Technisch kompatibel mit X-Plane 12 (Vulkan), aber Stabilitätsprobleme gemeldet (Flickering, Crashes). ~10ms zusätzliche Latenz. Offizielle Doku: [NVIDIA Linux README Ch. 39](https://download.nvidia.com/XFree86/Linux-x86_64/575.57.08/README/nvpresent.html). Eigener Abschnitt in nvidia.md sinnvoll.

---

## 2. `mesa.md` — Mesa/AMD/Intel Grafiktreiber (Neue Seite)

**Warum:** `nvidia.md` existiert und ist ausgezeichnet. Für AMD/Intel-GPUs (Mesa-Stack) gibt es nichts.

**Dateiname:** `mesa.md` — kurz, technisch korrekt (Mesa ist der gemeinsame Stack für AMD + Intel), analog zu `nvidia.md`

### Unterthemen

- **Überblick**
    - Mesa als Open-Source-Grafikstack
    - Abgrenzung zu Nvidia (proprietär vs. Open Source)
    - Unterstützte GPUs: AMD (RDNA, RDNA2, RDNA3), Intel Arc
    - Vulkan-Treiber: RADV (AMD), ANV (Intel)
- **Treiberversionen und Aktualität**
    - Debian Stable vs. Backports vs. kisak-mesa
    - Warum neuere Mesa-Versionen wichtig sind (X-Plane-Bugfixes, Vulkan-Features)
    - Mesa-Version prüfen: `glxinfo`, `vulkaninfo`
    - Backports aktivieren (Debian-spezifisch)
- **Vulkan-Konfiguration**
    - Vulkan ICD-Auswahl (`VK_ICD_FILENAMES`)
    - RADV vs. AMDVLK — Unterschiede und Empfehlung
    - Vulkan-Layers und Debugging (`VK_INSTANCE_LAYERS`)
    - vulkaninfo zur Diagnose
- **AMD-spezifische Optimierung**
    - GPU Power Profile (`pp_power_profile_mode`)
    - Performance-Level (`power_dpm_force_performance_level`)
    - OverDrive / Undervolting (`amdgpu.ppfeaturemask`)
    - Kernel-Parameter für AMDGPU
    - ACO-Shader-Compiler (Standard seit Mesa 20+)
    - Verweis auf systemtuning.md (C-States, Governor)
- **Intel Arc (experimentell)**
    - Aktueller Supportstatus
    - Bekannte Einschränkungen mit X-Plane
    - Erforderliche Kernel-/Mesa-Version
- **Performance-Monitoring**
    - MangoHUD (Querverweis zu nvidia.md)
    - `radeontop` für AMD
    - `intel_gpu_top` für Intel
- **Fehlerbehebung**
    - Schwarzer Bildschirm / Vulkan-Fehler
    - GPU-Reset-Erkennung (`dmesg | grep amdgpu`)
    - Mesa-Umgebungsvariablen für Debugging
    - Häufige Probleme mit X-Plane und Mesa

---

## 3. `input_devices.md` — Eingabegeräte unter Linux (Neue Seite)

**Warum:** Joystick/Throttle/Rudder-Setup ist ein typischer Linux-Schmerzpunkt. Die bestehende config.md erwähnt Controller nur als Aufzählung.

**Dateiname:** `input_devices.md`

### Unterthemen

- **Überblick**
    - Linux-Eingabesystem: evdev, /dev/input/, udev
    - Wie X-Plane Geräte erkennt (SDL2 Game Controller API)
    - Unterschied zu Windows (DirectInput)
- **Erkennung und Diagnose**
    - Geräte auflisten: `lsusb`, `/dev/input/js*`, `evtest`
    - jstest-gtk für grafische Kalibrierung
    - SDL2-Gerätenamen vs. Kernel-Gerätenamen
    - Wenn ein Gerät nicht erkannt wird — Kernel-Module, Firmware
- **Kalibrierung**
    - X-Plane-interne Kalibrierung (Nullzone, Empfindlichkeit, Kurven)
    - Linux-seitige Kalibrierung (`jscal`, persistent über udev)
    - Wann welche Methode sinnvoll ist
- **Mehrere identische Geräte**
    - Problem: Linux weist /dev/input/js* dynamisch zu
    - udev-Regeln für persistente Zuordnung (by-id, Seriennummer)
    - Beispiel: Zwei Thrustmaster TCA Quadrants unterscheiden
- **Bekannte Hardware**
    - Thrustmaster TCA (Sidestick, Quadrant) — Linux-Kompatibilität
    - Logitech/Saitek Panels (Radio, Autopilot, Multi) — eingeschränkt
    - VKB, Virpil, Winwing — HID-Kompatibilität
    - CH Products — ältere Hardware, oft problemlos
    - Xbox/PlayStation Controller als Fallback
- **USB-Energiemanagement**
    - Autosuspend kann Controller deaktivieren
    - Deaktivierung pro Gerät (`/sys/bus/usb/devices/*/power`)
    - udev-Regel für dauerhaftes Wachbleiben
    - Verweis auf systemtuning.md
- **Fehlerbehebung**
    - Achsen invertiert oder vertauscht
    - Gerät verschwindet nach Standby
    - Mehrfach-Erkennung / Phantom-Achsen
    - X-Plane Joystick-Konfigurationsdateien (Backup, Reset)

---

## 4. `wayland.md` — Display-Server für X-Plane (Neue Seite)

**Warum:** Debian 13 (Trixie) wird Wayland als Standard einführen. X-Plane läuft über XWayland. Nutzer brauchen Orientierung.

**Dateiname:** `wayland.md`

### Unterthemen

- **X11 vs. Wayland — Überblick**
    - Was ist ein Display-Server und warum ist er relevant?
    - X11: etabliert, voll unterstützt, im Wartungsmodus
    - Wayland: modern, sicherer, ersetzt X11 schrittweise
    - Debian 12 = X11 Standard, Debian 13 = Wayland Standard
- **XWayland — die Kompatibilitätsbrücke**
    - X-Plane nutzt X11-APIs → läuft unter Wayland über XWayland
    - XWayland-Funktionsweise (kurz)
    - Automatisch aktiv in GNOME/KDE Wayland-Sitzungen
- **Performance-Vergleich**
    - Compositor-Overhead unter Wayland vs. X11
    - VSync-Verhalten und Frame-Pacing
    - Eingabelatenz (relevant für Controller!)
    - Benchmarks: wann Unterschiede messbar sind, wann nicht
- **Bekannte Probleme mit X-Plane**
    - Cursor-Capture (Mausfang im Cockpit)
    - Vollbildmodus vs. Borderless Window
    - Multi-Monitor unter Wayland (Scaling, Refresh-Rate-Mixing)
    - GPU-spezifische Unterschiede (Nvidia vs. AMD unter Wayland)
- **Empfehlung**
    - Aktueller Stand: X11-Sitzung empfohlen für X-Plane
    - Wie man zwischen Wayland und X11 wechselt (GDM/SDDM)
    - Wann Wayland-Wechsel realistisch wird
- **Fehlerbehebung**
    - `echo $XDG_SESSION_TYPE` — welchen Server nutze ich?
    - X-Plane startet nicht unter Wayland
    - Grafikfehler nur unter Wayland

---

## 5. `audio.md` — Audio-Konfiguration (Neue Seite)

**Warum:** Kein Wort zu Audio im gesamten Projekt. Relevant für VATSIM-Nutzer (Funk) und allgemeine Soundqualität.

**Dateiname:** `audio.md`

### Unterthemen

- **Audio-Systeme unter Linux**
    - PulseAudio (Debian 12 Standard)
    - PipeWire (Debian 13 Standard, Debian 12 optional)
    - ALSA als Basis — wann direkt relevant?
    - Welches System nutze ich? (`pactl info`, `pw-cli info`)
- **X-Plane Audio-Engine**
    - FMOD als Standard-Engine
    - OpenAL als Alternative
    - Linux-spezifische Besonderheiten
- **Grundkonfiguration**
    - Standard-Audiogerät setzen (pavucontrol / wpctl)
    - Samplerate-Konfiguration (44.1 vs. 48 kHz)
    - Buffer-Größe und Latenz
- **Mehrere Audioausgänge**
    - Headset für VATSIM-Funk, Lautsprecher für Engine Sound
    - PulseAudio/PipeWire Routing pro Anwendung
    - pavucontrol für X-Plane-spezifisches Routing
- **VATSIM-spezifische Konfiguration**
    - Audio for VATSIM (AFV) unter Linux
    - Mikrofon-Setup und Echo-Unterdrückung
    - Push-to-Talk mit Joystick-Buttons
    - Verweis auf flight_operations/vatsim.md
- **Fehlerbehebung**
    - Kein Sound in X-Plane
    - Audio-Knacken / Crackling (Buffer-Underrun)
    - Samplerate-Mismatch zwischen Geräten
    - Audio nach Standby/Resume weg

---

## 6. `multi_monitor.md` — Multi-Monitor-Setup (Neue Seite)

**Warum:** X-Plane unterstützt Multi-Monitor nativ, aber das Linux-Setup (Nvidia Mosaic, Xrandr, Compositor) ist komplex.

**Dateiname:** `multi_monitor.md`

### Unterthemen

- **Überblick**
    - Warum Multi-Monitor bei Flugsimulation?
    - X-Plane-eigene Multi-Monitor-Unterstützung (Visual Offsets)
    - Einzel-PC vs. Netzwerk-Rendering (mehrere Instanzen)
- **Einzel-PC: Monitor-Konfiguration**
    - Nvidia: nvidia-settings, Mosaic/BaseMosaic
    - AMD: xrandr, arandr
    - Auflösung und Refresh-Rate angleichen
    - Bezel Correction (Rahmenausgleich)
- **X-Plane Visual Outputs**
    - Instruktoren-Ansicht (Full-Screen vs. Window)
    - Visual Offsets konfigurieren
    - Asymmetrische Setups (z.B. 3 Monitore vorne, 1 unten für Instrumente)
- **Netzwerk-Rendering**
    - Master/Slave-Konfiguration (mehrere X-Plane-Instanzen)
    - Netzwerk-Anforderungen (Gigabit LAN)
    - Synchronisation und Latenz
    - Externe Visuals auf separaten PCs
- **Performance-Überlegungen**
    - GPU-Last steigt linear mit Pixelzahl
    - Einstellungen für Multi-Monitor anpassen
    - Welche Grafikkarte für wieviele Monitore?
- **Fehlerbehebung**
    - Monitore werden nicht korrekt erkannt
    - Tearing über Monitor-Grenzen
    - Compositor deaktivieren für Gaming

---

## 7. `xplane/plugins.md` — Plugin-Verwaltung (Neue Seite)

**Warum:** Keine allgemeine Plugin-Seite. Es gibt addon-spezifische Seiten (AutoOrtho, Ortho4XP), aber kein Überblick über das Plugin-System und Linux-Kompatibilität.

**Dateiname:** `xplane/plugins.md`

### Unterthemen

- **Überblick**
    - X-Plane Plugin-Architektur (XPLM API)
    - Plugin-Verzeichnisse: Resources/plugins vs. Custom Scenery/*/plugins
    - Plattform-spezifische Binaries (lin.xpl, win.xpl, mac.xpl)
- **Native Linux-Plugins**
    - Welche Plugins bieten Linux-Builds?
    - FlyWithLua — Lua-Scripting, nativ verfügbar
    - XPRealistic — Verfügbarkeit
    - Avitab — In-Cockpit-Browser
    - Traffic-Plugins (TCAS, AI Traffic)
- **Windows-Only-Plugins**
    - Erkennung: fehlendes lin.xpl
    - Optionen: Wine-Wrapper (nicht empfohlen für Plugins)
    - Alternative Linux-Plugins für gleiche Funktion
    - Welche populären Plugins kein Linux unterstützen
- **Plugin-Verwaltung**
    - Aktivieren/Deaktivieren ohne Löschen
    - Plugin Admin im X-Plane-Menü
    - Load Order und Konflikte
    - XOrganizer für Profil-basierte Verwaltung (Verweis)
- **Debugging**
    - Log.txt: Plugin-bezogene Meldungen finden
    - Häufige Fehler: fehlende Libraries, Versionskonflikte
    - `ldd lin.xpl` — fehlende Shared Libraries identifizieren
    - GDB für Plugin-Crashes (fortgeschritten)
- **Empfohlene Plugins für Linux-Nutzer**
    - Curated Liste der getesteten, stabilen Linux-Plugins
    - Kategorien: Utility, Immersion, ATC, Traffic

---

## 8. `kvm.md` — WiP-Abschnitt aufräumen

**Status:** Der „WiP: X-Plane Plugins in a Windows OS in KVM" Abschnitt enthält nur Stichpunkte (Streamdeck, MyFS Flight).

**Optionen:**

- **Option A:** Ausbauen — Streamdeck USB-Passthrough, Windows-Plugin in KVM, Netzwerk-Bridge
- **Option B:** Entfernen — WiP-Abschnitt löschen, da nicht genug Substanz

---

## Querverweise

| Von | Nach | Grund |
|-----|------|-------|
| `config.md` | `audio.md` | Audio-Einstellungen → Linux-Audiosystem |
| `config.md` | `input_devices.md` | Controller-Konfiguration → Linux-Setup |
| `config.md` | `mesa.md` / `nvidia.md` | Vulkan-Einstellungen → Treiberseite |
| `input_devices.md` | `systemtuning.md` | USB-Energiemanagement |
| `audio.md` | `flight_operations/vatsim.md` | VATSIM-Funk |
| `wayland.md` | `multi_monitor.md` | Display-Server bei Multi-Monitor |
| `mesa.md` | `systemtuning.md` | GPU Power Profile + Governor |
| `plugins.md` | `addon/xorganizer.md` | Profil-basierte Verwaltung |
| `linux.md` | Alle neuen Seiten | Übersichtsseite erweitern |
| `glossary.md` | — | Neue Einträge: Mesa, RADV, Wayland, PipeWire, FMOD, evdev |

## Nach Abschluss aller Seiten

- `linux.md` (DE + EN) — Übersichtsseite um neue Themen erweitern
- `glossary.md` (DE + EN) — Neue Glossar-Einträge
- `mkdocs.yml` — Alle Nav-Einträge in beiden Sprachbäumen
- `index.md` (DE + EN) — Changelog aktualisieren
