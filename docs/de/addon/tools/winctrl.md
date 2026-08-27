---
description: "Das X-Plane WINCTRL Plugin steuert WINCTRL-Cockpitpanels unter Linux und macOS per USB HID — LCD-, LED- und Tastensteuerung ohne SimAppPro."
---
# X-Plane WINCTRL Plugin

Das X-Plane WINCTRL Plugin ist ein natives [Plugin](../../glossary.md#plugin), das WINCTRL-Cockpitpanels (MCDU, FCU, EFIS) direkt per USB-HID mit X-Plane verbindet — ohne die Windows-only Software SimAppPro. Für Linux- und macOS-Nutzer ist es die einzige Möglichkeit, WINCTRL-Hardware vollständig zu nutzen.

## Hintergrund

- **Entwickler:** Ramon (rswilem), Community-Beiträge
- **Repository:** [github.com/rswilem/winctrl-xplane-plugin](https://github.com/rswilem/winctrl-xplane-plugin) (GPL-3.0)
- **Download:** [X-Plane.org](https://forums.x-plane.org/files/file/95987-winctrl-plugin-for-x-plane-mac-linux-windows/)
- **Plattformen:** Linux, macOS, Windows
- **Kompatibilität:** X-Plane 11 und 12

!!! note "Hardware und Plugin heißen gleich"

    WINCTRL ist sowohl der Hardware-Hersteller als auch der Name dieses Plugins. Auf dieser Seite meint **WINCTRL** allein die Hardware; die Software heißt **X-Plane WINCTRL Plugin** oder kurz das Plugin.

Das Plugin kommuniziert direkt über USB-HID mit der Hardware: es liest Tasten, Drehregler und Schalter aus und steuert im Gegenzug LCD-Displays, LED-Beleuchtung und Annunciatoren. Achsen (Schubhebel, Joystick) werden bewusst X-Planes interner Joystick-Konfiguration überlassen — Kalibrierung, Totzonen und Kennlinien sind dort besser aufgehoben. Für Tasten gilt derselbe Vorrang: Was unter **Einstellungen → Joystick** zugewiesen ist, gewinnt, und das Plugin hält sein eigenes Kommando für diese Taste zurück. Die Entwicklung ist sehr aktiv mit regelmäßigen Releases.

## Funktionsumfang

- **Automatische Geräteerkennung:** Keine manuelle Konfiguration nötig
- **LCD/Display-Ansteuerung:** MCDU-Bildschirme, PDC-Displays, FCU-Zahlendisplays
- **LED/Annunciator-Steuerung:** Tastenbeleuchtung, Hintergrundbeleuchtung, Warnlichter synchron mit dem Flugzeugzustand
- **Multi-Aircraft-Profile:** Unterschiedliche Dataref-Mappings pro Flugzeugtyp
- **Selbsttest-Emulation:** MCDU/FMC-Selbsttest bei ToLiss-Flugzeugen
- **Eigene FMC-Schriften:** Display-Schriften als `.xpwwf`-Dateien
- **SkunkCrafts Updater:** Automatische Updates nach der Erstinstallation

**Unterstützte Hardware:** MCDU-32, PFP 3N/4/7, FCU (optional mit EFIS L/R), 32 ECAM, 32 AGP, 32 TCAS, 32 RMP, 32 NWS, 3N PAP MCP, 3N/3M PDC, URSA MINOR Airline- und Fighter-Joysticks, URSA MINOR 32 Throttle (optional mit 32 PAC), ORION Joystick Base II und Throttle Base II

**Unterstützte Flugzeuge:** ToLiss A3XX-Familie, Laminar A330/737, Zibo/LevelUp 737, FlightFactor 767/777/A350, JustFlight BAe 146 u.a.

### Eigene FMC-Schriften

Die Schrift des FMC-Displays lässt sich austauschen. Schriften werden im Font-Editor des Projekts erstellt, als `.xpwwf`-Datei heruntergeladen und abgelegt unter:

```
X-Plane 12/Resources/plugins/winctrl/fonts/
```

Ausgewählt wird im Simulator unter **Plugins → WINCTRL → FMC → Display font**. Seit dem Release vom August 2026 liegen auch die mitgelieferten Schriften in diesem Verzeichnis statt in der Binary, was die Ladezeiten verkürzt.

## Mehrwert in der Flugsimulation

WINCTRL-Hardware bietet unter Linux ohne das Plugin nur eingeschränkte Joystick-Funktionalität — die eigentlichen Cockpitpanel-Features (Displays, LEDs, Taster-Feedback) bleiben ungenutzt, da SimAppPro nicht für Linux verfügbar ist. Das Plugin ersetzt den im Flug entscheidenden Teil von SimAppPro: die Laufzeit-Anbindung, über die der Simulator Displays und Leuchten ansteuert. Firmware-Updates, Kalibrierung und der Hardware-Selbsttest brauchen weiterhin SimAppPro auf einer Windows-Maschine.

## Installation

**Download:** [GitHub Releases](https://github.com/rswilem/winctrl-xplane-plugin/releases)

Den Ordner `winctrl` nach `Resources/plugins/` kopieren. Das Plugin erkennt angeschlossene Hardware automatisch.

### Linux-Hinweise: udev-Regeln

Raw-HID-Knoten tragen keine ACL, deshalb bringt erst eine udev-Regel die Panels in Reichweite des Plugins — [Controller](../../xplane/setup_diagnose/config.md#controller) erklärt, warum Standard-Joysticks ohne solche Regel auskommen und diese Panels nicht.

Debian empfiehlt den udev-Tag `uaccess`: Er vergibt eine ACL an den am Seat angemeldeten Benutzer, statt das Gerät für alle zu öffnen. Datei `/etc/udev/rules.d/70-winctrl.rules` anlegen:

```
# WINCTRL-HID-Geräte (USB-Vendor-ID 0x4098)
SUBSYSTEM=="hidraw", ATTRS{idVendor}=="4098", TAG+="uaccess"
```

udev vergleicht `idVendor` mit dem sysfs-Wert, den der Kernel als Hexadezimal-String schreibt — `4098` in der Regel meint also die USB-Vendor-ID **0x4098**, denselben Wert, den das Plugin als `WINCTRL_VENDOR_ID` fest hinterlegt. Eine Umrechnung ins Dezimalsystem wäre falsch.

!!! warning "Der Dateiname entscheidet, ob `uaccess` wirkt"

    Ausgewertet wird der Tag ausschließlich von `73-seat-late.rules`. Eine Regeldatei namens `99-winctrl.rules` sortiert *danach*, der Tag bleibt dann wirkungslos — die Datei muss vor 73 einsortieren, daher `70-winctrl.rules`.

Das README verwendet stattdessen `MODE="0666"`, was das Gerät jedem lokalen Benutzer öffnet, mit gerätespezifischen Regeln in dieser Form:

```
KERNEL=="hidraw*", ATTRS{idProduct}=="...", ATTRS{idVendor}=="4098", MODE="0666", SYMLINK+="..."
```

Diese Form funktioniert unabhängig vom Dateinamen und ist die richtige Wahl, wenn die Symlinks gebraucht werden. `GROUP="plugdev", MODE="0660"` ist der ältere Mittelweg und beschränkt den Zugriff auf Mitglieder dieser Gruppe.

Das Neuladen der Regeln erfasst bereits angeschlossene Geräte nicht — entweder das Panel neu einstecken oder die Ereignisse für das aktuell Angeschlossene neu auslösen:

```bash
sudo udevadm control --reload-rules && sudo udevadm trigger
```

Der vollständige Regelsatz mit gerätespezifischen Produkt-IDs und Symlinks ist im [Repository-README](https://github.com/rswilem/winctrl-xplane-plugin#linux-udev-rules) dokumentiert — er ist als verbindliche Quelle zu verwenden.

## Quellen

- [WINCTRL — GitHub](https://github.com/rswilem/winctrl-xplane-plugin)
- [WINCTRL — X-Plane.org](https://forums.x-plane.org/files/file/95987-winctrl-plugin-for-x-plane-mac-linux-windows/)
