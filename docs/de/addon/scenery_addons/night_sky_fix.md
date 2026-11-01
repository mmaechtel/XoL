---
description: "Night Sky Fix für X-Plane 12 — Sternkataloge mit bis zu 900.000 Sternen für eine sichtbare Milchstraße, dazu ein FlyWithLua-Skript für realistische Sternhelligkeit."
---
# Night Sky Fix

Night Sky Fix ersetzt den Sternkatalog von [X-Plane](../../glossary.md#x-plane) 12 durch einen deutlich dichteren und ergänzt ein optionales FlyWithLua-Skript, das die Darstellung der Sterne korrigiert. Die Standard-`earth_astro.dat` enthält rund 8.500 Sterne bis Magnitude 6,5 — die Grenze des bloßen Auges. Schwächere Sterne sind einzeln nicht auflösbar, ihr gemeinsames Licht ist aber als Schleier sichtbar; ohne sie zeigt der Himmel leere Flecken. Die Kataloge des Mods reichen bis Magnitude 11, mit der größten Variante wird die Milchstraße sichtbar.

## Hintergrund

- **Entwickler:** lucas1999
- **Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/100904-night-sky-fix/)
- **Plattformen:** Keine Plattformeinschränkung — das Paket enthält eine Datendatei und ein Lua-Skript, keine Binary
- **Kompatibilität:** X-Plane 12
- **Optional:** [FlyWithLua NG+](../scripting/flywithlua.md) für das Skript
- **Lizenz:** Freeware, Weitergabe nicht gestattet

## Funktionsumfang

- **Sternkatalog-Varianten:** Sechs `earth_astro.dat`-Varianten, von 9.000 Sternen (Magnitude 6,5) bis 900.000 (Magnitude 11):

| Sterne | Grenzmagnitude |
|---|---|
| 9.000 | 6,5 |
| 16.000 | 7,0 |
| 45.000 | 8,0 |
| 120.000 | 9,0 |
| 300.000 | 10,0 |
| 900.000 | 11,0 |

- **Dunkles Band und Horizont:** Das Skript entfernt das dunkle Band, das Sterne verdeckt (vor allem den Polarstern), und korrigiert die atmosphärische Extinktion — die Sternhelligkeit nimmt jetzt zum Horizont hin ab, wo Sterne zuvor selbst in der Dämmerung sichtbar blieben
- **Sternbilder:** Das Skript passt den photometrischen Gain an, sodass helle Sterne hervortreten und Sternbilder erkennbar werden
- **Höhenabhängiger Gain:** Mit dem Skript sind am Boden nur die Hauptsternbilder zu sehen; je höher das Flugzeug steigt, desto mehr schwache Sterne erscheinen
- **Mond:** Das Skript hebt die Oberflächenhelligkeit des Mondes auf realistischere 2.500 Nits an

## Mehrwert in der Flugsimulation

Nachts zeichnet das Standard-X-Plane einen Himmel, in dem alle Sterne ungefähr gleich aussehen und Teile des Himmels leer bleiben. Die dichteren Kataloge füllen die leeren Flecken; sichtbar wird die Milchstraße mit der Variante von 900.000 Sternen. Das optionale Skript macht Sternbilder erkennbar, hält den Blick vom Vorfeld zurückhaltend und lässt mit zunehmender Höhe schwächere Sterne erscheinen. Der Aufwand beschränkt sich auf das Ersetzen einer Datendatei und optional ein kurzes Skript.

## Installation

**Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/100904-night-sky-fix/)

1. Den originalen Sternkatalog sichern und die gewählte Variante darüber kopieren — der Ordnername `default data` enthält ein Leerzeichen und muss gequotet werden (Pfad an die X-Plane-Installation anpassen):

    ```bash
    cd "/pfad/zu/X-Plane 12/Resources/default data" &&
    cp earth_astro.dat earth_astro.dat.orig &&
    cp /pfad/zur/gewaehlten/earth_astro.dat .
    ```

2. Optional, aber empfohlen: das Lua-Skript nach `Resources/plugins/FlyWithLua/Scripts/` kopieren.

Ohne Sicherung stellt der X-Plane-Installer die Standarddatei wieder her: Ein Update bietet an, die geänderte Datei zu überschreiben.

!!! warning "Nebenwirkung des Skripts"

    Das Skript setzt das private Dataref `sim/private/controls/dome/per_view` auf `1`. Das entfernt das dunkle Band, die Bodenbeleuchtung kann sich beim Vor- und Zurückstellen der Zeit aber verzögert aktualisieren. Wird die Zeile im Skript auskommentiert (`--`), entfällt die Verzögerung, und das Band kehrt zurück. Der zweite geänderte Wert, `sim/private/controls/stars/gain_photometric` (Standard 20), variiert je nach Höhe zwischen 1 und 30 und lässt sich im Skript an Geschmack und Monitor anpassen.

## Quellen

- [Night Sky Fix — forums.x-plane.org](https://forums.x-plane.org/files/file/100904-night-sky-fix/)
