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
- [ToLiss-Ökosystem](addon/toliss_ecosystem.md) und [Videos](videos.md): Video „Beyond the Default Cockpit" eingebettet (EN)
- [ToLiss-Ökosystem](addon/toliss_ecosystem.md) und [Videos](videos.md): Video „Vom Briefing zum Gate" eingebettet (DE)
- ATC-Sektion erweitert: 6 neue Flugphasen-Seiten — [Pushback & Taxi](flight_operations/pushback_taxi.md), [Start](flight_operations/takeoff.md), [Abflug und Steigflug](flight_operations/departure.md), [Streckenflug](flight_operations/enroute.md), [Anflug](flight_operations/approach.md), [Landung und Abstellen](flight_operations/landing.md) — vollständige Gate-to-Gate ATC-Kommunikationsanleitung
- Neue Addon-Seiten: [SkunkCrafts Updater](addon/skunkcrafts_updater.md) (Update-Tool mit glibc-Anforderung und Wayland-Hinweisen), [XPPython3](addon/xppython3.md) (Python-3-Scripting-Engine mit Debian-Abhängigkeiten)
- Navigation umgebaut: Addon-Kategorien flachgezogen (Verschiedenes-Wrapper entfernt), [ToLiss-Ökosystem](addon/toliss_ecosystem.md) als eigener Menüpunkt, Ortho Streaming als Unterkapitel
- ToLiss SimBrief Connector entfernt (veraltet), [simbrief_hub](https://github.com/hotbso/simbrief_hub)-Referenz im [ToLiss-Ökosystem](addon/toliss_ecosystem.md) ergänzt
- [XRoad](addon/xroad.md): GitHub-Repository-Link ergänzt
- Addon-Seiten überarbeitet: Faktenkorrekturen ([Follow the Greens](addon/followthegreens.md), [XGS](addon/xgs.md), [AutoGate](addon/autogate.md)), Linux-Hinweise ergänzt ([ToLiss-Ökosystem](addon/toliss_ecosystem.md)), Intro-Umschreibung ([XTextureExtractor](addon/xtextureextractor.md))
- [ToLiss-Ökosystem](addon/toliss_ecosystem.md) umstrukturiert: Übersichts-Absatz, `###`-Überschriften statt Fettdruck für bessere Navigation
- Neue Addon-Seiten: [ToLiss-Ökosystem](addon/toliss_ecosystem.md) (Callouts, Automatisierung, Boarding, Bodendienste), [XGS](addon/xgs.md) (Landing-Speed-Analyse), [Follow the Greens](addon/followthegreens.md) (A-SMGCS Rollführung)
- Addon-Sektion erweitert: [AutoDGS](addon/autodgs.md), [openSAM](addon/opensam.md), [AutoGate](addon/autogate.md), [DataRefTool](addon/datareftool.md), [Little XpConnect](addon/littlexpconnect.md), [XTextureExtractor](addon/xtextureextractor.md) — neue Kategorien Werkzeuge und erweiterte Verkehr & Bodenbetrieb
- Addon-Sektion ausgebaut: Neue Seiten [FlyWithLua](addon/flywithlua.md), [AviTab](addon/avitab.md), [XCamera](addon/xcamera.md), [LiveTraffic](addon/livetraffic.md), [Better Pushback](addon/betterpushback.md) — jeweils mit Hintergrund, Linux-Installation, bekannten Problemen und Quellen
- Bestehende Seiten [XRoad](addon/xroad.md) und [AEP](addon/aep.md) nach einheitlichem Template überarbeitet
- Navigation: Verschiedenes-Sektion mit Kategorien (Scripting, Cockpit & Kamera, Verkehr & Bodenbetrieb, Szenerie)
- Neue Seite [Performance-Grundlagen](performance_overview.md): CPU-, I/O- und Netzwerk-Lastdimensionen, Wechselwirkungen, Frame Time als Maßeinheit, Optimierungsansätze im Überblick
- [Orthofotographie](addon/orthophotography_intro.md), [Performance-Grundlagen](performance_overview.md) und [Videos](videos.md): Ortho-Streaming- und Performance-Videos eingebettet (DE + EN)
- [Performance-Grundlagen](performance_overview.md) korrigiert: SSD-Latenzen, DDR5-Bandbreite und TCP-Congestion-Formulierung präzisiert

### 2026-02-14
- [X-Plane Konfiguration](xplane/config.md) erweitert: udev-Regeln für Controller ausführlich dokumentiert (Device-IDs ermitteln, Regel-Beispiel, identische Geräte per USB-Port unterscheiden)
- [Nvidia-Treiber](nvidia.md) auditiert: Paketmanager-Methode als empfohlenen Ansatz ergänzt, Persistence-Mode- und Modeset-Aussagen korrigiert, Composition-Pipeline-Einstellungen als X11-only gekennzeichnet, Quellenabschnitt ergänzt
- [X-Plane Konfiguration](xplane/config.md) korrigiert: `__GL_*`-Variablen differenziert (`__GL_SYNC_TO_VBLANK` wirkt auf Vulkan), NVIDIA Smooth Motion als experimentelle Option ergänzt
- [Systemtools](systemtools.md) verifiziert: Fehlendes `sudo` bei ioping-Befehlen ergänzt (direkter Device-Zugriff erfordert Root)
- [Systemtools](systemtools.md) auditiert: btop-Hotkey korrigiert, cpupower/turbostat/mpstat-Beschreibungen präzisiert, glances- und fatrace-Notation verbessert, Tabellen-Beschriftungen formatiert
- [Systemtuning](systemtuning.md) faktengeprüft: Scheduler-Angaben korrigiert, nicht funktionalen Kernel-Parameter entfernt, NVMe-Hinweise präzisiert, Quellenabschnitt ergänzt
- [Erste Schritte](begin.md) überarbeitet: Fehlerbehebung zusammengeführt, 32-Bit-Hinweis präzisiert, Display-Server-Verweis ergänzt
- Sprachliche Überarbeitung (DE): [Erste Schritte](begin.md) und [Docker](docker.md) auf unpersönlichen Stil umgestellt
- [Glossar](glossary.md) erweitert: Neue Begriffe PDS und irqbalance
- [Systemtuning](systemtuning.md) Glossar-Verlinkungen ergänzt: FPS, Frame Time, Latenz, Preemption, NVMe, C-States, EEVDF, PDS, irqbalance
- [Systemtuning](systemtuning.md) und [Videos](videos.md): System-Tuning-Video eingebettet (DE + EN)
- [Glossar](glossary.md) erweitert: Neuer Begriff SoftIRQ
- [Systemtools](systemtools.md) Glossar-Verlinkungen ergänzt: NVMe, C-States, IRQ, CPU-Governor, Latenz, APST
- Neue Seite [System-Tuning Einführung](systemtuning_intro.md): Video-Intro als Klammer für Tuning und Monitoring
- Navigation: Systemtools umbenannt in System Monitoring, gruppiert unter System-Tuning


