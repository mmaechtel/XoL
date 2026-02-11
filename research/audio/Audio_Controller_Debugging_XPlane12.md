# Audio, Controller-Konfiguration und Debugging in X-Plane 12

Research Paper -- Agent C
Datum: 2025-02-09

---

## Inhaltsverzeichnis

1. [Audio-Einstellungen in X-Plane 12](#1-audio-einstellungen-in-x-plane-12)
2. [Controller-Konfiguration in X-Plane 12](#2-controller-konfiguration-in-x-plane-12)
3. [Log-Dateien und Debugging](#3-log-dateien-und-debugging)
4. [Quellenverzeichnis](#4-quellenverzeichnis)

---

## 1. Audio-Einstellungen in X-Plane 12

### 1.1 Audio-Engine: FMOD

X-Plane 12 nutzt **FMOD Studio 2.02** als zentrale Audio-Engine. FMOD hat das ältere OpenAL-basierte System aus X-Plane 10/11 vollständig ersetzt.

- X-Plane 11 nutzte FMOD Studio 1.08.xx
- X-Plane 12 nutzt FMOD Studio 2.02.xx (konkret wird mindestens Version 2.02.19 für FMOD-Projekte vorausgesetzt)
- Die Umstellung ist abwärtskompatibel: ältere 1.08 Sound-Banks werden in XP12 geladen, aber das Live-Update-Feature erfordert FMOD Studio 2.02
- Ein Flugzeug nutzt entweder FMOD oder das Legacy-Soundsystem (OpenAL-basiert) -- Mischen ist nicht möglich

**Quelle:** [FMOD 2.0 Upgrade Notes -- X-Plane Developer](https://developer.x-plane.com/article/fmod-2-0-upgrade-notes/), [Using FMOD with X-Plane](https://developer.x-plane.com/article/using-fmod-with-x-plane/), [FMOD Sound -- X-Plane Developer](https://developer.x-plane.com/docs/sound/)

### 1.2 OpenAL: Status und Rolle

OpenAL ist **nicht vollständig abgelöst**, aber stark in den Hintergrund getreten:

- X-Plane 12 lädt OpenAL-Soft weiterhin beim Start (vor dem Laden von Plugins), damit Plugins die Bibliothek nutzen können
- Auf Linux wird die dynamische Bibliothek vom System-Loader gefunden, da X-Plane sie bereits geladen hat
- OpenAL dient primär noch als Audio-API für ältere Plugins und Legacy-Flugzeuge ohne FMOD-Soundbanks
- Es gibt **keine Garantie**, dass OpenAL auf jedem System verfügbar ist (Nutzer können Sound deaktivieren)
- Private OpenAL-Kontexte sind auf Linux und macOS generell sicher nutzbar

**Aktuelle OpenAL-Soft-Version (upstream):** 1.25.1 (20. Januar 2025)

Wichtige Releases:
| Version | Datum | Kernaenderungen |
|---------|-------|-----------------|
| 1.25.1 | 2025-01-20 | Fixes: OpenSL, JACK, WASAPI, CoreAudio Capture, HRTF-Debug-Assertions |
| 1.25.0 | 2024-12-22 | Codebase auf C++20 aktualisiert, 4th-Order-Ambisonics, CAF-Support |
| 1.24.3 | 2024-03-30 | fmtlib-Build-Fixes, dynamische WASAPI-Enumerierung, neue bsinc48-Resampler |
| 1.24.2 | 2024-01-11 | AL_SOFT_bformat_hoa-Extension, PulseAudio Default-Device-Change-Events |
| 1.24.0 | 2023-11-16 | Codebase auf C++17, ALC_SOFT_system_events, AL_EXT_debug |

**OpenAL-Soft Konfiguration auf Linux:**
- Konfiguration per User und per System moeglich ueber `alsoftrc.sample`
- Unterstuetzte Backends: PipeWire, PulseAudio, ALSA
- CMake-Output zeigt an, welche Backends erkannt wurden

**Quelle:** [OpenAL -- X-Plane Developer](https://developer.x-plane.com/article/openal/), [GitHub: kcat/openal-soft](https://github.com/kcat/openal-soft), [Releases](https://github.com/kcat/openal-soft/releases)

### 1.3 FMOD Sound-Bus-Hierarchie (XPLMSound API)

Die XPLMSound-API definiert 11 Audio-Busse (XPLMAudioBus-Enumeration):

| Bus-Konstante | Wert | Beschreibung |
|--------------|------|-------------|
| `xplm_AudioRadioCom1` | 0 | Eingehende Sprache auf COM1 |
| `xplm_AudioRadioCom2` | 1 | Eingehende Sprache auf COM2 |
| `xplm_AudioRadioPilot` | 2 | Eigene Sprache des Piloten |
| `xplm_AudioRadioCopilot` | 3 | Eigene Sprache des Copiloten |
| `xplm_AudioExteriorAircraft` | 4 | Flugzeug-Aussengeraeusche |
| `xplm_AudioExteriorEnvironment` | 5 | Umgebungsgeraeusche aussen |
| `xplm_AudioExteriorUnprocessed` | 6 | Unverarbeitete Aussengeraeusche |
| `xplm_AudioInterior` | 7 | Cockpit-/Kabinengeraeusche |
| `xplm_AudioUI` | 8 | User-Interface-Sounds |
| `xplm_AudioGround` | 9 | Bodenfahrzeug-Sounds |
| `xplm_Master` | 10 | Master-Bus (selten direkt genutzt) |

Zusaetzlich gibt es zwei FMOD-Bank-IDs:
- **xplm_MasterBank**: Verwaltet Flugzeug- und Umgebungsaudio
- **xplm_RadioBank**: Verwaltet COM1/COM2/GND/Pilot/Copilot-Kanaele

Die FMOD-Bus-Hierarchie in X-Plane ist:
- **Master** (Eltern-Bus, keine Signalverarbeitung, nur Gesamtlautstaerke)
    - **Interior** (Cockpit-Innensounds)
    - **Exterior Processed** (verarbeitete Aussengeraeusche)
        - **Environment** (Umgebungs- und Wettersounds)
    - **Exterior Unprocessed** (unverarbeitete Aussengeraeusche)
    - **Radios** (COM1, COM2, Morse, Marker)
    - **UI** (Interface-Sounds)
    - **Ground** (Bodenfahrzeuge)

Das Master-Bus-Format muss auf "Surround 5.1 on Desktop" gesetzt sein; X-Plane mischt automatisch fuer die tatsaechliche Lautsprecherkonfiguration.

**Quelle:** [XPLMSound API -- X-Plane Developer](https://developer.x-plane.com/sdk/XPLMSound/), [FMOD 2.0 Upgrade Notes](https://developer.x-plane.com/article/fmod-2-0-upgrade-notes/)

### 1.4 Audio-Einstellungen im X-Plane-Menue

Zugang: **Settings > Sound** (Mauszeiger an den oberen Bildschirmrand bewegen, Settings-Icon klicken, dann Sound).

**Lautstaerkeregler (Slider):**

X-Plane 12 bietet 8 Lautstaerkeregler (X-Plane 11 hatte 7). Die Slider steuern die relativen Lautstaerken aller Sounds. Standardmaessig stehen alle auf 100% (Slider ganz rechts).

Basierend auf den SDK-Bus-Definitionen und Release Notes sind die Slider-Kategorien:
1. **Master** -- Gesamtlautstaerke
2. **Interior** -- Cockpit-Innensounds
3. **Exterior** -- Aussengeraeusche des Flugzeugs
4. **Environment** -- Umgebungsgeraeusche (Wind, Regen, Verkehr)
5. **Radios** -- COM/RAMP-Funkverkehr (in 12.2.0 korrigiert, dass dieser Slider korrekt funktioniert)
6. **Copilot** -- Copilot-Sprache
7. **UI** -- Bedienoberflaeche
8. **Pilot** -- Eigene Sprache (neu in XP12)

*Anmerkung: Die exakten Slider-Labels konnten nicht aus einer einzelnen offiziellen Quelle verifiziert werden. Die obige Liste ist abgeleitet aus der XPLMSound-API, den Release Notes und dem B2VolumeControl-Plugin (8 Knoepfe fuer XP12). Eine definitive Liste erfordert Pruefung direkt im Simulator.*

**Weitere Audio-Optionen:**
- ATC-Sound und -Text ein-/ausschalten
- Pilotenstimme: maennlich/weiblich
- Sound Device: Auswahl des FMOD-Ausgabegeraets (relevant fuer PipeWire/PulseAudio-Auswahl unter Linux)
- Speech Synthesis Status wird angezeigt (aller interner ATC-Funk ist voraufgezeichnet, kein TTS)

**Sound-Datarefs (bekannt):**
- `sim/operation/sound/inside_ratio` -- Array-Dataref: Wie weit "innen" sich die Kamera in jedem Sound-Space befindet (0-1)
- `sim/operation/sound/radio_volume_ratio` -- Float (0-1): COM-Radio-Lautstaerke
- `sim/operation/sound/master_volume_ratio` -- Float (0-1): Master-Lautstaerke

*Anmerkung: Eine vollstaendige Dataref-Liste ist nur ueber DataRefEditor/DataRefTool im laufenden Simulator einsehbar.*

**Quelle:** [X-Plane 12 Desktop Manual](https://www.x-plane.com/manuals/desktop/), [X-Plane 12.2.0 Release Notes](https://www.x-plane.com/kb/x-plane-12-2-0-release-notes/)

### 1.5 3D-Audio / Spatial Audio

X-Plane 12 unterstuetzt vollstaendig **3D Spatial Audio** ueber FMOD:

- FMOD verwaltet alle raeumlichen Informationen relativ zur aktuellen Kameraposition
- **Sound Cones**: Jeder FMOD-Kanal kann einen Richtungskegel erhalten (Orientierungsvektor in lokalen Koordinaten). Innerhalb des Kegels wird Sound mit voller Lautstaerke gehoert; ausserhalb wird er reduziert
- Sound-Quellen werden automatisch als 3D markiert, wenn ein Richtungskegel gesetzt wird
- **Fade Distance**: Entfernungsbasiertes Ausblenden ist konfigurierbar (XPLMSetAudioFadeDistance-API)
- **Position**: 3D-Position jeder Soundquelle wird relativ zur Kamera gesetzt (XPLMSetAudioPosition-API)

Praktisch bedeutet das:
- Motor- und Propellergeraeusche bewegen sich mit dem Flugzeug
- Umgebungsgeraeusche (anderer Verkehr) sind raeumlich korrekt positioniert
- Beim Wechsel zwischen Innen- und Aussenkamera aendert sich die Akustik

**Quelle:** [XPLMSound API](https://developer.x-plane.com/sdk/XPLMSound/), [XPMP2 Sound Support](https://twinfan.github.io/XPMP2/Sound.html)

### 1.6 Linux-spezifische Audio-Besonderheiten

#### FMOD unter Linux

X-Plane nutzt FMOD, und FMOD kommuniziert direkt mit dem Linux-Audiosystem. X-Plane selbst kuemmert sich nicht um die Audio-Infrastruktur -- es ist FMOD, das mit PulseAudio, PipeWire oder ALSA spricht.

**FMOD-Erkennung der Audio-Backends:**
1. FMOD prueft standardmaessig, ob PulseAudio verfuegbar ist (via `/usr/bin/pulseaudio --check`)
2. Auf PipeWire-Systemen existiert diese Binary typischerweise **nicht**
3. Fallback: FMOD nutzt den PipeWire-ALSA-Sink

**PipeWire-Kompatibilitaet:**
- Seit FMOD Studio 2.02.05 ist PipeWire offiziell unterstuetzt
- Fuer optimale Kompatibilitaet sollten installiert sein:
    - `pipewire-pulse` (PulseAudio-Kompatibilitaetsschicht)
    - `pipewire-alsa` (ALSA-Kompatibilitaetsschicht)
- In X-Plane 12: Sound Device im Settings-Menue explizit auf "pipewire" oder ein spezifisches ALSA-Device setzen

**Workaround bei fehlender PulseAudio-Erkennung:**

Wenn FMOD PulseAudio nicht erkennt (und damit nicht die pipewire-pulse-Bruecke nutzt), kann ein Symlink helfen:
```bash
sudo ln -s /bin/true /usr/bin/pulseaudio
```
Damit besteht FMODs PulseAudio-Check und Audio wird ueber pipewire-pulse geroutet.

**Umgebungsvariable:**
- `FMOD_ALSA_DEVICE=pulse` -- erzwingt PulseAudio-Backend in FMOD
- Nutzbar auch fuer FMOD Studio selbst: `FMOD_ALSA_DEVICE=pulse fmodstudio`

#### Haeufige Linux-Audio-Probleme

**Audio-Crackling / Knistern:**
- Ursache: Buffer-Underruns bei hoher CPU-Last
- Loesungen:
    - PipeWire: `default.clock.min-quantum = 1024` in pipewire.conf setzen
    - Headroom und Period-Size in pipewire-pulse.conf erhoehen
    - Autosuspend in PipeWire deaktivieren
- X-Plane-spezifisch: `--no_sound` als Diagnose-Flag nutzen, um Audioprobleme zu isolieren

**Samplerate-Mismatch:**
- X-Plane/FMOD erwartet typischerweise 48 kHz
- PipeWire-Konfiguration: `default.clock.rate = 48000` in pipewire.conf
- Sample-Rate-Switching aktivieren fuer automatische Anpassung

**Audio nach Standby/Resume:**
- Kein X-Plane-spezifisches Problem, sondern PipeWire/PulseAudio-seitig
- `systemctl --user restart pipewire pipewire-pulse` als Workaround

**Quelle:** [Troubleshooting audio issues with PipeWire on Linux -- X-Plane](https://www.x-plane.com/kb/troubleshooting-audio-issues-with-pipewire-on-linux/), [FMOD 2.0 Upgrade Notes](https://developer.x-plane.com/article/fmod-2-0-upgrade-notes/)

---

## 2. Controller-Konfiguration in X-Plane 12

### 2.1 Geraeteerkennung: SDL2

X-Plane nutzt **SDL2** (Simple DirectMedia Layer) fuer die Erkennung von Eingabegeraeten. SDL2 verwendet auf Linux zwei Backend-Treiber in Prioritaetsreihenfolge:

1. **HIDAPI** (hoechste Prioritaet): Direkter HID-Zugriff auf bekannte Controller (Xbox, PlayStation 4/5, Nintendo Switch Pro). Liefert konsistenteres Verhalten ueber alle Plattformen
2. **evdev** (Fallback): Generisches Linux-Kernel-Interface fuer alle anderen Controller. Nutzt die Kernel-Joystick-Events (/dev/input/event*)

Erkennungslogik: SDL2 initialisiert die Treiber in der Prioritaetsreihenfolge. Der erste Treiber, der ein Geraet beansprucht, erhaelt exklusiven Zugriff. HIDAPI hat Vorrang bei unterstuetzten Geraeten.

Seit X-Plane 11.10: Wenn ein USB-Geraet entweder eine Achse, einen Button oder einen Hat-Switch praesentiert, behandelt X-Plane es als Joystick.

**Quelle:** [Using Joysticks in X-Plane 11 on Linux Systems](https://www.x-plane.com/kb/using-joysticks-x-plane-11-linux-systems/), [SDL Joystick and Gamepad System (DeepWiki)](https://deepwiki.com/libsdl-org/SDL/5.1-joystick-and-gamepad-system)

### 2.2 Linux-Berechtigungen und udev-Regeln

**Kernproblem:** Linux sperrt standardmaessig den Zugriff auf Input-Devices fuer normale Benutzer. X-Plane sollte **niemals als root (sudo)** gestartet werden.

**Loesung: udev-Regeln**

Beispiel fuer eine udev-Regel:
```
KERNEL=="event*", ATTRS{idProduct}=="0bd4", ATTRS{idVendor}=="06a3", MODE="0666"
```

- `idVendor` und `idProduct` identifizieren das spezifische Geraet
- `MODE="0666"` gibt allen Nutzern Lese-/Schreibzugriff
- VID/PID ermitteln via `lsusb -n`
- Regel in `/etc/udev/rules.d/` ablegen (z.B. `99-joystick.rules`)
- Aktivieren: `sudo udevadm control --reload-rules && sudo udevadm trigger`

**Bekanntes Problem:** Joysticks koennen unter Linux vom Kernel erkannt werden (jstest-gtk funktioniert), aber SDL2 erkennt sie nicht -- meist wegen fehlender udev-Berechtigungen auf die evdev-Nodes.

**Quelle:** [Using Joysticks in X-Plane 11 on Linux Systems](https://www.x-plane.com/kb/using-joysticks-x-plane-11-linux-systems/), [SDL Issue #12397](https://github.com/libsdl-org/SDL/issues/12397)

### 2.3 Kalibrierung in X-Plane

Zugang: **Settings > Joystick & Equipment**

#### Achsen-Zuordnung (Axis Tab)
- Alle Achsen des Joysticks durch den vollen Bewegungsbereich bewegen
- Farbcodierung: **Gruen** = zugewiesen und kalibriert, **Rot** = nicht kalibriert
- Primaere Achsen: Pitch, Roll, Yaw, Throttle
- Nicht genutzte Hardware-Achsen muessen auf "none" gesetzt werden
- **"Use this position as center"**: Korrigiert Hardware, die nicht praezise in die Neutralstellung zurueckkehrt

#### Erwartete Input-Werte (Diagnose ueber Data Input & Output)
| Position | Wert |
|----------|------|
| Stick zentriert | ca. 0.0 |
| Voller Querruder links | ca. -1.0 |
| Voller Querruder rechts | ca. +1.0 |
| Voller Hoehenruder zurueck | ca. +1.0 |
| Voller Hoehenruder vor | ca. -1.0 |
| Volles Seitenruder links | ca. -1.0 |
| Volles Seitenruder rechts | ca. +1.0 |

#### Nullzone / Dead Zone (Nullzone Tab)
- Drei Slider fuer Pitch, Roll und Yaw
- Hoehere Prozentwerte erzeugen groessere tote Zonen, in denen Joystick-Bewegung keine Flugzeugreaktion erzeugt
- Sinnvoll bei Geraeten mit Jitter oder Drift

#### Empfindlichkeitskurven / Response Curves (Nullzone Tab)
- Drei Slider fuer Pitch, Roll, Yaw
- **Links**: Lineare Antwort (50% Stick = 50% Steuerausschlag)
- **Rechts**: Kurvige Antwort (gedaempft nahe der Mitte, empfindlich an den Extremen)
- Ermoeglicht praezise Hoehensteuerung nahe Neutral bei vollem Steuerweg an den Raendern

#### Stabilitaetsunterstuetzung (Stability Augmentation)
- Separate Slider im oberen linken Bereich
- Automatische Steuereingaben zum Leveln, Rollstabilisierung und Gier-Korrektur
- Slider nach rechts = mehr Unterstuetzung, weniger Reaktionsfaehigkeit

#### Button-Zuordnung
- **Buttons: Basic Tab**: Button druecken, dann Funktion zuweisen. Schalter koennen getrennte Funktionen fuer "up" und "down" haben
- **Buttons: Adv Tab**: Zugang zu erweiterten Command-Funktionen (vollstaendige Command-Liste aus `Resources/plugins/Commands.txt`)

#### Force Feedback (XP12-Neuerung)
- Ab X-Plane 12.00: Force-Feedback-Achsen koennen mit dem "ffb"-Tag markiert werden
- Verhindert ungewollte Trim-Akkumulation bei FFB-Joysticks

**Quelle:** [Configuring Flight Controls -- X-Plane](https://www.x-plane.com/kb/configuring-flight-controls/), [My Joystick or Yoke Isn't Working](https://www.x-plane.com/kb/my-joystick-or-yoke-isnt-working/)

### 2.4 Joystick-Konfigurationsdateien

#### Dateitypen und Speicherorte

| Dateityp | Pfad (relativ zu X-Plane-Root) | Beschreibung |
|----------|-------------------------------|--------------|
| `.joy` | `Resources/joystick configs/` | Geraetedefinitionen mit Grafiken und Standardzuweisungen |
| `.prf` | `Output/preferences/` | Benutzerspezifische Joystick-Einstellungen |
| Joystick Settings | `Output/preferences/X-Plane Joystick Settings.prf` | Hauptdatei fuer Joystick-Konfiguration |

Unter Linux liegen diese relativ zum X-Plane-Installationsverzeichnis, typischerweise:
```
/home/<user>/X-Plane 12/Output/preferences/
/home/<user>/X-Plane 12/Resources/joystick configs/
```

#### .joy-Dateiformat (Spezifikation)

Textbasiertes Format, eingefuehrt in X-Plane 11.

**Header:**
```
1100 version
OS: Linux
Name: Thrustmaster T.16000M
```

**Geraeteidentifikation:**
- Per Name: Betriebssystem-Gerätename
- Per USB-ID: `VID:0x046D PID:0xC214` (Hex oder Dezimal)

**View-Sektionen:**
- PNG-Bilder des Controllers mit Annotationen fuer Buttons und Achsen
- Mehrere Views moeglich (Vorderseite, Rueckseite, Throttle-Quadrant)
- Bilder sollten 2000x2000 Pixel nicht ueberschreiten

**Button-Definitionen:**
```
Button 0: 150 200
Button 1 (Trigger): 180 220
```

**Achsen-Definitionen:**
```
Axis 0 (x): 100 150
Axis 1 (y): 100 200
Axis Group (Stick): 0 1
```

**Hat Switches:**
- Vier Buttons in Up/Right/Down/Left-Reihenfolge gruppierbar

**Assignments-Sektion:**
- Achsenzuweisungen: pitch, roll, yaw, throttle, collective, brakes, prop, mixture, flaps, etc.
- Button-Zuweisungen: Sim-Commands aus `Resources/plugins/Commands.txt`
- Empfehlung: Assignments ueber X-Plane-UI generieren ("Save as Default for [device]")

**Erweiterte Features (XP11.20+):**
- Konfigurationsgruppen fuer verwandte Steuerelemente
- Exklusive Gruppen (Single-Choice-Auswahl)
- Self-Centering-Achsen als lineare Controls via Delta-Bewegung
- Achsen koennen Custom-Commands basierend auf Stick-Position ausloesen

**Phantom Controls:** Nicht existierende Achsen/Buttons als "hidden" markieren

**Kalibrierung:** `Calibration: Relaxed` fuer Custom-Hardware mit eingeschraenktem Bereich

**.prf-Datei:**
- Textbasiert, editierbar
- Enthaelt Device-HID/VID-Nummern, `_joy_location`-Eintraege
- Nullzone-Werte als `_joy_null0`, `_joy_null1`, etc.

**Backup und Wiederherstellung:**
- Gesamtes `Output/preferences/`-Verzeichnis sichern
- Alternativ: nur `X-Plane Joystick Settings.prf` sichern
- Reset: Datei loeschen, X-Plane erstellt sie beim naechsten Start neu

**Quelle:** [Joystick Configuration (.joy) File Specification -- X-Plane Developer](https://developer.x-plane.com/article/creating-joystick-configuration-joy-files/)

### 2.5 Bekannte Controller-Probleme unter Linux

**Geraet wird von X-Plane nicht erkannt:**
- Haeufigste Ursache: Fehlende udev-Berechtigungen auf evdev-Nodes
- SDL2 nutzt `/dev/input/event*` (nicht `/dev/input/js*`)
- Pruefen: `ls -la /dev/input/event*` -- muss fuer den Nutzer lesbar sein

**Joystick funktioniert in jstest-gtk, aber nicht in X-Plane:**
- SDL2 hat eigene Erkennungslogik, die von der Kernel-Joystick-API abweichen kann
- Loesung: udev-Regeln spezifisch fuer evdev-Nodes erstellen

**Achsen invertiert oder vertauscht:**
- X-Plane: "Reverse"-Checkbox in den Axis Settings
- Linux-seitig: `jscal` fuer Kalibrierung, persistent ueber udev

**Geraet verschwindet nach Standby/Resume:**
- USB-Autosuspend kann Controller deaktivieren
- Loesung: Autosuspend deaktivieren per udev-Regel oder sysfs:
  ```bash
  echo -1 > /sys/bus/usb/devices/<device>/power/autosuspend
  ```

**Mehrfacherkennung / Phantomachsen:**
- Einige Geraete melden sich als mehrere Input-Devices
- X-Plane kann Phantom-Achsen anzeigen, die es nicht gibt
- `.joy`-Datei: Phantom-Controls als "hidden" markieren

**Linux-spezifische .joy-Dateien in XP12:**
- HOTAS Warthog: In X-Plane 12.00 hinzugefuegt
- VKB Gladiator MK II: In X-Plane 12.00 hinzugefuegt
- VirtualFly: In X-Plane 12.1.0 hinzugefuegt
- RealSimGear: In X-Plane 12.1.0 hinzugefuegt

**Quelle:** [Using Joysticks in X-Plane 11 on Linux Systems](https://www.x-plane.com/kb/using-joysticks-x-plane-11-linux-systems/), [SDL Issue #1314: Joystick calibration impossible on Linux](https://github.com/libsdl-org/SDL/issues/1314), [X-Plane 12.00 Release Notes](https://www.x-plane.com/kb/x-plane-12-00-release-notes/), [X-Plane 12.1.0 Release Notes](https://www.x-plane.com/kb/x-plane-12-1-0-release-notes/)

---

## 3. Log-Dateien und Debugging

### 3.1 Log.txt: Pfad und Aufbau

**Pfad unter Linux:**
```
<X-Plane 12 Installationsverzeichnis>/Log.txt
```
Typischerweise: `/home/<user>/X-Plane 12/Log.txt`

**Verhalten:**
- Log.txt wird bei **jedem Start** neu geschrieben (ueberschrieben)
- **Ab X-Plane 12.2.0**: Log-Rotation! Bis zu vier Kopien werden aufbewahrt:
    - `Log.txt` (aktuell)
    - `Log.1.txt`, `Log.2.txt`, `Log.3.txt` (aelter)
    - Gleiches fuer `Log_ATC.txt`
    - Aeltere Logs werden in `Output/Log Archive/` verschoben
    - Dateinamen enthalten Datum/Zeitstempel basierend auf letztem Aenderungsdatum
- Separate Log-Dateien fuer Plane Maker und Airfoil Maker (ab 12.2.0)

**Typische Sektionen im Log.txt:**

1. **Header / Build-Info:**
   - X-Plane-Version, Build-Nummer, Kompilierungsdatum
   - Beispiel: `Log.txt for X-Plane 12.2.0`

2. **Systeminformationen:**
   - CPU-Informationen (Modell, Kerne, Taktrate)
   - RAM-Groesse
   - Betriebssystem und Kernel-Version

3. **GPU/Vulkan-Initialisierung:**
   - Erkannte Vulkan-Layers
   - Vulkan-Geraet (z.B. `Vulkan Device : NVIDIA GeForce RTX 3070`)
   - VRAM-Information
   - Shader-Kompilierung

4. **Plugin-Laden:**
   - Jedes Plugin mit Pfad und Identifier
   - Beispiel: `Loaded: /home/user/X-Plane 12/Resources/plugins/BetterPushback/lin_x64/BetterPushback.xpl (skiselkov.BetterPushback)`

5. **Geraeteerkennung:**
   - Erkannte Joysticks/Controller
   - Audio-Device-Auswahl

6. **Laufzeit-Meldungen:**
   - Warnungen, Fehler, Performance-Hinweise

**Quelle:** [X-Plane 12.2.0 Release Notes](https://www.x-plane.com/kb/x-plane-12-2-0-release-notes/)

### 3.2 Wichtige Log-Eintraege erkennen

#### GPU-/Vulkan-Initialisierung
- **Erfolg:** `Vulkan Device : <GPU-Name>` mit VRAM-Info
- **Fehler:** `Failed to find a suitable device`, `Failed to find Vulkan runtime`
- **Device Loss:** `Encountered Vulkan device loss error!` -- GPU-Crash waehrend der Laufzeit
- **Zink:** Meldungen ueber Zink-Driver-Nutzung (OpenGL-ueber-Vulkan-Translation)

#### Plugin-Fehler
- `Loaded:` gefolgt von Pfad -- erfolgreicher Plugin-Load
- Fehlende Plugins: keine `Loaded:`-Zeile fuer erwartetes Plugin
- Fehlermeldungen mit Plugin-Namen deuten auf Inkompatibilitaet hin
- `ldd lin.xpl` auf Linux: Fehlende Shared Libraries identifizieren

#### Performance-Warnungen
- FPS-bezogene Meldungen
- VRAM-Allokationsfehler (besonders mit Zink: ab 12.2.0 werden Fehlermeldungen angezeigt)
- Texture-Mipmap-Warnungen (ab 12.2.0 unterdrueckt, wenn Mipmap-Levels differieren)

#### Crash-Indikatoren
- `Encountered Vulkan device loss error` -- GPU-Crash
- NaN-Werte in Systemen (XP12 loggt diese ausfuehrlich)
- Stack Traces bei Abstuerzen
- ATC-bezogene Crashes (mehrere in 12.1.0 und 12.2.0 behoben)

### 3.3 Debug-Modi und Kommandozeilenparameter

#### Allgemeine Nutzung unter Linux
```bash
cd "/home/user/X-Plane 12/"
./X-Plane-x86_64 --<option>
```

Vollstaendige Liste aller Optionen:
```bash
./X-Plane-x86_64 --help
```

#### Dokumentierte Kommandozeilenparameter

**Sound:**
| Parameter | Beschreibung |
|-----------|-------------|
| `--no_sound` | Startet ohne Sound-Initialisierung (isoliert Audio-Probleme) |

**Video/GPU (Deaktivierung):**
| Parameter | Beschreibung |
|-----------|-------------|
| `--no_vbos` | Deaktiviert Vertex Buffer Objects |
| `--no_fbos` | Deaktiviert Framebuffer Objects |
| `--no_pbos` | Deaktiviert Pixelbuffer Objects |
| `--no_sprites` | Deaktiviert Point Sprites (Runway Lights) |
| `--no_pixel_counters` | Deaktiviert Pixel Counter (Sonnblendung) |
| `--no_aniso_filtering` | Deaktiviert anisotrope Texturfilterung |
| `--no_hw_mipmap` | Deaktiviert HW-beschleunigte Mipmap-Erstellung |
| `--no_fshaders` | Deaktiviert Fragment Shader |
| `--no_vshaders` | Deaktiviert Vertex Shader |
| `--no_glsl` | Deaktiviert GLSL |
| `--no_threaded_ogl` | Deaktiviert Multi-Threaded OpenGL |

**Video/GPU (Erzwingen):**
| Parameter | Beschreibung |
|-----------|-------------|
| `--use_vbos` | Erzwingt VBOs |
| `--use_sprites` | Erzwingt Point Sprites |
| `--use_fshaders` | Erzwingt Fragment Shader |
| `--use_vshaders` | Erzwingt Vertex Shader |
| `--use_glsl` | Erzwingt GLSL |
| `--force_run` | Ignoriert Mindestanforderungen |

**Performance-Testing:**
| Parameter | Beschreibung |
|-----------|-------------|
| `--fps_test=N` | Frame-Rate-Test (3-stelliger Code: Hundert=Viewpoint, Zehn=Wetter, Einer=Rendering) |
| `--require_fps=N` | Pass/Fail-Modus (Exit 0 wenn FPS > N, sonst Exit 1) |
| `--load_smo=<path>` | Replay-Movie laden |
| `--verbose` | Per-Frame-Daten ausgeben fuer statistische Analyse |
| `--log_path=<path>` | Log-Ausgabe umleiten |
| `--pref:name=value` | Einzelne Settings ueberschreiben |

**Testing/Scripting:**
| Parameter | Beschreibung |
|-----------|-------------|
| `--testing` | Aktiviert Telnet-Testing-Interface (Port 49000) |
| `--script=<file>` | Fuehrt Test-Script aus (.txt oder .test) |

**GPU-Crash-Analyse (ab 12.2.0):**
| Parameter | Beschreibung |
|-----------|-------------|
| `--aftermath` | Aktiviert GPU-Crash-Datensammlung (NVIDIA, AMD, Intel) |

**FPS-Test-Code-Struktur (3-stellig):**
- Hunderter (Viewpoint): 0=Cockpit, 1=Oben, 2=Nacht-Cockpit
- Zehner (Wetter): 0-7 (verschiedene Wolken-/Sichtbedingungen)
- Einer (Rendering): 1=Low, 2=Medium, 3=High, 4=Very High, 5=Extreme

**Quelle:** [Command Line Options -- X-Plane Developer](https://developer.x-plane.com/article/command-line-options/), [Benchmarking Using the Frame Rate Test](https://www.x-plane.com/kb/frame-rate-test/), [Testing in X-Plane](https://developer.x-plane.com/article/testing-in-x-plane/)

### 3.4 DataRef-Debugging

#### DataRefEditor (Laminar Research)
- **Kompatibilitaet:** X-Plane 11 und 12
- **Installation:** `DataRefEditor`-Ordner in `X-Plane 12/Resources/Plugins/` kopieren
- **Zugang:** Plugins > Data Ref Editor > Show Data Refs
- **Funktionen:**
    - Anzeige aller 2000+ Datarefs mit aktuellen Werten
    - Werte aendern durch Links-/Rechtsklick
    - Filterung: Textfragment im Suchfeld eingeben (Gross-/Kleinschreibung beachten!)
    - Art Controls und Sim Stats ueber separate Menuepunkte (sim/private/ Domain)
    - Array-Datarefs: Slider am unteren Fensterrand zum Navigieren (Index +1 oder +100)
    - Mehrere DRE-Fenster gleichzeitig moeglich
- **Download:** [DataRefEditor -- X-Plane Developer](https://developer.x-plane.com/tools/datarefeditor/)

#### DataRefTool (Lee C. Baker)
- **Kompatibilitaet:** X-Plane 12.04+ (Version 2.2.0+), nutzt neue API fuer Dataref-Suche
- **Plattformen:** Windows 10+, macOS 11+, Linux
- **Vorteile gegenueber DataRefEditor:**
    - Case-insensitive Suche
    - Regex-Suche
    - Change-Detection: Filtert nur kuerzlich geaenderte Datarefs
    - Command-Erkennung: Zeigt kuerzlich ausgefuehrte Commands
    - Plugin/Scenery/Aircraft Reload on demand
    - Watch-Window fuer bestimmte Datarefs
- **Download:** [datareftool.com](https://datareftool.com/download/)

**Quelle:** [DataRefEditor](https://developer.x-plane.com/tools/datarefeditor/), [DataRefTool](https://datareftool.com/), [GitHub: leecbaker/datareftool](https://github.com/leecbaker/datareftool)

### 3.5 Developer Mode / Debug Menu

**In-Sim Developer Features:**
- `sim/operation/show_fps` -- Togglet On-Screen-FPS-Anzeige
- `sim/operation/dev_console` -- Togglet Developer Console
- Developer Menu > Show Data Output Graph -- Zeigt FPS-Daten als In-Sim-Graph
- Developer Menu: Zugang zu erweiterten Diagnose-Funktionen

**Telnet-Testing (ab --testing Flag):**
```bash
./X-Plane-x86_64 --testing
# In einem anderen Terminal:
telnet localhost 49000
```

Verfuegbare Telnet-Commands:
- `acf <path>` -- Flugzeug laden
- `move lle <lat> <lon> <ele>` -- Flugzeug positionieren
- `move <ICAO>` -- Flugzeug an Flughafen platzieren
- `command <cmd> [duration]` -- Sim-Command ausfuehren
- `expect <dataref> <op> <value>` -- Dataref-Wert pruefen
- `wait <seconds>` -- Pause
- `dref set <dataref> <value>` -- Dataref setzen
- `camera dump` -- Aktuelle Kameraposition ausgeben
- `camera <params>` -- Kamera setzen

**CLI Tab Completion (ab 12.1.0):**
- Tab-Completion fuer Sim-Commands
- Help-Tips im Terminal

**Quelle:** [Testing in X-Plane](https://developer.x-plane.com/article/testing-in-x-plane/), [X-Plane 12.1.0 Release Notes](https://www.x-plane.com/kb/x-plane-12-1-0-release-notes/)

### 3.6 GPU-Debugging

#### Vulkan Validation Layers
- Vulkan hat **keine eingebauten Validation Layers**
- Bereitgestellt durch das **LunarG Vulkan SDK**
- Unter Debian/Ubuntu: `sudo apt install vulkan-validationlayers`
- Aktivierung: `VK_INSTANCE_LAYERS=VK_LAYER_KHRONOS_validation ./X-Plane-x86_64`
- Validation Layers geben Debug-Meldungen auf stdout aus
- **Achtung:** Massive Performance-Einbussen! Nur fuer Debugging nutzen

#### MicroProfile (integriert)
- X-Plane integriert MicroProfile, eine Open-Source-Bibliothek fuer Performance-Analyse
- Zeigt Frame-Time-Breakdowns: welche Rendering-Tasks wieviel Zeit verbrauchen
- Ermoeglicht praezise Identifikation von Performance-Engpaessen

#### RenderDoc
- Capture-Support in X-Plane 12 wiederhergestellt (seit 12.00, XPD-13899)
- Ermoeglicht Frame-by-Frame GPU-Analyse

#### Aftermath (GPU-Crash-Analyse)
- **Seit X-Plane 11.50:** NVIDIA Aftermath-Support
- **Seit X-Plane 12.2.0:** Massiv ueberarbeitet, jetzt auch AMD und Intel GPUs
- Starten mit `--aftermath` Flag oder `X-Plane_aftermath.bat` (Windows) / direkt via CLI (Linux)
- Funktionsweise:
    - Injiziert Checkpoints in den GPU-Commandstream bei jeder Draw/Dispatch-Operation
    - Bei Device Loss: Markers helfen, den GPU-Programmzustand zu rekonstruieren
    - Produziert "GPU Crash"-Reports statt generischer Device-Loss-Meldungen
- **Trade-off:** Performance-Overhead, aber unschaetzbare Diagnosedaten
- Device Losses sind **nicht** durch zu wenig VRAM oder Add-ons verursacht

**Verbesserungen bei Device Losses:**
- 12.06: ~75% weniger Device Losses
- 12.1.0: NVIDIA-Treiber-Bug behoben, weitere Reduktion
- 12.2.0: Aftermath mit Per-Command-Checkpoint-Injection fuer alle GPU-Hersteller

**Quelle:** [Vulkan and Metal: Testing and Bug Fighting](https://developer.x-plane.com/2019/12/vulkan-and-metal-testing-and-bug-fighting/), [What's up with device losses in X-Plane anyways?](https://developer.x-plane.com/2025/05/whats-up-with-device-losses-in-x-plane-anyways/), [X-Plane 12.2.0 Release Notes](https://www.x-plane.com/kb/x-plane-12-2-0-release-notes/)

### 3.7 GDB-Nutzung fuer X-Plane Crashes

**GDB starten:**
```bash
cd "/home/user/X-Plane 12/"
gdb ./X-Plane-x86_64
(gdb) run
```

**Bei Crash Backtrace erhalten:**
```
(gdb) backtrace 20
```
Zeigt die Aufrufkette (bis zu 20 Ebenen) an der Stelle, wo X-Plane gestoppt hat.

**Ausfuehrliche Analyse:**
```
(gdb) backtrace full
(gdb) info registers
(gdb) x/16i $pc
(gdb) thread apply all backtrace
```

**Logging in Datei:**
```
(gdb) set logging file gdb-xplane.txt
(gdb) set logging on
(gdb) backtrace full
(gdb) set logging off
```

**Core Dumps aktivieren (falls kein Core Dump erzeugt wird):**
```bash
ulimit -c unlimited
./X-Plane-x86_64
```

**Core Dump analysieren:**
```bash
gdb ./X-Plane-x86_64 core
(gdb) backtrace full
```

**Core-Dump-Speicherorte unter Linux:**
- Standardmaessig im Arbeitsverzeichnis der Anwendung
- systemd: `/var/lib/systemd/coredump/` (komprimiert mit zstd)
- apport (Ubuntu): `/var/crash/`
- Pfad pruefen: `cat /proc/sys/kernel/core_pattern`

**Hinweise:**
- X-Plane erzeugt auf Linux einfache Backtrace-Dateien (nicht Minidumps wie auf Windows)
- Plugin-Crashes: Plugin-Code nutzt `backtrace()` und `backtrace_symbols()` -- diese sind **nicht signal-safe** und dienen nur der Demonstration
- Fuer robustere Crash-Analyse: libunwind verwenden

**Quelle:** [Crash Handling -- X-Plane Developer](https://developer.x-plane.com/code-sample/crash-handling/), [HowToGetABacktrace -- Debian Wiki](https://wiki.debian.org/HowToGetABacktrace)

### 3.8 Crash-Reports

**Speicherorte:**
- **Log.txt** (Hauptdiagnose-Datei, immer zuerst pruefen)
- **backtrace.txt** (im X-Plane-Arbeitsverzeichnis, wenn Plugin-Crash-Handler aktiv)
- **crash_dump.dmp** (Windows: Minidump; Linux: nicht standardmaessig)
- **Core Dumps** (Linux: abhaengig von `core_pattern`-Konfiguration)

**Lesen von Crash-Reports:**
1. Log.txt: Letzte Zeilen vor dem Crash pruefen
2. GPU-Abschnitt: Vulkan-Device-Loss-Meldungen
3. Plugin-Abschnitt: Welche Plugins geladen waren
4. Performance-Daten: Gab es Speicherprobleme?

**Verbesserungen in 12.2.0+:**
- Verbesserte Logging bei Device-Loss-Fehlern
- Verbesserte Logging fuer fehlende Scenery
- Verbesserte SDK-Fehlerbehandlung und -Logging
- Reduzierte ueberfluessige Logging-Ausgabe waehrend VR-Controller-Erkennung

**Linux-spezifische Fixes in juengeren Releases:**
- 12.1.0: IPv6-Haenger bei Kernel 6.9.0+ behoben (XPD-15378)
- 12.1.0: Linux-Steam CTD bei Locale-Setup behoben (XPD-15347)
- 12.1.0: Zink-Crashes auf Linux behoben (XPD-15411)
- 12.2.0: Fullscreen-Start auf einigen Linux-Installationen behoben
- 12.2.0: Ubuntu 24.10 mit NVIDIA GPUs -- Startproblem behoben
- 12.2.0: AMD GPU Linux-Startproblem behoben
- 12.2.0: WebKit-Warnung auf Linux wenn nicht ladbar
- 12.4.0: GPU-Auswahl fuer Zink bei Multi-GPU-Systemen

**Quelle:** [X-Plane 12.1.0 Release Notes](https://www.x-plane.com/kb/x-plane-12-1-0-release-notes/), [X-Plane 12.2.0 Release Notes](https://www.x-plane.com/kb/x-plane-12-2-0-release-notes/), [X-Plane 12.4.0 Release Notes](https://www.x-plane.com/kb/x-plane-12-4-0-release-notes/)

---

## 4. Quellenverzeichnis

### Offizielle X-Plane-Dokumentation

| Thema | URL |
|-------|-----|
| FMOD Sound (Hub) | https://developer.x-plane.com/docs/sound/ |
| FMOD 2.0 Upgrade Notes | https://developer.x-plane.com/article/fmod-2-0-upgrade-notes/ |
| Using FMOD with X-Plane | https://developer.x-plane.com/article/using-fmod-with-x-plane/ |
| Sound (.snd) File Format | https://developer.x-plane.com/article/sound-snd-file-format-specification/ |
| OpenAL in X-Plane | https://developer.x-plane.com/article/openal/ |
| XPLMSound API | https://developer.x-plane.com/sdk/XPLMSound/ |
| Joystick .joy File Spec | https://developer.x-plane.com/article/creating-joystick-configuration-joy-files/ |
| Command Line Options | https://developer.x-plane.com/article/command-line-options/ |
| Testing in X-Plane | https://developer.x-plane.com/article/testing-in-x-plane/ |
| Crash Handling (Code Sample) | https://developer.x-plane.com/code-sample/crash-handling/ |
| DataRefEditor | https://developer.x-plane.com/tools/datarefeditor/ |
| X-Plane Datarefs | https://developer.x-plane.com/datarefs/ |
| Vulkan/Metal Bug Fighting | https://developer.x-plane.com/2019/12/vulkan-and-metal-testing-and-bug-fighting/ |
| Device Losses in X-Plane | https://developer.x-plane.com/2025/05/whats-up-with-device-losses-in-x-plane-anyways/ |

### X-Plane Knowledge Base

| Thema | URL |
|-------|-----|
| Desktop Manual | https://www.x-plane.com/manuals/desktop/ |
| Configuring Flight Controls | https://www.x-plane.com/kb/configuring-flight-controls/ |
| Joystick Troubleshooting | https://www.x-plane.com/kb/my-joystick-or-yoke-isnt-working/ |
| Joysticks on Linux | https://www.x-plane.com/kb/using-joysticks-x-plane-11-linux-systems/ |
| PipeWire Audio Troubleshooting | https://www.x-plane.com/kb/troubleshooting-audio-issues-with-pipewire-on-linux/ |
| Command Line Usage | https://www.x-plane.com/kb/using-command-line-options/ |
| Frame Rate Test | https://www.x-plane.com/kb/frame-rate-test/ |

### Release Notes

| Version | URL |
|---------|-----|
| 12.00 | https://www.x-plane.com/kb/x-plane-12-00-release-notes/ |
| 12.1.0 | https://www.x-plane.com/kb/x-plane-12-1-0-release-notes/ |
| 12.1.2 | https://www.x-plane.com/kb/x-plane-12-1-2-release-notes/ |
| 12.2.0 | https://www.x-plane.com/kb/x-plane-12-2-0-release-notes/ |
| 12.2.1 | https://www.x-plane.com/kb/x-plane-12-2-1-release-notes/ |
| 12.4.0 | https://www.x-plane.com/kb/x-plane-12-4-0-release-notes/ |

### Externe Projekte

| Projekt | URL |
|---------|-----|
| OpenAL Soft (GitHub) | https://github.com/kcat/openal-soft |
| OpenAL Soft Releases | https://github.com/kcat/openal-soft/releases |
| DataRefTool | https://datareftool.com/ |
| DataRefTool (GitHub) | https://github.com/leecbaker/datareftool |
| XPMP2 Sound Support | https://twinfan.github.io/XPMP2/Sound.html |
| SDL Joystick System | https://deepwiki.com/libsdl-org/SDL/5.1-joystick-and-gamepad-system |
| SDL Issue #12397 | https://github.com/libsdl-org/SDL/issues/12397 |
| SDL Issue #1314 | https://github.com/libsdl-org/SDL/issues/1314 |

### Linux/Systemdokumentation

| Thema | URL |
|-------|-----|
| Debian Backtraces | https://wiki.debian.org/HowToGetABacktrace |
| Arch Linux Core Dump | https://wiki.archlinux.org/title/Core_dump |
| Arch Linux Gamepad | https://wiki.archlinux.org/title/Gamepad |

---

## Offene Punkte / Luecken

Die folgenden Punkte konnten nicht mit ausreichender Quellenqualitaet belegt werden:

1. **Exakte SDL-Version in X-Plane 12:** Ob X-Plane SDL2 oder SDL3 (bzw. sdl2-compat) bundelt, konnte aus keiner offiziellen Quelle bestimmt werden. Pruefung moeglich via `ldd X-Plane-x86_64 | grep SDL` auf einer Installation.

2. **Vollstaendige Liste der 8 Sound-Slider-Labels:** Die exakten UI-Labels der 8 Lautstaerkeregler konnten nicht aus einer einzelnen offiziellen Quelle extrahiert werden. Die abgeleitete Liste (Abschnitt 1.4) ist plausibel, aber unbestätigt. Verifizierung erfordert Screenshot oder Pruefung im laufenden Simulator.

3. **Vollstaendige Sound-Datarefs:** Die sim/operation/sound/*-Datarefs sind nur fragmentarisch dokumentiert. Vollstaendige Liste nur ueber DataRefEditor/DataRefTool im Simulator einsehbar.

4. **X-Plane 12 Log.txt exakte Sektionsstruktur:** Kein offizielles Dokument beschreibt die genaue Gliederung der Log.txt. Die beschriebene Struktur (Abschnitt 3.1) ist aus Beispielen und Referenzen zusammengesetzt.

5. **Exakter Pfad fuer Crash-Backtrace auf Linux:** X-Plane schreibt auf Linux "einfache Backtraces" -- der genaue Dateiname und Pfad ist nicht offiziell dokumentiert. Vermutlich im X-Plane-Root als backtrace.txt oder direkt in Log.txt.
