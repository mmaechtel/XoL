---
description: "OpenTrack Head-Tracking für X-Plane unter Linux — 6DOF-Tracking mit NeuralNet-Webcam-Tracker, IR-Geräten oder SmoothTrack. Debian-Build-Anleitung und HeadTrack-Plugin-Einrichtung."
---
# OpenTrack

OpenTrack ist eine Head-Tracking-Anwendung für Linux, Windows und macOS, die Kopfbewegungen in X-Plane-Kamerabewegungen umsetzt. In Kombination mit dem HeadTrack-[Plugin](../../glossary.md#plugin) von amyinorbit ergibt sich der empfohlene Head-Tracking-Stack für [X-Plane](../../glossary.md#x-plane) 12 unter Linux.

## Hintergrund

- **Entwickler:** Stanisław Halik und Mitwirkende
- **Repository:** [github.com/opentrack/opentrack](https://github.com/opentrack/opentrack) (ISC-Lizenz)
- **Plattformen:** Windows, Linux (macOS derzeit nicht gepflegt)
- **Kompatibilität:** X-Plane 10, 11, 12

OpenTrack wird aktiv weiterentwickelt und ist der Nachfolger von FaceTrackNoIR. Es unterstützt eine breite Palette an Eingabe-Trackern und Ausgabeprotokollen. Unter Linux ermöglicht der NeuralNet Tracker KI-basiertes Head-Tracking über eine Standard-Webcam — ohne spezielle Hardware.

### HeadTrack-Plugin

- **Entwickler:** amyinorbit
- **Repository:** [github.com/amyinorbit/headtrack](https://github.com/amyinorbit/headtrack) (MIT-Lizenz)
- **Plattformen:** Windows, Linux, macOS

HeadTrack ist ein leichtgewichtiges X-Plane-Plugin, das 6DOF-Tracking-Daten über UDP-Port 4242 empfängt. Das letzte Release stammt vom Oktober 2022 und die Entwicklung ruht, die Linux-Binary funktioniert aber weiterhin mit X-Plane 12. Es dient als Brücke zwischen OpenTrack und X-Plane — die empfohlene Verbindungsmethode unter Linux, weil OpenTracks eigenes X-Plane-Plugin nicht als Binary ausgeliefert wird.

## Funktionsumfang

- **6DOF Head-Tracking:** Pitch, Yaw, Roll und X/Y/Z-Translation
- **NeuralNet Tracker:** KI-basierte Gesichtserkennung über Webcam — keine IR-Hardware nötig, läuft auf CPU (erfordert ONNX Runtime, siehe Installation)
- **PointTracker:** Klassisches Tracking mit 3 IR-LEDs oder Reflexpunkten und IR-Kamera
- **ArUco-Marker:** Gedruckter Papiermarker vor einer Webcam — kostenlose Alternative zu IR-Hardware
- **SmoothTrack-Eingabe:** Empfängt Tracking-Daten von der [SmoothTrack](https://smoothtrack.app/)-Smartphone-App (kostenpflichtig, iOS/Android) über WiFi/UDP
- **Filter und Kurven:** Accela-Filter, Response-Kurven, Totzonen und Glättung pro Achse
- **Hotkeys:** Start/Stop, Rezentrierung und Zero per Tastatur oder Joystick-Button

## Mehrwert in der Flugsimulation

Head-Tracking unter Windows basiert typischerweise auf TrackIR mit proprietären Treibern. Unter Linux bietet OpenTrack eine Open-Source-Alternative mit nativer Unterstützung für Webcam-basiertes KI-Tracking — der NeuralNet Tracker funktioniert ohne spezielle Hardware und ist damit die zugänglichste Head-Tracking-Lösung für Linux-Flugsimulanten. Das HeadTrack-Plugin stellt eine zuverlässige Datenübertragung an X-Plane 12 sicher, wo das eingebaute OpenTrack-Plugin Schwächen zeigt.

## Empfohlener Aufbau

Der empfohlene Datenfluss unter Linux:

```
Eingabe (eine Option wählen):
  ├─ NeuralNet Tracker (Webcam, keine Hardware)
  ├─ PointTracker (IR-LEDs + Kamera)
  └─ SmoothTrack (Smartphone-App)
        │
        ▼
OpenTrack (Linux, aus Quellcode gebaut oder Paket)
  ├─ Filter: Accela (Standard, empfohlen)
  ├─ Response-Kurven pro Achse
  └─ Ausgabe: "UDP over network" → 127.0.0.1:4242
        │
        ▼
HeadTrack-Plugin (amyinorbit) in X-Plane
  └─ In-Sim-GUI für Empfindlichkeit und Glättung
```

!!! warning "Das eingebaute OpenTrack-X-Plane-Plugin vermeiden"

    OpenTrack hat ein eigenes X-Plane-Ausgabeprotokoll mit einem zugehörigen Plugin (`opentrack.xpl`, POSIX Shared Memory). Es wird nicht als Binary ausgeliefert — es entsteht nur, wenn der Pfad zum X-Plane-SDK über `-DSDK_XPLANE=` mitgegeben wird, und funktioniert ausschließlich lokal. Stattdessen das HeadTrack-Plugin mit UDP-Ausgabe verwenden.

## Installation

### OpenTrack auf Debian/Ubuntu

```bash
sudo apt install build-essential cmake git libopencv-dev libproc2-dev qt6-base-private-dev qt6-tools-dev
git clone https://github.com/opentrack/opentrack.git
cd opentrack && cmake -B build && cmake --build build --parallel $(nproc)
```

!!! note "NeuralNet Tracker benötigt ONNX Runtime"

    Die obigen Build-Befehle erzeugen ein funktionierendes OpenTrack, aber ohne den NeuralNet Tracker, sofern ONNX Runtime nicht installiert ist. Unter Debian/Ubuntu `libonnxruntime-dev` installieren (falls verfügbar), oder das [ONNX Runtime Release](https://github.com/microsoft/onnxruntime/releases) herunterladen und `-DONNXRuntime_DIR=<Pfad>` zum CMake-Befehl hinzufügen.

### HeadTrack-Plugin

**Download:** [HeadTrack Releases](https://github.com/amyinorbit/headtrack/releases)

Die ZIP-Datei nach `Resources/plugins/` entpacken. Dadurch entsteht der Ordner `htrack/` mit dem Linux-Binary unter `lin_x64/htrack.xpl`.

Keine zusätzlichen Systempakete erforderlich.

## Konfiguration

### OpenTrack-Ausgabe

1. OpenTrack starten
2. Einen Tracker als Eingabe wählen (z.B. „NeuralNet tracker" für Webcam)
3. **Output** auf „UDP over network" setzen
4. In den Ausgabe-Einstellungen Ziel-IP auf `127.0.0.1` und Port auf `4242` setzen
5. Accela-Filter konfigurieren (Standardeinstellungen sind ein guter Ausgangspunkt)
6. Response-Kurven pro Achse anpassen — Empfindlichkeit für Yaw/Pitch reduzieren, um ruckartige Bewegungen zu vermeiden

### HeadTrack-Plugin in X-Plane

Nach Installation des Plugins und Start von X-Plane:

1. HeadTrack-Einstellungen über das Plugin-Menü öffnen
2. Empfindlichkeit und Glättung anpassen — mit niedrigen Werten beginnen und schrittweise erhöhen
3. Den Recenter-Hotkey in OpenTrack nutzen, um die neutrale Kopfposition vor jedem Flug zurückzusetzen

### NeuralNet Tracker

Der NeuralNet Tracker verwendet ein neuronales Netzwerkmodell (ONNX Runtime) zur Erkennung der Kopfposition über eine Standard-Webcam. ONNX Runtime muss vor dem Build separat installiert werden — unter Debian/Ubuntu `libonnxruntime-dev` installieren (falls verfügbar), oder das [ONNX Runtime Release](https://github.com/microsoft/onnxruntime/releases) herunterladen und `-DONNXRuntime_DIR=<Pfad>` beim CMake-Schritt angeben. Er läuft vollständig auf der CPU und benötigt keine GPU.

- Funktioniert mit den meisten USB- und eingebauten Webcams
- Ausreichende Beleuchtung ist wichtig — starkes Gegenlicht vermeiden
- Performance: Die CPU-Auslastung ist typischerweise gering genug, um neben X-Plane ohne Einfluss zu laufen

### SmoothTrack (Smartphone)

[SmoothTrack](https://smoothtrack.app/) ist eine kostenpflichtige Smartphone-App (iOS/Android), die Head-Tracking über die Frontkamera bereitstellt und die Daten per WiFi sendet.

- In OpenTrack: Eingabe auf „UDP over network" setzen, um SmoothTrack-Daten zu empfangen
- Alternativ: SmoothTrack direkt an HeadTrack auf Port 4242 senden, ohne OpenTrack dazwischen

## Quellen

- [OpenTrack — GitHub](https://github.com/opentrack/opentrack)
- [HeadTrack — GitHub](https://github.com/amyinorbit/headtrack)
- [SmoothTrack — Website](https://smoothtrack.app/)
- [LinuxTrack](linuxtrack.md) — Alternative Head-Tracking-Lösung für Linux
- [XCamera](xcamera.md) — Kamera-Plugin mit OpenTrack-Integration
