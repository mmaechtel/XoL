# Analyse Run O — LEMD → EDDM (2026-02-25)

**Route:** LEMD (Madrid-Barajas) → EDDM (München), ~1.500 km, FL330, Überflug Pyrenäen/Alpen
**Dauer:** 92 Min (5.531s), 26.212 Telemetrie-Samples @ 5 Hz
**Config:** Änderung 11 (threads=6) + **Änderung 12** (max_concurrent_tasks=48, network_concurrent=48, max_tiles_per_cycle=80)
**Mid-flight:** generation.threads 6→4 (nach ~40 Min)
**Besonderheit:** Erster Run nach Circuit-Breaker-Tuning. Absturz beim ersten Versuch (Pop-Out-Fenster → gamescope-Crash, bekanntes Problem). Zweiter Versuch sauber.

---

## 1. FPS-Profil

| Metrik | Run N | **Run O** | Trend |
|--------|-------|-----------|-------|
| FPS Median | 29,9 | **29,7** | = |
| FPS Mean | 30,9 | **29,4** | ~ |
| FPS Min | 0,0 | **19,9** | ↑ (keine Pausen) |
| FPS Max | 84,0 | **74** | ~ |
| FPS < 25 (gesamt) | 6,4% | **2,5%** | **↓↓↓** |
| FPS P5 | — | **26** | — |
| FPS P95 | — | **31** | — |

**Timing Baseline:** CPU P50=16,9ms, GPU P50=16,6ms, CPU P95=20,0ms, GPU P95=29,3ms.
GPU Time Max = 132ms (kein Artefakt wie Run N, normaler Shader-Compile-Spike).

### Stutter-Budget

| Phase | Events | Dauer | Anteil |
|-------|--------|-------|--------|
| Gate (Airport laden) | 5 | ~6s | GPU-getrieben, normal |
| Takeoff | **0** | **0s** | **ELIMINIERT** (Run N: 57s) |
| Climb | 1 | 9,2s | DSF-Crossing, kein XEL |
| Cruise | 12 | ~12s Cluster | Kurze Dips, kein sustained |
| Approach EDDM | 3 | 6,2s | Compound, deutlich kürzer |
| Gate EDDM | 2 | ~4s | GPU-getrieben, normal |

**Bewertung:** 97,5% der Flugzeit über 25 FPS. Takeoff-Stutter eliminiert. Approach von 61s auf 6,2s reduziert.

---

## 2. Degradation Events (25 Gesamt, davon 20 > 0,5s)

| Event | t (min) | Dauer | FPS min | AGL | GS | CPU avg | GPU avg | BN | Kategorie |
|-------|---------|-------|---------|-----|-----|---------|---------|-----|-----------|
| E00–E04 | 8,9–9,5 | 0,6–2,7s | 20–24 | 0m | 0 | 8–11ms | 31–34ms | GPU | E-GPU (Airport) |
| **E05** | **22,5** | **9,2s** | **20** | **3125m** | **309** | **33ms** | **17ms** | **CPU** | **B-DSF** |
| E06 | 30,0 | 0,8s | 20 | 8434m | 410 | 25ms | 25ms | BAL | C-Memory |
| **E07–E12** | **34,2–34,4** | **0,5–3,7s** | **20** | **10k m** | **438** | **29–33ms** | **15–18ms** | **CPU** | **D-Compound** |
| E13 | 49,9 | 0,7s | 20 | 10394m | 443 | 28ms | 20ms | CPU | A-XEL-CPU |
| E14–E18 | 52,1–52,4 | 0,5–1,0s | 20 | 10,2–10,3k | 443 | 28–31ms | 18–21ms | CPU/BAL | A-XEL-CPU/C-Memory |
| **E19** | **67,3** | **0,7s** | **20** | **5027m** | **383** | **33ms** | **16ms** | **CPU** | **D-Compound** |
| **E20–E22** | **79,3–79,4** | **0,7–6,2s** | **20** | **163–192m** | **133** | **30–32ms** | **19–20ms** | **CPU** | **D-Compound** |
| E23–E24 | 91,2 | 0,8–3,0s | 20 | 0m | 0 | 15–19ms | 31–35ms | GPU | E-GPU (Airport) |

---

## 3. Event E05 — Climb (9,2s)

**Telemetrie:** AGL 3125m, GS 309 kts, FPS 20 für 9,2s. CPU-dominiert (33ms vs 17ms GPU).
**XEL:** Nur 49% CPU, 203 Threads, 6843 MB RSS — **kein Thread-Bomb!**
**vmstat:** 0 allocstalls, pgfaults 170k/s (moderat). Null Memory Pressure.
**Reclaim Traces:** 0 Events.

**Diagnose:** Reines DSF-Boundary-Crossing (Pyrenäen-Überflug). X-Plane lädt neue DSF-Tiles synchron auf Main Thread. XEL ist dabei **idle**. Das Circuit-Breaker-Tuning hat hier keinen Effekt — das Problem liegt in X-Plane.

**Vergleich Run N:** Dort war der Climb bereits Thread-Bomb (547 Threads). Hier nur 203 — Änderung 12 wirkt.

---

## 4. Events E07–E12 — Cruise FL330 (Cluster, 34,2–34,4 min)

**Telemetrie:** FL330, GS 438 kts. 6 Events in 20s, längster 3,7s.
**XEL:** 1057% CPU, 379 Threads, 13 GB RSS — **Thread-Burst aber kurz**.
**vmstat:** allocstalls **4195/s** Peak, pgfaults 1,6M/s, pgscan_direct 305k/s, kswapd 952k/s, pswpout 124k/s.

**Diagnose:** D-Compound — XEL-Burst + Memory Pressure gleichzeitig. Aber: **Dauer 3,7s statt 57s (Run N Takeoff) oder 61s (Run N Approach)**. Der Circuit Breaker hat die Burst-Dauer drastisch verkürzt. Die Pools (48 statt 128) werden schnell voll → CB trips → Prefetch pausiert → System erholt sich.

---

## 5. Events E20–E22 — Approach EDDM (6,2s)

**Telemetrie:** AGL 163–192m, GS 133 kts, FPS 20 für 6,2s. CPU-dominiert.
**XEL:** 1070% CPU, 285 Threads, 13,7 GB RSS.
**vmstat:** allocstalls 400/s, pgfaults 1,8M/s, pgscan_direct 25k/s, kswapd 420k/s.
**Reclaim Traces:** 0 im Fenster (Traces vermutlich unter anderer Zeitgrenze).

**Diagnose:** D-Compound (Approach-typisch), aber **6,2s statt 61s in Run N**. Der Dreifach-Problem-Mechanismus (DSF + XEL + Memory) ist noch da, aber die Burst-Dauer ist durch die Pool-Verkleinerung drastisch reduziert.

---

## 6. Systemmetriken (Gesamt)

| Metrik | Run N | **Run O** | Trend |
|--------|-------|-----------|-------|
| RAM Peak | — | **52 GB** used | — |
| Swap Peak | — | **14,5 GB** | — |
| VRAM Peak | 20,1 GB (82%) | **21,3 GB (87%)** | ~ (längerer Flug) |
| allocstalls (Sekunden > 0) | ~14s | **93s** | ↑ |
| allocstalls total | — | **118.439** | — |
| allocstall max/s | 6.948 | **10.341** | ↑ |
| XEL CPU P50 / P95 / max | — | 1% / 158% / **1218%** | — |
| XEL Threads P50 / max | — | 38 / **547** | — |
| XEL RSS max | 15,4 GB | **15,1 GB** | = |
| Trace Reclaim Events | 13.338 | **127.874** | ↑ (längerer Flug) |
| Trace IO Slow | 44 | **28.099** | ↑ |
| XEL CPU > 500% | — | 3,4% der Zeit | — |

**Anmerkung allocstalls:** Die Gesamtzahl ist höher als Run N, aber die **Auswirkung** ist dramatisch geringer. In Run N konzentrierten sich Stalls auf 2 Mega-Events (57s + 61s = 118s Stutter). In Run O verteilen sie sich auf kurze Bursts (max 3,7s). Das System erholt sich schnell dank CB-Intervention.

---

## 7. Bewertung Änderung 12 (Circuit Breaker scharf stellen)

| Aspekt | Vorher (Run N) | Nachher (Run O) | Bewertung |
|--------|----------------|-----------------|-----------|
| Takeoff-Stutter | **57s** | **0s** | **ELIMINIERT** |
| Approach-Stutter | **61s** | **6,2s** | **-90%** |
| Max Event-Dauer | 61s | **9,2s** (DSF, nicht XEL) | **-85%** |
| FPS < 25 | ~8% | **2,5%** | **-69%** |
| CB-Wirksamkeit | Zahnlos (Pools zu groß) | **Greift rechtzeitig** | Ziel erreicht |
| Thread-Max | 547 | 547 (unverändert) | Pool limitiert Dauer, nicht Threads |

**Fazit:** Die Pool-Verkleinerung (128→48) ist der bisher wirksamste einzelne Tuning-Schritt gegen FPS-Stutter. Der CB konnte vorher nie rechtzeitig auslösen — jetzt greift er nach dem ersten Batch und begrenzt die Burst-Dauer.

---

## 8. Tuning-Empfehlungen

### Bereits wirksam (behalten)
- `max_concurrent_tasks = 48` — Haupthebel, CB-Schärfung
- `network_concurrent = 48`
- `max_tiles_per_cycle = 80`
- `generation.threads = 6` (mid-flight auf 4, kein messbarer Unterschied)
- `max_concurrent_jobs = 4`, `memory_size = 4 GB`

### Nächste Kandidaten (Änderung 13+)

1. **`max_concurrent_tasks` weiter auf 32** — E07-E12 zeigt noch 4195 allocstalls/s bei 48. Mit 32 würde der CB noch früher greifen. Risiko: Prefetch wird bei DSF-Crossings zu langsam → kurze Texture-Gaps.

2. **`max_concurrent_jobs` 4→2** — Weniger parallele DDS-Jobs = weniger gleichzeitige CPU-Arbeit. Konservativer Schritt, aber möglicherweise merkbar bei Tile-Ladezeiten.

3. **`generation.threads` auf 4 fixieren** — Mid-flight getestet, kein negativer Effekt sichtbar. Aber: Der Unterschied zu 6 war nicht klar messbar (Änderung kam nach dem Hauptproblem am Takeoff). Separater Test empfohlen.

4. **zram auf 48 GB** — Swap Peak 14,5 GB bei 32 GB zram = 45%. Bei schwereren Runs (Run K: 81%) droht NVMe-Spill. Preemptiv erhöhen.

5. **DSF-Loading (X-Plane-seitig)** — Nicht tunable. Einziger Hebel: `-prefetch_apt 1` (undokumentiert, experimentell). Oder: Laminar Feature-Request für asynchrones DSF-Loading.
