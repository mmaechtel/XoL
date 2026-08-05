---
description: "OSM Offshore Oil Rigs platziert weltweit Offshore-Ölplattformen als Heliports in X-Plane auf Basis von OpenStreetMap-Positionsdaten."
---
# OSM Offshore Oil Rigs

OSM Offshore Oil Rigs ist ein Szeneriepaket für [X-Plane](../../glossary.md#x-plane), das Offshore-Ölplattformen als Heliports in Ozeanen und Meeren weltweit platziert. Alle Positionsdaten stammen aus der OpenStreetMap-Datenbank (OSM) und nutzen den Tag `man_made=offshore_platform`. Das Paket verwendet die in X-Plane 12 eingebauten Ölplattform-Modelle — eigene 3D-Assets sind nicht enthalten.

## Hintergrund

- **Typ:** Szeneriepaket (keine Plugin-Abhängigkeit)
- **Entwickler:** Saar Nagar (snagar.dev)
- **Distribution:** [x-plane.to](https://x-plane.to/file/1896/osm-offshore-oil-rigs) (Freeware)
- **Plattformen:** Windows, macOS, Linux (Standard-Szenerieordner, plattformunabhängig)
- **Kompatibilität:** X-Plane 12

Das Paket wurde per Skript generiert — mit dem quelloffenen Python-Tool [osm_to_xplane_dist](https://github.com/snagar/osm_to_xplane_dist) des Autors. Bei nur 298 KB besteht es vollständig aus `apt.dat`-Heliport-Definitionen und [DSF](../../glossary.md#dsf-distribution-scenery-format)-Referenzen — jede Ölplattform ist als Heliport mit Koordinaten, Ausrichtung und Helipad-Abmessungen aus OSM registriert.

??? abstract "Technischer Hintergrund: apt.dat-Heliport-Format"

    X-Plane stellt Heliports in `apt.dat`-Dateien über Row Code 17 (Heliport-Header) und Row Code 102 (Helipad-Definition) dar. Jeder Helipad-Eintrag enthält Breiten- und Längengrad (8 Dezimalstellen), Ausrichtung (True Heading), Abmessungen in Metern und Oberflächentyp. Das Format unterstützt den Metadaten-Schlüssel `is_oilrig` (Row Code 1302) zur spezifischen Kennzeichnung von Ölplattform-Heliports. Das Generierungsskript extrahiert OSM-Nodes mit dem Tag `man_made=offshore_platform`, konvertiert deren Koordinaten und filtert gegen bestehende X-Plane-Ölplattform-Positionen, um Überlappungen zu minimieren.

## Funktionsumfang

- **Weltweite Abdeckung** — Ölplattformen überall dort platziert, wo OSM Einträge mit `man_made=offshore_platform` enthält
- **OSM-basierte Positionierung** — reale Koordinaten aus der OpenStreetMap-Datenbank
- **Mission-X-Integration** — Ölplattformen dienen als Helikopter-Missionsziele für das [Mission-X](https://x-plane.to/file/135/mission-x)-Plugin (gleicher Autor), das zufällige Fracht-, Medevac- und Versorgungsmissionen zu Offshore-Plattformen ermöglicht
- **Minimaler Ressourcenbedarf** — 298 KB Gesamtgröße, keine eigenen 3D-Modelle, keine Plugin-Abhängigkeit

!!! note "OSM-Datenabdeckung"

    Die OpenStreetMap-Abdeckung für Offshore-Plattformen variiert regional. Die Nordsee (UK, Norwegen) und der Golf von Mexiko sind dank aktiver Communities und öffentlicher Behördendaten (z. B. dem U.S. Bureau of Safety and Environmental Enforcement) gut kartiert. Andere Regionen — Persischer Golf, Südostasien, Westafrika — haben trotz hoher realer Plattformdichte weniger Einträge.

## Mehrwert in der Flugsimulation

X-Planes Standard-Szenerie enthält nur eine begrenzte Anzahl von Offshore-Ölplattformen. Für Helikopterpiloten erfordern realistische Offshore-Operationen Ziele an realen Positionen — Ölplattformen als Anflugziele für Versorgung, Crew-Transfer und Notfalleinsätze. Dieses Paket schließt die Lücke, indem es Heliports an OSM-dokumentierten Plattformstandorten weltweit platziert. In Kombination mit Mission-X ermöglicht es prozedurale Helikoptermissionen zu Offshore-Zielen. Unter Linux installiert sich das Paket als gewöhnlicher Szenerieordner ohne Plugin-Abhängigkeiten.

## Installation

**Download:** [x-plane.to](https://x-plane.to/file/1896/osm-offshore-oil-rigs)

1. Den Inhalt nach `X-Plane 12/`[Custom Scenery](../../glossary.md#custom-scenery)`/` entpacken
2. X-Plane starten und beenden, um die Szenerie in der [scenery_packs.ini](../../glossary.md#scenery_packsini) zu registrieren
3. Für manuelle Anordnung den Eintrag **unterhalb** von [GLOBAL_AIRPORTS](../../glossary.md#global-airports) platzieren, um höherwertige Flughafen-Szenerie nicht zu überschreiben

**Mission-X-Nutzer:** Nach der Installation im Mission-X-Setup-Bildschirm die **APT Data Optimization** ausführen, um die neuen Heliports für die Missionsgenerierung zu indexieren.

!!! tip "Überlappungsbehandlung"

    Das Generierungsskript filtert gegen bestehende X-Plane-Ölplattform-Positionen, aber einzelne Überlappungen können verbleiben. Der Autor nimmt Meldungen über doppelte Positionen über die Distributionsseite entgegen.

---

## Weiterführende Kapitel

| Thema | Seite | Fokus |
|---|---|---|
| Szeneriekomponenten | [Wie X-Plane die Welt aufbaut](../aufbau_quellen/scenery_components.md) | scenery_packs.ini-Ladereihenfolge und Schicht-Interaktion |
| Szeneriequellen | [Quellen](../aufbau_quellen/scenery_sources.md) | Übersicht der Szenerie-Anbieter und Datenbanken |

---

## Quellen

- [OSM Offshore Oil Rigs — x-plane.to](https://x-plane.to/file/1896/osm-offshore-oil-rigs)
- [osm_to_xplane_dist — GitHub](https://github.com/snagar/osm_to_xplane_dist)
- [Mission-X — x-plane.to](https://x-plane.to/file/135/mission-x)
- [Tag:man_made=offshore_platform — OpenStreetMap-Wiki](https://wiki.openstreetmap.org/wiki/Tag:man_made=offshore_platform)
