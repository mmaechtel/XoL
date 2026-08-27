---
title: Linux-Optimierungen für X-Plane
description: "Linux-Optimierungsebenen für X-Plane: NVIDIA-Treiber, Liquorix-Kernel, X11 vs. Wayland Display-Server und Dateisystem-I/O-Tuning."
---
# Optimierungen

Zwischen Kernel und Anwendung liegen mehrere Schichten, die X-Planes Rendering-Pipeline beeinflussen: GPU-Treiber, Scheduler, Display-Server und Dateisystem. Der NVIDIA-Treiber bringt Vulkan-Support und Kernel Mode Setting — bei Liquorix mit eigenen Header-Paketen. Der Liquorix-Kernel selbst ersetzt den Mainline-Scheduler durch PDS mit 1000-Hz-Timer und Full Preempt, reagiert damit viermal schneller auf Lastwechsel als der Stock-Kernel. X-Plane spricht kein Wayland nativ; in einer Wayland-Session läuft es über XWayland, was die Eingabelatenz gegenüber einer direkten X11-Session verdoppelt. Auf Dateisystem-Ebene profitiert X-Plane von NVMe-SSDs mit deaktiviertem Power-Saving und optimierten Mount-Optionen.

- **[Nvidia-Treiber](nvidia.md)** — Installation und Konfiguration für Vulkan-Performance
- **[Liquorix Kernel](liquorix.md)** — Low-Latency-Kernel für Echtzeit-Workloads
- **[Display-Server](displayserver.md)** — X11 vs. Wayland für X-Plane
- **[X11-Session](displayserver_x11.md)** — X11-spezifische Konfiguration
- **[Wayland-Session](displayserver_wayland.md)** — Wayland-spezifische Konfiguration
- **[Dateisystem](filesystem.md)** — Speicherstruktur und I/O-Optimierung
