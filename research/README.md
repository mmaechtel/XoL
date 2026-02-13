# XoL Research Repository

**Erstellt:** 2026-02-13
**Zweck:** Wissensbasis für `docs/en/` Dokumentation (X-Plane on Linux)

---

## Struktur

```
research/
├── xplane-config/          # 4 Dateien: Konfiguration, Grafik, Performance-Profile, Lektorat
├── display-server/         # 5 Dateien: Wayland, X11, Gaming-Vergleich, Lektorat, Faktencheck
├── systemtools/            # 5 Dateien: CPU, I/O, Interrupts, Combined, Lektorat
├── systemtuning/           # 2 Dateien: Latenzreduktion, Desktop-Workloads
├── audio/                  # 1 Datei: PipeWire/PulseAudio, FMOD, Controller
├── szenerie/               # 1 Datei: Ortho-Cache-Verhalten
├── addons/                 # 1 Datei: XOrganizer unter Wine
├── notebooklm/             # 2 Dateien: TTS-Skripte für NotebookLM Audio Overview
├── analyses/               # Persistierte Skill-Ergebnisse
└── INDEX.md                # Relevanz-Mapping: Research -> Docs-Seiten
```

**Total:** 21 Research-Dateien + 5 Prozess-/Tracker-Dateien

Siehe `INDEX.md` für das Relevanz-Mapping zu den einzelnen Docs-Seiten.

---

## Inhalte

### X-Plane Konfiguration
- [XPlane12_Konfiguration_Linux_Spezifika.md](xplane-config/XPlane12_Konfiguration_Linux_Spezifika.md) — Linux-spezifische Konfiguration (Vulkan, Shader-Cache, Mesa, Audio, Controller)
- [Grafikeinstellungen_XPlane12_Technische_Grundlagen.md](xplane-config/Grafikeinstellungen_XPlane12_Technische_Grundlagen.md) — Rendering-Architektur, Vulkan/Zink, Einstellungsparameter
- [XPlane12_Einstellungsprofile_Linux_Performance.md](xplane-config/XPlane12_Einstellungsprofile_Linux_Performance.md) — Einstellungsprofile nach GPU-Klasse, Linux-Performance
- [LEKTORAT_config_md.md](xplane-config/LEKTORAT_config_md.md) — Redaktionelle Bewertung für config.md

### Display-Server
- [wayland_display_server.md](display-server/wayland_display_server.md) — Konsolidiertes Paper: Architektur, Kompatibilität, Performance
- [wayland_vs_x11.md](display-server/wayland_vs_x11.md) — X-Plane-Kompatibilität Wayland vs. X11
- [wayland_vs_x11_gaming.md](display-server/wayland_vs_x11_gaming.md) — Performance/Latenz-Vergleich Gaming
- [LEKTORAT_wayland.md](display-server/LEKTORAT_wayland.md) — Redaktionelle Bewertung und Gliederungsplan
- [FAKTENCHECK_displayserver.md](display-server/FAKTENCHECK_displayserver.md) — 6 Fehler, 4 Nuancen, 17 korrekt

### Systemtools
- [cpu_monitoring_tools.md](systemtools/cpu_monitoring_tools.md) — htop, btop, cpupower, s-tui, turbostat, mpstat
- [io_monitoring_tools.md](systemtools/io_monitoring_tools.md) — iotop, iostat, ioping, nvme-cli
- [interrupt_monitoring_tools.md](systemtools/interrupt_monitoring_tools.md) — /proc/interrupts, irqtop, lsirq, IRQ-Shielding
- [Linux_Monitoring_Tools_Combined.md](systemtools/Linux_Monitoring_Tools_Combined.md) — All-in-one Dashboards: glances, nmon, powertop
- [LEKTORAT_systemtools.md](systemtools/LEKTORAT_systemtools.md) — Redaktionelle Bewertung und Gliederungsplan

### Systemtuning
- [Empfohlene Systemkonfigurationen zur Latenzreduktion unter Linux](systemtuning/Empfohlene%20Systemkonfigurationen%20zur%20Latenzreduktion%20unter%20Linux) — Systemkonfigurationen für niedrige Latenz
- [Systemlatenz unter Linux-Desktop-Workloads](systemtuning/Systemlatenz%20unter%20Linux-Desktop-Workloads) — Desktop-Latenz-Analyse

### Audio
- [Audio_Controller_Debugging_XPlane12.md](audio/Audio_Controller_Debugging_XPlane12.md) — PipeWire/PulseAudio, FMOD, Controller, Debugging

### Szenerie
- [Cache-Verhalten_Orthoszenerie_XPlane.md](szenerie/Cache-Verhalten_Orthoszenerie_XPlane.md) — Ortho4XP vs. AutoOrtho Cache-Verhalten

### Addons
- [XOrganizer_Wine_Linux.md](addons/XOrganizer_Wine_Linux.md) — XOrganizer unter Wine, .NET-Abhängigkeiten, Alternativen
- [xearthlayer-cpu-settings.md](xearthlayer-cpu-settings.md) — CPU-Tuning-Einstellungen für xEarthLayer

### NotebookLM
- [NOTEBOOKLM_display-server_qa.md](notebooklm/NOTEBOOKLM_display-server_qa.md) — TTS-Skript: Display-Server Q&A
- [NOTEBOOKLM_scenery-ini_summary.md](notebooklm/NOTEBOOKLM_scenery-ini_summary.md) — TTS-Skript: scenery_packs.ini Zusammenfassung

### Prozess-Dateien
- [AUDIT_FLOW.md](AUDIT_FLOW.md) — Content-Audit Prozess (Flow, Template, Regeln, QS)
- [AUDIT_STATUS.md](AUDIT_STATUS.md) — Audit-Fortschritt + Zyklushistorie
- [VIDEO_STATUS.md](VIDEO_STATUS.md) — Tracker: welches Video wo eingebettet ist

---

**Letzte Aktualisierung:** 2026-02-13
