---
title: X-Plane Performance Fundamentals
description: "X-Plane performance fundamentals: CPU, I/O, and network load dimensions, VRAM management, frame time analysis, and latency sources."
---
# Performance

X-Plane is a hybrid of real-time physics simulation, massive data I/O, and — with ortho streaming — continuous network traffic. These three load dimensions compete for shared resources: CPU cycles, cache, memory bandwidth, and PCIe lanes. The bottleneck shifts dynamically — during scene loading storage dominates, in flight the CPU, during streaming the network. The chapters in this section explain where bottlenecks arise and how they amplify each other.

The main thread remains the central bottleneck: physics, avionics, and render preparation run sequentially on a single core. Multi-threading for scenery processing offloads that core but primarily improves the worst individual frames (P95/P99), not average FPS. VRAM management is entirely X-Plane's responsibility — no streaming tool accesses graphics memory directly. Demand grows exponentially with zoom level, and overflow behavior on Linux differs fundamentally depending on the GPU driver. Frame time percentiles reveal what FPS averages conceal. Why temporal predictability matters more than raw throughput, and which system sources generate latency, is explained in a dedicated chapter.

- **[Load Dimensions](performance_overview.md)** — CPU, I/O, and network: identifying bottlenecks
- **[Latency and Predictability](latency.md)** — Why latency matters more than throughput, four latency sources
- **[CPU & RAM](cpu_ram.md)** — Threading model, core allocation, and RAM as staging area
- **[GPU & VRAM](gpu_vram.md)** — Texture paging, driver differences, and frame time analysis
