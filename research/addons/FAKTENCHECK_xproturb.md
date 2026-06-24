# Faktencheck: X-ProTurb — Professional Turbulence Engine (EN + DE)

**Datum:** 2026-06-24
**Geprüfte Seiten:** `docs/en/addon/flylua_scripts/xproturb.md`, `docs/de/addon/flylua_scripts/xproturb.md`
**Primärquelle:** forums.x-plane.org/files/file/100195 (WebFetch 403 — Inhalt über WebSearch rekonstruiert)

---

## Hinweis zur Quellenlage

Die x-plane.org-Forumsseite blockiert WebFetch (HTTP 403, siehe Memory). Der Beschreibungstext wurde über mehrere gezielte WebSearch-Abfragen rekonstruiert; die unten zitierten Passagen stammen aus den Suchergebnis-Auszügen des offiziellen Forum-Eintrags.

## Korrekt (bestätigt)

| # | Behauptung | Beleg (Zitat) |
|---|------------|---------------|
| 1 | Ersetzt XP12-Default-Turbulenz, basiert auf Level-D-Sim-Standards | „replaces X-Plane 12's generic shaking … built from the same standards used to qualify full-motion Level-D airline simulators" |
| 2 | Zwei gekoppelte Systeme (Atmosphäre + Flugzeug) | „models the atmosphere and the aircraft as two separate, physically-coupled systems" |
| 3 | Entwickler sfkcyl = Safak Cayli, Level-D-Sim-Entwickler | „associated with developer sfkcyl, who is noted as a Level D simulator developer" |
| 4 | Läuft unter FlyWithLua, kein Per-Aircraft-Setup | „It runs under FlyWithLua, installs in seconds … with zero per-aircraft setup" |
| 5 | Standards MIL-F-8785C, FAR 25.341 (Pratt), ICAO 9625 Level-D | „real certification math — MIL-F-8785C, FAA AC/FAR 25.341 (Pratt), ICAO 9625 (Level-D) — not tuned curves" |
| 6 | 6-DOF inkl. Heave, Sway, Surge | „full 6-DOF response with real vertical heave (elevator drop/lift), plus sway and surge" |
| 7 | Δn via FAR-25.341-Pratt-Formel, aus Geometrie gelesen | „per-aircraft load factor (Δn in g) via the FAR 25.341 Pratt formula, auto-read from the aircraft's geometry" |
| 8 | von Kármán / Dryden Spektren | „real atmospheric spectra using Dryden and von Kármán gust models" |
| 9 | CAT: Richardson-Zahl, tropopausen-fixiert, Kelvin-Helmholtz | „Richardson-number Clear-Air Turbulence, tropopause-locked CAT profile, and Kelvin-Helmholtz billows" |
| 10 | Mountain Wave: Queney, Rotor, Wave-Breaking, hydraulic jump, Scorer | „Queney lee waves, rotor zones, wave breaking, hydraulic jump (Boulder/Bora downslope windstorms) and the Scorer parameter" |
| 11 | CB/Storm: Kerne, Hagel, Starkregen, FAA-Bänder LIGHT→EXTREME | „CB cores, hail and heavy-rain turbulence scaled to proper FAA severity bands (LIGHT → EXTREME)" |
| 12 | Fly-by-Wire-Erkennung (Airbus) | „an Airbus is recognised and its own flight-control law is left to set the ride" |
| 13 | UI mit 5 Tabs, Aircraft-Recognition-Chip, Echtzeit-Readouts | „colour-coded panels across all five tabs; live aircraft-recognition chip (type + fly-by-wire/conventional); honest real-time readouts" |
| 14 | Kostenlos für privaten Gebrauch | „It is free for personal use" |

## Korrekturen gegenüber Erstentwurf

### 1. PDF-Handbuch (N/V → entfernt)
**Erstentwurf:** „a PDF manual is included."
**Befund:** In keiner Quelle belegbar. Ersetzt durch die belegte 5-Tab-UI-Beschreibung (#13).

### 2. Δn-Feature (präzisiert)
**Erstentwurf:** generische G-Kraft-Schwankung.
**Korrektur:** „via the FAR 25.341 Pratt formula, read automatically from each aircraft's geometry" (#7).

### 3. UI (präzisiert)
**Erstentwurf:** „live diagnostic UI".
**Korrektur:** „five colour-coded tabs … live aircraft-recognition chip" (#13).

## Nuancen

### N1. Plattformen
**Befund:** „Windows, macOS, Linux" nicht wörtlich genannt. Folgt aber zwingend aus der reinen FlyWithLua-Lua-Natur. Formuliert als „Windows, macOS, Linux (via FlyWithLua)".

### N2. Verwandter Eintrag
Es existiert ein vermutlich älterer/verwandter Forum-Eintrag „XPT_Turbulence" (file 100180) desselben Umfelds — nicht verlinkt, da X-ProTurb (100195) das beworbene Produkt ist.
