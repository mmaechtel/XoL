---
description: "XEarthLayer is a Rust-based ortho streaming tool for X-Plane 12 on Linux with GPU-accelerated encoding, adaptive prefetch, two-tier cache, and CPU tuning options."
---
# XEarthLayer

**XEarthLayer** is a Rust-based alternative to [AutoOrtho](../../glossary.md#autoortho) for streaming [orthophoto](../../glossary.md#orthophotos) textures in X-Plane 12. The project is inspired by AutoOrtho but relies on a high-performance Rust implementation with optional GPU-accelerated encoding, adaptive prefetching, and a two-tier cache system.

!!! note "Active Development"
    XEarthLayer is a young project under active development. Current versions run stably, but feature scope may change between releases.

## How It Works

XEarthLayer uses a **[FUSE](../../glossary.md#fuse-filesystem-in-userspace)-based virtual file system** (see [How Ortho Streaming Works](how_streaming_works.md)) to provide orthophoto textures on demand. When X-Plane accesses a tile, the satellite image is downloaded from the configured map provider, compressed to [DDS](../../glossary.md#dds-directdraw-surface) format (BC1/BC3), and delivered to the simulator via the VFS.

### DDS Compression Backends

XEarthLayer offers three backends for DDS texture compression, selectable via `compressor` in the `[texture]` section of `config.ini`:

| Backend | Description |
|---|---|
| **ISPC** (default) | Intel ISPC-optimized SIMD compression — significantly faster than the original pure-Rust implementation |
| **GPU** | GPU-accelerated encoding via wgpu/WGSL compute shaders (requires `--features gpu-encode` build flag) |
| **Software** | Pure-Rust fallback, no external dependencies |

The GPU backend offloads BC1/BC3 compression to the graphics card via compute shaders, freeing CPU cores for X-Plane. When multiple GPUs are present, a specific device can be selected via `gpu_device` in the `[texture]` section.

All backends use a **streaming mipmap architecture** that generates mipmaps progressively instead of buffering them in memory, reducing peak memory usage significantly.

### Two-Tier Cache

XEarthLayer uses a two-tier cache system:

1. **Memory cache**: Frequently used tiles are kept in RAM for minimal latency
2. **Disk cache**: All downloaded and converted tiles are persistently stored in region-based subdirectories with parallel scanning for fast startup

When the configured cache size is reached, older tiles are automatically removed to make room for new ones.

### Adaptive Prefetch

XEarthLayer's **adaptive prefetching** uses a boundary-driven model: a `SceneryWindow` tracks the aircraft position relative to DSF tile boundaries, and a `BoundaryMonitor` detects edge crossings on row and column axes. When an edge is crossed, tiles are preloaded with asymmetric depth — typically 3 rows deep and 3–4 columns wide, adjusted to the direction of travel.

The system self-calibrates and adapts its prefetch strategy to available bandwidth and the current flight phase. On-demand tile requests from X-Plane always take priority over prefetch through **priority scheduling** (on-demand jobs run at higher priority than prefetch). A **resource-aware circuit breaker** pauses prefetch when resource pool utilization (CPU, network, disk I/O) exceeds safe thresholds — ensuring that currently visible tiles are always loaded first.

## Map Sources

XEarthLayer supports the following map providers:

- Bing Maps
- Google Maps
- Apple Maps
- ArcGIS
- MapBox
- USGS

## System Requirements

| Requirement | Recommendation |
|---|---|
| Operating system | Linux (FUSE required) |
| Simulator | X-Plane 12.3 or later |
| GPU (optional) | 4 GB VRAM minimum, 12+ GB recommended (for GPU encoding backend) |
| Internet connection | ≥ 500 Mbps recommended |
| Storage | SSD for disk cache |
| Build environment | Rust toolchain (only when building from source) |

!!! note "Linux Only"
    XEarthLayer is currently only available for Linux. Windows and macOS support are not implemented.

## Installation

Pre-built packages are available on the [GitHub Releases page](https://github.com/samsoir/xearthlayer/releases) (`.deb`, `.rpm`, `.tar.gz`).

Installation on Debian:

```bash
# Download the latest .deb package from the releases page and install
sudo dpkg -i xearthlayer_<version>_amd64.deb

# Setup
xearthlayer setup
```

Alternatively, XEarthLayer can be built from source (requires Rust toolchain):

```bash
git clone https://github.com/samsoir/xearthlayer.git
cd xearthlayer
make release            # Standard build (ISPC + Software backends)
# make release-gpu      # Build with GPU encoding backend
make install            # Installs to ~/.local/bin
xearthlayer setup
```

The setup process configures the cache directory and the link to the X-Plane [Custom Scenery](../../glossary.md#custom-scenery) folder. Temporary files are stored in `~/.xearthlayer/tmp` (not the system `/tmp`, which is often RAM-backed and can cause out-of-memory issues).

## Usage

XEarthLayer must be started before X-Plane so that the virtual file system is mounted:

```bash
# Standard start
xearthlayer

# Start with cache pre-warming for a specific airport
xearthlayer run --airport KJFK
```

For adaptive prefetching to work, **ForeFlight telemetry** must be enabled in X-Plane (UDP port 49002) so that XEarthLayer can receive aircraft position and speed data. Alternatively, XEarthLayer can obtain position data from online networks (VATSIM, IVAO, PilotEdge) via their REST APIs.

## Regional Packages

XEarthLayer requires separate **[DSF](../../glossary.md#dsf-distribution-scenery-format)/TER packages** (Digital Surface Format / Terrain) that contain the [mesh](../../glossary.md#mesh) data and terrain definitions for the respective regions. Pre-built packages can be installed directly via the CLI:

```bash
# List available packages
xearthlayer packages list

# Install a package (e.g., Europe)
xearthlayer packages install eu

# Update installed packages
xearthlayer packages update
```

Package downloads run in parallel (configurable 1–10 concurrent parts, default 5) with per-part progress display and automatic retry on failure.

The packages are sourced from the [XEarthLayer Regional Scenery Repository](https://github.com/samsoir/xearthlayer-regional-scenery) and are based on the [Shred86 Ortho4XP fork](https://github.com/shred86/Ortho4XP).

## CPU Tuning

By default, XEarthLayer uses **all available CPU cores** for parallel tile generation. Even with the more efficient ISPC backend, DDS compression remains CPU-intensive. This is optimal when XEarthLayer runs alone — but can lead to bottlenecks when X-Plane is active at the same time.

!!! tip "GPU Encoding as Alternative"
    With the GPU encoding backend, DDS compression is offloaded to the graphics card. This reduces CPU load but can lead to GPU bottlenecks, since X-Plane itself is GPU-intensive. The trade-off depends on available VRAM and GPU headroom.

### The Problem

X-Plane is heavily main-thread bound. When XEarthLayer saturates all cores, this leads to:

- **Thread oversubscription**: More active threads than available cores force constant context switches
- **Hyperthreading limitation**: Two CPU-intensive threads on the same physical core together reach only about 120–130% of a single thread's performance
- **X-Plane stuttering**: Frame time increases because the X-Plane main thread competes for CPU time

### Relevant Settings

Three settings in `~/.xearthlayer/config.ini` control CPU usage:

| Setting | Section | Default | Function |
|---|---|---|---|
| `threads` | `[generation]` | Number of CPUs | Worker threads for tile generation |
| `cpu_concurrent` | `[executor]` | ~CPUs × 1.25 | Concurrent DDS encoding operations (most effective lever) |
| `max_concurrent_jobs` | `[control_plane]` | CPUs × 2 | Maximum concurrent tile jobs overall |

### Recommended Values

**Rule of thumb**: When running X-Plane in parallel, limit to half the *physical* cores.

| Scenario | `threads` | `cpu_concurrent` | `max_concurrent_jobs` |
|---|---|---|---|
| XEL alone (default) | 16 | 20 | 32 |
| XEL + X-Plane | 6–8 | 6–8 | 12–16 |
| XEL + X-Plane + streaming | 4 | 4 | 8 |

*Example values for a system with 16 logical CPUs (8 cores + hyperthreading)*

---

## Comparison with AutoOrtho

| Dimension | XEarthLayer | AutoOrtho (ProgrammingDinosaur Fork) |
|---|---|---|
| Programming language | Rust (+ optional GPU compute shaders) | Python + native C pipeline |
| DDS compression | ISPC SIMD (default) or GPU-accelerated | C-based with dedicated decode pool |
| Prefetch strategy | Boundary-driven (adaptive depth) | Proximity-based |
| Cache eviction | Automatic (older tiles removed) | Automatic (older tiles removed) |
| X-Plane 12 features | Full (seasons, regional textures — via Ortho4XP-based DSF/TER packages) | Yes (seasons built-in) |
| Platform | Linux only | Windows, Linux, macOS (Apple Silicon) |
| Simulator | X-Plane 12 only | X-Plane 11.50+ and 12 |
| Installation | Binary packages or from source | Binary installer or Python |
| Regional packages | Integrated CLI install (`xearthlayer packages install`) | Integrated overlay downloads |
| SimBrief integration | In development | Yes |
| GUI | CLI with live dashboard | GUI with configuration panels |

XEarthLayer is aimed at Linux users seeking maximum streaming performance through GPU offloading and boundary-driven prefetch. AutoOrtho offers broader platform support, seasons, and an easier GUI-based setup.

---

## Further Reading

| Topic | Page | Focus |
|---|---|---|
| AutoOrtho | [AutoOrtho](autoortho.md) | Alternative streaming solution with wider platform support |
| Ortho4XP | [Ortho4XP](../orthophotography/ortho4xp.md) | Static ortho tile generation for offline use |
| Static + Streaming | [Static + Streaming](static_plus_streaming.md) | Combining local tiles with streaming |
| Scenery Components | [How X-Plane Builds the World](../aufbau_quellen/scenery_components.md) | scenery_packs.ini load order |
| Kernel Tuning | [Kernel Tuning](../../linux/system/systemtuning.md) | CPU governor, IRQ pinning, scheduler tuning |
| Filesystem | [Filesystem](../../linux/optimizations/filesystem.md) | NVMe/SSD optimization for cache performance |

---

## Sources

- [GitHub Repository](https://github.com/samsoir/xearthlayer)
- [XEarthLayer Website](https://xearthlayer.app/)
- [Regional Scenery Packages](https://github.com/samsoir/xearthlayer-regional-scenery)
