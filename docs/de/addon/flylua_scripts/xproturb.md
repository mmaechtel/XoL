---
description: "X-ProTurb — FlyWithLua-Turbulenz-Engine für X-Plane 12 mit physikbasierten Atmosphärenmodellen (MIL-F-8785C, ICAO 9625) und flugzeugspezifischer Böenreaktion."
---
# X-ProTurb — Professional Turbulence Engine

X-ProTurb ist ein [FlyWithLua](../scripting/flywithlua.md)-Skript, das das simple Turbulenzmodell von [X-Plane](../../glossary.md#x-plane) 12 durch eine physikbasierte Engine ersetzt. Statt eines zufälligen „Wacklers" mit einem Intensitätsregler von 0–10 berechnet es Turbulenz nach denselben Zertifizierungsnormen, nach denen Full-Motion-Level-D-Airline-Simulatoren qualifiziert werden — und lässt jedes Flugzeug individuell darauf reagieren.

## Hintergrund

- **Entwickler:** sfkcyl (Safak Cayli, Level-D-Simulator-Entwickler)
- **Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/100195-x-proturb-professional-turbulence-engine/)
- **Plattformen:** Windows, macOS (Intel und Apple Silicon), Linux — native Bibliotheken, mit automatischem Fallback auf eine gleichwertige Lua-Implementierung
- **Kompatibilität:** X-Plane 12
- **Abhängigkeit:** [FlyWithLua NG+](../scripting/flywithlua.md) 2.8.13 oder neuer; unter Linux und macOS Python 3 für den optionalen LiveCAT-Helfer
- **Lizenz:** Kostenlos für den privaten Gebrauch

## Die Grundidee — zwei getrennte Systeme

Die Engine trennt sauber „Was passiert in der Luft?" von „Wie reagiert mein Flugzeug darauf?":

- Die **Atmosphäre** trägt ihr eigenes, physikalisch modelliertes Turbulenzfeld.
- Das **Flugzeug** reagiert je nach Typ — Masse, Tragfläche, Geschwindigkeit und Struktur werden automatisch ausgelesen.

Eine leichte Cessna wird in derselben Böe durchgeschüttelt, die ein Großraumflugzeug kaum bemerkt — ohne Handabstimmung pro Flugzeug und ohne willkürlichen Intensitätsfaktor.

## Normen

Turbulenz wird aus anerkannten Luftfahrtnormen abgeleitet statt aus abgestimmten Kurven:

- **MIL-F-8785C** — US-Militärstandard für Flugeigenschaften; die Engine skaliert die spürbare Reaktion jedes Flugzeugs auf dessen zertifiziertes Ziel
- **FAR 25.341 (Pratt)** — FAA-Böenlastvorschrift, nach der Verkehrsflugzeuge ausgelegt werden
- **ICAO 9625 Level-D** — die höchste Realismusstufe für Vollflugsimulatoren im Airline-Pilotentraining

## Funktionsumfang

- **Böen an der Zelle:** Vertikal- und Seitenböen wirken auf X-Planes eigene Flügel-, Höhenleitwerks- und Seitenleitwerkselemente, sodass Profildaten, Klappen, Machzahl und Flächenbelastung des Flugzeugs die Reaktion bestimmen; die Böe läuft mit den richtigen Verzögerungen von der Nase zum Heck
- **Kalibrierung:** Eine einmalige Messung je Flugzeug erfasst, wie Rumpf, Triebwerksgondeln und andere Körper auf Böen reagieren (siehe [Kalibrierung](#kalibrierung)). Die Kalibrierung ist optional; ohne sie reagieren diese Körper nicht auf Böen
- **Lastvielfaches Δn:** Typabhängige Schwankung der G-Kräfte über die FAR-25.341-Pratt-Formel, automatisch aus der Geometrie jedes Flugzeugs gelesen
- **von-Kármán- / Dryden-Spektren:** Zwei anerkannte Böenmodelle, die die Turbulenzenergie über realistische Wellenlängen verteilen statt über flaches Zufallsrauschen
- **CAT:** Clear Air Turbulence mit Richardson-Zahl-Modell, tropopausen-fixiertem CAT-Profil und Kelvin-Helmholtz-Billows — die heimtückische Turbulenz, die ohne sichtbare Vorwarnung auftritt
- **Mountain-Wave-Suite:** Queney-Leewellen, Rotorzonen, Wave-Breaking, hydraulischer Sprung (Boulder/Bora-Fallwinde) und der Scorer-Parameter für gefangene vs. propagierende Wellen
- **CB-/Sturmmodellierung:** Cumulonimbus-Kerne, Hagel- und Starkregen-Turbulenz nach den offiziellen FAA-Schweregraden (leicht → extrem), mit Turbulenz-Vorwarnung
- **Wetter-Integration:** Die Engine liest X-Planes eigenes 3D-Wettergitter, misst im Flug, wie viel Turbulenz X-Planes Wetter tatsächlich auf das Flugzeug bringt, und ergänzt nur die Energie darüber — nichts wird doppelt gezählt
- **Oberflächenrauigkeit:** Die bodennahe Turbulenz folgt dem Gelände in Luv, entnommen aus der ESA-WorldCover-Karte mit 10 m Auflösung (Wald, Stadt, Ackerland, Wasser); Pisten und Vorfelder zählen als offenes Gelände
- **LiveCAT:** Optionaler Helfer für reale Daten (GFS-Grenzschicht, Bodenwärmefluss, CAT-/SIGMET-/PIREP-Hinweise); ohne Internet läuft die Engine vollständig weiter
- **Zwei Skalen:** ATMOSPHERE bewertet die Turbulenz in der Luft auf der ICAO-EDR-Skala, AIRCRAFT zeigt, was am Pilotensitz ankommt — ein Großraumflugzeug erlebt die atmosphärische Stufe „moderate“ als leichtes Rütteln
- **Fly-by-Wire-tauglich:** Die Engine greift nie in Steuerung, Autopilot, Fly-by-Wire-Gesetze oder Gierdämpfer ein
- **Panel:** Fünf Tabs (Status, Weather, Phenomena, Aircraft, Settings) mit einem Balken je Turbulenzquelle, EDR-Anzeigen, einem PIREP im AIM-Format und einer Vorhersage rund 25 nm voraus

## Mehrwert in der Flugsimulation

Die Default-Turbulenz von X-Plane ist im Kern ein einzelnes Zufallsruckeln mit Intensitätsregler. X-ProTurb macht daraus eine echte Physik-Engine: Die Atmosphäre wird auf Basis zertifizierungsnaher Normen modelliert, und jedes Flugzeug der Flotte reagiert nach seinen eigenen Eigenschaften darauf — ohne Handabstimmung pro Flugzeug. Typischer Aufwand: unter 1 ms pro Frame.

## Installation

**Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/100195-x-proturb-professional-turbulence-engine/)

Das komplette Paket nach `Resources/plugins/FlyWithLua/Scripts/` kopieren:

- das Skript `X-ProTurb_*.lua`
- den Ordner `XPT_Runtime` (vollständig)
- `xproturb_livecat.py` (Linux und macOS; Windows nutzt `xproturb_livecat.exe`)
- die sechs Dateien `albedo_*.csv`

Beim Update zuerst die alte `X-ProTurb_*.lua` löschen; ob die Einstellungsdatei `X-ProTurb.txt` erhalten bleiben kann, steht im mitgelieferten Changelog. Schritt-für-Schritt-Anleitungen je Plattform enthält `KURULUM_INSTALL.txt`. Das Panel öffnet sich über `Plugins > FlyWithLua > FlyWithLua Macros > X-ProTurb`.

### Kalibrierung

Die Kalibrierung wird einmal je Flugzeug über eine Schaltfläche in der oberen Leiste des Panels gestartet und dauert etwa 1,5 Minuten. Vorher das Wetter manuell auf Clear stellen; die Triebwerke müssen laufen. Das Flugzeug wird rund 300 m über den Boden gehoben, durchläuft die Tests für jede Klappenstellung und wird anschließend an seiner Ausgangsposition abgesetzt. Ein Neustart des Simulators ist nicht nötig — den Flug neu einrichten und weiterfliegen.

## Quellen

- [X-ProTurb — forums.x-plane.org](https://forums.x-plane.org/files/file/100195-x-proturb-professional-turbulence-engine/)
