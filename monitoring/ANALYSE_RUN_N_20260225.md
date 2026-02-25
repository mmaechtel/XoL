# Analyse Run N — LZKZ → EDDM (2026-02-25)

**Route:** LZKZ (Košice) → EDDM (München), ~540 km, FL250, Approach über München
**Dauer:** 80,5 Min (4829s), 21.719 Telemetrie-Samples @ 5 Hz
**Config:** Änderung 10 aktiv (max_concurrent_jobs=4, memory_size=4 GB, threads=12)
**Besonderheit:** Erster Run mit VRAM-Daten (NVML-Fix), OBS Streaming parallel aktiv

---

## 1. FPS-Profil

| Metrik | Wert |
|--------|------|
| FPS Median | 29,9 |
| FPS Mean | 30,9 |
| FPS Min | 0,0 (Pause) |
| FPS Max | 84,0 |
| FPS < 25 | 6,4% (1.387 Samples, ~277s) |
| FPS ≥ 30 | 46,2% |
| FPS 28–30 | 45,8% |

**Timing Baseline:** Frame P50=33,5ms (30 FPS), CPU P50=15,4ms, GPU P50=18,3ms.
Frame Time ist bei 50,25ms gecapped (= 19,9 FPS, gamescope Minimum). Wenn es stottert, stottert es auf genau 20 FPS.

### Stutter-Budget

| Phase | FPS < 25 | Anteil |
|-------|----------|--------|
| Gate (gs≈0, agl<10) | 804 Samples (161s) | Scenery-Loading |
| Airborne (agl≥10) | 583 Samples (117s) | **4,6%** der Flugzeit |
| Ground Roll | variabel | Takeoff + Landing |

**Bewertung:** 95,4% der Flugzeit über 25 FPS. Median 29,9 zeigt, dass das System meist am 30-FPS-Limit (VSync/gamescope) operiert. Die 4,6% Airborne-Stutter verteilen sich auf wenige Bursts.

---

## 2. Degradation Events (systematisch)

46 Events mit frame_time > 40ms und Dauer > 0,5s identifiziert. Davon 6 Airborne-Hauptereignisse:

| Event | Zeitpunkt (UTC) | Dauer | Phase | CPU_avg | GPU_avg | Bottleneck |
|-------|-----------------|-------|-------|---------|---------|------------|
| 32 | 14:19 | **57s** | Takeoff | 24ms | 26ms | Balanced |
| 33 | 14:21 | 3,7s | Climb-out | 22ms | 28ms | Balanced |
| 34–36 | 14:51 | 3×0,8s | Cruise FL250 | 31ms | 17ms | CPU |
| 39 | 14:59 | **61s** | Approach | 26ms | 24ms | Balanced |
| 40–43 | 15:05 | Cluster | Final App | 27ms | 23ms | CPU/BAL |
| 44–45 | 15:07 | 2,5s | Taxi EDDM | 21ms | 25ms | Balanced |

**Anomalie:** GPU Time Max = 1713ms (14:12 UTC, Cruise). Ursache: X-Plane GPU-Pipeline-Stall bei Airport-Object-Loading ("Loading sim objects for airport LOLH"). Measurement-Artefakt im Dataref, kein echter Render-Stall.

---

## 3. Event 32 — Takeoff (57s)

**X-Plane Log:** Keine DSF-Loads während des Events.
**XEL Log:** Flight phase `ground→cruise` bei gs=51,5 kts. 5.707 Log-Zeilen: Prefetch-Batch 200 Tiles, massive Tile-Generation.
**System:** XEL 35→547 Threads, CPU 1315%. Null allocstalls, null PSI.
**Reclaim Trace:** Nur 10 kswapd wake/sleep Events — kswapd reicht aus, kein Direct Reclaim.
**GPU:** Util 75% → 27%, Power 250W → 125W. GPU hungert.

**Diagnose:** Reines CPU-Scheduling-Problem. XEL's Phase-Transition `ground→cruise` triggert Prefetch-Burst (200 Tiles). Thread-Pool (generation.threads=12) plus Tokio-Runtime saturiert alle 16 HW-Threads. X-Plane Main Thread verdrängt. Kein Memory-Problem, kein DSF-Problem.

---

## 4. Event 34–36 — Cruise FL250 (3× kurze Bursts)

**X-Plane Log:** `+49+010.dsf` **5065ms**, `+48+010.dsf` in Teilen (2181ms, 3887ms) — DSF Lon-Boundary bei 10°E.
**XEL Log:** 2.035 Zeilen/30s, `skipped_cached=0` — alle Tiles frisch generiert.
**Reclaim:** 6 kswapd Events — harmlos.

**Diagnose:** X-Plane DSF-Loading (5s synchron auf Main Thread) bei Lon-Boundary-Crossing. XEL generiert parallel uncached Tiles. Kurze Bursts, schnelle Recovery.

---

## 5. Event 39 — Approach München (61s) — HAUPTBEFUND

**Position:** Lat 48,24° → 48,29°, Lon 11,30° → 11,34°. Kein DSF-Boundary-Crossing (durchgehend DSF 48/11).

### X-Plane Log: Massive DSF-Kaskade

| DSF | Ladezeit | Effekt |
|-----|----------|--------|
| +47+009 | **6.818ms** (7s) | Main Thread blockiert |
| +49+009 | **13.037ms** (13s) | Main Thread blockiert |
| +49+009 | 3.908ms | Nachladen |
| +48+009 | 8.819ms + **14.368ms** | Schwerste Stalls (14s) |

Dazu Dutzende `E/SCN: Failed to find resource 'AEP/PrivateAssets/...'` Fehler — **AEP Overlays (Beta)** referenzieren fehlende Objekte. Tritt bei jedem DSF-Load für die betroffenen Tiles auf.

### XEL Log: Burst

5.058 Zeilen/90s, `skipped_cached=47` — fast nichts gecacht. Massive Tile-Generation parallel zu X-Plane DSF-Loads.

### Reclaim Trace: 13.338 Events

| Prozess | Events | Anteil |
|---------|--------|--------|
| tokio-runtime-w (XEL) | 7.403 | 55% |
| **Main** (X-Plane) | **4.485** | **34%** |
| cuda-EvtHandlr (NVIDIA) | 578 | 4% |
| pipewire-pulse | 118 | 1% |
| threaded-ml (X-Plane) | 97 | 1% |

### vmstat: Drei Phasen

**Phase 1 (32s) — CPU-Sättigung:** XEL 600–1210% CPU, 547 Threads. pgfaults 1,5M/s, aber 0 allocstalls. kswapd arbeitet (pgsteal 250k/s), hält noch mit.

**Phase 2 (12s) — Memory Pressure:** kswapd überfordert → Direct Reclaim.

| Sekunde | allocstall/s | pgscan_direct/s | pswpout/s |
|---------|-------------|-----------------|-----------|
| +26s | **780** | 50.749 | 827 |
| +30s | **160** | 10.449 | 587 |
| +32s | **6.948** | **1.522.360** | **148.761** |
| +33s | **2.461** | 243.326 | 36.402 |

**Phase 3 (22s) — Abklingen:** XEL idle, Threads sinken 547→35. FPS bleibt bei 19,9 — X-Plane arbeitet aufgestaute DSF-Daten sequentiell ab.

### Slow IO

44 Events (6–11ms NVMe-Latenz) — NVMe unter Sustained Read/Write von XEL + X-Plane DSF parallel.

### Diagnose: Dreifach-Problem

1. **X-Plane DSF Loading (primär):** 3 DSF-Tiles gleichzeitig geladen (47/9, 48/9, 49/9). Schwerster Load: **14,4s synchron auf Main Thread**. Nicht Boundary-bedingt — Approach bringt diese Tiles in den Sichtradius.
2. **XEL Thread-Explosion (sekundär):** 547 Threads, 1200% CPU. Konkurriert mit X-Plane um Kerne. Verschärft den DSF-Load-Stall.
3. **Memory Pressure (tertiär, ab Sekunde 26):** 1,5M pgfaults/s überfordert kswapd. Direct Reclaim trifft X-Plane Main Thread (34% der Events) → zusätzliche Latenz. allocstalls bis 6.948/s.

---

## 6. Event 40–43 — Final Approach EDDM (Cluster)

**X-Plane Log:** `+49+013.dsf (5453ms, 3808ms)`, `+48+013.dsf (2631ms)`, "Loading sim objects for airport EDDM".
**XEL Log:** 1.088 Zeilen — moderater Burst, Approach-Tiles teilweise aus Event 39 gecacht.
**Reclaim:** 7 kswapd Events — kein Direct Reclaim.

**Diagnose:** DSF-Loading für EDDM-Region + Airport-Objects. Kürzer als Event 39, da Tiles teilweise gecacht.

---

## 7. Event 44–45 — Taxi EDDM (2,5s)

**X-Plane Log:** Keine Events.
**XEL Log:** Phase-Transition `cruise→ground`, 59 Ground-Tiles submitted.
**Reclaim:** **2.847 Events**, 99% auf `tokio-runtime-w` (XEL) — XEL Workers in Direct Reclaim.

**Diagnose:** Post-Landung: XEL generiert Ground-Resolution-Tiles (höheres Zoom als Cruise). X-Plane Main Thread nicht betroffen (0% Reclaim-Anteil). Kurzer Burst.

---

## 8. VRAM-Profil

| Phase | VRAM (MiB) |
|-------|-----------|
| Gate (X-Plane Start) | 3.160 → 7.681 |
| Taxi + Takeoff | 14.024 → 14.280 |
| Cruise | 14.280 → 14.350 |
| Approach München | 19.822 → 19.956 |
| Final + Landing | 19.956 → 20.104 |

**Peak:** 20.104 MiB / 24.564 MiB (82%). Bei 24 GB VRAM genug Headroom für Normalflüge. X-Plane verwaltet VRAM-Eviction intern gut.

---

## 9. XEL-Profil

| Metrik | Wert |
|--------|------|
| CPU idle (<5%) | 75,5% der Samples |
| CPU extreme (>1000%) | 2,9% |
| RSS Peak | 15.375 MB (15,0 GB) |
| RSS avg | 10.979 MB |
| Thread Explosion (>200 Threads) | 29,4% der Samples |

---

## 10. Erkenntnisse

### Takeoff vs. Approach — verschiedene Root Causes

| Dimension | Takeoff (Event 32) | Approach (Event 39) |
|-----------|-------------------|-------------------|
| Primär-Ursache | **XEL CPU-Explosion** | **X-Plane DSF Loading (14s)** |
| Sekundär | — | XEL CPU-Explosion |
| Tertiär | — | Memory Pressure (13k Reclaim) |
| allocstalls | **0** | **6.948/s** |
| DSF-Loading | Nein | 3 DSFs parallel (7s + 13s + 14s) |
| X-Plane Main Thread Reclaim | **0%** | **34%** |
| GPU Util min | 27% | 33% |

### Was gut funktioniert (Änderung 10)

- Null sustained allocstalls für Takeoff-Phase (rein CPU, kein Memory)
- Swap-on-NVMe bleibt bei 0 (zram fängt alles)
- FPS Median 29,9 (am VSync-Limit)
- 95,4% Flugzeit über 25 FPS

### Was nicht funktioniert

1. **generation.threads=12 ist zu hoch:** XEL belegt regelmäßig 13 Kerne bei 8C/16T. Bereits geändert (Änderung 11: threads=6).
2. **X-Plane DSF-Loading ist synchron und langsam:** Bis 14s Blocking auf Main Thread. Nicht durch Tuning beeinflussbar — X-Plane-Architekturproblem.
3. **AEP Overlays (Beta):** Fehlende `PrivateAssets/*` Objekte erzeugen Dutzende `E/SCN`-Fehler pro DSF-Load. Möglicherweise Overhead durch fehlgeschlagene Resource-Lookups. Update abwarten.
4. **FPS-Recovery dauert zu lange:** Nach XEL-Burst bleibt FPS noch 20+s bei 19,9 (aufgestaute DSF-Loads).

### Offene Fragen für Run O

- Reicht `generation.threads=6` um den Takeoff-Stutter zu eliminieren?
- Bleibt der Approach-Stutter bestehen? (DSF-Loading-Komponente ist thread-unabhängig)
- Ist der Memory-Pressure-Peak ohne XEL-Thread-Explosion reproduzierbar?

---

## 11. Tuning-Empfehlung

**Änderung 11 (bereits angewendet):** `generation.threads = 12 → 6`

**Falls Approach-Stutter in Run O persistiert:**
- `executor.max_concurrent_tasks = 128 → 48` (weniger In-Flight-Tasks → weniger pgfaults)
- `executor.network_concurrent = 128 → 64` (weniger parallele Downloads)

**AEP Overlays:** Auf Update aus Beta warten. Alternativ: temporär deaktivieren falls Fehler-Overhead messbar.
