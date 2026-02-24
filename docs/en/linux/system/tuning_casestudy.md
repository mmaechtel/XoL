---
description: "Tuning case study for X-Plane on Linux: five steps from micro-stutters to stable frame times — memory pressure, IO latency, swap destination, page-cluster, and watermark tuning with real measurements."
---
# Case Study: Eliminating Micro-Stutters

The [Kernel Tuning](systemtuning.md) page provides general tuning profiles for stock and Liquorix kernels. This page goes one step further: it shows how to **diagnose** memory-related stutters, **why** specific parameter changes help, and **what measurable effect** they have — based on systematic measurements on a test system running X-Plane with ortho streaming and a KVM virtual machine in parallel.

!!! note "Relationship to the tuning profiles"
    The sysctl values in this case study are more aggressive than [Profile B](systemtuning.md#profile-b-liquorix-kernel) — they were tuned for a heavy workload with simultaneous ortho streaming, addon scenery, and a KVM guest. Profile B is a safe starting point; the values here show how far the parameters can be pushed when measurements confirm the need.

## The Problem: Frame Drops During Flight

### What the Pilot Sees

A flight begins smoothly at 40+ FPS. After 15–20 minutes — typically when crossing scenery tile boundaries or when [ortho streaming](../../scenery/ortho_streaming/how_streaming_works.md) loads a new region — the image freezes for 1–2 seconds. FPS drops to single digits, recovers briefly, then stutters again. The pattern repeats every 10–15 minutes, always during scenery transitions. Between episodes, performance is normal.

These micro-stutters are not caused by insufficient GPU or CPU power. They originate in the **memory subsystem** — the kernel cannot deliver data fast enough because memory management is misconfigured.

### What the System Is Doing

Each visible symptom maps to a specific kernel mechanism:

| Symptom | Kernel Cause | Mechanism |
|---|---|---|
| 1–2 second freeze | [Direct Reclaim](swap.md#page-reclaim) | The allocating process is blocked while the kernel frees memory synchronously |
| FPS drops to single digits | Alloc Stalls | Threads wait for memory allocation — render thread cannot submit frames |
| Stutter during scenery transitions | [kswapd](swap.md#page-reclaim) overwhelmed | Background reclaim cannot keep up with allocation rate |
| Periodic pattern (every 10–15 min) | Scenery tile loading | X-Plane + ortho streaming simultaneously demand large memory allocations |

On the test system baseline, these mechanisms produced measurable impact: Direct Reclaim reached up to 75,000 pages/s, allocation stalls peaked at over 1,000/s, and dirty pages accumulated to 500 MB on average with spikes above 1 GB.

---

## Monitoring: What to Measure and Why

### Key Kernel Metrics

Before tuning, you need to identify **which** subsystem is causing the problem. The kernel exposes the relevant counters through `/proc/vmstat` and `/proc/meminfo`:

| Metric | Source | What It Reveals |
|---|---|---|
| `allocstall_normal` | /proc/vmstat | Threads blocked waiting for memory — the direct stutter cause |
| `pgsteal_direct` | /proc/vmstat | Pages reclaimed synchronously — each event blocks a process |
| `pgscan_kswapd` | /proc/vmstat | Background reclaim activity — high values indicate memory pressure |
| `nr_dirty` | /proc/vmstat | Pending dirty pages — accumulation indicates writeback bottleneck |
| `nr_free_pages` | /proc/vmstat | Current free memory — low values trigger reclaim |
| `MemAvailable` | /proc/meminfo | Memory available without swapping — the practical headroom |
| `SwapUsed` | /proc/meminfo | Current swap consumption — rising values during flight indicate pressure |

GPU metrics (utilization, VRAM, power draw) via NVML complement the kernel data — GPU utilization dropping while the process still runs indicates the CPU/memory subsystem is starving the GPU.

??? abstract "Advanced: Per-Process Tracing"

    Aggregate counters show **that** reclaim is happening but not **which process** triggered it. For targeted diagnosis, kernel tracepoints provide per-event attribution:

    - `vmscan:mm_vmscan_direct_reclaim_begin/end` — duration of each Direct Reclaim event, tagged with the triggering process. Shows whether X-Plane's render thread is affected or a background process.
    - `block:block_rq_issue/complete` (filtered for latency >5 ms) — identifies NVMe IO outliers that correlate with frame drops.

    These tracepoints can be accessed via `bpftrace` or `perf` (see [Monitoring](systemtools.md) for tool details). The key insight: when the render thread appears in Direct Reclaim events, the stutters are memory-caused.

### Three-Phase Pattern

A typical flight session shows three distinct phases:

| Phase | Duration | Behavior |
|---|---|---|
| **Warm-up** | First 5–10 min | Initial scenery loading, high allocation rate, some reclaim activity expected |
| **Ramp-up** | 10–30 min | Scenery transitions trigger periodic memory pressure spikes — this is where stutters appear |
| **Steady State** | After 30+ min | Cache is warm, allocations stabilize, reclaim activity drops to near zero |

Tuning should target the **Ramp-up phase** — the Steady State is typically fine even with suboptimal settings. Measurements should cover at least 60 minutes to capture the transition between phases.

---

## Tuning Steps: From Chaos to Stability

The following four steps were applied incrementally on the test system. Each step addresses a specific bottleneck, and measurements confirm the effect before proceeding to the next.

### Step 1: Memory Pressure — Give kswapd Headroom

**Problem:** The default `vm.min_free_kbytes` value is too small for workloads that allocate memory in large bursts (scenery loading, ortho tile decompression). kswapd wakes too late, and Direct Reclaim takes over — blocking application threads.

**Solution:** Increase the free memory reserve so kswapd starts reclaiming earlier, before Direct Reclaim is triggered. Simultaneously tighten dirty page limits to prevent writeback storms.

```ini title="/etc/sysctl.d/99-xplane-tuning.conf"
vm.min_free_kbytes = 1048576
vm.dirty_background_ratio = 1
vm.dirty_ratio = 5
vm.dirty_expire_centisecs = 1500
vm.dirty_writeback_centisecs = 500
```

```bash
sudo sysctl --system
```

| Parameter | Default | Tuned | Effect |
|---|---|---|---|
| `vm.min_free_kbytes` | ~67 MB | 1 GB | kswapd wakes with 1 GB headroom instead of 67 MB |
| `vm.dirty_background_ratio` | 10% | 1% | Writeback starts at ~940 MB instead of ~9.4 GB |
| `vm.dirty_ratio` | 20% | 5% | Hard limit at ~4.7 GB instead of ~18.8 GB |
| `vm.dirty_expire_centisecs` | 3000 | 1500 | Dirty pages flushed after 15s instead of 30s |
| `vm.dirty_writeback_centisecs` | 500 | 500 | Flush thread interval (unchanged) |

For details on how [watermarks](swap.md#watermarks) and [kswapd](swap.md#page-reclaim) interact, see the Swap page.

**Measured effect:** Direct Reclaim dropped from 75,000 pages/s to zero during normal flight — the most impactful single change. Dirty pages dropped from 502 MB average to under 200 MB during active flight; the remaining accumulation was resolved by IO tuning in Step 2.

### Step 2: IO Latency — Remove Software Overhead on NVMe

**Problem:** The default IO scheduler (`kyber` or `mq-deadline`) and Write-Back Throttling (WBT) add software-side queuing delays. On NVMe drives with hardware multi-queue support, this overhead is unnecessary and increases write latency — particularly during Btrfs metadata commits.

**Solution:** Set the IO scheduler to `none` and disable WBT. NVMe drives handle queue management in hardware.

| Parameter | Default | Tuned | Effect |
|---|---|---|---|
| IO scheduler | `kyber` or `mq-deadline` | `none` | Bypass software scheduler — direct hardware queue access |
| WBT (`wbt_lat_usec`) | 2000 µs | 0 (disabled) | No write throttling — NVMe handles congestion internally |
| Readahead | Varies | 256 KB | Balanced for mixed sequential/random IO |

These settings can be applied persistently via udev rules:

```ini title="/etc/udev/rules.d/60-nvme-tuning.rules"
ACTION=="add|change", KERNEL=="nvme[0-9]*n1", ATTR{queue/scheduler}="none"
ACTION=="add|change", KERNEL=="nvme[0-9]*n1", ATTR{queue/wbt_lat_usec}="0"
ACTION=="add|change", KERNEL=="nvme[0-9]*n1", ATTR{queue/read_ahead_kb}="256"
```

!!! note "Only for NVMe"
    Scheduler `none` is safe for [NVMe](../../glossary.md#nvme-non-volatile-memory-express) drives because they manage queuing in hardware. SATA SSDs and HDDs still benefit from a software scheduler (`mq-deadline` or `bfq`).

**Measured effect:** Average write latency dropped from 36–47 ms to 1.8 ms. TLB shootdowns (a side effect of excessive page remapping) dropped to zero in vmstat.

### Step 3: Swap Destination — zram Instead of NVMe

**Problem:** When swap resides on the same NVMe as X-Plane data and ortho caches, three IO streams compete: swap pages, scenery files, and ortho tiles. Under memory pressure, swap IO saturates the drive, blocking scenery loading — visible as multi-second DSF load times.

**Solution:** Use [zram](swap.md#zram) as the primary swap device. zram compresses pages in RAM — no disk IO occurs. The NVMe swap partition serves only as emergency fallback.

| Configuration | Latency | IO Contention |
|---|---|---|
| Swap on same NVMe | ~15 µs + queue wait | Competes with scenery and ortho IO |
| Swap on dedicated NVMe | ~15 µs | Eliminated |
| **zram (lz4)** | **~1.7 µs** | **None — entirely in RAM** |

For zram setup and the comparison with zswap, see [zram](swap.md#zram).

!!! warning "zram requires sufficient total RAM"
    zram compresses pages in RAM — the compressed data still occupies physical memory. On the test system, 17 GB of swapped-out pages consumed 14.6 GB of RAM after compression (ratio 1.17:1). The primary benefit is not saving RAM but **eliminating IO contention** on the NVMe. This approach only works when enough total RAM remains after the main applications are loaded. On a system where X-Plane, ortho streaming, and other processes already exhaust physical memory, zram cannot help — the compressed pages would further reduce the available RAM pool.

**Measured effect:** NVMe swap was never touched — zram absorbed 100% of swap traffic. Write volume on the previously contended NVMe dropped by 86%. DSF worst-case load time improved from 63 seconds to 22 seconds.

### Step 4: Swap Readahead

**Problem:** The default `vm.page-cluster=3` causes the kernel to read 8 pages (32 KiB) per swap access as readahead. With zram, each page must be individually decompressed — readahead provides no benefit and increases latency.

**Solution:** Set page-cluster to 0 (single-page reads).

```ini title="/etc/sysctl.d/99-zram.conf"
vm.page-cluster = 0
```

```bash
sudo sysctl --system
```

**Measured effect:** Part of the overall sysctl tuning applied from Step 1 onward. Eliminates unnecessary decompression overhead on every swap-in.

### Step 5: Watermark Optimization — Proactive kswapd for Burst Allocations

**Problem:** After Steps 1–4, the steady state was solved — zero stalls, zero Direct Reclaim. But the **ramp-up phase** (minute 10–60, while scenery caches are still warming) still showed periodic memory pressure spikes. Per-process tracing revealed that **67% of all Direct Reclaim events hit the X-Plane render thread** directly — causing the remaining micro-stutters.

Root cause analysis identified three contributing factors:

| Factor | Setting | Effect |
|---|---|---|
| `watermark_boost_factor=0` | Liquorix default | kswapd does not get a temporary boost after reclaim — it reclaims too few pages per wake-up and falls behind |
| `min_free_kbytes=1 GB` | Step 1 | Only 400 MB headroom above the threshold — burst allocations cross min watermark before kswapd can react |
| `swappiness=1` | Step 1 | Anonymous pages are only swapped under extreme pressure — when swap finally happens, it happens as a panic burst |

!!! warning "Common misconception: watermark_boost_factor=0 for zram"
    Many zram guides recommend `watermark_boost_factor=0` with the reasoning that the boost mechanism is "designed for spinning disks." This is incomplete. The boost temporarily raises watermarks after a reclaim event, making kswapd reclaim more aggressively in the next cycle. For workloads with bursty allocation patterns (scenery loading, ortho tile decompression), this proactive behavior is essential — without it, kswapd cannot keep pace and Direct Reclaim takes over.

**Solution:** Widen the watermark gap, re-enable kswapd boost, and allow gradual background swapping:

```ini title="/etc/sysctl.d/99-xplane-tuning.conf"
vm.min_free_kbytes = 2097152
vm.watermark_boost_factor = 15000
vm.watermark_scale_factor = 50
vm.swappiness = 10
```

```bash
sudo sysctl --system
```

| Parameter | Before | After | Effect |
|---|---|---|---|
| `vm.min_free_kbytes` | 1 GB (Step 1) | 2 GB | kswapd wakes with 2 GB headroom — burst allocations stay above min watermark |
| `vm.watermark_boost_factor` | 0 | 15000 | kswapd temporarily boosts watermarks after reclaim — reclaims more pages per cycle |
| `vm.watermark_scale_factor` | 10 | 50 | Wider gap between low and min watermark — kswapd has more runway before Direct Reclaim |
| `vm.swappiness` | 1 | 10 | Gradual background swap instead of panic bursts — anonymous pages move to zram before pressure becomes critical |

**Measured effect:** The ramp-up phase (minute 10–60) showed significantly reduced memory pressure. Direct Reclaim events on the render thread dropped, and the transition to steady state became smoother. See the [Swap page](swap.md#recommended-configuration) for the general watermark and swappiness recommendations.

---

## Results Summary

The combined effect of all five steps, measured on the test system (steady-state values from a multi-hour session):

| Metric | Baseline | After Tuning | Change |
|---|---|---|---|
| Direct Reclaim (max) | 75,000 pages/s | 0/s (steady state) | Eliminated |
| Alloc Stalls (max) | 1,000/s | 0/s (steady state) | Eliminated |
| Dirty Pages (avg) | 502 MB | 2.4 MB | -99% |
| NVMe Write Latency (avg) | 36 ms | 6 ms | -83% |
| NVMe Write Latency (max, steady state) | 260 ms | 44 ms | -83% |
| Swap on NVMe | Active (1.1 GB churn/5 min) | Inactive (zram absorbs 100%) | Eliminated |
| DSF Load Time (worst) | 63 s | 22 s | -65% |
| NVMe Write Volume | 25 GB/session | 3.6 GB/session | -86% |

!!! tip "Generalizable takeaways"
    The specific values depend on the system and workload, but the **principles** apply broadly:

    1. **Give kswapd headroom** — `min_free_kbytes` should match the burst allocation rate, not the system default
    2. **Separate swap from data IO** — zram eliminates the contention entirely, without needing a dedicated SSD
    3. **Remove software overhead on NVMe** — multi-queue hardware does not benefit from a software scheduler
    4. **Tune watermarks for burst workloads** — `watermark_boost_factor` and `watermark_scale_factor` control how proactively kswapd reclaims during allocation spikes
    5. **Measure before and after** — aggregate counters from `/proc/vmstat` are sufficient to confirm whether a change had the intended effect

---

## Further Reading

| Topic | Page | Focus |
|---|---|---|
| Kernel Tuning | [Kernel Tuning](systemtuning.md) | Two tuning profiles — standard kernel vs. Liquorix |
| Swap & Memory | [Swap & Memory Management](swap.md) | Page reclaim, watermarks, zram setup, swappiness |
| Monitoring | [Monitoring](systemtools.md) | Tools to measure every metric referenced here |
| Latency | [Latency and Predictability](../../fundamentals/performance/latency.md) | Why latency matters more than throughput |
| Filesystem | [Filesystem](../optimizations/filesystem.md) | IO scheduler, mount options, SSD tuning |

---

## Sources

- [/proc/sys/vm/ — Linux Kernel Documentation](https://docs.kernel.org/admin-guide/sysctl/vm.html) — vm.min_free_kbytes, dirty ratios, swappiness, watermark parameters
- [Memory Management Concepts — Linux Kernel Documentation](https://docs.kernel.org/admin-guide/mm/concepts.html) — Page reclaim, watermarks, kswapd behavior
- [zram block device — Linux Kernel Documentation](https://docs.kernel.org/admin-guide/blockdev/zram.html) — Compressed swap in RAM
- [Block layer: Writeback Throttling — LWN](https://lwn.net/Articles/682582/) — WBT mechanism and when to disable it
- [Zram — Arch Wiki](https://wiki.archlinux.org/title/Zram) — Practical setup and tuning recommendations
