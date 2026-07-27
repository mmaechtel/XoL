---
description: "NOAA-Weather-Plugin ergänzt reale Schneeabdeckung und METAR-Vergleich in X-Plane 12 unter Linux. Setzt XPPython3 voraus, inkl. wgrib2-Binary."
---
# NOAA Weather

NOAA Weather ist ein Python-basiertes [Plugin](../../glossary.md#plugin), das X-Plane 12 um reale Schneebedeckung und METAR-Monitoring ergänzt. Es lädt Wetterdaten von NOAA (National Oceanic and Atmospheric Administration) herunter und gleicht sie mit X-Planes eingebautem Real Weather ab.

## Hintergrund

- **Entwickler:** Antonio Golfari (biuti), ursprünglich von Joan Perez i Cauhe
- **Repository:** [github.com/biuti/XplaneNoaaWeather](https://github.com/biuti/XplaneNoaaWeather) (Open Source, GPLv2 oder später)
- **Plattformen:** Windows, macOS, Linux
- **Kompatibilität:** X-Plane 12.4+
- **Voraussetzung:** [XPPython3](../scripting/xppython3.md) 4.6.0+

Da X-Plane 12 seine eigene Wettererzeugung auf NOAA-GFS-Daten aufbaut, arbeitet das Plugin nicht als vollständiger Wetterersatz, sondern als Ergänzung — primär für Schneedarstellung und Wetter-Monitoring. Das Plugin wird aktiv gepflegt und regelmäßig aktualisiert.

## Funktionsumfang

- **Schneebedeckung:** Lädt NOAA-GFS-Schneehöhen- und Niederschlagsdaten herunter und erzeugt standortspezifischen Schnee, den X-Plane 12 nativ nicht korrekt darstellen kann
- **Schneewert-Wiederverwendung:** Nutzt den letzten gültigen Schneewert in einem Radius von 70 nm erneut, wenn GFS-Daten nicht verfügbar sind
- **METAR-Vergleich:** Zeigt X-Plane-12-Real-Weather-METAR neben externen Quellen (NOAA, IVAO, VATSIM) in einem eigenen Fenster an
- **Pistenreibung:** Simuliert Pistenbehandlung bei kaltem Wetter für realistischeres Bremsverhalten (ab X-Plane 12.4+)
- **Real-Weather-Monitoring:** Überwacht und visualisiert in Echtzeit, was X-Planes interne Wetter-Engine tatsächlich erzeugt

## Mehrwert in der Flugsimulation

X-Plane 12 bezieht seine Wetterdaten zwar bereits von NOAA, kann Schneebedeckung aber nicht standortgenau darstellen. NOAA Weather schließt diese Lücke mit echten GFS-Schneehöhendaten und bietet zusätzlich einen METAR-Vergleich, der besonders für Online-Flüge auf IVAO oder VATSIM hilfreich ist. Da kommerzielle Wetter-Alternativen wie Active Sky oder xEnviro kein Linux unterstützen, ist NOAA Weather eine der wenigen Optionen für Linux-Nutzer.

## Installation

**Download:** [GitHub Releases](https://github.com/biuti/XplaneNoaaWeather/releases)

[XPPython3](../scripting/xppython3.md) muss bereits installiert sein. Vor der Installation eine eventuell vorhandene ältere Version vollständig löschen (nicht überschreiben). Die ZIP-Datei nach `Resources/plugins/PythonPlugins/` entpacken:

```
Resources/plugins/PythonPlugins/
├── PI_noaaWeather.py
└── noaaweather/
```

### Linux-Hinweise

Das Plugin enthält eine vorkompilierte `linux-wgrib2`-Binary (erstellt auf Ubuntu 20.04 LTS) zum Dekodieren der GFS-GRIB2-Dateien. Diese ist mit den meisten aktuellen Distributionen kompatibel. Falls die mitgelieferte Binary nicht funktioniert, lässt sich wgrib2 aus dem Quellcode kompilieren.

Weitere Linux-spezifische Probleme sind nicht bekannt.

## Quellen

- [NOAA Weather — GitHub](https://github.com/biuti/XplaneNoaaWeather)
- [NOAA Weather — X-Plane.org Forum](https://forums.x-plane.org/forums/topic/72313-noaa-weather-plugin/)
- [XPPython3 — Dokumentation](https://xppython3.readthedocs.io/en/latest/index.html)
