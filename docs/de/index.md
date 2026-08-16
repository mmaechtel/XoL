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

### 2026-08-16

- Die [ToLiss Mods](addon/toliss/mods/index.md) sind jetzt eine eigene Sektion mit einer Seite pro Mod — [Easy Freighter](addon/toliss/mods/easy_freighter.md) und die [Carda Realistic Engine Mods](addon/toliss/mods/carda_engines.md) eingeschlossen
- Die beiden Flügel-Mods für die ToLiss-Airbusse haben eigene Seiten bekommen, [Durantula Wing Enhancement MOD](addon/toliss/mods/durantula_wing_mod.md) und [RealWings](addon/toliss/mods/realwings.md), statt zweier Abschnitte auf der Sammelseite — jeweils mit Entwickler, Download und Lizenz im Kopf, der vollständigen Installation über den nativen Linux-Installer samt nicht-interaktiver Aufrufe und dem Hinweis, warum die beiden Alternativen sind und nicht übereinander gehören
- Neue Seite [ToLiss Photon](addon/toliss/mods/toliss_photon.md): eine Beleuchtungsüberarbeitung für ToLiss A319, A320, A321 und A330-900, die jedes Außenlicht in den OBJ-Dateien des Flugzeugs neu anlegt und das Blinken von Beacon und Strobe an ein natives Plugin übergibt — ohne FlyWithLua und ohne XPPython3. Halogen, Xenon und LED lassen sich im Simulator umschalten und werden pro Livery gespeichert, die optionale Cockpitbeleuchtung von Gus Rodrigues kommt mit. Die Seite behandelt den Linux-Installer: den Ausweg bei schwarzem Fenster über Konsolen- oder Software-Rendering, die Abhängigkeit der Ordnerauswahl von `zenity`/`kdialog` und warum er nach den Wing-Mods und nach jedem ToLiss-Update erneut laufen muss

### 2026-08-12

- Neue Seite [AutoHaze](addon/flylua_scripts/autohaze.md): ein FlyWithLua-Skript, das den Standard-Dunst von X-Plane durch eine Trübung aus Satelliten-Aerosoldaten, Bodenwetter und realer Grenzschichthöhe ersetzt — oberhalb der METAR-Sichtobergrenze hat der Simulator nämlich keine Daten mehr und fällt auf einen festen, meist zu hohen Wert zurück. Linux-Unterstützung besteht ab Version 2.4; die Seite sammelt die Besonderheiten der Helper-Binary, die Behebung der SSL-Zertifikatsfehler und die Logdatei
- Neue Seite [Bay's Lighting Mod](addon/scenery_addons/bays_lighting_mod.md): eine komplette Überarbeitung der Flughafen-, Nacht- und Cockpitbeleuchtung samt Wolkenstreuung und Sichtweite. Die Seite erklärt, warum sich Nachtbeleuchtung und Ortho-Szenerien in die Quere kommen — Ortho entfernt die entfernte, eingebackene Lichtschicht, wodurch die Lichter rund ums Flugzeug abrupt enden, mit und ohne Mod

### 2026-08-04
- Adversarische Gegenprüfung der am 2026-08-03 überarbeiteten Seiten, mit mehreren Korrekturen. [Szenerie-Quellen](scenery/aufbau_quellen/scenery_sources.md): X-World Pro bringt ein eigenes Linux-Installationsskript mit, der Symlink von Hand betrifft also nur die freie Vegetations-Library — die bisherige Anleitung hätte zu einer defekten Pro-Installation geführt. [XPME](scenery/ortho_streaming/xpme.md) nennt sehr wohl eine Rückgabefrist. [Ortho4XP](scenery/orthophotography/ortho4xp.md): Die Option, Pisten der Geländekontur folgen zu lassen, entfiel mit X-Plane 11, nicht 12, der Sonny-Spiegel führt 0,5″-Kacheln auch für die Alpen, und die Forum-Links zeigen wieder auf das Ortho4XP-Forum
- Kleinere Präzisierungen auf denselben Seiten: `masking_mode` wählt einen Maskenalgorithmus und keine Textur, `road_level=1` enthält auch Trunk-Straßen, `custom_dem` braucht GDAL nur für Nicht-HGT-Raster, und [XPAIS Marine Traffic](addon/traffic/xpais_marine_traffic.md) hat nun die vollständige Konfiguration und Menüliste, den richtigen Rumpf-Fallback und die zwei Entwurfsentscheidungen nicht mehr als Grenzen aufgeführt
