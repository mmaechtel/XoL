---
description: "Orthofotografie für X-Plane: statische Tile-Generierung mit Ortho4XP und Echtzeit-Streaming für fotorealistische Bodentexturen unter Linux."
---
# Orthofotografie

Für fotorealistische Bodentexturen existieren zwei Ansätze: statische Generierung mit Ortho4XP erzeugt DDS-Kacheln vorab und speichert sie lokal — bis zu Zoom Level 19 für maximale Detailtreue, aber speicherintensiv. Streaming-Lösungen liefern Kacheln zur Laufzeit über ein virtuelles Dateisystem, ohne Vorabgenerierung. Ortho4XP generiert neben Texturen auch hochauflösende Meshes, optional mit LiDAR-Daten für präzisere Geländedarstellung.

- **[Konzepte & Methoden](orthophotography_intro.md)** — Überblick über statische und Streaming-Verfahren
- **[Ortho4XP](ortho4xp.md)** — Statische Ortho-Kacheln offline generieren
