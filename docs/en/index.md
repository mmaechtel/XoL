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

### 2026-03-14
- [VATSIM](flight_operations/vatsim/vatsim.md): Flight route recommendations now available as interactive web app at [atc.emvisio.de](https://atc.emvisio.de)
- [XEarthLayer](scenery/ortho_streaming/xearthlayer.md) updated for v0.3.1: GPU-accelerated DDS encoding, ISPC SIMD compression as default, boundary-driven prefetch system, online network support (VATSIM/IVAO/PilotEdge)
- [AutoOrtho](scenery/ortho_streaming/autoortho.md) updated for v2.2.0: ~2x faster loading times, SimBrief integration with route-based prefetch, seasons support

### 2026-03-06
- [How Streaming Works](scenery/ortho_streaming/how_streaming_works.md) expanded: New section on FUSE congestion bottleneck — explains how low `max_background` defaults limit concurrent tile requests and cause frame drops at DSF boundaries

### 2026-02-27
- [Swap & Memory Management](linux/system/swap.md), [System Tuning](linux/system/systemtuning.md), and [Tuning Case Study](linux/system/tuning_casestudy.md) revised: Updated zram recommendations — `swappiness=180` + `watermark_scale_factor=125` instead of `watermark_boost_factor=15000`, based on 14 measurement runs. Separate configuration blocks for zram and disk swap, new field notes on dirty ratio tuning and vfs_cache_pressure





