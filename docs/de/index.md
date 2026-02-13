# **XoL**: Running **X**-Plane **o**n **L**inux

Diese Dokumentation richtet sich an Linux-erfahrene Benutzer, die X-Plane unter Linux betreiben möchten. Eine funktionierende Linux-Installation wird vorausgesetzt.

Die hier gezeigten Beispiele basieren auf Debian Linux, lassen sich aber leicht auf andere Distributionen übertragen. Die grundlegenden Konzepte und Vorgehensweisen bleiben dabei gleich - lediglich die spezifischen Paketmanager-Befehle oder Repository-Konfigurationen müssen entsprechend angepasst werden.

## Featured Video

<div class="video-container" markdown>
<video controls width="100%" preload="metadata" poster="../assets/video/xplane_und_scenery_packs.ini/X-Planes_Welt__Richtig_gebaut.jpg">
  <source src="../assets/video/xplane_und_scenery_packs.ini/X-Planes_Welt__Richtig_gebaut.mp4" type="video/mp4">
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

### 2026-02-13
- Neue Seite [Videos](videos.md) — Videosammlung mit eingebetteten Übersichtsvideos
- [XEarthLayer](addon/xearthlayer.md) ergänzt: CPU-Tuning-Abschnitt mit Thread-Konfiguration, Szenario-Tabelle und Disk-I/O-Profilen für den Parallelbetrieb mit X-Plane
- [Display-Server](displayserver.md) und Startseite: Videos an den Kapitelanfang verschoben
- [Wayland-Session](displayserver_wayland.md) gestrafft: Redundante Latenztabelle und Desktop-Eintrag durch Verweise auf Hauptseiten ersetzt
- [Einführung](intro.md) ergänzt: Übersichtsvideo eingebettet
- [Einführung Orthofotografie](addon/orthophotography_intro.md) ergänzt: Neuer Abschnitt zur Einordnung der Ortho-Streamer in der scenery_packs.ini mit Beispiel-Konfigurationen für AutoOrtho, XEarthLayer und XPME
- [Szenerien-Komponenten](scenery_components.md) und Startseite: Neues Video zur scenery_packs.ini eingebettet
- [Szenerien-Komponenten](scenery_components.md) ergänzt: Verweise auf Ortho-Streaming und Ortho4XP im Add-ons-Abschnitt

### 2026-02-11
- [Display-Server](displayserver.md) Seiten faktengeprüft: Debian-Defaults korrigiert, XWayland-Zeile in Hugl-Tabelle ergänzt, Latenzmessungen präzisiert, NVIDIA-Modeset-Default aktualisiert, MESA-Variable auf Mesa-Treiber eingeschränkt

### 2026-02-09
- Neue Seiten [Display-Server](displayserver.md) — Übersicht, [X11-Session](displayserver_x11.md) und [Wayland-Session](displayserver_wayland.md): Protokollvergleich (X11/Wayland/XWayland), Hardware-Latenzmessungen, GPU-Empfehlungen, Session-Wechsel, Troubleshooting
- [Glossar](glossary.md) erweitert: Compositor, Display-Server, Wayland, X11, XWayland
- [X-Plane Konfiguration](xplane/config.md) Display-Server-Abschnitt gekürzt mit Verweis auf neue Seiten
- Neue Seite [Systemtools](systemtools.md) — Monitoring-Tools (htop, turbostat, mpstat, iotop, ioping, glances u.a.) zur Verifikation der Tuning-Einstellungen. Alle Angaben gegen Primärquellen faktengeprüft
- Neue Seite [Systemtuning](systemtuning.md) — Latenzoptimierung für X-Plane: zwei Kernel-Profile (Standardkernel vs. Liquorix), Governor, C-States, Interrupt-Shielding, NVMe-Energiesparen, Kernel-Wechsel via GRUB
- [X-Plane Konfiguration](xplane/config.md) überarbeitet: Fokus auf Linux-Spezifika — Vulkan/Zink, Shader-Cache, Umgebungsvariablen, Display-Server, Audio, Controller, CLI-Fehlerbehebung. Quellenabschnitt mit Primärquellen ergänzt
- [Liquorix](liquorix.md) ergänzt: EEVDF-Scheduler und Optimierungsmodell erklärt
- [Systemfehler](xplane/systemfehler.md) auf Navigationsseite reduziert, [Glossar](glossary.md) um Zink, FMOD, evdev, RADV erweitert
- Neue [XEarthLayer](addon/xearthlayer.md)-Dokumentation — Rust-basierte Streaming-Alternative mit adaptivem Prefetch
- [Orthofotografie](addon/orthophotography_intro.md) neu strukturiert, [AutoOrtho](addon/autoortho.md) aktualisiert (Fork 2.0), [Statisch + Streaming](addon/static_plus_streaming.md) vollständig überarbeitet
