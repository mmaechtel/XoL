---
description: "Ortho-Streaming für X-Plane unter Linux: AutoOrtho und XEarthLayer liefern Satellitenbilder per FUSE, kombinierbar mit lokalen Ortho4XP-Tiles."
---
# Ortho Streaming

AutoOrtho und XEarthLayer streamen Satellitenbilder bei Bedarf über ein virtuelles FUSE-Dateisystem direkt in X-Plane — globale Abdeckung ohne lokale Vorabgenerierung. AutoOrtho in der aktiven Fork-Version 2.0 bietet eine native C-Pipeline für schnelleres Laden, XEarthLayer setzt auf Rust mit adaptivem Prefetch, der zwischen Ring-Vorladen am Boden und Track-Vorhersage im Reiseflug wechselt. Beide Systeme lassen sich mit lokalen Ortho4XP-Kacheln kombinieren: die statischen Tiles haben in der `scenery_packs.ini` Vorrang, Streaming füllt den Rest.

- **[AutoOrtho](autoortho.md)** — Ortho-Streaming für globale Abdeckung
- **[XEarthLayer](xearthlayer.md)** — Rust-basiertes Streaming mit adaptivem Prefetch
- **[Statisch + Streaming](static_plus_streaming.md)** — Beide Systeme kombinieren
