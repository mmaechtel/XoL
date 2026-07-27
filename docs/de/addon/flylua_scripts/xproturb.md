---
description: "X-ProTurb ist eine FlyWithLua-Turbulenz-Engine für X-Plane 12 — physikbasierte atmosphärische Turbulenz nach MIL-F-8785C, FAR 25.341 und ICAO 9625 Level-D, mit flugzeugspezifischer 6-DOF-Reaktion."
---
# X-ProTurb — Professional Turbulence Engine

X-ProTurb ist ein [FlyWithLua](../scripting/flywithlua.md)-Skript, das das simple Turbulenzmodell von [X-Plane](../../glossary.md#x-plane) 12 durch eine physikbasierte Engine ersetzt. Statt eines zufälligen „Wacklers" mit einem Intensitätsregler von 0–10 berechnet es Turbulenz nach denselben Zertifizierungsnormen, nach denen Full-Motion-Level-D-Airline-Simulatoren qualifiziert werden — und lässt jedes Flugzeug individuell darauf reagieren.

## Hintergrund

- **Entwickler:** sfkcyl (Safak Cayli, Level-D-Simulator-Entwickler)
- **Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/100195-x-proturb-professional-turbulence-engine/)
- **Plattformen:** Windows, macOS, Linux (über FlyWithLua)
- **Kompatibilität:** X-Plane 12
- **Abhängigkeit:** [FlyWithLua NG+](../scripting/flywithlua.md)
- **Lizenz:** Kostenlos für den privaten Gebrauch

## Die Grundidee — zwei getrennte Systeme

Die Engine trennt sauber „Was passiert in der Luft?" von „Wie reagiert mein Flugzeug darauf?":

- Die **Atmosphäre** trägt ihr eigenes, physikalisch modelliertes Turbulenzfeld.
- Das **Flugzeug** reagiert je nach Typ — Masse, Tragfläche, Geschwindigkeit und Struktur werden automatisch ausgelesen.

Eine leichte Cessna wird in derselben Böe durchgeschüttelt, die ein Großraumflugzeug kaum bemerkt — ohne Einrichtung pro Flugzeug und ohne willkürlichen Intensitätsfaktor.

## Normen

Turbulenz wird aus anerkannten Luftfahrtnormen abgeleitet statt aus abgestimmten Kurven:

- **MIL-F-8785C** — US-Militärstandard für Flugeigenschaften; die Engine kalibriert die spürbare Reaktion jedes Flugzeugs auf dessen zertifiziertes Ziel
- **FAR 25.341 (Pratt)** — FAA-Böenlastvorschrift, nach der Verkehrsflugzeuge ausgelegt werden
- **ICAO 9625 Level-D** — die höchste Realismusstufe für Vollflugsimulatoren im Airline-Pilotentraining

## Funktionsumfang

- **6-DOF-Reaktion:** Das Flugzeug bewegt sich in allen sechs Freiheitsgraden — inklusive echtem vertikalem *Heave* (dem Absacken und Hochgedrückt-werden im Sitz) sowie Sway und Surge
- **Lastvielfaches Δn:** Typabhängige Schwankung der G-Kräfte über die FAR-25.341-Pratt-Formel, automatisch aus der Geometrie jedes Flugzeugs gelesen
- **von-Kármán- / Dryden-Spektren:** Zwei anerkannte Böenmodelle, die die Turbulenzenergie über realistische Wellenlängen verteilen statt über flaches Zufallsrauschen
- **CAT:** Clear Air Turbulence mit Richardson-Zahl-Modell, tropopausen-fixiertem CAT-Profil und Kelvin-Helmholtz-Billows — die heimtückische Turbulenz, die ohne sichtbare Vorwarnung auftritt
- **Mountain-Wave-Suite:** Queney-Leewellen, Rotorzonen, Wave-Breaking, hydraulischer Sprung (Boulder/Bora-Fallwinde) und der Scorer-Parameter für gefangene vs. propagierende Wellen
- **CB-/Sturmmodellierung:** Cumulonimbus-Kerne, Hagel- und Starkregen-Turbulenz nach den offiziellen FAA-Schweregraden (leicht → extrem), mit Turbulenz-Vorwarnung
- **Wetter-Integration:** Die Engine liest X-Planes eigenes 3D-Wettergitter und kompensiert Doppelzählung — oder übernimmt die Turbulenz im eigenen Modus vollständig
- **Fly-by-Wire-Erkennung:** Bei Airbus-Maschinen erkennt die Engine das elektronische Steuerungssystem und lässt dessen Flight-Control-Laws die Charakteristik bestimmen, wie es das reale Flugzeug auch täte

## Mehrwert in der Flugsimulation

Die Default-Turbulenz von X-Plane ist im Kern ein einzelnes Zufallsruckeln mit Intensitätsregler. X-ProTurb macht daraus eine echte Physik-Engine: Die Atmosphäre wird auf Basis zertifizierungsnaher Normen modelliert, und jedes Flugzeug der Flotte reagiert nach seinen eigenen Eigenschaften darauf — ohne Abstimmung pro Flugzeug. Eine professionelle UI mit fünf farbcodierten Tabs zeigt in Echtzeit, was die Engine gerade berechnet, inklusive eines Live-Aircraft-Recognition-Chips (Typ plus Fly-by-Wire oder konventionell) und ehrlicher Anzeigen aller Quellen, die die Charakteristik beeinflussen.

## Installation

**Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/100195-x-proturb-professional-turbulence-engine/)

Die Skriptdateien in `Resources/plugins/FlyWithLua/Scripts/` ablegen. Die Engine läuft automatisch mit der gesamten Flotte — vom Segelflugzeug bis zum schweren Twin, Default, Freeware oder Study-Level — ohne Konfiguration pro Flugzeug.

## Quellen

- [X-ProTurb — forums.x-plane.org](https://forums.x-plane.org/files/file/100195-x-proturb-professional-turbulence-engine/)
