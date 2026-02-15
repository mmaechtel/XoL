# Follow the Greens

Follow the Greens (FtG) ist ein Taxiway-Leitsystem nach realem Vorbild (A-SMGCS — Advanced Surface Movement Guidance and Control System). Das [Plugin](../glossary.md#plugin) aktiviert grüne Rollbahnlichter vor dem Flugzeug und signalisiert Haltepositionen mit roten Lichtern — wie es an Flughäfen wie London Heathrow, Dubai, München und Seoul bereits im Einsatz ist.

## Hintergrund

- **Entwickler:** Pierre Mareschal (devleaks)
- **Repository:** [github.com/devleaks/followthegreens](https://github.com/devleaks/followthegreens) (Open Source, MIT-Lizenz)
- **Plattformen:** Windows, macOS, Linux (plattformunabhängig via Python)
- **Kompatibilität:** [X-Plane](../glossary.md#x-plane) 12 (Release 2), X-Plane 11 + 12 (Release 1, nur noch kritische Fixes)
- **Preis:** Kostenlos

Das Plugin wird aktiv weiterentwickelt. Release 2 ("Follow the Greens 4D") fügt Geschwindigkeitsmanagement hinzu — ein A-SMGCS Level 4 Feature.

## Funktionsumfang

- **Grüne Rollbahnlichter:** Leuchten progressiv vor dem Flugzeug auf und zeigen die Taxi-Route an
- **Rote Haltebalken:** Signalisieren Halt an Kreuzungen und Rollhaltepunkten
- **4D-Geschwindigkeitsmanagement:** Das "Rabbit"-Licht (pulsierende Lichtfolge) passt Geschwindigkeit und Lauflänge automatisch an — schnell und weit bedeutet Beschleunigen, langsam und kurz bedeutet Bremsen
- **Routing-Algorithmus:** Berücksichtigt Taxiway-Breiten, Einbahnstraßen-Beschränkungen und Netzwerk-Constraints
- **Taxiway-Anzeige:** ShowTaxiways-Modus zum Hervorheben des gesamten Rollbahnnetzes
- **Pistenbeleuchtung:** Intensität der Pistenbeleuchtung einstellbar
- **Command-Bindings:** Aktionen (OK, Cancel, Clearance, Speed, Bookmark, NewGreens) lassen sich an Tasten oder Buttons binden
- **[SkunkCrafts Updater](skunkcrafts_updater.md):** Automatische Updates werden unterstützt

## Mehrwert in der Flugsimulation

Die gelben Bodenpfeile in X-Plane zeigen zwar die allgemeine Taxi-Richtung, bieten aber kein dynamisches Leitsystem. Follow the Greens ergänzt progressive Beleuchtung und Geschwindigkeitsempfehlungen — besonders hilfreich an unbekannten Flughäfen mit komplexen Rollwegen.

## Installation

**Voraussetzung:** [XPPython3](xppython3.md) (ab Version 4.5). XPPython3 enthält einen eigenen Python-Interpreter — eine separate Python-Installation ist nicht erforderlich.

**Download:** [GitHub Releases](https://github.com/devleaks/followthegreens/releases)

Die Dateien `PI_FollowTheGreens.py`, `PI_SetRunwayLightIntensity.py` und den Ordner `followthegreens/` nach `Resources/plugins/PythonPlugins/` kopieren. Nach dem Neuladen der Python-Skripte erscheint im Plugin-Menü der Eintrag "Follow the greens...".

Da FtG ein reines Python-Plugin ist, werden keine nativen Binaries benötigt. Es sind keine Linux-spezifischen Probleme bekannt.

!!! info "Voraussetzung: Taxiway-Netzwerk"

    FtG benötigt ein definiertes Taxiway-Netzwerk im Flughafen. Standard-Flughäfen in X-Plane erfüllen diese Voraussetzung. Bei Custom-Szenerien ohne Taxiway-Netzwerk funktioniert das Plugin nicht.

## Quellen

- [Follow the Greens — GitHub](https://github.com/devleaks/followthegreens)
- [Follow the Greens — Dokumentation](https://devleaks.github.io/followthegreens/)
- [Follow the Greens — forums.x-plane.org](https://forums.x-plane.org/files/file/71124-follow-the-greens/)
