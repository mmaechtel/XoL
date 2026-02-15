# TerrainRadar

TerrainRadar ist ein natives [Plugin](../glossary.md#plugin), das ein EGPWS-Terrain-Display (Enhanced Ground Proximity Warning System) und ein vertikales Situationsdisplay (VSD) in X-Plane darstellt. Die Geländedarstellung ist farbcodiert relativ zur aktuellen Flughöhe: Schwarz (>1.000 ft darunter), Gelb (<1.000 ft), Rot (<100 ft — Kollisionsgefahr).

## Hintergrund

- **Entwickler:** Denis Antontsev (DrGluck) und Sergey Popovichev (Vanger)
- **Download:** [X-Plane.org](https://forums.x-plane.org/files/file/37864-terrain-radar-vertical-situation-display/)
- **Plattformen:** Windows, macOS, Linux (native Binaries)
- **Kompatibilität:** X-Plane 12

Das Plugin arbeitet in zwei Modi: Bei unterstützten Flugzeugen integriert es sich direkt in das Navigation Display (TERR-Taste), bei allen anderen Flugzeugen steht ein frei positionierbares Overlay-Fenster zur Verfügung.

## Funktionsumfang

- **Terrain-Display:** Farbcodierte Geländedarstellung auf dem ND oder als Overlay-Fenster
- **Vertical Situation Display (VSD):** Geländeprofil im Vertikalschnitt entlang der Flugroute
- **Peaks-Modus:** Zeigt Geländespitzen auch in Reiseflughöhe weiter an
- **EGPWS-Warnungen:** Vorhersage und Warnung bei drohender Geländekollision
- **Overlay-Fenster:** Abkoppelbar, skalierbar, auf zweiten Monitor verschiebbar
- **Breite Flugzeugunterstützung:** Integrierter ND-Modus für Zibo 737, FlightFactor 777, ToLiss-kompatible Flugzeuge, iniSimulations A300/A310 u.v.m.

## Mehrwert in der Flugsimulation

Geländewarnung ist besonders bei Anflügen in bergigem Gelände und bei schlechter Sicht sicherheitskritisch. TerrainRadar liefert die visuelle Geländedarstellung, die in echten Verkehrsflugzeugen zum Standard gehört. Dank des universellen Overlay-Modus funktioniert es auch mit Flugzeugen, die kein integriertes Terrain-Display mitbringen.

!!! note "X-Plane 12.3+"

    X-Plane 12.3 führte native Terrain-Anzeige auf den X1000-Avionik-Instrumenten ein. TerrainRadar bietet weiterhin Mehrwert durch breitere Flugzeugunterstützung, das VSD-Feature und den universellen Overlay-Modus.

## Installation

**Download:** [X-Plane.org](https://forums.x-plane.org/files/file/37864-terrain-radar-vertical-situation-display/)

Den Ordner `TerrainRadar` nach `Resources/plugins/` entpacken.

## Quellen

- [TerrainRadar — X-Plane.org](https://forums.x-plane.org/files/file/37864-terrain-radar-vertical-situation-display/)
- [TerrainRadar Plugin Review — X-PlaneReviews](https://xplanereviews.com/forums/topic/669-plugin-review-terrainradar-by-drgluck/)
