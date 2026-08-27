---
title: Linux-System-Tuning für X-Plane
description: "Linux-System-Tuning für X-Plane: Zwei Kernel-Profile mit Fokus auf Latenz statt Durchsatz, plus Monitoring-Tools zur Verifikation jeder Einstellung."
---
# System

Latenz statt Durchsatz ist das Optimierungsziel für X-Plane unter Linux: ein stabiles Frametime-Budget zählt mehr als maximale Rechenleistung. Diese Sektion zeigt zwei Kernel-Profile — eines für den Standard-Kernel, eines für Liquorix — und die Monitoring-Werkzeuge, mit denen sich jede Tuning-Maßnahme verifizieren lässt.

- **[Warum Latenz zählt](latency.md)** — Video-Einführung und Tuning-Philosophie
- **[Kernel-Tuning](systemtuning.md)** — Kernel-Parameter, CPU-Governor, Interrupt-Affinität, NVMe-Tuning
- **[Swap & Speicherverwaltung](swap.md)** — Page Reclaim, Watermark-Tuning, Swap-Konfiguration, OOM-Prävention
- **[Monitoring](systemtools.md)** — btop, turbostat, perf, mpstat und weitere Analyse-Tools
- **[Fallstudie Tuning](tuning_casestudy.md)** — Gemessene Tuning-Schritte von Mikrorucklern zu stabilen Framezeiten
