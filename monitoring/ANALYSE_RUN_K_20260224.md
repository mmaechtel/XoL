# Run K — Ergebnisse: 116-Minuten XEL-dominierter Langflug

**Datum:** 2026-02-24
**System:** Ryzen 9 9800X3D 8C/16T, 96 GB RAM, RTX 4090 24 GB, 3x NVMe (2x SN850X 8TB + 990 PRO 4TB)
**Kernel:** Liquorix 6.18 (PDS)
**Workload:** X-Plane 12 (Peak 19,7 GB RSS) + XEarthLayer v0.3.0 (Peak 25,8 GB RSS) + QEMU/KVM (4,3 GB) + Swift Pilot Client
**Route:** EDDB (Berlin) → SW über Deutschland/Alpen → LIMC (Mailand Malpensa), ~800 km
**Änderungen seit Run J:** Änderung 8 aktiv (CB 30, max_concurrent_jobs 4, Concurrency zurückgedreht)

---

## 0. Testbedingungen

| Parameter | Wert |
|-----------|------|
| Dauer | 115,8 Min (6.891 vmstat-Samples) |
| Sidecar (bpftrace) | Ja — trace_reclaim, trace_io_slow, trace_fence |
| XEL-Log | Ja — 110k Zeilen, volle Session |
| Prewarm | EDDB, 4.257 Tiles, **0 Cache-Hits** (Cold Start) |
| XEL Tiles generiert | 22.812 (237 GB DDS-Volumen) |
| DSF-Loads (X-Plane) | 369 Events, 31 > 5s, max 14,75s |
| Crashes | 0 |

---

## 1. Erwartungen vs. Ergebnisse

| Metrik | Run I (Gesamt) | Run J (Gesamt) | **Run K (Gesamt)** | **Run K (Steady, ab Min 88)** |
|--------|---------------|---------------|-------------------|-------------------------------|
| Alloc Stall Samples | 102 (1,5%) | 81 (2,7%) | **235 (3,4%)** | **0** |
| Alloc Stall Peak/s | 13.992 | 8.833 | **13.831** | **0** |
| Direct Reclaim (bpftrace) | 29.030 | 40.926 | **171.744** | — |
| X-Plane Main Reclaim | 18.653 (64%) | 32.600 (80%) | **125.578 (73%)** | — |
| Main Thread ≥16ms | — | 2 | **23** | — |
| Main Thread Worst | — | — | **68,6 ms** | — |
| kswapd Efficiency | 97,5% | 97,5% | **96,3%** | **100%** |
| Direct Reclaim Efficiency | — | — | **54,8%** | **100%** |
| Swap Peak MB | 6.270 | 10.774 | **26.571** | ~26.400 |
| free avg MB | — | — | **4.706** | 3.497 |
| Slow IO (>5ms) | ~1.539 | 35 | **65** | **0** |
| EMFILE | 16.079 | 0 | **1.104** | **0** |
| Write-Lat max ms | 120,3 | 6,1 | **58,3** | <4 |
| DMA Fence Stalls | 0 | 0 | **0** | **0** |

**Bewertung:** Run K ist der bisher **schwerste Lastfall** (22.812 XEL-Tiles, 369 DSFs, Cold Start, 800 km neue Route). Absolute Zahlen sind die höchsten aller Runs. Aber: **Steady State ab Min 88 ist makellos** — null Stalls, null Reclaim, null Slow-IO.

---

## 2. Kernbefunde

### 2.1 Drei-Phasen-Verhalten

| Phase | Zeitraum | Dauer | Alloc Stalls | Beschreibung |
|-------|----------|-------|-------------|-------------|
| Warm-up | Min 0–3,3 | 3,3 Min | 45 | Initiales Szenerieladen, Peak 438/s |
| Ramp-up | Min 3,3–88,1 | 84,8 Min | 190 | Chronische Bursts alle 3–10 Min, Swap 0→26 GB |
| Steady | Min 88,1–115,8 | 27,7 Min | **0** | Makellos, Swap stabil, nur Swap-In |

Innerhalb des Ramp-up:

| Sub-Phase | Zeitraum | Stalls | Charakter |
|-----------|----------|--------|-----------|
| Quiet | Min 3,3–20,4 | 0 | 17,1 Min stall-frei (alle Startup-Tiles geladen) |
| Moderate | Min 20–42 | 62 | DSF-Ring-Wechsel, Peak 660/s |
| Schwer | Min 42–88 | 127 | Swap-Explosion, Peak 13.831/s, 6 Major-Bursts |

### 2.2 Memory Pressure

| Metrik | Wert | Bewertung |
|--------|------|-----------|
| available_mb min | 30.400 (bei Min 29) | Knapp, aber nie < 30 GB |
| Swap Peak | 26,6 GB (81% zram) | Höchster je gemessener Wert. 5,4 GB Headroom. |
| NVMe-Swap | **0** | zram absorbiert alles |
| Swap-In aktiv | 60,9% der Samples | Chronisches Working-Set-Thrashing via zram |
| Swap-Out aktiv | 3,0% der Samples | Konzentriert auf Min 40–90 |
| Direct Reclaim Efficiency | 54,8% (Ramp-up) | Fast die Hälfte der Scans verschwendet |
| Workingset Refault Anon | Hoch (Min 50–65) | zram-Thrashing: sofortiges Zurücklesen |

**Ursachenkette Ramp-up:**
```
XEL generiert 22.812 Tiles (237 GB DDS) → RSS Peak 25,8 GB
+ X-Plane lädt 369 DSFs → RSS wächst 9,6→19,7 GB
+ Gesamt Working Set ~50 GB auf 92 GB RAM
→ Kernel swappt XEL's Cold Pages nach zram (0→26,6 GB)
→ Jeder DSF-Load-Burst (bis 7 GB/s Read) provoziert Direct Reclaim
→ 45,5% der Scans finden keine reclaimbare Pages → CPU-Verschwendung auf Main Thread
```

### 2.3 XEarthLayer Streaming Activity

| Metrik | Wert |
|--------|------|
| Tiles generiert | 22.812 (18.508 ZL12 + 4.304 ZL14) |
| Prewarm | 4.257 Tiles in 3:08 (Cold Start, 0 Cache) |
| Ground Prefetch | 5.370 Tiles nach Prewarm |
| Cruise Prefetch | 8.446 Tiles |
| Letztes Tile generiert | Min 68 (20:14 UTC) |
| Reine Cache-Phase | Min 68–109 (40,7 Min, null Generation) |
| Circuit Breaker Triggers | 352 (47,7% der Cruise-Zeit blockiert) |
| CB Peak FUSE-Rate | 216 req/s (Threshold: 30) |
| EMFILE-Burst | 1.104 in 1 Sekunde (Min 21, falscher Takeoff) |
| Prefetch-Modus | Opportunistic |
| Tile-Latenz Prewarm p95 | 6.170 ms |
| Tile-Latenz Cruise avg | 704 ms (Median 316 ms) |
| Tiles > 10s | 12 (Bing-Timeout-Cluster) |

**Kernproblem bestätigt:** Circuit Breaker Threshold 30 liegt weit unter der normalen FUSE-Rate (Median 58,6 req/s). Prefetch war 47,7% der Cruise-Zeit blockiert. Erst als alle Tiles für die Route generiert waren (Min 68), hörten die CB-Triggers auf.

### 2.4 Direct Reclaim Attribution (bpftrace)

| Prozess | Events | Anteil | Total Stall | Worst |
|---------|--------|--------|-------------|-------|
| **X-Plane Main Thread** | 125.578 | **73,1%** | 66,6 s | **68,6 ms** |
| X-Plane cuda-EvtHandlr | 10.406 | 6,1% | 7,7 s | 63,8 ms |
| **XEL tokio-runtime** | 8.981 | **5,2%** | 11,9 s | **204,1 ms** |
| X-Plane threaded-ml | 4.827 | 2,8% | 4,0 s | 48,9 ms |
| bpftrace (Monitoring) | 4.799 | 2,8% | 3,4 s | 67,0 ms |
| Swift Pilot Client | 5.646 | 3,3% | 4,5 s | 52,6 ms |
| Rest (107 Prozesse) | 15.507 | 9,0% | — | — |

**Vergleich mit Zwischenauswertung (Min 0–35):**

| Metrik | Min 0–35 | Min 0–88 (Final) | Erklärung |
|--------|----------|-------------------|-----------|
| XEL tokio Anteil | 61,5% | **5,2%** | Frühe Dominanz durch Prewarm/Prefetch-Burst |
| Main Thread Anteil | 25% | **73,1%** | DSF-Loading ab Min 33 dominiert |
| Total Events | 2.542 | **171.744** | 93% der Events fallen in Min 48–88 |

Die Zwischenauswertung bei Min 35 war irreführend: XEL dominierte den Startup, aber der Hauptteil der Reclaim-Events kam später durch X-Plane's DSF-Loading.

### 2.5 Alloc-Stall-Cluster (Top 5)

| Cluster | Minute | Peak/s | Trigger |
|---------|--------|--------|---------|
| 1 | 60,5 | 13.831 | DSF +47+008 (Italien), 1,2M Direct Scans/s |
| 2 | 51,5 | 8.086 | DSF +48+009, Swap-Explosion 7→15 GB |
| 3 | 42,5 | 9.419 | DSF +49+009 (14,75s Load), erster schwerer Burst |
| 4 | 63,2 | 13.376 | DSF-Cluster Norditalien, 1,3M Direct Scans/s |
| 5 | 69,6 | 7.234 | DSF Malpensa-Approach, Swap 20→22 GB |

Alle schweren Bursts korrelieren direkt mit DSF-Load-Events. X-Plane liest bis zu 7 GB/s von NVMe, was den Page-Cache verdrängt und Direct Reclaim auf dem Main Thread auslöst.

---

## 3. GPU / VRAM

`vram.csv` ist leer (nur Header) — gamescope blockiert NVML. Keine GPU-Metriken verfügbar.

**Indirekt:** Null DMA-Fence-Stalls (trace_fence.log leer). GPU-seitig keine Blockaden.

---

## 4. Disk IO

| Metrik | nvme0n1 | nvme1n1 | nvme2n1 |
|--------|---------|---------|---------|
| Read avg / max (MB/s) | 13,8 / 3.386 | 13,3 / 3.374 | 14,3 / 3.388 |
| Read Latency avg (ms) | 0,315 | 0,358 | 0,281 |
| Read Latency max (ms) | 3,60 | 3,04 | 3,00 |
| Write Latency max (ms) | 57,7 | 58,1 | 58,3 |
| Slow IO Events | 22 | 20 | 23 |

**65 Slow-IO-Events insgesamt** (alle Writes, null Slow-Reads):
- 34 Events in Min 1,5–3,8 (Startup-Flush)
- 9 Events in Min 21,3 (Journal-Sync)
- 22 Events in Min 32,7–33,1 (Btrfs-Commit-Burst)
- **Ab Min 33: Null Write-Events > 4ms für 82 Minuten**

**NVMe PM QOS bestätigt stabil:** Kein 10-11ms Power-State-Pattern. Alle 65 Slow-Events sind Journal-Flushes.

**Vergleich:** Run H: 339, Run I: 1.539, Run J: 35, **Run K: 65**. Exzellent.

---

## 5. CPU & Frequenz

Aus proc.csv:

| Prozess | CPU% avg | CPU% max | Threads |
|---------|----------|----------|---------|
| X-Plane | ~350% | ~600% | 82–97 |
| XEL | ~20–80% (Bursts) | ~200% | 35–547 |
| QEMU | niedrig | — | stabil |

XEL Thread-Count ist Prefetch-Aktivitätsindikator:
- 35 = idle
- 120–200 = leichter Prefetch
- 300–547 = Heavy Burst (Startup, Cruise-Eintritt)

Keine Thread-Bomb wie in Run J (dort 36→300 in 14s → Freeze). max_concurrent_jobs=4 hält die Threads unter Kontrolle.

---

## 6. Per-Process Memory

| Prozess | Start RSS | Peak RSS | End RSS | Swap-Beitrag |
|---------|-----------|----------|---------|-------------|
| X-Plane | 9,6 GB | **19,7 GB** | 19,3 GB | gering (aktives Working Set) |
| XEL | 19,0 GB | **25,8 GB** | **6,5 GB** | **~16 GB nach zram** |
| QEMU | 4,3 GB | 4,3 GB | 4,1 GB | ~0,2 GB |

**Die zentrale Dynamik:** XEL's RSS fällt von 25,8 auf 6,5 GB — das sind keine freigegebenen Pages, sondern **nach zram geswappte Cold Pages**. Der Kernel opfert XEL's idle Tiles für X-Plane's wachsendes DSF-Working-Set.

---

## 7. Vergleich Runs H→I→J→K

| Metrik | H (Gesamt) | I (Gesamt) | J (Gesamt) | **K (Gesamt)** | **K (Steady)** |
|--------|-----------|-----------|-----------|---------------|----------------|
| Stall Samples | 117 | 102 | 81 | **235** | **0** |
| Stall % | — | 1,5% | 2,7% | **3,4%** | **0%** |
| Reclaim Events | 84.140 | 29.030 | 40.926 | **171.744** | ~0 |
| Main Thread % | 24% | 64% | 80% | **73%** | — |
| Main ≥16ms | — | — | 2 | **23** | — |
| Swap Peak GB | 12,0 | 6,3 | 10,8 | **26,6** | 26,4 |
| NVMe Swap | 0 | 0 | 0 | **0** | 0 |
| Slow IO | 339 | 1.539 | 35 | **65** | 0 |
| EMFILE | 1.126 | 16.079 | 0 | **1.104** | 0 |
| Stall-freie Tail | ~23 Min | **62 Min** | 0 Min | **27,7 Min** | — |
| XEL Tiles | — | 13.461 | 316 | **22.812** | 0 |
| DSF Loads | — | — | — | **369** | — |
| Ramp-up Dauer | ~85 Min | ~0 Min* | ∞ (kein Steady) | **88 Min** | — |

*Run I: 62 Min stall-frei von Anfang an (warmer Cache, moderate Route)

**Fazit Vergleich:** Run K hatte den mit Abstand schwersten Lastfall. Die höheren absoluten Zahlen spiegeln den Cold-Start + 800 km neue Route + 22k Tiles wider, nicht eine Regression im Tuning. Der Steady State (27,7 Min null Stalls) bestätigt, dass der Tuning-Stack funktioniert sobald das Working Set geladen ist.

---

## 8. Handlungsempfehlungen

### 8.1 Circuit Breaker Threshold 30 → 50 [BEREITS VORBEREITET]

**Problem:** CB Threshold 30 blockiert Prefetch 47,7% der Cruise-Zeit. Normale FUSE-Rate im Flug: Median 58,6 req/s.
**Erwartung:** Prefetch kann während normalem Flug arbeiten, nur bei echten Overload-Bursts (>50 req/s) pausieren.
**Risiko:** Gering — der CB schützt vor FUSE-Überlast; bei 50 greift er immer noch bei den schweren Spitzen (>100 req/s, 8% der Triggers).
**Status:** Änderung 9, bereits in config.ini.

### 8.2 max_concurrent_jobs 4 → 6 [BEREITS VORBEREITET]

**Problem:** Nur 4 parallele Tile-Jobs = ~20 Tiles/s Durchsatz. X-Plane fordert via FUSE 60–200 Tiles/s.
**Erwartung:** +50% Generation-Throughput, Prefetch kann vorlaufen.
**Risiko:** Moderat — mehr CPU-Konkurrenz mit X-Plane. Thread-Count unter Beobachtung halten.
**Status:** Änderung 9, bereits in config.ini.

### 8.3 Prewarm grid_size 4 → 6 [BEREITS VORBEREITET]

**Problem:** grid_size=4 (16 DSF-Tiles) ließ 15.000 Tiles für den Ground-Prefetch übrig.
**Erwartung:** 36 DSF-Tiles (~9.600 DDS-Tiles), ~7 Min Prewarm. Mehr Puffer vor Cruise-Eintritt.
**Risiko:** Gering — längere Prewarm-Phase (~7 vs. 3 Min), aber User wartet ohnehin auf X-Plane-Start.
**Status:** Änderung 9, bereits in config.ini.

### 8.4 Immer Prewarm vor dem Flug

**Befund:** Heute war 0% Cache-Hit beim Prewarm — ein kompletter Cold Start für den Berlin-Raum. Prewarm VOR dem X-Plane-Start ausführen.
**Aktion:** `xearthlayer run --airport <ICAO>` als festen Schritt vor dem Flug einplanen.

### 8.5 zram-Headroom beobachten

**Befund:** Peak 26,6 GB von 32 GB zram (81%). Bei noch schwereren Lastfällen (längere Route, mehr Addons) droht NVMe-Swap-Spill.
**Aktion:** Kein sofortiger Handlungsbedarf. Falls ein künftiger Run > 30 GB zram zeigt: zram auf 48 GB erhöhen (RAM reicht).

### 8.6 EMFILE bei False-Takeoff-Detection

**Befund:** 1.104 EMFILE-Errors in 1s durch falschen Cruise-Trigger bei schnellem Taxi (44,6 kt).
**Aktion:** XEL-seitig — Takeoff-Detection-Schwelle prüfen. Workaround: fd-Limit ist bereits 1M, also sind die Errors nicht durch System-Limits verursacht sondern durch XEL-interne FD-Pool-Erschöpfung unter Burst-Last.

---

## 9. Zusammenfassung

Run K war der bisher schwerste Lastfall: Cold-Start Berlin, 800 km neue Route über die Alpen nach Mailand, 22.812 generierte XEL-Tiles, 369 DSF-Loads. Das System brauchte 88 Minuten bis zum Steady State — deutlich länger als bei warmen Caches.

**Positiv:**
- Steady State ab Min 88 makellos (27,7 Min null Stalls, null Reclaim)
- IO-Latenz exzellent (PM QOS stabil, null Slow-Reads)
- zram absorbiert 26,6 GB Swap ohne NVMe-Spill
- Keine Crashes, keine Thread-Bomb, keine GPU-Probleme
- Tuning-Stack funktioniert — das Problem ist die Ramp-up-Dauer

**Negativ:**
- 235 Stall-Samples (höchster Wert aller Runs)
- 23 Frame-Drops auf Main Thread (≥16ms), Worst 68,6 ms
- Circuit Breaker blockierte Prefetch fast die halbe Cruise-Zeit
- Direct Reclaim Efficiency nur 54,8% im Ramp-up (CPU-Verschwendung)
- 88 Min bis Steady State bei Cold Start — für den Piloten inakzeptabel

**Nächster Schritt:** Run mit Änderung 9 (CB 50, Jobs 6, Prewarm 6×6). Erwartung: kürzere Ramp-up-Phase, weniger Startup-Stutter, Prefetch kann vorlaufen.
