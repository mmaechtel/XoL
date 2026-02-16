# **XoL**: Running **X**-Plane **o**n **L**inux

Diese Dokumentation richtet sich an Linux-erfahrene Benutzer, die X-Plane unter Linux betreiben möchten. Eine funktionierende Linux-Installation wird vorausgesetzt.

Die hier gezeigten Beispiele basieren auf Debian Linux, lassen sich aber leicht auf andere Distributionen übertragen. Die grundlegenden Konzepte und Vorgehensweisen bleiben dabei gleich - lediglich die spezifischen Paketmanager-Befehle oder Repository-Konfigurationen müssen entsprechend angepasst werden.

## Featured Video

<div class="video-container" markdown>
<video controls width="100%" preload="metadata" poster="../assets/video/de/Toliss_Plugin_Flow/Vom_Briefing_zum_Gate.jpg">
  <source src="../assets/video/de/Toliss_Plugin_Flow/Vom_Briefing_zum_Gate.mp4" type="video/mp4">
</video>
</div>

[Alle Videos →](videos.md)

## Inhalt der Dokumentation

Die Dokumentation behandelt die Konfiguration und Optimierung von X-Plane unter Linux. Im Kern geht es um Systemtuning — Kernel-Parameter, CPU-Governor, GPU-Treiber, Display-Server-Wahl und Dateisystem-Optimierung — ergänzt durch Performance-Analyse mit den integrierten Tools von X-Plane und Linux-Monitoring-Werkzeugen. Weitere Abschnitte behandeln Szenerie-Verwaltung mit Orthofoto-Streaming, Flugbetrieb einschließlich ATC-Verfahren über alle Flugphasen sowie ein Nachschlagewerk Linux-kompatibler Addons und Plugins.

## Struktur der Anleitungen

Die Anleitungen sind modular aufgebaut — einzelne Themen lassen sich unabhängig umsetzen oder nach Bedarf kombinieren. Jede Anleitung beschreibt das Ziel, zeigt die notwendigen Schritte und bietet Tipps zur Fehlerbehebung. Die Inhalte gliedern sich in Bereiche zu Linux-Systemoptimierung, X-Plane-Konfiguration und Performance, Szenerie-Verwaltung, Addons und Plugins sowie Flugbetrieb.

## Beitragen

Diese Dokumentation ist ein offenes Projekt. Verbesserungen oder Ergänzungen können über GitHub beigetragen werden:

- Issues für Fehler oder Vorschläge erstellen
- Pull Requests für Änderungen einreichen
- Erfahrungen in den Diskussionen im Footer dieser Webseite (z.B. über den Discord-Link) teilen

## Letzte Änderungen

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


