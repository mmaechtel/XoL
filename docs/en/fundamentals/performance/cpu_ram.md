---
title: "CPU & RAM: X-Plane Threading Model"
description: "X-Plane threading model explained: main thread bottleneck, scenery multi-threading, ortho streaming CPU budget, and RAM as staging area."
---
# CPU & RAM

## Introduction

The [performance overview](performance_overview.md) describes why single-core performance, cache hierarchy, and memory bandwidth matter for X-Plane. This chapter goes deeper into how X-Plane actually uses its CPU cores and system memory — particularly when ortho streaming tools run as separate processes alongside the simulator.

## X-Plane's Threading Model

X-Plane distributes its workload across multiple threads with distinct responsibilities:

**Main Thread**

- Physics ([Blade Element Theory](../../glossary.md#blade-element-theory)), avionics, [plugin](../../glossary.md#plugin) callbacks, render preparation
- Heavily single-core dependent — the sequential nature of physics calculations limits parallelization
- Determines the minimum [frame time](../../glossary.md#frame-time): no frame can finish faster than the main thread takes

**Scenery Threads**

- Loading [DSF](../../glossary.md#dsf-distribution-scenery-format) data, object culling, scenery processing
- Distributable across multiple cores (multi-threading)
- Offload heavy loading and processing operations from the main thread

**Texture Pager**

- Asynchronous texture loading: disk → RAM → [VRAM](../../glossary.md#vram-video-ram)
- Runs in the background without directly blocking the render thread
- Generates I/O load on storage and memory bandwidth

**Other Threads**

- Audio ([FMOD](../../glossary.md#fmod)), network (VATSIM, real-time weather), UI rendering

### The Main Thread as Bottleneck

The central architectural principle: the main thread must *complete* every frame before the next one can begin. All other threads feed into the main thread — scenery data, textures, network data. When the main thread waits for data, a [frame time](../../glossary.md#frame-time) spike occurs. When it's overloaded with calculations, the framerate drops uniformly.

This is why X-Plane benefits more from high single-core performance (IPC × clock speed) than from many cores. More cores help with the supporting threads but do not raise the main thread limit.

## Multi-Threading for Scenery Processing

Distributing scenery processing across multiple CPU cores is one of the most impactful architectural changes in recent X-Plane versions.

### Before: Everything on One Core

Without multi-threading, a single core processes all scenery data sequentially. When a heavy scenery chunk arrives — a dense airport, a new ortho tile — that core stalls, and the main thread has to wait. The result: a single long frame that manifests as a stutter.

### After: Distribution Across Multiple Cores

With multi-threading, scenery processing is split across multiple cores. Heavy chunks are processed in parallel without blocking the main thread. Average [FPS](../../glossary.md#fps-frames-per-second) often change only marginally — the decisive improvement lies in the worst individual frames (see [frame time percentiles](gpu_vram.md#frame-time-percentiles)).

??? abstract "Background: Why the average barely improves"

    Multi-threading moves work from the main thread to helper cores. If the main thread previously spent 90% of its time on physics and only 10% on scenery, multi-threading only affects that 10%. The average frame time decreases minimally. The improvement only shows in the extreme cases — frames where the scenery portion exceptionally accounted for 50% or more. These are exactly the frames that multi-threading shortens drastically.

## CPU Budget with Ortho Streaming

With ortho streaming, two independent processes run in parallel on the same CPU:

### Simulator Process (X-Plane)

Uses the threads described above. The main thread claims one core nearly fully, while scenery and texture threads distribute across additional cores.

### Streaming Process (Separate Program)

The ortho streaming tool — whether [AutoOrtho](../../glossary.md#autoortho), XPME, or XEarthLayer — runs as a standalone process with its own tasks:

- **Tile download:** Network I/O for downloading map tiles from CDN servers
- **Tile decoding:** JPEG/PNG decompression and conversion to [DDS](../../glossary.md#dds-directdraw-surface) format — the most CPU-intensive step
- **Cache management:** Managing RAM and disk cache for already downloaded tiles
- **[FUSE](../../glossary.md#fuse-filesystem-in-userspace) layer:** Presents the converted textures as a virtual filesystem from which X-Plane reads

Typical usage: 1–3 CPU cores and 1–4 GB RAM, depending on tool configuration (number of download threads, cache size, prefetch behavior).

### Resource Contention

Both processes share CPU cycles, cache, and memory bandwidth. Without explicit [IRQ](../../glossary.md#irq-interrupt-request) pinning, network interrupts from the streaming tool can land on the same cores that X-Plane's main thread uses. The [performance overview](performance_overview.md) describes this mechanism and countermeasures in detail.

**Rule of thumb for ortho streaming:** 6+ CPU cores provide sufficient headroom for simulator and streaming tool side by side. With 4 cores, contention becomes noticeable — especially at high zoom levels that require more tiles per unit of time.

## RAM as Staging Area

System memory (RAM) plays a triple role:

1. **Texture staging area:** Texture data is loaded from the SSD into RAM, decompressed and prepared there, before being uploaded to [VRAM](../../glossary.md#vram-video-ram)
2. **Cache for the streaming tool:** The ortho tool buffers downloaded and converted tiles in RAM before serving them via [FUSE](../../glossary.md#fuse-filesystem-in-userspace)
3. **Linux page cache:** The kernel automatically caches file accesses in free RAM — with large scenery installations, the page cache can consume several gigabytes

### When RAM Becomes the Bottleneck

RAM itself is rarely the primary bottleneck. It becomes critical in two scenarios:

- **Insufficient free RAM:** When X-Plane, the streaming tool, and the page cache together exhaust available memory, the system starts swapping. The resulting I/O stalls are orders of magnitude slower than RAM accesses.
- **Memory bandwidth exhausted:** At full core utilization, all threads compete for memory bandwidth. The symptom — FPS drops despite CPU utilization below 100% — is described as the memory wall in the [performance overview](performance_overview.md).

**Recommendation:** 32 GB RAM provides sufficient headroom for X-Plane with ortho streaming. 16 GB works but leaves little reserve for the page cache and parallel streaming.

## Further Reading

| Topic | Page | Focus |
|---|---|---|
| Load dimension interactions | [Performance Overview](performance_overview.md) | CPU, I/O, network bottlenecks |
| VRAM management | [GPU & VRAM](gpu_vram.md) | Texture paging, frame time percentiles |
| Latency sources | [Latency and Predictability](latency.md) | Scheduling, interrupts, power states |
| IRQ pinning and CPU affinity | [System Tuning](../../linux/system/systemtuning.md) | CPU governor, kernel parameters |
| I/O scheduler and filesystem | [Filesystem](../../linux/optimizations/filesystem.md) | Mount options, TRIM |
| Ortho streaming configuration | [AutoOrtho](../../scenery/ortho_streaming/autoortho.md) | Cache, prefetching |
| Low-latency kernel | [Liquorix](../../linux/optimizations/liquorix.md) | Scheduler, preemption |
