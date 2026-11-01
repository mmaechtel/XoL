---
description: "SimLoad Manager für X-Plane 12 — natives Plugin für Boarding, Fracht, Betankung und animierte Ground Ops mit Ground Planner; läuft unter Linux ohne SGES."
---
# SimLoad Manager

SimLoad Manager ist ein natives [Plugin](../../glossary.md#plugin) für [X-Plane](../../glossary.md#x-plane) 12, das realistisches Passagier-Boarding, Cargo-Beladung und Betankung simuliert und ein eigenes Ground Handling mitbringt: animierte Fahrzeuge, Passagiere und Crew, pro Flugzeug im integrierten Ground Planner angeordnet. Es arbeitet ohne SGES oder andere Plugins.

## Hintergrund

- **Entwickler:** RackhamRPL
- **Download:** [X-Plane.org](https://forums.x-plane.org/files/file/93858-simload-manager-realistic-pax-cargo-fuel-ground-operations/)
- **Plattformen:** Windows, macOS, Linux (nativer `lin_x64`-Build)
- **Kompatibilität:** X-Plane 12.4.4 oder neuer
- **Abhängigkeiten:** Keine — [SGES](../flylua_scripts/sges.md) ist optional und erfordert nur dann [FlyWithLua NG+](../scripting/flywithlua.md)
- **Optional:** SimBrief-Konto (ein angereicherter manueller Flugplan ist ebenfalls möglich)

Unterstützt werden die Laminar-Standardflotte (737-800, A330-300, MD-82, C750 und die meisten kleineren Laminar-Flugzeuge), Zibo/LevelUp 737-600 bis 900ER, alle ToLiss-Flugzeuge, X-Crafts E-Jets und ERJ, Flight Factor 757/767 und A320, FPS 747-800, Rotate MD80, FlyJSim 732 sowie die Colimata Concorde FXP. Beim Q4XP deaktiviert SimLoad Manager die Gewichts- und Treibstoff-Integration automatisch.

## Funktionsumfang

- **Beladungssimulation:** Laden und Entladen von PAX, Cargo und Treibstoff, mit automatischer Einheitenerkennung (kg/lbs)
- **Variation der Beladung:** No-Shows, Standbys, Fuel Top-up, Tankering, Low-Cost-Modus und Zufallsereignisse
- **Ground Ops:** Alle Fahrzeuge verwaltet SimLoad Manager selbst — animierte X-Plane-Fahrzeuge sowie 3D-Modelle von Isar Simworks (Treppen, ULD-Loader, Frisch- und Abwasserfahrzeuge); jedes Fahrzeug ist im Profil optional
- **Passagiere und Crew:** Animierte Passagiere und Crew
- **Ground Planner:** Editor für Bodenprofile je Flugzeug — Fahrzeugpositionen, Routen vorwärts und rückwärts, Wartezeiten, Höhenanpassung sowie Test einzelner Fahrzeuge oder ganzer Stages im Simulator
- **Fahrzeug-Beacons:** An, während der Fahrt oder aus
- **Ground-Handling-Details:** GPU-Management pro Flugzeugtyp, Checkliste, Busse und Treppen kommen nach dem Catering
- **Datenquellen:** SimBrief-Import oder angereicherter manueller Flugplan; automatische Flugplanerkennung
- **Workflows:** Departure- und Arrival-Modus, Turnaround und RON, Crew Briefing, Catering und Cleaning
- **Geschwindigkeitsmodi:** Realistic, Fast, Very Fast oder Custom
- **Sicherheitsstopps:** Alle Operationen stoppen bei aktiviertem Beacon, dazu die Regel „Don't touch the chocks“
- **Loadsheet:** SLMLS-Loadsheet, auch als ACARS-Uplink über Hoppie oder SayIntentions.ai (adressiert an Flugnummer oder SimBrief-Callsign)
- **Sound:** Umgebungsgeräusche, KI-Sprachansagen und Boarding-Musik (eigene WAV-Dateien möglich)
- **Webserver:** Die UI lässt sich auf einem zweiten Bildschirm, einem Tablet oder im AviTab-Browser öffnen
- **Integrationen:** Custom Commands, Flight Sim Deck, SimChecklist.eu, Auto-Save; UI-Sprachen EN/FR/IT/ES/DE

## Mehrwert in der Flugsimulation

Ein Turnaround braucht Zeit und folgt einer Sequenz. SimLoad Manager fügt diese Phase jedem Flug hinzu: Fahrzeuge fahren ans Flugzeug, Passagiere steigen ein, während Fracht geladen und getankt wird, und das Loadsheet kommt, sobald alles abgeschlossen ist. Die Bodenfahrzeuge gehören zum Plugin, ein separates Ground-Service-Addon ist dafür nicht nötig. Mit [XP CabinState](../cockpit/xp_cabinstate.md) kann SimLoad Manager außerdem Crew und Boarding in der Kabinensimulation steuern.

## Installation

**Download:** [X-Plane.org](https://forums.x-plane.org/files/file/93858-simload-manager-realistic-pax-cargo-fuel-ground-operations/)

Das Archiv entpacken und den kompletten Ordner `SimLoadManager/` nach `Resources/plugins/` kopieren — nicht umbenennen. Nach dem Start von X-Plane steht das Plugin unter **Plugins → SimLoad Manager** bereit.

- **Einstellungen:** Liegen in `Output/preferences/simload_settings.txt` — das Löschen des Plugin-Ordners beim Update setzt sie nicht zurück
- **Bodenprofile:** Liegen in `Resources/plugins/SimLoadManager/profiles/` und lassen sich teilen; die Builds enthalten keine Profile; Default-Profile und eine Anleitung verlinkt der Entwickler
- **Updates:** Über den [SkunkCrafts Updater](../tools/skunkcrafts_updater.md)

!!! warning "Umstieg von der FlyWithLua-Version"

    Vor der Installation des Plugins die frühere FlyWithLua-Version von SimLoad Manager aus `FlyWithLua/Scripts/` entfernen. Das Paket enthält eine optionale SGES-Brücke (`FlyWithLua_Scripts/SimLoadManager_SGES_bridge.lua` und `lua/slm5_sges.lua`). Sie wird nur benötigt, wenn SGES genutzt wird.

### Linux-Hinweise

Das Paket enthält eine native `lin_x64/SimLoadManager.xpl`. Dieses Setup wurde erfolgreich unter Linux getestet — das X-Plane-Log zeigt das Laden des Plugins aus dem `lin_x64`-Ordner. Für den SimBrief-Import nutzt der Linux-Build die System-libcurl (`libcurl.so.4`), die bei den meisten Distributionen bereits installiert ist.

## Quellen

- [SimLoad Manager — X-Plane.org](https://forums.x-plane.org/files/file/93858-simload-manager-realistic-pax-cargo-fuel-ground-operations/)
