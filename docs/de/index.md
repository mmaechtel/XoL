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

### 2026-03-14
- [XEarthLayer](scenery/ortho_streaming/xearthlayer.md) aktualisiert auf v0.3.1: GPU-beschleunigte DDS-Komprimierung, ISPC-SIMD-Kompression als Standard, Boundary-Driven-Prefetch-System, Online-Netzwerk-Unterstützung (VATSIM/IVAO/PilotEdge)
- [AutoOrtho](scenery/ortho_streaming/autoortho.md) aktualisiert auf v2.2.0: ~2x schnellere Ladezeiten, SimBrief-Integration mit routenbasiertem Prefetch, Seasons-Unterstützung

### 2026-03-06
- [Wie Streaming funktioniert](scenery/ortho_streaming/how_streaming_works.md) ergänzt: Neuer Abschnitt zum FUSE-Congestion-Engpass — erklärt, wie niedrige `max_background`-Standardwerte parallele Tile-Anfragen limitieren und Frame-Drops an DSF-Grenzen verursachen

### 2026-02-27
- [Swap & Speicherverwaltung](linux/system/swap.md), [Systemtuning](linux/system/systemtuning.md) und [Fallstudie Tuning](linux/system/tuning_casestudy.md) überarbeitet: Revidierte Empfehlungen für zram — `swappiness=180` + `watermark_scale_factor=125` statt `watermark_boost_factor=15000`, basierend auf 14 Messläufen. Getrennte Konfigurationsblöcke für zram und Disk-Swap, neue Praxisnotizen zu Dirty-Ratio-Tuning und vfs_cache_pressure





