---
description: "SimLoad Manager für X-Plane 12 — FlyWithLua-Skript zur realistischen Simulation von Boarding, Fracht- und Treibstoffbeladung."
---
# SimLoad Manager

SimLoad Manager ist ein [FlyWithLua](../scripting/flywithlua.md)-Skript, das realistisches Passagier-Boarding, Cargo-Beladung und Betankung für X-Plane 12 simuliert. Es integriert sich mit SimBrief, um Flugplandaten (Passagieranzahl, Frachtgewicht, Treibstoffmengen) zu importieren und bietet Echtzeit-Fortschrittsbalken mit dynamischen Zeitschätzungen.

## Hintergrund

- **Entwickler:** RackhamRPL
- **Download:** [X-Plane.org](https://forums.x-plane.org/files/file/93858-simload-manager-realistic-pax-cargo-fuel-ground-operations/)
- **Plattformen:** Windows, macOS, Linux (reines Lua)
- **Kompatibilität:** X-Plane 12
- **Abhängigkeiten:** [FlyWithLua NG+](../scripting/flywithlua.md), [SGES](https://forums.x-plane.org/files/file/62296-simple-ground-equipment-services-low-tech-services/) (für Bodenequipment-Integration)
- **Optional:** SimBrief-Konto (manuelle Eingabe und Flight Sim Deck ebenfalls als Datenquellen nutzbar)

Das Skript wird aktiv gepflegt und häufig aktualisiert. Unterstützt werden Laminar-Standardflugzeuge (B737-800, A330-300, MD-82), Zibo/Level Up B737-Varianten, ToLiss-Flugzeuge, X-Crafts E-Jets, Flight Factor 757/767 und FPS 747-800. Q4XP ist ausgenommen (nutzt eigenes Tablet-System).

## Funktionsumfang

- **Realistische Beladungssimulation:** Passagiere steigen dynamisch basierend auf Cargo- und Treibstoff-Fortschritt ein, mit automatischer Einheitenerkennung (kg/lbs)
- **Mehrere Datenquellen:** SimBrief Auto-Import, manuelle Eingabe oder Flight Sim Deck-Integration
- **Departure- und Arrival-Modi:** Zwei getrennte Workflows mit jeweils eigenen Schritten
- **Turnaround und RON:** Automatische Flugplanerkennung beim Turnaround, Remain Over Night-Handling
- **Ground-Handling-Phasen:** Crew Briefing, Catering & Cleaning in den Workflow integriert (Crew Briefing per Einstellung überspringbar)
- **Mehrere Geschwindigkeitsmodi:** Realistisch, Schnell, Sehr schnell oder Benutzerdefiniert (frei editierbares Timing)
- **Fortschrittsvisualisierung:** Echtzeit-Fortschrittsbalken mit dynamischen Zeitschätzungen für PAX, Cargo und Treibstoff
- **Loadsheet-Generierung:** Automatisches realistisches Loadsheet (SLMLS-System), passt sich der Datenquelle an
- **SGES-Integration:** Löst automatisch Treppen, Gepäckbänder, Tankwagen, Pylonen und Passagierfluss je nach Standtyp aus
- **Beacon-basierte Sicherheitsstopps:** Alle Operationen stoppen bei aktiviertem Beacon-Light
- **Soundeffekte:** Umgebungsgeräusche und KI-generierte Sprachansagen während der Beladung
- **AutoDGS-Kompatibilität:** Jetway/Treppen-Steuerung mit Konfliktvermeidung
- **SimChecklist.eu-Integration:** Anbindung an den Online-Checklisten-Dienst
- **Flight-Save und Fortsetzen:** Automatische Zustandssicherung bei Mode-Wechseln — unterbrochene Flüge per „Load Last Flight" fortsetzbar
- **ACARS-Loadsheet-Uplink:** Loadsheet-Übertragung an ToLiss-Flugzeuge über das Hoppie-Netzwerk (ACARS)
- **API für externe Tools:** Eigene X-Plane-Commands und exponierte DataRefs

## Mehrwert in der Flugsimulation

Sofortiges Laden bricht die Immersion — reale Turnarounds benötigen Zeit und folgen einer Sequenz. SimLoad Manager fügt jedem Flug eine realistische Bodenoperationsphase hinzu: Passagiere steigen ein, während Fracht geladen wird, Tankwagen kommen, und das Loadsheet wird nach Abschluss generiert. In Kombination mit SGES wird das Vorfeld während des Turnarounds lebendig.

## Installation

**Download:** [X-Plane.org](https://forums.x-plane.org/files/file/93858-simload-manager-realistic-pax-cargo-fuel-ground-operations/)

Folgendes in `Resources/plugins/FlyWithLua/Scripts/` ablegen:

- `SimLoadManager.lua` — Hauptskript
- `SLM-Data/` — Datenordner (Sounds, Loadsheet-Modul, Einstellungen)

Den `SLM-Data/`-Ordner und dessen Inhalte nicht umbenennen.

!!! warning "Update von früheren Versionen"

    Vor der Installation von v3.x alle bisherigen SimLoad Manager-Dateien aus `FlyWithLua/Scripts/` löschen. Die Ordnerstruktur hat sich geändert — alte Dateien wie `SimLoadManager_loadsheet.lua` und `SimLoad-Manager-Sounds/` werden nicht mehr verwendet.

## Quellen

- [SimLoad Manager — X-Plane.org](https://forums.x-plane.org/files/file/93858-simload-manager-realistic-pax-cargo-fuel-ground-operations/)
