# **XoL**: Running **X**-Plane **o**n **L**inux

Diese Dokumentation richtet sich an Linux-erfahrene Benutzer, die X-Plane unter Linux betreiben möchten. Eine funktionierende Linux-Installation wird vorausgesetzt.

Die hier gezeigten Beispiele basieren auf Debian Linux, lassen sich aber leicht auf andere Distributionen übertragen. Die grundlegenden Konzepte und Vorgehensweisen bleiben dabei gleich - lediglich die spezifischen Paketmanager-Befehle oder Repository-Konfigurationen müssen entsprechend angepasst werden.

## Featured Video

<div class="video-container" markdown>
<video controls width="100%" preload="metadata" poster="../assets/video/de/systemtools/System-Tuning_für_X-Plane.jpg">
  <source src="../assets/video/de/systemtools/System-Tuning_für_X-Plane.mp4" type="video/mp4">
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

### 2026-02-13
- [Erste Schritte](begin.md) korrigiert: Installer-Anleitung aktualisiert, Systemempfehlungen präzisiert, veraltete Paketnamen und Single-Core-Aussagen korrigiert, Querverweise ergänzt
- [Erste Schritte](begin.md) Glossar-Verlinkungen ergänzt: GRUB, NVMe, VRAM, Orthofotos, FPS, Wayland
- Video-Inhalte sprachgetrennt: Deutsche Videos nur auf DE-Seiten, englisches Video auf EN-Seiten
- Neue Seite [Videos](videos.md) — Videosammlung mit eingebetteten Übersichtsvideos
- [XEarthLayer](addon/xearthlayer.md) ergänzt: CPU-Tuning-Abschnitt für den Parallelbetrieb mit X-Plane
- [Einführung Orthofotografie](addon/orthophotography_intro.md) ergänzt: Einordnung der Ortho-Streamer in der scenery_packs.ini
- [Szenerien-Komponenten](scenery_components.md) ergänzt: Videos und Verweise auf Ortho-Streaming und Ortho4XP
- [Wayland-Session](displayserver_wayland.md) gestrafft, [Display-Server](displayserver.md) und [Einführung](intro.md): Videos eingebettet
- [Über diese Dokumentation](about.md) überarbeitet: Lizenz, Datenschutz, rechtliche Hinweise, Zielgruppe
- [Glossar](glossary.md) ausgebaut: 40 neue Begriffe zu Kernel, Grafik, Dateisystem, Audio und Szenerien

### 2026-02-11
- [Display-Server](displayserver.md) Seiten faktengeprüft: Debian-Defaults korrigiert, XWayland-Zeile in Hugl-Tabelle ergänzt, Latenzmessungen präzisiert, NVIDIA-Modeset-Default aktualisiert, MESA-Variable auf Mesa-Treiber eingeschränkt

