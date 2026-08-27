---
description: "Tuning case study for X-Plane on Linux — from micro-stutters to stable frame times via watermark tuning, IO latency, and NVMe power management."
---
# Case Study: Eliminating Micro-Stutters

The [Kernel Tuning](systemtuning.md) page provides general tuning profiles for stock and Liquorix kernels. This page goes one step further: it shows how to **diagnose** memory-related stutters, **why** specific parameter changes help, and **what measurable effect** they have — based on systematic measurements (16 runs) on a test system running X-Plane with ortho streaming and a KVM virtual machine in parallel.

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

The following three steps were applied incrementally on the test system. Each step addresses a specific bottleneck, and measurements confirm the effect before proceeding to the next.

### Step 1: Watermark Tuning — Give kswapd Headroom

**Problem:** The default `vm.min_free_kbytes` value is too small for workloads that allocate memory in large bursts (scenery loading, ortho tile decompression). kswapd wakes too late, and Direct Reclaim takes over — blocking application threads.

**Solution:** The kernel manages three [watermarks](swap.md#watermarks) per memory zone: WMARK_HIGH (kswapd sleeps), WMARK_LOW (kswapd wakes), and WMARK_MIN (Direct Reclaim). The distance between LOW and MIN is the kswapd lead time — the larger it is, the less likely Direct Reclaim becomes.

Two parameters control this:

- `vm.min_free_kbytes` sets WMARK_MIN — the emergency reserve. But it also shifts all watermarks up, locking RAM away from userspace.
- `vm.watermark_scale_factor` sets the **distance** between watermarks independently of the emergency reserve.

The key insight: use `min_free_kbytes` conservatively (1 GB) and `watermark_scale_factor` aggressively (500) to get maximum kswapd lead time with minimum wasted RAM:

```
APPROACH A: min_free_kbytes=3GB, watermark_scale_factor=125
  WMARK_MIN  = 3.0 GB  (locked — wasted)
  WMARK_LOW  = 4.2 GB  (kswapd wakes)
  WMARK_HIGH = 5.4 GB
  Lead time  = 1.2 GB

APPROACH B: min_free_kbytes=1GB, watermark_scale_factor=500
  WMARK_MIN  = 1.0 GB  (only 1 GB locked)
  WMARK_LOW  = 5.8 GB  (kswapd wakes EARLIER)
  WMARK_HIGH = 10.6 GB (MORE lead time)
  Lead time  = 4.8 GB
```

Approach B provides 4x more kswapd lead time while wasting 2 GB less RAM.

**Measured effect**

| Watermark Tuning | Direct Reclaim Main Thread | Max Latency | FPS < 25 |
|---|---|---|---|
| Default (min_free=66 MB) | 12,472 events | 80 ms | 6.9% |
| min_free=2 GB, wsf=125 | 0 (short flights) | 0 ms | 3.1% |
| min_free=2 GB, wsf=125 | 20,515 (Europe 90 min) | 80 ms | 3.8% |
| min_free=3 GB, wsf=125 | 0 (Europe 150 min) | 0 ms | 3.6% |

The table above demonstrates that sufficient watermark distance eliminates Direct Reclaim — `min_free_kbytes=3GB` with `wsf=125` achieved zero events even on 150-minute flights. The final configuration (`min_free_kbytes=1GB`, `watermark_scale_factor=500`) provides the same protection with less wasted RAM: the kswapd lead time is actually larger (4.8 GB vs. 1.2 GB), while the emergency reserve drops from 3 GB to 1 GB.

**Complete sysctl configuration**

```ini title="/etc/sysctl.d/99-xplane-tuning.conf"
vm.min_free_kbytes = 1048576
vm.watermark_scale_factor = 500
vm.swappiness = 8
vm.page_cluster = 0
vm.vfs_cache_pressure = 100
vm.dirty_background_ratio = 3
vm.dirty_ratio = 10
```

```bash
sudo sysctl --system
```

| Parameter | Default | Tuned | Effect |
|---|---|---|---|
| `vm.min_free_kbytes` | ~67 MB | 1 GB | Emergency reserve — kswapd wakes with headroom |
| `vm.watermark_scale_factor` | 10 | 500 | kswapd lead time ~4.8 GB instead of ~96 MB |
| `vm.swappiness` | 60 | 8 | Swap only under real pressure — preserve hot anonymous pages |
| `vm.page_cluster` | 3 | 0 | Single-page swap reads — NVMe has no seek overhead, readahead wastes RAM under pressure |
| `vm.vfs_cache_pressure` | 100 | 100 | Default — no tuning needed |
| `vm.dirty_background_ratio` | 10% | 3% | Writeback starts at ~2.9 GB instead of ~9.4 GB |
| `vm.dirty_ratio` | 20% | 10% | Hard limit at ~9.6 GB instead of ~18.8 GB |

For details on how [watermarks](swap.md#watermarks) and [kswapd](swap.md#page-reclaim) interact, see the Swap page.

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

### Step 3: NVMe Power Management — Eliminate Wake-Up Latency

**Problem:** NVMe SSDs in power-saving mode have wake-up latencies in the millisecond range — longer than a complete frame at 60 Hz. Block tracing showed a characteristic 10–11 ms pattern correlating with frame drops.

**Solution:** Disable NVMe Autonomous Power State Transitions (APST) to keep drives in their lowest-latency operating state.

In `/etc/default/grub`, extend `GRUB_CMDLINE_LINUX_DEFAULT`:

```
nvme_core.default_ps_max_latency_us=0
```

```bash
sudo update-grub
```

Reboot required.

!!! note "Runtime changes"
    The sysfs parameter `/sys/module/nvme_core/parameters/default_ps_max_latency_us` only affects **newly initialized** NVMe devices. For already-active devices, use per-device PM QOS:
    ```bash
    for dev in /sys/class/nvme/nvme*/device/power/pm_qos_latency_tolerance_us; do echo 0 | sudo tee "$dev"; done
    ```
    The GRUB method is the most reliable approach.

**Measured effect:** 97% of slow I/O events (>5 ms) were eliminated. The characteristic 10–11 ms pattern in block tracing disappeared entirely.

---

## Results Summary

The combined effect of all three steps, measured on the test system (steady-state values from a multi-hour session):

| Metric | Baseline | After Tuning | Change |
|---|---|---|---|
| Direct Reclaim (max) | 75,000 pages/s | 0/s (steady state) | Eliminated |
| Alloc Stalls (max) | 1,000/s | 0/s (steady state) | Eliminated |
| Dirty Pages (avg) | 502 MB | 2.4 MB | -99% |
| NVMe Write Latency (avg) | 36 ms | 6 ms | -83% |
| NVMe Write Latency (max, steady state) | 260 ms | 44 ms | -83% |
| NVMe Write Volume | 25 GB/session | 3.6 GB/session | -86% |

!!! tip "Generalizable takeaways"
    The specific values depend on the system and workload, but the **principles** apply broadly:

    1. **Give kswapd headroom via watermark_scale_factor** — this is more effective than raising `min_free_kbytes`, which wastes RAM
    2. **Remove software overhead on NVMe** — multi-queue hardware does not benefit from a software scheduler
    3. **Disable NVMe power saving** — wake-up latencies cause measurable frame drops
    4. **Measure before and after** — aggregate counters from `/proc/vmstat` are sufficient to confirm whether a change had the intended effect

### Field Notes: Lessons from the Tuning Process

The three steps above are presented as a clean progression, but the actual tuning process involved 16 measurement runs and revised conclusions. A few observations that may be useful:

- **Parameters interact non-linearly.** Changing one parameter can invalidate conclusions about another. Always re-evaluate the full set when making significant changes.
- **The three-phase pattern is consistent.** Every run showed the same warm-up → ramp-up → steady-state pattern. Tuning primarily affects the ramp-up phase duration and severity. If your system is stable in steady state but stutters during the first 30–60 minutes, focus on watermark tuning rather than CPU or GPU optimization.
- **NVMe power state latency is real and measurable.** Disabling APST (`pm_qos_latency_tolerance_us=0`) eliminated 97% of slow I/O events (>5 ms). This is a low-effort, high-impact change for any latency-sensitive NVMe workload — not just flight simulation.

---

## Further Reading

| Topic | Page | Focus |
|---|---|---|
| Kernel Tuning | [Kernel Tuning](systemtuning.md) | Two tuning profiles — standard kernel vs. Liquorix |
| Swap & Memory | [Swap & Memory Management](swap.md) | Page reclaim, watermarks, swappiness |
| Monitoring | [Monitoring](systemtools.md) | Tools to measure every metric referenced here |
| Latency | [Latency and Predictability](../../fundamentals/performance/latency.md) | Why latency matters more than throughput |
| Filesystem | [Filesystem](../optimizations/filesystem.md) | IO scheduler, mount options, SSD tuning |

---

## Sources

- [/proc/sys/vm/ — Linux Kernel Documentation](https://docs.kernel.org/admin-guide/sysctl/vm.html) — vm.min_free_kbytes, dirty ratios, swappiness, watermark parameters
- [Memory Management Concepts — Linux Kernel Documentation](https://docs.kernel.org/admin-guide/mm/concepts.html) — Page reclaim, watermarks, kswapd behavior
- [Block layer: Writeback Throttling — LWN](https://lwn.net/Articles/682582/) — WBT mechanism and when to disable it
- [Solid State Drive/NVMe — Arch Wiki](https://wiki.archlinux.org/title/Solid_state_drive/NVMe) — NVMe power management (APST)
