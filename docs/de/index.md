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

### 2026-08-27

- Die Übersichtsseiten der Sektionen tragen jetzt echten Orientierungstext statt eines Einzeilers — was die Sektion abdeckt, für wen, und in welcher Reihenfolge lesen: [Grundlagen](fundamentals/index.md), [Hilfsprogramme](linux/extensions/index.md), [Aufbau & Quellen](scenery/aufbau_quellen/index.md), [Orthofotografie](scenery/orthophotography/index.md), [Autogen](scenery/autogen/index.md), [Scripting](addon/scripting/index.md), [ToLiss Mods](addon/toliss/mods/index.md), [Sounds](addon/sounds/index.md), [Werkzeuge](addon/tools/index.md), [Verkehr & Bodenbetrieb](addon/traffic/index.md), [Szenerie-Plugins](addon/scenery_addons/index.md), [Via KVM](addon/kvm/index.md), [Wetter](flight_operations/weather/index.md), [Online](flight_operations/vatsim/index.md) und [Videos](videos.md). Dabei wurden einige Kurzbeschreibungen gegen die Detailseiten berichtigt — XRoads blendet Straßenpolygone auf Ortho-Kacheln aus statt Verkehr zu ergänzen, XOrganizer ist Windows-only, und unter X-Plane 12 ersetzt openSAM v5 das eigenständige AutoDGS
- [Easy Freighter](addon/toliss/mods/easy_freighter.md) erklärt jetzt, wie die Frachttür pro Livery geschaltet wird, und listet die Einrichtungsschritte
- Die [Videos](videos.md)-Seiten beschreiben jedes Video mit Dauer und Upload-Datum maschinenlesbar, sodass Suchmaschinen sie als Videoergebnisse anzeigen können
- Die Seitenleiste zeigt nur noch die aktive Sektion, was das Seitengewicht um rund 40 % senkt; die eingestellten Flughafen-Blogbeiträge wurden entfernt

### 2026-08-21

- Die Seite [X-Plane WINCTRL Plugin](addon/tools/winctrl.md) wurde überarbeitet. Der Hersteller firmiert inzwischen als WINCTRL, deshalb ist „Winwing" aus der Dokumentation verschwunden; **WINCTRL** meint die Hardware, die Software heißt **X-Plane WINCTRL Plugin**. Der udev-Abschnitt empfiehlt jetzt den Debian-Tag `uaccess` statt `MODE="0666"` — samt der Falle, dass die Regeldatei `70-winctrl.rules` heißen muss, weil `99-*` nach `73-seat-late.rules` einsortiert und der Tag dann wirkungslos bleibt. Die Vendor-ID `4098` ist ein Hexadezimal-String (0x4098); der bisherige gegenteilige Hinweis war falsch. Neu: eigene FMC-Display-Schriften als `.xpwwf`-Dateien und der Vorrang von Tasten, die in X-Plane zugewiesen sind. Unterstützte Hardware und der Vergleich mit SimAppPro wurden korrigiert
- [X-Plane-Konfiguration](xplane/setup_diagnose/config.md#controller): neue Tabelle zur Unterscheidung der zwei Geräteklassen — Joysticks, Yokes und Schubhebel erledigt der Kernel, konfiguriert wird in X-Plane; Cockpitpanels legen dagegen einen Raw-HID-Knoten an, der root gehört, und brauchen udev-Regel plus Plugin

### 2026-08-17

- [AviTab](addon/cockpit/avitab.md): neuer Tipp, wie Little Navmap als Moving Map im AviTab Browser läuft — der eingebaute Webserver von Little Navmap liefert die Karte mit aktueller Flugzeugposition aufs Cockpit-Tablet, mit funktionierendem `config.ini`-Beispiel für Linux; die Seite [Little XpConnect](addon/tools/littlexpconnect.md) verweist darauf
