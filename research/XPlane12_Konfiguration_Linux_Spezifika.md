# X-Plane 12 Konfiguration unter Linux — Konsolidiertes Research-Paper

## Zusammenfassung

Dieses Paper fasst die Linux-spezifischen Aspekte der X-Plane 12 Konfiguration zusammen. X-Plane 12 ist eine Cross-Plattform-Anwendung; die allgemeinen Grafikeinstellungen (Texture Quality, Shadow Quality, Cloud Quality etc.) sind plattformunabhängig und werden von Laminar Research dokumentiert. Dieses Paper fokussiert ausschließlich auf das, was unter Linux anders ist: Vulkan-Treiber und Zink, Shader-Caching, Umgebungsvariablen, Audio-Systemintegration, Controller-Erkennung, Compositor-Verhalten und Linux-spezifisches Debugging.

Quellbasis: Drei separate Recherche-Papers (Agent A: Grafikgrundlagen, Agent B: Performance/Profile, Agent C: Audio/Controller/Debugging), konsolidiert mit Fokus auf Linux-Relevanz.

---

## 1. Vulkan unter Linux

### 1.1 Vulkan ist die einzige Rendering-API

X-Plane 12 nutzt ausschließlich Vulkan (Linux/Windows) bzw. Metal (macOS). Es gibt kein OpenGL-Fallback für die Haupt-Rendering-Pipeline.

> "X-Plane 12 uses Vulkan/Metal as its renderer, always."
> — Ben Supnik, Laminar Research

**Mindestanforderung:** Vulkan 1.3
- NVIDIA: Proprietärer Treiber 510+, empfohlen 580+ (für 12.4.0)
- AMD: Mesa RADV 22.0+ (Vulkan 1.3 Unterstützung)
- Intel Arc: Ab X-Plane 12.3.0 unterstützt, Mesa ANV-Treiber

**Quellen:**
- https://developer.x-plane.com/2022/09/x-plane-12-early-access-is-here/
- https://www.x-plane.com/kb/x-plane-12-system-requirements/

### 1.2 Zink — OpenGL-zu-Vulkan-Brücke für Plugins

X-Plane 12 liefert den Zink-Treiber mit, um Plugin-OpenGL-Rendering in native Vulkan-Befehle umzuwandeln. Dies ist eine Linux- und Windows-übergreifende Lösung, aber unter Linux besonders relevant wegen der Mesa/RADV-Stack-Interaktion.

**Performance-Gewinn:**
- Ohne Zink (native OpenGL/Vulkan Interop): bis zu 10 ms/Frame zusätzlich, in Extremfällen 30 ms
- Mit Zink: FPS-Vergleich aus Entwicklerdoku: 50 FPS → 80 FPS (30 FPS Gewinn)
- Hauptnutznießer: AMD-GPUs (native OpenGL/Vulkan-Interop war besonders problematisch)

**Plattform-Support:**
- NVIDIA: Ab 12.1.0 Beta 6 wieder aktiviert (war zuvor wegen Crashes deaktiviert)
- AMD: Seit Einführung aktiviert
- Intel: Unterstützt

**Bekannte Einschränkungen:**
- Shared OpenGL Contexts für Hintergrundverarbeitung "not 100% stable"
- `GL_FRAMEBUFFER_SRGB` Enable/Disable kann zu verschwindenden Rendering-Artefakten führen
- Ab 12.4.0: GPU-Auswahl für Zink bei Multi-GPU-Systemen hinzugefügt

**Debug-Modus:** `--debug_gl` aktiviert OpenGL-Debug-Callbacks für Plugin-Entwickler.

**Quellen:**
- https://developer.x-plane.com/2023/02/addressing-plugin-flickering/
- https://www.gamingonlinux.com/2023/02/x-plane-12-now-uses-the-open-source-zink-driver-to-help-plugins/
- https://www.x-plane.com/kb/x-plane-12-4-0-release-notes/

### 1.3 RADV vs. NVIDIA proprietär

**RADV (AMD):**
- ACO-Shader-Compiler ist Standard seit Mesa 20+ (kompiliert SPIR-V → NIR → GPU-nativer Code)
- AMDVLK wurde September 2025 eingestellt; RADV ist der einzige aktiv entwickelte Vulkan-Treiber für AMD unter Linux
- Valve beteiligt sich aktiv an RADV-Entwicklung (Steam Deck)

**NVIDIA:**
- Proprietärer Treiber mit eigener Vulkan-Implementierung
- `__GL_*`-Umgebungsvariablen betreffen ausschließlich OpenGL, nicht Vulkan — für X-Plane 12 irrelevant

**Keine systematischen X-Plane 12 Benchmarks zwischen RADV und NVIDIA proprietär vorhanden.**

**Quellen:**
- https://github.com/GPUOpen-Drivers/AMDVLK/discussions/416
- https://docs.mesa3d.org/drivers/radv.html

---

## 2. Shader-Cache-Systeme

X-Plane 12 nutzt unter Linux **zwei separate Shader-Cache-Systeme:**

### 2.1 X-Plane-eigener Shader-Cache

- **Pfad:** `<X-Plane-Root>/Output/shadercache/vulkan/`
- Enthält vorkompilierte Vulkan-Pipeline-Objekte
- Kann bei Crashes oder Performance-Anomalien gelöscht werden → wird beim nächsten Start neu aufgebaut
- Neuaufbau kann mehrere Minuten dauern

### 2.2 Mesa Shader-Cache (nur AMD/Intel)

- **Standard-Pfad:** `~/.cache/mesa_shader_cache/` (folgt XDG-Konventionen)
- **Überschreibbar:** `MESA_SHADER_CACHE_DIR=<Pfad>`
- **Standard-Maximum:** 1 GB (überschreibbar mit `MESA_SHADER_CACHE_MAX_SIZE`, z.B. `2G`)
- Cacht von ACO kompilierte Shader auf Treiberebene
- NVIDIA hat einen eigenen internen Shader-Cache (nicht über Mesa)

**Quellen:**
- https://docs.mesa3d.org/envvars.html

---

## 3. Linux-relevante Umgebungsvariablen

### 3.1 Mesa/RADV (AMD GPUs)

| Variable | Werte | Effekt | X-Plane-Relevanz |
|----------|-------|--------|-------------------|
| `MESA_SHADER_CACHE_DIR` | Pfad | Shader-Cache-Speicherort | Auf schnellere SSD umleiten |
| `MESA_SHADER_CACHE_MAX_SIZE` | z.B. `2G` | Cache-Größe (Standard: 1 GB) | Mehr Cache = weniger Rekompilierung |
| `MESA_VK_WSI_PRESENT_MODE` | `fifo`, `mailbox`, `immediate` | Swapchain-Präsentation | `mailbox` = Tearing-frei mit niedriger Latenz |
| `RADV_TEX_ANISO` | 1-16 | Erzwingt anisotrope Filterung | Texturqualität bei Distanz |
| `RADV_FORCE_VRS` | `2x2`, `2x1`, `1x2` | Variable Rate Shading | 10-30% FPS-Gewinn auf RDNA2+, reduzierte Bildqualität. **Nicht mit X-Plane getestet.** |

### 3.2 NVIDIA

| Variable | Werte | Effekt | X-Plane-Relevanz |
|----------|-------|--------|-------------------|
| `__GL_THREADED_OPTIMIZATIONS` | `0`/`1` | OpenGL Worker-Thread | **Nur OpenGL** — für X-Plane 12 (Vulkan) irrelevant |
| `__GL_YIELD` | `NOTHING`/`USLEEP` | CPU-Yield bei OpenGL | **Nur OpenGL** — irrelevant |

**Wichtig:** Die `__GL_*`-Variablen betreffen ausschließlich OpenGL. Da X-Plane 12 primär Vulkan nutzt, sind sie für die Haupt-Rendering-Pipeline nicht relevant.

**Quellen:**
- https://docs.mesa3d.org/envvars.html
- https://docs.mesa3d.org/drivers/radv.html

---

## 4. Compositor-Impact: X11 vs. Wayland

X-Plane 12 hat **keine native Wayland-Unterstützung** und läuft unter Wayland-Sitzungen über XWayland.

**Performance-Unterschiede:**
- X11: Fullscreen-Anwendungen können Compositor umgehen (Compositor-Bypass) → kein Overhead
- Wayland/XWayland: Kein Compositor-Bypass für XWayland-Fenster → zusätzliche Kopie
- Phoronix-Tests (2023): X-Plane auf NVIDIA performte unter X.Org besser als unter Wayland/GNOME 43

**Empfehlung:** Für maximale Performance X11-Sitzung verwenden.

**Bekannte Wayland-Probleme:**
- 12.1.4: Fehler beim Fenstergröße-ändern unter Wayland (behoben)
- Fullscreen-Verhalten unter XWayland kann unzuverlässig sein
- Cursor-Capture kann problematisch sein

**Quellen:**
- https://www.phoronix.com/review/wayland-nv-amd-2023/4
- https://www.x-plane.com/kb/x-plane-12-1-0-release-notes/

---

## 5. Audio unter Linux

### 5.1 Audio-Engine

X-Plane 12 nutzt **FMOD Studio 2.02** als Audio-Engine. OpenAL bleibt nur für Legacy-Plugins/Flugzeuge verfügbar.

FMOD kommuniziert direkt mit PulseAudio/PipeWire/ALSA.

### 5.2 PipeWire-Kompatibilität

PipeWire wird seit FMOD 2.02.05 unterstützt. Es gibt einen **offiziellen X-Plane KB-Artikel** für PipeWire-Audio-Probleme.

**Workaround bei fehlender Erkennung:**
- Symlink `/usr/bin/pulseaudio → /bin/true`
- Pakete `pipewire-pulse` und `pipewire-alsa` installieren

**Quellen:**
- https://www.x-plane.com/kb/troubleshooting-audio-issues-with-pipewire-on-linux/
- https://developer.x-plane.com/docs/sound/

### 5.3 OpenAL Soft

OpenAL Soft (https://github.com/kcat/openal-soft) ist Open Source und unter Linux gut integriert. Es wird nur noch für Legacy-Plugins benötigt, die die alte XPLMSound-API nutzen. Die FMOD-basierte Audio-Pipeline ist der Standard.

---

## 6. Controller unter Linux

### 6.1 Geräterkennung

X-Plane nutzt **SDL2** mit zwei Backends:
- **HIDAPI:** Priorität für bekannte Controller (USB HID direkt)
- **evdev:** Fallback über `/dev/input/event*`

**Wichtig:** X-Plane darf **niemals als root** gestartet werden. udev-Regeln sind zwingend nötig, damit der Nutzer Zugriff auf evdev-Nodes hat.

### 6.2 udev-Regeln

Offizielle Anleitung: https://www.x-plane.com/kb/using-joysticks-x-plane-11-linux-systems/

Typische Regel (Zugriff auf evdev-Nodes für Input-Geräte):
```
SUBSYSTEM=="input", ATTRS{idVendor}=="<VID>", ATTRS{idProduct}=="<PID>", MODE="0666"
```

### 6.3 Konfigurationsdateien

| Dateityp | Pfad | Beschreibung |
|----------|------|-------------|
| `.joy` | `Resources/joystick configs/` | Gerätedefinitionen mit Grafiken und Standardzuweisungen |
| `.prf` | `Output/preferences/` | Benutzerspezifische Joystick-Einstellungen |

Unter Linux: `~/X-Plane 12/Output/preferences/`

**Linux-spezifische .joy-Dateien in XP12:**
- HOTAS Warthog (12.00)
- VKB Gladiator MK II (12.00)
- VirtualFly (12.1.0)
- RealSimGear (12.1.0)

### 6.4 Bekannte Linux-Probleme

- **Gerät nicht erkannt:** Fehlende udev-Berechtigungen auf evdev-Nodes. SDL2 nutzt `/dev/input/event*`, nicht `/dev/input/js*`
- **Achsen invertiert:** "Reverse"-Checkbox in X-Plane, alternativ `jscal` auf Linux-Seite
- **Gerät verschwindet nach Standby:** USB-Autosuspend deaktivieren per udev-Regel
- **Phantomachsen:** Einige Geräte melden sich als mehrere Input-Devices; `.joy`-Datei mit "hidden"-Markierung

**Quellen:**
- https://www.x-plane.com/kb/using-joysticks-x-plane-11-linux-systems/
- https://developer.x-plane.com/article/creating-joystick-configuration-joy-files/
- https://www.x-plane.com/kb/my-joystick-or-yoke-isnt-working/

---

## 7. Debugging unter Linux

### 7.1 Log.txt

**Pfad:** `<X-Plane 12 Root>/Log.txt`

**Ab 12.2.0: Log-Rotation** — bis zu 4 Kopien:
- `Log.txt` (aktuell), `Log.1.txt`, `Log.2.txt`, `Log.3.txt`
- Ältere Logs in `Output/Log Archive/` mit Zeitstempel

### 7.2 Kommandozeilenparameter

Vollständige Liste: `./X-Plane-x86_64 --help` (siehe auch `research/xplane-help.out`).

```bash
cd ~/X-Plane\ 12/
./X-Plane-x86_64 --<option>
```

**Für Linux-Nutzer besonders relevant:**

| Parameter | Beschreibung | Linux-Anwendungsfall |
|-----------|-------------|---------------------|
| `--no_joysticks` | Startet ohne Controller-Initialisierung | Isoliert evdev/udev-Probleme |
| `--no_sound` | Startet ohne Sound-Initialisierung | Isoliert PipeWire/PulseAudio-Probleme |
| `--safe_mode=PLG` | Deaktiviert nur Plugins (auch: `GFX`, `SCN`, `ART`, `UI`, kombibar) | Gezieltes Debugging statt alles abschalten |
| `--window=<W>x<H>` | Erzwingt Fenstermodus mit Auflösung | Umgeht Wayland/XWayland-Fullscreen-Probleme |
| `--full=<W>x<H>` | Erzwingt Vollbild mit Auflösung | Monitor-Auflösung explizit setzen |
| `--disable_networking` | Deaktiviert Netzwerk komplett | IPv6-Probleme isolieren (Kernel 6.9+ Bug war Linux-spezifisch) |
| `--aftermath` | GPU-Crash-Datensammlung (NVIDIA, AMD, Intel ab 12.2.0) | Post-Mortem-Analyse bei Device Loss |
| `--debug_gl` | OpenGL-Debug-Callbacks für Zink/Plugin-Rendering | Plugin-Flickering unter Mesa/RADV diagnostizieren |
| `--pref:<key>=<value>` | Preference per CLI überschreiben | Launch-Scripte mit verschiedenen Profilen |
| `--dref:<ref>=<value>` | DataRef beim Start setzen | Automatisierung, Testszenarien |

**Benchmark-Modus:**

| Parameter | Beschreibung |
|-----------|-------------|
| `--fps_test=N` | 3-stelliger Code: Hundert=Viewpoint (0=Cockpit, 1=Oben), Zehner=Wetter (0-7), Einer=Qualität (1-5) |
| `--verbose` | Per-Frame-Timing-Daten statt nur Durchschnitt |
| `--require_fps=N` | Exit 0 wenn FPS > N, sonst Exit 1 — für Scripting |
| `--weather_seed=N` | Reproduzierbares Wetter über Runs |
| `--time_seed=N` | Reproduzierbarer Non-Weather-RNG |

**Beispiele für Linux-Anwendungsfälle:**

```bash
# Controller-Problem isolieren
./X-Plane-x86_64 --no_joysticks

# Nur Plugins deaktivieren (Rest normal)
./X-Plane-x86_64 --safe_mode=PLG

# Fenstermodus bei Wayland-Fullscreen-Problemen
./X-Plane-x86_64 --window=1920x1080

# Reproduzierbarer Benchmark (Cockpit, klares Wetter, High Quality)
./X-Plane-x86_64 --fps_test=003 --verbose --weather_seed=42

# Pass/Fail-Test für CI oder Hardware-Checks
./X-Plane-x86_64 --fps_test=003 --require_fps=30
```

**Hinweis:** Die zahlreichen `--no_vbos`, `--no_fbos` etc. Flags sind OpenGL-Legacy-Optionen und unter X-Plane 12 (Vulkan) irrelevant.

### 7.3 Vulkan Validation Layers

```bash
sudo apt install vulkan-validationlayers
VK_INSTANCE_LAYERS=VK_LAYER_KHRONOS_validation ./X-Plane-x86_64
```

**Achtung:** Massive Performance-Einbußen — nur für Debugging.

### 7.4 GPU-Crash-Analyse (Aftermath)

Ab 12.2.0 für NVIDIA, AMD und Intel GPUs verfügbar:
```bash
./X-Plane-x86_64 --aftermath
```

Injiziert Checkpoints in den GPU-Commandstream. Bei Device Loss: Markers helfen, den GPU-Zustand zu rekonstruieren.

### 7.5 GDB für Crashes

```bash
cd ~/X-Plane\ 12/
gdb ./X-Plane-x86_64
(gdb) run
# Bei Crash:
(gdb) backtrace full
(gdb) thread apply all backtrace
```

**Core Dumps aktivieren:**
```bash
ulimit -c unlimited
./X-Plane-x86_64
```

Core-Dump-Pfad prüfen: `cat /proc/sys/kernel/core_pattern`

### 7.6 DataRef-Debugging

- **DataRefEditor** (Laminar, kostenlos): https://developer.x-plane.com/tools/datarefeditor/
- **DataRefTool** (Community, ab XP12.04+): https://datareftool.com/ — Regex-Suche, Change-Detection

**Quellen:**
- https://developer.x-plane.com/article/command-line-options/
- https://developer.x-plane.com/2025/05/whats-up-with-device-losses-in-x-plane-anyways/
- https://wiki.debian.org/HowToGetABacktrace

---

## 8. Bekannte Linux-spezifische Bugs (Versionshistorie)

| Problem | Version | Status |
|---------|---------|--------|
| Hängt bei IPv6-Abfrage (Kernel 6.9.0) | 12.1.0 | Behoben |
| Startet nur im Fenstermodus statt Vollbild | 12.1.0 | Behoben |
| Zink-Crash mit Plugins (AMD) | 12.1.0 | Behoben |
| X-Plane startet nicht mit AMD GPU | 12.2.0 | Behoben |
| Wasser/Vegetation falsch auf AMD GPUs | 12.2.0 | Behoben |
| Kein Vollbild auf manchen Linux-Installationen | 12.2.0 | Behoben |
| Startet nicht auf Ubuntu 24.10 mit NVIDIA | 12.2.0 | Behoben |
| Exposure Fusion fehlerhaft auf AMD GPUs | 12.3.0 | Behoben |
| Screenshot-Fehler mit AMD GPUs | 12.3.0 | Behoben |
| Wayland: Fenstergröße-Fehler | 12.1.4 | Behoben |
| Steam-Snap-Paket auf Linux | 12.2.1 | Behoben (Snap unsupported) |
| Crash mit Intel ARC GPUs | 12.3.0 | Behoben |
| Zink GPU-Auswahl bei Multi-GPU | 12.4.0 | Hinzugefügt |
| Ubuntu 20.04 LTS Support | 12.1.3 | Entfallen |
| Inkrementeller Memory-Leak NVIDIA ohne ReBar | 12.2.0 | Behoben |

**Quellen:**
- https://www.x-plane.com/kb/x-plane-12-1-0-release-notes/
- https://www.x-plane.com/kb/x-plane-12-2-0-release-notes/
- https://www.x-plane.com/kb/x-plane-12-3-0-release-notes/
- https://www.x-plane.com/kb/x-plane-12-4-0-release-notes/

---

## 9. Performance-Monitoring-Tools unter Linux

| Tool | GPU-Typ | Funktion |
|------|---------|----------|
| `nvidia-smi` | NVIDIA | GPU-Auslastung, VRAM, Temperatur |
| `radeontop` | AMD | GPU-Auslastung, VRAM |
| `intel_gpu_top` | Intel | GPU-Auslastung |
| `MangoHud` | Alle | In-Game Overlay (FPS, Frame-Time, GPU/CPU) |
| `htop` | — | CPU-Auslastung pro Kern |
| `GALLIUM_HUD` | Mesa | Echtzeit-Performance-Metriken |

---

## Quellenverzeichnis

### Offizielle X-Plane Dokumentation
- System Requirements: https://www.x-plane.com/kb/x-plane-12-system-requirements/
- Rendering Options: https://www.x-plane.com/kb/configuring-the-rendering-options/
- Best Performance: https://www.x-plane.com/kb/setting-the-rendering-options-for-best-performance/
- Linux Troubleshooting: https://www.x-plane.com/kb/linux-troubleshooting/
- PipeWire Audio: https://www.x-plane.com/kb/troubleshooting-audio-issues-with-pipewire-on-linux/
- Joysticks on Linux: https://www.x-plane.com/kb/using-joysticks-x-plane-11-linux-systems/
- Flight Controls: https://www.x-plane.com/kb/configuring-flight-controls/
- Frame Rate Test: https://www.x-plane.com/kb/frame-rate-test/
- Command Line Options: https://developer.x-plane.com/article/command-line-options/

### Developer Blog
- Plugin Flickering (Zink): https://developer.x-plane.com/2023/02/addressing-plugin-flickering/
- Device Losses: https://developer.x-plane.com/2025/05/whats-up-with-device-losses-in-x-plane-anyways/
- Multi-Core Future: https://developer.x-plane.com/2025/12/the-glorious-multi-core-future-is-now-the-boring-present/
- FMOD Sound: https://developer.x-plane.com/docs/sound/
- .joy File Spec: https://developer.x-plane.com/article/creating-joystick-configuration-joy-files/

### Release Notes
- 12.1.0: https://www.x-plane.com/kb/x-plane-12-1-0-release-notes/
- 12.2.0: https://www.x-plane.com/kb/x-plane-12-2-0-release-notes/
- 12.3.0: https://www.x-plane.com/kb/x-plane-12-3-0-release-notes/
- 12.4.0: https://www.x-plane.com/kb/x-plane-12-4-0-release-notes/

### Linux/Mesa/Vulkan
- Mesa Environment Variables: https://docs.mesa3d.org/envvars.html
- RADV Documentation: https://docs.mesa3d.org/drivers/radv.html
- AMDVLK Discontinued: https://github.com/GPUOpen-Drivers/AMDVLK/discussions/416

### Externe Quellen
- Phoronix Wayland vs X11: https://www.phoronix.com/review/wayland-nv-amd-2023/4
- GamingOnLinux Zink: https://www.gamingonlinux.com/2023/02/x-plane-12-now-uses-the-open-source-zink-driver-to-help-plugins/
- OpenAL Soft: https://github.com/kcat/openal-soft
- DataRefTool: https://github.com/leecbaker/datareftool
- Debian Backtrace: https://wiki.debian.org/HowToGetABacktrace
