# XoL Content Audit — Status

Lebende Statusdatei für den Content-Audit. Wird über mehrere Audit-Zyklen hinweg geführt.
Prozess-Definition: siehe `AUDIT_FLOW.md`.

---

## Aktueller Zyklus

**Gestartet:** 2026-02-12
**Runde:** 1
**Nächstes Kapitel:** #4 `linux/system/systemtuning.md`

---

## Fortschritts-Tracker

Nach jedem abgeschlossenen Schritt: Feld mit Datum füllen.

| # | Datei | Zeilen | Deep Analysis | Expert Review | User-Review | Korrekturen | Note |
|---|-------|--------|:---:|:---:|:---:|:---:|:---:|
| | **Runde 1 — Kern-Dokumentation** | | | | | | |
| 1 | `begin.md` | 228 | 2026-02-13 | 2026-02-13 | 2026-02-13 | 2026-02-13 | C |
| 2 | `linux/optimizations/nvidia.md` | 164 | 2026-02-14 | 2026-02-14 | 2026-02-14 | 2026-02-14 | C |
| 3 | `linux/optimizations/liquorix.md` | 139 | 2026-02-15 | 2026-02-15 | 2026-02-15 | 2026-02-15 | D |
| 4 | `linux/system/systemtuning.md` | 441 | | | | | |
| 5 | `linux/system/systemtools.md` | 421 | 2026-02-14 | 2026-02-14 | 2026-02-14 | 2026-02-14 | B |
| 6 | `linux/optimizations/filesystem.md` | 160 | | | | | |
| 7 | `xplane/setup_diagnose/performance.md` | 206 | | | | | |
| — | **DE-Angleichung R1** | | | | | | |
| | **Runde 2 — Kurzcheck** | | | | | | |
| 8 | `xplane/setup_diagnose/config.md` | 335 | | | | | |
| 9 | `linux/optimizations/displayserver.md` | 155 | | | | | |
| 10 | `linux/optimizations/displayserver_x11.md` | 139 | | | | | |
| 11 | `linux/optimizations/displayserver_wayland.md` | 141 | | | | | |
| — | **DE-Angleichung R2** | | | | | | |
| | **Runde 3 — Scenery & Addons** | | | | | | |
| 12 | `scenery/aufbau_quellen/scenery_components.md` | 163 | 2026-02-16 | 2026-02-16 | 2026-02-16 | 2026-02-16 | C |
| 13 | `scenery/orthophotography/ortho4xp.md` | 221 | | | | | |
| 14 | `scenery/ortho_streaming/autoortho.md` | 242 | | | | | |
| 15 | `scenery/ortho_streaming/xearthlayer.md` | 133 | | | | | |
| 16 | `scenery/ortho_streaming/static_plus_streaming.md` | 109 | | | | | |
| — | **DE-Angleichung R3** | | | | | | |
| | **Runde 4 — Peripherie** | | | | | | |
| 17 | `linux/extensions/kvm.md` | 90 | | | | | |
| 18 | `linux/extensions/docker.md` | 102 | | | | | |
| 19 | `linux/extensions/wine.md` | 95 | | | | | |
| 20 | `addon/tools/xorganizer.md` | 95 | | | | | |
| 21 | `linux/extensions/pyenv.md` | 161 | | | | | |
| 22 | `linux/extensions/zsh.md` | 82 | | | | | |
| — | **DE-Angleichung R4** | | | | | | |
| | **Runde 5 — Flight Ops & Referenz** | | | | | | |
| 23 | `flight_operations/weather/briefing.md` | 120 | | | | | |
| 24 | `flight_operations/atc/clearance.md` | 62 | | | | | |
| 25 | `flight_operations/vatsim/vatsim.md` | 41 | | | | | |
| 26 | `glossary.md` | 150 | | | | | |
| 27 | `intro.md` | 76 | | | | | |
| — | **DE-Angleichung R5** | | | | | | |

---

## Nicht im Audit

| Datei | Grund |
|-------|-------|
| `index.md` | Changelog, kein Inhalt |
| `linux/index.md` | Übersichtsseite |
| `xplane/systemfehler/index.md` | Stub |
| `xplane/systemfehler/geraeteverluste.md` | Stub |
| `scenery/aufbau_quellen/scenery_sources.md` | Stub |
| `scenery/orthophotography/orthophotography_intro.md` | Stub |
| `addon/scenery_addons/xroad.md` | Stub |
| `addon/scenery_addons/aep.md` | Stub |
| `flight_operations/index.md` | Übersichtsseite |
| `about.md` | Meta-Seite |
| `Maps.md` | Karten-Embed |

---

## Ausstehende Aufnahme

Seit Erstellung des Audit-Plans sind zahlreiche neue Seiten hinzugekommen, die noch nicht im Fortschritts-Tracker stehen. Einsortierung in passende Runden nach Abschluss von Runde 1.

- `fundamentals/performance/` — performance_overview.md, latency.md, cpu_ram.md, gpu_vram.md
- `linux/system/latency.md` — Video-Einstieg
- `addon/toliss/` — toliss_ecosystem.md, toliss_mods.md
- `addon/cockpit/` — kabinxp.md, linuxtrack.md, terrainradar.md
- `addon/flylua_scripts/` — sges.md
- `addon/scenery_addons/` — lst.md, noaa_weather.md
- `addon/tools/` — xlinspeak.md, winctrl.md
- `addon/kvm/` — mobiflight.md, sayintentions.md
- `addon/sounds/` — kosp_project.md, mango_studios.md
- `addon/scripting/` — flywithlua.md
- `flight_operations/atc/` — pushback_taxi.md, takeoff.md, departure.md, enroute.md, approach.md, landing.md
- `scenery/aufbau_quellen/scenery_sources.md`

---

## Abgeschlossene Zyklen

_Hier werden nach Abschluss eines vollständigen Audit-Durchlaufs die Ergebnisse zusammengefasst._

<!-- Template für abgeschlossenen Zyklus:

### Zyklus YYYY-MM — YYYY-MM

| Kennzahl | Wert |
|----------|------|
| Kapitel auditiert | /27 |
| Gesamtnoten | A: , B: , C: , D: |
| FAIL-Findings gesamt | |
| WARN-Findings gesamt | |
| Korrekturen umgesetzt | |
| DE-Angleichungen | /5 Runden |

-->
