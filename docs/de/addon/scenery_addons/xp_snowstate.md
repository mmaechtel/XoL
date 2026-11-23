---
description: "XP SnowState für X-Plane 12 — natives Plugin, das X-Planes Schnee mit echten Schneehöhen aus Messstationen und Wettermodellen korrigiert; Beta mit Linux-Build."
---
# XP SnowState

XP SnowState ist ein natives [Plugin](../../glossary.md#plugin) für [X-Plane](../../glossary.md#x-plane) 12. Es vergleicht den Schnee, den X-Plane zeigt, mit echten Schneehöhen aus Messstationen und Wettermodellen und korrigiert nur, wenn X-Plane klar danebenliegt. Das Paket enthält einen nativen Linux-Build.

!!! note "Beta"

    XP SnowState ist derzeit eine zeitlich begrenzte Beta, die bis zum 29. November 2026 läuft. Einen öffentlichen Download gibt es noch nicht; diese Seite enthält deshalb keinen Download-Link. Die Beschreibung kann sich bis zur Veröffentlichung ändern.

## Hintergrund

- **Entwickler:** Isar Simworks (München)
- **Website:** [isarsimworks.de](https://isarsimworks.de/)
- **Lizenz:** Noch nicht angekündigt
- **Status:** Zeitlich begrenzte Beta bis 29. November 2026, kein öffentlicher Download
- **Plattformen:** Windows 10/11 (64 Bit), Linux (64 Bit), macOS 11+
- **Kompatibilität:** X-Plane 12; 12.4.4+ empfohlen und für den Modus REGIONAL nötig
- **Abhängigkeiten:** Keine (kein XPPython3); eine Internetverbindung ist erforderlich

Seit 12.4.4 zeichnet X-Plane bei Real Weather selbst regionalen Schnee; die Daten stammen aus einem GFS-Raster von 0,25° (rund 28 km breite Zellen). Im Flachland passt das, in den Bergen mittelt eine Zelle aber Tal und Gipfel: Täler bekommen zu viel Schnee, Gipfel zu wenig. Als Beispiel aus dem Test nennt der Entwickler Innsbruck, wo X-Plane 9 cm am Flughafen zeigte, obwohl dort kein Schnee lag.

## Funktionsumfang

- **Wettermodelle:** Schneehöhe von Open-Meteo (DWD ICON, ECMWF, NOAA GFS, MeteoSwiss 1 km), passend zur echten Geländehöhe gewählt
- **Messstationen:** Weltweite SYNOP-Meldungen und nationale Messnetze (SLF, GeoSphere Austria, DWD, SNOTEL, JMA, FMI, SMHI), gewichtet nach Entfernung, Höhenunterschied und Alter
- **Pistenzustand:** Schnee, Matsch oder Eis auf den Pisten aus der METAR-Pistenzustandsgruppe, aus dem Wetter abgeleitet oder manuell gesetzt
- **Bedienung:** Fenster im Simulator und WebUI in jedem Browser unter `http://127.0.0.1:8797/`, auf Deutsch und Englisch
- **Diagnose:** METAR in der Nähe im Klartext, Stationen mit Höhe und Entfernung sowie X-Planes eigener Schneewert im direkten Vergleich

## Modi

Der Modus bestimmt, wie weit das Plugin eingreift. Voreingestellt ist AUTO.

| Modus | Verhalten |
|---|---|
| AUTO | Korrigiert nur bei klarer Abweichung (ab 3 cm und 50 %) und gibt an X-Plane zurück, sobald es wieder stimmt |
| ECHT | Setzt immer die echte Schneehöhe |
| REGIONAL | Schreibt echte Schneehöhen rund um das Flugzeug in X-Planes eigene Schneedatei; X-Plane verteilt den Schnee danach selbst. Originale werden gesichert und wiederhergestellt |
| MANUELL | Fester Wert zum Testen |
| BEOBACHTEN | Schreibt nichts, vergleicht nur |
| AUS | Plugin inaktiv |

In AUTO, ECHT und MANUELL gilt der Schneewert für die gesamte sichtbare Szene. REGIONAL wirkt nur mit X-Planes Real Weather: Jeder Gitterpunkt in X-Planes Schneedatei erhält die Schneehöhe, die zu seiner Geländehöhe passt, und am Boden sowie im Anflug stimmt der Wert an der Flugzeugposition genau. Das Raster bleibt bei 0,25°, der Schnee unterscheidet sich also von Region zu Region, nicht aber zwischen einem Tal und dem Gipfel direkt darüber.

## Mehrwert in der Flugsimulation

Bei Winterflügen zu Talflughäfen wie Innsbruck, Samedan oder Bozen entscheidet der Schnee am Platz darüber, wie der Anflug aussieht und wie sich die Piste verhält. Im Modus AUTO lässt XP SnowState X-Planes Schnee in Ruhe, solange er stimmt, und korrigiert ihn bei klarer Abweichung. Der Modus REGIONAL geht weiter: Statt eines Werts für die ganze Szene korrigiert er X-Planes regionalen Schnee, und am Boden sowie im Anflug stimmt der Wert am Flugzeug genau. Der Entwickler empfiehlt ihn für Gebirge und Talflughäfen.

!!! warning "Nur ein Plugin darf den Schnee setzen"

    Der Entwickler bittet darum, [xa-snow](xa-snow.md) zu entfernen, das X-Planes eigenen Schnee und XP SnowState stört. [NOAA Weather](noaa_weather.md) schreibt dieselben X-Plane-Datarefs für Schnee und Pistenreibung: dort **Accumulated Snow** und **Adjusted Runway Friction** abschalten oder XP SnowState im Modus BEOBACHTEN betreiben.

## Installation

**Download:** Während der Beta kein öffentlicher Download

XP SnowState ist ein natives Plugin: Der Ordner `XPSnowState` wird nach `Resources/plugins/` kopiert. Beim ersten Start lädt das Plugin einmalig die weltweite Stationsliste (rund 9 MB, einige Minuten). Das Menü **Plugins → XP SnowState Beta** öffnet Fenster und WebUI.

### Linux-Hinweise

Der Linux-Build der Beta hängt nur von der C-Bibliothek ab und benötigt glibc 2.38 oder neuer — vorhanden in Ubuntu 24.04 und Debian 13, nicht aber in Ubuntu 22.04 oder Debian 12. Im Simulator wurde das Plugin für diese Seite nicht getestet; die Beschreibung folgt README und Handbuch des Beta-Pakets.

## Quellen

- [Isar Simworks](https://isarsimworks.de/)
- README und Handbuch des Beta-Pakets XP SnowState 1.0.0
