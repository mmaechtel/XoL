---
title: "X-Plane Fundamentals: CPU, I/O, Network"
description: "How X-Plane distributes workload across CPU, storage I/O, and network — understanding the competing resource demands before optimizing."
---
# Fundamentals

X-Plane distributes its workload across three axes — CPU, storage I/O, and network — all competing for shared hardware resources: CPU cycles, cache, memory bandwidth, and PCIe lanes. Where the bottleneck lies shifts with flight phase and configuration: storage dominates while scenery loads, the CPU in flight, the network during ortho streaming. This section builds the mental model needed before touching a single setting — the following Linux and X-Plane chapters assume it.

Start with the [load dimensions](performance/performance_overview.md) to see how the three axes interact, then read why [latency and predictability](performance/latency.md) matter more than average FPS. The [CPU & RAM](performance/cpu_ram.md) chapter explains the main-thread bottleneck and what multi-threading can and cannot offload; [GPU & VRAM](performance/gpu_vram.md) covers texture paging, driver differences, and frame time percentiles. Readers who only want practical tuning steps can skip ahead to [System](../linux/system/index.md) — but the steps there build on the concepts introduced here.

- **[Performance](performance/index.md)** — CPU, GPU memory and I/O: load dimensions, threading and VRAM analysis
