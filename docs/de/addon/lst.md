# LST (Living Scenery Technology)

LST ist ein natives [Plugin](../glossary.md#plugin), das Flughafenszenerie durch animierten Bodenverkehr zum Leben erweckt. Fahrzeuge, Fußgänger, Bodendienstfahrzeuge und Züge bewegen sich entlang definierter Routen — inklusive realistischer Staus, Beschleunigung und Abbremsung.

## Hintergrund

- **Entwickler:** X-Codr Designs
- **Website:** [x-codrdesigns.com](https://www.x-codrdesigns.com/living-scenery-technology)
- **Download:** [X-Plane.org](https://forums.x-plane.org/files/file/82876-living-scenery-technology/)
- **Plattformen:** Windows, macOS, Linux (native Binaries)
- **Kompatibilität:** X-Plane 12

LST ist der moderne Nachfolger des älteren GroundTraffic-Plugins. Wo GroundTraffic pro Szenerie eine eigene Plugin-Instanz benötigte (begrenzt auf ~30–40), arbeitet LST als globales Plugin, das beliebig viele Szenerien gleichzeitig bedient. Das Plugin wird aktiv gepflegt.

## Funktionsumfang

- **Routenbasierte Animation:** Objekte bewegen sich entlang entwicklerdefinierter Pfade mit realistischer Beschleunigung und Abbremsung
- **Verzweigungen:** Objekte wechseln zufällig zwischen Routen für natürlichen Verkehrsfluss — kein plötzliches Erscheinen an unnatürlichen Stellen
- **Mindestabstand:** Fahrzeuge halten automatisch Abstand und bremsen stufenweise ab (Stau-Simulation)
- **Partikelsystem:** Zugriff auf X-Plane-12-Partikeleffekte (Abgase, Rauch) an Szenerieobjekten
- **FMOD-Sound:** Richtungsabhängige, entfernungsgedämpfte Sounds an bewegten und statischen Objekten
- **Positions-Trigger:** Ereignisse an bestimmten Orten auslösen (z.B. Türen öffnen bei Fahrzeugankunft)
- **Performance:** Tausende animierte Objekte bei weniger als 5–10 % Framerate-Einbuße

## Mehrwert in der Flugsimulation

Ohne LST wirken Flughafenszenerien statisch — Vorfeldfahrzeuge stehen reglos, Straßen bleiben leer. LST bringt Bewegung in die Szenerie: Busse pendeln zwischen Terminals, Gepäckwagen fahren zum Flugzeug, Autos fließen auf den Zufahrtsstraßen. Immer mehr Szenerie-Entwickler integrieren LST in ihre Produkte, wodurch der Nutzen mit jeder neuen Szenerie wächst.

## Installation

**Download:** [X-Plane.org](https://forums.x-plane.org/files/file/82876-living-scenery-technology/)

Den Ordner `Living Scenery Technology` nach `Resources/plugins/` kopieren. Das Plugin aktiviert sich automatisch, sobald eine LST-fähige Szenerie geladen wird.

### Linux-Hinweise

Die Linux-Binary ist im Download enthalten. Es sind keine Linux-spezifischen Probleme bekannt.

Die offiziellen Entwickler-Tools (Konverter, Generator) sind Windows-only. Für Linux existiert die Community-Alternative [lst-utils](https://github.com/devleaks/lst-utils) (Python, MIT-Lizenz).

## Quellen

- [LST — X-Plane.org](https://forums.x-plane.org/files/file/82876-living-scenery-technology/)
- [LST — X-Codr Designs](https://www.x-codrdesigns.com/living-scenery-technology)
