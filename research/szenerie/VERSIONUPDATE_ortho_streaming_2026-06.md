# Versionsupdate: XEarthLayer & AutoOrtho (Juni 2026)

**Datum:** 2026-06-24
**Geprüfte Seiten:** `docs/{en,de}/scenery/ortho_streaming/xearthlayer.md`, `.../autoortho.md`
**Primärquellen:** GitHub-Release-Seiten (direkt per WebFetch gelesen)

---

## XEarthLayer — v0.4.4 → v0.4.6

**Quelle:** github.com/samsoir/xearthlayer/releases (Latest: v0.4.6, 11. Mai 2026; davor v0.4.5, 6. Mai 2026). Bestätigt per WebSearch.

Übernommene Neuerungen (im „Neu in v0.4.6"-Block + Cache-/Setup-Abschnitten):

- **Setup-Wizard, vier Schritte:** Custom Scenery → Package Location → Cache Configuration → DDS Encoding
- **Dynamische Cache-Dimensionierung:** Disk-Cache Standard 25% des freien Speichers, Untergrenze 10 GB; Memory-Cache aus verfügbarem RAM abgeleitet
- **GPU-Encoding-Schritt:** Adapter-Enumeration + Warnung bei Multi-GPU
- **`packages.disable_overlays`**, maskierte Credentials (`google_api_key`, `mapbox_access_token`) in Config-Ausgabe
- **Download-Konsolidierung:** eine Strategie mit Retry pro Teil, Speicherplatz-Pre-Check, sauberer Abbruch bei erstem Fehler
- **v0.4.5-Fix:** Kacheln aus fehlgeschlagenen Chunk-Downloads werden nicht mehr gecacht (keine persistenten Magenta-Tiles mehr); `xearthlayer cache clear`

## AutoOrtho (ProgrammingDinosaur-Fork) — 2.2.0 → 2.5.0

**Quelle:** github.com/ProgrammingDinosaur/autoortho4xplane/releases (Latest: „AutoOrtho Continued 2.5.0", 19. Juni 2026; davor 2.4.0, 2.3.2, 2.3.1).

**Entscheidung (User, 2026-06-24):** Laufende Versionsnummern des Forks **weglassen** (vorher „2.2.0"/„Fork 2.0"), da kein Content verloren geht — deckt sich mit „Versionsnummern minimieren" (CLAUDE.md / AUDIT_FLOW). Inhaltliche Neuerungen versionsfrei eingebaut:

- **2.4.0:** vereinheitlichte Single-Process-Architektur über alle OS; VRAM-Optimierung via dynamischer DDS-Dimensionierung; partial-cache-Vermeidung, Mipmap-Fallback-Scaling
- **2.3.1:** Karten-UI vom eingebetteten Browser auf lokalen Endpunkt umgestellt; gebündeltes Chromium entfernt (kleiner, stabiler); macOS-Startup-Crash-Fix
- **2.3.2:** Küstenlinien-Blending-Korrektur; Exit-Freeze-Fix; FUSE-Verbesserungen; Vermeidung degradierter Zoomstufen im DDS-Cache
- **2.5.0:** Performance- + Cache-Verbesserungen; Fix der Linux-Memory-Berechnung

Entfernte Versionsnennungen: Heading „(Current: 2.2.0)", „Starting with version 2.0", „~2x faster (as of 2.2.0)", Tabellen-Zelle „Up to ZL18 (Fork 2.0)", kubilus1 „0.7.2" → „final release (January 2024)".
