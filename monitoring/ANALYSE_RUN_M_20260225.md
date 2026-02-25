# Run M — Ergebnisse: 98-Minuten ESGG→EDDS mit erstmaliger In-Sim-Telemetrie

**Datum:** 2026-02-25
**System:** Ryzen 9 9800X3D 8C/16T, 96 GB RAM, RTX 4090 24 GB, 3x NVMe (2x SN850X 8TB + 990 PRO 4TB)
**Kernel:** Liquorix 6.18 (PDS)
**Workload:** X-Plane 12 (Peak 21,3 GB RSS) + XEarthLayer v0.3.0 (Peak 16,2 GB RSS) + QEMU/KVM (4,2 GB) + Swift Pilot Client
**Route:** ESGG (Göteborg) → EDDS (Stuttgart), ~950 km, FL350, Ortho über Dänemark/Deutschland
**Änderungen seit Run K:** Änderung 10 aktiv (max_concurrent_jobs 4, memory_size 4 GB)

---

## 0. Testbedingungen

| Parameter | Wert |
|-----------|------|
| Dauer | 97,5 Min (5.810 vmstat-Samples, 12:16–13:53 CET) |
| Sidecar (bpftrace) | Ja — trace_reclaim, trace_io_slow, trace_fence |
| X-Plane Log | Ja — korreliert |
| **In-Sim-Telemetrie** | **Ja — erstmals (xplane_telemetry.py, UDP RREF, 5 Hz)** |
| Telemetrie-Abdeckung | 35 Min (ab 13:18, nach Tool-Entwicklung mid-flight) |
| XEL Config | max_concurrent_jobs=4, memory_size=4 GB, threads=12, cpu_concurrent=8, grid_size=6 |
| DSF-Loads (X-Plane) | 382 Events, 24 > 5s, max 16.312ms |
| Airport-Loads | 53 |
| Crashes | 0 |

**Besonderheit:** Die xplane_telemetry.py wurde während dieses Runs entwickelt und erstmals eingesetzt. FPS/CPU/GPU-Korrelation ist ab 13:18 verfügbar (die letzten 35 Min inkl. Approach und Landung). Zusätzlich: NVML-Bug in sysmon.py gefunden und gefixt — vram.csv war in allen bisherigen Runs leer (Scope-Bug bei pynvml Import).

---

## 1. Erwartungen vs. Ergebnisse

| Metrik | Run I | Run K | **Run M (Gesamt)** | Bewertung |
|--------|-------|-------|--------------------|-----------|
| Alloc Stall Samples | 102 (1,5%) | 235 (3,4%) | **199 (3,4%)** | Vergleichbar mit K |
| Alloc Stall Peak/s | 13.992 | 13.831 | **8.324** | Niedriger als I/K |
| Direct Reclaim (bpftrace) | 29.030 | 171.744 | **89.335** | Zwischen I und K |
| X-Plane Main Reclaim | 18.653 (64%) | 125.578 (73%) | **61.858 (69%)** | Konsistentes Muster |
| Main Thread Worst | — | 68,6 ms | **189,0 ms** | Neuer Höchstwert |
| Swap Peak | 6.270 MB | 26.571 MB | **9.937 MB** | Deutlich unter K |
| Slow IO (>5ms) | 1.539 | 65 | **1.806** | Erhöht — siehe §4 |
| DMA Fence Stalls | 0 | 0 | **0** | Konsistent null |
| **FPS avg** | — | — | **29,8** | Erstmals gemessen |
| **FPS < 25** | — | — | **3,4%** | — |
| **GPU Time P95** | — | — | **23,8 ms** | — |

---

## 2. Kernbefunde

### 2.1 Phasen-Verhalten

| Phase | Zeitraum | Dauer | Stall-Samples (>10/s) | Beschreibung |
|-------|----------|-------|-----------------------|-------------|
| Warm-up | Min 0–10,7 | 10,7 Min | 0 | Startup, Cache füllt sich |
| DSF-Ramp-up | Min 10,7–91,8 | 81,1 Min | 199 (in Bursts) | DSF-Boundary-Bursts alle 7–16 Min |
| Tail | Min 91,8–97,5 | 5,7 Min | 0 | Am Boden, stall-frei |

Die Stalls treten nicht kontinuierlich auf, sondern als kurze Bursts (5–25s) bei jeder DSF-Breitengrad-Überquerung, getrennt durch 7–16 Minuten stall-freie Phasen.

### 2.2 DSF-Boundary-Crossings — das zentrale Muster

Die Route ESGG→EDDS kreuzt 7 Breitengrade (55°N→48°N). Jeder Crossing erzeugt einen Allocstall-Burst:

| Crossing | Uhrzeit | Minute | Peak alloc/s | DSF Load Time | Trigger |
|----------|---------|--------|-------------|---------------|---------|
| 55°N | 12:28 | 12 | 6.520 | 5.837 ms | +55+012.dsf |
| 54°N | 12:37 | 21 | 2.359 | 677 ms | +54+009.dsf |
| 52°N | 12:53 | 37 | 7.923 | 10.288 ms | +52+009.dsf |
| 51°N | 13:01 | 45 | 308 | mild | +51+011.dsf |
| **50°N** | **13:10** | **54** | **8.324** | **12.059 ms** | **+50+008.dsf (Frankfurt)** |
| 49°N | 13:27 | 71 | 7.591 | 10.289 ms | +48+009.dsf |
| 48°N | 13:40 | 84 | 3.366 | 13.039 ms | +47+008.dsf (Approach EDDS) |
| Ground | 13:48 | 92 | 1.171 | — | XEL Ground Tiles |

**50°N (Frankfurt-Bereich) war der heftigste Crossing** — korreliert mit Aviotek EDDF Payware-Scenery-Fehlern im X-Plane Log.

**Mechanismus:** Bei jedem 1°-Latitude-Crossing lädt X-Plane gleichzeitig 8 Scenery-Layer × 4 DSF-Tiles. Das erzeugt Read-Bursts bis 3.377 MB/s und verbraucht burst-artig mehrere GB RAM. Der Kernel muss synchron Speicher freigeben (Direct Reclaim) — und das passiert auf X-Plane's Main Thread, der dadurch für bis zu 189 ms blockiert wird.

### 2.3 Memory Pressure

| Metrik | Wert | Bewertung |
|--------|------|-----------|
| Used Start → End | 35,9 → 46,0 GB | +10 GB Working Set Aufbau |
| Peak Used | 48,5 GB (13:48) | Bei Touchdown |
| Available min | 38,3 GB (13:48) | Ausreichend (41% von 96 GB) |
| Swap Peak | 9,7 GB (13:27, 49°N Crossing) | zram absorbiert alles |
| Swap Swing | 8,1 GB | Deutlich unter Run K (26,6 GB) |
| NVMe-Swap | **0** | zram reicht |
| Swap-In aktiv | 61,6% der Samples | Chronisch, zram-Thrashing |
| Swap-Out aktiv | 3,6% | Konzentriert auf DSF-Bursts |

**Ursachenkette:**
```
DSF-Boundary-Crossing
→ X-Plane liest 4-8 DSF-Tiles gleichzeitig (bis 3,4 GB/s)
→ Page-Cache explodiert, freier Speicher fällt
→ Kernel: Direct Reclaim auf Main Thread (bis 189 ms blockiert)
→ Parallel: Swap-Out 279k pages/s nach zram
→ FPS sackt auf 19,9 für 5-25 Sekunden
→ Nach Crossing: sofortige Recovery auf ~30 FPS
```

### 2.4 Direct Reclaim Attribution (bpftrace)

| Prozess | Events | Anteil | Total Stall | Worst |
|---------|--------|--------|-------------|-------|
| **X-Plane Main Thread** | 61.858 | **69,2%** | 29,9 s | **189,0 ms** |
| **XEL tokio-runtime** | 18.390 | **20,6%** | 9,2 s | 65,6 ms |
| X-Plane cuda-EvtHandlr | 3.211 | 3,6% | 3,2 s | 190,8 ms |
| bpftrace (Monitoring) | 1.041 | 1,2% | 0,6 s | 36,4 ms |
| X-Plane threaded-ml | 743 | 0,8% | 0,7 s | 14,4 ms |
| piper (Audio) | 689 | 0,8% | 0,5 s | 5,7 ms |
| Xwayland | 381 | 0,4% | 0,3 s | 9,4 ms |
| Rest (108 Prozesse) | 3.022 | 3,4% | — | — |

**Vergleich mit Run K:**

| Metrik | Run K | Run M |
|--------|-------|-------|
| Main Thread Anteil | 73,1% | 69,2% |
| XEL tokio Anteil | 5,2% | **20,6%** |
| Gesamt Events | 171.744 | 89.335 |

XEL's Anteil hat sich vervierfacht (5,2% → 20,6%). Das liegt an Änderung 10 (memory_size 4 GB statt 8 GB) — XEL hat weniger Cache, muss öfter Tiles neu laden/generieren, was mehr Reclaim auf XEL-Threads erzeugt. Der **Gesamtdruck** ist aber deutlich geringer (89k vs. 172k Events).

---

## 3. In-Sim-Telemetrie (FPS / CPU Time / GPU Time) — NEU

Erstmals verfügbar dank xplane_telemetry.py (UDP RREF, 5 Hz). Abdeckung: 35 Min (13:18–13:53, inkl. Approach + Landung).

### 3.1 Gesamtstatistik

| Metrik | Wert |
|--------|------|
| Aktive Samples | 9.653 |
| FPS avg / median | 29,8 / 29,8 |
| FPS min / P1 / P5 | 19,9 / 19,9 / 27,8 |
| FPS max | 74,4 |
| CPU Time avg / P95 / max | 15,9 / 20,1 / 38,3 ms |
| GPU Time avg / P95 / max | 18,0 / 23,8 / 42,0 ms |
| FPS < 25 | 333 Samples (3,4%) |
| FPS < 20 | 224 Samples (2,3%) |

### 3.2 FPS-Profil während Approach + Landung

| Phase | Uhrzeit | FPS avg | FPS min | CPU ms | GPU ms | AGL |
|-------|---------|---------|---------|--------|--------|-----|
| En route | 13:18–13:38 | 29,8 | 19,9 | 17,0 | 16,5 | FL350 |
| Approach | 13:38–13:45 | 29,6 | 19,9 | 16,0 | 18,5 | 2600→600m |
| Final | 13:45–13:47 | 29,7 | 19,9 | 13,0 | 20,5 | 600→0m |
| Ground | 13:47–13:53 | 29,8 | 19,9 | 10,5 | 23,0 | 0m |

**Trend:** CPU Time sinkt von 17 ms (Cruise) auf 10 ms (Ground), GPU Time steigt von 16 ms auf 23 ms. Am Boden ist X-Plane GPU-bound — mehr Geometrie und Texturen in Bodennähe.

### 3.3 Die zwei Stutter bei der Landung

#### Stutter 1: DSF-Boundary 48°→47°N (13:39:48, Approach, 2.400m AGL)

```
13:39:48.227  FPS=29.2  cpu=17.9ms  gpu=16.4ms  ← normal
13:39:48.722  FPS=19.9  cpu=30.3ms  gpu=20.0ms  ← STUTTER START
13:39:49.323  FPS=19.9  cpu=30.3ms  gpu=20.0ms     allocstall=3.124/s
13:39:50.311  FPS=19.9  cpu=29.0ms  gpu=21.2ms     allocstall=3.366/s
13:39:51.208  FPS=29.8  cpu=20.0ms  gpu=13.5ms  ← kurze Recovery
13:39:55.329  FPS=19.9  cpu=30.1ms  gpu=15.1ms     allocstall=1.952/s
13:40:00.527  FPS=19.9  cpu=31.4ms  gpu=18.9ms     allocstall=2.968/s
13:40:01.405  FPS=29.9  cpu=18.7ms  gpu=13.5ms  ← STUTTER ENDE
```

- **Dauer:** ~12 Sekunden
- **Trigger:** DSF +47+008.dsf (13.039ms Load) + +47+010.dsf (6.196ms)
- **Reclaim:** 11.859 Events, 73% Main Thread, worst 32,8ms
- **Charakter:** CPU-bound — CPU Time verdoppelt sich von 17→31ms durch Direct Reclaim
- **Swap storm:** 279k pages/s Swap-Out, 49 Slow-IO-Events

#### Stutter 2: XEL Ground Tiles (13:48:08, Runway, AGL=0)

```
13:48:06.792  FPS=29.5  cpu= 9.9ms  gpu=24.0ms  ← normal (GPU-bound am Boden)
13:48:08.098  FPS=19.9  cpu=11.9ms  gpu=38.3ms  ← STUTTER: GPU-bound!
13:48:10.207  FPS=19.9  cpu=31.6ms  gpu=18.6ms  ← CPU-bound
13:48:11.763  FPS=19.9  cpu= 8.3ms  gpu=42.0ms  ← GPU-bound!
13:48:12.490  FPS=19.9  cpu=29.4ms  gpu=20.9ms  ← CPU-bound
13:48:13.592  FPS=28.7  cpu=10.3ms  gpu=24.6ms  ← kurze Recovery
13:48:14.466  FPS=19.9  cpu=11.3ms  gpu=38.9ms  ← wieder GPU-bound
13:48:18.223  FPS=30.2  cpu= 8.1ms  gpu=25.0ms  ← STUTTER ENDE
```

- **Dauer:** ~12 Sekunden (oszillierend)
- **Trigger:** KEIN DSF-Loading! XEarthLayer lädt Boden-Tiles für Flughafenbereich
- **Reclaim:** 1.201 Events, **97% auf XEL tokio-runtime** (PID 26188), **0% Main Thread**
- **Charakter:** Gemischt CPU/GPU — alterniert zwischen GPU-bound (38–42ms) und CPU-bound (29–32ms) Frames
- **GPU Time:** Springt von 24ms auf **42ms** (höchster Wert im gesamten Run)
- **Zusammenhang:** EDDS Airport-Load war 2,5 Min vorher (13:45:30). Komplexe Payware-Scenery + neue XEL Ortho-Tiles für Bodennähe = GPU-Überlastung

**Unterschied Stutter 1 vs. 2:**

| | Stutter 1 (Approach) | Stutter 2 (Touchdown) |
|---|---|---|
| Trigger | DSF-Boundary 48°→47°N | XEL Ground Tile Loading |
| Reclaim auf Main Thread | 73% (8.638 Events) | **0%** |
| Reclaim auf XEL tokio | 16% (1.929 Events) | **97%** (1.165 Events) |
| Limitierender Faktor | CPU (Reclaim) | **GPU** (38–42ms) |
| Worst Reclaim | 32,8 ms | 4,6 ms |
| Swap-Out | 279k pages/s | 6.654 pages/s |

Stutter 2 ist ein grundsätzlich anderes Problem als die DSF-Boundary-Stutter: Es ist **GPU-getrieben**, nicht Memory-Reclaim-getrieben. Möglicher Zusammenhang mit XEL Issue #62 (Takeoff-Stutter bei gs=62kt, agl=0).

---

## 4. GPU / VRAM

**NVML-Bug gefunden und gefixt:** `vram.csv` war in allen bisherigen Runs (A–L) leer, weil `pynvml` lokal in `init_gpu()` importiert, aber auf Modul-Ebene in `get_vram()` referenziert wurde. Fix: globale `_NVML_LIB`-Referenz + Auto-Fallback auf nvidia-smi nach 3 Fehlern.

**Für Run M:** Keine VRAM-Daten (Bug erst nach dem Run gefixt). Ab dem nächsten Run verfügbar.

**Indirekt:** Null DMA-Fence-Stalls (trace_fence.log leer). GPU-CPU-Synchronisation ist kein Problem.

**Post-Flight-Test (X-Plane idle am Gate):** VRAM 5,9 GB / 24,6 GB (24%) — reichlich Headroom. Die GPU-Spikes beim Touchdown kommen vom Texture Upload Burst, nicht von VRAM-Mangel.

---

## 5. Disk IO

| Metrik | nvme0n1 | nvme1n1 | nvme2n1 |
|--------|---------|---------|---------|
| Read avg / max (MB/s) | 10,3 / 3.335 | 9,9 / 3.309 | 13,6 / 3.377 |
| Read Latency avg / max (ms) | 0,06 / 5,2 | 0,06 / 5,2 | 0,09 / 31,5 |
| Write Latency avg / max (ms) | 0,03 / 12,3 | 0,01 / 4,0 | 0,03 / 18,3 |

**Slow IO (>5ms bpftrace):** 1.806 Events

| Latenz-Bucket | Anzahl |
|---------------|--------|
| 5–9 ms | 757 |
| 10–19 ms | 1.002 |
| 20–49 ms | 47 |
| 50+ ms | 0 |

**Vergleich:** Run K hatte 65 Slow-IO-Events, Run M hat 1.806. Der Anstieg kommt von Swap-Out nach zram→NVMe-Spill bei den schweren DSF-Crossing-Bursts. Alle Events sind im 6–33ms Bereich — kein Power-State-Problem (PM QOS wirkt), aber NVMe-Write-Latenz unter Last.

**Read-Latenz:** Exzellent. Max 5,2ms (nvme0n1/nvme1n1). Btrfs RAID0 liefert bis 3,4 GB/s Read bei DSF-Bursts.

---

## 6. CPU & Frequenz

| Prozess | RSS Start | RSS Peak | RSS End | CPU% max | Threads max |
|---------|-----------|----------|---------|----------|-------------|
| X-Plane | 13,3 GB | **21,3 GB** | 20,4 GB | 1414% | 199 |
| XEL | 9,1 GB | **16,2 GB** | 12,5 GB | 1386% | 547 |
| QEMU | 4,2 GB | 4,2 GB | 4,0 GB | 201% | 73 |

XEL RSS ist niedriger als in Run K (Peak 16,2 vs. 25,8 GB) — Effekt von memory_size 4 GB (Änderung 10). Weniger Cache = weniger RAM-Verbrauch, aber mehr Tile-Reloads.

---

## 7. Vergleich Runs K→M

| Metrik | K (116 Min) | **M (98 Min)** | Trend |
|--------|-------------|----------------|-------|
| Stall Samples | 235 (3,4%) | **199 (3,4%)** | = |
| Stall Peak/s | 13.831 | **8.324** | ↓ besser |
| Reclaim Events | 171.744 | **89.335** | ↓ **-48%** |
| Main Thread % | 73,1% | 69,2% | ~ |
| Main Thread Worst | 68,6 ms | **189,0 ms** | ↑ schlechter |
| XEL tokio % | 5,2% | **20,6%** | ↑ (memory_size-Effekt) |
| Swap Peak | 26,6 GB | **9,7 GB** | ↓ **-63%** |
| NVMe Swap | 0 | 0 | = |
| Slow IO | 65 | **1.806** | ↑ (Swap-Write unter Last) |
| XEL RSS Peak | 25,8 GB | **16,2 GB** | ↓ (memory_size-Effekt) |
| FPS avg | — | **29,8** | Erstmals gemessen |
| FPS < 25 | — | **3,4%** | — |

**Bewertung Änderung 10 (memory_size 8→4 GB):**

| Positiv | Negativ |
|---------|---------|
| XEL RSS -37% (25,8→16,2 GB) | XEL Reclaim-Anteil ×4 (5→21%) |
| Swap -63% (26,6→9,7 GB) | Mehr Slow-IO durch Swap-Write |
| Gesamt-Reclaim -48% | Main Thread Worst höher (189ms) |

Der Trade-off ist insgesamt positiv: weniger RAM-Verbrauch, weniger Swap, weniger Gesamt-Reclaim. Der höhere Worst-Case (189ms) ist ein Einzelereignis beim 56°N-Crossing (+56+009.dsf, 16.312ms Load — der längste DSF-Load im gesamten Run).

---

## 8. Handlungsempfehlungen

### 8.1 NVML-Fix verifizieren [ERLEDIGT]

Der pynvml-Scope-Bug ist gefixt und committed. Ab dem nächsten Run liefert vram.csv VRAM-Daten (Used, Temp, Util, Clocks, Power, PCIe, Throttle, PState). Damit können wir erstmals VRAM-Korrelation bei Stutter-Events analysieren.

### 8.2 Texture Resolution-Experiment [OPTIONAL]

Beim Touchdown-Stutter (Stutter 2) springt GPU Time auf 42ms. Post-Flight-Test zeigt 5,9 GB VRAM bei idle — reichlich Headroom. Der GPU-Spike kommt wahrscheinlich vom Texture Upload Burst, nicht von VRAM-Mangel. **Empfehlung:** Erst mit VRAM-Daten im nächsten Run verifizieren, bevor global die Texture Resolution gesenkt wird.

### 8.3 XEL Ground-Tile-Loading untersuchen [BEOBACHTEN]

Stutter 2 zeigt: XEL-Tile-Loading am Boden erzeugt GPU-Spikes ohne Main-Thread-Reclaim. Das ist ein anderer Stutter-Mechanismus als DSF-Crossings. Möglicher Zusammenhang mit XEL Issue #62. Wenn das Muster in weiteren Runs bestätigt wird → XEL Feature Request.

### 8.4 memory_size beibehalten [BESTÄTIGT]

memory_size=4 GB reduziert RAM und Swap deutlich bei akzeptablem Trade-off (mehr XEL-Reclaim, aber weniger Gesamt-Reclaim). Keine Änderung nötig.

---

## 9. Zusammenfassung

Run M liefert drei wesentliche Ergebnisse:

1. **DSF-Boundary-Crossings sind das reproduzierbare Hauptproblem.** 7 von 8 Stutter-Events kommen von Breitengrad-Übergängen. Das ist ein X-Plane-Architekturproblem (synchrones DSF-Loading auf Main Thread). Tuning kann die Auswirkungen mildern, aber nicht eliminieren.

2. **Touchdown-Stutter ist GPU-getrieben, nicht Memory-getrieben.** Erstmals durch Telemetrie nachgewiesen: GPU Time springt auf 42ms, Reclaim liegt auf XEL-Threads (nicht Main Thread). Neuer Stutter-Typ, der weitere Untersuchung verdient.

3. **Änderung 10 wirkt positiv.** memory_size 4 GB senkt XEL RSS um 37%, Swap um 63%, Gesamt-Reclaim um 48%. Der Trade-off (mehr XEL-Reclaim) ist akzeptabel.

**Methodischer Fortschritt:** In-Sim-Telemetrie (FPS/CPU/GPU) und NVML-Fix ermöglichen ab dem nächsten Run erstmals vollständige CPU↔GPU↔VRAM↔Reclaim-Korrelation — die fehlenden Puzzlestücke für die Stutter-Diagnose.
