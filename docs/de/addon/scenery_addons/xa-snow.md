---
description: "xa-snow legt reale NOAA-Schneehöhen auf die X-Plane-12-Szenerie — eingestellt, seit X-Plane 12.4.4 liegenden Schnee selbst zeichnet; nativer Linux-Build."
---
# xa-snow

xa-snow ist ein eigenständiges [Plugin](../../glossary.md#plugin) von hotbso, das die Schneedecke von X-Plane 12 aus realen NOAA-Schneehöhen setzt. Es lädt akkumulierte Schneehöhendaten von NOAA herunter und wendet sie in Echtzeit auf die Simulation an.

!!! warning "Eingestellt"

    Der Entwickler hat xa-snow für überholt erklärt und das Repository archiviert: X-Plane 12.4.4 unterstützt liegenden Schnee nativ. Die letzte Version bleibt verfügbar, weitere Updates gibt es nicht. Laminar Research bittet darum, xa-snow vor dem Einsatz von X-Plane 12.4.4 zu entfernen, weil es X-Planes globale Schneeparameter überschreibt. Der Entwickler von [XP SnowState](xp_snowstate.md) (Beta) bittet um dasselbe.

## Hintergrund

- **Entwickler:** hotbso (Holger Teutsch), ursprünglich von zodiac1214
- **Repository:** [github.com/hotbso/xa-snow](https://github.com/hotbso/xa-snow) (Open Source, GPL-3.0; libspng-Komponente BSD-2-Clause)
- **Plattformen:** Windows, macOS, Linux (native Binaries)
- **Kompatibilität:** [X-Plane](../../glossary.md#x-plane) 12
- **Status:** Eingestellt, Repository archiviert

Vor X-Plane 12.4.4 setzte xa-snow X-Planes Schneedecke aus der NOAA-Schneehöhe an der Flugzeugposition.

## Funktionsumfang

- **NOAA-Schneedaten:** Lädt 6-Stunden-Vorhersagen der akkumulierten Schneehöhe für die gesamte Erde herunter
- **Interpolation:** Versucht, Wechsel der Schneehöhe zeitlich und räumlich zwischen den NOAA-Gitterpunkten (0,25° Lat/Lon) zu glätten
- **Küstenlinien-Bearbeitung:** Extrapoliert Landschnee zu Küstenlinien, die NOAA-IR-Bilder übersehen, mit optionaler Temperaturkorrektur zum Abschmelzen von ausgedehntem Küstenschnee bei hoher Bodentemperatur
- **Historischer Schnee:** Versucht optional, archivierte Schneedaten für ein vergangenes Datum samt Uhrzeit zu laden, das vor Flugstart eingestellt wird — das Archiv umfasst ungefähr ein Jahr, enthält aber Lücken
- **Auto-Update:** Aktualisiert optional die Schneehöhen-Daten während langer Flüge — ressourcenintensiv und vom Upstream als potenziell instabil eingestuft
- **Pisteneis:** Die Option „Lock Elsa Up“ verringert Eis auf Pisten und Rollwegen; unter X-Plane 12.4.x begrenzt sie außerdem die Pistenreibung auf die Stufe „Pfützen“
- **Manuelles Wetter überschreiben:** Erzwingt den Schnee-Download auch bei manuellem Wetter (Standard: überspringt Download, um Sommerszenerie beizubehalten)

**Per-Scenery-Konfiguration**

Legacy-Szeneries (meist aus XP11) zeigen übermäßig Schnee auf Runways und Taxiways. `xa-snow.cfg-sample` aus dem Plugin-Verzeichnis als `xa-snow.cfg` in eine Szenerie kopieren, um die Schneehöhe auf diesem Flughafen zu begrenzen.

## Mehrwert in der Flugsimulation

Vor 12.4.4 zeigte X-Plane überall in der Szene dieselbe Schneedecke. xa-snow koppelte sie an die NOAA-Schneehöhe unter dem Flugzeug. Weil die ganze Szene diesen einen Wert zeigte, konnte Schnee trotz Glättung plötzlich erscheinen oder verschwinden, etwa beim Überflug eines einzelnen verschneiten Gipfels.

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
- [X-Plane 12.4.4 Release Notes — Laminar Research](https://www.x-plane.com/kb/x-plane-12-4-4-release-notes/)
- [Accumulated Snow — Threshold Forum](https://forum.thresholdx.net/files/file/3871-accumulated-snow/)
