---
description: "Einstieg in VATSIM für X-Plane — Kontoerstellung, Client-Installation und Flugplanung mit optimaler ATC-Abdeckung über den ATC Flight Planner."
---
# VATSim

VATSIM (Virtual Air Traffic Simulation Network) ist das weltweit größte Online-Aviation-Netzwerk für virtuelle Flugsimulation mit realistischem Flugverkehr und Flugsicherung.

## Was ist VATSIM?

VATSIM bietet Piloten und Fluglotsen die Möglichkeit, in einer realistischen Umgebung zu fliegen und zu arbeiten. Das Netzwerk simuliert echte Flugverkehrsabläufe mit:

- Realistischen Flugplänen
- Live-Fluglotsen
- Wetterdaten
- Flugverkehrsregeln

## Erste Schritte

Um mit VATSIM zu beginnen:

1. **VATSIM Account** — Registrierung auf [vatsim.net](https://vatsim.net)
2. **VATSIM Client** — einen kompatiblen Client herunterladen (z.B. xPilot für X-Plane, vPilot für MSFS)
3. **Flugplan** — einen realistischen Flugplan erstellen
4. **Training** — das [Pilot Learning Center](https://my.vatsim.net/learn) für Grundlagen nutzen

## Nützliche Links

- [VATSIM Website](https://vatsim.net)
- [Pilot Learning Center](https://my.vatsim.net/learn)
- [VATSIM Rules](https://vatsim.net/docs/policy)
- [Approved Software](https://vatsim.net/docs/policy/approved-software)

---

## ATC Flight Planner

Der **[ATC Flight Planner](https://atc.emvisio.de)** ist eine Webapp, die VATSIM-Flugrouten mit maximaler ATC-Abdeckung findet. Die App sammelt laufend Controller-Buchungen, Event-Zeitpläne und Live-Traffic-Daten von VATSIM und berechnet, welche Abflug-/Ankunfts-Kombinationen für ein gewähltes Zeitfenster und einen Flugzeugtyp die beste Controller-Abdeckung bieten.

### Wie funktioniert das?

Die App berechnet ATC-Abdeckungs-Zeitfenster für Flughäfen weltweit auf Basis gebuchter Controller-Sessions. Bei der Flugplanung werden diese Zeitfenster mit Flugzeug-Performance-Daten (Reisegeschwindigkeit, Reichweite) korreliert, um realistisch fliegbare und vollständig durch aktive Controller abgedeckte Routen zu ermitteln. Das Ergebnis ist eine nach kombiniertem ATC-Coverage-Score sortierte Liste von Abflug-Ziel-Paaren.

### Flug planen

1. **Flugzeug und Zeit wählen** — Flugzeugtyp und gewünschtes Abflugfenster festlegen
2. **Routen durchsuchen** — die App rankt Flughäfen nach ATC-Verfügbarkeit, optional filterbar nach Coverage-Score, Live-Traffic-Dichte oder Bahnlänge
3. **Karte erkunden** — Flughäfen sind farbcodiert nach Abdeckungsqualität für visuelle Routenfindung
4. **ATC-Timeline prüfen** — ein 7-Tage-Controller-Buchungsplan zeigt genau, wann an jedem Flughafen Abdeckung verfügbar ist
5. **An SimBrief übergeben** — ein Klick generiert einen SimBrief-Flugplan mit vorausgefülltem Abflug, Ziel, Flugzeugtyp, Airline und Callsign

### Geführte Workflows

Die App enthält eingebaute Workflow-Anleitungen (oben rechts, neben dem Hilfe-Button), die verschiedene Anwendungsfälle Schritt für Schritt durchgehen — von Quick Dispatch über Event-Flüge bis hin zur Livery-first-Planung.

**Optimal Routes — der schnellste Weg zum Flugplan**

Der "Optimal Routes"-Workflow generiert einen vollständig ausgefüllten SimBrief-Flugplan mit 100% ATC-Abdeckung in nur wenigen Klicks: Abflugdatum/-zeit eingeben, maximale akzeptable Verzögerung und gewünschte Flugdauer festlegen, dann "Find Routes" klicken. Das System findet automatisch die besten Abflughäfen mit ATC, sucht für jeden das optimale Ziel und verschiebt den Abflugzeitpunkt in 15-Minuten-Schritten, um die kombinierte ATC-Abdeckung zu maximieren. Die Ergebnisse sind nach Combined Score (0–9) gerankt — ein Klick auf das beste Ergebnis übergibt alles an SimBrief.

### Weitere Features

- **Event-Integration** — anstehende VATSIM-Events durchsuchen und passende Abflug- oder Ankunftsflughäfen innerhalb des Event-Zeitfensters finden
- **Livery-Auswahl** — Airline-Lackierungen nach Land filtern und direkt in den Flugplan übernehmen
- **Live-Traffic-Ansicht** — zeigt, welche Flughäfen aktuell die meisten aktiven Piloten haben

!!! tip "Flugzeug- und Livery-Konfiguration"
    Die vorkonfigurierten Flugzeugtypen und Lackierungen sind auf ToLiss und X-Plane ausgerichtet. Alle Flugzeug-Performance-Daten (Reisegeschwindigkeit, Reichweite, Flugphasen-Dauern) lassen sich individuell anpassen, um jeden Flugzeugtyp abzubilden.

---

## Weiterführende Kapitel

| Thema | Seite | Schwerpunkt |
|---|---|---|
| Clearance | [Clearance](../atc/clearance.md) | IFR-Freigabeverfahren und CPDLC |
| Pushback & Taxi | [Pushback & Taxi](../atc/pushback_taxi.md) | Rollverfahren am Boden |
| Streckenflug | [Streckenflug](../atc/enroute.md) | Center-Lotse und Frequenzwechsel |
| Anflug | [Anflug](../atc/approach.md) | Anflugverfahren und Radar Vectors |
| Wetter-Briefing | [Wetter-Briefing](../weather/briefing.md) | Wettervorbereitung für Online-Flüge |
