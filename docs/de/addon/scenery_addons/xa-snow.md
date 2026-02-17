# xa-snow

xa-snow ist ein eigenständiges [Plugin](../../glossary.md#plugin) von hotbso, das reale Schneebedeckung auf die X-Plane-12-Szenerie legt. Es lädt akkumulierte Schneehöhendaten von NOAA herunter und wendet sie in Echtzeit auf die Simulation an.

## Hintergrund

- **Entwickler:** hotbso (Holger Teutsch), ursprünglich von zodiac1214
- **Repository:** [github.com/hotbso/xa-snow](https://github.com/hotbso/xa-snow) (Open Source, LGPL-2.1)
- **Plattformen:** Windows, macOS, Linux (native Binaries)
- **Kompatibilität:** [X-Plane](../../glossary.md#x-plane) 12

xa-snow ersetzt X-Planes einheitlichen regionalen Schnee durch standortspezifische Bedeckung auf Basis tatsächlicher Wetterdaten. Das Plugin wird aktiv gepflegt und regelmäßig aktualisiert.

## Funktionsumfang

- **NOAA-Schneedaten:** Lädt 6-Stunden-Vorhersagen der akkumulierten Schneehöhe für die gesamte Erde herunter
- **Räumliche Interpolation:** Überwindet X-Planes Beschränkung auf einheitliche regionale Schneebedeckung mit 0,25° Lat/Lon-Auflösung
- **Historischer Schnee:** Zugriff auf archivierte Schneedaten für bestimmte Daten (365-Tage-Archiv)
- **Auto-Update:** Aktualisiert die Schneebedeckung optional während des Fluges beim Wechsel zwischen Regionen
- **Pistenreibung:** Einstellbares Pisteneis-Verhalten über die Option „Lock Elsa Up" (reduziert Pistenreibung in X-Plane 12.4.x+)
- **Manuelles Wetter überschreiben:** Erzwingt den Schnee-Download auch bei manuellem Wetter (Standard: überspringt Download, um Sommerszenerie beizubehalten)

**Per-Scenery-Konfiguration**

Szenerie-Entwickler können `xa-snow.cfg`-Dateien einbinden, um das Schneeverhalten für bestimmte Flughäfen oder Regionen anzupassen.

## Mehrwert in der Flugsimulation

X-Planes eingebauter Schnee wird einheitlich über große Regionen verteilt — entweder ist alles bedeckt oder nichts. xa-snow bringt saisonalen Realismus, indem es Schnee dort zeigt, wo er tatsächlich liegt: schneebedeckte Alpen neben grünen Tälern, realistische Baumgrenzenübergänge und korrekte küstennahe Schneegrenzen. In Kombination mit Echtzeit-Wetter entsteht ein überzeugendes Winterflug-Erlebnis.

## Installation

**Download:** [GitHub Releases](https://github.com/hotbso/xa-snow/releases)

Die ZIP-Datei nach `Resources/plugins/` entpacken. Nach der Erstinstallation übernimmt der [SkunkCrafts Updater](../tools/skunkcrafts_updater.md) automatische Updates (PROD- oder BETA-Kanal).

### Linux-Hinweise

Seit v2.3.1 linkt die Linux-Binary gegen `libcurl4-gnutls` für bessere Kompatibilität mit Steam/Proton-Umgebungen. Auf Debian-basierten Systemen:

```bash
sudo apt install libcurl4-gnutls-dev
```

Weitere Linux-spezifische Probleme sind nicht bekannt.

## Quellen

- [xa-snow — GitHub](https://github.com/hotbso/xa-snow)
- [Accumulated Snow — Threshold Forum](https://forum.thresholdx.net/files/file/3871-accumulated-snow/)
