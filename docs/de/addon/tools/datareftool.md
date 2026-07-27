---
description: "DataRefTool (DRT) für X-Plane 12: DataRefs in Echtzeit durchsuchen, beobachten und bearbeiten. Unverzichtbar für Plugin-Entwicklung unter Linux."
---
# DataRefTool

DataRefTool (DRT) ist ein Entwicklungs- und Debugging-Werkzeug für [X-Plane](../../glossary.md#x-plane) 12, mit dem Datarefs durchsucht, beobachtet und bearbeitet sowie Commands ausgelöst werden können.

## Hintergrund

- **Entwickler:** Lee C. Baker
- **Website:** [datareftool.com](https://datareftool.com)
- **Lizenz:** v1 war Open Source (MIT, [GitHub](https://github.com/leecbaker/datareftool)); v2 ist Closed Source
- **Plattformen:** Windows, macOS, Linux (native Binaries)
- **Kompatibilität:** X-Plane 12.1+ (v2); X-Plane 10/11 (v1)

Das [Plugin](../../glossary.md#plugin) existiert seit X-Plane 10. Version 2 wurde als Closed-Source-Neuentwicklung für X-Plane 12 veröffentlicht und nutzt die Dataref-Enumerations-API (XPLM400) von X-Plane 12.04.

## Funktionsumfang

- **Dataref-Browser:** Alle Datarefs lesen, schreiben und durchsuchen (inkl. Arrays); Detailfenster stellen den Wertverlauf grafisch dar
- **Command-Browser:** Commands suchen und direkt ausführen
- **Änderungserkennung:** Datarefs hervorheben, die sich kürzlich geändert haben
- **Watch-Fenster und Befehlsverlauf:** Bestimmte Dataref-Werte in einem kompakten Panel überwachen; ein separates Befehlsverlauf-Fenster protokolliert Befehle, wenn sie ausgelöst werden
- **Regex-Suche:** Mehrere Suchbegriffe, reguläre Ausdrücke, Groß-/Kleinschreibung optional
- **Plugin-/Szenerie-Reload:** Neuladen direkt aus DRT anstoßen
- **Multi-Window:** Mehrere DRT-Fenster gleichzeitig möglich
- **Ignore-Liste:** `drt_ignore.txt` im Verzeichnis `Resources/plugins/` zum Ausschließen problematischer Datarefs

## Mehrwert in der Flugsimulation

DRT ist das Standardwerkzeug für Plugin-Entwicklung und Fehlersuche in X-Plane. Es ermöglicht die Echtzeitbeobachtung aller Datarefs, was bei der Analyse von Plugin-Konflikten oder der Entwicklung eigener FlyWithLua-Skripte unverzichtbar ist. Bei geöffneten Fenstern liest DRT jeden Frame die fensterrelevanten Datarefs, was die [FPS](../../glossary.md#fps-frames-per-second) reduzieren kann — bei geschlossenen Fenstern liegt der Performance-Einfluss bei null.

## Installation

**Download:** [datareftool.com/download](https://datareftool.com/download)

Die ZIP-Datei nach `Resources/plugins/` entpacken. Minimale Systemanforderung auf Linux: glibc 2.34 oder neuer (Debian 12 Bookworm und später). Es werden keine zusätzlichen Systempakete benötigt. Es sind keine Linux-spezifischen Probleme bekannt.

## Quellen

- [DataRefTool — Website](https://datareftool.com)
- [DataRefTool v1 — GitHub (archiviert)](https://github.com/leecbaker/datareftool)
