---
description: "WINCTRL verbindet Winwing-Cockpitpanels unter Linux und macOS per USB HID mit X-Plane — vollwertige LCD-, LED- und Tastensteuerung ohne SimAppPro."
---
# WINCTRL

WINCTRL ist ein natives [Plugin](../../glossary.md#plugin), das Winwing-Cockpitpanels (MCDU, FCU, EFIS) direkt per USB-HID mit X-Plane verbindet — ohne die Windows-only Software SimAppPro. Für Linux- und macOS-Nutzer ist es die einzige Möglichkeit, Winwing-Hardware vollständig zu nutzen.

## Hintergrund

- **Entwickler:** Ramon (rswilem), Community-Beiträge
- **Repository:** [github.com/rswilem/winctrl-xplane-plugin](https://github.com/rswilem/winctrl-xplane-plugin) (GPL-3.0)
- **Download:** [X-Plane.org](https://forums.x-plane.org/files/file/95987-winctrl-plugin-for-x-plane-mac-linux-windows/)
- **Plattformen:** Linux, macOS, Windows
- **Kompatibilität:** X-Plane 11 und 12

Das Plugin kommuniziert direkt über USB-HID mit der Hardware: es liest Tasten, Drehregler und Schalter aus und steuert im Gegenzug LCD-Displays, LED-Beleuchtung und Annunciatoren. Achsen (Schubhebel, Joystick) werden bewusst X-Planes interner Joystick-Konfiguration überlassen. Die Entwicklung ist sehr aktiv mit regelmäßigen Releases.

## Funktionsumfang

- **Automatische Geräteerkennung:** Keine manuelle Konfiguration nötig
- **LCD/Display-Ansteuerung:** MCDU-Bildschirme, PDC-Displays, FCU-Zahlendisplays
- **LED/Annunciator-Steuerung:** Tastenbeleuchtung, Hintergrundbeleuchtung, Warnlichter synchron mit dem Flugzeugzustand
- **Multi-Aircraft-Profile:** Unterschiedliche Dataref-Mappings pro Flugzeugtyp
- **Selbsttest-Emulation:** MCDU/FMC-Selbsttest bei ToLiss-Flugzeugen
- **SkunkCrafts Updater:** Automatische Updates nach der Erstinstallation

**Unterstützte Hardware:** MCDU-32, PFP 3N/4/7, FCU, EFIS, ECAM32, PAP3, AGP, URSA MINOR Joystick/Throttle, 3N/3M PDC

**Unterstützte Flugzeuge:** ToLiss A3XX-Familie, Laminar A330/737, Zibo/LevelUp 737, FlightFactor 767/777/A350, JustFlight BAe 146 u.a.

## Mehrwert in der Flugsimulation

Winwing-Hardware bietet unter Linux ohne WINCTRL nur eingeschränkte Joystick-Funktionalität — die eigentlichen Cockpitpanel-Features (Displays, LEDs, Taster-Feedback) bleiben ungenutzt, da SimAppPro nicht für Linux verfügbar ist. WINCTRL erschließt den vollen Funktionsumfang der Hardware auf allen Plattformen.

## Installation

**Download:** [GitHub Releases](https://github.com/rswilem/winctrl-xplane-plugin/releases)

Den Ordner `winctrl` nach `Resources/plugins/` kopieren. Das Plugin erkennt angeschlossene Hardware automatisch.

### Linux-Hinweise: udev-Regeln

Für den HID-Zugriff ohne Root-Rechte sind udev-Regeln erforderlich. Datei `/etc/udev/rules.d/99-winctrl.rules` anlegen:

```
# Winwing/WINCTRL HID-Geräte (Vendor-ID 4098)
SUBSYSTEM=="hidraw", ATTRS{idVendor}=="4098", MODE="0666"
```

Die USB-HID-Vendor-ID von Winwing lautet `4098` — nicht `1002` (das ist die AMD/ATI-PCI-Vendor-ID und passt auf kein Winwing-Gerät). Gerätespezifische Regeln folgen der README-Form:

```
KERNEL=="hidraw*", ATTRS{idProduct}=="...", ATTRS{idVendor}=="4098", MODE="0666", SYMLINK+="..."
```

Danach udev-Regeln neu laden:

```bash
sudo udevadm control --reload-rules && sudo udevadm trigger
```

Der vollständige Regelsatz mit gerätespezifischen Produkt-IDs und Symlinks ist im [Repository-README](https://github.com/rswilem/winctrl-xplane-plugin#linux-udev-rules) dokumentiert — er ist als verbindliche Quelle zu verwenden.

## Quellen

- [WINCTRL — GitHub](https://github.com/rswilem/winctrl-xplane-plugin)
- [WINCTRL — X-Plane.org](https://forums.x-plane.org/files/file/95987-winctrl-plugin-for-x-plane-mac-linux-windows/)
