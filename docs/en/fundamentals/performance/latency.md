---
title: Latency and Predictability in X-Plane
description: "Latency vs. throughput in X-Plane: why temporal predictability beats raw FPS, and four system sources that cause frame time spikes."
---
# Latency and Predictability

X-Plane calculates a complex world with physics, weather, scenery, and input devices. What determines result quality is not maximum computing power but temporal predictability — how consistently each individual frame is computed. This chapter explains why latency is the real problem and which system sources cause it. The three load dimensions (CPU, I/O, network) and their interactions are covered in the [Load Dimensions](performance_overview.md) chapter.

## Performance and Latency — An Important Distinction

When people talk about "performance," they usually mean high FPS. That's correct for shooters or racing games — throughput matters there: as many frames per second as possible. A flight simulator like X-Plane is different.

X-Plane calculates a complex world with physics, weather, scenery, and input devices. Individual frames are expensive, and the target framerate is typically 25–35 [FPS](../../glossary.md#fps-frames-per-second). What matters is not the average, but **consistency** — [frame-time](../../glossary.md#frame-time) regularity. A system delivering a stable 35 FPS produces smoother motion than one fluctuating between 25 and 50.

The cause of inconsistency is usually not insufficient computing power, but **[latency](../../glossary.md#latency)** — short delays from system events that interrupt the main thread.

Typical symptoms of poor latency:

- Micro-stutters despite stable CPU/GPU load
- Delayed input response (joystick, rudder pedals)
- Inconsistent reaction time in the same scene

**Key insight:** For X-Plane, latency optimization matters more than throughput maximization. Temporal predictability beats raw computing power.

## Understanding Latency Sources

System latency doesn't originate from a single source but from four independent categories:

| Category | Impact | Typical Symptom |
|---|---|---|
| **Scheduling** | Delayed thread start | Stutters after load spikes |
| **Power Management** | Wake-up latency from sleep states | Periodic brief interruptions |
| **Interrupts** | Competition for CPU time | Stutters during I/O or input |
| **Memory/IO** | Blocking background operations | Stutters when loading new scenery |

**Scheduling**

The Linux scheduler decides when a thread gets CPU time. A conservative scheduler waits longer before reacting — this saves power but increases latency. Modern schedulers use deadline-based task selection and adaptive [preemption](../../glossary.md#preemption), allowing latency-sensitive threads to be scheduled more efficiently.

**Power Management**

CPU load doesn't cause stutters — transitions between power states do. When a core wakes from a deep sleep state, delays of up to several hundred microseconds occur. [NVMe](../../glossary.md#nvme-non-volatile-memory-express) SSDs in power-saving mode also produce noticeable wake-up latencies (details under [Disable NVMe Power Saving](../../linux/system/systemtuning.md#disable-nvme-power-saving)).

**Interrupts**

Hardware interrupts (USB devices, network, storage) preempt the running thread. A single interrupt at the wrong time can violate a frame deadline:

```
periodic main thread + random interrupt = missed deadline
```

**Memory/IO**

The kernel optimizes throughput through batched background work (writeback, cache cleanup, paging). This creates rare but noticeable blocks — especially when loading large ortho textures.

---

## Further Reading

| Topic | Page | Focus |
|---|---|---|
| Kernel Tuning | [Kernel Tuning](../../linux/system/systemtuning.md) | Concrete parameters for both kernel profiles |
| Load Dimensions | [Load Dimensions](performance_overview.md) | CPU, I/O, network — identifying bottlenecks |
| CPU & RAM | [CPU & RAM](cpu_ram.md) | Threading model, main thread as bottleneck |
| GPU & VRAM | [GPU & VRAM](gpu_vram.md) | Frame time percentiles, VRAM pressure |
| Low-Latency Kernel | [Liquorix](../../linux/optimizations/liquorix.md) | Scheduler, preemption tuning |
| Why Latency Matters | [Why Latency Matters](../../linux/system/latency.md) | Introduction and video |
| Monitoring | [System Monitoring](../../linux/system/systemtools.md) | Measuring and verifying latency |
