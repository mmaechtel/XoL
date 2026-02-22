---
description: "X-Plane 12 unter Linux — Einrichtung, Kernel-Tuning, GPU-Treiber, Dateisystem-Optimierung, Szenerie-Verwaltung und Addon-Katalog."
---
# **XoL**: Running **X**-Plane **o**n **L**inux

Diese Dokumentation behandelt Einrichtung und Optimierung von X-Plane 12 (Laminar Research) unter Linux. Sie richtet sich an erfahrene Linux-Nutzer — eine funktionierende Installation wird vorausgesetzt. Die Beispiele basieren auf Debian, lassen sich aber mit geringen Anpassungen auf andere Distributionen übertragen.

## Einstieg

- **Warum Linux?** [Einführung](intro.md) erklärt, was X-Plane unter Linux besonders macht.
- **Neu mit X-Plane unter Linux?** [Erste Schritte](begin.md) behandelt Systemvoraussetzungen, Installation und ersten Start.
- **X-Plane läuft bereits?** [Performance](fundamentals/performance/performance_overview.md) erklärt die drei Lastdimensionen (CPU, I/O, Netzwerk) als Basis für das [System-Tuning](linux/system/systemtuning.md).

## Über diese Dokumentation

Im Kern geht es um Linux-Systemtuning — Kernel-Parameter, CPU-Governor, GPU-Treiber, Display-Server-Wahl und Dateisystem-Optimierung — ergänzt durch Performance-Analyse mit den integrierten Tools von X-Plane und Linux-Monitoring-Werkzeugen. Weitere Abschnitte behandeln Szenerie-Verwaltung mit Orthofoto-Streaming, Flugbetrieb einschließlich ATC-Verfahren sowie ein Nachschlagewerk Linux-kompatibler Addons und Plugins. Die Anleitungen sind modular aufgebaut — einzelne Themen lassen sich unabhängig umsetzen oder nach Bedarf kombinieren.

## Beitragen

Diese Dokumentation ist ein offenes Projekt. Verbesserungen oder Ergänzungen können über GitHub beigetragen werden:

- Issues für Fehler oder Vorschläge erstellen
- Pull Requests für Änderungen einreichen
- Erfahrungen in den Diskussionen im Footer dieser Webseite (z.B. über den Discord-Link) teilen

## Featured Video: X-Plane 12: Jagd nach FPS

<div class="video-container" style="max-width: 640px;" markdown>
<video controls width="100%" preload="metadata" aria-label="Video: X-Plane 12 — Jagd nach FPS" poster="../assets/video/de/X-Plane_12__Jagd_nach_FPS/X-Plane_12__Jagd_nach_FPS.jpg">
  <source src="../assets/video/de/X-Plane_12__Jagd_nach_FPS/X-Plane_12__Jagd_nach_FPS.mp4" type="video/mp4">
</video>
</div>

[Alle Videos →](videos.md)

## Letzte Änderungen

### 2026-02-22
- Neue Seite [Fallstudie Tuning](linux/system/tuning_casestudy.md) — Vier gemessene Tuning-Schritte von Mikrorucklern zu stabilen Framezeiten: Memory Pressure, IO-Latenz, zram-Swap und Watermark-Tuning

### 2026-02-21
- Neue Seite [OSM Offshore Oil Rigs](scenery/autogen/osm_offshore_oil_rigs.md) — Weltweite Offshore-Ölplattformen als Heliports auf Basis von OpenStreetMap-Daten, mit Mission-X-Integration für Helikoptermissionen
- Neue Seite [Funktionsweise Ortho-Streaming](scenery/ortho_streaming/how_streaming_works.md) — X-Planes Textur-Ladekette, FUSE-Dateisystem und die gemeinsame Streaming-Pipeline hinter AutoOrtho und XEarthLayer
- Neue Seite [Swap & Speicherverwaltung](linux/system/swap.md) — Page-Reclaim-Mechanik, Swap-Konfiguration, zram-Kompression und Tuning-Empfehlungen für die Flugsimulation
- Neue Seite [Smoke & Steam for SimHeaven](scenery/autogen/smoke_steam_simheaven.md) — Partikelbasierte Rauch- und Dampfeffekte für X-World-Schornsteine und Kühltürme
- [Einführung](intro.md) erweitert: X-Planes offene Architektur (DataRefs, Plugin-SDK, offene Dateiformate) und Linux' offener Stack als sich ergänzendes Argument verknüpft, Szenerie-Streaming über FUSE als konkreter Linux-Vorteil ergänzt

### 2026-02-20
- Neue Rubrik [Autogen](scenery/autogen/index.md) mit [XPNetwork Europa](scenery/autogen/xpnetwork_europa.md) — OSM-basierte europäische Straßen-, Schienen- und Schiffsnetzwerke mit lokalisierten Verkehrsobjekten
- Neue Seite [XP Walkaround](addon/cockpit/xpwalkaround.md) — First-Person-Walkaround mit Taschenlampe, Campsite-System und Mouse Look, SimpleWalkaround als kostenlose Alternative
- [Systemtuning](linux/system/systemtuning.md), [Performance](xplane/setup_diagnose/performance.md) und [Dateisystem](linux/optimizations/filesystem.md) erweitert: Faktencheck gegen Primärquellen — RAID-Kapazitätsangaben, Mount-Optionen, schedutil/Liquorix-Interaktion und weitere Details präzisiert
- [Performance](xplane/setup_diagnose/performance.md): MangoHUD-Warnung für Wayland + NVIDIA ergänzt (fehlende GPU-Metriken durch Debian-Paket ohne NVML)





