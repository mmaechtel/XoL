# Why Latency Matters

<div class="video-container" markdown>
<video controls width="100%" preload="metadata" aria-label="Video: Two Paths to Smoother Flight" poster="../../../assets/video/en/Two_Paths_to_Smoother_Flight/Two_Paths_to_Smoother_Flight.jpg">
  <source src="../../../assets/video/en/Two_Paths_to_Smoother_Flight/Two_Paths_to_Smoother_Flight.mp4" type="video/mp4">
</video>
</div>

For X-Plane, temporal predictability matters more than raw throughput — a stable 35 FPS image looks smoother than one fluctuating between 25 and 50. Micro-stutters rarely stem from insufficient computing power but from latency: scheduling delays, CPU wake-up times from sleep states, interrupts at the wrong moment, and blocking memory operations. The tuning page presents two kernel profiles — the stock profile forces application priority, the Liquorix profile removes external disturbances — each tailored to the kernel's scheduling model. Applying the same parameters on the wrong kernel will degrade results.

The monitoring page provides the tools to verify every tuning measure: Is the governor actually active? Are interrupts landing on the protected cores? Is the NVMe causing wake-up latencies? Each tool — from turbostat to mpstat to ioping — maps to a specific tuning setting.

- **[Tuning](systemtuning.md)** — Kernel parameters, CPU governor, interrupt affinity, NVMe tuning
- **[Monitoring](systemtools.md)** — btop, turbostat, perf, mpstat and other analysis tools
