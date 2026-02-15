# SGES — Simple Ground Equipment & Services

SGES ist ein [FlyWithLua](flywithlua.md)-Skript, das umfangreiche Bodenabfertigungs-Ausrüstung zu [X-Plane](../glossary.md#x-plane) 12 hinzufügt. Es platziert und animiert statische und bewegte Objekte rund um das Flugzeug auf dem Vorfeld — von GPU und Tankwagen bis hin zu animierten Passagieren und einem vereinfachten Marshaller.

## Hintergrund

- **Entwickler:** XPJavelin
- **Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/62296-simple-ground-equipment-services-low-tech-services/)
- **Plattformen:** Windows, macOS, Linux (reines Lua)
- **Kompatibilität:** X-Plane 12
- **Abhängigkeit:** [FlyWithLua NG+](flywithlua.md)
- **Updates:** Über [SkunkCrafts Updater](skunkcrafts_updater.md)

## Funktionsumfang

- **Vorfeldfahrzeuge:** GPU, ASU, Tankwagen, Bandlader, ULD-Lader, Catering-Fahrzeug, Bus, Gepäckwagen, Follow-Me-Car
- **Statische Ausrüstung:** Pylonen, funktionale Bremsklötze (verhindern Rollen auf geneigten Vorfeldern), Fluggasttreppen mit Wartungstreppen-Variante
- **Animierte Elemente:** Animierte Passagiere, fahrende Fahrzeuge (Follow-Me-Car, Rettungswagen, Tankwagen, Gepäckwagen, Passagierbus), vereinfachter Marshaller
- **Pushback:** Einfacher Pushback mit Schlepper, kompatibel mit Flugzeugträgern
- **Enteisung:** Aktive Enteisung, die das Flugzeug für eine konfigurierbare Zeitspanne vor X-Plane-Vereisung schützt (aktiviert sich nur bei niedrigen Temperaturen)
- **Adaptives Ground-Kit:** Passt Ausrüstung automatisch an Frachter, Passagierflugzeuge, Regionalflieger, Business-Jets oder GA-Flugzeuge an
- **Militär-Variante:** Grün lackierte Fahrzeuge für militärische Vorfeld-Szenarien
- **Fangsysteme:** Fangseile, Netzbarrieren, EMAS (Engineered Material Arresting System)
- **Notfall-Szenarien:** Unfälle, Brände, Schiffswracks, Industrie-/Waldbrände (löschbar durch X-Plane-Wasserbomber)

Alle Ausrüstungsteile sind über ein nicht-invasives Popup-Menü einzeln umschaltbar. Kompatibel mit X-Plane 12.2+ nativen Bremsklötzen.

## Mehrwert in der Flugsimulation

SGES füllt die Lücke zwischen statischen Default-Vorfeldern und kostenpflichtigen Ground-Service-Lösungen. Das adaptive Ground-Kit passt die Ausrüstung automatisch an den Flugzeugtyp an — keine manuelle Konfiguration nötig. Die funktionalen Bremsklötze und der animierte Bodenverkehr erhöhen die Immersion, ohne weitere Ground-Service-Plugins vorauszusetzen. SGES ergänzt [Better Pushback](betterpushback.md) (für realistischen Pushback) und [openSAM](opensam.md) (für Jetways und VDGS).

## Installation

**Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/62296-simple-ground-equipment-services-low-tech-services/)

Die SGES-Dateien in `Resources/plugins/FlyWithLua/Scripts/` ablegen. Die mitgelieferte `skunkcrafts_updater.cfg` kommt nach `Resources/plugins/FlyWithLua/` (Root, nicht Scripts).

Nach dem ersten Start eine Taste für das SGES-Menü zuweisen über `Settings > Keyboard`. Den Flughafen-Cache über `Plugins > FlyWithLua > Macros > SGES refresh` generieren.

SGES wird mit fünf PDF-Handbüchern geliefert, die allgemeine Nutzung, animierte Passagiere, Fangsysteme und Marshaller-Funktionen abdecken.

## Quellen

- [SGES — forums.x-plane.org](https://forums.x-plane.org/files/file/62296-simple-ground-equipment-services-low-tech-services/)
- [SGES — x-plane.to](https://x-plane.to/file/176/simple-ground-equipment-services-low-tech-ground-services)
