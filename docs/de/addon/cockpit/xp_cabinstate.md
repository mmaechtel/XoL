---
description: "XP CabinState für X-Plane 12 — Kabinen-, Crew- und Passagiersimulation mit SimLoad-Manager-Anbindung; unter Linux per Wine im Headless-Modus getestet."
---
# XP CabinState

XP CabinState simuliert Kabine, Crew und Passagiere neben [X-Plane](../../glossary.md#x-plane) 12: Boarding, Sicherheitsvorführung, Trolley-Service und Durchsagen passend zu Flugphase, Höhe und Kabinenzeichen. Es ist ein eigenständiges Windows-Programm, das X-Plane über die eingebaute Web API ausliest und über eine Browser-WebUI bedient wird. Linux wird offiziell nicht unterstützt, das Programm läuft aber headless unter [Wine](../../glossary.md#wine-wine-is-not-an-emulator).

## Hintergrund

- **Entwickler:** Vito Jackson (Isar Simworks, München)
- **Website:** [isarsimworks.de](https://isarsimworks.de/shop.php?p=xp-cabinstate)
- **Lizenz:** Free-Edition kostenlos, Pro-Edition kostenpflichtig (Lizenzschlüssel, offline geprüft)
- **Plattformen:** Offiziell nur Windows 10/11 — macOS und Linux werden nicht unterstützt
- **Kompatibilität:** X-Plane 12.1.1 oder neuer (eingebaute Web API, standardmäßig aktiv)
- **Flugzeuge:** 12 Kabinen — ToLiss A319 bis A340-600, Zibo/LevelUp 737-600 bis 900ER, DeltaWing ATR 72-600
- **Begleit-Plugin:** XP CabinState Link (Figuren, Kabinenzeichen und Kabinensound in X-Plane) — nur Windows-Build

## Funktionsumfang

- **Kompletter Flugablauf:** Boarding, Sicherheitsvorführung, Trolley-Service, Landung, Aussteigen und Reinigung; die Crew reagiert auf Rufknöpfe
- **Durchsagen:** Crew-Durchsagen auf Deutsch und Englisch, Gate-Durchsagen mit Terminal-Sound, Boarding-Musik und Gong
- **Bordbildschirm:** Sicherheitsvideo und Kabinenkarte mit Route und Position
- **3D-Kabine:** Kabinenansicht mit Crew und Sitzbelegung in der WebUI
- **Flug anlegen:** Aus SimBrief oder gesteuert von SimLoad Manager
- **Tablet und Zweitrechner:** Die WebUI läuft in jedem Browser im selben Netzwerk

**Free vs. Pro**

| Funktion | Free | Pro |
|---|---|---|
| Flugablauf in allen 12 Kabinen, Durchsagen, Bordbildschirm | Ja | Ja |
| Tablets und Zweitgeräte gleichzeitig | 1 | Unbegrenzt |
| Logbuch | Letzte 5 Flüge | Vollständig, mit Flugbericht |
| Airline-Modus (Flotte, Bank, Personal, Verträge, Abrechnung) | — | Ja |
| Eigene Medien und Sitzpläne | — | Ja |

## Mehrwert in der Flugsimulation

In den meisten Simulator-Setups bleibt die Kabine hinter der Cockpittür leer und stumm. XP CabinState füllt diese Lücke mit einer Crew, die auf das Geschehen im Cockpit reagiert — die Begrüßung des Kapitäns folgt dem Pushback, der Service wird bei stärkeren Turbulenzen unterbrochen, und Durchsagen folgen der Flugphase. Zusammen mit einem Lade-Tool bilden Turnaround am Gate und Leben in der Kabine einen durchgehenden Ablauf.

## SimLoad-Manager-Anbindung

Unter **Einstellungen → Flugablauf** lässt sich [SimLoad Manager](../traffic/simloadmanager.md) als Ladequelle wählen. SimLoad Manager steuert dann Boarding, Crew, Catering und Aussteigen; die passenden CabinState-Optionen werden ausgeblendet. Die Passagierzahl wird beim Anlegen des Flugs aus SimLoad Manager übernommen und bis zum Beginn des Boardings aktualisiert. Die Option ist nur wählbar, während SimLoad Manager in X-Plane läuft.

## Linux-Setup (Wine)

!!! warning "Workaround, kein offizieller Support"

    Der Entwickler unterstützt nur Windows. Das folgende Setup wurde zum Zeitpunkt des Tests mit dem ToLiss A320 erprobt: Flugablauf, Durchsagen und die 3D-Kabinenansicht der WebUI funktionieren. Programmversionen und Startoptionen können sich ändern.

Den kompletten Ordner `XP CabinState` entpacken und `XPCabinState.exe`, `xpcabinstate.dat` sowie die mitgelieferten Laufzeitdateien zusammenlassen; nur den ganzen Ordner verschieben, nie einzelne Dateien. Die folgenden Befehle aus diesem Ordner heraus starten. Ein eigener Wine-Prefix genügt; Mono und Gecko werden nicht benötigt und lassen sich beim Anlegen überspringen:

```bash
WINEPREFIX="$HOME/.wine-xpcabinstate" WINEDLLOVERRIDES="mscoree,mshtml=" wineboot -i
WINEPREFIX="$HOME/.wine-xpcabinstate" wine XPCabinState.exe --headless --run-seconds=86400
```

- **`--headless`** ist nötig — das Programmfenster braucht WebView2/.NET, das unter Wine nicht verfügbar ist
- **`--run-seconds`** ist nötig — ohne die Option stürzt das Programm mit `OverflowError: timestamp out of range` ab; der Wert ist die Laufzeit in Sekunden und darf großzügig gewählt werden (86400 entspricht 24 Stunden)
- **WebUI:** Standardmäßig Port 8130 auf allen Interfaces; ist er belegt, nimmt das Programm den nächsten freien Port (die Adresse steht im Protokoll `Documents/XP-CabinState/XP CabinState.log` im Wine-Prefix). Einmal `http://127.0.0.1:8130/?k=<schlüssel>` mit dem Zugangsschlüssel aus `Documents/XP-CabinState/Spielstand/ui_key.txt` aufrufen, den Port bei Bedarf anpassen — der Browser merkt sich den Zugang per Cookie
- **Ton:** Kommt aus dem Browser (Schalter in der WebUI); nur in einem Browser einschalten, sonst laufen Durchsagen doppelt
- **Bordbildschirm:** Unter `/?ife=1` erreichbar, etwa im [AviTab](avitab.md)-Browser

Da XP CabinState Link keinen Linux-Build hat, fehlen die Figuren in der X-Plane-Kabine, der Ton im Sim, das X-Plane-Menü und die Kabinenkamera. Alles andere läuft in der WebUI.

## Quellen

- [XP CabinState — Isar Simworks Shop](https://isarsimworks.de/shop.php?p=xp-cabinstate)
- [Isar Simworks — Installation](https://isarsimworks.de/installation.php)
