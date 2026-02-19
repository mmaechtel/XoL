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

### 2026-02-19
- [My FS Flights](addon/kvm/myfs_flights.md) überarbeitet: IP-Konfiguration im Plugin dokumentiert, KVM-zu-Linux-Verbindung als getestet bestätigt

### 2026-02-18
- [AutoOrtho](scenery/ortho_streaming/autoortho.md) korrigiert: Falschen USGS-Provider-Verweis behoben, unbelegte RAM- und Bandbreitenangaben entfernt
- [XEarthLayer](scenery/ortho_streaming/xearthlayer.md) korrigiert: Internet-Empfehlung von 800 auf 500 Mbps aktualisiert, versionsspezifischen Installationsbefehl entfernt, Quellen ergänzt
- [AutoOrtho](scenery/ortho_streaming/autoortho.md) überarbeitet: Seitenstruktur mit Thementrennern verbessert, redundanten Fazit-Abschnitt entfernt, Fett-Formatierung vereinheitlicht
- [XEarthLayer](scenery/ortho_streaming/xearthlayer.md) korrigiert: Irreführende Rust-Build-Voraussetzung im Vergleichsabschnitt behoben
- [XEarthLayer](scenery/ortho_streaming/xearthlayer.md) überarbeitet: Stabilitätswarnung an aktuelle Reife angepasst, CLI-Live-Statusanzeige in Vergleichstabelle ergänzt

### 2026-02-17
- Neue Videos: [GPU & VRAM](fundamentals/performance/gpu_vram.md) — GPU-Performance und VRAM-Management (DE + EN)
- Weiterführende Kapitel in den Sektionen Linux, Flugbetrieb, Szenerie und X-Plane ergänzt (33 Seiten)
- [CPU & RAM](fundamentals/performance/cpu_ram.md), [GPU & VRAM](fundamentals/performance/gpu_vram.md), [Latenz](fundamentals/performance/latency.md): Weiterführende Kapitel vereinheitlicht mit zusätzlichen Querverweisen
- Neue Seite [Latenz und Vorhersagbarkeit](fundamentals/performance/latency.md) — Warum Latenz wichtiger ist als Durchsatz, vier Latenzquellen
- Komplette Neustrukturierung: Alle Sektionen in thematische Unterverzeichnisse mit Übersichtsseiten aufgeteilt — inhaltliche Zusammenfassungen kaskadieren von der tiefsten Ebene aufwärts
- Neue Seiten: [CPU & RAM](fundamentals/performance/cpu_ram.md) — Threading-Modell und Arbeitsspeicher, [GPU & VRAM](fundamentals/performance/gpu_vram.md) — Texture Paging, Treiber-Unterschiede und Frame-Time-Analyse
- Neue Seite: [Warum Latenz zählt](linux/system/latency.md) — Video-Einführung in die Tuning-Philosophie



