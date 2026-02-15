# XCamera

XCamera ist ein Kamerasystem für [X-Plane](../glossary.md#x-plane) 11/12, das das Standard-View-System durch ein vollständig konfigurierbares, flugzeugspezifisches Kamera-Framework ersetzt.

## Hintergrund

- **Entwickler:** Stick and Rudder Studios
- **Website:** [stickandrudderstudios.com/x-camera](https://stickandrudderstudios.com/x-camera/)
- **Lizenz:** Kommerziell (Closed Source)
- **Plattformen:** Windows, macOS, Linux (native Binaries)
- **Kompatibilität:** X-Plane 11.3+ und X-Plane 12
- **Preis:** Kostenlose Version verfügbar; Registrierung für $18 USD (Einstellungen speichern, volle Airport-Kameras)

XCamera wird aktiv gepflegt. Das [Plugin](../glossary.md#plugin) ist ein eigenständiges XPLM-Plugin und benötigt weder FlyWithLua noch andere Scripting-Frameworks.

## Funktionsumfang

- **Custom Views:** Mehrere Kamera-Kategorien und Views pro Flugzeug, gespeichert in flugzeugspezifischen Konfigurationsdateien
- **Kamera-Übergänge:** Smooth- und Bezier-Curve-Transitionen zwischen Kameras, automatische Sequenzen
- **Airport-Kameras:** Automatisch generierte Kameras an Gates, Schildern, Runways und Tower-Positionen
- **Walk Mode / Free Camera:** Freie Bewegung per Tastatur im und um das Flugzeug
- **G-Loaded Camera:** Ersetzt ab X-Plane 12.4.1 die frühere Cinema-Verite-Funktion
- **External Cameras:** Konfigurierbare Außenansichten mit Orbit und Fly-by
- **AI Aircraft Views:** Blick aus der Perspektive von AI-Flugzeugen
- **Mini Control Panel:** Farbkodiertes dynamisches Panel für schnelle Kameraauswahl
- **Head Tracking:** TrackIR (Windows), OpenTrack (Linux/macOS, empfohlen), [LinuxTrack](linuxtrack.md) (nicht mehr gepflegt), SimHat (iPhone)

### Free vs. Registriert

- **Free:** Alle Funktionen nutzbar, aber erweiterte Einstellungen werden nicht gespeichert. Airport-Kameras sind eingeschränkt.
- **Registriert ($18 USD):** Einstellungen werden gespeichert, volle Airport-Kamera-Generierung. Ein 2.X-Key gilt für alle 2.X-Versionen.

## Mehrwert in der Flugsimulation

XCamera bietet hunderte flugzeugspezifische Kamerapositionen, die über die Community geteilt werden. Die Bezier-Übergänge zwischen Kameras erzeugen einen cinematischen Effekt, der bei Standard-Views fehlt. Airport-Kameras ermöglichen Außenansichten von Gate, Tower oder Runway — nützlich für realistische Anflug-Beobachtungen. Der Walk Mode erlaubt eine freie Erkundung des Flugzeugs und der Umgebung.

## Installation

**Download:** [stickandrudderstudios.com/x-camera/download-x-camera](https://stickandrudderstudios.com/x-camera/download-x-camera/) (Free-Version) oder [X-Plane.Org Store](https://store.x-plane.org/X-Camera_p_889.html) (Registriert)

Die ZIP-Datei nach `Resources/plugins/` entpacken. Es entsteht der Ordner `X-Camera/` mit der Linux-Binary unter `64/lin.xpl`.

Es werden keine zusätzlichen Systempakete benötigt. Es sind keine Linux-spezifischen Probleme bekannt.

### Head Tracking auf Linux

Für Head Tracking auf Linux wird **OpenTrack** empfohlen. LinuxTrack wird nicht mehr aktiv gepflegt.

**OpenTrack-Einrichtung**

1. OpenTrack installieren und konfigurieren (Eingabe: Webcam mit NeuralNet-Tracker, IR-Clip o.ä.)
2. In OpenTrack: Output auf "UDP over network" setzen
3. Das OpenTrack-eigene X-Plane-Plugin (im OpenTrack-Build enthalten) in `Resources/plugins/` ablegen und in X-Plane "Track Head Motion" aktivieren
4. In XCamera: Die "TrackIR"-Checkbox bei den gewünschten Views aktivieren — XCamera behandelt OpenTrack-Daten wie TrackIR-Daten

**OpenTrack auf Debian/Ubuntu installieren**

```bash
sudo apt install cmake qtbase5-dev libopencv-dev libprocps-dev
git clone https://github.com/opentrack/opentrack.git
cd opentrack && mkdir build && cd build
cmake .. && make -j$(nproc)
```

Alternativ stehen in einigen Distributionen fertige Pakete zur Verfügung.

## Quellen

- [X-Camera — Stick and Rudder Studios](https://stickandrudderstudios.com/x-camera/)
- [X-Camera — forums.x-plane.org](https://forums.x-plane.org/files/file/24209-x-camera-linmacwin-32-64/)
- [OpenTrack — GitHub](https://github.com/opentrack/opentrack)
- [OpenTrack X-Plane Plugin — im OpenTrack-Build enthalten](https://github.com/opentrack/opentrack/tree/master/x-plane-plugin)
