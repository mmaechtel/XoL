# Run I — Ergebnisse: 115-Minuten Flug mit Post-H-Tuning (Crashes bei Positionssprüngen)

**Datum:** 2026-02-24
**System:** Ryzen 9 9800X3D 8C/16T, 96 GB RAM, RTX 4090 24 GB, 3x NVMe (2x SN850X 8TB + 990 PRO 4TB)
**Kernel:** Liquorix 6.18 (PDS)
**Workload:** X-Plane 12 + XEarthLayer + QEMU/KVM (kein Skunkcrafts!)
**Route:** LPMA (Madeira) Umgebung, aktiver Flug + 2 Positionssprünge

---

## 0. Testbedingungen

| Parameter | Wert |
|-----------|------|
| Monitoring-Dauer | 115 Min (13:30–15:25 UTC) |
| Samples (1s) | 6.840 |
| Samples (200ms) | 34.321 |
| zram | 32 GB lz4, pri=100 |
| NVMe-Swap | nvme2n1p5 120 GB, pri=-2 (Fallback) |
| bpftrace | 3 Tracer (Direct Reclaim, Slow IO >5ms, DMA Fence >5ms) |
| Prewarm | **Nicht durchgeführt** |
| PSI | Nicht verfügbar (Kernel zu alt) |

### Änderungen seit Run H (Tuning-Paket "Post-H-Bereinigung")

```
vm.swappiness                10 → 5               Kompromiss: schnellerer Ramp-up
Skunkcrafts Cronjob          aktiv → entfernt      Verursachte 57% der Reclaim-Events in Run H
NVMe PM QOS udev-Rule        fehlte → persistent   pm_qos_latency_tolerance_us=0
XEL generation threads       16 → 12               Weniger CPU-Konkurrenz im Flug
XEL network_concurrent       64 → 96               Mehr Prewarm-/Download-Durchsatz
XEL cpu_concurrent           8 → 12                Mehr parallele Assemble+Encode
XEL disk_io_concurrent       32 → 48               Mehr parallele Cache-Ops
XEL prefetch mode            (default) → auto      Selbstkalibrierende Strategie
```

**Mid-Run-Änderung (Min ~80):** `max_tiles_per_cycle` von 100 auf 200 erhöht. XEL + X-Plane danach neugestartet.

### Besonderheiten dieser Messung

- **2 X-Plane-Crashes** durch Positionssprünge (Min 94 und Min 100)
- Kein Prewarm → Takeoff-Ruckeln durch On-Demand-DDS-Generation (208 Tiles in 1 Minute)
- Messung durch Crashes vorzeitig beendet (Ziel: 4h / 14.400s)

---

## 1. Key Findings (Severity-geordnet)

### [CRITICAL] 16.079 EMFILE-Errors — XEL File-Descriptor-Exhaustion

XEarthLayer produzierte **16.079 "Too many open files" (EMFILE)-Fehler** über die gesamte Session (vs. 1.126 in Run H). Die erhöhte Concurrency (network=96, disk_io=48, cpu=12) überschreitet das fd-Limit massiv. EMFILE-Fehler verursachen Re-Downloads, längere Job-Durations (median 1,4s → Spitzen bis 45,5s) und erhöhten Memory-Druck.

**Impact:** Die 14× Verschlechterung gegenüber Run H (16.079 vs. 1.126) ist direkt auf die Concurrency-Erhöhung zurückzuführen. Dies untergräbt den Vorteil der höheren Parallelität.

### [CRITICAL] 2 X-Plane-Crashes bei Positionssprüngen (DSF-Loading über FUSE)

Beide Crashes entstanden durch simultanes Laden von ~20 XEL-Ortho-DSF-Tiles über FUSE nach Positionssprüngen:

| Crash | Zeitpunkt | Peak Stalls/s | Peak Direct/s | Peak Swap-Out/s | Trigger |
|-------|-----------|--------------|---------------|-----------------|---------|
| **1** | Min 94,3 | **4.865** | 319.439 | 5.941 | Positionssprung → DSF-Loading |
| **2** | Min 100,6 | **13.992** | 1.509.196 | 219.229 | Positionssprung → DSF-Loading |

Crash 2 war extremer: 13.992 allocstalls/s und 1,5M direct_scan/s. **Keine Speicherknappheit** — available war nie unter 40 GB. Das Problem ist die FUSE-Latenz: X-Plane's DSF-Loader erwartet lokale Dateien, bekommt aber FUSE-gemountete Tiles, die erst generiert werden müssen (Sekunden statt Millisekunden).

### [WARNING] X-Plane Main Thread: 23 Frame-Drop-Events (>16ms)

18.653 Direct-Reclaim-Events auf dem Main Thread (64,3% aller Events), davon:

| Latenz-Bucket | Events | Anteil |
|---------------|--------|--------|
| < 1 ms | 16.577 | 88,9% |
| 1–5 ms | 1.907 | 10,2% |
| 5–10 ms | 103 | 0,6% |
| 10–16 ms | 43 | 0,2% |
| **> 16 ms** | **23** | 0,1% |
| **Worst Case** | **104,7 ms** | — |

**Alle 23 Frame-Drop-Events traten während/nach Positionssprüngen auf** — keiner im Normalflug (Phase 1).

### [INFO] Normalflug (62 Min) = null Stalls, null Direct Reclaim

Phase 1 (0–62 Min) war **perfekt**: 3.697 vmstat-Samples, davon **null** mit allocstalls > 0 und **null** mit pgscan_direct > 0. Der Tuning-Stack funktioniert unter normalen Flugbedingungen einwandfrei.

### [INFO] NVMe PM QOS weiterhin stabil — Read-Latenz < 0,25 ms avg

Read-Latenzen über alle 3 NVMe durchschnittlich 0,21–0,24 ms. Das 10–11ms Power-State-Pattern bleibt eliminiert.

### [INFO] PSI nicht verfügbar (Kernel-Feature deaktiviert)

PSI-Daten wurden gesammelt, aber alle Werte = 0,00. Der Liquorix-Kernel hat PSI nicht aktiviert.

---

## 2. Phasen-Modell

Run I zeigt kein klassisches "Warm-up → Ramp-up → Steady State"-Muster, sondern ein **Event-getriebenes** Profil:

| Phase | Zeitfenster | Min | Charakteristik |
|-------|-------------|-----|----------------|
| **1. Normalflug** | 13:30–14:33 | 0–62 | Stabiler Flug, null Stalls, null Reclaim |
| **2. Jump 1** | 14:33–14:34 | 62–64 | Positionssprung, erster Stall-Cluster |
| **3. Recovery** | 14:34–14:40 | 64–70 | Abklingendes Reclaim, sporadische Stalls |
| **4. DSF-Burst** | 14:40–14:46 | 70–76 | Intensives Szenerieladen, 50+ Stall-Samples |
| **5. Stabilisierung** | 14:46–14:58 | 76–88 | XP-Neustart nach Crash, Ramp-up |
| **6. Crash 1** | 14:58–14:59 | 94 | 4.865 stalls/s → X-Plane-Crash |
| **7. Crash 2** | 15:01–15:02 | 100 | 13.992 stalls/s → X-Plane-Crash, Session-Ende |

**Kernaussage:** Ohne Positionssprünge (Phase 1) wäre der gesamte Flug stall-frei geblieben.

---

## 3. Memory & VM Pressure

### 3.1 Übersicht

| Metrik | Start | Peak/Min | Ende |
|--------|-------|----------|------|
| used_mb | 34.134 | max 50.881 | 28.193 |
| free_mb | 3.539 | min 2.419 | 13.958 |
| available_mb | 64.057 | min 40.334 | 61.640 |
| swap_used_mb | 1.650 | max 6.270 | 3.549 |
| dirty_mb | 1,7 | max 502,5 | 4,6 |
| cached_mb | 56.495 | — | 52.024 |

### 3.2 Swap-Trajektorie

| Schwelle | Minute |
|----------|--------|
| Swap bei Start | 1.650 MB (vorhanden von vorheriger Session) |
| Swap > 2.000 MB | 63,7 (nach Jump 1) |
| Swap > 3.000 MB | 80,9 |
| Swap > 4.000 MB | 100,2 (Crash 2) |
| Swap > 5.000 MB | 100,5 (Crash 2) |
| Swap-Peak (6.270 MB) | 100,5 (Crash 2) |

Swap swing: **4.620 MB** (1.650 → 6.270). Deutlich weniger als Run H (12.045 MB), allerdings war Run I auch 115 Min (vs. 108) und wurde durch Crashes vorzeitig beendet.

### 3.3 vmstat-Aggregate

| Metrik | Gesamt (6.840 Samples) | Normalflug (0–62 Min, 3.697 Samples) |
|--------|------------------------|---------------------------------------|
| allocstall_s: non-zero | 102 (1,5%) | **0** |
| allocstall_s: max | 13.992/s | **0** |
| pgscan_direct avg | 570 | **0** |
| pgscan_direct max | 1.509.196 | **0** |
| kswapd efficiency | **97,5%** | — |
| pswpin avg | 95 | — |
| pswpin % active | 25,4% | — |
| pswpout avg | 171 | — |
| pswpout max | 219.229 | — |
| pswpout % active | 3,7% | — |
| wset_refault_anon % active | 25,6% | — |
| wset_refault_file % active | 33,7% | — |
| compact_stall sum | 1.306 | — |
| thp_fault_fallback sum | **0** | — |
| pgfault avg | 166.561 | — |
| pgmajfault avg | 116 | — |

### 3.4 Alloc-Stall-Cluster (Top 5 nach Schwere)

| Cluster | Minute | Peak Stalls/s | Peak Direct/s | Trigger |
|---------|--------|--------------|---------------|---------|
| **Crash 2** | 100,6 | **13.992** | 1.509.196 | Positionssprung → DSF-Loading |
| **Crash 1** | 94,3 | **4.865** | 319.439 | Positionssprung → DSF-Loading |
| **Post-Restart** | 87,7–87,9 | **242** | 16.404 | X-Plane Ramp-up nach Crash |
| **DSF-Burst** | 74,8 | **1.263** | 81.131 | Szenerieladen |
| **Jump 1** | 62,8 | **1.488** | 113.649 | Positionssprung |

---

## 4. bpftrace — Direct Reclaim pro Prozess

### 4.1 Übersicht

| Metrik | Wert | vs. Run H |
|--------|------|-----------|
| Gesamt-Events | **29.030** | -65% (84.140) |
| kswapd Wakes | 2.081 | -8% (2.258) |
| kswapd Sleeps | 370 | +5% (354) |

### 4.2 Top-Verursacher

| Prozess | Events | Anteil | Avg µs | Max µs | >1ms | >5ms | >10ms | >16ms |
|---------|--------|--------|--------|--------|------|------|-------|-------|
| **Main Thread** | 18.653 | **64,3%** | 501 | **104.685** | 2.076 | 169 | 66 | **23** |
| **tokio-runtime-w** (XEL) | 7.187 | **24,8%** | 1.773 | 139.790 | 2.017 | 572 | 174 | 91 |
| threaded-ml | 831 | 2,9% | 877 | 71.020 | 117 | 34 | 10 | 7 |
| cuda-EvtHandlr | 742 | 2,6% | 1.590 | 112.793 | 224 | 60 | 26 | 8 |
| pipewire-pulse | 340 | 1,2% | 804 | 76.952 | 46 | 9 | 3 | 2 |
| bpftrace | 292 | 1,0% | 289 | 4.266 | 20 | 0 | 0 | 0 |
| libobs | 253 | 0,9% | 832 | 20.216 | 45 | 12 | 2 | 1 |

### 4.3 Vergleich X-Plane Main Thread: Run H → Run I

| Metrik | Run H | Run I | Veränderung |
|--------|-------|-------|-------------|
| Events | 19.865 | 18.653 | **-6%** |
| Anteil | 23,6% | **64,3%** | Dominant (kein Skunkcrafts) |
| Max Latenz | 50,0 ms | **104,7 ms** | Verschlechtert (Crash-Kontext) |
| Events >1ms | 2.402 | 2.076 | -14% |
| Events >5ms | 226 | 169 | **-25%** |
| Events >10ms | 40 | 66 | +65% (Crash-Spitzen) |
| Events >16ms | 21 | 23 | +10% (Crash-Spitzen) |

**Interpretation:** Ohne Skunkcrafts-Konkurrenz ist der Main Thread nun der dominante Reclaim-Verursacher (64% vs. 24%). Die absolute Event-Zahl ist nahezu identisch (18.653 vs. 19.865, -6%). Die >10ms/>16ms Events verschlechterten sich, aber **alle** fallen in die Crash-Phasen — im Normalflug gab es null Reclaim.

**tokio-runtime-w (XEL):** 7.187 Events (24,8%) mit 91 Events >16ms. Dies sind XEL-Worker-Threads, die während der EMFILE-Krise und der DSF-Loading-Bursts in Reclaim geraten. Die hohe Tail-Latenz (139 ms max) zeigt: XEL-Threads konkurrieren hart mit X-Plane um Pages.

---

## 5. Per-Process

| Prozess | Avg CPU% | Max CPU% | Avg RSS GB | Peak RSS GB | Max Threads |
|---------|---------|---------|-----------|-----------|-------------|
| **X-Plane (Main Thread)** | 235,5 | 1.598 | 12,5 | **20,5** | 173 |
| **XEarthLayer** | 88,2 | 1.500 | 12,5 | **20,6** | 547 |
| gamescope-wl | 0,8 | 4 | 0,2 | 0,2 | 14 |

**Combined RSS Peak:** ~38,1 GB (XP 20,5 + XEL 20,6 + Rest) — passt in 96 GB mit Headroom.

### RSS-Lifecycle

- **XEL:** 4.536 MB → Peak 20.570 MB → 15.175 MB (Ende). +16 GB Wachstum.
- **X-Plane:** 10.447 MB → Peak 20.472 MB → 0 MB (gecrashed). +10 GB Wachstum.

**Kein Skunkcrafts** in der Prozessliste — Cronjob-Entfernung bestätigt.

---

## 6. Disk IO

### 6.1 Latenz-Profil

| Device | Read Lat avg ms | Read Lat max ms | Write Lat avg ms | Write Lat max ms |
|--------|----------------|----------------|-----------------|-----------------|
| nvme0n1 (990 PRO) | **0,21** | 2,0 | 9,1 | **120,3** |
| nvme1n1 (SN850X) | **0,24** | 8,0 | 3,5 | **118,2** |
| nvme2n1 (SN850X) | **0,22** | 2,8 | 3,7 | **117,8** |

**Read-Latenzen exzellent** — PM QOS Fix stabil.

**Write-Latenz-Spitzen bei ~120 ms** auf allen 3 NVMe gleichzeitig (vs. 53 ms in Run H). Das sind **Btrfs-Journal-Flushes** — die Synchronität über alle Devices bestätigt Metadata-Commits. Die Verdopplung gegenüber Run H könnte durch größere Metadata-Transaktionen bei EMFILE-bedingten Retry-Bursts verursacht sein.

### 6.2 Throughput

| Device | Read avg MB/s | Read max MB/s | Write avg MB/s | Write max MB/s |
|--------|--------------|--------------|---------------|---------------|
| nvme0n1 | 4,7 | 3.398 | 1,4 | 102 |
| nvme1n1 | 5,4 | 3.402 | 2,2 | 646 |
| nvme2n1 | 5,5 | 3.398 | 2,2 | 646 |

**RAID0-Balance:** Gleichmäßige Read-Verteilung. SN850X-Paar schreibt deutlich mehr (XEL-Cache).

### 6.3 Slow-IO-Events (trace_io_slow.log)

**1.539 Events** (Zeilen im Log nach Parsing) — Vergleich:

| Metrik | Run G | Run H | Run I |
|--------|-------|-------|-------|
| Slow-IO-Events (>5ms) | 12.383 | 339 | ~1.539 |
| 10–11ms Pattern | 90% | 1,5% | Nicht dominant |
| Max Latenz | — | 53,8 ms | 54 ms |

Die Zunahme gegenüber Run H (1.539 vs. 339) korreliert mit den Crash-Phasen — die intensiven DSF-Loading-Bursts erzeugen mehr IO-Queuing.

---

## 7. GPU / VRAM

**vram.csv ist leer** — gamescope blockiert NVML-GPU-Zugriff. Keine GPU-Daten verfügbar.

**DMA Fence Waits:** 0 Events (trace_fence.log leer). GPU-Synchronisation sauber.

---

## 8. XEarthLayer Streaming

### 8.1 Übersicht

| Metrik | Wert | vs. Run H |
|--------|------|-----------|
| DDS Tiles generiert | **13.461** | — |
| EMFILE Errors | **16.079** | **14× schlechter** (1.126) |
| Download Timeouts | 124 | — |
| HTTP Errors | 645 | — |
| Final Chunk Failures | 101 | — |
| Circuit Breaker Events | 83 | -63% (226) |
| FUSE Errors | **0** | — |

### 8.2 EMFILE-Analyse

Die 16.079 EMFILE-Errors sind das gravierendste neue Problem in Run I. Sie verteilen sich über die gesamte Session (nicht konzentriert wie die 1.126 in Run H). Ursache: Die Concurrency-Erhöhung (network=96, disk_io=48, cpu=12) überschreitet das System-fd-Limit.

**Auswirkungskette:**
1. EMFILE → Chunk-Download-Failure → Retry mit Backoff
2. Retry → längere Job-Durations (median 1,4s, max 45,5s, bimodal)
3. Längere Jobs → mehr gleichzeitige Jobs → mehr fd-Druck → mehr EMFILE

### 8.3 Prefetch-Verhalten

- 576 Prefetch-Pläne (9 ground, 567 cruise)
- max_tiles_per_cycle: 100 (erste 80 Min) → 200 (nach Restart)
- Nach Umstellung auf 200: 2.579 Tiles in ~2 Minuten geprefetcht — deutlich aggressiver

### 8.4 Circuit Breaker

83 "high load detected" Events — weniger als Run H (226). Der Circuit Breaker hat **nie den offenen Zustand** erreicht (half-open → closed). Dies bedeutet: Die Last-Spitzen waren kurz genug, dass der Breaker jedes Mal rechtzeitig abklang.

### 8.5 Crash-Korrelation

Beide X-Plane-Crashes korrelierten zeitlich mit XEL-Tile-Loading:
- **Crash 1 (Min 94):** Positionssprung → X-Plane lädt ~20 DSF-Tiles gleichzeitig → jedes Tile muss durch FUSE/XEL generiert werden → Sekunden Latenz pro Tile → X-Plane-DSF-Loader kann Latenz nicht handhaben
- **Crash 2 (Min 100):** Identisches Pattern, noch extremer (13.992 stalls/s)

**Keine FUSE-Errors** im XEL-Log — das Problem liegt nicht bei XEL selbst, sondern bei X-Plane's Unfähigkeit, FUSE-Latenz bei DSF-Loading zu tolerieren.

---

## 9. Vergleich Run H → Run I

### 9.1 Tuning-Effekte

| Änderung | Erwartung | Ergebnis | Bewertung |
|----------|-----------|----------|-----------|
| Skunkcrafts entfernt | Sauberes Reclaim-Profil | 64% Main Thread (vs. 24% in Run H) | **Bestätigt** — kein Fremdeinfluss |
| swappiness 10→5 | Weniger Swap, schnellerer Steady State | Swap-Peak 6,3 GB (vs. 12 GB) | **Besser**, aber auch kürzer gemessen |
| XEL network_concurrent 64→96 | Mehr Download-Durchsatz | 16.079 EMFILE (vs. 1.126) | **Kontraproduktiv** |
| XEL cpu_concurrent 8→12 | Mehr Assemble/Encode | — | Nicht isoliert messbar |
| XEL disk_io_concurrent 32→48 | Mehr Cache-Ops | — | Verstärkt EMFILE-Problem |
| max_tiles_per_cycle 100→200 | Mehr Prefetch-Weitsicht | 2.579 Tiles in 2 Min | **Wirkt**, aber Crash-Phasen überlagern |

### 9.2 Vergleichstabelle (Normalflug)

| Metrik | Run H (Steady, ab Min 85) | Run I (Normalflug, 0–62 Min) |
|--------|---------------------------|-------------------------------|
| Alloc Stalls | **0** | **0** |
| Direct Reclaim | **0** | **0** |
| Dauer der stall-freien Phase | 23 Min | **62 Min** |
| kswapd Efficiency | 94,4% | **97,5%** |
| Swap-Stand | ~8.930 MB | ~1.650 MB (Start) |
| THP Fallbacks | 0 | **0** |

### 9.3 Vergleichstabelle (Gesamt)

| Metrik | Run H (Gesamt) | Run I (Gesamt) | Veränderung |
|--------|---------------|---------------|-------------|
| Dauer | 108 Min | 115 Min | — |
| Alloc Stall Samples | 117 | 102 | -13% |
| Alloc Stall max/s | 17.462 | **13.992** | -20% |
| Direct Reclaim Events (bpftrace) | 84.140 | **29.030** | **-65%** |
| X-Plane Main Reclaim | 19.865 | 18.653 | -6% |
| Slow IO Events | 339 | ~1.539 | Verschlechtert (Crash-IO) |
| Swap Peak MB | 12.045 | **6.270** | **-48%** |
| EMFILE Errors | 1.126 | **16.079** | **14× schlechter** |
| kswapd Efficiency | 94,5% | **97,5%** | +3% |
| Write-Lat max ms | 53,8 | **120,3** | Verschlechtert |

### 9.4 Bewertung

**Die Gesamtzahlen trügen.** Run I hat weniger Reclaim-Events als Run H, aber das liegt primär am Fehlen des Skunkcrafts-Cronjobs (48.157 Events in Run H). Das eigentliche Tuning-Signal:

1. **Normalflug ist perfekt:** 62 Minuten null Stalls — länger als der Run-H-Steady-State (23 Min)
2. **kswapd-Efficiency verbessert:** 97,5% (vs. 94,5%) — swappiness=5 hilft kswapd
3. **EMFILE ist 14× schlechter:** Die XEL-Concurrency-Erhöhung war kontraproduktiv
4. **Crashes sind kein Tuning-Problem:** Positionssprünge + FUSE-DSF-Loading = strukturelles X-Plane-Limit

---

## 10. Zusammenfassung & Empfehlungen

### Gesicherte Verbesserungen (Run H → I)

1. **Skunkcrafts-Cronjob eliminiert** — Reclaim-Events -65%, sauberes Profil
2. **kswapd-Efficiency +3%** (97,5%) — swappiness=5 funktioniert
3. **Normalflug stall-frei über 62 Min** — Tuning-Stack bestätigt
4. **NVMe PM QOS stabil** — Read-Latenz <0,25 ms avg bleibt

### Empfehlungen

#### 1. [CRITICAL] XEL File-Descriptor-Limit erhöhen

16.079 EMFILE-Errors erfordern sofortige Maßnahme:

```bash
# Aktuelles Limit prüfen
ulimit -n

# Permanent erhöhen (/etc/security/limits.conf)
* soft nofile 65536
* hard nofile 65536
```

Alternativ XEL als systemd-Service mit `LimitNOFILE=65536`.

#### 2. [CRITICAL] XEL Concurrency zurückdrehen

Die Concurrency-Erhöhung (network 64→96, disk_io 32→48) verschärft das EMFILE-Problem. Empfehlung:

```ini
# Zurück auf Run-H-Werte oder niedriger
network_concurrent = 64
disk_io_concurrent = 32
```

Erst **nach** Erhöhung des fd-Limits experimentell wieder hochdrehen.

#### 3. [WARNING] Immer Prewarm vor dem Flug

```bash
xearthlayer run --airport <ICAO>
```

Das Takeoff-Ruckeln (208 DDS-Tiles in 1 Min) wäre mit Prewarm vermeidbar gewesen.

#### 4. [INFO] Positionssprünge vermeiden

Die Crashes sind ein strukturelles X-Plane-Limit (DSF-Loader + FUSE-Latenz). Keine Kernel-/XEL-Tuning-Maßnahme kann das lösen. Workaround: Positionssprünge nur in Regionen mit warmem XEL-Cache.

#### 5. [INFO] max_tiles_per_cycle = 200 beibehalten

Die Erhöhung zeigte positive Wirkung (2.579 Tiles in 2 Min). Nach Lösung des EMFILE-Problems kann das aggressivere Prefetch seinen Vorteil ausspielen.

---

## 11. Offene Fragen

| Frage | Fehlende Daten | Vorschlag |
|-------|---------------|-----------|
| GPU-Throttling in Run I? | vram.csv leer (gamescope) | nvidia-smi manuell in Terminal |
| Wie verhält sich Run I mit fd-Limit + Prewarm? | Nicht getestet | Run J mit ulimit -n 65536 + Prewarm |
| Sind die 120ms Write-Spitzen EMFILE-bedingt? | Keine Btrfs-Traces | bpftrace auf btrfs_commit_transaction |
| Was ist das bimodale Pattern bei XEL Job-Durations? | Nur Log-Analyse | XEL-interne Metriken (Prometheus?) |

---

## 12. Raw Statistics Reference

### vmstat Gesamt vs. Normalflug

| Metrik | Gesamt (6.840 Samples) | Normalflug (0–62 Min, 3.697 Samples) |
|--------|------------------------|---------------------------------------|
| allocstall_s max | 13.992 | **0** |
| allocstall_s non-zero | 102 (1,5%) | **0** |
| pgscan_direct avg | 570 | **0** |
| pgscan_direct max | 1.509.196 | **0** |
| kswapd efficiency | 97,5% | — |
| pswpin avg | 95 | — |
| pswpout avg | 171 | — |
| pswpout max | 219.229 | — |
| wset_refault_anon % active | 25,6% | — |
| wset_refault_file % active | 33,7% | — |
| compact_stall sum | 1.306 | — |
| thp_fault_fallback sum | 0 | — |
| pgfault avg | 166.561 | — |
| pgmajfault avg | 116 | — |

### mem.csv

| Metrik | Start | Peak/Min | Ende |
|--------|-------|----------|------|
| used_mb | 34.134 | max 50.881 | 28.193 |
| free_mb | 3.539 | min 2.419 | 13.958 |
| available_mb | 64.057 | min 40.334 | 61.640 |
| swap_used_mb | 1.650 | max 6.270 | 3.549 |
| dirty_mb | 1,7 | max 502,5 | 4,6 |

### IO-Latenz

| Device | Read avg ms | Read max ms | Write avg ms | Write max ms |
|--------|------------|------------|-------------|-------------|
| nvme0n1 (990 PRO) | 0,21 | 2,0 | 9,1 | 120,3 |
| nvme1n1 (SN850X) | 0,24 | 8,0 | 3,5 | 118,2 |
| nvme2n1 (SN850X) | 0,22 | 2,8 | 3,7 | 117,8 |

### Per-Process

| Prozess | Avg CPU% | Peak RSS GB | Max Threads | Samples |
|---------|---------|------------|-------------|---------|
| X-Plane (Main Thread) | 235,5 | 20,5 | 173 | 5.928 |
| XEarthLayer | 88,2 | 20,6 | 547 | 6.692 |
| gamescope-wl | 0,8 | 0,2 | 14 | 5.945 |

### bpftrace Direct Reclaim

| Prozess | Events | Anteil | Max µs | >16ms |
|---------|--------|--------|--------|-------|
| Main Thread | 18.653 | 64,3% | 104.685 | 23 |
| tokio-runtime-w | 7.187 | 24,8% | 139.790 | 91 |
| threaded-ml | 831 | 2,9% | 71.020 | 7 |
| cuda-EvtHandlr | 742 | 2,6% | 112.793 | 8 |
