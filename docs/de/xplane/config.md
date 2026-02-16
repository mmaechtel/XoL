# X-Plane Konfiguration unter Linux

X-Plane 12 ist eine Cross-Plattform-Anwendung — die allgemeinen Grafikeinstellungen (Texturen, Schatten, Wolken, Antialiasing) funktionieren auf allen Betriebssystemen gleich und sind in der [offiziellen Dokumentation](https://www.x-plane.com/kb/configuring-the-rendering-options/) beschrieben. Diese Seite behandelt ausschließlich, was unter Linux **anders** ist.

## Vulkan und Zink

X-Plane 12 nutzt ausschließlich Vulkan als Rendering-API. Ein OpenGL-Fallback existiert nicht.

**Treiber-Anforderungen (Vulkan 1.3)**

| GPU | Treiber | Mindestversion |
|-----|---------|---------------|
| NVIDIA | Proprietärer Treiber | 510+ |
| AMD | Mesa RADV | 22.0+ |
| Intel Arc | Mesa ANV | In neueren Versionen unterstützt |

Für NVIDIA-Treiber-Installation und -Optimierung siehe [Nvidia Treiber](../optimizations/nvidia.md).

### Zink — Plugin-Kompatibilität

Viele X-Plane-Plugins nutzen OpenGL für ihre Darstellung (z.B. Cockpit-Displays, Overlays). Da X-Plane 12 aber ausschließlich Vulkan verwendet, muss das OpenGL-Rendering der Plugins übersetzt werden. X-Plane liefert dafür den [Zink](../glossary.md#zink)-Treiber mit — eine Übersetzungsschicht, die OpenGL-Befehle in Vulkan-Befehle umwandelt.

**Warum das unter Linux besonders relevant ist**

- Ohne Zink versucht der Treiber, OpenGL und Vulkan gleichzeitig zu koordinieren (Native Interop). Das kostete bis zu 10 ms pro Frame, in Extremfällen 30 ms
- Mit Zink: messbar 50 FPS → 80 FPS in Tests von Laminar Research
- AMD-GPUs ([RADV](../glossary.md#radv)) profitieren am stärksten — die native OpenGL/Vulkan-Interop war auf Mesa besonders problematisch
- NVIDIA: Zink-Support hat eine wechselhafte Geschichte — der Status wechselt zwischen Releases und kann sich mit Updates ändern

**Bekannte Einschränkung:** Shared OpenGL Contexts für Hintergrundverarbeitung in Plugins sind mit Zink nicht vollständig stabil. Für allgemeine OpenGL-Fehlerdiagnose bei Plugins kann `--debug_gl` nützlich sein.

## Shader-Cache

X-Plane 12 verwendet unter Linux zwei unabhängige Shader-Cache-Systeme. Wenn nach einem Treiberupdate Grafikfehler auftreten oder die Performance unerklärlich schlecht ist, kann es helfen, einen oder beide Caches zu löschen.

### X-Plane-eigener Cache

Enthält vorkompilierte Vulkan-Pipeline-Objekte.

- **Pfad:** `<X-Plane 12>/Output/shadercache/vulkan/`
- Löschen: Verzeichnisinhalt entfernen. Wird beim nächsten Start automatisch neu aufgebaut (kann mehrere Minuten dauern)

### Mesa Shader-Cache (nur AMD/Intel)

Der Mesa-Treiberstack cacht zusätzlich die vom ACO-Compiler erzeugten Shader.

- **Standard-Pfad:** `~/.cache/mesa_shader_cache/` (ab Mesa 24.2: `~/.cache/mesa_shader_cache_db/`)
- **Standard-Maximum:** 1 GB

Cache auf schnellere SSD umleiten oder vergrößern:

```bash
export MESA_SHADER_CACHE_DIR=/pfad/zur/schnellen/ssd/mesa_cache
export MESA_SHADER_CACHE_MAX_SIZE=2G
```

NVIDIA nutzt einen eigenen internen Shader-Cache, der nicht über Mesa konfiguriert wird.

## Umgebungsvariablen

Einige Mesa/RADV-Variablen können für X-Plane unter Linux nützlich sein. Setzen per Launch-Script oder direkt vor dem Aufruf:

```bash
MESA_VK_WSI_PRESENT_MODE=mailbox ./X-Plane-x86_64
```

**Nützliche Variablen (AMD/Intel mit Mesa)**

| Variable | Empfohlener Wert | Effekt |
|----------|-----------------|--------|
| `MESA_VK_WSI_PRESENT_MODE` | `mailbox` | Tearing-frei bei niedriger Latenz. Alternative: `immediate` (niedrigste Latenz, aber Tearing) |
| `MESA_SHADER_CACHE_MAX_SIZE` | `2G` | Shader-Cache vergrößern (Standard: 1 GB) |
| `MESA_SHADER_CACHE_DIR` | Pfad | Shader-Cache auf schnelleren Datenträger umleiten |

!!! warning "NVIDIA: `__GL_*`-Variablen — nicht pauschal setzen"
    `__GL_THREADED_OPTIMIZATIONS` und `__GL_YIELD` betreffen ausschließlich OpenGL und haben unter X-Plane 12 (Vulkan) **keinen Effekt**.

    `__GL_SYNC_TO_VBLANK` dagegen wirkt auch auf Vulkan — allerdings nur bei aktivem VSync (FIFO-Präsentationsmodus). Mit `__GL_SYNC_TO_VBLANK=0` wird das VSync auf Treiberebene ausgehebelt, obwohl X-Plane es aktiviert hat. **Empfehlung:** VSync über die X-Plane-Einstellungen steuern, nicht über Umgebungsvariablen.

    Weitere `__GL_*`-Variablen mit Vulkan-Wirkung: `__GL_SHARPEN_ENABLE` (Image Sharpening) und `__GL_SHOW_GRAPHICS_OSD` (Performance-Overlay).

!!! note "Experimentell: NVIDIA Smooth Motion (RTX 40/50)"
    `NVPRESENT_ENABLE_SMOOTH_MOTION=1` aktiviert KI-basierte Frame-Interpolation auf Treiberebene. Der NVIDIA-Treiber generiert per Tensor Cores einen interpolierten Zwischenframe zwischen jedem gerenderten Frame und verdoppelt so die wahrgenommene Framerate — ohne Engine-Integration.

    X-Plane 12 hat kein natives DLSS Frame Generation, daher ist Smooth Motion derzeit die einzige Möglichkeit für treiberbasierte Frame-Generierung. Erfordert mindestens Treiber 580.82 (RTX 40) bzw. 575.51 (RTX 50). Automatisch wird Low Latency Mode aktiviert, um die zusätzliche Eingabelatenz zu kompensieren.

    Start per Launch-Script: `NVPRESENT_ENABLE_SMOOTH_MOTION=1 ./X-Plane-x86_64`

    **Bekannte Einschränkungen:** Berichte über Flickering, Vulkan-Fehler und Artefakte bei schnellen Blickwechseln existieren in der X-Plane-Community. Die Qualität liegt unter nativem DLSS Frame Generation, da keine Motion Vectors aus der Engine genutzt werden. Trotzdem: der Autor dieser Dokumentation hat mit Smooth Motion unter X-Plane bereits sehr gute Ergebnisse erzielt — es lohnt sich, die Option auszuprobieren.

!!! note "Experimentell: Variable Rate Shading"
    `RADV_FORCE_VRS=2x2` kann auf RDNA2+ GPUs (RX 6000 und neuer) 10-30% FPS-Gewinn bringen, reduziert aber die Bildqualität. **Nicht mit X-Plane getestet** — Artefakte möglich.

## Display-Server

X-Plane 12 hat keine native Wayland-Unterstützung. Details zur Session-Wahl, Latenzmessungen und GPU-spezifischen Empfehlungen: [Display-Server](../optimizations/displayserver.md).

!!! tip "Empfehlung: X11-Session verwenden"
    Unter X11 kommuniziert X-Plane direkt mit dem X-Server — keine Übersetzung, kein Overhead. Details: [X11-Session für X-Plane](../optimizations/displayserver_x11.md)

Bei Fullscreen-Problemen unter Wayland kann `--window=1920x1080` als Workaround dienen (siehe [Fehlerbehebung](#diagnose-start-mit-cli-parametern)).

## Audio

X-Plane 12 nutzt [FMOD](../glossary.md#fmod) Studio 2.02 als Audio-Engine. Unter Debian 12 (PulseAudio) funktioniert Audio in der Regel ohne Konfiguration.

!!! tip "PipeWire: Kein Sound?"
    Unter PipeWire (Debian 13 Standard, in Debian 12 Standard für GNOME, optional für andere DEs) erkennt FMOD das Audiosystem manchmal nicht. FMOD prüft `/usr/bin/pulseaudio --check` — auf reinen PipeWire-Systemen existiert diese Binary nicht.

    Lösung:

    ```bash
    sudo apt install pipewire-pulse pipewire-alsa
    # Falls das allein nicht reicht:
    sudo ln -s /bin/true /usr/bin/pulseaudio
    ```

    Offizieller Troubleshooting-Artikel: [PipeWire Audio Issues](https://www.x-plane.com/kb/troubleshooting-audio-issues-with-pipewire-on-linux/)

    Zur Diagnose: `--no_sound` startet X-Plane ohne Audio-Initialisierung und isoliert Audio-Probleme.

## Controller

X-Plane erkennt Controller unter Linux über SDL2 mit [evdev](../glossary.md#evdev)-Backend (`/dev/input/event*`). Damit das funktioniert, braucht der Nutzer Leserechte auf die Input-Devices — **X-Plane darf niemals als root gestartet werden**.

### udev-Regeln

Wenn ein Controller nicht erkannt wird, fehlen meist die Berechtigungen. Die offizielle Anleitung beschreibt die Grundlagen: [Using Joysticks on Linux](https://www.x-plane.com/kb/using-joysticks-x-plane-11-linux-systems/)

Darüber hinaus lassen sich mit eigenen udev-Regeln Berechtigungen setzen, stabile Symlinks anlegen und die Gerätezuordnung dauerhaft festlegen — besonders nützlich bei Setups mit mehreren Controllern.

**Schritt 1: Device-IDs ermitteln**

Zunächst die angeschlossenen USB-Controller auflisten:

```bash
lsusb | grep -i -E "thrustmaster|logitech|saitek|vkb|virpil|winwing"
```

Für die udev-Regel werden Vendor-ID und Product-ID benötigt. Die Details eines bestimmten Event-Devices anzeigen:

```bash
# Event-Nummer ermitteln (Joystick-Devices filtern):
cat /proc/bus/input/devices | grep -A 4 "Thrustmaster"

# Vollständige Attribut-Hierarchie für die udev-Regel:
udevadm info --attribute-walk --name=/dev/input/event<N>
```

Relevante Felder: `idVendor`, `idProduct`, optional `serial` (die meisten Flight-Sim-Controller haben keine Seriennummer).

**Schritt 2: Regel-Datei erstellen**

```bash
sudo nano /etc/udev/rules.d/70-flight-controllers.rules
```

```ini
# Thrustmaster T.16000M FCS — Berechtigungen + Symlink
KERNEL=="event*", SUBSYSTEM=="input", ATTRS{idVendor}=="044f", ATTRS{idProduct}=="b10a", \
  MODE="0660", GROUP="input", SYMLINK+="input/flight-stick"

# Logitech/Saitek Pro Flight Rudder Pedals
KERNEL=="event*", SUBSYSTEM=="input", ATTRS{idVendor}=="06a3", ATTRS{idProduct}=="0764", \
  MODE="0660", GROUP="input", SYMLINK+="input/flight-rudder"
```

Die Vendor- und Product-IDs (`044f:b10a` etc.) durch die eigenen Werte aus Schritt 1 ersetzen.

**Schritt 3: Regeln aktivieren**

```bash
sudo udevadm control --reload-rules
sudo udevadm trigger --subsystem-match=input
```

Alternativ: Gerät abstecken und wieder einstecken. Symlinks prüfen:

```bash
ls -la /dev/input/flight-*
```

!!! tip "Identische Geräte unterscheiden"
    Zwei gleiche Controller (z.B. zwei TCA-Quadranten) haben die gleiche VID:PID und meist keine Seriennummer. Die einzige stabile Unterscheidung ist der **physische USB-Port-Pfad**.

    Port-Pfad ermitteln:

    ```bash
    udevadm info --query=path --name=/dev/input/event<N>
    ```

    In der Regel dann zusätzlich nach `KERNELS` filtern (z.B. `KERNELS=="3-2.1"` für den Port). **Wichtig:** Die Geräte müssen immer am gleichen USB-Port eingesteckt bleiben.

    X-Plane identifiziert Controller intern per VID:PID über SDL2 und nutzt keine Symlinks. Bei identischen Geräten kann die Zuordnung trotz udev-Regeln zwischen Neustarts wechseln. Als Workaround lässt sich die Reihenfolge über die SDL2-Umgebungsvariable erzwingen:

    ```bash
    SDL_JOYSTICK_DEVICE=/dev/input/by-path/<pfad-1>:/dev/input/by-path/<pfad-2> ./X-Plane-x86_64
    ```

    Die stabilen Pfade unter `/dev/input/by-path/` sind an den physischen USB-Port gebunden und ändern sich nicht.

### Konfigurationsdateien

| Datei | Pfad (relativ zu X-Plane 12) | Inhalt |
|-------|------------------------------|--------|
| `.joy` | `Resources/joystick configs/` | Gerätedefinitionen |
| `.prf` | `Output/preferences/` | Benutzerspezifische Zuweisungen |

Backup: Das gesamte `Output/preferences/`-Verzeichnis sichern. Reset: `X-Plane Joystick Settings.prf` löschen — wird beim nächsten Start neu erstellt.

### Häufige Probleme

- **Gerät nicht erkannt:** SDL2 nutzt `/dev/input/event*`, nicht `/dev/input/js*`. Wenn das Gerät in `jstest-gtk` funktioniert aber nicht in X-Plane → udev-Regeln für evdev-Nodes prüfen
- **Gerät verschwindet nach Standby:** USB-Autosuspend deaktivieren — siehe [Systemtuning](../system/systemtuning.md)
- **Phantomachsen / Mehrfacherkennung:** Einige Geräte melden sich als mehrere Input-Devices. In der `.joy`-Datei können Phantom-Controls als "hidden" markiert werden
- **Achsen invertiert:** "Reverse"-Checkbox in den X-Plane Achsen-Einstellungen

Zur Diagnose: `--no_joysticks` startet X-Plane ohne Controller-Initialisierung (siehe [Fehlerbehebung](#diagnose-start-mit-cli-parametern)).

## Fehlerbehebung

### Log-Dateien

X-Plane schreibt bei jedem Start eine neue `Log.txt` im Installationsverzeichnis.

**Log-Rotation (in neueren Versionen)**

- Bis zu 4 Kopien: `Log.txt` (aktuell), `Log.1.txt`, `Log.2.txt`, `Log.3.txt`
- Ältere Logs werden in `Output/Log Archive/` mit Zeitstempel archiviert
- Separate `Log_ATC.txt` mit eigenem Rotationszyklus

**Was suchen?**

- **GPU-Initialisierung:** `Vulkan Device :` zeigt erkannte GPU und VRAM
- **Plugin-Probleme:** `Loaded:` gefolgt von Plugin-Pfad bestätigt erfolgreiches Laden. Fehlt eine Zeile → Plugin wurde nicht geladen
- **Device Loss:** `Encountered Vulkan device loss error!` — GPU-Crash während der Laufzeit

### Diagnose-Start mit CLI-Parametern

Die Kommandozeile ist unter Linux das mächtigste Werkzeug zur Fehlersuche. Statt X-Plane über den Launcher zu starten:

```bash
cd ~/X-Plane\ 12/
./X-Plane-x86_64 --<option>
```

**Szenario: X-Plane startet nicht oder crasht**

```bash
# Grafik-Problem? Nur Grafik im Safe Mode:
./X-Plane-x86_64 --safe_mode=GFX

# Plugin-Problem? Nur Plugins deaktivieren:
./X-Plane-x86_64 --safe_mode=PLG

# Mehrere Subsysteme gleichzeitig:
./X-Plane-x86_64 --safe_mode=PLG,SCN

# Alles im Safe Mode:
./X-Plane-x86_64 --safe_mode
```

Die `--safe_mode`-Optionen im Detail:

| Option | Deaktiviert |
|--------|------------|
| `GFX` | Grafik-Einstellungen zurückgesetzt |
| `PLG` | Alle Plugins |
| `SCN` | Custom Scenery |
| `ART` | Art Controls |
| `UI` | UI-Einstellungen zurückgesetzt |

**Szenario: Audio oder Controller funktionieren nicht**

```bash
# Ohne Sound starten (isoliert PipeWire/PulseAudio):
./X-Plane-x86_64 --no_sound

# Ohne Controller starten (isoliert evdev/udev):
./X-Plane-x86_64 --no_joysticks

# Ohne Netzwerk (isoliert IPv6/Netzwerk-Probleme):
./X-Plane-x86_64 --disable_networking
```

**Szenario: Fullscreen-Probleme unter Wayland**

```bash
# Fenstermodus erzwingen:
./X-Plane-x86_64 --window=1920x1080

# Oder Vollbild mit expliziter Auflösung:
./X-Plane-x86_64 --full=2560x1440
```

**Szenario: Performance testen / vergleichen**

```bash
# Reproduzierbarer Benchmark (Cockpit, klares Wetter, High Quality):
./X-Plane-x86_64 --fps_test=003 --verbose --weather_seed=42

# Pass/Fail-Test für Scripting (mindestens 30 FPS):
./X-Plane-x86_64 --fps_test=003 --require_fps=30
```

Der `--fps_test`-Code ist dreistellig: Hunderterstelle = Kameraposition (0=Cockpit, 1=Draufsicht), Zehnerstelle = Wetter (0-7), Einerstelle = Qualität (1=Low bis 5=Extreme). Der Test läuft 90 Sekunden und schreibt Ergebnisse in `Log.txt`.

**Launch-Scripte mit Profilen**

Mit `--pref` und `--dref` lassen sich Einstellungen per Kommandozeile überschreiben — nützlich für verschiedene Startprofile:

```bash
# DataRef beim Start setzen:
./X-Plane-x86_64 --dref:sim/private/controls/rain/kill_it=1

# Preference überschreiben:
./X-Plane-x86_64 --pref:_is_full_res=1
```

!!! note "Vollständige Parameterliste"
    `./X-Plane-x86_64 --help` zeigt alle verfügbaren Optionen. Viele der dort aufgeführten `--no_vbos`, `--no_fbos` etc. sind OpenGL-Legacy-Flags und unter X-Plane 12 (Vulkan) irrelevant.

### GPU-Debugging

**Aftermath (GPU-Crash-Analyse)**

X-Plane kann bei GPU-Crashes (Device Loss) detaillierte Diagnosedaten sammeln — für alle GPU-Hersteller (NVIDIA, AMD, Intel):

```bash
./X-Plane-x86_64 --aftermath
```

Aftermath injiziert Checkpoints in den GPU-Commandstream. Bei einem Device Loss helfen diese Markers, den GPU-Zustand zum Zeitpunkt des Fehlers zu rekonstruieren. Performance-Overhead vorhanden, aber die Diagnosedaten sind bei wiederkehrenden GPU-Crashes unverzichtbar. Für ein tieferes Verständnis von Device Losses und ihren Ursachen siehe [Geräteverluste](geraeteverluste.md).

**Vulkan Validation Layers**

Für tiefgehende Vulkan-Diagnose:

```bash
sudo apt install vulkan-validationlayers
VK_INSTANCE_LAYERS=VK_LAYER_KHRONOS_validation ./X-Plane-x86_64
```

!!! warning "Nur für Debugging"
    Validation Layers verursachen massive Performance-Einbußen. Nur aktivieren, wenn gezielt nach Vulkan-Fehlern gesucht wird.

### Crash-Analyse mit GDB

Bei wiederholten Crashes kann GDB einen Backtrace liefern:

```bash
cd ~/X-Plane\ 12/
gdb ./X-Plane-x86_64
(gdb) run
# Nach dem Crash:
(gdb) backtrace full
(gdb) thread apply all backtrace
```

**Core Dumps aktivieren** (falls kein Core Dump erzeugt wird):

```bash
ulimit -c unlimited
./X-Plane-x86_64
```

Core-Dump-Pfad prüfen: `cat /proc/sys/kernel/core_pattern`

Unter systemd liegen Core Dumps in `/var/lib/systemd/coredump/` (komprimiert).

## Quellen

Die wichtigsten Quellen zu den auf dieser Seite behandelten Themen:

- [Addressing Plugin Flickering](https://developer.x-plane.com/2023/02/addressing-plugin-flickering/) — Laminar-Research-Blogpost zur Zink-Integration und OpenGL/Vulkan-Interop
- [Mesa Environment Variables](https://docs.mesa3d.org/envvars.html) — Offizielle Mesa-Dokumentation für Shader-Cache, Present-Mode und Treibervariablen
- [PipeWire Audio Troubleshooting](https://www.x-plane.com/kb/troubleshooting-audio-issues-with-pipewire-on-linux/) — Offizieller X-Plane-KB-Artikel zu FMOD und PipeWire-Kompatibilität
- [Using Joysticks on Linux](https://www.x-plane.com/kb/using-joysticks-x-plane-11-linux-systems/) — Offizieller X-Plane-Guide für udev-Regeln und Controller-Berechtigungen
- [Vulkan Specification](https://registry.khronos.org/vulkan/) — Khronos-Group-Vulkan-API-Spezifikation und -Referenz
- [NVIDIA Driver README: Environment Variables](https://download.nvidia.com/XFree86/Linux-x86_64/570.86.16/README/openglenvvariables.html) — Offizielle Dokumentation der `__GL_*`-Variablen inkl. Vulkan-Wirkung
- [NVIDIA Driver README: Smooth Motion](https://download.nvidia.com/XFree86/Linux-x86_64/580.95.05/README/nvpresent.html) — Offizielle Dokumentation der KI-basierten Frame-Interpolation
- [Mesa Vulkan Drivers](https://docs.mesa3d.org/vulkan.html) — Mesa-Dokumentation für RADV, ANV und andere Vulkan-Treiberimplementierungen

## Hintergrund: Antialiasing und Rendering

??? abstract "Technischer Hintergrund: Anti-Aliasing in X-Plane"

    #### Aliasing und Abtastung

    Aliasing ist ein Phänomen, das durch die diskrete Abtastung eines kontinuierlichen Signals entsteht, wie durch das **Nyquist-Shannon-Theorem** beschrieben. Dieses Theorem besagt, dass die Abtastfrequenz mindestens doppelt so hoch wie die höchste Signal-Frequenz sein muss, um Aliasing-Artefakte zu vermeiden. In der Computergrafik führt eine unzureichende Abtastfrequenz zu Treppeneffekten, insbesondere an Kanten, die nicht mit dem Pixelgitter ausgerichtet sind.

    #### AA-Techniken in X-Plane 12

    **FXAA (Fast Approximate Anti-Aliasing)** ist eine Post-Processing-Technik zur Kantenglättung. Sie ist rechenleistungsschonend und benötigt keinen zusätzlichen Speicher, kann aber zu unscharfen Instrumenten führen, besonders bei 1080p. Bei 4K-Auflösungen zeigt FXAA bessere Ergebnisse. Ab Version 12.1.0 ist FXAA als separater Schalter verfügbar, ab 12.4.0 werden Cockpit-Displays von FXAA ausgenommen (bessere Lesbarkeit).

    **MSAA (Multi-Sample Anti-Aliasing)** ist eine hardware-implementierte Technik mit Abdeckungsmaske pro Pixel. Sie ist besonders effektiv an geometrischen Kanten, hat aber Schwierigkeiten mit transparenten Geometrien. In X-Plane 12.1 wurden diese Probleme durch Alpha-to-Coverage und Alpha-to-One verbessert.

    X-Plane nutzt Deferred Rendering, bei dem Metadaten in einem G-Buffer gespeichert werden. Dies reduziert Overdraw, erhöht jedoch die Komplexität bei MSAA, da Beleuchtungsschritte pro Sample ausgeführt werden müssen.

    #### Treiberbasierte MSAA

    MSAA kann auch über den Grafiktreiber erzwungen werden. Dies führt zu einer schnelleren Ausführung, aber auch zu ungenauerer Beschattung, da die komplexe X-Plane Renderpipeline nicht berücksichtigt wird.

    #### Empfehlung

    Für optimale Bildqualität: FSR deaktivieren (Regler auf Maximum), dann MSAA schrittweise erhöhen und Performance prüfen. FXAA optional aktivieren, wobei die Auswirkung auf die Bildschärfe zu berücksichtigen ist. Falls das nicht ausreicht, bietet ein Monitor mit höherer Auflösung die effektivste Verbesserung.

??? abstract "Technischer Hintergrund: PBR und Innenraumbeleuchtung"

    #### Physically Based Rendering

    Die Beleuchtung in X-Plane basiert auf **Physically Based Rendering (PBR)**, was zu realistischen, aber auch komplexen Lichteffekten führt. Materialien werden durch ihre Umgebung beeinflusst — ein Cockpit in einem pinkfarbenen Hangar würde eine entsprechende Tönung annehmen. Wetterbedingungen wie ein orangefarbener Sonnenuntergang wirken sich auf die Cockpitbeleuchtung aus.

    #### Bekannte Einschränkungen

    Die aktuelle Renderpipeline von X-Plane hat einige technische Einschränkungen. Jeder Pixel wird unabhängig und parallel berechnet, ohne Kontext über die umgebende Geometrie. Besonders bei schmalen Geometrien wie Cockpitkanten oder Flügelkurven können ungewollt Licht von der Umgebung aufgenommen werden.

    Screen-Space Reflections (SSR) können zu sichtbaren Artefakten führen — schimmernde Reflexionen auf nassem Asphalt oder ungleichmäßige Reflexionen durch fehlende Strahlkohärenz. Eine vollständige Lösung würde erhebliche Rechenleistung erfordern.

    #### Entwicklung

    Ab Version 12.2.0 wurde das Tone-Mapping auf AgX umgestellt und Exposure Fusion für Innenansichten eingeführt, was die Balance zwischen hellen und dunklen Bereichen verbessert. SSAO wurde für Bäume, Gebäude und Flugzeuge rekalibriert. Die Optimierung der Innenraumbeleuchtung hat laut Laminar Research weiterhin hohe Priorität.
