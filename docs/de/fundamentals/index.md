---
title: "X-Plane-Grundlagen: CPU, I/O, Netzwerk"
description: "Wie X-Plane seine Last auf CPU, Storage-I/O und Netzwerk verteilt — die konkurrierenden Ressourcenanforderungen vor der Optimierung verstehen."
---
# Grundlagen

X-Plane verteilt seine Last auf drei Achsen — CPU, Speicher-I/O und Netzwerk —, die um gemeinsame Hardware-Ressourcen konkurrieren: CPU-Zyklen, Cache, Speicherbandbreite und PCIe-Lanes. Wo der Engpass liegt, wechselt je nach Flugphase und Konfiguration: Beim Laden der Szenerie dominiert der Speicher, im Flug die CPU, beim Ortho-Streaming das Netzwerk. Diese Sektion vermittelt das Denkmodell, das vor jeder einzelnen Einstellung stehen sollte — die folgenden Linux- und X-Plane-Kapitel setzen es voraus.

Einstieg sind die [Lastdimensionen](performance/performance_overview.md), die zeigen, wie die drei Achsen ineinandergreifen; danach folgt, warum [Latenz und Vorhersagbarkeit](performance/latency.md) mehr zählen als der FPS-Durchschnitt. Das Kapitel [CPU & RAM](performance/cpu_ram.md) erklärt den Main-Thread-Engpass und was Multi-Threading auslagern kann und was nicht; [GPU & VRAM](performance/gpu_vram.md) behandelt Texture Paging, Treiber-Unterschiede und Frame-Time-Perzentile. Wer nur praktische Tuning-Schritte sucht, kann direkt zu [System](../linux/system/index.md) springen — die dortigen Schritte bauen aber auf den hier eingeführten Begriffen auf.

- **[Performance](performance/index.md)** — CPU, GPU-Speicher und I/O: Lastdimensionen, Threading und VRAM-Analyse
