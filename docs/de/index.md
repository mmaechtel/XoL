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

### 2026-11-23

- Neue Seite: [XP SnowState](addon/scenery_addons/xp_snowstate.md) korrigiert X-Planes Schnee mit echten Schneehöhen aus Messstationen und Wettermodellen — ein natives Plugin mit Linux-Build, derzeit in der Beta
- [NOAA Weather](addon/scenery_addons/noaa_weather.md) für X-Plane 12.4.4 überarbeitet: Schnee aus X-Planes eigenen Wetterdateien, neuer Ordneraufbau, eine Tabelle der Einstellungen mit der Empfehlung für Online-Flüge und die Grenzen eines einzigen Schneewerts im Gebirge
- [xa-snow](addon/scenery_addons/xa-snow.md) wurde vom Entwickler eingestellt, weil X-Plane 12.4.4 liegenden Schnee selbst zeichnet

### 2026-11-22

- [SGES](addon/flylua_scripts/sges.md): Die Entwicklung des FlyWithLua-Skripts ist eingestellt; die Seite beschreibt jetzt den nativen Nachfolger SGES NG, der sich im Test befindet (X-Plane 12.4 oder neuer, ohne FlyWithLua)
- [X-ProTurb](addon/flylua_scripts/xproturb.md) aktualisiert: einmalige Kalibrierung je Flugzeug, reale Wetterdaten über LiveCAT, getrennte Skalen für Atmosphäre und Flugzeug sowie überarbeitete Installation
- [SimLoad Manager](addon/traffic/simloadmanager.md) öffnet und schließt die Flugzeugtüren automatisch, wenn Bodenfahrzeuge ankommen; [XP CabinState](addon/cockpit/xp_cabinstate.md) bringt neue Servicewagen und Updates direkt im Programm
- [XEarthLayer](scenery/ortho_streaming/xearthlayer.md): Die Regionalpakete sind in ZL16 gebaut, rund um ICAO-Flughäfen in ZL17

### 2026-11-02

- [XEarthLayer](scenery/ortho_streaming/xearthlayer.md) auf den Stand von Version 0.5.0 gebracht: macOS-Unterstützung, generierte Nachtbeleuchtung für Ortho-Szenerie, die neu gebaute Paketbibliothek mit 17 Regionen samt neuem Paketmanager, eine eigene Prefetch-Spur, die X-Planes Kachelanfragen nie ausbremst, und XDG-Pfade unter `~/.config` und `~/.cache`. Ein Warnkasten beschreibt den Umstieg von der alten Paketgeneration
