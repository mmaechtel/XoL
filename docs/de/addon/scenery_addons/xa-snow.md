---
description: "xa-snow überlagert reale NOAA-Schneetiefen-Daten auf X-Plane-12-Szenerie und ersetzt einheitlichen Regionalschnee durch standortgenaue Abdeckung."
---
# xa-snow

xa-snow ist ein eigenständiges [Plugin](../../glossary.md#plugin) von hotbso, das reale Schneebedeckung auf die X-Plane-12-Szenerie legt. Es lädt akkumulierte Schneehöhendaten von NOAA herunter und wendet sie in Echtzeit auf die Simulation an.

## Hintergrund

- **Entwickler:** hotbso (Holger Teutsch), ursprünglich von zodiac1214
- **Repository:** [github.com/hotbso/xa-snow](https://github.com/hotbso/xa-snow) (Open Source, GPL-3.0; libspng-Komponente BSD-2-Clause)
- **Plattformen:** Windows, macOS, Linux (native Binaries)
- **Kompatibilität:** [X-Plane](../../glossary.md#x-plane) 12

xa-snow ersetzt X-Planes einheitlichen regionalen Schnee durch standortspezifische Bedeckung auf Basis tatsächlicher Wetterdaten. Das Plugin wird aktiv gepflegt und regelmäßig aktualisiert.

## Funktionsumfang

- **NOAA-Schneedaten:** Lädt 6-Stunden-Vorhersagen der akkumulierten Schneehöhe für die gesamte Erde herunter
- **Räumliche Interpolation:** Überwindet X-Planes Beschränkung auf einheitliche regionale Schneebedeckung mit 0,25° Lat/Lon-Auflösung
- **Küstenlinien-Bearbeitung:** Extrapoliert Landschnee zu Küstenlinien, die NOAA-IR-Bilder übersehen, mit optionaler Temperaturkorrektur zum Abschmelzen von ausgedehntem Küstenschnee bei hoher Bodentemperatur
- **Historischer Schnee:** Lädt optional archivierte Schneedaten für ein vergangenes Datum (vor Flugstart) — das Archiv umfasst ungefähr ein Jahr, enthält aber Lücken
- **Auto-Update:** Aktualisiert optional die Schneehöhen-Daten während langer Flüge — ressourcenintensiv und vom Upstream als potenziell instabil eingestuft
- **Pistenreibung:** Einstellbares Pisteneis-Verhalten über die Option „Lock Elsa Up" (reduziert Pistenreibung in X-Plane 12.4.x+)
- **Manuelles Wetter überschreiben:** Erzwingt den Schnee-Download auch bei manuellem Wetter (Standard: überspringt Download, um Sommerszenerie beizubehalten)

**Per-Scenery-Konfiguration**

Legacy-Szeneries (meist aus XP11) zeigen übermäßig Schnee auf Runways und Taxiways. `xa-snow.cfg-sample` aus dem Plugin-Verzeichnis als `xa-snow.cfg` in eine Szenerie kopieren, um die Schneehöhe auf diesem Flughafen zu begrenzen.

## Mehrwert in der Flugsimulation

X-Planes eingebauter Schnee wird einheitlich über große Regionen verteilt — entweder ist alles bedeckt oder nichts. xa-snow bringt saisonalen Realismus, indem es Schnee dort zeigt, wo er tatsächlich liegt: schneebedeckte Alpen neben grünen Tälern, realistische Baumgrenzenübergänge und korrekte küstennahe Schneegrenzen. In Kombination mit Echtzeit-Wetter entsteht ein überzeugendes Winterflug-Erlebnis.

## Installation

**Download:** [GitHub Releases](https://github.com/hotbso/xa-snow/releases)

Die ZIP-Datei nach `Resources/plugins/` entpacken. Nach der Erstinstallation übernimmt der [SkunkCrafts Updater](../tools/skunkcrafts_updater.md) automatische Updates (PROD- oder BETA-Kanal).

### Linux-Hinweise

Die Linux-Binary linkt gegen `libcurl-gnutls.so.4` für bessere Kompatibilität mit Steam/Proton-Umgebungen. Auf Debian trixie und später:

```bash
sudo apt install libcurl3t64-gnutls
```

Weitere Linux-spezifische Probleme sind nicht bekannt.

## Quellen

- [xa-snow — GitHub](https://github.com/hotbso/xa-snow)
- [Accumulated Snow — Threshold Forum](https://forum.thresholdx.net/files/file/3871-accumulated-snow/)
