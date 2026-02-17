---
description: "MobiFlight-Middleware für Home-Cockpits mit X-Plane unter Linux: Netzwerk-Split oder KVM/QEMU-VM mit USB-Passthrough für Arduino-Hardware."
---
# MobiFlight

MobiFlight ist eine Open-Source-Middleware für den Bau von Home-Cockpits. Die Software verbindet Mikrocontroller (Arduino, Raspberry Pi Pico) mit [X-Plane](../../glossary.md#x-plane) und übersetzt Simulator-Variablen in physische Ausgaben (LEDs, 7-Segment-Anzeigen, Stepper-Motoren) und umgekehrt physische Eingaben (Schalter, Encoder, Potentiometer) in Simulator-Befehle. Der MobiFlight Connector ist **ausschließlich für Windows** verfügbar — unter Linux ist ein Netzwerk-Split (Connector auf einem Windows-Rechner oder einer KVM/QEMU-VM) erforderlich.

## Hintergrund

- **Entwickler:** Sebastian Möbius (Community-Projekt, MIT-Lizenz)
- **Website:** [mobiflight.com](https://www.mobiflight.com)
- **GitHub:** [MobiFlight/MobiFlight-Connector](https://github.com/MobiFlight/MobiFlight-Connector)
- **Plattformen:** Nur Windows 10+ (.NET Framework 4.8, Windows Forms)
- **Kompatibilität:** X-Plane 11/12, MSFS 2020/2024, Prepar3D

## Funktionsumfang

- **DataRef-Zugriff:** Lesen und Schreiben beliebiger X-Plane DataRefs über UDP (Port 49000)
- **Commands:** Auslösen von X-Plane Commands (z.B. `sim/autopilot/heading_up`)
- **Aircraft-Erkennung:** Automatischer Wechsel der Konfiguration je nach geladenem Flugzeug
- **HubHop-Presets:** Über 7.000 Community-Presets für verschiedene Aircraft (Zibo 737, ToLiss A320 u.a.)
- **Hardware-Support:** Arduino Mega/Nano/Pro Micro, Raspberry Pi Pico, MIDI-Controller, HID-Geräte, kommerzielle Panels (Winwing, VKB, Octavi)
- **Kein X-Plane-Plugin nötig:** Die Kommunikation nutzt X-Planes eingebaute UDP-Schnittstelle — kein zusätzliches Plugin erforderlich

## KVM-Setup

Da der MobiFlight Connector nicht unter Linux läuft (Wine/Proton ist aufgrund tiefer Windows-API-Abhängigkeiten nicht praktikabel), gibt es zwei Wege:

### Netzwerk-Split (empfohlen)

MobiFlight kommuniziert mit X-Plane über UDP — das Protokoll ist netzwerkbasiert und plattformunabhängig. Damit lässt sich ein Split-Setup betreiben:

- **Linux-PC:** X-Plane 12 (nativ)
- **Windows-PC oder -VM:** MobiFlight Connector + angeschlossene Hardware

In MobiFlight die IP-Adresse des Linux-PCs eintragen (statt `127.0.0.1`). X-Plane akzeptiert UDP-Verbindungen standardmäßig auf Port 49000.

### Windows-VM mit USB-Passthrough

Steht kein zweiter Rechner zur Verfügung, kann eine Windows-VM (KVM/QEMU) auf dem Linux-Host den Connector ausführen. Die Arduino-Hardware wird per USB-Passthrough an die VM durchgereicht (siehe [Docker & Virtualisierung](../../linux/extensions/docker.md) für KVM-Grundlagen).

**Voraussetzungen**

- Windows 10+ Guest in KVM/QEMU
- USB-Passthrough für Arduino/Pico-Boards konfiguriert
- Bridged oder NAT-Netzwerk mit Host-Zugriff (für UDP Port 49000)

Für das UDP-Forwarding zwischen VM und nativem X-Plane auf dem Host eignet sich [SayIntentionsForMac](https://github.com/paulfisher53/SayIntentionsForMac) — das Projekt stellt `sudppipe.exe` und eine Dummy-`X-Plane.exe` bereit, die die UDP-Verbindung direkt an den Host weiterleiten. Damit entfällt die Installation eines zusätzlichen Plugins in X-Plane. Dieses Setup wurde erfolgreich getestet.

## Quellen

- [MobiFlight — Offizielle Website](https://www.mobiflight.com)
- [MobiFlight — GitHub Repository](https://github.com/MobiFlight/MobiFlight-Connector)
- [MobiFlight — Dokumentation](https://docs.mobiflight.com)
- [MobiFlight — X-Plane Quick Start Guide](https://www.mobiflight.com/en/tutorials/x-plane-quick-start-guide.html)
- [HubHop — Community-Preset-Datenbank](https://hubhop.mobiflight.com)
