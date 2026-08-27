---
title: "X-Plane 12: Vulkan, Audio, Controller"
description: "X-Plane 12 unter Linux: Vulkan-Rendering, Zink für Plugins, Shader-Caches, PipeWire-Audio, Controller-Einrichtung und GPU-Fehlersuche."
---
# X-Plane unter Linux

X-Plane 12 nutzt Vulkan als einzige Rendering-API — die meisten Grafikeinstellungen sind plattformübergreifend identisch, aber unter Linux kommen Besonderheiten hinzu: Zink als OpenGL-Brücke für Plugins, Mesa-Shader-Caches, PipeWire-Audio und Controller-Erkennung über evdev. Setup & Diagnose deckt die Konfiguration und Performance-Analyse ab — vom Microprofiler über MangoHUD bis zu reproduzierbaren Benchmarks per CLI. Die Fehlerdiagnose behandelt GPU Device Losses, Safe-Mode-Optionen und Subsystem-Isolierung für systematisches Troubleshooting.

- **[Setup & Diagnose](setup_diagnose/index.md)** — Konfiguration, Performance-Analyse und CLI-Diagnose
- **[Systemfehler](systemfehler/index.md)** — GPU-Crashes, Device Losses und systematische Fehlersuche
