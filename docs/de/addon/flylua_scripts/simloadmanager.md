# SimLoad Manager

SimLoad Manager ist ein [FlyWithLua](../scripting/flywithlua.md)-Skript, das realistisches Passagier-Boarding, Cargo-Beladung und Betankung für X-Plane 12 simuliert. Es integriert sich mit SimBrief, um Flugplandaten (Passagieranzahl, Frachtgewicht, Treibstoffmengen) zu importieren und bietet Echtzeit-Fortschrittsbalken mit dynamischen Zeitschätzungen.

## Hintergrund

- **Entwickler:** RackhamRPL
- **Download:** [X-Plane.org](https://forums.x-plane.org/files/file/93858-simload-manager-realistic-pax-cargo-fuel-ground-operations/)
- **Plattformen:** Windows, macOS, Linux (reines Lua)
- **Kompatibilität:** X-Plane 12
- **Abhängigkeiten:** [FlyWithLua NG+](../scripting/flywithlua.md), SimBrief-Konto (erforderlich), [SGES](https://forums.x-plane.org/files/file/62296-simple-ground-equipment-services-low-tech-services/) (optional, für visuelles Bodenequipment)

Das Skript wird aktiv gepflegt und häufig aktualisiert. Es funktioniert mit jedem Flugzeug — keine flugzeugspezifische Konfiguration nötig.

## Funktionsumfang

- **Realistische Beladungssimulation:** Passagiere steigen dynamisch basierend auf Cargo- und Treibstoff-Fortschritt ein
- **SimBrief-Integration:** Importiert automatisch PAX-Anzahl, Frachtgewicht, Treibstoff und Zeiten aus dem aktuellen Flugplan
- **Mehrere Geschwindigkeitsmodi:** Realistisch, Schnell, Sehr schnell oder Benutzerdefiniert (frei editierbares Timing)
- **Fortschrittsvisualisierung:** Echtzeit-Fortschrittsbalken mit dynamischen Zeitschätzungen für PAX, Cargo und Treibstoff
- **Loadsheet-Generierung:** Automatisches realistisches Loadsheet (SLMLS-System)
- **SGES-Integration:** Bei installiertem SGES begleitet visuelles Bodenequipment (Treppen, Gepäckbänder, Tankwagen, Pylonen, Passagierfluss) den Beladungsvorgang
- **Soundeffekte:** Umgebungsgeräusche und KI-generierte Sprachansagen während der Beladung
- **AutoDGS-Kompatibilität:** Vermeidet Jetway-Konflikte bei erkanntem AutoDGS
- **API für externe Tools:** Exponierte DataRefs und FlyWithLua-Befehle

## Mehrwert in der Flugsimulation

Sofortiges Laden bricht die Immersion — reale Turnarounds benötigen Zeit und folgen einer Sequenz. SimLoad Manager fügt jedem Flug eine realistische Bodenoperationsphase hinzu: Passagiere steigen ein, während Fracht geladen wird, Tankwagen kommen, und das Loadsheet wird nach Abschluss generiert. In Kombination mit SGES wird das Vorfeld während des Turnarounds lebendig.

## Installation

**Download:** [X-Plane.org](https://forums.x-plane.org/files/file/93858-simload-manager-realistic-pax-cargo-fuel-ground-operations/)

Die Skript-Dateien in `Resources/plugins/FlyWithLua/Scripts/` ablegen:

- `SimLoadManager.lua` — Hauptskript
- `SimLoadManager_loadsheet.lua` — Loadsheet-Modul
- `SimLoad-Manager-Sounds/` — Soundeffekte-Ordner

Einstellungen werden in `FlyWithLua/Modules/simload_settings.txt` gespeichert (wird beim ersten Start automatisch erstellt).

!!! warning "Update von Versionen vor v1.9.0"

    Vor dem Update `FlyWithLua/Modules/simload_settings.txt` löschen. Die Datei wird beim Start automatisch neu erstellt. Ohne Löschung können falsche Timings oder Interface-Fehler auftreten.

## Quellen

- [SimLoad Manager — X-Plane.org](https://forums.x-plane.org/files/file/93858-simload-manager-realistic-pax-cargo-fuel-ground-operations/)
