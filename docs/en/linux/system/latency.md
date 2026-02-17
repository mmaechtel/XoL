---
description: "Why latency matters for X-Plane on Linux: stable frame times beat high FPS, two kernel tuning profiles, and monitoring tools for verification."
---
# Why Latency Matters

<div class="video-container" markdown>
<video controls width="100%" preload="metadata" aria-label="Video: Two Paths to Smoother Flight" poster="../../../assets/video/en/Two_Paths_to_Smoother_Flight/Two_Paths_to_Smoother_Flight.jpg">
  <source src="../../../assets/video/en/Two_Paths_to_Smoother_Flight/Two_Paths_to_Smoother_Flight.mp4" type="video/mp4">
</video>
</div>

For X-Plane, temporal predictability matters more than raw throughput — a stable 35 FPS image looks smoother than one fluctuating between 25 and 50. Micro-stutters rarely stem from insufficient computing power but from latency: scheduling delays, CPU wake-up times from sleep states, interrupts at the wrong moment, and blocking memory operations. The tuning page presents two kernel profiles — the stock profile forces application priority, the Liquorix profile removes external disturbances — each tailored to the kernel's scheduling model. Applying the same parameters on the wrong kernel will degrade results.

The monitoring page provides the tools to verify every tuning measure: Is the governor actually active? Are interrupts landing on the protected cores? Is the NVMe causing wake-up latencies? Each tool — from turbostat to mpstat to ioping — maps to a specific tuning setting.

The theoretical foundations — why latency matters more than throughput and which system sources generate latency — are covered in the [Latency and Predictability](../../fundamentals/performance/latency.md) chapter.

- **[Tuning](systemtuning.md)** — Kernel parameters, CPU governor, interrupt affinity, NVMe tuning
- **[Monitoring](systemtools.md)** — btop, turbostat, perf, mpstat and other analysis tools

---

## Further Reading

| Topic | Page | Focus |
|---|---|---|
| Kernel Tuning | [Kernel Tuning](systemtuning.md) | CPU governor, interrupt affinity, NVMe tuning |
| Monitoring | [Monitoring](systemtools.md) | Verify tuning with turbostat, mpstat, ioping |
| Latency and Predictability | [Latency and Predictability](../../fundamentals/performance/latency.md) | Theoretical foundations of system latency |
| Liquorix Kernel | [Liquorix Kernel](../optimizations/liquorix.md) | Low-latency kernel with PDS scheduler |
| Load Dimensions | [Load Dimensions](../../fundamentals/performance/performance_overview.md) | CPU, GPU, IO — where bottlenecks form |
