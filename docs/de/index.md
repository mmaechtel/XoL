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

### 2026-11-02

- [XEarthLayer](scenery/ortho_streaming/xearthlayer.md) auf den Stand von Version 0.5.0 gebracht: macOS-Unterstützung, generierte Nachtbeleuchtung für Ortho-Szenerie, die neu gebaute Paketbibliothek mit 17 Regionen samt neuem Paketmanager, eine eigene Prefetch-Spur, die X-Planes Kachelanfragen nie ausbremst, und XDG-Pfade unter `~/.config` und `~/.cache`. Ein Warnkasten beschreibt den Umstieg von der alten Paketgeneration

### 2026-11-01

- Neue Plugin-Seiten: [AOC Datalink Center](addon/cockpit/aoc_datalink_center.md) bringt ACARS/CPDLC-Dispatch über Hoppie als natives Linux-Plugin, [XP CabinState](addon/cockpit/xp_cabinstate.md) simuliert Kabine, Crew und Passagiere — offiziell nur für Windows, dokumentiert mit getestetem Wine-Setup und der Anbindung an SimLoad Manager —, [XP BirdState](addon/scenery_addons/xp_birdstate.md) ergänzt Vogelschwärme mit offiziellem Linux-Build, und [Night Sky Fix](addon/scenery_addons/night_sky_fix.md) ersetzt den Sternkatalog für eine sichtbare Milchstraße
- [SimLoad Manager](addon/traffic/simloadmanager.md) ist jetzt ein natives Plugin mit eigenen Bodenfahrzeugen, Passagieren und Crew — ohne FlyWithLua und ohne SGES; die Seite ist nach Verkehr & Bodenbetrieb umgezogen

### 2026-08-27

- Die Übersichtsseiten der Sektionen tragen jetzt echten Orientierungstext statt eines Einzeilers — was die Sektion abdeckt, für wen, und in welcher Reihenfolge lesen: [Grundlagen](fundamentals/index.md), [Hilfsprogramme](linux/extensions/index.md), [Aufbau & Quellen](scenery/aufbau_quellen/index.md), [Orthofotografie](scenery/orthophotography/index.md), [Autogen](scenery/autogen/index.md), [Scripting](addon/scripting/index.md), [ToLiss Mods](addon/toliss/mods/index.md), [Sounds](addon/sounds/index.md), [Werkzeuge](addon/tools/index.md), [Verkehr & Bodenbetrieb](addon/traffic/index.md), [Szenerie-Plugins](addon/scenery_addons/index.md), [Via KVM](addon/kvm/index.md), [Wetter](flight_operations/weather/index.md), [Online](flight_operations/vatsim/index.md) und [Videos](videos.md). Dabei wurden einige Kurzbeschreibungen gegen die Detailseiten berichtigt — XRoads blendet Straßenpolygone auf Ortho-Kacheln aus statt Verkehr zu ergänzen, XOrganizer ist Windows-only, und unter X-Plane 12 ersetzt openSAM v5 das eigenständige AutoDGS
- [Easy Freighter](addon/toliss/mods/easy_freighter.md) erklärt jetzt, wie die Frachttür pro Livery geschaltet wird, und listet die Einrichtungsschritte
- Die [Videos](videos.md)-Seiten beschreiben jedes Video mit Dauer und Upload-Datum maschinenlesbar, sodass Suchmaschinen sie als Videoergebnisse anzeigen können
- Die Seitenleiste zeigt nur noch die aktive Sektion, was das Seitengewicht um rund 40 % senkt; die eingestellten Flughafen-Blogbeiträge wurden entfernt
