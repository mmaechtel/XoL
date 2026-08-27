---
title: "X-Plane-Scripting: FlyWithLua, XPPython3"
description: "FlyWithLua und XPPython3: die zwei Scripting-Frameworks für X-Plane 12 unter Linux. Lua für leichte Skripte, Python 3 für komplexe Plugins."
---
# Scripting

FlyWithLua und XPPython3 sind die beiden Scripting-Frameworks für X-Plane, und beide laufen nativ unter Linux. FlyWithLua nutzt Lua für schnelle, leichtgewichtige Skripte mit direktem DataRef-Zugriff, Dear-ImGui-Fenstern und FMOD-Audio — die Grundlage für die meisten Community-Skripte, darunter die in dieser Dokumentation gesammelten [FlyWithLua-Skripte](../flylua_scripts/index.md). XPPython3 kapselt das komplette X-Plane-SDK in Python 3, bringt einen eigenen Interpreter mit, liefert pip für Drittpakete und passt besser zu komplexen Plugins, die auf Python-Bibliotheken setzen.

Einstieg ist [FlyWithLua](flywithlua.md) — dort stehen Installation, der fehlende libglut-Symlink unter Debian Bookworm und die FMOD-Fehlermeldung bei bestimmten Flugzeugen, die alarmierend aussieht, das Plugin aber weiterlaufen lässt. [XPPython3](xppython3.md) folgt mit dem Debian-Abhängigkeits-Setup und den Plugins, die darauf aufbauen, etwa Follow the Greens. Beide Frameworks lassen sich in einer X-Plane-Installation parallel betreiben.

- **[FlyWithLua](flywithlua.md)** — Lua-basiertes Scripting-Framework
- **[XPPython3](xppython3.md)** — Python-3-Plugin-Framework
