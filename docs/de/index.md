# **XoL**: Running **X**-Plane **o**n **L**inux

Diese Dokumentation behandelt Einrichtung und Optimierung von X-Plane 12 (Laminar Research) unter Linux. Sie richtet sich an erfahrene Linux-Nutzer — eine funktionierende Installation wird vorausgesetzt. Die Beispiele basieren auf Debian, lassen sich aber mit geringen Anpassungen auf andere Distributionen übertragen.

## Einstieg

- **Warum Linux?** [Einführung](intro.md) erklärt, was X-Plane unter Linux besonders macht.
- **Neu mit X-Plane unter Linux?** [Erste Schritte](begin.md) behandelt Systemvoraussetzungen, Installation und ersten Start.
- **X-Plane läuft bereits?** [Performance-Grundlagen](performance_overview.md) erklärt die drei Lastdimensionen (CPU, I/O, Netzwerk) als Basis für das [System-Tuning](systemtuning.md).

## Über diese Dokumentation

Im Kern geht es um Linux-Systemtuning — Kernel-Parameter, CPU-Governor, GPU-Treiber, Display-Server-Wahl und Dateisystem-Optimierung — ergänzt durch Performance-Analyse mit den integrierten Tools von X-Plane und Linux-Monitoring-Werkzeugen. Weitere Abschnitte behandeln Szenerie-Verwaltung mit Orthofoto-Streaming, Flugbetrieb einschließlich ATC-Verfahren sowie ein Nachschlagewerk Linux-kompatibler Addons und Plugins. Die Anleitungen sind modular aufgebaut — einzelne Themen lassen sich unabhängig umsetzen oder nach Bedarf kombinieren.

## Beitragen

Diese Dokumentation ist ein offenes Projekt. Verbesserungen oder Ergänzungen können über GitHub beigetragen werden:

- Issues für Fehler oder Vorschläge erstellen
- Pull Requests für Änderungen einreichen
- Erfahrungen in den Diskussionen im Footer dieser Webseite (z.B. über den Discord-Link) teilen

## Featured Video: Vom Briefing zum Gate

<div class="video-container" style="max-width: 640px;" markdown>
<video controls width="100%" preload="metadata" aria-label="Video: Vom Briefing zum Gate" poster="../assets/video/de/Vom_Briefing_zum_Gate/Vom_Briefing_zum_Gate.jpg">
  <source src="../assets/video/de/Vom_Briefing_zum_Gate/Vom_Briefing_zum_Gate.mp4" type="video/mp4">
</video>
</div>

[Alle Videos →](videos.md)

## Letzte Änderungen

### 2026-02-16
- Barrierefreiheit verbessert: größere Schrift, Tastatur-Focus-Indikatoren, Skip-Link, Video-ARIA-Labels
- Quellenabschnitte überarbeitet: Arch-Wiki-Links durch distro-unabhängige Quellen ersetzt
- [Szenerie-Komponenten](scenery_components.md) auditiert: Prioritätsrichtung korrigiert, DDS-Format, OSM-Klarstellung, Ton angeglichen
- Neues Video: [Display-Server](displayserver.md) — Entscheidungshilfe X11 vs Wayland
- Neue Videos: [Einführung](intro.md) — Doku-Tour durch XoL (DE + EN)
- [Szenerien-Komponenten](scenery_components.md): Fachbegriffe mit [Glossar](glossary.md) verlinkt, neuer Eintrag Global Airports

### 2026-02-15
- Neue Addon-Seiten: [SGES](addon/sges.md), [KabinXP](addon/kabinxp.md), [LST](addon/lst.md), [LinuxTrack](addon/linuxtrack.md), [XLinSpeak](addon/xlinspeak.md), [WINCTRL](addon/winctrl.md), [TerrainRadar](addon/terrainradar.md), [NOAA Weather](addon/noaa_weather.md), [MobiFlight](addon/mobiflight.md), [SayIntentions.AI](addon/sayintentions.md)
- Neue Sounds-Kategorie: [KOSP Project](addon/kosp_project.md), [Mango Studios](addon/mango_studios.md)
- Neue Seite [Performance-Grundlagen](performance_overview.md)
- ATC-Sektion: 6 Flugphasen-Seiten ([Pushback & Taxi](flight_operations/pushback_taxi.md), [Start](flight_operations/takeoff.md), [Abflug & Steigflug](flight_operations/departure.md), [Streckenflug](flight_operations/enroute.md), [Anflug](flight_operations/approach.md), [Landung & Abstellen](flight_operations/landing.md))
- [ToLiss-Ökosystem](addon/toliss_ecosystem.md) umstrukturiert, Videos eingebettet
- Bestehende Addon-Seiten überarbeitet: Querverweise, Korrekturen, Preise und redundante Linux-Hinweise entfernt
- Navigation: Kategorien flachgezogen, Sounds-Kategorie hinzugefügt
- [FlyWithLua](addon/flywithlua.md): Allgemeine Skript-Installationsanleitung ergänzt
- [Performance](xplane/performance.md) überarbeitet: Fließtext statt verschachtelter Listen, Richtwert- und Microprofiler-Tabellen, Diagnose-Workflows, Quellenabschnitt

### 2026-02-14
- Neue Seite [System-Tuning Einführung](systemtuning_intro.md), Videos eingebettet (DE + EN)
- [Liquorix-Kernel](liquorix.md) auditiert: Scheduler-Beschreibung korrigiert, Schnellinstallation ergänzt, Seite überarbeitet
- [Nvidia-Treiber](nvidia.md), [Systemtuning](systemtuning.md), [Systemtools](systemtools.md), [X-Plane Konfiguration](xplane/config.md) auditiert und faktengeprüft
- [Erste Schritte](begin.md) überarbeitet, [Glossar](glossary.md) erweitert
- Navigation: System Monitoring unter System-Tuning gruppiert


