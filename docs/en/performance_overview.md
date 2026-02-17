# Performance Fundamentals

<div class="video-container" markdown>
<video controls width="100%" preload="metadata" aria-label="Video: The Performance Puzzle" poster="../assets/video/en/The_Performance_Puzzle/The_Performance_Puzzle.jpg">
  <source src="../assets/video/en/The_Performance_Puzzle/The_Performance_Puzzle.mp4" type="video/mp4">
</video>
</div>

## Introduction

Scenery loads slowly, textures are missing during flyovers, micro-stutters appear without any obvious cause — typical symptoms that X-Plane users on Linux will recognize. The root cause is rarely a single component. X-Plane is a hybrid of compute-intensive physics simulation, massive data I/O, and — with ortho streaming — continuous network traffic. Three load dimensions compete for shared resources, and the weakest link determines what makes it to the screen.

This chapter explains the fundamentals of these interactions. Concrete optimization measures are covered in the specialized chapters linked at the end.

## The Three Load Dimensions

X-Plane stresses three hardware subsystems simultaneously, each with its own bottlenecks:

| Load Dimension | Primary Resource | Typical Bottleneck |
|---|---|---|
| CPU Compute | Processor cores, cache, RAM | Clock speed, IPC, cache misses |
| Local I/O | Storage subsystem (SSD/[NVMe](glossary.md#nvme-non-volatile-memory-express)) | IOPS, throughput, [latency](glossary.md#latency) |
| Network Streaming | Network interface, WAN connection | Bandwidth, jitter, packet loss |

**The weakest link determines overall performance — and that weakest link shifts dynamically.** During scenery loading, local I/O dominates (textures loading); in flight, the CPU takes over (physics and rendering); with ortho streaming, the network becomes critical. None of these dimensions can be considered in isolation.

## CPU-Bound Performance

X-Plane's physics model is based on [Blade Element Theory](glossary.md#blade-element-theory): the aircraft is divided into numerous segments, with airflow and forces calculated in real-time for each one. This computation runs on the main thread, making it heavily dependent on single-core performance.

### IPC and Microarchitecture

Raw clock speed only tells half the story. What matters is the number of instructions completed per clock cycle (IPC — Instructions per Cycle). Modern architectures with wide execution units and efficient branch prediction achieve significantly more computations per time unit at the same clock speed compared to older generations.

In X-Plane, low IPC manifests as a hard FPS ceiling: even at maximum clock speed, the framerate stays below expectations because the main thread completes too little work per cycle.

??? abstract "Background: Why IPC Matters More Than Clock Speed"

    A processor core running at 5 GHz with low IPC can be slower than one at 4.5 GHz with high IPC. The IPC rate is determined by the width of execution units, the depth of out-of-order pipelining, and the efficiency of branch prediction. X-Plane benefits particularly from high IPC because Blade Element calculations have sequential dependencies that can only be parallelized to a limited degree.

### Cache Hierarchy and Memory Wall

X-Plane works with large data structures — terrain meshes, scenery objects, texture metadata. When these don't fit in the L3 cache, cache misses force the processor to wait for main memory. At full core utilization, memory bandwidth becomes the bottleneck — a phenomenon known as the "Memory Wall."

The symptom in X-Plane: FPS drops at densely built-up scenery or complex airports, even though CPU utilization isn't at 100%. The processor is waiting for data instead of computing.

??? abstract "Background: Memory Wall"

    On a typical DDR5 system with 35–50 GB/s bandwidth per channel (depending on clock speed), a single core can already demand several GB/s of memory bandwidth. When all cores are active and accessing data outside the L3 cache, the shared memory bandwidth becomes the limiting factor. More cores don't help in this scenario — they make the problem worse.

### Interrupt Load and Context Switches

When the processor simultaneously handles [IRQ](glossary.md#irq-interrupt-request) requests from [NVMe](glossary.md#nvme-non-volatile-memory-express) SSDs and the network interface, compute cores get pulled out of their calculation loops. Each context switch costs not only CPU cycles but also invalidates cache lines and disrupts pipelining. Without dedicated IRQ pinning, this can lead to sporadic micro-stutters — brief [frame time](glossary.md#frame-time) spikes that are difficult to reproduce.

See [System Tuning](system/systemtuning.md) for IRQ pinning and [CPU affinity](glossary.md#cpu-affinity)

## Local I/O Performance

Local I/O load comes from loading scenery data, textures, meshes, and autogen objects. The choice of storage medium has a significant impact on loading times and in-flight stutters.

### Storage Types Compared

| Storage Type | Seq. Read | Random 4K IOPS | Latency |
|---|---|---|---|
| HDD (7200 RPM) | ~200 MB/s | ~100–200 | 5–10 ms |
| SATA SSD | ~550 MB/s | ~80,000–100,000 | 75–150 µs |
| NVMe SSD (PCIe 4.0) | ~7,000 MB/s | ~800,000–1,000,000 | 20–50 µs |
| NVMe SSD (PCIe 5.0) | ~12,000 MB/s | ~1,500,000+ | 15–40 µs |

For X-Plane, both sequential throughput (large texture files) and IOPS (many small scenery files) matter. [NVMe](glossary.md#nvme-non-volatile-memory-express) SSDs offer a 10x+ advantage over SATA SSDs in sequential throughput; the gap in IOPS is similarly large.

### Filesystem and I/O Scheduler

Even with fast hardware, the I/O stack can become a bottleneck. The [I/O scheduler](glossary.md#io-scheduler) affects latency during mixed read/write workloads, and the filesystem — [Ext4](glossary.md#ext4-fourth-extended-filesystem), [Btrfs](glossary.md#btrfs-b-tree-filesystem), or XFS — comes with different journaling strategies.

See [Filesystem](optimizations/filesystem.md) for I/O scheduler, [noatime](glossary.md#noatime), and [TRIM](glossary.md#trim) configuration

### Page Cache Pressure

A practical problem with large scenery installations: when X-Plane reads data heavily, the Linux page cache fills up. Once the system starts dirty page writeback, the entire I/O pipeline can stall — even if the SSD itself is fast enough. This manifests as sudden stutters when loading scenery that have nothing to do with CPU or GPU load.

## Network Streaming

Network I/O plays a growing role in X-Plane. Three typical scenarios generate continuous data traffic:

- **Ortho Streaming:** [AutoOrtho](glossary.md#autoortho) streams [orthophotos](glossary.md#orthophotos) in real-time from the server instead of storing them locally. The data stream must flow fast enough for textures to load before you fly over them.
- **Weather Data:** Real-time weather services deliver wind fields, cloud layers, and precipitation data over the network.
- **VATSIM/Online ATC:** Multiplayer networks generate bidirectional data traffic for position reports and voice communication.

### The Illusion of a Constant Stream

Streaming software assumes that data flows at a steady rate. In practice, that's rarely the case:

- **TCP Congestion Control:** A single lost packet can significantly reduce throughput for several round-trip times. The flow control algorithm throttles preemptively — even when the connection is actually clear.
- **Jitter:** Even with stable average bandwidth, the actual data rate fluctuates significantly. Typical jitter values on WAN connections range from 1 to 50 ms.
- **Shared Bandwidth:** With cloud-hosted data sources, many users share the same infrastructure. "Noisy neighbors" can unpredictably reduce available throughput.

### Impact on the Simulation

When the network stream stalls, X-Plane lacks the texture data for the current viewing area. The result: blurry or missing ground textures, loading stutters, and [frame time](glossary.md#frame-time) spikes. With ortho streaming in particular, every interruption is immediately visible because [AutoOrtho](glossary.md#autoortho) provides textures through a [FUSE](glossary.md#fuse-filesystem-in-userspace) filesystem — X-Plane sees an I/O request that's waiting on network data.

## Interactions Between Dimensions

### Resource Competition

The three load dimensions share CPU cycles and memory bandwidth. An example: X-Plane calculates physics on cores 0–11 while scenery data loads from the NVMe SSD and AutoOrtho receives textures from the network. Without explicit IRQ pinning, both I/O paths land on the same cores. The TCP stack interprets the processing delay as congestion and throttles — the stream stalls.

### PCIe Bandwidth Distribution

The GPU, [NVMe](glossary.md#nvme-non-volatile-memory-express) SSD, and network interface share the available PCIe lanes from the CPU. On a typical desktop processor, simultaneous use of a GPU (16 lanes), an NVMe SSD (4 lanes), and a network interface can exhaust the available PCIe capacity.

??? abstract "Background: PCIe Bandwidth"

    PCIe 4.0 provides ~2 GB/s per lane, PCIe 5.0 ~4 GB/s. A GPU with 16 PCIe 4.0 lanes has a theoretical ~32 GB/s available, an NVMe SSD with 4 lanes ~8 GB/s. When all devices generate high load simultaneously, they share the root complex bandwidth — latencies across all devices increase.

### The Domino Effect

The most dangerous interaction is a chain reaction triggered by streaming interruptions:

1. The network stream stalls (jitter spike)
2. The I/O thread blocks waiting for data
3. Cores go idle — the OS uses them for background tasks
4. The stream returns and delivers data in a burst
5. Backlogged data, new computations, and deferred I/O operations collide

This pattern can briefly overload the system and delay subsequent frames — a self-reinforcing effect that manifests as periodic stutters.

## The Frame as a Unit of Measurement

All three load dimensions affect the same metric: [frame time](glossary.md#frame-time). A frame time of 33 ms corresponds to ~30 [FPS](glossary.md#fps-frames-per-second), 16.6 ms corresponds to ~60 FPS. Any spike in one of the three dimensions — a cache miss, an I/O stall, a network hiccup — directly impacts frame time.

Why consistent frame times matter more than high FPS, and how to diagnose frame time issues with the Microprofiler, is covered in the [System Tuning](system/systemtuning.md) and [X-Plane Performance](xplane/performance.md) chapters.

## Optimization Approaches Overview

The following strategies address the described load dimensions. Each is covered in detail in a specialized chapter.

**Caching and Prefetching**

- AutoOrtho buffers streamed textures locally on the [NVMe](glossary.md#nvme-non-volatile-memory-express) SSD before X-Plane requests them — the most important protection against streaming interruptions
- Cache size and prefetch behavior can be configured in AutoOrtho
- A filesystem with [noatime](glossary.md#noatime) and an appropriate [I/O scheduler](glossary.md#io-scheduler) further reduces I/O path overhead
- See [AutoOrtho](scenery/autoortho.md) and [Filesystem](optimizations/filesystem.md)

**IRQ Pinning and Thread Affinity**

- Pin network [IRQs](glossary.md#irq-interrupt-request) and I/O threads to dedicated CPU cores so the X-Plane main thread can compute undisturbed
- Configure [irqbalance](glossary.md#irqbalance) to keep specific cores free from interrupts
- See [System Tuning](system/systemtuning.md)

**Monitoring and Profiling**

- Monitor CPU utilization per core — idle cores during simulation indicate I/O stalls
- Measure I/O latency and network throughput in parallel to identify the active bottleneck dimension
- See [System Monitoring](system/systemtools.md)

## Further Reading

| Topic | Page | Focus |
|---|---|---|
| System Tuning | [Introduction](system/index.md) | Overview and video |
| CPU & Interrupts | [Tuning](system/systemtuning.md) | [CPU governor](glossary.md#cpu-governor), IRQ pinning, [kernel parameters](glossary.md#kernel-parameter) |
| Storage & Filesystem | [Filesystem](optimizations/filesystem.md) | I/O scheduler, mount options, TRIM |
| Monitoring | [System Monitoring](system/systemtools.md) | CPU, I/O, and network analysis |
| X-Plane Internals | [Performance](xplane/performance.md) | Microprofiler, FPS display, graphics settings |
| Ortho Streaming | [AutoOrtho](scenery/autoortho.md) | Cache configuration, prefetching |
| GPU Driver | [Nvidia](optimizations/nvidia.md) | Driver optimization, persistence mode |
| Kernel | [Liquorix](optimizations/liquorix.md) | Low-latency kernel, scheduler |
