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

## Featured Video: Vom Briefing zum Gate

<div class="video-container" style="max-width: 640px;" markdown>
<video controls width="100%" preload="metadata" aria-label="Video: Vom Briefing zum Gate" poster="../assets/video/de/Vom_Briefing_zum_Gate/Vom_Briefing_zum_Gate.jpg">
  <source src="../assets/video/de/Vom_Briefing_zum_Gate/Vom_Briefing_zum_Gate.mp4" type="video/mp4">
</video>
</div>

[Alle Videos →](videos.md)

## Letzte Änderungen

### 2026-02-17
- Komplette Neustrukturierung: Alle Sektionen in thematische Unterverzeichnisse mit Übersichtsseiten aufgeteilt — inhaltliche Zusammenfassungen kaskadieren von der tiefsten Ebene aufwärts
- Neue Seiten: [CPU & RAM](fundamentals/performance/cpu_ram.md) — Threading-Modell und Arbeitsspeicher, [GPU & VRAM](fundamentals/performance/gpu_vram.md) — Texture Paging, Treiber-Unterschiede und Frame-Time-Analyse
- Neue Seite: [Warum Latenz zählt](linux/system/overview.md) — Video-Einführung in die Tuning-Philosophie

### 2026-02-16
- Neues Video: [Display-Server](linux/optimizations/displayserver.md) — Entscheidungshilfe X11 vs Wayland
- Neue Videos: [Einführung](intro.md) — Doku-Tour durch XoL (DE + EN)
- [ToLiss-Ökosystem](addon/toliss/toliss_ecosystem.md): simbrief_hub-Abschnitt ergänzt, neue Seite [ToLiss Mods](addon/toliss/toliss_mods.md)

### 2026-02-15
- Neue Addon-Seiten: [SGES](addon/flylua_scripts/sges.md), [KabinXP](addon/cockpit/kabinxp.md), [LST](addon/scenery_addons/lst.md), [LinuxTrack](addon/cockpit/linuxtrack.md), [XLinSpeak](addon/tools/xlinspeak.md), [WINCTRL](addon/tools/winctrl.md), [TerrainRadar](addon/cockpit/terrainradar.md), [NOAA Weather](addon/scenery_addons/noaa_weather.md), [MobiFlight](addon/kvm/mobiflight.md), [SayIntentions.AI](addon/kvm/sayintentions.md)
- Neue Sounds-Kategorie: [KOSP Project](addon/sounds/kosp_project.md), [Mango Studios](addon/sounds/mango_studios.md)
- Neue Seite [Performance](fundamentals/performance/performance_overview.md)
- ATC-Sektion: 6 Flugphasen-Seiten ([Pushback & Taxi](flight_operations/atc/pushback_taxi.md), [Start](flight_operations/atc/takeoff.md), [Abflug & Steigflug](flight_operations/atc/departure.md), [Streckenflug](flight_operations/atc/enroute.md), [Anflug](flight_operations/atc/approach.md), [Landung & Abstellen](flight_operations/atc/landing.md))
- [FlyWithLua](addon/scripting/flywithlua.md): Allgemeine Skript-Installationsanleitung ergänzt


