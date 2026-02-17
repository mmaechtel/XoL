---
description: "TOI Cabin Ready: FlyWithLua-Skript zur Automatisierung des Cabin-Ready-ECAM-Aufrufs für ToLiss-Airbus-Flugzeuge in X-Plane 12 bei Abflug und Anflug."
---
# TOI Cabin Ready

TOI Cabin Ready ist ein [FlyWithLua](../scripting/flywithlua.md)-Skript, das automatisch die „Cabin Ready"-ECAM-Meldung für ToLiss-Airbus-Flugzeuge auslöst und das manuelle Drücken der FWD-CALL-Taste überflüssig macht.

## Hintergrund

- **Entwickler:** cxn0026
- **Download:** [X-Plane.org](https://forums.x-plane.org/files/file/91876-toliss-airbus-cabin-ready-automatic-flywithlua-script/)
- **Plattformen:** Windows, macOS, Linux (reines Lua)
- **Kompatibilität:** X-Plane 12
- **Abhängigkeit:** [FlyWithLua NG+](../scripting/flywithlua.md)

Das Skript automatisiert zwei Cabin-Ready-Auslöser:

- **Abflug:** Startet einen Countdown (4–8 Minuten, skaliert nach Passagieranzahl), wenn das Beacon-Licht eingeschaltet wird
- **Anflug:** Sendet Cabin Ready wenige Sekunden nachdem Klappen und Fahrwerk in der unteren Position sind

Sonderfälle wie Durchstarten und Durchgangsflüge werden berücksichtigt — im schlechtesten Fall muss die FWD-CALL-Taste manuell gedrückt oder ein unnötiger Ton hingenommen werden. Das Skript hebt einen bestehenden Cabin-Ready-Status niemals auf.

## Funktionsumfang

- **Automatischer Abflug-Auslöser:** Beacon-On startet einen PAX-skalierten Countdown
- **Automatischer Anflug-Auslöser:** Klappen + Fahrwerk unten löst Cabin Ready aus
- **Go-Around-sicher:** Verarbeitet Fehlanflüge ohne fehlerhafte Zustände
- **Alle ToLiss-Flugzeuge:** Funktioniert mit der gesamten ToLiss-Airbus-Familie (A319, A320neo, A321/neo, A330neo, A340-600)

## Mehrwert in der Flugsimulation

Der FWD CALL für Cabin Ready ist eine Routineaufgabe, die den Cockpit-Ablauf unterbricht — besonders in den geschäftigen Abflug- und Anflugphasen. Dieses Skript automatisiert das Verfahren realistisch (Timing skaliert nach Passagieranzahl) und ermöglicht es, sich auf das Fliegen zu konzentrieren.

## Installation

**Download:** [X-Plane.org](https://forums.x-plane.org/files/file/91876-toliss-airbus-cabin-ready-automatic-flywithlua-script/)

Die `.lua`-Datei in `Resources/plugins/FlyWithLua/Scripts/` ablegen.

## Quellen

- [Toliss Airbus Cabin Ready — X-Plane.org](https://forums.x-plane.org/files/file/91876-toliss-airbus-cabin-ready-automatic-flywithlua-script/)
