# WINCTRL

WINCTRL ist ein natives [Plugin](../glossary.md#plugin), das Winwing-Cockpitpanels (MCDU, FCU, EFIS, Pedale) direkt per USB-HID mit X-Plane verbindet — ohne die Windows-only Software SimAppPro. Für Linux- und macOS-Nutzer ist es die einzige Möglichkeit, Winwing-Hardware vollständig zu nutzen.

## Hintergrund

- **Entwickler:** Ramon (rswilem), Community-Beiträge
- **Repository:** [github.com/rswilem/winctrl-xplane-plugin](https://github.com/rswilem/winctrl-xplane-plugin) (GPL-3.0)
- **Download:** [X-Plane.org](https://forums.x-plane.org/files/file/95987-winctrl-plugin-for-x-plane-mac-linux-windows/)
- **Plattformen:** Linux, macOS, Windows
- **Kompatibilität:** X-Plane 12
- **Preis:** Kostenlos (Open Source)

Das Plugin kommuniziert direkt über USB-HID mit der Hardware: es liest Tasten, Drehregler und Schalter aus und steuert im Gegenzug LCD-Displays, LED-Beleuchtung und Annunciatoren. Achsen (Schubhebel, Joystick) werden bewusst X-Planes interner Joystick-Konfiguration überlassen. Die Entwicklung ist sehr aktiv (32 Releases seit Juli 2025).

## Funktionsumfang

- **Automatische Geräteerkennung:** Keine manuelle Konfiguration nötig
- **LCD/Display-Ansteuerung:** MCDU-Bildschirme, PDC-Displays, FCU-Zahlendisplays
- **LED/Annunciator-Steuerung:** Tastenbeleuchtung, Hintergrundbeleuchtung, Warnlichter synchron mit dem Flugzeugzustand
- **Multi-Aircraft-Profile:** Unterschiedliche Dataref-Mappings pro Flugzeugtyp
- **Selbsttest-Emulation:** MCDU/FMC-Selbsttest bei ToLiss-Flugzeugen
- **SkunkCrafts Updater:** Automatische Updates nach der Erstinstallation

**Unterstützte Hardware:** MCDU-32, PFP 3N/4/7, FCU, EFIS, ECAM32, PAP3, AGP, URSA MINOR Joystick/Throttle, 3N/3M PDC

**Unterstützte Flugzeuge:** ToLiss A3XX-Familie, Laminar A330/737, Zibo/LevelUp 737, FlightFactor 767/777/A350, iniSimulations A300/A310, JustFlight BAe 146 u.a.

## Mehrwert in der Flugsimulation

Winwing-Hardware bietet unter Linux ohne WINCTRL nur eingeschränkte Joystick-Funktionalität — die eigentlichen Cockpitpanel-Features (Displays, LEDs, Taster-Feedback) bleiben ungenutzt, da SimAppPro nicht für Linux verfügbar ist. WINCTRL erschließt den vollen Funktionsumfang der Hardware auf allen Plattformen.

## Installation

**Download:** [GitHub Releases](https://github.com/rswilem/winctrl-xplane-plugin/releases)

Den Ordner `winctrl` nach `Resources/plugins/` kopieren. Das Plugin erkennt angeschlossene Hardware automatisch.

### Linux-Hinweise: udev-Regeln

Für den HID-Zugriff ohne Root-Rechte sind udev-Regeln erforderlich. Datei `/etc/udev/rules.d/99-winctrl.rules` anlegen:

```bash
# Winwing/WINCTRL HID-Geräte
SUBSYSTEM=="hidraw", ATTRS{idVendor}=="1002", MODE="0666"
```

Danach udev-Regeln neu laden:

```bash
sudo udevadm control --reload-rules && sudo udevadm trigger
```

Die vollständige Regel-Datei mit gerätespezifischen Symlinks ist im [Repository-README](https://github.com/rswilem/winctrl-xplane-plugin#linux) dokumentiert.

## Quellen

- [WINCTRL — GitHub](https://github.com/rswilem/winctrl-xplane-plugin)
- [WINCTRL — X-Plane.org](https://forums.x-plane.org/files/file/95987-winctrl-plugin-for-x-plane-mac-linux-windows/)
