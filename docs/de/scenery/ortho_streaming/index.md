---
description: "Ortho-Streaming für X-Plane unter Linux: AutoOrtho, XEarthLayer und XPME liefern Satellitenbilder per FUSE, kombinierbar mit lokalen Ortho4XP-Tiles."
---
# Ortho Streaming

AutoOrtho und XEarthLayer streamen Satellitenbilder bei Bedarf über ein virtuelles FUSE-Dateisystem direkt in X-Plane — globale Abdeckung ohne lokale Vorabgenerierung. AutoOrtho in der aktiven Fork-Version 2.0 bietet eine native C-Pipeline für schnelleres Laden, XEarthLayer setzt auf Rust mit adaptivem Prefetch, der zwischen Ring-Vorladen am Boden und Track-Vorhersage im Reiseflug wechselt. Beide lassen sich mit lokalen Ortho4XP-Kacheln kombinieren: die statischen Tiles haben in der `scenery_packs.ini` Vorrang, Streaming füllt den Rest. XPME ist eine dritte Möglichkeit, Closed Source und Freemium — die hochauflösenden Texturen setzen ein kostenpflichtiges Abonnement voraus, und es steht im Konflikt mit vorhandenen Ortho4XP-Kacheln.

- **[Wie Ortho-Streaming funktioniert](how_streaming_works.md)** — X-Planes Textur-Ladekette, FUSE als virtuelles Dateisystem und die Streaming-Pipeline
- **[AutoOrtho](autoortho.md)** — Ortho-Streaming für globale Abdeckung
- **[XEarthLayer](xearthlayer.md)** — Rust-basiertes Streaming mit adaptivem Prefetch
- **[XPME](xpme.md)** — Closed-Source-Freemium-Alternative mit eigenen Basispaketen
- **[Statisch + Streaming](static_plus_streaming.md)** — Beide Systeme kombinieren

!!! note "Nachtflüge"

    Ortho-Kacheln ersetzen die Bodentexturen, die X-Planes entfernte Nachtbeleuchtung tragen. Bei einem Nachtflug enden die Lichter deshalb abrupt rund ums Flugzeug — die Streaming-Schicht für solche Flüge abzuschalten kostet optisch nichts und stellt die Beleuchtung bis zum Horizont wieder her. Siehe [Bay's Lighting Mod](../../addon/scenery_addons/bays_lighting_mod.md).
