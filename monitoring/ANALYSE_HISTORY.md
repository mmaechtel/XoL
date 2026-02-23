# Tuning-Historie: X-Plane 12 + XEarthLayer + QEMU/KVM

**System:** Ryzen 9 9800X3D 8C/16T, 96 GB RAM, RTX 4090 24 GB, 3x NVMe (2x SN850X 8TB + 990 PRO 4TB)
**Kernel:** Liquorix 6.18 (PDS), Btrfs RAID0 (xplane_data) + RAID1 (home)
**Zeitraum:** 2026-02-17 bis 2026-02-22

---

## Run A — Baseline (2026-02-17, 5 Min)

Erste Messung, keine Tunings. Unveränderte Liquorix-Defaults.

| Metrik | Wert | Bewertung |
|--------|------|-----------|
| Direct Reclaim | max 75.183 pages/s | Schlecht — synchrones Warten |
| Alloc Stalls | max 1.042/s | Mikroruckler |
| Major Faults | 724/s avg | Aktives Swap-In |
| Swap Swing | 1.1 GB / 5 Min | Hohe Churn |
| Dirty Pages | 502 MB avg, 1.3 GB max | Writeback staut |
| Write-Latenz p95 | 260–312 ms (alle NVMe) | Kyber + WBT drosseln |
| TLB Shootdowns | 16.000/s | Übermäßiges Reclaim |

**Identifizierte Probleme:** min_free_kbytes zu klein (512 MB), swappiness zu hoch (10), Kyber-Scheduler + WBT drosseln NVMe-Writes, Dirty-Limits zu hoch, Btrfs commit=120s staut Metadata.

---

## Änderung 1 — sysctl Tuning

```
vm.min_free_kbytes    512 MB → 1 GB       kswapd bekommt Vorlauf
vm.swappiness         10 → 1              Kernel bevorzugt Page-Cache-Reclaim
vm.page-cluster       3 → 0              Kein Swap-Readahead (Random-Zugriff)
vm.vfs_cache_pressure 100 → 150          VFS-Cache schneller freigeben
vm.dirty_background_ratio 3 → 1          Writeback ab ~940 MB
vm.dirty_ratio        10 → 5             Hard-Limit 4,7 GB
vm.dirty_expire_centisecs 3000 → 1500    Pages nach 15s flushen
vm.dirty_writeback_centisecs 1500 → 500  Flush alle 5s
```

---

## Run B — +sysctl, idle (2026-02-17, 5 Min)

| Metrik | Run A | Run B | Veränderung |
|--------|-------|-------|-------------|
| Direct Reclaim | 75.183/s | **0** | Eliminiert |
| Alloc Stalls | 1.042/s | **0** | Eliminiert |
| Major Faults | 724/s | 192/s | -73% |
| Dirty Pages | 502 MB | 33 MB | -93% |
| Write-Lat avg | 36–47 ms | 4–7 ms | -85% |

## Run C — +sysctl, aktiver Flug (2026-02-17, 5 Min)

| Metrik | Run A | Run C | Veränderung |
|--------|-------|-------|-------------|
| Direct Reclaim | 75.183/s | **0** | Eliminiert |
| Alloc Stalls | 1.042/s | **0** | Eliminiert |
| Major Faults | 724/s | 505/s | -30% |
| Dirty Pages | 502 MB | 194 MB | -61% |
| Write-Lat avg | 36–47 ms | 36–47 ms | Unverändert |

**Erkenntnis:** sysctl löst Reclaim/Stalls, aber Write-Latenz bleibt — IO-Scheduler ist das Problem.

---

## Änderung 2 — NVMe IO-Tuning + Btrfs

```
IO-Scheduler     kyber → none       NVMe Multi-Queue braucht keinen Software-Scheduler
WBT              2000 µs → 0 (aus)  Keine Write-Drosselung auf NVMe
Readahead        512/128/512 → 256  Einheitlich
Btrfs commit     120s → 30s/60s     Kleinere, häufigere Metadata-Commits
```

---

## Run D — +IO-Tuning (2026-02-17, 15 Min)

| Metrik | Run A | Run D | Veränderung |
|--------|-------|-------|-------------|
| Direct Reclaim | 75.183/s | **0** | Eliminiert |
| Write-Lat avg | 36–47 ms | **1,8 ms** | **-95%** |
| Write-Lat max | 260–312 ms | **283 ms** | Tail bleibt |
| Dirty Pages | 502 MB | **30 MB** | -94% |
| TLB Shootdowns (vmstat) | 16.000/s | **0/s** | Eliminiert |
| Swap Swing | 1.1 GB/5 Min | 211 MB/15 Min | -95% |

**Erkenntnis:** IO-Scheduler=none + WBT=0 löst Write-Latenz. Kurztest sieht perfekt aus.

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

## Änderung 5 — Watermark + Swappiness + NVMe PM QOS (geplant für Run H)

```
vm.min_free_kbytes           1 GB → 2 GB        Mehr Puffer vor Direct Reclaim
vm.watermark_boost_factor    0 → 15000           kswapd-Boost reaktivieren (Liquorix-Default war 0!)
vm.watermark_scale_factor    10 → 50             Breitere Watermark-Lücke
vm.swappiness                1 → 10              Graduelles Background-Swap statt Panik-Burst
NVMe pm_qos_latency_tolerance_us  100000 → 0     Power-State-Exit-Latenz eliminieren
bpftrace BPFTRACE_MAP_KEYS_MAX    4096 → 65536   Map-Overflow vermeiden
```

**Erwartung Run H:** Ramp-up-Phase deutlich ruhiger durch proaktiveres kswapd-Verhalten. Weniger/keine Direct-Reclaim-Events auf dem X-Plane Main Thread. Samsung 990 PRO ohne 10 ms Latenz-Spikes.

---

## Gesamtentwicklung — Schlüsselmetriken

| Metrik | A (Baseline) | D (+IO) | E (90 Min) | F/2 (Steady) | G (Steady) |
|--------|-------------|---------|------------|---------------|------------|
| Direct Reclaim max/s | 75.183 | 0 | 2.122.555 | **0** | **0** |
| Alloc Stalls max/s | 1.042 | 0 | 13.383 | **0** | **0** |
| Write-Lat avg (ms) | 36–47 | 1,8 | 16,1 | — | — |
| Write-Lat max (ms) | 260–312 | 283 | 699 | **44** | — |
| Dirty Pages avg (MB) | 502 | 30 | 39 | **2,4** | ~2 |
| Swap auf NVMe | ja | ja | 11,6 GB | **0** | **0** |
| DSF-Load max (ms) | — | — | 63.385 | **22.116** | — |
| PSI | 0 | 0 | 0 | — | **0** |
| GPU Throttle | — | — | — | — | **0** |

**Fazit:** Der Steady State ist gelöst — null Stalls, null Reclaim, null GPU-Throttling. Die Ramp-up-Phase (Szenerieladen) bleibt das letzte Problem. Die Run-G-Analyse hat die Ursache präzise identifiziert: deaktivierter kswapd-Boost + zu enge Watermarks + zu restriktive Swap-Policy. Die für Run H geplanten Änderungen adressieren genau diese Punkte.
