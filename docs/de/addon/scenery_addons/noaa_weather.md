---
description: "NOAA Weather ergänzt Schneedecke, Pistenreibung wie auf behandelter Piste und ein METAR-Fenster (NOAA, IVAO, VATSIM) in X-Plane 12 unter Linux. Setzt XPPython3 voraus."
---
# NOAA Weather

NOAA Weather ist ein Python-basiertes [Plugin](../../glossary.md#plugin), das X-Plane 12 um Schneedecke, eine Anpassung der Pistenreibung und METAR-Monitoring ergänzt. Es arbeitet neben X-Planes eingebautem Real Weather und ersetzt es nicht.

## Hintergrund

- **Entwickler:** Antonio Golfari (biuti), ursprünglich von Joan Perez i Cauhe
- **Repository:** [github.com/biuti/XplaneNoaaWeather](https://github.com/biuti/XplaneNoaaWeather) (Open Source, GPLv2 oder später)
- **Plattformen:** Windows, macOS, Linux
- **Kompatibilität:** X-Plane 12.4.4 oder neuer (aktuelle Vorabversionen); für X-Plane 12.4.0–12.4.3 das Release NOAA Weather 12.4 verwenden
- **Voraussetzung:** [XPPython3](../scripting/xppython3.md) 4.8.0+ für die aktuellen Vorabversionen, 4.6.0+ für NOAA Weather 12.4

X-Plane 12 baut seine Wetter-Engine bereits auf NOAA-GFS-Daten auf, das Plugin erzeugt deshalb kein eigenes Wetter; nach Angabe des Entwicklers beobachtet es vor allem, was Real Weather tut. Seit X-Plane 12.4.4 enthalten die Real-Weather-Dateien die Schneehöhe, und das Plugin lädt keine GFS-Daten mehr selbst herunter.

## Funktionsumfang

- **Schneedecke:** Liest die Schneehöhe an der Flugzeugposition aus X-Planes Real-Weather-Dateien und setzt daraus die Schneedecke — nach Angabe des Entwicklers wertet X-Plane 12.4.4 diese Daten selbst noch nicht korrekt aus
- **Letzter Schneewert:** Behält den letzten gültigen Schneewert bis zu 70 nm bei, wenn an der Position kein Wert vorliegt, etwa über Wasser
- **Pistenreibung:** X-Plane simuliert keine Pistenbehandlung, bei Vereisung werden Pisten deshalb auch an großen Flughäfen zur Eisfläche. Das Plugin senkt solche Werte auf höchstens „verschneit“
- **METAR-Fenster:** Zeigt das METAR aus X-Planes Real Weather neben einer externen Quelle (NOAA, IVAO oder VATSIM) für einen beliebigen Flughafen an
- **Wetter-Infofenster:** Zeigt die aktuellen Real-Weather-Werte an der Flugzeugposition: Wind, Sicht, Temperatur, Druck und Pistenreibung

## Einstellungen

Die Einstellungen liegen im Menü **Plugins → XP NOAA Weather → Configuration**. Nur zwei davon verändern den Simulator; die METAR-Einstellungen betreffen allein die Anzeige.

| Einstellung | Standard | Wirkung |
|---|---|---|
| Accumulated Snow | an | Setzt die Schneedecke für die gesamte sichtbare Szene |
| Adjusted Runway Friction | an | Verringert die Glätte wie auf einer behandelten Piste |
| METAR Source | NOAA | Quelle im METAR-Fenster: NOAA, IVAO oder VATSIM |
| METAR Decoding | aus | Ergänzt das rohe METAR um Klartext |

!!! tip "Online-Flüge"

    Auf VATSIM oder IVAO arbeiten Lotsen und ATIS mit dem METAR des Netzwerks, das von X-Planes Real Weather abweichen kann. Die METAR-Quelle auf das Netzwerk stellen, um diese Meldung zu sehen; das Wetter im Simulator kommt weiterhin aus Real Weather.

## Grenzen der Schneedecke

Das Plugin setzt einen einzigen Schneewert für die gesamte sichtbare Szene, entnommen aus der GFS-Gitterzelle an der Flugzeugposition. Diese Zelle ist rund 28 km breit und mittelt Tal und Gipfel. Berge und Täler zeigen deshalb gleich viel Schnee, und im Gebirge passt der Wert zu keinem von beiden. [XP SnowState](xp_snowstate.md) (Beta) korrigiert den Schnee mit Daten, die die Geländehöhe berücksichtigen.

!!! warning "Nur ein Plugin darf den Schnee setzen"

    NOAA Weather und XP SnowState schreiben dieselben X-Plane-Datarefs für Schnee und Pistenreibung. Sind beide aktiv, in NOAA Weather **Accumulated Snow** abschalten. Für die Pistenreibung gibt es zwei Wege: **Adjusted Runway Friction** ebenfalls abschalten oder in XP SnowState **Bahnzustand setzen** auf „aus“ stellen und die Reibung NOAA Weather überlassen. Das METAR-Fenster arbeitet in beiden Fällen weiter.

## Mehrwert in der Flugsimulation

X-Planes eigene Schneedarstellung ist noch nicht verlässlich. NOAA Weather setzt die Schneehöhe aus Real Weather als Schneedecke um das Flugzeug, verringert die Pistenglätte bei Vereisung und ergänzt einen METAR-Vergleich. Kommerzielle Wetter-Engines wie Active Sky oder xEnviro laufen nicht unter Linux; NOAA Weather ersetzt sie nicht. Thematisch verwandt ist [AutoHaze](../flylua_scripts/autohaze.md), das den atmosphärischen Dunst aus gemessenen Aerosoldaten neu berechnet.

## Installation

**Download:** [GitHub Releases](https://github.com/biuti/XplaneNoaaWeather/releases)

[XPPython3](../scripting/xppython3.md) muss bereits installiert sein. Unter X-Plane 12.4.4 oder neuer das neueste als *Pre-release* markierte Release wählen. Es besteht aus einem einzigen Ordner, der nach `Resources/plugins/PythonPlugins/` kopiert wird:

```
Resources/plugins/PythonPlugins/
└── PI_NOAAWeather/
    ├── PI_NOAAWeather.py
    ├── bin/
    ├── scripts/
    └── version.txt
```

Vor der Installation eine eventuell vorhandene ältere Version vollständig löschen (nicht überschreiben) — insbesondere den alten Aufbau mit `PI_noaaWeather.py` und dem Ordner `noaaweather/`. [XOrganizer](../tools/xorganizer.md) listet nur `PI_*.py`-Dateien direkt in `PythonPlugins/` und zeigt das Plugin nicht an; es wird trotzdem geladen.

### Linux-Hinweise

Das Plugin enthält eine vorkompilierte `linux-wgrib2`-Binary (erstellt auf Ubuntu 20.04 LTS) zum Lesen der Real-Weather-GRIB2-Dateien. Diese ist mit den meisten aktuellen Distributionen kompatibel. Läuft sie auf einem System nicht, lässt sich `bin/linux-wgrib2` im Plugin-Ordner durch ein selbst kompiliertes wgrib2 ersetzen.

Weitere Linux-spezifische Probleme sind nicht bekannt.

## Quellen

- [NOAA Weather — GitHub](https://github.com/biuti/XplaneNoaaWeather)
- [NOAA Weather — X-Plane.org Forum](https://forums.x-plane.org/forums/topic/72313-noaa-weather-plugin/)
- [XPPython3 — Dokumentation](https://xppython3.readthedocs.io/en/latest/index.html)
