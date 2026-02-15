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

Die Dokumentation umfasst die wichtigsten Bereiche der X-Plane-Konfiguration unter Linux. Im Fokus stehen die optimalen Einstellungen für X-Plane, die Performance-Optimierung durch Kernel, Treiber und Systemeinstellungen, sowie die Installation und Konfiguration wichtiger Erweiterungen wie AutoOrtho. Zusätzlich werden häufige Probleme und deren Lösungen ausführlich behandelt. Ein besonderer Schwerpunkt liegt auf der Performance-Analyse mit integrierten und externen Tools, der Optimierung des Dateisystems für schnelle Ladezeiten und der hardware-spezifischen Anpassung für maximale Leistung.

## Struktur der Anleitungen

Die technischen Anleitungen sind modular aufgebaut und ermöglichen eine flexible Implementierung. Einzelne Komponenten können nach Bedarf umgesetzt oder das gesamte System nach den Anforderungen angepasst werden. Jede Anleitung beschreibt das Ziel und den Nutzen der Änderung, zeigt die notwendigen Schritte auf, erklärt wichtige Konfigurationsoptionen und bietet Tipps zur Fehlerbehebung. Die Anleitungen sind dabei in logische Abschnitte gegliedert: Grundlegende Systemoptimierung, Performance-Monitoring und -Analyse, Hardware-spezifische Anpassungen sowie fortgeschrittene Konfigurationen für spezielle Anwendungsfälle.

## Beitragen

Diese Dokumentation ist ein offenes Projekt. Verbesserungen oder Ergänzungen können über GitHub beigetragen werden:

- Issues für Fehler oder Vorschläge erstellen
- Pull Requests für Änderungen einreichen
- Erfahrungen in den Diskussionen im Footer dieser Webseite (z.B. über den Discord-Link) teilen

## Letzte Änderungen

### 2026-02-15
- Neue Addon-Seiten: [SGES](addon/sges.md), [KabinXP](addon/kabinxp.md), [LST](addon/lst.md), [LinuxTrack](addon/linuxtrack.md), [XLinSpeak](addon/xlinspeak.md), [WINCTRL](addon/winctrl.md), [TerrainRadar](addon/terrainradar.md), [NOAA Weather](addon/noaa_weather.md)
- Neue Addon-Seiten (Via KVM): [MobiFlight](addon/mobiflight.md), [SayIntentions.AI](addon/sayintentions.md)
- Neue Seite [Performance-Grundlagen](performance_overview.md)
- ATC-Sektion: 6 neue Flugphasen-Seiten ([Pushback & Taxi](flight_operations/pushback_taxi.md), [Start](flight_operations/takeoff.md), [Abflug & Steigflug](flight_operations/departure.md), [Streckenflug](flight_operations/enroute.md), [Anflug](flight_operations/approach.md), [Landung & Abstellen](flight_operations/landing.md))
- [ToLiss-Ökosystem](addon/toliss_ecosystem.md) umstrukturiert, Videos eingebettet (DE + EN)
- Addon-Sektion ausgebaut: [FlyWithLua](addon/flywithlua.md), [AviTab](addon/avitab.md), [XCamera](addon/xcamera.md), [LiveTraffic](addon/livetraffic.md), [Better Pushback](addon/betterpushback.md), [AutoDGS](addon/autodgs.md), [openSAM](addon/opensam.md), [AutoGate](addon/autogate.md), [DataRefTool](addon/datareftool.md), [Little XpConnect](addon/littlexpconnect.md), [XTextureExtractor](addon/xtextureextractor.md), [SkunkCrafts Updater](addon/skunkcrafts_updater.md), [XPPython3](addon/xppython3.md), [ToLiss-Ökosystem](addon/toliss_ecosystem.md), [XGS](addon/xgs.md), [Follow the Greens](addon/followthegreens.md)
- Navigation überarbeitet: Addon-Kategorien flachgezogen, Ortho Streaming und FlyWithLua-Skripte als eigene Kategorien
- Addon-Seiten überarbeitet: Querverweise zwischen verwandten Plugins ergänzt, Übersetzungskorrekturen (DE), inhaltliche Korrekturen (Flugzeugbezeichnungen, Versionsangaben), veraltete Formulierungen aktualisiert
- [ToLiss-Ökosystem](addon/toliss_ecosystem.md) ergänzt: Carda Realistic Engine Mods (hochdetaillierte 3D-Triebwerke für A319/A320/A321)

### 2026-02-14
- Neue Seite [System-Tuning Einführung](systemtuning_intro.md), Videos eingebettet (DE + EN)
- [Nvidia-Treiber](nvidia.md), [Systemtuning](systemtuning.md), [Systemtools](systemtools.md), [X-Plane Konfiguration](xplane/config.md) auditiert und faktengeprüft
- [Erste Schritte](begin.md) überarbeitet, [Glossar](glossary.md) erweitert
- Navigation: System Monitoring unter System-Tuning gruppiert


