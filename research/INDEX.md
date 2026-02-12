# Research — Index

Thematische Übersicht aller Research-Papers und Lektorate.
Status-Referenz: siehe [`TODO.md`](../TODO.md)

---

## xplane-config/

X-Plane Konfiguration, Grafikeinstellungen, Performance-Profile.
**Zielseite:** `xplane/config.md` | **Status:** geprüft

| Datei | Typ | Inhalt |
|-------|-----|--------|
| `XPlane12_Konfiguration_Linux_Spezifika.md` | Research | Linux-spezifische Konfiguration (Vulkan, Shader-Cache, Mesa, Audio, Controller) |
| `Grafikeinstellungen_XPlane12_Technische_Grundlagen.md` | Research | Rendering-Architektur, Vulkan/Zink, Einstellungsparameter |
| `XPlane12_Einstellungsprofile_Linux_Performance.md` | Research | Einstellungsprofile nach GPU-Klasse, Linux-Performance |
| `LEKTORAT_config_md.md` | Lektorat | Redaktionelle Bewertung für config.md-Umsetzung |
| `xplane-help.out` | Referenz | X-Plane CLI-Hilfe-Ausgabe |

---

## display-server/

Wayland, X11, XWayland — Display-Server-Wahl für X-Plane.
**Zielseiten:** `displayserver.md`, `displayserver_wayland.md`, `displayserver_x11.md` | **Status:** geprüft

| Datei | Typ | Inhalt |
|-------|-----|--------|
| `wayland_display_server.md` | Research | Konsolidiertes Paper: Architektur, Kompatibilität, Performance |
| `wayland_vs_x11.md` | Rohdaten | X-Plane-Kompatibilität Wayland vs. X11 |
| `wayland_vs_x11_gaming.md` | Rohdaten | Performance/Latenz-Vergleich Gaming |
| `LEKTORAT_wayland.md` | Lektorat | Redaktionelle Bewertung und Gliederungsplan |
| `FAKTENCHECK_displayserver.md` | Faktencheck | 6 Fehler, 4 Nuancen, 17 korrekt — Korrekturen eingearbeitet |

---

## systemtools/

Linux-Monitoring-Tools für Performance-Analyse.
**Zielseite:** `systemtools.md` | **Status:** umgesetzt

| Datei | Typ | Inhalt |
|-------|-----|--------|
| `cpu_monitoring_tools.md` | Research | htop, btop, cpupower, s-tui, turbostat, mpstat |
| `io_monitoring_tools.md` | Research | iotop, iostat, ioping, nvme-cli |
| `interrupt_monitoring_tools.md` | Research | /proc/interrupts, irqtop, lsirq, IRQ-Shielding |
| `Linux_Monitoring_Tools_Combined.md` | Research | All-in-one Dashboards: glances, nmon, powertop |
| `LEKTORAT_systemtools.md` | Lektorat | Redaktionelle Bewertung und Gliederungsplan |

---

## systemtuning/

Kernel-Tuning, Latenzreduktion, CPU-Governor.
**Zielseite:** `systemtuning.md` | **Status:** umgesetzt (Korrekturen offen)

| Datei | Typ | Inhalt |
|-------|-----|--------|
| `Empfohlene Systemkonfigurationen zur Latenzreduktion unter Linux` | Research | Systemkonfigurationen für niedrige Latenz |
| `Systemlatenz unter Linux-Desktop-Workloads` | Research | Desktop-Latenz-Analyse |

---

## audio/

Audio-Konfiguration, Controller, Debugging.
**Zielseite:** `audio.md` | **Status:** offen

| Datei | Typ | Inhalt |
|-------|-----|--------|
| `Audio_Controller_Debugging_XPlane12.md` | Research | PipeWire/PulseAudio, FMOD, Controller, Debugging |

---

## szenerie/

Szenerie-Management, Ortho-Systeme, Cache-Verhalten.
**Zielseite:** — (kein eigener TODO-Eintrag)

| Datei | Typ | Inhalt |
|-------|-----|--------|
| `Cache-Verhalten_Orthoszenerie_XPlane.md` | Research | Ortho4XP vs. AutoOrtho Cache-Verhalten |

---

## addons/

Externe Tools und Wine-basierte Addons.
**Zielseite:** `addon/xorganizer.md` | **Status:** offen

| Datei | Typ | Inhalt |
|-------|-----|--------|
| `XOrganizer_Wine_Linux.md` | Research | XOrganizer unter Wine, .NET-Abhängigkeiten, Alternativen |

---

## Audit

Content-Audit des gesamten EN-Books auf Faktenrichtigkeit, Aktualität, Relevanz, Detailgrad.

| Datei | Typ | Inhalt |
|-------|-----|--------|
| `AUDIT_FLOW.md` | Prozess | Flow, Tabellen-Template, Regeln, QS (ändert sich selten) |
| `AUDIT_STATUS.md` | Status | Fortschritts-Tracker, Zyklushistorie (lebende Datei) |

Audit-Ergebnisse pro Kapitel werden in den jeweiligen Kategorie-Ordnern als `AUDIT_<dateiname>.md` abgelegt.

---

## Sonstige (Root)

| Datei | Typ | Inhalt |
|-------|-----|--------|
| `IMPORTANT_TO_FIX.txt` | Notizen | Ursprüngliche Korrekturhinweise (vollständig migriert nach `TODO.md` — kann entfernt werden) |
