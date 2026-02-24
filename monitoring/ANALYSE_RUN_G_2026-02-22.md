# Run G — Ergebnisse: 81-Minuten Langflug mit erweiterter Instrumentierung

**Datum:** 2026-02-22
**System:** Ryzen 9 9800X3D 8C/16T, 96 GB RAM, RTX 4090 24 GB, 3x NVMe
**Kernel:** Liquorix 6.18 (PDS)
**Workload:** X-Plane 12 + XEarthLayer + QEMU/KVM
**Änderungen seit Run F:** Erweiterte sysmon.py-Instrumentierung (PCIe, Throttle, Swap-IO, Workingset-Refaults, THP, Crash-Diagnostik), bpftrace-Sidecar

---

## 0. Testbedingungen

| Parameter | Wert |
|-----------|------|
| Geplante Dauer | 120 Min |
| Tatsächliche Dauer | 81 Min (21:03–22:24), manuell gestoppt |
| Samples | 23.100 (200ms), 4.625 (1s-Probes) |
| zram | 32 GB lz4, pri=100 |
| NVMe-Swap | nvme2n1p5 120 GB, pri=-2 (Fallback) |
| Gesamt-Swap | ~151 GB (zram + NVMe) |
| bpftrace | 3 Tracer (Direct Reclaim, Slow IO >5ms, DMA Fence >5ms) |

---

## 1. Erwartungen vs. Ergebnisse

| Metrik | Run F (Teil 2) | Erwartung G | **Ergebnis G** | Bewertung |
|--------|----------------|-------------|----------------|-----------|
| Alloc Stalls | 0/s | 0/s | **42 Burst-Events, max 11.425/s** | Verschlechtert |
| Direct Reclaim | 0/s | 0/s | **pgscan_direct avg 2.049/s, max 1.288.656/s** | Verschlechtert |
| Swap Peak | 25.813 MB (79% zram) | <32 GB | **18.156 MB (11,7% von 151 GB)** | OK |
| Dirty Pages avg | 2,4 MB | ~2-3 MB | **3,6 MB** | OK |
| VRAM Peak | — | <22 GB | **23.055 MiB (93,9%)** | Knapp |
| GPU Throttle | — | 0 | **0** | Erreicht |
| GPU Fence Stalls | — | 0 | **0** | Erreicht |

---

## 2. Kernbefunde

### 2.1 Drei-Phasen-Verhalten (bestätigt Run F Muster)

| Phase | Zeitfenster | Charakteristik |
|-------|-------------|----------------|
| **Warm-up** | 0–11 Min | used ~41 GB, swap ~1,8 GB, kein Reclaim |
| **Ramp-up** | 12–60 Min | used 41→55 GB, swap 1,8→15,5 GB, 42 Alloc-Stall-Bursts |
| **Steady State** | 60–81 Min | used ~55,7 GB, swap ~15,5 GB stabil, kein Reclaim |

Die Ramp-up-Phase ist deutlich länger als bei Run F (50 Min vs. ~20 Min). Erst nach Minute 60 stabilisiert sich das System vollständig.

### 2.2 Memory Pressure — Signifikante Aktivität in der Ramp-up-Phase

| Metrik | Run F (Teil 2, Steady) | Run G (Gesamt) | Run G (Min 60–81, Steady) |
|--------|------------------------|-----------------|---------------------------|
| pgscan_kswapd avg/s | ~0 | 15.397 | ~1.000–2.500 |
| pgscan_direct avg/s | 0 | 2.049 | **0** |
| Alloc Stalls | 0 | 42 Events | **0** |
| pgmajfault avg/s | 76 | 662 | ~56 |
| pswpin avg/s | — | 605 | ~52 |
| pswpout avg/s | — | 1.306 | ~11 |

**Neue vmstat-Metriken (erstmals in Run G):**

| Metrik | Avg/s | Max/s | Interpretation |
|--------|-------|-------|----------------|
| pswpin | 605 | 94.224 | 85,8% aller Samples aktiv — nahezu kontinuierliches Swap-In |
| pswpout | 1.306 | 538.360 | Burst-weise (5,1% der Samples), massive Spitzen |
| wset_refault_anon | 625 | 93.929 | 86,4% aktiv — **Thrashing-Signatur** |
| wset_refault_file | 2.398 | 122.830 | 62,4% aktiv — Page-Cache wird reclaimed und re-faultet |
| thp_fault_fallback | 0 | 0 | Keine THP-Probleme |

**Bewertung:** Die Workingset-Refault-Rate von 86% (anon) zeigt, dass Seiten nach dem Swap-Out schnell wieder benötigt werden. Das ist zram-internes Thrashing — schnell (Kompression/Dekompression), aber CPU-intensiv. Die Steady-State-Phase nach Minute 60 ist dagegen exzellent.

### 2.3 Direct Reclaim Efficiency

| Pfad | Scanned | Stolen | Efficiency |
|------|---------|--------|------------|
| kswapd (Background) | 71,2M | 66,5M | **93,4%** — gesund |
| Direct (Synchron) | 9,5M | 4,3M | **45,2%** — schlecht |

kswapd arbeitet effizient, kommt aber in Lastspitzen nicht nach. Die Folge: Prozesse geraten in synchrones Direct Reclaim mit nur 45% Effizienz (viel Scanning, wenig Ergebnis).

### 2.4 Alloc-Stall-Bursts (6 Cluster)

| Cluster | Zeitfenster | Max Stalls/s | Korrelation |
|---------|-------------|-------------|-------------|
| 1 | Min 11,9–14,4 | **11.425** | Szenerieladen Start |
| 2 | Min 20,4 | 1.284 | Tile-Loading |
| 3 | Min 23,4–24,1 | 3.785 | Tile-Loading |
| 4 | Min 30,0–32,9 | 5.252 | Szenerieladen + IO-Storm |
| 5 | Min 42,0–42,9 | **8.242** | Swap-Out-Storm (538k pages/s) |
| 6 | Min 50,9–51,9 | 4.414 | Letzte Druckwelle |

Nach Minute 60: **Null Alloc Stalls, null Direct Reclaim.**

---

## 3. bpftrace — Erstmals Direct Reclaim pro Prozess

### 3.1 Direct Reclaim Events (trace_reclaim.log, 4,7 MB)

| Metrik | Wert |
|--------|------|
| Gesamt-Events | **71.160** |
| Reclaimed Pages | ~4,5M (≈17,6 GB) |
| kswapd Wakes | 739 |
| kswapd Sleeps | 231 |

**Top-Verursacher:**

| Prozess | Events | Anteil | Max Dauer |
|---------|--------|--------|-----------|
| **X-Plane Main Thread** | 47.583 | **66,9%** | 20,6 ms |
| **tokio-runtime-w** (XEL) | 13.879 | 19,5% | ~5 ms |
| bpftrace (Tracer selbst) | 2.782 | 3,9% | — |
| cuda-EvtHandlr | 2.535 | 3,6% | — |
| Sonstige | 6.381 | 9,0% | — |

**X-Plane Main Thread Reclaim-Latenz:**

| Metrik | Wert |
|--------|------|
| avg | 485 µs |
| p50 | 321 µs |
| p95 | 1.359 µs |
| p99 | 2.360 µs |
| p99.9 | 5.525 µs |
| max | **20.613 µs (20,6 ms)** |
| Events >1 ms | 6.131 (12,9%) |
| Events >5 ms | 75 |
| Events >10 ms | 28 |

**Die 20 ms Worst-Case-Reclaim-Latenz auf dem Main Thread ist ein Frame-Drop bei 50 FPS.** Diese Events clustern bei Min 18, 27, 36, 46.

### 3.2 Slow IO (trace_io_slow.log, 697 MB)

| Metrik | Wert |
|--------|------|
| Erfasste Events | **12.383** |
| bpftrace Map-Overflows | ~3.042.000 (Daten verloren) |
| avg Latenz | 12,4 ms |
| max Latenz | 35 ms |

**ACHTUNG:** Die 697 MB Dateigröße kommt von ~3M bpftrace Map-Overflow-Warnungen. Die Default-Map-Kapazität (4.096 Einträge) war für die IO-Parallelität zu klein. Der tatsächliche Slow-IO-Count ist höher als 12.383.

**Per-Device:**

| Device | Events | Anteil | Avg Lat | Max Lat | Charakteristik |
|--------|--------|--------|---------|---------|----------------|
| **nvme1n1** | 11.187 | **90,3%** | 10,6 ms | 19 ms | 92% bei exakt 10–11 ms |
| nvme0n1 | 953 | 7,7% | 29,6 ms | 35 ms | Höchste Einzellatenzen |
| nvme2n1 | 243 | 2,0% | 27,0 ms | 33 ms | System-Disk, wenig betroffen |

**nvme1n1 (Samsung 990 PRO):** 92% der Events clustern bei exakt 10–11 ms. Das ist die typische **NVMe Power-State-Exit-Latenz** (PS3/PS4 → PS0). Der Drive geht zwischen IO-Bursts in Deep Sleep und braucht ~10 ms zum Aufwachen. Handlungsempfehlung: `default_ps_max_latency_us` oder PM QOS prüfen.

**Zeitliche Verteilung:** 71% der Slow-IO-Events fallen in die ersten 20 Minuten (Szenerieladen). Nach Minute 30 nur noch residuale Aktivität.

### 3.3 DMA Fence Waits (trace_fence.log, 22 Bytes)

**Null Events.** Die GPU hat den CPU-Thread nie >5 ms blockiert. Die Vulkan-Rendering-Pipeline ist sauber.

---

## 4. GPU / VRAM — Neue Metriken

### 4.1 Kerndaten

| Metrik | Avg | Min | Max |
|--------|-----|-----|-----|
| VRAM Used | 19.123 MiB (77,9%) | 13.957 MiB (56,8%) | **23.055 MiB (93,9%)** |
| GPU Util | 63,9% | 2% | 99% |
| GPU Clock | 2.722 MHz | 2.715 MHz | 2.730 MHz |
| Temp | 57°C | 50°C | 64°C |
| Power | 228,9 W | 88,2 W | 309,8 W |

### 4.2 Neue Metriken (erstmals in Run G)

| Metrik | Avg | Max | Bewertung |
|--------|-----|-----|-----------|
| PCIe TX | 50,9 KB/s | 948 KB/s | Vernachlässigbar |
| PCIe RX | 461 KB/s | 4.730 KB/s (4,6 MB/s) | Kein Bottleneck (28 GB/s theoretisch) |
| Throttle Reasons | 0 | 0 | **Null Throttling** |
| Perf State | P2 | P2 | 100% P2 (normal für 3D-Last) |
| Mem Clock | 10.251 MHz | 10.251 MHz | GDDR6X volle Geschwindigkeit |
| Mem Bus Util | 37,4% | 71% | Headroom vorhanden |

**VRAM-Peak bei Minute 60:** 23.055 MiB (93,9% von 24 GiB). Nur ~1,5 GiB Headroom — eng, aber kein OOM. Der VRAM-Swing über die Session beträgt ~9 GiB (XEL-Ortho-Tile-Cycling).

### 4.3 PSI (Pressure Stall Information)

**Alle Werte 0,00 über alle 4.570 Samples.** CPU, Memory und IO PSI zeigen keinerlei systemweite Stalls. Das steht scheinbar im Widerspruch zu den Alloc Stalls — erklärt sich aber dadurch, dass PSI erst anschlägt wenn *alle* Tasks in einer cgroup stallen, nicht einzelne.

---

## 5. Disk IO

### 5.1 Per-Device Throughput

| Device | Read avg MB/s | Read max MB/s | Write avg MB/s | Write max MB/s | Cumulative Read |
|--------|--------------|--------------|---------------|---------------|-----------------|
| nvme0n1 (990 PRO) | 16,5 | 3.385 | 0,25 | 284 | 381 GB |
| nvme1n1 (SN850X) | 15,8 | 3.380 | 0,004 | 54 | 366 GB |
| nvme2n1 (SN850X) | 16,8 | 3.387 | 0,32 | 284 | 388 GB |
| sda | 0 | 0 | 0 | 0 | 0 |

**Gleichmäßige Read-Verteilung** über alle 3 NVMe (365–388 GB). Peak-Aggregate: **~10,1 GB/s** concurrent reads — Btrfs RAID0 liefert.

### 5.2 Latenz-Profil

| Device | Read p95 ms | Read max ms | Write p95 ms | Write max ms |
|--------|------------|------------|-------------|-------------|
| nvme0n1 (990 PRO) | **0,85** | 33,6 | **32,7** | 34,5 |
| **nvme1n1 (SN850X)** | **10,7** | 15,2 | 11,0 | 12,0 |
| nvme2n1 (SN850X) | **0,79** | 34,6 | 6,8 | 36,0 |

**nvme1n1 ist der Latenz-Ausreißer bei Reads** (p95 = 10,7 ms vs. <1 ms bei den anderen). Bei den bpftrace-Daten war das der Drive mit 90% der Slow-IO-Events bei 10–11 ms. Ursache: NVMe Power-State-Transitionen.

**nvme0n1 ist der Latenz-Ausreißer bei Writes** (p95 = 32,7 ms). Die hohen Write-Latenzen korrelieren mit Btrfs-Journal/Metadata-Flushes während Heavy-Read-Phasen.

### 5.3 IO Spikes (>100 MB/s Read)

| Device | Spike-Samples | % der Samples |
|--------|--------------|--------------|
| nvme0n1 | 455 | 2,0% |
| nvme1n1 | 427 | 1,8% |
| nvme2n1 | 461 | 2,0% |

427 Timestamps hatten alle 3 NVMe gleichzeitig >100 MB/s — RAID0-Streaming funktioniert.

---

## 6. CPU & Frequenz

### 6.1 Aggregate

| Metrik | Avg | Max | P95 |
|--------|-----|-----|-----|
| User | 27,3% | 95,3% | 71,8% |
| Sys | 2,1% | 77,6% | 5,6% |
| IOWait | 0,28% | 19,6% | 1,4% |
| IRQ+SoftIRQ | 0,56% | 11,7% | 0,9% |
| Guest | 0,87% | 10,9% | 1,5% |
| **Gesamt** | **~30%** | — | ~80% |

### 6.2 Core-Isolation (bestätigt)

| Gruppe | CPUs | Avg User+Sys | Rolle |
|--------|------|-------------|-------|
| X-Plane Hot | 0–5 | 55–58% | Hauptlast, 3D V-Cache-Kerne |
| Sekundär | 6–7 | 23–26% | X-Plane Worker |
| SMT Siblings | 8–13 | ~9% | Weitgehend idle |
| KVM | 14–15 | ~13% | QEMU/KVM, Guest 6,7–6,9% |

Kein Guest-Activity auf den X-Plane-Kernen. Saubere Trennung.

### 6.3 Frequenz

| Gruppe | Avg MHz | Min | Max |
|--------|---------|-----|-----|
| CPUs 0–5 (X-Plane) | **4.652** | 2.584 | 5.277 |
| CPUs 6–7 | 3.949 | 2.452 | 5.259 |
| CPUs 8–13 (SMT) | 4.139 | 2.579 | 5.455 |
| CPUs 14–15 (KVM) | 4.017 | 2.591 | 5.266 |

**50% der Samples >5.100 MHz.** Bimodal: Idle-Kerne bei ~2.600 MHz, Last-Kerne bei ~5.200 MHz. Kein Thermal Throttling.

---

## 7. Per-Process

| Prozess | Avg CPU% | Max CPU% | Avg RSS GB | Max RSS GB | Max Threads |
|---------|---------|---------|-----------|-----------|-------------|
| **X-Plane** | 396,5 | 1.389,9 | 20,5 | **23,7** | 109 |
| **XEarthLayer** | 27,2 | 1.140,1 | 14,4 | **19,6** | 432 |
| **QEMU** | 15,9 | 199,7 | 4,9 | 5,1 | 57 |
| gamescope | 1,0 | 3,8 | 0,08 | 0,17 | 14 |

**Aggregate RSS Peak: 47,6 GB** (~49,6% von 96 GB). Mit Kernel-Caches, Page Tables und ungetrackten Prozessen effektiv 60–70 GB.

**XEarthLayer Lifecycle:** Peak 20 GB bei Min 30–35 (Tile-Loading), dann gradueller Rückgang auf 14 GB. Kein Memory-Leak-Indiz.

---

## 8. Vergleich Run F → Run G

| Metrik | Run F (Teil 2, Steady) | Run G (Steady, Min 60–81) | Run G (Gesamt) |
|--------|------------------------|---------------------------|----------------|
| Dirty Pages avg | 2,4 MB | ~2 MB | 3,6 MB |
| Swap Used (Peak) | 25,8 GB | ~15,5 GB | 18,2 GB |
| Alloc Stalls | 0 | **0** | 42 Events |
| Direct Reclaim | 0 | **0** | avg 2.049/s |
| pgmajfault avg/s | 76 | ~56 | 662 |
| PSI (alle) | — | 0,00 | 0,00 |
| GPU Throttle | — | 0 | 0 |
| GPU Fence Stalls | — | 0 | 0 |

**Kernaussage:** Der Steady State (ab Minute 60) ist mit Run F vergleichbar — kein Reclaim, kein Druck. Die Ramp-up-Phase ist allerdings länger und intensiver.

---

## 9. Handlungsempfehlungen

### 9.1 NVMe Power-State für nvme1n1

nvme1n1 verursacht 90% der Slow-IO-Events bei exakt 10–11 ms (Power-State-Exit-Latenz). Prüfen:

```bash
# Aktuelle PM QOS Einstellung
cat /sys/class/nvme/nvme1/device/power/pm_qos_latency_tolerance_us
# NVMe Power States
nvme id-ctrl /dev/nvme1n1 | grep -i "ps "
```

Ggf. `pm_qos_latency_tolerance_us=0` setzen um Deep Sleep zu unterbinden.

### 9.2 bpftrace Map-Größe

Die Default-Map-Kapazität (4.096) war für die IO-Parallelität zu klein. Für Run H:

```bash
bpftrace -e '...' -m 65536  # oder BPFTRACE_MAP_KEYS_MAX=65536
```

Das vermeidet die 697 MB Warn-Datei und erfasst alle Events.

### 9.3 Ramp-up Memory Pressure

Die 42 Alloc-Stall-Bursts und 71.160 Direct-Reclaim-Events in der Ramp-up-Phase sind das Hauptproblem. Mögliche Stellschrauben:

1. **min_free_kbytes erhöhen** (aktuell 1 GB → 2 GB): Gibt kswapd mehr Vorlauf
2. **zram auf 48 GB erhöhen**: Mehr Headroom für die Ramp-up-Phase
3. **XEL `max_tiles_per_cycle` weiter reduzieren** (100 → 50): Bremst Tile-Loading, reduziert Memory-Burst

### 9.4 VRAM Headroom

93,9% Peak ist eng. Bei dichterer Szenerie oder höheren Textureinstellungen droht VRAM-OOM. Keine unmittelbare Aktion nötig, aber beobachten.

---

## 10. Zusammenfassung

Run G bestätigt die Stabilität des Tuning-Stacks nach der Ramp-up-Phase. Der Steady State (ab Minute 60) zeigt:
- Null Alloc Stalls, null Direct Reclaim
- Null GPU-Throttling, null DMA Fence Stalls
- Stabile 55,7 GB used / 36 GB available
- GPU bei 64% avg, 57°C, P2 constant

Die **Ramp-up-Phase (12–60 Min)** bleibt die Schwachstelle: 47.583 Direct-Reclaim-Events auf dem X-Plane Main Thread (Worst Case 20,6 ms = Frame Drop) und 42 Alloc-Stall-Bursts. Die neuen Metriken (Workingset-Refaults, Swap-IO-Raten) machen dieses zram-interne Thrashing erstmals sichtbar.

**Neue Erkenntnisse durch erweiterte Instrumentierung:**
- bpftrace Direct Reclaim: X-Plane Main Thread ist Haupt-Verursacher (67%)
- bpftrace Slow IO: nvme1n1 Power-State-Transitionen als dominante IO-Latenz-Quelle
- NVML Extended: Null PCIe-Bottleneck, null Throttling — GPU ist kein Faktor
- Workingset-Refaults: 86% Anon-Refault-Rate zeigt aktives zram-Thrashing
