# LinuxTrack

LinuxTrack ist eine Head-Tracking-Software für Linux und macOS, die über das [Plugin](../../glossary.md#plugin) xlinuxtrack Kopfbewegungen in X-Planes Kamerabewegungen umsetzt. Es unterstützt TrackIR, Webcams und Wiimotes als Eingabegeräte und bietet 6DOF-Tracking (6 Freiheitsgrade).

## Hintergrund

- **Entwickler:** uglyDwarf (Michal), aktiver Fork: fwfa123 (LinuxTrack X-IR)
- **Repository:** [github.com/uglyDwarf/linuxtrack](https://github.com/uglyDwarf/linuxtrack) (MIT-Lizenz)
- **Aktiver Fork:** [github.com/fwfa123/linuxtrackx-ir](https://github.com/fwfa123/linuxtrackx-ir)
- **Plattformen:** Linux, macOS
- **Kompatibilität:** X-Plane 12

Das Originalprojekt wird seit 2016 nicht mehr regulär released und hat eine veraltete Qt4-Abhängigkeit. Der aktive Fork **LinuxTrack X-IR** (v0.99.29, Januar 2026) löst diese Probleme: Qt5/Qt6-Unterstützung, AppImage-Distribution und modernisiertes X-Plane-Plugin.

## Funktionsumfang

- **6DOF Head-Tracking:** Pitch, Yaw, Roll und X/Y/Z-Translation
- **Unterstützte Hardware:** TrackIR 2–5, SmartNav 3/4, UVC-Webcams, PS3 Eye, Wiimote, generische HID-Joysticks
- **Konfigurierbare Empfindlichkeit:** Sensitivity-Kurven, Totzone und Filter pro Achse
- **Joystick-Buttons:** Start/Stop, Rezentrierung und Freeze per Knopfdruck
- **Wine-Bridge:** Ermöglicht Windows-Spielen unter Proton/Wine die Nutzung von LinuxTrack

## Mehrwert in der Flugsimulation

Head-Tracking verändert das Flugerlebnis grundlegend — natürliche Blickbewegungen im Cockpit statt Maussteuerung. LinuxTrack ist die native Linux-Lösung dafür, die direkt mit den gängigen Tracking-Geräten kommuniziert. Besonders für TrackIR-Besitzer unter Linux gibt es kaum Alternativen.

## Installation

**Empfohlen:** Den X-IR Fork als AppImage verwenden.

**Download:** [LinuxTrack X-IR Releases](https://github.com/fwfa123/linuxtrackx-ir/releases)

1. LinuxTrack installieren (AppImage oder aus Quellcode bauen)
2. LinuxTrack-GUI starten (`ltr_gui`), Tracking-Gerät konfigurieren
3. Im Tab „Misc." auf „Install XPlane plugin..." klicken und das X-Plane-Verzeichnis auswählen
4. GUI schließen — nur der Hintergrund-Daemon (`ltr_server1`) darf während des Fluges laufen

### Debian-Abhängigkeiten (Build aus Quellcode)

```bash
sudo apt install build-essential git automake libmxml-dev libopencv-dev libtool libusb-1.0-0-dev zlib1g-dev libv4l-dev bison flex
```

Für Qt5-Unterstützung zusätzlich `qtbase5-dev`.

### Hinweise

- TrackIR 4/5 erfordert eine Firmware-Extraktion beim ersten Start
- Die GUI (`ltr_gui`) darf beim Fliegen **nicht** laufen — nur der Daemon `ltr_server1`
- Alternative: [OpenTrack](https://github.com/opentrack/opentrack) bietet ähnliche Funktionalität mit breiterer Plattformunterstützung
- [XCamera](xcamera.md) unterstützt LinuxTrack als Eingabe für Head-Tracking

## Quellen

- [LinuxTrack — GitHub](https://github.com/uglyDwarf/linuxtrack)
- [LinuxTrack X-IR — GitHub](https://github.com/fwfa123/linuxtrackx-ir)
- [LinuxTrack — Wiki](https://github.com/uglyDwarf/linuxtrack/wiki)
