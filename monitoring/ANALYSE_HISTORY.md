# Tuning-Historie: X-Plane 12 + XEarthLayer + QEMU/KVM

**System:** Ryzen 9 9800X3D 8C/16T, 96 GB RAM, RTX 4090 24 GB, 3x NVMe (2x SN850X 8TB + 990 PRO 4TB)
**Kernel:** Liquorix 6.18 (PDS), Btrfs RAID0 (xplane_data) + RAID1 (home)
**Zeitraum:** 2026-02-17 bis 2026-02-25

---

## Runs A–D — Baseline + sysctl + IO-Tuning (2026-02-17)

Kurzruns (5–15 Min) zum Identifizieren und Beheben der Grundprobleme.

**Run A (Baseline):** Alle Metriken schlecht — Direct Reclaim 75k/s, Alloc Stalls 1k/s, Write-Latenz 260–312 ms, Dirty Pages 502 MB. Ursachen: min_free_kbytes zu klein, Kyber-Scheduler + WBT drosseln NVMe, Dirty-Limits zu hoch.

**Änderung 1 (sysctl):** min_free_kbytes 512M→1G, swappiness 10→1, page-cluster 3→0, vfs_cache_pressure 100→150, dirty_background_ratio 3→1, dirty_ratio 10→5, dirty_expire 30→15s, dirty_writeback 15→5s.
→ **Run B/C:** Direct Reclaim + Stalls eliminiert. Write-Latenz bleibt — IO-Scheduler ist das Problem.

**Änderung 2 (NVMe IO + Btrfs):** IO-Scheduler kyber→none, WBT→0, Readahead 256 KB einheitlich, Btrfs commit 120→30/60s.
→ **Run D:** Write-Latenz **-95%** (1,8 ms avg), Dirty Pages **-94%** (30 MB), TLB Shootdowns eliminiert.

---

## Run E — Langflug (2026-02-18, 90 Min)

Erster Langflug mit allen bisherigen Tunings.

| Metrik | Run D (15 Min) | Run E (90 Min) | Bewertung |
|--------|----------------|----------------|-----------|
| Direct Reclaim | 0 | **2.122.555/s** (0,3% der Zeit) | Kehrt bei Last zurück |
| Alloc Stalls | 0 | **13.383/s** (0,3%) | Kehrt bei Last zurück |
| Write-Lat avg (nvme0n1) | 1,8 ms | **16,1 ms** | Verschlechtert |
| Write-Lat max (nvme0n1) | 283 ms | **699 ms** | Deutlich schlechter |
| DSF-Load max | — | **63.385 ms** (63s!) | X-Plane hängt |
| EMFILE Errors | — | **3.474** in 4s | XEL FD-Exhaustion |
| Swap Swing | 211 MB/15 Min | **11.595 MB/90 Min** | Massiver Swap-Traffic |
| Dirty Pages | 30 MB | 39 MB | Stabil |

**Ursache:** Swap + xplane_data auf gleicher NVMe (nvme0n1) → Write-Contention. XEL EMFILE-Kaskade → Re-Downloads → Page-Cache-Explosion → Swap-Storm → DSF-Stalls bis 63s.

---

## Änderung 3 — zram + XEL-Config + Disk-Cleanup + NoCow

```
zram 32 GB lz4 (pri=100)           Swap im RAM statt auf NVMe
NVMe-Swap pri=-2                   Nur noch Fallback
XEL network_concurrent 128 → 64   Weniger FD-Druck
XEL disk_io_concurrent 64 → 32    Weniger parallele Writes
XEL max_tiles_per_cycle 200 → 100 Langsameres Prefetch
NoCow auf Tile-Caches              chattr +C, kein Btrfs-CoW-Overhead
Disk 91% → 74%                     Btrfs-Allocator defragmentiert
```

---

## Run F — zram-Validierung (2026-02-22, 143 Min in 2 Teilen)

Teil 1: 90 Min (inkl. X-Plane Crash + Neustart). Teil 2: 53 Min stabiler Flug.

| Metrik | Run E | Run F/1 | Run F/2 (Steady) | Veränderung |
|--------|-------|---------|-------------------|-------------|
| Direct Reclaim max | 2.122.555/s | 762.842/s | **0/s** | Steady: eliminiert |
| Alloc Stalls max | 13.383/s | 10.900/s | **0/s** | Steady: eliminiert |
| NVMe-Swap genutzt | 11.595 MB | **0** (zram 100%) | **0** | **Eliminiert** |
| Write-Volume (Swap-NVMe) | 25,1 GB | **3,6 GB** | — | **-86%** |
| Write-Lat avg (Swap-NVMe) | 16,1 ms | 6,0 ms | — | **-49%** (non-zero) |
| Write-Lat max | 699 ms | 476 ms | **44 ms** | **-94%** (Steady) |
| DSF-Load max | 63.385 ms | **22.116 ms** | — | **-65%** |
| EMFILE Errors | 3.474 | **2.116** | — | -39% |
| Dirty Pages avg | 39 MB | **2,4 MB** | — | **-94%** |
| Major Faults avg | 377/s | 860/s | **76/s** | Steady: -80% |

**Kernbefund:** zram absorbiert 100% Swap (Peak 79% von 32 GB). Steady State ist exzellent — null Stalls, null Reclaim. Ramp-up-Phase (Szenerieladen) zeigt weiterhin Memory-Pressure.

---

## Änderung 4 — Erweiterte Instrumentierung

Keine System-Tunings, nur bessere Messtechnik:

```
sysmon.py: +PCIe TX/RX, +Throttle Reasons, +Perf State (NVML)
sysmon.py: +pswpin/pswpout, +workingset_refault_anon/file, +thp_fault_fallback
sysmon.py: +dmesg pre/post Snapshots, +GPU Event Monitor (journalctl)
bpftrace:  Direct Reclaim pro Prozess, Slow IO >5ms, DMA Fence >5ms
```

---

## Run G — Erweiterte Instrumentierung (2026-02-22, 81 Min)

| Metrik | Run F/2 (Steady) | Run G (Gesamt) | Run G (Steady, ab Min 60) |
|--------|------------------|----------------|---------------------------|
| Alloc Stalls | 0 | 42 Bursts, max 11.425/s | **0** |
| Direct Reclaim | 0 | avg 2.049/s | **0** |
| pgmajfault avg/s | 76 | 662 | ~56 |
| Dirty Pages avg | 2,4 MB | 3,6 MB | ~2 MB |
| GPU Throttle | — | **0** | **0** |
| DMA Fence Stalls | — | **0** | **0** |
| PSI (alle) | — | **0,00** | **0,00** |
| VRAM Peak | — | **93,9%** (23 GiB) | — |

**Neue Erkenntnisse durch erweiterte Instrumentierung:**

| Befund | Daten | Bedeutung |
|--------|-------|-----------|
| X-Plane Main Thread = 67% der Direct Reclaim Events | 47.583 von 71.160 | Main Thread wird durch Reclaim blockiert |
| Worst-Case Reclaim-Latenz: 20,6 ms | bpftrace | = 1 Frame Drop bei 50 FPS |
| Workingset Anon Refaults: 86% | vmstat | zram-internes Thrashing in Ramp-up |
| nvme1n1 (990 PRO): 90% der Slow-IO-Events | bpftrace | NVMe Power-State-Exit 10–11 ms |
| `watermark_boost_factor = 0` | sysctl | Liquorix deaktiviert kswapd-Boost! |
| `free` pendelt bei 1,4–2 GB | mem.csv | Nur 400 MB über min_free_kbytes |
| PCIe-Traffic vernachlässigbar | NVML | Kein GPU-Daten-Bottleneck |

**Ursachenanalyse Swap-Storm (Minute 42):**

```
free = 1.4 GB (knapp über min_free_kbytes = 1 GB)
  + watermark_boost_factor = 0 (kswapd reclaimed zu wenig pro Wakeup)
  + swappiness = 1 (Anon-Pages erst im Notfall swappen)
  → kswapd kommt nicht nach → Direct Reclaim auf X-Plane Main Thread
  → Panik-Swap-Out: 538.360 pages/s → alle Prozesse stecken in Reclaim
```

---

## Änderung 5 — Watermark + Swappiness + NVMe PM QOS

```
vm.min_free_kbytes           1 GB → 2 GB        Mehr Puffer vor Direct Reclaim
vm.watermark_boost_factor    0 → 15000           kswapd-Boost reaktivieren (Liquorix-Default war 0!)
vm.watermark_scale_factor    10 → 50             Breitere Watermark-Lücke
vm.swappiness                1 → 10              Graduelles Background-Swap statt Panik-Burst
NVMe pm_qos_latency_tolerance_us  100000 → 0     Power-State-Exit-Latenz eliminieren
bpftrace BPFTRACE_MAP_KEYS_MAX    4096 → 65536   Map-Overflow vermeiden
```

---

## Run H — Watermark-Optimierung (2026-02-24, 108 Min)

Route: EDDH → ESSA (Hamburg → Stockholm), Geradeausflug über Ostsee.
**Confounding Factor:** Skunkcrafts Updater Cronjob feuerte um 12:00 UTC (Min 77), 12-Sekunden-Burst.

| Metrik | Run G (Gesamt) | Run H (Gesamt) | Run H (Steady, ab Min 85) |
|--------|---------------|---------------|---------------------------|
| Alloc Stalls | 42 Events, max 11.425/s | 117 Events, max 17.462/s | **0** |
| Direct Reclaim (bpftrace) | 71.160 Events | 84.140 Events | — |
| X-Plane Main Reclaim | 47.583 (67%) | **19.865 (24%)** | — |
| SkunkcraftsUpda Reclaim | — (nicht aktiv) | **48.157 (57%)** | — |
| Slow IO Events (>5ms) | 12.383 | **339 (-97%)** | — |
| 10–11ms IO-Pattern | 90% der Events | **1,5% (5 Events)** | — |
| Swap Peak | 18.156 MB | 12.045 MB | ~8.930 MB |
| free avg | ~1.400 MB | **~4.880 MB** | ~3.300 MB |
| kswapd Efficiency | 93,4% | **94,5%** | 94,4% |
| GPU Throttle | 0 | — (kein NVML) | — |
| DMA Fence Stalls | 0 | **0** | **0** |

**Gesicherte Verbesserungen durch Tuning:**

1. **NVMe PM QOS:** 97,3% Reduktion der Slow-IO-Events. 10–11ms Power-State-Pattern eliminiert.
2. **kswapd-Headroom:** free avg 4,9 GB (vs. 1,4 GB). min_free_kbytes=2 GB + boost_factor=15000 wirken.
3. **X-Plane Main Thread Reclaim: -58%** (19.865 vs. 47.583) trotz stärkerer Konkurrenz.
4. **Swap gradueller:** pswpout nur 2,5% aktiv (vs. 5,1%), erst bei Min 54 erstes GB.
5. **bpftrace-Datenqualität:** MAP_KEYS=65536 → keine Overflows, 45 KB statt 697 MB.

**Neue Erkenntnisse:**

- **Skunkcrafts Cronjob (12:00 UTC, 12s Burst) = #1 Reclaim-Verursacher (57,2%)** — überlagert Tuning-Effekte
- Ramp-up verlängert auf 85 Min (vs. 60 Min), ~10 Min davon durch Cronjob-Burst
- X-Plane Main Thread Worst Case: 50 ms (vs. 20,6 ms in Run G) — durch Skunkcrafts-Konkurrenz
- EMFILE-Burst: 1.126 "Too many open files" bei XEL (fd-Limit)

**Maßnahmen nach Run H:**

- Skunkcrafts-Cronjob aus crontab entfernt (war `0 */4 * * *`)
- Gesamte User-Crontab bereinigt (auch obsolete UnWetter-Archiv-Jobs entfernt)
- Alle Tuning-Settings persistent gemacht (sysctl.conf + udev-Rule)
- swappiness von 10 auf **5** reduziert (Kompromiss: weniger Ramp-up-Dauer vs. Panik-Bursts)
- Duplikate in `/etc/sysctl.d/99-custom-tuning.conf` bereinigt

---

## Änderung 6 — Post-Run-H Bereinigung + XEL-Optimierung

```
Skunkcrafts Cronjob          aktiv → entfernt     Verursachte 57% aller Reclaim-Events
UnWetter-Archiv Cronjobs     aktiv → entfernt     Nicht mehr benötigt
vm.swappiness                10 → 5               Kompromiss: schnellerer Ramp-up, keine Panik-Bursts
NVMe PM QOS udev-Rule        fehlte → angelegt    /etc/udev/rules.d/61-nvme-pmqos.rules
sysctl.conf Duplikate         ja → bereinigt       watermark_boost_factor + scale_factor waren doppelt
XEL prefetch mode            (default) → auto     Selbstkalibrierende Prefetch-Strategie
XEL generation threads       16 → 12              Kompromiss: Prewarm-Power vs. Flug-Konkurrenz
XEL network_concurrent       64 → 96              Mehr Prewarm-Durchsatz, Circuit Breaker drosselt im Flug
XEL cpu_concurrent           8 → 12               Mehr parallele Assemble+Encode Ops
XEL disk_io_concurrent       32 → 48              Mehr parallele Cache-Ops
```

## Run I — Post-H-Tuning, kein Skunkcrafts (2026-02-24, 115 Min, 2 Crashes)

Route: LPMA (Madeira) Umgebung. Kein Prewarm. 2 X-Plane-Crashes bei Positionssprüngen. Mid-Run `max_tiles_per_cycle` 100→200.

| Metrik | Run H (Gesamt) | Run I (Gesamt) | Run I (Normalflug, 0–62 Min) |
|--------|---------------|---------------|-------------------------------|
| Direct Reclaim (bpftrace) | 84.140 | **29.030 (-65%)** | **0** |
| Alloc Stalls max/s | 17.462 | 13.992 | **0** |
| Alloc Stall Samples | 117 | 102 | **0** |
| X-Plane Main Reclaim | 19.865 | 18.653 (-6%) | — |
| kswapd Efficiency | 94,5% | **97,5%** | — |
| Swap Peak MB | 12.045 | **6.270 (-48%)** | ~1.650 |
| EMFILE Errors | 1.126 | **16.079 (14×!)** | — |
| Slow IO Events (>5ms) | 339 | ~1.539 | — |
| Write-Lat max ms | 53,8 | 120,3 | — |
| DMA Fence Stalls | 0 | **0** | — |

**Kernbefunde:**

1. **Normalflug perfekt:** 62 Min null Stalls, null Reclaim — Tuning-Stack bestätigt
2. **Skunkcrafts-Elimination bestätigt:** -65% Reclaim-Events (84k→29k)
3. **kswapd-Efficiency +3%:** swappiness=5 verbessert Reclaim-Balance
4. **EMFILE-Krise 14× schlimmer:** XEL-Concurrency-Erhöhung kontraproduktiv (network 64→96, disk_io 32→48)
5. **Crashes = X-Plane + FUSE-Limit:** DSF-Loading über FUSE bei Positionssprüngen → nicht behebbar durch Tuning
6. **Write-Latenz-Spitzen verdoppelt:** 120ms (vs. 54ms), möglicherweise EMFILE-bedingte Retry-Bursts

**Maßnahmen nach Run I:**

- XEL Concurrency auf Run-H-Werte zurückdrehen (network=64, disk_io=32)
- fd-Limit auf 65536 erhöhen (`/etc/security/limits.conf`)
- Immer Prewarm vor dem Flug (`xearthlayer run --airport <ICAO>`)

---

## Änderung 7 — Mid-Run-I XEL-Prefetch

```
XEL max_tiles_per_cycle      100 → 200            Mehr Prefetch-Weitsicht (geändert bei Min ~80)
```

---

## Run J — Ortho4XP-Flug, XEL Thread-Bomb → Freeze (2026-02-24, 51 Min)

Route: LFMN → Italien/Schweiz/EDDS. Überwiegend installierte Ortho4XP-Pakete, XEL nur Gap-Filler (316 Tiles).
QEMU mid-flight gestartet (nach Freeze). Gamescope-Freeze bei Min 39, X-Plane per `kill -9` beendet.

| Metrik | Run I (Gesamt) | Run J (Gesamt) | Bemerkung |
|--------|---------------|---------------|-----------|
| Direct Reclaim (bpftrace) | 29.030 | **40.926 (+41%)** | Ortho4XP-DSF-Loading treibt Reclaim |
| Alloc Stalls max/s | 13.992 | 8.833 | Weniger extrem, aber chronisch |
| Alloc Stall Samples | 102 (1,5%) | 81 (2,7%) | Höherer Anteil |
| Main Thread Reclaim | 18.653 (64%) | **32.600 (80%)** | X-Plane's eigenes DSF-Loading dominiert |
| Main Thread >16ms | 23 | **2** | Bessere Tail-Latenz |
| kswapd Efficiency | 97,5% | 97,5% | Identisch |
| Swap Peak MB | 6.270 | **10.774** | Ortho4XP-DSFs schwerer |
| pswpin active | 25,4% | **68,4%** | Chronisches Working-Set-Thrashing |
| EMFILE Errors | 16.079 | **0** | Kein XEL-Netzwerk nötig |
| XEL Tiles | 13.461 | **316** | XEL fast idle |
| Write-Lat max ms | 120,3 | **6,1** | Bestätigt: 120ms war EMFILE-bedingt |
| Slow IO Events | ~1.539 | **35** | NVMe-PM-QOS stabil |

**Kernbefunde:**

1. **XEL Thread-Bomb = Freeze-Ursache:** 36→300 Threads, +9,4 GB in 14s, Circuit Breaker zu langsam
2. **Ortho4XP-DSFs erzeugen periodische Stalls:** Alle 8–10 Min bei Ring-Wechsel, bis 2,3M Triangles/Tile
3. **Kein Steady State erreicht:** Im Gegensatz zu Run I (62 Min stall-frei) hatte Run J durchgehend Stall-Bursts
4. **0 EMFILE:** Warmer lokaler Cache = kein Netzwerk = keine fd-Erschöpfung
5. **Write-Latenz-Beweis:** 6ms max (vs. 120ms in Run I) — bestätigt EMFILE als Ursache der Run-I-Spitzen
6. **QEMU = Compaction-Krise:** 5 GB in 30s → alle 6.711 compact_stalls + 1.898 THP-Fallbacks der Session

---

## Änderung 8 — Anti-Thread-Bomb + Concurrency zurückdrehen

```
XEL circuit_breaker_threshold    50 → 30             Früher drosseln (Run J: CB zu langsam bei 316-Tile-Burst)
XEL circuit_breaker_open_ms      500 → 200            Schneller auslösen
XEL max_concurrent_jobs          8 → 4                Weniger parallele FUSE-Jobs
XEL cpu_concurrent               12 → 8               Zurück, weniger Thread-Druck
XEL network_concurrent           96 → 64              Zurück auf Run-H-Wert (EMFILE-Fix)
XEL disk_io_concurrent           48 → 32              Zurück auf Run-H-Wert (EMFILE-Fix)
```

---

## Run K — XEL Cold-Start Langflug (2026-02-24, 116 Min)

Route: EDDB → SW über Deutschland/Alpen → LIMC (Mailand Malpensa), ~800 km. Cold Start (0 Cache-Hits).
Schwerster Lastfall bisher: 22.812 XEL-Tiles, 369 DSF-Loads, 237 GB DDS-Volumen.

| Metrik | Run I (Gesamt) | Run J (Gesamt) | Run K (Gesamt) | Run K (Steady) |
|--------|---------------|---------------|---------------|----------------|
| Alloc Stall Samples | 102 (1,5%) | 81 (2,7%) | **235 (3,4%)** | **0** |
| Direct Reclaim (bpf) | 29.030 | 40.926 | **171.744** | ~0 |
| Main Thread Reclaim | 18.653 (64%) | 32.600 (80%) | **125.578 (73%)** | — |
| Main Thread ≥16ms | — | 2 | **23** | — |
| Main Thread Worst | — | — | **68,6 ms** | — |
| XEL tokio Reclaim | — | — | 8.981 (5,2%) | — |
| Swap Peak GB | 6,3 | 10,8 | **26,6 (81% zram)** | 26,4 |
| NVMe Swap | 0 | 0 | **0** | 0 |
| Slow IO | 1.539 | 35 | **65** | 0 |
| EMFILE | 16.079 | 0 | **1.104** | 0 |
| Ramp-up Dauer | ~0 Min | ∞ | **88 Min** | — |
| Stall-freie Tail | 62 Min | 0 Min | **27,7 Min** | — |

**Kernbefunde:**

1. **Steady State ab Min 88 makellos:** Null Stalls, null Reclaim, null Slow-IO — Tuning-Stack bestätigt
2. **Circuit Breaker Threshold 30 blockiert Prefetch 47,7% der Cruise-Zeit** — FUSE-Median 58,6 req/s liegt deutlich über Threshold
3. **DSF-Loading = Haupttreiber der Ramp-up-Stalls:** Jeder schwere Burst korreliert mit DSF-Load-Events (bis 7 GB/s NVMe-Read)
4. **X-Plane Main Thread = 73% aller Reclaim-Events (125.578)** — DSF-Loading erzwingt Page-Cache-Verdrängung → Direct Reclaim
5. **Direct Reclaim Efficiency nur 54,8%** im Ramp-up — fast die Hälfte der Scans verschwendet (dirty/pinned Pages)
6. **zram absorbiert 26,6 GB** (81% Auslastung) ohne NVMe-Spill — noch 5,4 GB Headroom
7. **IO exzellent:** PM QOS stabil, nur 65 Slow-Events (alle Journal-Flushes), null Slow-Reads
8. **EMFILE:** 1.104 in 1s durch falschen Takeoff-Trigger (schnelles Taxi 44,6 kt)

---

## XEL-Update (2026-02-25) — PR #57 + PR #61

XEarthLayer-Update mit zwei kritischen Fixes:

- **PR #57 (Priority Inversion Fix):** On-Demand-Requests haben jetzt Pipeline-Priorität über Prefetch. Eliminiert die Thread-Bomb-Ursache aus Run J.
- **PR #61 (CB Resource-Pool):** Circuit Breaker nutzt jetzt `ResourcePools::max_utilization()` (Trip bei ~90%) statt FUSE-Request-Rate. `circuit_breaker_threshold` deprecated und entfernt.

**Erkenntnis:** Die 47,7% CB-Blockade in Run K war ein **Bug** — der CB zählte Cache-Hits (50-150 req/s beim normalen Rendern) als Last. Unser Tuning (50→30→50) hat gegen einen Softwarefehler gekämpft, nicht gegen ein Konfigurationsproblem.

---

## Änderung 9 — XEL-Update + Config-Anpassung (2026-02-25)

```
XEL circuit_breaker_threshold    ENTFERNT (deprecated) War Bug-Workaround, CB jetzt resource-pool-basiert
XEL circuit_breaker_open_ms      200 → 500 (Default)   Aggressive Timing war Workaround, Default reicht
XEL circuit_breaker_half_open_s  2 → 5 (Default)       Gleicher Grund
XEL network_concurrent           64 → 128 (Default)    EMFILE-Workaround entfällt (Pipeline-Fix PR #57)
XEL disk_io_concurrent           32 → 64 (Default)     Gleicher Grund
XEL disk_io_profile              nvme → auto (Default)  Auto-Erkennung funktioniert
XEL max_concurrent_jobs           4 → 8                 Priority Inversion Fix eliminiert Thread-Bomb-Risiko
XEL prewarm grid_size             4 → 6                 36 DSF-Tiles, ±117nm E/W bei 50°N (Reserve für Grid-Ecken)
```

---

## Gesamtentwicklung — Schlüsselmetriken

| Metrik | A (Baseline) | D (+IO) | E (90 Min) | F/2 (Steady) | G (Steady) | H (Steady) | I (Normalflug) | J (Gesamt)* | K (Steady)** |
|--------|-------------|---------|------------|---------------|------------|------------|-----------------|-------------|-------------|
| Direct Reclaim max/s | 75.183 | 0 | 2.122.555 | **0** | **0** | **0** | **0** | 1.293.750 | **0** |
| Alloc Stalls max/s | 1.042 | 0 | 13.383 | **0** | **0** | **0** | **0** | 8.833 | **0** |
| Write-Lat avg (ms) | 36–47 | 1,8 | 16,1 | — | — | 0,25 | 0,21–0,24 | 0,37–0,50 | <0,5 |
| Write-Lat max (ms) | 260–312 | 283 | 699 | **44** | — | 53,8 | 120,3 | **6,1** | <4 |
| Dirty Pages avg (MB) | 502 | 30 | 39 | **2,4** | ~2 | ~16 | 45 | 1,7 | ~2 |
| Swap auf NVMe | ja | ja | 11,6 GB | **0** | **0** | **0** | **0** | **0** | **0** |
| Slow IO (>5ms) | — | — | — | — | 12.383 | **339** | ~1.539 | **35** | **0** |
| EMFILE | — | — | 3.474 | — | — | 1.126 | 16.079 | **0** | **0** |
| PSI | 0 | 0 | 0 | — | **0** | — | n/a | 0 | — |
| GPU Throttle | — | — | — | — | **0** | — | — | — | — |

*Run J: Ortho4XP-Szenerie, XEL nur Gap-Filler, Freeze bei Min 39.
**Run K Steady: Ab Min 88, schwerster Lastfall (Cold Start, 22k Tiles, 800 km neue Route).

---

## Änderung 12 — Circuit Breaker scharf stellen (2026-02-25)

**Befund Run N:** `generation.threads=6` (Änd. 11) reicht nicht — Tokio-Runtime spawned weiterhin 315–547 Threads. Der Circuit Breaker war zahnlos: Bei `max_concurrent_tasks=128` waren die Pools so groß, dass der Breaker nie rechtzeitig triggerte.

**Strategie:** Pool-Größen reduzieren, damit der CB früher auslöst. CPU-Limits nicht anfassen.

```
XEL max_concurrent_tasks         128 → 48             CB sieht Pool-Sättigung schneller
XEL network_concurrent           128 → 48             Weniger parallele HTTP-Connections
XEL max_tiles_per_cycle           200 → 80            Kleinere Prefetch-Batches
```

---

## Run O — LEMD → EDDM mit Circuit-Breaker-Tuning (2026-02-25, 92 Min)

Route: LEMD (Madrid) → EDDM (München), ~1.500 km, FL330, Pyrenäen/Alpen-Überflug.
Änderung 12 aktiv. Mid-flight: generation.threads 6→4.

| Metrik | Run N (80 Min) | **Run O (92 Min)** | Trend |
|--------|----------------|---------------------|-------|
| FPS < 25 | 6,4% | **2,5%** | **↓↓↓** |
| Takeoff-Stutter | **57s** | **0s** | **ELIMINIERT** |
| Approach-Stutter | **61s** | **6,2s** | **↓ 90%** |
| Max Event-Dauer | 61s | **9,2s** (DSF, nicht XEL) | **↓ 85%** |
| FPS Median | 29,9 | **29,7** | = |
| allocstall max/s | 6.948 | 10.341 | ↑ (aber kurze Bursts) |
| XEL Threads max | 547 | 547 | = (Pool limitiert Dauer, nicht Threads) |
| XEL RSS Peak | 15,4 GB | **15,1 GB** | = |
| VRAM Peak | 20,1 GB (82%) | **21,3 GB (87%)** | ~ |

**Kernbefunde:**

1. **Takeoff-Stutter eliminiert:** 57s → 0s. CB greift bei kleineren Pools rechtzeitig, Prefetch-Burst wird gedrosselt bevor Thread-Bomb eskaliert.
2. **Approach -90%:** 61s → 6,2s. Dreifach-Problem (DSF + XEL + Memory) noch vorhanden, aber CB begrenzt Burst-Dauer.
3. **Cruise-Dips kurz und harmlos:** Cluster E07–E12 (max 3,7s) statt durchgehende Minuten-Stutter. Allocstalls treten auf, aber System erholt sich dank CB-Pause.
4. **DSF-Loading bleibt Flaschenhals:** E05 (9,2s Climb) = reines X-Plane DSF-Crossing, XEL idle (49% CPU, 203 Threads). Nicht tunable.
5. **Pool-Verkleinerung = wirksamster einzelner Tuning-Schritt** gegen FPS-Stutter in der gesamten Historie.

Detailanalyse: [ANALYSE_RUN_O_20260225.md](ANALYSE_RUN_O_20260225.md)

**Zeitraum:** 2026-02-17 bis 2026-02-25

## Aktueller Tuning-Stack (persistent, Stand 2026-02-25)

```
# sysctl (/etc/sysctl.d/99-custom-tuning.conf)
vm.swappiness = 5
vm.min_free_kbytes = 2097152          (2 GB)
vm.watermark_boost_factor = 15000
vm.watermark_scale_factor = 50
vm.page-cluster = 0
vm.vfs_cache_pressure = 150
vm.dirty_background_ratio = 1
vm.dirty_ratio = 5
vm.dirty_expire_centisecs = 1500
vm.dirty_writeback_centisecs = 500

# NVMe IO (/etc/udev/rules.d/60-nvme-tuning.rules)
scheduler = none
WBT = 0
readahead = 256 KB
pm_qos_latency_tolerance_us = 0       (/etc/udev/rules.d/61-nvme-pmqos.rules)

# zram
32 GB lz4, pri=100 (zram-swap.service)

# Btrfs (fstab)
xplane_data: commit=30s
home: commit=60s

# XEL (~/.xearthlayer/config.ini) — nach Änderung 12 (2026-02-25)
# Nur Nicht-Default-Werte:
generation threads = 6               (Default: 16, Thread-Pool-Limit für CPU-bound Work)
cpu_concurrent = 8                   (Default: 10, CPU shared mit X-Plane)
max_concurrent_jobs = 4              (Default: 16, allocstall-Elimination)
max_concurrent_tasks = 48            (Default: 128, CB-Schärfung — Änderung 12)
network_concurrent = 48              (Default: 128, CB-Schärfung — Änderung 12)
max_tiles_per_cycle = 80             (Default: 200, kleinere Prefetch-Batches — Änderung 12)
memory_size = 4 GB                   (Default: 8 GB, RSS-Reduktion)
prewarm grid_size = 6                (Default: 4, Reserve für Grid-Ecken)
# fd-Limit: ulimit -n = 1.048.576 (systemweit)
```

**Fazit Run K:** Schwerster Lastfall (Cold Start, 800 km, 22k Tiles). Steady State ab Min 88 makellos. 47,7% CB-Blockade war ein **XEL-Bug** (Cache-Hits als Last gezählt). Behoben durch PR #61 (resource-pool CB) + PR #57 (Priority Inversion Fix). Änderung 9: Alle CB-Workarounds entfernt, nur CPU-Bottleneck-Werte + Prewarm 6×6 bleiben. Offene XEL-Issues: #58 (Band-Misalignment), #62 (Takeoff-Stutter).

---

## Änderung 10 — allocstall-Elimination + RSS-Reduktion (2026-02-25)

```
XEL max_concurrent_jobs          8 → 4                 allocstalls 1.862/s → 0 (Run L₁ vs. L₂)
XEL memory_size                  8 → 4 GB              RSS-Reduktion (-37%), Swap -63%
```

Bestätigt durch Run L₁ (EDLW, jobs=8: 1.862/s allocstalls, 60k Reclaim) vs. Run L₂ (EDDH, jobs=4: **0 allocstalls, 0 Direct Reclaim**).

---

## Run M — ESGG→EDDS mit In-Sim-Telemetrie (2026-02-25, 98 Min)

Route: ESGG (Göteborg) → EDDS (Stuttgart), ~950 km, FL350, 7 DSF-Boundary-Crossings.
Erstmaliger Einsatz von xplane_telemetry.py (FPS/CPU/GPU Time via UDP RREF, 5 Hz).
NVML-Bug in sysmon.py entdeckt und gefixt (pynvml Scope-Bug → vram.csv war in allen Runs leer).

| Metrik | Run K (116 Min) | **Run M (98 Min)** | Trend |
|--------|-----------------|---------------------|-------|
| Alloc Stall Samples | 235 (3,4%) | **199 (3,4%)** | = |
| Alloc Stall Peak/s | 13.831 | **8.324** | ↓ |
| Direct Reclaim (bpf) | 171.744 | **89.335 (-48%)** | ↓ |
| Main Thread Reclaim % | 73,1% | 69,2% | ~ |
| Main Thread Worst | 68,6 ms | **189,0 ms** | ↑ |
| XEL tokio Reclaim % | 5,2% | **20,6%** | ↑ (memory_size-Effekt) |
| Swap Peak | 26,6 GB | **9,7 GB (-63%)** | ↓ |
| XEL RSS Peak | 25,8 GB | **16,2 GB (-37%)** | ↓ |
| FPS avg / P5 / min | — | **29,8 / 27,8 / 19,9** | Erstmals gemessen |
| GPU Time avg / P95 / max | — | **18,0 / 23,8 / 42,0 ms** | Erstmals gemessen |

**Kernbefunde:**

1. **DSF-Boundary-Crossings = reproduzierbares Hauptproblem:** 7 von 8 Stutter-Events korrelieren mit 1°-Breitengrad-Übergängen. X-Plane-Architekturproblem (synchrones DSF-Loading auf Main Thread). Tuning mildert, eliminiert nicht.
2. **Touchdown-Stutter ist GPU-getrieben (NEU):** Erstmals durch Telemetrie nachgewiesen — GPU Time springt auf 42ms, Reclaim liegt zu 97% auf XEL-Threads, 0% auf Main Thread. Neuer Stutter-Typ, möglicherweise verwandt mit XEL Issue #62.
3. **Änderung 10 wirkt positiv:** memory_size 4 GB senkt XEL RSS -37%, Swap -63%, Gesamt-Reclaim -48%. Trade-off: XEL-Reclaim-Anteil ×4 (5→21%).
4. **NVML war nie kaputt durch gamescope:** pynvml lokal importiert, global referenziert → NameError bei jedem Aufruf, still geschluckt. Fix: `_NVML_LIB` globale Referenz + Auto-Fallback. Ab nächstem Run: volle VRAM-Daten.

Detailanalyse: [ANALYSE_RUN_M_20260225.md](ANALYSE_RUN_M_20260225.md)

---

## Änderung 11 — XEL Thread-Explosion begrenzen (2026-02-25)

**Befund aus Run N (LZKZ Takeoff-Analyse, vor Änderung):**
Beim Takeoff spawnt XEL in 35 Sekunden **512 neue Threads** (35 → 547), belegt **13 CPU-Kerne** (1315% Peak), System-CPU geht von 80% idle auf **0% idle**. X-Plane Main Thread wird verdrängt → GPU hungert (Util 75% → 27%, Power 250W → 125W) → FPS locked auf 19,9 für **57 Sekunden**. Kein allocstall, kein Reclaim, kein PSI-Druck — reines **CPU-Scheduling-Problem**.

`max_concurrent_jobs=4` (Änderung 10) begrenzt nur Job-Ebene, nicht die Executor-Threads darunter. Der `generation.threads=12` Thread-Pool plus Tokio-Overhead = 13 Kerne belegt.

```
XEL generation threads               12 → 6           Direkte Begrenzung der CPU-bound Thread-Pool-Größe
```

**Ziel:** Bei 8 echten Kernen (16T) bleiben 2 Kerne für X-Plane Main Thread frei. Erwarteter XEL-Peak: ~6–7 Kerne statt 13. FPS-Dip beim Takeoff sollte von 20 auf 25–28 steigen.

**Weitere Kandidaten (nicht geändert, beobachten):**
- `executor.max_concurrent_tasks = 128` (→32 falls threads=6 nicht reicht)
- `executor.network_concurrent = 128` (→48)
- `prefetch.max_tiles_per_cycle = 200` (→50)

Validierung: Run O (nächster Flug nach XEL-Neustart).

---

## Run N — LZKZ → EDDM mit Cross-Korrelation (2026-02-25, 80 Min)

Route: LZKZ (Košice) → EDDM (München), ~540 km, FL250. Änderung 10 aktiv, threads=12 (vor Änderung 11).
Erster Run mit VRAM-Daten (NVML-Fix). OBS Streaming parallel. Systematische Event-Analyse: X-Plane Timing → alle Logs korreliert.

| Metrik | Run M (98 Min) | **Run N (80 Min)** | Trend |
|--------|----------------|---------------------|-------|
| FPS Median / Mean | — / 29,8 | **29,9 / 30,9** | ~ |
| Airborne Stutter (FPS<25) | — | **4,6%** (117s) | Erstmals gemessen |
| Alloc Stall Peak/s | 8.324 | **6.948** | ↓ |
| Direct Reclaim Events (bpf) | 89.335 | **13.338** (nur Approach) | ↓↓ |
| Main Thread Reclaim % | 69,2% | **34%** (Approach only) | ↓ |
| XEL RSS Peak | 16,2 GB | **15,4 GB** | ~ |
| Swap auf NVMe | 0 | **0** | = |
| VRAM Peak | — | **20,1 GB / 24,6 GB (82%)** | Erstmals gemessen |
| Slow IO (>5ms) | 1.806 | **44** (nur Approach) | ↓↓ |

**Kernbefunde (Event-basierte Cross-Korrelation):**

1. **Takeoff-Stutter (57s) = reines CPU-Problem:** XEL Phase-Transition `ground→cruise` bei gs=52 kts → 547 Threads, 1315% CPU. Null allocstalls, null Reclaim, null DSF-Loading. GPU hungert (27% Util). Änderung 11 (threads 12→6) adressiert dies direkt.

2. **Approach-Stutter (61s) = Dreifach-Problem (NEU):**
   - *Primär:* X-Plane DSF Loading — 3 DSFs parallel (7s + 13s + **14,4s synchron** auf Main Thread)
   - *Sekundär:* XEL Thread-Explosion (547T, 1200% CPU) konkurriert um Kerne
   - *Tertiär:* Memory Pressure nach 26s → 13k Reclaim-Events, **34% auf X-Plane Main Thread**, allocstalls 6.948/s
   - Kein DSF-Boundary-Crossing — Approach bringt Tiles 47/9, 48/9, 49/9 in Sichtradius

3. **AEP Overlays (Beta) stören:** Dutzende `E/SCN: Failed to find resource 'AEP/PrivateAssets/...'` pro DSF-Load. Overhead durch fehlgeschlagene Resource-Lookups. Update abwarten.

4. **VRAM unkritisch:** 20,1 GB Peak bei 24,6 GB total (82%). X-Plane verwaltet VRAM-Eviction intern gut. Kein Handlungsbedarf.

5. **Cruise-Stutter (3×0,8s) = DSF Lon-Boundary bei 10°E:** `+49+010.dsf` (5065ms) + `+48+010.dsf` (3887ms). XEL `skipped_cached=0` — alle Tiles frisch generiert. Bekanntes Boundary-Muster.

**Fazit:** Takeoff und Approach haben **verschiedene Root Causes**. Änderung 11 sollte Takeoff deutlich verbessern, aber Approach nur teilweise — dort dominiert X-Plane's synchrones DSF-Loading (14s).

Detailanalyse: [ANALYSE_RUN_N_20260225.md](ANALYSE_RUN_N_20260225.md)

---

## Gesamtentwicklung — Schlüsselmetriken

| Metrik | A (Baseline) | D (+IO) | E (90 Min) | F/2 (Steady) | G (Steady) | H (Steady) | I (Normalflug) | J (Gesamt)* | K (Steady)** | M (Gesamt)*** | N (Gesamt)**** | O (Gesamt)† |
|--------|-------------|---------|------------|---------------|------------|------------|-----------------|-------------|-------------|---------------|----------------|-------------|
| Direct Reclaim max/s | 75.183 | 0 | 2.122.555 | **0** | **0** | **0** | **0** | 1.293.750 | **0** | 451.643 | 1.522.360 | — |
| Alloc Stalls max/s | 1.042 | 0 | 13.383 | **0** | **0** | **0** | **0** | 8.833 | **0** | 8.324 | 6.948 | **10.341** |
| Write-Lat avg (ms) | 36–47 | 1,8 | 16,1 | — | — | 0,25 | 0,21–0,24 | 0,37–0,50 | <0,5 | 0,03–0,09 | — | — |
| Write-Lat max (ms) | 260–312 | 283 | 699 | **44** | — | 53,8 | 120,3 | **6,1** | <4 | 18,3 | — | — |
| Dirty Pages avg (MB) | 502 | 30 | 39 | **2,4** | ~2 | ~16 | 45 | 1,7 | ~2 | ~5 | — | — |
| Swap auf NVMe | ja | ja | 11,6 GB | **0** | **0** | **0** | **0** | **0** | **0** | **0** | **0** | **0** |
| Slow IO (>5ms) | — | — | — | — | 12.383 | **339** | ~1.539 | **35** | **0** | 1.806 | 44 | **28.099** |
| EMFILE | — | — | 3.474 | — | — | 1.126 | 16.079 | **0** | **0** | 0 | 0 | 0 |
| FPS avg / median | — | — | — | — | — | — | — | — | — | 29,8 / — | 30,9 / 29,9 | **29,4 / 29,7** |
| FPS < 25 | — | — | — | — | — | — | — | — | — | — | ~8%†† | **2,5%** |
| Takeoff-Stutter | — | — | — | — | — | — | — | — | — | — | **57s** | **0s** |
| Approach-Stutter | — | — | — | — | — | — | — | — | — | — | **61s** | **6,2s** |
| GPU Time max (ms) | — | — | — | — | — | — | — | — | — | 42,0 | 1713‡ | **132** |
| VRAM Peak (GB) | — | — | — | — | — | — | — | — | — | — | 20,1 (82%) | **21,3 (87%)** |

*Run J: Ortho4XP-Szenerie, Freeze bei Min 39.
**Run K Steady: Ab Min 88, Cold Start 22k Tiles.
***Run M: DSF-Burst-Phase, Stalls nur bei Boundary-Crossings.
****Run N: Stalls nur beim Approach (61s Dreifach-Problem). Takeoff-Stutter rein CPU-bedingt.
†Run O: Circuit-Breaker-Tuning (Pools 128→48). allocstalls höher in Summe, aber nur kurze Bursts statt Mega-Events.
††Run N FPS<25 geschätzt aus Airborne-Stutter 4,6% + Gate-Loading.
‡GPU Time 1713ms = Measurement-Artefakt (Airport Object Loading), kein Render-Stall.

**Zeitraum:** 2026-02-17 bis 2026-02-25
