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

### 2026-02-19
- [My FS Flights](addon/kvm/myfs_flights.md) revised: Documented IP configuration in plugin settings, confirmed KVM-to-Linux connection as tested

### 2026-02-18
- [AutoOrtho](scenery/ortho_streaming/autoortho.md) corrected: Fixed wrong USGS provider reference, removed unverified RAM and bandwidth figures
- [XEarthLayer](scenery/ortho_streaming/xearthlayer.md) corrected: Updated internet recommendation from 800 to 500 Mbps, removed version-specific install command, added sources
- [AutoOrtho](scenery/ortho_streaming/autoortho.md) revised: Improved page structure with section separators, removed redundant Conclusion section, unified bold formatting
- [XEarthLayer](scenery/ortho_streaming/xearthlayer.md) corrected: Fixed misleading Rust build environment requirement in comparison section
- [XEarthLayer](scenery/ortho_streaming/xearthlayer.md) revised: Toned down stability warning to reflect current maturity, added CLI live status output to comparison table

### 2026-02-17
- New videos: [GPU & VRAM](fundamentals/performance/gpu_vram.md) — GPU performance and VRAM management (DE + EN)
- Further Reading sections added across Linux, Flight Operations, Scenery, and X-Plane sections (33 pages)
- [CPU & RAM](fundamentals/performance/cpu_ram.md), [GPU & VRAM](fundamentals/performance/gpu_vram.md), [Latency](fundamentals/performance/latency.md): Further Reading sections standardized with additional cross-references
- New page [Latency and Predictability](fundamentals/performance/latency.md) — Why latency matters more than throughput, four latency sources
- Complete restructure: All sections split into thematic subdirectories with section index pages — content summaries cascade from deepest level upward
- New pages: [CPU & RAM](fundamentals/performance/cpu_ram.md) — Threading model and system memory, [GPU & VRAM](fundamentals/performance/gpu_vram.md) — Texture paging, driver differences and frame time analysis
- New page: [Why Latency Matters](linux/system/latency.md) — Video introduction to the tuning philosophy



