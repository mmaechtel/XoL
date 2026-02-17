---
description: "Einrichtung und Diagnose von X-Plane 12 unter Linux: Konfigurationsunterschiede, Performance-Analyse mit Microprofiler und MangoHUD, CLI-Fehlerbehebung."
---
# Setup & Diagnose

Die Konfigurationsseite behandelt, was unter Linux anders ist: Vulkan als einzige Rendering-API, Zink als OpenGL-Übersetzungsschicht für Plugins, Shader-Caches, Mesa- und NVIDIA-Umgebungsvariablen, Audio unter PipeWire, Controller-Erkennung über evdev und udev-Regeln, sowie CLI-Diagnose von Safe Mode bis GDB-Backtrace. Die Performance-Seite ergänzt die Analyseperspektive — X-Planes interner Microprofiler identifiziert, ob CPU oder GPU den Frame limitiert, MangoHUD liefert den Frame-Time-Graphen als Vulkan-Overlay, und gezielte Diagnose-Workflows verbinden Symptome mit den passenden Linux-Tools.

- **[Konfiguration](config.md)** — Grafikeinstellungen, Rendering-Optionen und Linux-spezifische Anpassungen
- **[Performance](performance.md)** — FPS-Analyse, Engpass-Diagnose und Optimierungsstrategien
