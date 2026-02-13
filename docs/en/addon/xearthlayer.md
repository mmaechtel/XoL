# XEarthLayer

**XEarthLayer** is a Rust-based alternative to AutoOrtho for streaming orthophoto textures in X-Plane 12. The project is inspired by AutoOrtho but relies on a high-performance Rust implementation with adaptive prefetching and a two-tier cache system.

!!! warning "Early Development Stage"
    XEarthLayer is in active development. Feature scope and stability may change significantly between versions.

## How It Works

XEarthLayer uses a **FUSE-based virtual file system** to provide orthophoto textures on demand. When X-Plane accesses a tile, the satellite image is downloaded from the configured map provider, converted to DDS format (BC1/BC3 compression), and delivered to the simulator via the VFS.

### Two-Tier Cache

XEarthLayer uses a two-tier cache system:

1. **Memory cache**: Frequently used tiles are kept in RAM for minimal latency
2. **Disk cache**: All downloaded and converted tiles are persistently stored on disk

When the configured cache size is reached, older tiles are automatically removed to make room for new ones.

### Adaptive Prefetch

A core feature of XEarthLayer is its **adaptive prefetching**, which switches between two modes:

- **Ground mode (ring prefetch)**: At low altitude and speed, tiles are preloaded in concentric rings around the current position — optimal for approach situations and low-level flying
- **Cruise mode (track prediction)**: At higher speed and altitude, the system predicts the expected flight path and preloads tiles along the projected route

The system self-calibrates and adapts its prefetch strategy to available bandwidth and the current flight phase. A **circuit breaker mechanism** ensures that prefetch requests are deprioritized when on-demand requests from X-Plane need priority — ensuring that currently visible tiles are always loaded first.

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
| Simulator | X-Plane 12 |
| Internet connection | ≥ 800 Mbps recommended |
| Storage | SSD for disk cache |
| Build environment | Rust toolchain (only when building from source) |

!!! note "Linux Only"
    XEarthLayer is currently only available for Linux. Windows and macOS support are not implemented.

## Installation

Pre-built packages for various distributions are available on the [GitHub Releases page](https://github.com/samsoir/xearthlayer/releases):

- **Debian/Ubuntu**: `.deb` package
- **Fedora**: `.rpm` package
- **Arch Linux**: AUR package
- **Other distributions**: generic `.tar.gz` archive

Example for Debian/Ubuntu:

```bash
# Download and install the .deb package
sudo dpkg -i xearthlayer_0.3.0-1_amd64.deb

# Setup
xearthlayer setup
```

Alternatively, XEarthLayer can be built from source (requires Rust toolchain):

```bash
git clone https://github.com/samsoir/xearthlayer.git
cd xearthlayer
make release
make install    # Installs to ~/.local/bin
xearthlayer setup
```

The setup process configures the cache directory and the link to the X-Plane Custom Scenery folder.

## Usage

XEarthLayer must be started before X-Plane so that the virtual file system is mounted:

```bash
# Standard start
xearthlayer

# Start with cache pre-warming for a specific airport
xearthlayer run --airport KJFK
```

For adaptive prefetching to work, **ForeFlight telemetry** must be enabled in X-Plane (UDP port 49002) so that XEarthLayer can receive aircraft position and speed data.

## Regional Packages

XEarthLayer requires separate **DSF/TER packages** (Digital Surface Format / Terrain) that contain the mesh data and terrain definitions for the respective regions. Pre-built packages can be installed directly via the CLI:

```bash
# List available packages
xearthlayer packages list

# Install a package (e.g., Europe)
xearthlayer packages install eu

# Update installed packages
xearthlayer packages update
```

The packages are sourced from the [XEarthLayer Regional Scenery Repository](https://github.com/samsoir/xearthlayer-regional-scenery) and are based on the [Shred86 Ortho4XP fork](https://github.com/shred86/Ortho4XP).

## CPU Tuning

By default, XEarthLayer uses **all available CPU cores** for parallel tile generation and DDS compression. This is optimal when XEarthLayer runs alone — but causes problems when X-Plane is active at the same time.

### The Problem

X-Plane is heavily main-thread bound. When XEarthLayer saturates all cores, this leads to:

- **Thread oversubscription**: More active threads than available cores force constant context switches
- **Hyperthreading limitation**: Two CPU-intensive threads on the same physical core together reach only about 120–130% of a single thread's performance
- **X-Plane stuttering**: Frame time increases because the X-Plane main thread competes for CPU time

### Relevant Settings

Three settings in `~/.xearthlayer/config.ini` form a hierarchy:

| Setting | Section | Default | Function |
|---|---|---|---|
| `threads` | `[generation]` | Number of CPUs | Worker threads for tile generation |
| `cpu_concurrent` | `[executor]` | CPUs × 1.25 | Concurrent CPU-intensive operations (DDS encoding) |
| `max_concurrent_jobs` | `[control_plane]` | CPUs × 2 | Maximum concurrent tile jobs overall |

The most effective lever is `cpu_concurrent` — it limits DDS encoding operations (BC1/BC3 compression), which account for the largest CPU share.

### Recommended Values

**Rule of thumb**: When running X-Plane in parallel, limit to half the *physical* cores.

| Scenario | `threads` | `cpu_concurrent` | `max_concurrent_jobs` |
|---|---|---|---|
| XEL alone (default) | 16 | 20 | 32 |
| XEL + X-Plane | 6–8 | 6–8 | 12–16 |
| XEL + X-Plane + streaming | 4 | 4 | 8 |
| XEL in background | 2 | 2 | 4 |

*Example values for a system with 16 logical CPUs (8 cores + hyperthreading)*

```ini
# ~/.xearthlayer/config.ini — example for XEL + X-Plane
[generation]
threads = 6

[executor]
cpu_concurrent = 6

[control_plane]
max_concurrent_jobs = 12
```

!!! tip "Network is often the bottleneck"
    With a slow internet connection, reducing CPU threads barely affects performance since the threads are waiting for downloads anyway. The prefetch system automatically adapts to the lower throughput.

Additionally, the disk I/O profile indirectly affects CPU load:

| `disk_io_profile` | Concurrent I/O ops | Recommended for |
|---|---|---|
| `hdd` | 1–4 | Traditional hard drives |
| `ssd` | 32–64 | SATA/AHCI SSDs |
| `nvme` | 128–256 | NVMe drives |
| `auto` (default) | Auto-detected | Most systems |

---

## Comparison with AutoOrtho

| Dimension | XEarthLayer | AutoOrtho (ProgrammingDinosaur Fork) |
|---|---|---|
| Programming language | Rust | Python (+ C pipeline in 2.0) |
| Prefetch strategy | Adaptive (ground/cruise modes) | Simple (proximity-based) |
| Cache eviction | Automatic (older tiles removed) | Automatic (older tiles removed) |
| Platform | Linux only | Windows, Linux, macOS |
| Simulator | X-Plane 12 only | X-Plane 11.50+ and 12 |
| Installation | Binary packages or from source | Binary or Python |
| Regional packages | Separate DSF/TER packages needed | Integrated overlay downloads |
| GUI | None | Modern GUI available |

XEarthLayer is aimed at Linux users seeking maximum streaming performance who are willing to set up a Rust build environment. AutoOrtho offers broader platform support and easier setup.

## Resources

- [GitHub Repository](https://github.com/samsoir/xearthlayer)
