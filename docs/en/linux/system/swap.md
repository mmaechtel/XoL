---
description: "Linux swap and memory management for X-Plane: page reclaim mechanics, watermark tuning, swap configuration, and tuning recommendations for flight simulation."
---
# Swap & Memory Management

[X-Plane](../../glossary.md#x-plane) with addons and ortho streaming can consume 20–30 GB of RAM. When physical memory runs out, the Linux kernel begins swapping — moving memory pages to disk. For a real-time rendering application, every swap-in introduces a page fault that stalls the rendering thread. Understanding how the kernel manages memory and configuring swap correctly prevents stutters, frame drops, and OOM kills.

## How Swap Works

### Page Reclaim

The kernel manages physical memory in **pages** (4 KiB each). When free memory drops below defined thresholds, the kernel must reclaim pages. It distinguishes two categories:

- **File-backed pages** (page cache): Cache data from files on disk. Clean pages can be discarded immediately since the data exists on disk. Dirty pages must be written back first.
- **Anonymous pages** (heap, stack, private mappings): Have no file system backing. These can **only** be reclaimed by writing them to swap — without swap, they are unrecoverable and the process gets killed.

Reclaim runs in two modes:

| Mode | Trigger | Behavior |
|---|---|---|
| **kswapd** (async) | Free memory < Low Watermark | Background thread, does not block applications |
| **Direct Reclaim** (sync) | Free memory < Min Watermark | The allocating process is blocked until pages are freed — causes latency spikes |

When Direct Reclaim also fails, the kernel activates the **OOM-Killer**.

### Watermarks

The kernel defines three thresholds per memory zone:

| Watermark | Effect |
|---|---|
| WMARK_HIGH | Enough memory available. kswapd sleeps. |
| WMARK_LOW | kswapd wakes up and starts background reclaim. |
| WMARK_MIN | Critical. Direct Reclaim is triggered. Allocations are blocked. |

The watermarks are controlled by:

- `vm.min_free_kbytes`: Sets WMARK_MIN (default: system-dependent, typically tens of MB)
- `vm.watermark_scale_factor`: Distance between watermarks (default: 10 = 0.1% of RAM)

### vm.swappiness

The simplified explanation "controls how aggressively the system swaps" is incomplete. `vm.swappiness` defines the **relative I/O cost ratio** between swapping anonymous pages and reclaiming file-backed pages.

**Value range:** 0–200 (default: 60)

| Value | Behavior |
|---|---|
| 0 | Anonymous pages are **not** scanned — only file-backed pages are reclaimed. Risk: OOM kills despite available swap. |
| 60 (default) | Moderate preference for file reclaim. |
| 100 | Equal weighting between anonymous and file-backed pages. |
| 200 | File-backed pages are not scanned — the kernel reclaims only anonymous pages, preserving file cache. |

??? abstract "Kernel-internal calculation"

    The kernel computes scan priorities in `mm/vmscan.c`:

    ```
    anon_prio = swappiness
    file_prio = 200 - swappiness
    ```

    These priorities feed into the scan decision as weighting factors. The ratio determines how many anonymous vs. file-backed pages are checked per scan cycle. At `swappiness=0`, anonymous pages are never scanned — the kernel only falls back to swap when free pages drop below the high watermark and no file-backed pages remain reclaimable.

!!! warning "swappiness=0 is risky"
    Setting `swappiness=0` can cause OOM kills even when swap space is available, because the kernel refuses to scan anonymous pages until it is too late. Values between 1 and 10 are safer for low-swap configurations.

---

## Swap Configuration

### Partition vs. File

| Property | Swap Partition | Swap File |
|---|---|---|
| Performance | Marginally better (no filesystem overhead) | Practically identical on ext4/XFS |
| Flexibility | Fixed size, repartitioning needed | Size easily adjustable |
| Setup effort | Requires dedicated partition | Can be created on existing partition |

For ext4 systems, both options are equivalent. Swap files offer more flexibility.

### Setup on Debian

**Swap Partition**

```bash
# Create partition with gdisk (type code: 8200)
sudo mkswap /dev/sdXn
sudo swapon /dev/sdXn
```

Add to `/etc/fstab` (use UUID from `blkid /dev/sdXn`):

```
UUID=<uuid>    none    swap    sw    0    0
```

**Swap File**

```bash
sudo dd if=/dev/zero of=/swapfile bs=1M count=8192    # 8 GiB
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

Add to `/etc/fstab`:

```
/swapfile    none    swap    sw    0    0
```

!!! warning "Do not use fallocate"
    `fallocate` creates files with preallocated but unwritten extents. The kernel reports these as holes, causing `swapon` to reject the file. Use `dd` for swap files.

### Sizing

| RAM | Recommended Swap |
|---|---|
| 16 GB | 8–16 GB |
| 32 GB | 4–8 GB |
| 64 GB | 4 GB |

### Swap Priorities

When multiple swap areas are configured, priorities control which is used first:

- **Different priorities:** Highest priority fills first. Lower priority serves as fallback.
- **Equal priorities:** Pages are distributed round-robin — effective striping across devices.

```
UUID=<uuid1>    none    swap    sw,pri=100    0    0
UUID=<uuid2>    none    swap    sw,pri=10     0    0
```

---

## Impact on X-Plane

### RAM Consumption

| Configuration | Typical Usage |
|---|---|
| Base installation (default scenery) | 10–14 GB |
| With addon aircraft + custom scenery | 16–24 GB |
| With ortho streaming (AutoOrtho/XEarthLayer) | 20–30+ GB |

[AutoOrtho](../../glossary.md#autoortho) alone can consume up to 16 GB of RAM. On a 32 GB system, swap activity can occur during scenery transitions or when other applications run in parallel.

### What Happens When X-Plane Pages Get Swapped

Every swap-in triggers a **major page fault**: the rendering thread is blocked while the kernel reads the page from the swap device. On [NVMe](../../glossary.md#nvme-non-volatile-memory-express), a single swap-in takes ~15 µs — fast enough for occasional swapping. On SATA, ~150 µs per page fault accumulate into visible stutters. On HDD, ~12 ms per fault causes multi-second freezes.

With ortho streaming active, three I/O streams compete on the same storage device:

1. **AutoOrtho/XEarthLayer** cache writes ([FUSE](../../glossary.md#fuse-filesystem-in-userspace)-based)
2. **Swap I/O** (pages being read/written)
3. **DSF scenery loading** by X-Plane (background threads)

### Same SSD vs. Dedicated SSD

| Configuration | Impact |
|---|---|
| Swap on same NVMe as X-Plane | Unproblematic for occasional swapping. NVMe provides enough IOPS. Risk: tail latency under heavy load. |
| Swap on same SATA SSD | Noticeable — queue depth limited (NCQ: max 32 commands). Swap competes directly with scenery loading. |
| Swap on dedicated SSD | Eliminates I/O contention completely. Rarely necessary for desktop/gaming systems. |

### Latency Comparison

| Medium | Random 4K Read Latency | Factor vs. RAM |
|---|---|---|
| DDR5 RAM | ~15 ns | 1x |
| NVMe SSD | ~15 µs | ~1,000x |
| SATA SSD | ~150 µs | ~10,000x |
| HDD | ~12 ms | ~800,000x |

### OOM-Killer

When the system runs out of both RAM and swap, the kernel activates the OOM-Killer. It selects the process with the highest badness score (primarily based on memory consumption) — almost always X-Plane.

- X-Plane is terminated immediately via `SIGKILL` (signal 9) — no clean shutdown, no save
- The kernel log (`dmesg`) shows: `Out of memory: Kill process <PID> (X-Plane-x86_64)`

---

## Recommended Configuration

### Watermark Tuning

The most effective measure against memory-related stutters is watermark tuning. Instead of raising `min_free_kbytes` to large values (which wastes RAM), use `watermark_scale_factor` to give kswapd more lead time:

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

!!! note "Why watermark_scale_factor=500?"
    The default `watermark_scale_factor=10` creates a gap of only ~96 MB between watermarks on a 96 GB system. At 500, the kswapd lead time grows to ~4.8 GB — kswapd wakes significantly earlier, preventing burst allocations (scenery loading, ortho tile decompression) from breaching the min watermark and triggering Direct Reclaim on application threads. See the [Tuning Case Study](tuning_casestudy.md#step-1-watermark-tuning-give-kswapd-headroom) for detailed measurements.

!!! note "Why swappiness=8?"
    With disk swap on NVMe, every swap-in costs ~15 µs — a page fault that blocks the rendering thread. Low swappiness tells the kernel that swap is expensive: it should prefer reclaiming file-backed pages (which can be discarded without I/O) over swapping anonymous pages. The large page cache (typically 30–40 GB during flight) provides ample reclaimable pages before swap is needed.

### Kernel Parameters Summary

| Parameter | Value | Effect |
|---|---|---|
| `vm.min_free_kbytes` | 1048576 (1 GB) | Emergency reserve — kswapd wakes with headroom |
| `vm.watermark_scale_factor` | 500 | kswapd lead time ~4.8 GB instead of ~96 MB |
| `vm.swappiness` | 8 | Swap only under real pressure — preserve hot anonymous pages |
| `vm.page_cluster` | 0 | Single-page swap reads — NVMe has no seek overhead |
| `vm.vfs_cache_pressure` | 100 | Default — no tuning needed |
| `vm.dirty_background_ratio` | 3 | Writeback starts at ~2.9 GB instead of ~9.4 GB |
| `vm.dirty_ratio` | 10 | Hard limit at ~9.6 GB instead of ~18.8 GB |

### RAM Sizing Guide

| RAM | Assessment |
|---|---|
| 16 GB | Minimum. Swap activity likely with addons or ortho streaming. Adequate swap partition essential. |
| 32 GB | Comfortable for most configurations. Swap as safety net for scenery transitions. |
| 64 GB | Swap should be inactive under normal conditions. |

!!! tip "RAM is the sustainable solution"
    Swap tuning is damage mitigation. The only way to reliably avoid swap-related performance degradation is sufficient physical RAM. For X-Plane with ortho streaming, 32 GB is the practical baseline.

### Field Notes: Dirty Ratio Tuning

The `dirty_background_ratio` and `dirty_ratio` settings interact with the memory configuration in non-obvious ways. During extended testing (16 measurement runs over several weeks with ortho streaming on NVMe), the following observations emerged:

- **Too aggressive writeback hurts on large-RAM systems.** With `dirty_background_ratio=1` on a 96 GB system, the writeback daemon fires at ~960 MB dirty — practically every tile cache write triggers a flush cycle. This burns CPU cycles and I/O bandwidth that compete with X-Plane's rendering. Raising to `dirty_background_ratio=3` (~2.9 GB threshold) let NVMe batch writes efficiently without constant flushing.
- **dirty_ratio headroom matters more than the absolute value.** At `dirty_ratio=5` (~4.8 GB), the gap between background (960 MB) and synchronous (4.8 GB) writeback was too narrow — parallel DDS tile generation could breach it during burst writes. Widening to `dirty_ratio=10` (~9.6 GB) eliminated write stalls entirely on NVMe.
- **These values are not universal.** They were tuned for a system with three NVMe SSDs in RAID0 that can sustain >6 GB/s sequential writes. Systems with SATA SSDs or single NVMe drives may need tighter limits to prevent I/O queue buildup.

The recommended values in [Profile B](systemtuning.md#profile-b-liquorix-kernel) (`dirty_background_ratio=3`, `dirty_ratio=10`) reflect this balance.

---

## Further Reading

| Topic | Page | Focus |
|---|---|---|
| Kernel Tuning | [Kernel Tuning](systemtuning.md) | CPU governor, sysctl profiles, interrupt affinity |
| Monitoring | [Monitoring](systemtools.md) | Verify swap activity with btop, vmstat, swapon |
| CPU & RAM | [CPU & RAM](../../fundamentals/performance/cpu_ram.md) | When RAM becomes the bottleneck |
| Filesystem | [Filesystem](../optimizations/filesystem.md) | SSD optimization, I/O scheduler, mount options |
| Latency | [Latency and Predictability](../../fundamentals/performance/latency.md) | Latency sources and measurement |
| Case Study | [Tuning Case Study](tuning_casestudy.md) | Practical impact of watermark and memory tuning with real measurements |

---

## Sources

- [Memory Management Concepts — Linux Kernel Documentation](https://docs.kernel.org/admin-guide/mm/concepts.html)
- [/proc/sys/vm/ — Linux Kernel Documentation](https://docs.kernel.org/admin-guide/sysctl/vm.html)
- [Swap — Arch Wiki](https://wiki.archlinux.org/title/Swap)
- [Swap — Debian Wiki](https://wiki.debian.org/Swap)
