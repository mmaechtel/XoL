---
description: "NOAA Weather ergänzt Schneedecke, Pistenreibung wie auf behandelter Piste und ein METAR-Fenster (NOAA, IVAO, VATSIM) in X-Plane 12 unter Linux. Setzt XPPython3 voraus."
---
# NOAA Weather

NOAA Weather ist ein Python-basiertes [Plugin](../../glossary.md#plugin), das X-Plane 12 um Schneedecke, eine Anpassung der Pistenreibung und METAR-Monitoring ergänzt. Es arbeitet neben X-Planes eingebautem Real Weather und ersetzt es nicht.

## Hintergrund

- **Entwickler:** Antonio Golfari (biuti), ursprünglich von Joan Perez i Cauhe
- **Repository:** [github.com/biuti/XplaneNoaaWeather](https://github.com/biuti/XplaneNoaaWeather) (Open Source, GPLv2 oder später)
- **Plattformen:** Windows, macOS, Linux
- **Kompatibilität:** X-Plane 12.4.4+ für die aktuellen Vorabversionen; für X-Plane 12.4 vor 12.4.4 bleibt NOAA Weather 12.4
- **Voraussetzung:** [XPPython3](../scripting/xppython3.md) 4.8.0+ für die aktuellen Vorabversionen, 4.6.0+ für NOAA Weather 12.4

Da X-Plane 12 seine eigene Wettererzeugung auf NOAA-GFS-Daten aufbaut, arbeitet das Plugin nicht als Wetterersatz — nach Angabe des Entwicklers beobachtet es vor allem, was Real Weather tut. Seit X-Plane 12.4.4 enthalten die Real-Weather-Dateien die Schneehöhe, das Plugin lädt deshalb keine GFS-Daten mehr selbst herunter. Das Plugin wird aktiv gepflegt.

## Funktionsumfang

- **Schneedecke:** Liest die Schneehöhe an der Flugzeugposition aus X-Planes Real-Weather-Dateien und setzt daraus die Schneedecke — nach Angabe des Entwicklers wertet X-Plane 12.4.4 diese Daten selbst noch nicht korrekt aus
- **Schneewert-Wiederverwendung:** Nutzt den letzten gültigen Schneewert in einem Radius von 70 nm erneut, wenn an der Position kein Wert vorliegt, etwa über Wasser
- **Pistenreibung:** Simuliert Pistenbehandlung bei kaltem Wetter, indem die Glätte verringert wird, die X-Plane aus Vereisungsbedingungen ableitet
- **METAR-Fenster:** Zeigt das X-Plane-12-Real-Weather-METAR neben einer externen Quelle (NOAA, IVAO oder VATSIM) für einen beliebigen Flughafen an
- **Real-Weather-Monitoring:** Zeigt in Echtzeit, was X-Planes interne Wetter-Engine tatsächlich erzeugt

## Einstellungen

Die Einstellungen liegen im Menü **Plugins → XP NOAA Weather → Configuration**. Nur zwei davon verändern den Simulator; die METAR-Einstellungen betreffen allein die Anzeige.

| Einstellung | Standard | Wirkung |
|---|---|---|
| Accumulated Snow | an | Setzt die Schneedecke für die gesamte sichtbare Szene |
| Adjusted Runway Friction | an | Senkt den Reibwert der Piste wie auf behandelter Piste |
| METAR Source | NOAA | Quelle im METAR-Fenster: NOAA, IVAO oder VATSIM |
| METAR Decoding | aus | Ergänzt das rohe METAR um Klartext |

!!! tip "Online-Flüge"
    Für Flüge auf VATSIM oder IVAO die METAR-Quelle auf das Netzwerk stellen. Das Fenster zeigt dann die Meldung, mit der die Lotsen arbeiten; das Wetter im Simulator kommt weiterhin aus X-Planes Real Weather. Der Entwickler weist darauf hin, dass Real Weather von dem abweichen kann, was ATC, ATIS und andere Piloten sehen.

## Grenzen der Schneedecke

Das Plugin setzt einen einzigen Schneewert für die gesamte sichtbare Szene, entnommen aus der GFS-Gitterzelle an der Flugzeugposition. Eine solche Zelle ist rund 28 km breit und mittelt Tal und Gipfel, Berge und Täler zeigen deshalb immer gleich viel Schnee. [XP SnowState](xp_snowstate.md) setzt für diesen Fall auf höhenabhängige Daten.

!!! warning "Nur ein Plugin darf den Schnee setzen"
    NOAA Weather und XP SnowState schreiben dieselben X-Plane-Regler für Schnee und Pistenreibung. Sind beide aktiv, in NOAA Weather **Accumulated Snow** und **Adjusted Runway Friction** abschalten; das METAR-Fenster arbeitet weiter.

## Mehrwert in der Flugsimulation

X-Plane 12 bezieht sein Wetter von NOAA und liefert seit 12.4.4 die Schneehöhe mit Real Weather aus, die Darstellung ist aber noch nicht verlässlich. NOAA Weather macht aus diesen Daten eine stimmige Schneedecke, entschärft die Pistenreibung und bietet zusätzlich einen METAR-Vergleich, der besonders für Online-Flüge auf IVAO oder VATSIM hilfreich ist. Da kommerzielle Wetter-Alternativen wie Active Sky oder xEnviro kein Linux unterstützen, ist NOAA Weather eine der wenigen Optionen für Linux-Nutzer. Thematisch verwandt ist [AutoHaze](../flylua_scripts/autohaze.md), das den atmosphärischen Dunst aus gemessenen Aerosoldaten neu berechnet.

## Installation

**Download:** [GitHub Releases](https://github.com/biuti/XplaneNoaaWeather/releases)

[XPPython3](../scripting/xppython3.md) muss bereits installiert sein. Die aktuellen Vorabversionen bestehen aus einem einzigen Ordner, der nach `Resources/plugins/PythonPlugins/` kopiert wird:

```
Resources/plugins/PythonPlugins/
└── PI_NOAAWeather/
    ├── PI_NOAAWeather.py
    ├── bin/
    ├── scripts/
    └── version.txt
```

Vor der Installation eine eventuell vorhandene ältere Version vollständig löschen (nicht überschreiben) — insbesondere den alten Aufbau mit `PI_noaaWeather.py` und dem Ordner `noaaweather/`.

### Linux-Hinweise

Das Plugin enthält eine vorkompilierte `linux-wgrib2`-Binary (erstellt auf Ubuntu 20.04 LTS) zum Dekodieren der GRIB2-Dateien. Diese ist mit den meisten aktuellen Distributionen kompatibel. Falls die mitgelieferte Binary nicht funktioniert, lässt sich wgrib2 aus dem Quellcode kompilieren.

XPPython3 lädt Plugins, die als Ordner verpackt sind, erst ab Version 4.8.0. [XOrganizer](../tools/xorganizer.md) listet nur `PI_*.py`-Dateien direkt in `PythonPlugins/` und zeigt das Plugin deshalb nicht an.

## Quellen

- [NOAA Weather — GitHub](https://github.com/biuti/XplaneNoaaWeather)
- [NOAA Weather — X-Plane.org Forum](https://forums.x-plane.org/forums/topic/72313-noaa-weather-plugin/)
- [XPPython3 — Dokumentation](https://xppython3.readthedocs.io/en/latest/index.html)
