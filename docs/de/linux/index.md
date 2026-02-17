# Linux-Optimierungen für X-Plane

Linux bietet an jeder Schicht des Systems Stellschrauben, die X-Planes Laufzeitverhalten direkt beeinflussen — vom Kernel-Scheduler über den GPU-Treiber bis zum Display-Server. Im System-Bereich geht es um Latenz-Tuning: zwei Profile für verschiedene Kernel-Typen plus die passenden Monitoring-Tools zur Verifikation. Die Optimierungen behandeln die konkreten Komponenten — NVIDIA-Treiber, Liquorix-Kernel, X11 vs. Wayland und Dateisystem-Konfiguration. Für Windows-only Addons und Entwicklungswerkzeuge stehen KVM, Wine, Docker und Python-Umgebungen bereit.

- **[System](system/index.md)** — Tuning, Monitoring
- **[Optimierungen](optimizations/index.md)** — Treiber, Kernel, Display-Server, Dateisystem
- **[Erweiterungen](extensions/index.md)** — KVM, Docker, Wine, pyenv, zsh