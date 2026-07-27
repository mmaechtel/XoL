---
description: "LinuxTrack Head-Tracking für X-Plane unter Linux — 6DOF-Tracking mit TrackIR, Webcam oder Wiimote. Installation und X-IR-Fork-Anleitung."
---
# LinuxTrack

LinuxTrack ist eine Head-Tracking-Software für Linux und macOS, die über das [Plugin](../../glossary.md#plugin) xlinuxtrack Kopfbewegungen in X-Planes Kamerabewegungen umsetzt. Es unterstützt TrackIR, Webcams und Wiimotes als Eingabegeräte und bietet 6DOF-Tracking (6 Freiheitsgrade).

## Hintergrund

- **Entwickler:** uglyDwarf (Michal), aktiver Fork: fwfa123 (LinuxTrack X-IR)
- **Repository:** [github.com/uglyDwarf/linuxtrack](https://github.com/uglyDwarf/linuxtrack) (MIT-Lizenz)
- **Aktiver Fork:** [gitlab.com/fwfa123/linuxtrackx-ir](https://gitlab.com/fwfa123/linuxtrackx-ir) (kanonisches Zuhause; das [GitHub-Repo](https://github.com/fwfa123/linuxtrackx-ir) ist ein Spiegel)
- **Plattformen:** Linux, macOS
- **Kompatibilität:** X-Plane 12

Das Originalprojekt wird seit 2016 nicht mehr regulär released und hat eine veraltete Qt4-Abhängigkeit. Der aktive Fork **LinuxTrack X-IR** löst diese Probleme: eine Qt6/CMake-zentrierte Neuarchitektur, AppImage-Distribution, eine MinGW-basierte Wine-Bridge und ein modernisiertes X-Plane-Plugin.

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

**Download:** [LinuxTrack X-IR Releases](https://gitlab.com/fwfa123/linuxtrackx-ir/-/releases) (AppImages werden auf GitLab veröffentlicht)

1. LinuxTrack installieren (AppImage oder aus Quellcode bauen)
2. LinuxTrack-GUI starten (`ltr_gui`), Tracking-Gerät konfigurieren
3. Im Tab „Gaming" auf „Install Xplane plugin..." klicken, dann zur X-Plane-Programmdatei navigieren und mit „Open" bestätigen
4. GUI schließen — empfohlen ist, während des Fluges nur den Hintergrund-Daemon (`ltr_server1`) laufen zu lassen

### Debian-Abhängigkeiten (Build aus Quellcode)

```bash
sudo apt install build-essential git cmake pkg-config libusb-1.0-0-dev zlib1g-dev bison flex qt6-base-dev qt6-tools-dev qt6-tools-dev-tools libqt6opengl6-dev libmxml-dev libx11-dev libxrandr-dev libgl1-mesa-dev libglu1-mesa-dev
```

Für Webcam-, Face-Tracking- und Wiimote-Unterstützung zusätzlich `libv4l-dev`, `libopencv-dev` und `libcwiid-dev`.

### Hinweise

- TrackIR 4/5 erfordert eine Firmware-Extraktion beim ersten Start
- Die GUI (`ltr_gui`) kann beim Fliegen laufen, empfohlen ist es nicht — das Tracking funktioniert allein mit dem Daemon `ltr_server1`
- Alternative: [OpenTrack](opentrack.md) bietet ähnliche Funktionalität mit Webcam-basiertem KI-Tracking und breiterer Plattformunterstützung
- [XCamera](xcamera.md) unterstützt LinuxTrack als Eingabe für Head-Tracking

## Quellen

- [LinuxTrack — GitHub](https://github.com/uglyDwarf/linuxtrack)
- [LinuxTrack X-IR — GitLab](https://gitlab.com/fwfa123/linuxtrackx-ir)
- [LinuxTrack — Wiki](https://github.com/uglyDwarf/linuxtrack/wiki)
