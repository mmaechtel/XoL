# Run J — Ergebnisse: 51-Minuten Flug über installierte Orthos, Freeze durch XEL Thread-Bomb

**Datum:** 2026-02-24
**System:** Ryzen 9 9800X3D 8C/16T, 96 GB RAM, RTX 4090 24 GB, 3x NVMe (2x SN850X 8TB + 990 PRO 4TB)
**Kernel:** Liquorix 6.18 (PDS)
**Workload:** X-Plane 12 + XEarthLayer + QEMU/KVM (mid-flight gestartet)
**Route:** LFMN (Nizza) → nordwärts über Italien/Schweiz/Süddeutschland (EDDS Stuttgart)
**Szenerie:** Überwiegend installierte Ortho4XP-Pakete — X-Plane bedient die meisten Anfragen lokal, XEL nur für Lücken

---

## 0. Testbedingungen

| Parameter | Wert |
|-----------|------|
| Monitoring-Dauer | 51 Min (16:00–16:51 UTC) |
| X-Plane lief seit | ~15:32 UTC (~28 Min vor Monitoring-Start) |
| Samples (1s) | 3.025 |
| Samples (200ms) | 15.129 |
| zram | 32 GB lz4, pri=100 |
| Prewarm | `xearthlayer run --airport LFMN` |
| Szenerie-Typ | Ortho4XP installiert (lokal), XEL nur Gap-Filler |

### Gleiche Settings wie Run I (keine Änderungen)

XEL-Config unverändert: threads=12, network_concurrent=96, cpu_concurrent=12, disk_io_concurrent=48, max_tiles_per_cycle=200, prefetch mode=auto.

### Besonderheiten dieser Messung

- **Installierte Ortho4XP-Pakete:** X-Plane lädt schwere DSF-Tiles (bis 2,3M Triangles) direkt von Disk — kein FUSE-Overhead
- **XEL als Gap-Filler:** Nur 316 Tiles für nicht abgedeckte Bereiche generiert
- **QEMU mid-flight gestartet:** virt-manager/libvirtd um 16:42:50 UTC gestartet (nach Freeze)
- **Freeze bei 16:39:10 UTC:** Gamescope-Bild eingefroren, Ton lief weiter, X-Plane bei 528% CPU
- **Kein X-Plane-Crash:** Prozess lief weiter, musste mit `kill -9` beendet werden

---

## 1. Key Findings (Severity-geordnet)

### [CRITICAL] XEL Thread-Bomb verursacht Render-Freeze

Um 16:36:48 UTC explodierte XEarthLayer von 36 auf **300 Threads** in 4 Sekunden und allokierte **9,4 GB RAM in 14 Sekunden** (316 DDS-Tiles = 3,35 GB Daten). Dies löste eine Reclaim-Kaskade aus:

| Sekunde | XEL Threads | XEL RSS MB | XEL CPU% |
|---------|-------------|-----------|---------|
| 16:36:48 | 36 | 325 | 2% |
| 16:36:51 | 230 | 1.080 | 585% |
| 16:36:52 | 243 | 5.087 | 1.012% |
| 16:36:57 | 296 | 8.479 | **1.015%** |
| 16:37:01 | 300 | **9.694** | 934% |
| 16:37:03 | 300 | 8.851 | **0%** (Threads tot) |

**Impact:** 8.652 Direct-Reclaim-Events in einer einzigen Sekunde (16:37:11). Kernel reclaimed 2,5 GB von X-Plane und pushte 2,3 GB nach Swap. X-Plane's Render-Pipeline geriet in einen Deadlock — ab 16:39:10 UTC spann die CPU bei 528% ohne Frames zu produzieren.

### [CRITICAL] X-Plane Render-Deadlock (kein GPU-Problem)

Ab 16:39:10 UTC war X-Plane in einem Spin-Loop:

| Metrik | Vor Freeze (16:39:09) | Im Freeze (16:39:10+) |
|--------|----------------------|----------------------|
| CPU% | 404 | **528–542** (konstant) |
| IO Read MB/s | 53 | **0,03** |
| RSS MB | 20.470 | 20.468–20.470 (statisch) |
| Context Switches/s | 58.711 | **27.629** |
| Page Faults/s | 13.536 | **227** |
| GPU State | P2 (aktiv) | **P5 (idle, 23%, 41W)** |

**Kein GPU-Fehler:** 0 DMA Fence Stalls, 0 Vulkan Errors, 0 Xid-Meldungen, kein `VK_ERROR_DEVICE_LOST`. Sound lief weiter (separater Thread). gamescope empfing keine Frames mehr (0% CPU). Der Freeze war ein **Software-Deadlock in X-Plane's Render-/Task-Pipeline**, vermutlich ausgelöst durch den plötzlichen Working-Set-Verlust (2,5 GB reclaimed).

### [WARNING] Periodische Stall-Bursts durch Ortho4XP DSF-Loading

81 Alloc-Stall-Samples über 51 Min — im Gegensatz zu Run I (0 Stalls in 62 Min). Ursache: X-Plane lud **installierte Ortho4XP DSF-Tiles** direkt von Disk. Diese Tiles sind sehr groß (bis 2,3M Triangles, 8s Ladezeit) und verursachen bei jedem Szeneriering-Wechsel (~alle 8-10 Min) einen Memory-Pressure-Burst.

| Burst | Minute | Peak Stalls/s | Trigger |
|-------|--------|--------------|---------|
| 1 | 3–5 | 190 | DSF-Ring +42/+44 |
| 2 | 9–10 | **4.643** | DSF-Ring +45 |
| 3 | 20 | **4.473** | DSF-Ring +46 |
| 4 | 27–28 | 2.100 | DSF-Ring +47 |
| 5 | 33 | 650 | DSF-Ring +47/+48 |
| 6 | 36–37 | **8.833** | DSF-Ring +48 (EDDS Stuttgart, 2,3M Tri) + **XEL Thread-Bomb** |

**Wichtig:** Diese Stalls kamen **nicht** von XEL-FUSE-Latenz (wie in Run I bei Crashes), sondern von X-Plane's eigenem DSF-Loading installierter Ortho4XP-Pakete. Die Ortho4XP-DSFs sind deutlich größer als Standard-DSFs und erzeugen mehr Memory-Druck beim Laden.

### [WARNING] Runloop-Backup: 25.338 Tasks

X-Plane's W/RLP-Warnings eskalierten bis auf **25.338 ausstehende Tasks** (est. runtime 564s) kurz vor dem Freeze. Peak früher im Flug: **119.238 Tasks** (est. 3.906s). Die Task-Queue war chronisch überlastet.

### [INFO] 0 EMFILE-Errors

Im Gegensatz zu Run I (16.079 EMFILE) produzierte Run J **null** EMFILE-Fehler. Erklärung: Der warme Ortho4XP-Cache bedeutete, dass XEL kaum Netzwerk-Downloads brauchte und wenig File-Descriptors öffnete.

### [INFO] NVMe IO exzellent

Nur 35 Slow-IO-Events (>5ms) über 51 Min. Read-Latenzen 0,37–0,50 ms avg. Kein 10–11ms Power-State-Pattern. PM QOS Fix stabil.

---

## 2. Phasen-Modell

| Phase | Zeitfenster (UTC) | Min | Charakteristik |
|-------|-------------------|-----|----------------|
| **1. DSF-Ramp-up** | 16:00–16:36 | 0–36 | Periodische Stall-Bursts alle 8–10 Min bei Ring-Wechseln |
| **2. XEL Thread-Bomb** | 16:36:48–16:37:12 | 36–37 | 300 Threads, +9,4 GB, 8.652 Reclaim-Events/s |
| **3. Degraded Recovery** | 16:37–16:39 | 37–39 | X-Plane bei reduzierter CPU (200–350%), letzte IO-Bursts |
| **4. Freeze** | 16:39:10–16:50 | 39–50 | CPU 528% Spin-Loop, 0 IO, GPU P5 Idle |
| **5. QEMU** | 16:42:50–16:50 | 43–50 | +5 GB RAM, Compaction-Krise (nach Freeze) |
| **6. Kill** | 16:50:26 | 50 | X-Plane per `kill -9` beendet |

**Kein Steady State erreicht.** Die Ortho4XP-DSF-Loading-Bursts verhinderten eine Stabilisierung, und der XEL-Thread-Bomb beendete den Flug vorzeitig.

---

## 3. Memory & VM Pressure

### 3.1 Übersicht

| Metrik | Start | Peak/Min | Ende |
|--------|-------|----------|------|
| used_mb | 25.827 | max 44.266 | 24.665 |
| free_mb | 5.822 | min 2.818 | 27.665 |
| available_mb | 63.697 | min 44.402 | 64.026 |
| swap_used_mb | 3.068 | max 10.774 | 5.223 |
| dirty_mb | 0,6 | max 17,2 | 1,2 |

### 3.2 Swap-Trajektorie

| Schwelle | Minute | Trigger |
|----------|--------|---------|
| 3.000 MB (Start) | 0 | Vorherige Session |
| 4.000 MB | 10,6 | DSF-Ring +45 |
| 5.000 MB | 20,5 | DSF-Ring +46 |
| 7.000 MB | 28,5 | DSF-Ring +47 |
| 9.000 MB | 37,0 | DSF-Ring +48 + XEL Bomb |
| **10.774 MB (Peak)** | 43,3 | QEMU Balloon |

Swap-Wachstumsrate korreliert direkt mit DSF-Loading-Bursts: +157 MB/min (Min 10–15), +369 MB/min (Min 20–25), +397 MB/min (Min 35–40).

### 3.3 vmstat-Aggregate

| Metrik | Gesamt (3.025 Samples) |
|--------|------------------------|
| allocstall_s: non-zero | 81 (2,7%) |
| allocstall_s: max | **8.833** |
| pgscan_direct avg | 2.122 |
| pgscan_direct max | 1.293.750 |
| kswapd efficiency | **97,5%** |
| pswpin avg | 284, active 68,4% |
| pswpout avg | 853, max 563.275, active 5,4% |
| wset_refault_anon % active | 17,7% |
| wset_refault_file % active | 82,3% |
| compact_stall sum | **6.711** (alle in Min 42–43, QEMU) |
| thp_fault_fallback sum | **1.898** (alle in Min 42–43, QEMU) |

**Chronisches Swap-In:** 68,4% aller Samples hatten pswpin > 0 — Working Set passt nicht komplett in RAM. Evicted Pages werden sofort wieder gebraucht (Anon Refaults). Dies war in Run I nicht der Fall (pswpin active nur 25,4%).

---

## 4. bpftrace — Direct Reclaim pro Prozess

### 4.1 Übersicht

| Metrik | Wert | vs. Run I |
|--------|------|-----------|
| Gesamt-Events | **40.926** | +41% (29.030) |
| kswapd Wakes | 1.035 | -50% (2.081) |
| kswapd Sleeps | 182 | -51% (370) |
| Wake/Sleep Ratio | **5,7:1** | Schlechter (= kswapd kommt nicht nach) |

### 4.2 Top-Verursacher

| Prozess | Events | Anteil | Avg µs | Max µs | >1ms | >5ms | >10ms | >16ms |
|---------|--------|--------|--------|--------|------|------|-------|-------|
| **Main Thread** (X-Plane) | 32.600 | **79,7%** | 437 | 71.348 | 2.140 | 32 | 3 | **2** |
| cuda-EvtHandlr | 2.258 | 5,5% | 526 | 74.385 | 227 | 5 | 2 | 2 |
| CPU 0/KVM | 1.740 | 4,3% | 623 | 2.097 | 315 | 0 | 0 | 0 |
| bpftrace | 653 | 1,6% | 416 | 5.558 | 45 | 3 | 0 | 0 |
| threaded-ml | 399 | 1,0% | 525 | 3.475 | 58 | 0 | 0 | 0 |
| CPU 1/KVM | 393 | 1,0% | 565 | 1.647 | 29 | 0 | 0 | 0 |
| pipewire-pulse | 392 | 1,0% | 494 | 4.372 | 36 | 0 | 0 | 0 |
| tokio-runtime-w (XEL) | 251 | 0,6% | 549 | 4.772 | 11 | 0 | 0 | 0 |

### 4.3 Vergleich Main Thread: Run I → Run J

| Metrik | Run I | Run J | Veränderung |
|--------|-------|-------|-------------|
| Events | 18.653 | **32.600** | **+75%** |
| Anteil | 64,3% | **79,7%** | Noch dominanter |
| Max Latenz | 104,7 ms | **71,3 ms** | Besser (kein Crash-Kontext) |
| Events >1ms | 2.076 | 2.140 | +3% |
| Events >16ms | 23 | **2** | **-91%** |

**Interpretation:** Mehr Events als Run I (32.600 vs. 18.653), aber **weniger extreme Tail-Latenz** (nur 2 Events >16ms vs. 23). Die Events verteilen sich über die gesamte Session durch die periodischen DSF-Loading-Bursts — nicht konzentriert in Crash-Phasen wie bei Run I.

**tokio-runtime-w (XEL) nur 251 Events (0,6%)** — bestätigt, dass XEL in Run J kaum Memory-Druck erzeugte (warmer Ortho4XP-Cache). In Run I waren es 7.187 (24,8%).

---

## 5. Per-Process

| Prozess | Avg CPU% | Max CPU% | Avg RSS GB | Peak RSS GB | Max Threads |
|---------|---------|---------|-----------|-----------|-------------|
| **X-Plane (Main Thread)** | 423,7 | 1.335 | 20,1 | **23,5** | 98 |
| **XEarthLayer** | 4,3 | **1.015** | 3,1 | **9,7** | **300** |
| **QEMU** (ab Min 43) | 63,7 | 202 | 2,8 | **5,3** | 52 |
| gamescope-wl | 0,7 | 3 | 0,1 | 0,2 | 14 |

**XEL avg CPU nur 4,3%** — bestätigt: bei installierter Ortho4XP-Szenerie hat XEL fast nichts zu tun. Der Peak bei 1.015% war ausschließlich der Thread-Bomb-Burst.

**X-Plane Peak RSS 23,5 GB** — höher als in Run I (20,5 GB), weil installierte Ortho4XP-DSFs mehr Geometrie laden (bis 2,3M Triangles pro Tile).

---

## 6. Disk IO

### 6.1 Latenz-Profil

| Device | Read Lat avg ms | Read Lat max ms | Write Lat avg ms | Write Lat max ms |
|--------|----------------|----------------|-----------------|-----------------|
| nvme0n1 (990 PRO) | **0,50** | 1,2 | 1,1 | 4,0 |
| nvme1n1 (SN850X) | **0,45** | 1,0 | 0,4 | 6,1 |
| nvme2n1 (SN850X) | **0,37** | 1,5 | 0,3 | 6,1 |

**Exzellent.** Keine Write-Latenz-Spitzen wie in Run I (120ms). Bestätigt: die 120ms-Spitzen in Run I waren EMFILE-bedingt.

### 6.2 Throughput

| Device | Read avg MB/s | Read max MB/s | Write avg MB/s | Write max MB/s |
|--------|--------------|--------------|---------------|---------------|
| nvme0n1 | 17,0 | 3.390 | 0,0 | 0,1 |
| nvme1n1 | 17,4 | 3.398 | 0,3 | 157 |
| nvme2n1 | 19,0 | 3.392 | 0,5 | 157 |

**RAID0-Balance:** Gleichmäßige Reads. nvme0n1 schreibt fast nichts (reine Scenery-Reads).

### 6.3 Slow-IO-Events

**35 Events** — vernachlässigbar. Kein 10–11ms Pattern. Max 12ms.

---

## 7. XEarthLayer Streaming

### 7.1 Übersicht

| Metrik | Run J | Run I | Vergleich |
|--------|-------|-------|-----------|
| DDS Tiles | **316** | 13.461 | -98% (nur Lücken-Tiles) |
| EMFILE Errors | **0** | 16.079 | **Eliminiert** |
| Circuit Breaker Events | **4** | 83 | -95% |
| Download Timeouts | **0** | 124 | |
| HTTP Errors | **0** | 645 | |

### 7.2 Der Thread-Bomb-Burst (16:36:48–16:37:02)

Alle 316 Tiles wurden in einem einzigen 2-Minuten-Burst generiert (252 bei 16:36, 64 bei 16:37). Der Circuit Breaker detektierte die Last (4 Events, rate=54–61 vs. threshold=50), aber **hat nie den offenen Zustand erreicht** — der Burst war zu schnell und zu massiv.

**Frage:** Warum 316 Tiles auf einmal? Vermutlich flog X-Plane in eine Lücke der Ortho4XP-Abdeckung (Schweizer Alpen / Süddeutschland), und XEL musste plötzlich einen ganzen Ring generieren. Mit installiertem Ortho4XP war XEL die ganze Zeit bei ~4% CPU — bis zu diesem Moment.

### 7.3 Prefetch-Statistik

- 1.826 Prefetch-Pläne, 100% cruise-Strategie
- 200 tiles/cycle (max_tiles_per_cycle)
- Cache-Hit-Rate: sehr niedrig (skipped_cached=0 für 936 Pläne) — XEL zählt auch Ortho4XP-abgedeckte Tiles als "nicht gecached", weil sie nicht in XELs eigenem Cache sind

---

## 8. X-Plane Szenerie-Analyse

### 8.1 DSF-Loading-Profile

Die installierten Ortho4XP-DSFs sind erheblich größer als Standard-Szenerie:

| DSF Tile | Ladezeit | Triangles | Bemerkung |
|----------|----------|-----------|-----------|
| +48+009 (zOrtho4XP) | **8,27s** | **2.340.806** | Schwerster einzelner DSF-Load |
| +48+007 (zzXEL_ortho) | 6,57s | — | XEL Gap-Filler |
| +47+008 | 9,61s | — | Ortho4XP |
| +46+007 | 9,26s | — | Ortho4XP |

### 8.2 Runloop-Backup

78 W/RLP-Warnings, zwei Eskalationswellen:

1. **Elapsed 0:40–0:43:** Peak **119.238 Tasks** (est. 3.906s) — initiales Szenerieladen
2. **Elapsed 1:05–1:06:** Peak **25.338 Tasks** (est. 564s) — EDDS Stuttgart + XEL Burst → Freeze

### 8.3 Letzte Events vor Freeze

- 16:37:15 UTC: Airport LSPK geladen (letztes xplane_events.csv Event)
- 16:38:14 UTC: Letzte TEX-Warning (EDDS Stuttgart Texturen)
- 16:38:48 UTC: Letztes RLP-Warning (25.338 Tasks)
- 16:39:10 UTC: **Freeze** — keine weiteren Events, Logs, oder IO

---

## 9. Vergleich Run I → Run J

### 9.1 Grundlegende Unterschiede

| Aspekt | Run I | Run J |
|--------|-------|-------|
| Szenerie-Typ | XEL-generiert (FUSE) | **Ortho4XP installiert** (lokal) |
| XEL-Rolle | Primärer Tile-Provider | **Gap-Filler** (316 Tiles) |
| XEL CPU avg | 88,2% | **4,3%** |
| X-Plane RSS Peak | 20,5 GB | **23,5 GB** (größere DSFs) |
| Stall-Muster | 0 in Normalflug, Stalls nur bei Crashes | **Periodische Stalls alle 8–10 Min** |
| Ende | 2 Crashes (Positionssprünge) | **Freeze** (XEL Thread-Bomb) |

### 9.2 Vergleichstabelle

| Metrik | Run I (Gesamt) | Run J (Gesamt) |
|--------|---------------|---------------|
| Dauer | 115 Min | 51 Min |
| Alloc Stall Samples | 102 (1,5%) | 81 (2,7%) |
| Alloc Stall max/s | 13.992 | **8.833** |
| Direct Reclaim Events | 29.030 | **40.926** |
| Main Thread Reclaim | 18.653 (64%) | **32.600 (80%)** |
| Main Thread >16ms | 23 | **2** |
| kswapd Efficiency | 97,5% | **97,5%** |
| Swap Peak MB | 6.270 | **10.774** |
| pswpin active | 25,4% | **68,4%** |
| EMFILE Errors | 16.079 | **0** |
| XEL Tiles | 13.461 | **316** |
| Write-Lat max ms | 120,3 | **6,1** |
| Slow IO Events | ~1.539 | **35** |

### 9.3 Bewertung

**Run J zeigt ein anderes Lastprofil als Run I:**

- **Run I (XEL-dominiert):** Normalflug stall-frei, Probleme nur bei Extremereignissen (Positionssprünge, EMFILE). XEL erzeugt gleichmäßige Last.
- **Run J (Ortho4XP-dominiert):** Periodische Stall-Bursts bei jedem Szeneriering-Wechsel. X-Plane's eigenes DSF-Loading ist der Memory-Druck-Treiber. XEL ist fast idle — bis zum katastrophalen Thread-Bomb-Burst.

**Ortho4XP-DSFs sind schwerer als XEL-DSFs:** Die installierten Tiles haben bis zu 2,3M Triangles und 8s Ladezeit. Dies erzeugt mehr Memory-Druck pro Tile als XELs leichtere On-Demand-Tiles.

**Swap-In ist chronisch:** 68,4% der Samples haben aktives Swap-In (vs. 25,4% in Run I). Die größeren Ortho4XP-DSFs erzwingen häufigeres Faulting von zuvor evicted Pages.

---

## 10. Empfehlungen

### 1. [CRITICAL] XEL Circuit Breaker härter einstellen

Der Breaker hat bei 316 Tiles in 2 Min (9,4 GB RAM) **nicht** in den offenen Zustand geschaltet. Empfehlung:

```ini
# Aggressiveren Breaker
circuit_breaker_threshold = 30        # (war 50) — früher drosseln
circuit_breaker_open_ms = 200         # (war 500) — schneller auslösen
max_concurrent_jobs = 4               # (war 8) — weniger parallele Jobs
```

### 2. [WARNING] Ortho4XP-DSF-Last berücksichtigen

Installierte Ortho4XP-Pakete erzeugen mehr Memory-Druck als XEL-Tiles. Bei Routes über Ortho4XP-Szenerie:

- Längere Ramp-up-Phase einplanen
- Swap-Wachstum von ~400 MB/Min bei Ring-Wechseln ist normal
- System erreicht Steady State erst, wenn alle Ringe im Flugbereich geladen sind

### 3. [WARNING] QEMU nicht während des Flugs starten

QEMU allokierte 5 GB in 30 Sekunden und löste alle Compaction-Stalls (6.711) und THP-Fallbacks (1.898) der Session aus. Empfehlung: VMs vor X-Plane starten oder erst nach Landung.

### 4. [INFO] Write-Latenz-Spitzen in Run I waren EMFILE-bedingt

Run J bestätigt: ohne EMFILE (0 vs. 16.079) sinkt die Write-Latenz von 120ms auf 6ms. Die Lösung des EMFILE-Problems (fd-Limit + Concurrency zurückdrehen) wird auch die Write-Latenz in XEL-dominierten Flügen normalisieren.

---

## 11. Offene Fragen

| Frage | Fehlende Daten | Vorschlag |
|-------|---------------|-----------|
| Warum 316 Tiles auf einmal? | XEL-Lücke in Abdeckung? | Ortho4XP-Coverage-Map prüfen |
| Kann X-Plane nach Reclaim-Storm recovern? | Nur 1 Freeze beobachtet | In Run K gezielt Reclaim provozieren |
| Reicht CB-Threshold=30 gegen Thread-Bombs? | Nicht getestet | Run K mit angepasstem CB |
| GPU-Status während Freeze? | vram.csv leer | nvidia-smi in separatem Terminal |

---

## 12. Raw Statistics Reference

### vmstat

| Metrik | Gesamt (3.025 Samples) |
|--------|------------------------|
| allocstall_s max | 8.833 |
| allocstall_s non-zero | 81 (2,7%) |
| pgscan_direct avg | 2.122 |
| kswapd efficiency | 97,5% |
| pswpin avg | 284, active 68,4% |
| pswpout avg | 853, max 563.275, active 5,4% |
| compact_stall sum | 6.711 (Min 42–43, QEMU) |
| thp_fault_fallback sum | 1.898 (Min 42–43, QEMU) |

### mem.csv

| Metrik | Start | Peak/Min | Ende |
|--------|-------|----------|------|
| used_mb | 25.827 | max 44.266 | 24.665 |
| free_mb | 5.822 | min 2.818 | 27.665 |
| available_mb | 63.697 | min 44.402 | 64.026 |
| swap_used_mb | 3.068 | max 10.774 | 5.223 |

### IO-Latenz

| Device | Read avg ms | Read max ms | Write avg ms | Write max ms |
|--------|------------|------------|-------------|-------------|
| nvme0n1 (990 PRO) | 0,50 | 1,2 | 1,1 | 4,0 |
| nvme1n1 (SN850X) | 0,45 | 1,0 | 0,4 | 6,1 |
| nvme2n1 (SN850X) | 0,37 | 1,5 | 0,3 | 6,1 |

### bpftrace Direct Reclaim

| Prozess | Events | Anteil | Max µs | >16ms |
|---------|--------|--------|--------|-------|
| Main Thread | 32.600 | 79,7% | 71.348 | 2 |
| cuda-EvtHandlr | 2.258 | 5,5% | 74.385 | 2 |
| CPU 0/KVM | 1.740 | 4,3% | 2.097 | 0 |
| tokio-runtime-w | 251 | 0,6% | 4.772 | 0 |
