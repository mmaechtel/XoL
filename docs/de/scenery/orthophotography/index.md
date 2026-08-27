---
title: Orthofotografie für X-Plane 12
description: "Orthofotografie für X-Plane: statische Tile-Generierung mit Ortho4XP und Echtzeit-Streaming für fotorealistische Bodentexturen unter Linux."
---
# Orthofotografie

Für fotorealistische Bodentexturen existieren zwei Ansätze. Statische Generierung mit Ortho4XP erzeugt DDS-Kacheln vorab und speichert sie lokal — bis zu Zoom Level 19 für maximale Detailtreue, aber speicherintensiv und auf die vorbereiteten Regionen beschränkt. Streaming-Lösungen wie AutoOrtho oder XEarthLayer liefern Kacheln zur Laufzeit über ein virtuelles Dateisystem, ohne Vorabgenerierung, um den Preis von Netzwerklast während des Flugs. Ortho4XP generiert neben Texturen auch hochauflösende Meshes, optional mit LiDAR-Daten für präzisere Geländedarstellung.

[Konzepte & Methoden](orthophotography_intro.md) vergleicht beide Ansätze, erklärt das `scenery_packs.ini`-Setup und ordnet sie nach Flugstil und Speicherbudget den Spielerprofilen zu. [Ortho4XP](ortho4xp.md) ist die Praxisanleitung für statische Kacheln unter Linux: Installation, OrthoForge, Parameterreferenz und LiDAR. Die Streaming-Tools haben eine eigene Sektion, [Ortho Streaming](../ortho_streaming/index.md), inklusive der Kombination [Statisch + Streaming](../ortho_streaming/static_plus_streaming.md) aus lokalen Kacheln und Bildern auf Abruf.

- **[Konzepte & Methoden](orthophotography_intro.md)** — Überblick über statische und Streaming-Verfahren
- **[Ortho4XP](ortho4xp.md)** — Statische Ortho-Kacheln offline generieren
