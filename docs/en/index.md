---
description: "X-Plane 12 on Linux — setup guides, kernel tuning, GPU drivers, filesystem optimization, scenery management, and addon catalog."
---
# **XoL**: Running **X**-Plane **o**n **L**inux

This documentation covers setup and optimization of X-Plane 12 (Laminar Research) under Linux. It is aimed at experienced Linux users — a working installation is assumed. The examples are based on Debian but transfer to other distributions with minor adjustments.

## Where to Start

- **Why Linux?** [Introduction](intro.md) explains what makes X-Plane on Linux different.
- **New to X-Plane on Linux?** [Getting Started](begin.md) covers system requirements, installation, and first launch.
- **X-Plane already running?** [Performance](fundamentals/performance/performance_overview.md) explains the three load dimensions (CPU, I/O, network) before diving into [System Tuning](linux/system/systemtuning.md).

## About This Documentation

The core focus is on Linux system tuning — kernel parameters, CPU governor, GPU drivers, display server selection, and filesystem optimization — complemented by performance analysis using both X-Plane's built-in tools and Linux monitoring utilities. Additional sections cover scenery management with orthophoto streaming, flight operations including ATC procedures, and a reference catalog of Linux-compatible addons and plugins. The guides are modular — individual topics can be implemented independently or combined as needed.

## Contributing

This documentation is an open project. Improvements or additions can be contributed via GitHub:

- Create issues for bugs or suggestions
- Submit pull requests for changes
- Share experiences in the discussions in the footer of this website (e.g., via the Discord link)

## Featured Video: X-Plane 12 Performance

<div class="video-container" style="max-width: 640px;" markdown>
<video controls width="100%" preload="metadata" aria-label="Video: X-Plane 12 Performance" poster="../assets/video/en/X-Plane_12_Performance/X-Plane_12_Performance.jpg">
  <source src="../assets/video/en/X-Plane_12_Performance/X-Plane_12_Performance.mp4" type="video/mp4">
</video>
</div>

[All Videos →](videos.md)

## Recent Changes

### 2026-04-08
- [XEarthLayer](scenery/ortho_streaming/xearthlayer.md) updated for v0.4.3: Three-tier cache with DDS disk layer eliminates re-encoding, speed-proportional prefetch box reduces over-fetching by ~45%, GPU encoding now built-in, CPU concurrency defaults to 50%

### 2026-04-04
- [XEarthLayer](scenery/ortho_streaming/xearthlayer.md) updated for v0.4.1: Streaming mipmap architecture cuts peak memory by 21–44%, parallel package downloads, temp directory moved to `~/.xearthlayer/tmp`
- [SimLoad Manager](addon/flylua_scripts/simloadmanager.md) updated for v3.7: Flight save/resume system, ACARS loadsheet uplink for ToLiss via Hoppie, new aircraft support (Flight Factor 757/767, FPS 747-800)

### 2026-03-21
- [Tuning Case Study](linux/system/tuning_casestudy.md) rewritten: Three-step diagnosis from micro-stutters to stable frame times — watermark tuning, IO latency, and NVMe power management with real measurements from 16 runs
- [Swap & Memory Management](linux/system/swap.md) rewritten: Page reclaim mechanics, watermark tuning, swap configuration — zram removed, simplified to disk swap with `watermark_scale_factor=500`
- [Kernel Tuning](linux/system/systemtuning.md) revised: Streamlined profiles for stock and Liquorix kernels, updated memory and NVMe sections






