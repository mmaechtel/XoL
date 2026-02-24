# Run H — Ergebnisse: 108-Minuten Langflug mit Watermark-Optimierung

**Datum:** 2026-02-24
**System:** Ryzen 9 9800X3D 8C/16T, 96 GB RAM, RTX 4090 24 GB, 3x NVMe (2x SN850X 8TB + 990 PRO 4TB)
**Kernel:** Liquorix 6.18 (PDS)
**Workload:** X-Plane 12 + XEarthLayer + Skunkcrafts Updater + QEMU/KVM
**Route:** EDDH (Hamburg) → ESSA (Stockholm), Geradeausflug über Ostsee

---

## 0. Testbedingungen

| Parameter | Wert |
|-----------|------|
| Monitoring-Dauer | 108 Min (10:43–12:31 UTC) |
| X-Plane lief seit | ~09:41 UTC (62 Min vor Monitoring-Start) |
| Samples (200ms) | 32.133 |
| Samples (1s) | 6.427 |
| zram | 32 GB lz4, pri=100 |
| NVMe-Swap | nvme2n1p5 120 GB, pri=-2 (Fallback) |
| bpftrace | 3 Tracer (Direct Reclaim, Slow IO >5ms, DMA Fence >5ms), BPFTRACE_MAX_MAP_KEYS=65536 |

### Änderungen seit Run G (Tuning-Paket "Watermark-Optimierung")

```
vm.min_free_kbytes           1 GB → 2 GB        Mehr kswapd-Vorlauf
vm.watermark_boost_factor    0 → 15000           kswapd-Boost reaktiviert
vm.watermark_scale_factor    10 → 50             Breitere Watermark-Lücke
vm.swappiness                1 → 10              Graduelles Background-Swap
NVMe pm_qos_latency_tolerance_us  100000 → 0     Power-State-Exit-Latenz eliminiert
```

---

## 1. Key Findings (Severity-geordnet)

### [CRITICAL] Skunkcrafts Updater Cronjob = #1 Reclaim-Verursacher (57,2%)

Ein **Cronjob** startete um exakt **12:00:00 UTC** (Min 76,5) den Skunkcrafts Updater. In nur **12 Sekunden** (12:00:02–12:00:14) erzeugte er **48.157 Direct-Reclaim-Events** (57,2% aller Events), 883% CPU Peak, ~21 GB IO-Reads und trieb den Swap auf sein Maximum (12 GB). Der User war sich des Cronjobs nicht bewusst.

| Prozess | Events | Anteil | Max Latenz | Events >16ms |
|---------|--------|--------|-----------|-------------|
| **SkunkcraftsUpda** (12s Burst) | 48.157 | **57,2%** | 44,5 ms | 32 |
| Main Thread (X-Plane) | 19.865 | 23,6% | 50,0 ms | 21 |
| cuda-EvtHandlr | 4.888 | 5,8% | 38,7 ms | — |
| tokio-runtime-w (XEL) | 2.975 | 3,5% | 48,6 ms | — |

**Impact:** Dieser 12-Sekunden-Burst verursachte den gesamten Stall-Cluster 29 (17.462/s, der schlimmste des Fluges) und trieb den Swap-Out auf 549k pages/s. Ohne diesen Cronjob wäre der schlimmste Stall-Cluster eliminiert und die Ramp-up-Phase ~10 Minuten kürzer.

### [CRITICAL] Peak Stall-Cluster bei Minute 77 — ausgelöst durch Cronjob

Cluster 29 (Min 76,5–76,7): **17.462 allocstalls/s** mit 2,3M pgscan_direct/s und 549k pswpout/s. Zeitgleich erreichte Swap sein Maximum (12.045 MB) und available sein Minimum (38.831 MB). **Direkt verursacht durch den Skunkcrafts-Cronjob** (zeitliche Korrelation: exakt 12:00 UTC).

### [WARNING] X-Plane Main Thread: 21 Frame-Drop-Events (>16ms)

19.865 Direct-Reclaim-Events auf dem Main Thread, davon:
- 2.402 Events >1ms (12,1%)
- 226 Events >5ms (1,1%)
- 40 Events >10ms (0,2%)
- **21 Events >16ms** (garantierter Frame-Drop)
- **Worst Case: 50,0 ms** (3 Frames bei 60 FPS)

### [WARNING] XEL EMFILE-Burst: 1.126 "Too many open files" bei 10:44:24

Alle 1.126 Events in einer einzigen Sekunde. Ursache: XEL-Tile-Cache-Zugriffe überschreiten das File-Descriptor-Limit.

### [INFO] NVMe 10–11ms Latenz-Muster vollständig eliminiert

PM QOS Fix bestätigt — Details in Abschnitt 7.

### [INFO] Steady State (ab Min 85) = exzellent

Null allocstalls, null Direct Reclaim, null Compaction Stalls, null THP-Fallbacks. Nur Background-kswapd + Swap-In-Refaulting.

---

## 2. Drei-Phasen-Verhalten

| Phase | Zeitfenster | Charakteristik |
|-------|-------------|----------------|
| **Clean** | 0–1,7 Min | Kein Swap, kein Reclaim, used ~33 GB |
| **Ramp-up** | 1,7–85 Min | Swap 0→12 GB, 33 Stall-Cluster, SkunkcraftsUpda-Dominanz |
| **Steady State** | 85–108 Min | used ~47 GB, available ~42 GB, swap ~9 GB stabil |

**Ramp-up länger als Run G** (85 Min vs. 60 Min). Ursachen:
1. Skunkcrafts-Cronjob um 12:00 UTC (Min 77) verlängerte die Ramp-up-Phase um ~10 Min
2. Geradeausflug EDDH→ESSA über Ostsee = niedriger Cache-Hit bei XEL
3. Swap-Wachstum langsamer (swappiness=10 = gradueller, aber langwieriger)

---

## 3. Memory & VM Pressure

### 3.1 Übersicht

| Metrik | Start | Peak | Ende (Steady) |
|--------|-------|------|---------------|
| used_mb | 33.042 | 49.321 | ~47.800 |
| free_mb | 29.713 | min 2.421 | ~3.300 |
| available_mb | 65.437 | min 38.831 | ~41.300 |
| swap_used_mb | 0 | 12.045 | ~8.930 |
| dirty_mb | 18,6 | 449,8 | ~1,0 |
| cached_mb | 31.209 | — | ~43.000 |

### 3.2 Swap-Trajektorie

| Schwelle | Minute |
|----------|--------|
| Swap > 1.000 MB | 54,4 |
| Swap > 5.000 MB | 65,9 |
| Swap > 10.000 MB | 76,6 |
| Swap-Peak (12.045 MB) | 76,6 |

Swap swing: **12.045 MB** (0 → 12 GB). Danach Rückgang auf ~9 GB im Steady State.

### 3.3 vmstat-Aggregate

| Metrik | Gesamt | Steady State (ab Min 86) |
|--------|--------|--------------------------|
| allocstall_s: non-zero | 117 Samples (1,8%) | **0** |
| allocstall_s: max | 17.462/s | **0** |
| pgscan_direct_s: avg | 1.794 | **0** |
| pgscan_kswapd_s: avg | 7.455 | 2.532 |
| kswapd efficiency | **94,5%** | **94,4%** |
| pswpin_s: avg | 421 | 166 |
| pswpin_s: % active | 51,2% | **96,3%** |
| pswpout_s: avg | 738 | 240 |
| pswpout_s: % active | 2,5% | 0,7% |
| wset_refault_anon: % active | 52,2% | 95,5% |
| wset_refault_file: % active | 58,0% | 54,7% |
| compact_stall_s: sum | 4.655 | **0** |
| thp_fault_fallback: sum | 1.234 | **0** |
| pgfault_s: avg | 171.428 | 33.092 |

### 3.4 Alloc-Stall-Cluster (Top 5 nach Schwere)

| Cluster | Minute | Peak Stalls/s | Peak Direct/s | Peak Swap-Out/s | Trigger |
|---------|--------|--------------|---------------|-----------------|---------|
| 29 | 76,5–76,7 | **17.462** | 2.334.293 | 549.476 | Swap-Storm + SkunkcraftsUpda |
| 11 | 29,0–29,6 | **11.617** | 738.392 | 0 | XEL Tile-Loading Burst |
| 21 | 70,8–70,9 | **7.399** | 1.833.853 | 232.556 | Swap-Storm |
| 28 | 76,1–76,2 | **2.892** | 506.153 | 182.621 | Vorläufer zu Cluster 29 |
| 5 | 17,5–18,0 | **1.157** | 91.204 | 0 | Szenerieladen |

---

## 4. bpftrace — Direct Reclaim pro Prozess

### 4.1 Übersicht

| Metrik | Wert |
|--------|------|
| Gesamt-Events | **84.140** (vs. 71.160 in Run G) |
| Reclaimed Pages | ~7,8M = **29,9 GiB** |
| kswapd Wakes | 2.258 |
| kswapd Sleeps | 354 |

### 4.2 Top-Verursacher

| Prozess | Events | Anteil | Avg µs | Max µs | >1ms | >5ms | >10ms | >16ms |
|---------|--------|--------|--------|--------|------|------|-------|-------|
| **SkunkcraftsUpda** | 48.157 | 57,2% | 694 | 44.492 | 8.735 | 871 | 149 | 32 |
| **Main Thread** | 19.865 | 23,6% | 467 | **50.034** | 2.402 | 226 | 40 | **21** |
| cuda-EvtHandlr | 4.888 | 5,8% | — | 38.688 | — | — | — | — |
| tokio-runtime-w | 2.975 | 3,5% | — | 48.620 | — | — | — | — |
| bpftrace | 1.556 | 1,8% | — | 19.907 | — | — | — | — |
| claude | 1.218 | 1,4% | — | 9.891 | — | — | — | — |
| threaded-ml | 1.149 | 1,4% | — | 32.792 | — | — | — | — |

### 4.3 Vergleich X-Plane Main Thread: Run G → Run H

| Metrik | Run G | Run H | Veränderung |
|--------|-------|-------|-------------|
| Events | 47.583 | 19.865 | **-58%** |
| Max Latenz | 20,6 ms | 50,0 ms | Verschlechtert |
| Events >1ms | 6.131 | 2.402 | **-61%** |
| Events >5ms | 75 | 226 | +201% |
| Events >10ms | 28 | 40 | +43% |
| Events >16ms | — | 21 | Neu gemessen |

**Interpretation:** Die Gesamtzahl der X-Plane-Reclaim-Events sank um 58%. Die Tail-Latenz verschlechterte sich jedoch — wahrscheinlich weil der Main Thread nun in stärkerem Wettbewerb mit SkunkcraftsUpdater um freie Pages steht. Ohne Skunkcrafts wäre die Tail-Latenz vermutlich besser.

---

## 5. Per-Process

| Prozess | Avg CPU% | Max CPU% | Avg RSS GB | Peak RSS GB | Peak Min | Max Threads |
|---------|---------|---------|-----------|-----------|----------|-------------|
| **X-Plane** | 283,5 | 1.707 | 16,4 | **19,1** | 76 | 154 |
| **XEarthLayer** | 89,8 | 1.328 | 17,2 | **21,2** | 47 | 547 |
| **SkunkcraftsUpda** | 439,0 | 883,6 | 0,6 | 1,3 | 77 | 76 |
| QEMU | — | — | — | — | — | — |
| gamescope-wl | 1,0 | 4,0 | 0,1 | 0,2 | — | 14 |

**Combined RSS Peak:** 39.657 MB (min 54,6) — XEL 20.764 + X-Plane 18.160 + Rest.

### RSS-Lifecycle

- **XEL:** 11.798 MB → Peak 21.178 MB (min 47) → 18.201 MB (Ende). +9.380 MB Wachstum.
- **X-Plane:** 2.935 MB → Peak 19.071 MB (min 76) → 16.295 MB (Ende). +16.136 MB Wachstum.
- **SkunkcraftsUpda:** 1.070 MB → Peak 1.282 MB (min 77) → 245 MB (Ende).

### IO-Volumen

| Prozess | Read GB | Write GB |
|---------|---------|----------|
| X-Plane Main | 84,9 | 0,4 |
| XEarthLayer | 41,1 | 22,7 |
| SkunkcraftsUpda | 21,2 | 0 |

---

## 6. Disk IO

### 6.1 Latenz-Profil

| Device | Read Lat avg ms | Read Lat max ms | Write Lat avg ms | Write Lat max ms |
|--------|----------------|----------------|-----------------|-----------------|
| nvme0n1 (990 PRO) | **0,25** | 2,0 | 10,2 | 53,7 |
| nvme1n1 (SN850X) | **0,26** | 9,1 | 3,5 | 53,6 |
| nvme2n1 (SN850X) | **0,25** | 8,0 | 3,6 | 53,8 |

**Read-Latenzen exzellent** (0,25 ms avg vs. Run G nvme1n1 p95=10,7 ms). Write-Latenz-Spitzen bei 53 ms auf allen 3 NVMe gleichzeitig = **Btrfs-Journal-Flush** (synchroner Metadata-Commit).

### 6.2 Throughput

| Device | Read avg MB/s | Read max MB/s | Write avg MB/s | Write max MB/s |
|--------|--------------|--------------|---------------|---------------|
| nvme0n1 | 6,9 | 3.433 | 1,1 | 85 |
| nvme1n1 | 7,6 | 3.441 | 1,8 | 712 |
| nvme2n1 | 7,9 | 3.437 | 1,8 | 712 |

**RAID0-Balance:** Gleichmäßige Read-Verteilung (320–404 Spikes >100 MB/s). Aggregate Peak ~10,3 GB/s.

---

## 7. NVMe PM QOS — Vergleich Run G → Run H

**Die wichtigste einzelne Verbesserung durch die Run-H-Settings.**

| Metrik | Run G | Run H | Veränderung |
|--------|-------|-------|-------------|
| Slow-IO-Events (>5ms) | 12.383 | **339** | **-97,3%** |
| Events bei 10–11 ms | ~11.145 (90%) | **5 (1,5%)** | **-99,95%** |
| Dominante Latenz | 10–11 ms (PM-Wake) | **6–8 ms (normales IO)** | Muster eliminiert |
| Events/Min (Steady) | >100/min | **0,5/min** | Eliminiert |
| bpftrace Map-Overflows | ~3.042.000 | **0** | Gelöst (MAP_KEYS 65536) |

**Bewertung:** `pm_qos_latency_tolerance_us=0` hat das NVMe Power-State-Exit-Problem **vollständig eliminiert**. Die verbleibenden 339 Events sind echtes IO unter Last (89% in einem einzigen Szenerieladen-Burst bei 11:30), kein Power-Management-Artefakt.

---

## 8. GPU / VRAM

**vram.csv ist leer** — gamescope blockiert NVML-GPU-Zugriff in dieser Session. Keine GPU-Daten verfügbar.

**DMA Fence Waits:** 0 Events (trace_fence.log leer). GPU-Synchronisation sauber.

---

## 9. XEarthLayer Streaming

### 9.1 XEL-Timeline (aus xearthlayer.log)

| Zeitpunkt (UTC) | Event |
|-----------------|-------|
| 09:41:44 | Prewarm EDDH: 7.992 Tiles (2.833 to generate) |
| 09:46:12 | Prefetch Start (ground strategy, 0% cache hit) |
| 09:46:44 | Erster Circuit Breaker (rate=50,4) |
| 10:02:55 | **Takeoff** (ground→cruise) |
| 10:43:00 | Monitoring-Start (XEL aktiv seit 62 Min) |
| 10:44:24 | **EMFILE-Burst: 1.126 "Too many open files"** |
| 11:24:27 | **Landung** (cruise→ground, ESSA Stockholm) |
| 11:34:36 | Telemetry stale (X-Plane beendet) |

### 9.2 Circuit Breaker

- **226 Events** über die gesamte Session
- Peak-Rate: 158,4 (vs. Threshold 50,0) bei 10:03:30
- Clusters: 09:46–10:07 (Ramp-up am Boden + Takeoff)

### 9.3 Cache-Verhalten

Route EDDH→ESSA = Geradeausflug über offene Ostsee. Kaum Landmasse = wenig DSF-Tiles, aber XEL muss Wasser-Texturen generieren. Niedrige Cache-Hit-Rate während des gesamten Flugs wegen erstmaligem Überflug dieser Route.

### 9.4 Turn Detection

Nur 4 Turns erkannt (alle während Anflug ESSA, 11:26–11:28 UTC). Keine scharfen Turns während des Reiseflugs.

---

## 10. Vergleich Run G → Run H

### 10.1 Tuning-Effekte

| Änderung | Erwartung | Ergebnis | Bewertung |
|----------|-----------|----------|-----------|
| min_free_kbytes 1→2 GB | Mehr kswapd-Vorlauf | free avg 4,9 GB (vs. ~1,4 GB) | **Erreicht** |
| watermark_boost_factor 0→15000 | kswapd-Boost reaktiviert | kswapd Efficiency 94,5% | **Erreicht** |
| watermark_scale_factor 10→50 | Breitere Watermark-Lücke | Mehr Puffer vor Direct Reclaim | **Erreicht** |
| swappiness 1→10 | Graduelles Swap | pswpout 2,5% vs. 5,1% aktiv | **Erreicht** |
| NVMe PM QOS → 0 | 10–11ms Pattern eliminiert | 339 vs. 12.383 Events (-97,3%) | **Erreicht** |

### 10.2 Vergleichstabelle

| Metrik | Run G (Gesamt) | Run H (Gesamt) | Run G (Steady) | Run H (Steady) |
|--------|---------------|---------------|----------------|----------------|
| Dauer | 81 Min | 108 Min | 21 Min | 23 Min |
| Alloc Stalls max/s | 11.425 | **17.462** | 0 | **0** |
| Alloc Stall Samples | 42 | 117 | 0 | **0** |
| Direct Reclaim Events (bpftrace) | 71.160 | 84.140 | — | — |
| X-Plane Main Reclaim | 47.583 | **19.865 (-58%)** | — | — |
| Slow IO Events | 12.383 | **339 (-97%)** | — | — |
| Swap Peak MB | 18.156 | 12.045 | ~15.500 | ~8.930 |
| free avg MB | ~1.400 | **~4.880** | — | ~3.300 |
| kswapd Efficiency | 93,4% | **94,5%** | — | 94,4% |
| Dirty avg MB | 3,6 | 43,0* | ~2 | ~16 |
| GPU Throttle | 0 | — (no data) | 0 | — |
| DMA Fence Stalls | 0 | **0** | 0 | **0** |

*Dirty avg höher wegen SkunkcraftsUpdater-Writes und veränderten Btrfs-Commit-Timings.

### 10.3 Confounding Factor: SkunkcraftsUpdater

**Run H ist nicht direkt mit Run G vergleichbar**, weil SkunkcraftsUpdater in Run H parallel lief, in Run G nicht. Dieser eine Addon verursachte:
- 57,2% aller Direct-Reclaim-Events
- 21 GB IO-Reads
- avg 439% CPU
- Peak RSS 1,3 GB

Das überlagert die Tuning-Effekte massiv. Die X-Plane-Main-Thread-Reduktion von 58% ist trotzdem ein starkes Signal, weil sie unter **schlechteren** Bedingungen (mehr Konkurrenz) erreicht wurde.

---

## 11. Zusammenfassung: Was hat sich definitiv verbessert?

### Gesicherte Verbesserungen durch Run-H-Tuning

1. **NVMe IO-Latenz: 97% Reduktion der Slow-IO-Events**
   - `pm_qos_latency_tolerance_us=0` eliminiert das 10–11ms Power-State-Wake-Muster
   - Read-Latenz avg: 0,25 ms (vs. nvme1n1 p95=10,7 ms in Run G)
   - Das allein entfernt ~10ms aus jeder IO-sensitiven Kette

2. **kswapd-Headroom verdreifacht**
   - free avg: 4,9 GB (vs. 1,4 GB in Run G)
   - min_free_kbytes=2 GB gibt kswapd erheblich mehr Vorlauf
   - kswapd-Efficiency stabil bei 94,5%

3. **X-Plane Main Thread Reclaim: -58%**
   - 19.865 Events (vs. 47.583 in Run G)
   - Trotz stärkerer Konkurrenz durch SkunkcraftsUpdater
   - watermark_boost_factor=15000 + breitere scale_factor wirken

4. **Swap-Verhalten gradueller**
   - Erst bei Min 54 erste 1 GB Swap (vs. deutlich früher in Run G)
   - swappiness=10 verhindert Panik-Bursts
   - pswpout nur 2,5% der Samples aktiv (vs. 5,1%)

5. **bpftrace Map-Overflow: gelöst**
   - MAP_KEYS=65536 → keine Datenverluste mehr
   - trace_io_slow.log: 45 KB (vs. 697 MB in Run G!)

---

## 12. Handlungsempfehlungen & Maßnahmen

### 12.1 [ERLEDIGT] Skunkcrafts Updater Cronjob entfernt

Ein Cronjob (`0 */4 * * *`) startete den Skunkcrafts Updater alle 4 Stunden. Der 12:00-UTC-Lauf verursachte in 12 Sekunden den schlimmsten Stall-Cluster der Session (57% aller Reclaim-Events).

**Maßnahme:** Cronjob aus `crontab -e` entfernt. Gesamte User-Crontab bereinigt (auch zwei obsolete UnWetter-Archiv-Cronjobs entfernt).

### 12.2 [ERLEDIGT] Tuning persistent gemacht

Alle Run-H-Settings sind nun persistent über Reboot:

| Parameter | Datei | Wert |
|-----------|-------|------|
| swappiness | `/etc/sysctl.d/99-custom-tuning.conf` | **5** (von 10 auf 5 reduziert — Kompromiss Ramp-up-Dauer vs. Panik-Bursts) |
| min_free_kbytes | `/etc/sysctl.d/99-custom-tuning.conf` | 2097152 (2 GB) |
| watermark_boost_factor | `/etc/sysctl.d/99-custom-tuning.conf` | 15000 |
| watermark_scale_factor | `/etc/sysctl.d/99-custom-tuning.conf` | 50 |
| NVMe PM QOS | `/etc/udev/rules.d/61-nvme-pmqos.rules` | 0 (alle NVMe) |

Duplikate in der sysctl.conf wurden bereinigt.

### 12.3 [OFFEN] XEL File-Descriptor-Limit erhöhen

1.126 EMFILE-Fehler bei 10:44:24 UTC. XEL öffnet viele Dateien gleichzeitig (Tile-Cache + Network).

```bash
# Prüfen
ulimit -n
# Erhöhen (in /etc/security/limits.conf oder systemd unit)
* soft nofile 65536
* hard nofile 65536
```

Alternativ: `network_concurrent` weiter reduzieren (64→32).

### 12.4 [OFFEN] Route vorab cachen (Prewarm)

EDDH→ESSA über Ostsee = überwiegend uncached Territory. Die niedrige Cache-Hit-Rate erzwingt Live-Generation aller Wasser-/Küsten-Tiles, was den Ramp-up verlängert.

### 12.5 [OFFEN] max_tiles_per_cycle reduzieren (100→50)

XEL generiert bis zu 100 Tiles pro Prefetch-Zyklus. Reduktion auf 50 verlangsamt das Tile-Loading, reduziert aber Peak-Memory-Druck.

### 12.6 [INFO] Run I: Sauberer Vergleich

Gleiche Route (EDDH→ESSA), gleiche Settings, kein Skunkcrafts-Cronjob. Damit wird die reine Tuning-Wirkung messbar.

---

## 13. Offene Fragen

| Frage | Fehlende Daten | Vorschlag |
|-------|---------------|-----------|
| GPU-Throttling in Run H? | vram.csv leer (gamescope blockiert NVML) | `nvidia-smi` manuell in separatem Terminal starten |
| Sind die 53ms Write-Latenz-Spitzen Btrfs-Journal? | Keine Btrfs-Trace-Daten | `bpftrace` auf btrfs_commit_transaction tracen |
| Wie verhält sich das System bei warmem XEL-Cache? | Nur Cold-Route getestet | Gleiche Route nochmal fliegen |
| Effekt von swappiness=5 (vs. 10)? | Nur Run H mit 10 gemessen | Run I wird zeigen ob Ramp-up kürzer wird |

---

## 14. Raw Statistics Reference

### vmstat Gesamt vs. Steady State

| Metrik | Gesamt (6.427 Samples) | Steady (1.286 Samples, ab Min 86) |
|--------|------------------------|-----------------------------------|
| allocstall_s max | 17.462 | 0 |
| allocstall_s non-zero | 117 (1,8%) | 0 |
| pgscan_direct avg | 1.794 | 0 |
| pgscan_kswapd avg | 7.455 | 2.532 |
| pgsteal_kswapd efficiency | 94,5% | 94,4% |
| pswpin avg | 421 | 166 |
| pswpout avg | 738 | 240 |
| wset_refault_anon % active | 52,2% | 95,5% |
| wset_refault_file % active | 58,0% | 54,7% |
| compact_stall sum | 4.655 | 0 |
| thp_fault_fallback sum | 1.234 | 0 |
| pgfault avg | 171.428 | 33.092 |

### mem.csv

| Metrik | Start | Peak/Min | Ende |
|--------|-------|----------|------|
| used_mb | 33.042 | max 49.321 | 47.794 |
| free_mb | 29.713 | min 2.421 | 3.325 |
| available_mb | 65.437 | min 38.831 | 41.277 |
| swap_used_mb | 0 | max 12.045 | 8.934 |
| dirty_mb | 18,6 | max 449,8 | 1,0 |

### IO-Latenz

| Device | Read avg ms | Read max ms | Write avg ms | Write max ms |
|--------|------------|------------|-------------|-------------|
| nvme0n1 (990 PRO) | 0,25 | 2,0 | 10,2 | 53,7 |
| nvme1n1 (SN850X) | 0,26 | 9,1 | 3,5 | 53,6 |
| nvme2n1 (SN850X) | 0,25 | 8,0 | 3,6 | 53,8 |

### Per-Process RSS/CPU

| Prozess | Avg CPU% | Peak RSS GB | IO Read GB | IO Write GB |
|---------|---------|------------|-----------|------------|
| X-Plane Main | 283,5 | 19,1 | 84,9 | 0,4 |
| XEarthLayer | 89,8 | 21,2 | 41,1 | 22,7 |
| SkunkcraftsUpda | 439,0 | 1,3 | 21,2 | 0 |
