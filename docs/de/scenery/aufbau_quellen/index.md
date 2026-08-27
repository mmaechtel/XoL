---
title: Aufbau und Quellen der X-Plane-Szenerie
description: "Aufbau der X-Plane-Szenerie: Mesh, Orthophotos, Autogen-Ebenen, Ladereihenfolge der scenery_packs.ini und verfügbare Quellen."
---
# Aufbau & Quellen

X-Planes Szenerie besteht aus drei Schichten: das Mesh definiert die Geländeform, Orthofotos projizieren Satellitenbilder als Bodentexturen, und Autogen bevölkert die Landschaft mit 3D-Objekten. Flughäfen liegen als eigene Prioritätsebene obenauf. Jedes Szeneriepaket gehört zu einer dieser Ebenen, und die `scenery_packs.ini` entscheidet, welches Paket sich bei Überlappung durchsetzt: höher gelistete Einträge haben Vorrang. Schwebende Flughäfen, unsichtbare Szenerie oder Autogen-Objekte auf Landebahnen deuten meist auf eine falsche Reihenfolge hin, nicht auf ein defektes Paket.

Einstieg ist [Komponenten](scenery_components.md) mit dem Schichtenmodell, den Regeln der Ladereihenfolge und einem ausgearbeiteten `scenery_packs.ini`-Beispiel. [Quellen](scenery_sources.md) gibt danach einen Überblick, woher Szenerie kommt: Standard-Szenerie mit Gateway-Airports, SimHeaven X-World für dichteres Autogen, Freeware und Payware sowie interaktive Weltkarten zur Abdeckungsprüfung. Die Sektionen [Orthofotografie](../orthophotography/index.md) und [Ortho Streaming](../ortho_streaming/index.md) bauen auf dieser Grundlage auf.

- **[Komponenten](scenery_components.md)** — Ladereihenfolge und scenery_packs.ini
- **[Quellen](scenery_sources.md)** — Übersicht der verfügbaren Szenerien-Optionen
