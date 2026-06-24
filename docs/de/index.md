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

### 2026-06-24
- Neue Seite [X-ProTurb](addon/flylua_scripts/xproturb.md): physikbasierte Turbulenz-Engine für X-Plane 12, modelliert die Atmosphäre nach MIL-F-8785C, FAR 25.341 und ICAO 9625 Level-D mit flugzeugspezifischer 6-DOF-Reaktion, von-Kármán-/Dryden-Spektren, CAT, Mountain-Wave- und CB-/Sturmmodellierung
- [XEarthLayer](scenery/ortho_streaming/xearthlayer.md) aktualisiert auf v0.4.6: vierstufiger Setup-Wizard mit dynamischer Disk-Cache-Dimensionierung (25% des freien Speichers) und RAM-basiertem Memory-Cache, GPU-Adapter-Auswahlschritt sowie Cache-Fix, sodass Kacheln aus fehlgeschlagenen Downloads nicht mehr gespeichert werden
- [AutoOrtho](scenery/ortho_streaming/autoortho.md) um die neuesten Features des ProgrammingDinosaur-Forks erweitert: vereinheitlichte Single-Process-Architektur über alle Betriebssysteme, VRAM-Optimierung durch dynamische DDS-Dimensionierung und schlanke Karten-UI ohne gebündelten Chromium-Browser

### 2026-04-27
- [XEarthLayer](scenery/ortho_streaming/xearthlayer.md) aktualisiert auf v0.4.4: Long-Haul-Prefetch-Fix (Dead-State auf Flügen >2 h behoben, mit 9-Stunden-LOWW-Log verifiziert), `max_concurrent_jobs`-Standard auf 50% der logischen CPUs halbiert für weniger X-Plane-Stuttering, getrennte Hit-Raten für Memory/DDS-Disk/Chunks-Ebenen im TUI

### 2026-04-08
- [XEarthLayer](scenery/ortho_streaming/xearthlayer.md) aktualisiert auf v0.4.3: Dreistufiger Cache mit DDS-Disk-Ebene vermeidet Re-Encoding, geschwindigkeitsproportionale Prefetch-Box reduziert Over-Fetching um ~45%, GPU-Encoding jetzt integriert, CPU-Parallelität standardmäßig auf 50%






