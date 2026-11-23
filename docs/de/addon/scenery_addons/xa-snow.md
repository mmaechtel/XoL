---
description: "xa-snow legt reale NOAA-Schneehöhen auf die X-Plane-12-Szenerie — eingestellt, seit X-Plane 12.4.4 liegenden Schnee selbst zeichnet; nativer Linux-Build."
---
# xa-snow

xa-snow ist ein eigenständiges [Plugin](../../glossary.md#plugin) von hotbso, das reale Schneebedeckung auf die X-Plane-12-Szenerie legt. Es lädt akkumulierte Schneehöhendaten von NOAA herunter und wendet sie in Echtzeit auf die Simulation an.

!!! warning "Eingestellt"

    Der Entwickler hat xa-snow für überholt erklärt und das Repository archiviert: X-Plane 12.4.4 unterstützt liegenden Schnee nativ. Die letzte Version bleibt verfügbar, weitere Updates gibt es nicht. Ist [XP SnowState](xp_snowstate.md) (Beta) oder die Schneedecke von [NOAA Weather](noaa_weather.md) aktiv, xa-snow entfernen.

## Hintergrund

- **Entwickler:** hotbso (Holger Teutsch), ursprünglich von zodiac1214
- **Repository:** [github.com/hotbso/xa-snow](https://github.com/hotbso/xa-snow) (Open Source, GPL-3.0; libspng-Komponente BSD-2-Clause)
- **Plattformen:** Windows, macOS, Linux (native Binaries)
- **Kompatibilität:** [X-Plane](../../glossary.md#x-plane) 12
- **Status:** Eingestellt, Repository archiviert

Vor X-Plane 12.4.4 ersetzte xa-snow X-Planes einheitlichen regionalen Schnee durch standortspezifische Bedeckung auf Basis tatsächlicher Wetterdaten.

## Funktionsumfang

- **NOAA-Schneedaten:** Lädt 6-Stunden-Vorhersagen der akkumulierten Schneehöhe für die gesamte Erde herunter
- **Räumliche Interpolation:** Überwand vor 12.4.4 X-Planes Beschränkung auf einheitliche regionale Schneebedeckung mit 0,25° Lat/Lon-Auflösung
- **Küstenlinien-Bearbeitung:** Extrapoliert Landschnee zu Küstenlinien, die NOAA-IR-Bilder übersehen, mit optionaler Temperaturkorrektur zum Abschmelzen von ausgedehntem Küstenschnee bei hoher Bodentemperatur
- **Historischer Schnee:** Lädt optional archivierte Schneedaten für ein vergangenes Datum (vor Flugstart) — das Archiv umfasst ungefähr ein Jahr, enthält aber Lücken
- **Auto-Update:** Aktualisiert optional die Schneehöhen-Daten während langer Flüge — ressourcenintensiv und vom Upstream als potenziell instabil eingestuft
- **Pistenreibung:** Einstellbares Pisteneis-Verhalten über die Option „Lock Elsa Up" (reduziert Pistenreibung in X-Plane 12.4.x+)
- **Manuelles Wetter überschreiben:** Erzwingt den Schnee-Download auch bei manuellem Wetter (Standard: überspringt Download, um Sommerszenerie beizubehalten)

**Per-Scenery-Konfiguration**

Legacy-Szeneries (meist aus XP11) zeigen übermäßig Schnee auf Runways und Taxiways. `xa-snow.cfg-sample` aus dem Plugin-Verzeichnis als `xa-snow.cfg` in eine Szenerie kopieren, um die Schneehöhe auf diesem Flughafen zu begrenzen.

## Mehrwert in der Flugsimulation

Vor 12.4.4 wurde X-Planes eingebauter Schnee einheitlich über große Regionen verteilt — entweder war alles bedeckt oder nichts. xa-snow brachte saisonalen Realismus, indem es Schnee dort zeigte, wo er tatsächlich lag: schneebedeckte Alpen neben grünen Tälern, realistische Baumgrenzenübergänge und korrekte küstennahe Schneegrenzen. In Kombination mit Echtzeit-Wetter entstand ein überzeugendes Winterflug-Erlebnis.

## Installation

**Download:** [GitHub Releases](https://github.com/hotbso/xa-snow/releases)

Die ZIP-Datei nach `Resources/plugins/` entpacken. Updates kamen bis zur Archivierung über den [SkunkCrafts Updater](../tools/skunkcrafts_updater.md).

### Linux-Hinweise

Die Linux-Binary linkt gegen `libcurl-gnutls.so.4` für bessere Kompatibilität mit Steam/Proton-Umgebungen. Ab Debian Trixie:

```bash
sudo apt install libcurl3t64-gnutls
```

Weitere Linux-spezifische Probleme sind nicht bekannt.

## Quellen

- [xa-snow — GitHub](https://github.com/hotbso/xa-snow)
- [Accumulated Snow — Threshold Forum](https://forum.thresholdx.net/files/file/3871-accumulated-snow/)
