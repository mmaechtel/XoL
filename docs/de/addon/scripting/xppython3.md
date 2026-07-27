---
description: "XPPython3 Python-3-Plugin-Framework für X-Plane 12 unter Linux: voller SDK-Zugriff, integriertes pip, Dear ImGui-UI und Debian-Abhängigkeiten."
---
# XPPython3

XPPython3 ist eine Python-3-Scripting-Engine für [X-Plane](../../glossary.md#x-plane) 12, die das komplette X-Plane SDK in Python verfügbar macht und so Python-Plugins neben nativen C/C++-Plugins ausführt.

## Hintergrund

- **Entwickler:** Peter Buckner (AvnWx.com), initialer Python-3-Port von Michal (uglyDwarf)
- **Dokumentation:** [xppython3.readthedocs.io](https://xppython3.readthedocs.io/en/latest/)
- **Projekt-Heimat:** [xppython3.readthedocs.io](https://xppython3.readthedocs.io/en/latest/) (Legacy-Python-3-Port: [github.com/uglyDwarf/x-plane_plugins](https://github.com/uglyDwarf/x-plane_plugins))
- **Plattformen:** Windows, macOS, Linux (native Binaries)
- **Kompatibilität:** X-Plane 12 (v4.x); X-Plane 11.50+ (Legacy v3.1.5)

XPPython3 ist der Nachfolger von Sandy Barbours PythonInterface (nur Python 2). Die aktuelle v4.x-Linie bündelt Python 3.12 intern — keine systemweite Python-Installation nötig.

## Funktionsumfang

- **Volle SDK-Abdeckung:** Alle X-Plane-SDK-Module aus Python zugänglich (Datarefs, Commands, Display, Menüs, Kamera, Navigation, Szenerie, Sound, Wetter)
- **Dear ImGui-Integration:** Moderne UI-Fenster über das `xp_imgui`-Modul
- **Integriertes pip:** Python-Pakete (numpy, Pillow, requests) direkt aus X-Plane installieren
- **Plugin-Typen:** Globale, flugzeug- und szenerie-spezifische Python-Plugins
- **Hot Reload:** Alle Python-Plugins neu laden, ohne X-Plane neu zu starten
- **Integrierter Updater:** Prüft über das Plugins-Menü auf neue XPPython3-Versionen
- **Kompilierte Plugins:** Unterstützung für `.pyc`- und verschlüsselte `.xpyce`-Dateien für kommerzielle Verbreitung

## Mehrwert in der Flugsimulation

XPPython3 öffnet das X-Plane SDK für das Python-Ökosystem — Entwickler können Standard-Python-Bibliotheken, pip-Pakete und vertraute Debugging-Werkzeuge einsetzen. Plugins wie [Follow the Greens](../traffic/followthegreens.md) und XP-NOAA-Weather setzen es voraus. Das Plugin-Ökosystem ist kleiner als das Lua-basierte von [FlyWithLua](flywithlua.md), aber XPPython3 bedient Entwickler, die Python bevorzugen, und Projekte, die von Pythons Bibliotheks-Ökosystem profitieren.

## Installation

**Download:** [xppython3.readthedocs.io](https://xppython3.readthedocs.io/en/latest/usage/installation_plugin.html) — `xp3-linux.zip` (Stable) oder `xp3-linuxb.zip` (Beta) herunterladen.

Die ZIP-Datei nach `Resources/plugins/` entpacken. Es entsteht folgende Verzeichnisstruktur:

```
Resources/plugins/XPPython3/
    lin_x64/
        XPPython3.xpl
        python3.12/
```

Beim ersten Start legt das [Plugin](../../glossary.md#plugin) automatisch `Resources/plugins/PythonPlugins/` an, in dem Python-Plugins von Drittanbietern abgelegt werden.

### Abhängigkeiten auf Debian/Ubuntu

```bash
sudo apt install libexpat1 libbsd0
```

Die Pakete `zlib1g` und `libc6` gehören zur Standard-Installation unter Debian/Ubuntu.

### Plugin lädt nicht

Wenn XPPython3 nicht im Plugins-Menü erscheint und keine Ausgabe in `Log.txt` erzeugt, ist eine fehlende Shared Library die häufigste Ursache. Diagnose mit:

```bash
ldd Resources/plugins/XPPython3/lin_x64/XPPython3.xpl
```

Jede Zeile mit `not found` zeigt eine fehlende Abhängigkeit an.

## Quellen

- [XPPython3 Dokumentation — xppython3.readthedocs.io](https://xppython3.readthedocs.io/en/latest/)
- [XPPython3 Quellcode — GitHub](https://github.com/pbuckner/x-plane_plugins)
- [XPPython3 v4.6.1 Released — forums.x-plane.org](https://forums.x-plane.org/forums/topic/338833-xppython3-v461-released/)
