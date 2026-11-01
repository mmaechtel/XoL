---
description: "XEarthLayer — Rust-based ortho streaming for X-Plane 12 on Linux with GPU-accelerated encoding, adaptive prefetch, generated night lighting, and a three-tier cache."
---
# XEarthLayer

**XEarthLayer** is a Rust-based alternative to [AutoOrtho](../../glossary.md#autoortho) for streaming [orthophoto](../../glossary.md#orthophotos) textures in X-Plane 12. The project is architecturally influenced by AutoOrtho but relies on a high-performance Rust implementation with built-in GPU-accelerated encoding, adaptive prefetching, generated night lighting, and a three-tier cache system.

!!! note "Active Development"
    XEarthLayer is a young project under active development. Current versions run stably, but feature scope may change between releases.

## How It Works

XEarthLayer uses a **[FUSE](../../glossary.md#fuse-filesystem-in-userspace)-based virtual file system** (see [How Ortho Streaming Works](how_streaming_works.md)) to provide orthophoto textures on demand. All installed ortho packages are combined into a single mount, `zzXEL_ortho`, in the Custom Scenery folder; overlay packages are linked into `yzXEL_overlay`. When X-Plane accesses a tile, the satellite image is downloaded from the configured map provider, compressed to [DDS](../../glossary.md#dds-directdraw-surface) format (BC1/BC3), and delivered to the simulator via the VFS. All other files (DSF, TER) pass through unchanged from the package.

### DDS Compression Backends

XEarthLayer offers three backends for DDS texture compression, selectable via `compressor` in the `[texture]` section of `config.ini`:

| Backend | Description |
|---|---|
| **ISPC** (default) | Intel ISPC SIMD compression, 5–10× faster than the software backend; prebuilt kernels included |
| **GPU** | GPU-accelerated encoding via wgpu/WGSL compute shaders (select at runtime via `texture.compressor = gpu`) |
| **Software** | Pure-Rust fallback, no external dependencies |

The GPU backend offloads BC1/BC3 compression to the graphics card via compute shaders, freeing CPU cores for X-Plane. It pays off on systems with both an integrated and a discrete GPU — for example an AMD Radeon iGPU on a Ryzen processor alongside a dedicated NVIDIA card — where the integrated GPU handles DDS encoding while the discrete GPU runs X-Plane. On a single-GPU system, GPU encoding competes with the simulator for the same card; XEarthLayer then logs a warning, and the setup wizard keeps ISPC. The adapter is chosen via `gpu_device` in the `[texture]` section of `config.ini`:

| Value | Effect |
|---|---|
| `integrated` (default) | Use the integrated GPU |
| `discrete` | Use the discrete GPU |
| *name substring* | Match by adapter name (e.g. `Radeon`, `RTX 5090`) |

Run `xearthlayer diagnostics` to list all available GPU adapters (only Vulkan adapters are listed on Linux; hosts with nothing but OpenGL fall back to ISPC).

### Three-Tier Cache

XEarthLayer uses a three-tier cache hierarchy:

- **Memory cache**: Staging buffer in RAM
- **DDS disk cache**: Encoded DDS tiles persist to disk and are the actual retention layer, avoiding re-encoding on revisits. Budget split configurable via `cache.dds_disk_ratio` (default 60:40 DDS to chunks; with night lighting enabled, applied to the 95% left after its 5% share)
- **Chunk disk cache**: Raw downloaded imagery chunks

When the configured cache size is reached, older tiles are automatically removed to make room for new ones. The setup wizard sizes the disk cache dynamically (default 25% of free space, floored to 10 GB) and derives the memory-cache budget from available RAM. The cache lives in `~/.cache/xearthlayer/` by default; a fast NVMe or SSD that is not the system volume is recommended via `cache.directory`. Tiles with failed chunk downloads are served to X-Plane but not cached.

### Adaptive Prefetch

XEarthLayer's **adaptive prefetching** queues scenery ahead of the aircraft before X-Plane requests it. The prefetch area moves with the aircraft. On the ground it is a square of `box_extent` centred on the aircraft; in cruise it grows with ground speed up to `box_extent` and shifts in the direction of travel. Prefetch runs in **its own lane** and yields to X-Plane's tile requests, so it never delays them; it also pauses during scenery loading, replay, or when telemetry stops. Prefetch is on by default; `prefetch.enabled = false` or `xearthlayer run --no-prefetch` switches it off.

### Night Lighting

The regional packages carry night recipes, from which XEarthLayer generates the lit textures (`*_LIT.dds`) X-Plane requests at night — so cities on ortho scenery stay lit even where X-Plane's autogen lights do not reach. The textures are built from the lit art of the local X-Plane installation and NASA VIIRS night-light data; the lit layer switches off close to the aircraft, where X-Plane's own 3D lights take over. Night lighting is enabled by default (`night.enabled`) and takes 5% of the disk cache.

## Map Sources

XEarthLayer supports the following map providers (selected via `provider.type` or in the setup wizard):

- Bing Maps (default)
- Google via GO2 (public tile servers, no API key)
- Google Maps API (paid API key)
- Apple Maps
- ArcGIS
- MapBox (access token required)
- USGS (US only)

## System Requirements

| Requirement | Recommendation |
|---|---|
| Operating system | Linux x86_64 with FUSE (prebuilt binaries: glibc 2.34 or newer); macOS on Apple Silicon with macFUSE |
| Simulator | X-Plane 12 |
| GPU | 8 GB VRAM minimum, 16+ GB recommended (for X-Plane rendering) |
| Internet connection | ≥ 800 Mbps recommended |
| Storage | SSD/NVMe for disk cache |
| Build environment | Rust via rustup and FUSE 3 headers (only when building from source) |

!!! note "Platforms"
    XEarthLayer runs on Linux and on macOS (Apple Silicon). There is no Windows build.

## Installation

Release builds are available on the [GitHub Releases page](https://github.com/samsoir/xearthlayer/releases) as `.deb` (Debian/Ubuntu), `.rpm` (Fedora/RHEL), and `x86_64-linux.tar.gz` tarball; Arch users build from the AUR. Pre-releases ship for Linux as a tarball only.

```bash
# Run in the download directory. Debian/Ubuntu: install the .deb from the releases page
sudo dpkg -i xearthlayer_*_amd64.deb

# Other distributions: unpack the tarball to ~/.local/bin
tar xzf xearthlayer-v*-x86_64-linux.tar.gz
mkdir -p ~/.local/bin
mv xearthlayer ~/.local/bin/
```

Alternatively, XEarthLayer can be built from source. Rust should be installed via [rustup](https://rustup.rs), since distribution packages are usually too old; rustup picks up the toolchain version pinned in the repository automatically:

```bash
sudo apt install libfuse3-dev   # Fedora: sudo dnf install fuse3-devel
git clone https://github.com/samsoir/xearthlayer.git
cd xearthlayer
make install                    # Builds and installs to ~/.local/bin (GPU backend included)
```

!!! warning "Switching from the previous package generation"
    The current library is a rebuilt world under new region codes. Old and new packages overlap and must not be installed side by side. All old packages have to be removed **before** installing new ones — also before the setup wizard offers the package manager. After updating the program, run:

    ```bash
    xearthlayer config upgrade
    xearthlayer packages remove --all --force
    xearthlayer packages remove --all --type overlay --force
    ```

Then run the setup wizard:

```bash
xearthlayer setup
```

The setup wizard walks through the X-Plane [Custom Scenery](../../glossary.md#custom-scenery) folder, the package location, the imagery provider, cache sizing, and the encoding backend (including GPU adapter selection), detects SimHeaven X-World Pro, and finally offers to open the package manager.

XEarthLayer follows the XDG conventions:

| What | Default path |
|---|---|
| Configuration | `~/.config/xearthlayer/config.ini` |
| Tile cache | `~/.cache/xearthlayer/` |
| Packages | `~/.local/share/xearthlayer/packages` |
| Logs | `~/.local/state/xearthlayer/` |

Temporary package downloads go to `~/.cache/xearthlayer/tmp` (not the system `/tmp`, which is often RAM-backed). Installations still using the older `~/.xearthlayer` layout are migrated automatically on first start: only `config.ini` is copied, while packages and cache stay in place and their old paths are written into the new configuration. `xearthlayer migrate` reviews the locations afterwards.

## Usage

XEarthLayer must be started before X-Plane so that the virtual file system is mounted:

```bash
# Standard start
xearthlayer

# Start with cache pre-warming for a specific airport
xearthlayer run --airport KJFK
```

Aircraft position, heading, and speed come automatically from the **X-Plane Web API** (port 8086) — no configuration in X-Plane is needed as long as the Web API is not disabled. A non-default port is set via `prefetch.web_api_port`. Without the Web API, XEarthLayer infers the position from FUSE access patterns.

XEarthLayer should only be stopped after X-Plane has exited — with `q` on the dashboard, or Ctrl+C. Terminating XEarthLayer while X-Plane is running crashes the simulator.

## Regional Packages

XEarthLayer requires separate **[DSF](../../glossary.md#dsf-distribution-scenery-format)/TER packages** (Distribution Scenery Format / Terrain) that contain the [mesh](../../glossary.md#mesh) data and terrain definitions for the respective regions. The library covers the world in 17 regions (about 161 GB in total, Antarctica not yet available). The interactive **package manager** handles installing, updating, and removing in the terminal:

```bash
# Open the package manager (Local, Library, Progress, Settings tabs)
xearthlayer packages

# Or on the command line: install one or more regions
xearthlayer packages install eu-west na-canada

# Update installed packages
xearthlayer packages update --all
```

Region codes are hierarchical (`EU-WEST`, `NA-CANADA-EAST`, `AS-CHINA-MONGOLIA` …); a prefix selects every package beneath it, so `na-canada` installs both halves of Canada. Matching overlay packages (roads, buildings) are only installed along with ortho packages if `packages.auto_install_overlays = true` is set (default `false`). Downloads run in parallel (`packages.concurrent_downloads`, 1–10, default 5), and the next package downloads while the previous one installs. New packages can be installed while XEarthLayer is running and are used on the next start; updates and removals are refused while it runs.

Users of SimHeaven X-World Pro set `packages.xworld_pro = true`: XEarthLayer then leaves out its own overlays on the continents X-World Pro covers and checks the `scenery_packs.ini` order at startup. `packages.disable_overlays = true` suppresses all XEarthLayer overlays without deleting them.

The packages are sourced from the [XEarthLayer Regional Scenery Repository](https://github.com/samsoir/xearthlayer-regional-scenery) and are generated with OXO (Ortho4 XEarthLayer Orchestrator), an Ortho4XP-based build pipeline.

## CPU Tuning

Even with the efficient ISPC backend, DDS compression remains CPU-intensive. XEarthLayer derives its internal concurrency (download, encoding, and disk I/O pools) from the number of logical cores; these pool sizes are not configurable. Older keys such as `cpu_concurrent` or `max_concurrent_jobs` in the `[executor]` section have no effect and are removed by `xearthlayer config upgrade`.

!!! tip "GPU Encoding as Alternative"
    For systems with a second GPU, see [DDS Compression Backends](#dds-compression-backends).

### The Problem

X-Plane is heavily main-thread bound. When XEarthLayer saturates all cores, this leads to:

- **Thread oversubscription**: More active threads than available cores force constant context switches
- **Hyperthreading limitation**: Threads on the same physical core share execution units, so additional logical CPUs do not add the throughput of additional physical cores
- **X-Plane stuttering**: Frame time increases because the X-Plane main thread competes for CPU time

### Relevant Settings

Two settings in `~/.config/xearthlayer/config.ini` control how much CPU XEarthLayer takes:

| Setting | Section | Default | Function |
|---|---|---|---|
| `threads` | `[generation]` | Half the CPU cores | Worker threads for tile generation |
| `capacity_share` | `[prefetch]` | `0.35` (0.05–0.50) | Prefetch capacity as a fraction of the capacity on-demand requests get |

**Rule of thumb**: When running X-Plane in parallel, `threads` should not exceed half the *physical* cores. If prefetch costs frame rate, `capacity_share` is lowered — prefetch no longer competes with X-Plane's tile requests, but it still competes with the simulator for CPU time.

---

## Comparison with AutoOrtho

| Dimension | XEarthLayer | AutoOrtho (ProgrammingDinosaur Fork) |
|---|---|---|
| Programming language | Rust (+ optional GPU compute shaders) | Python + native C pipeline |
| DDS compression | ISPC SIMD (default) or GPU-accelerated | C-based with dedicated decode pool |
| Prefetch strategy | Speed-scaled box ahead of the aircraft, separate prefetch lane | Position-based, optionally along the SimBrief route |
| Cache eviction | Automatic (older tiles removed) | Automatic (older tiles removed) |
| X-Plane 12 features | Regional mesh and terrain packages (generated with OXO), plus generated night lighting | Yes (seasons built-in) |
| Platform | Linux, macOS (Apple Silicon) | Windows, Linux, macOS (Apple Silicon) |
| Simulator | X-Plane 12 (X-Plane 11 untested) | X-Plane 11.50+ and 12 |
| Installation | `.deb`/`.rpm`/tarball, AUR, or from source | Binary installer or Python |
| Regional packages | Integrated package manager (TUI and CLI) | Integrated overlay downloads |
| GUI | CLI with live dashboard and package manager TUI | GUI with configuration panels |

XEarthLayer is aimed at Linux users seeking maximum streaming performance through GPU offloading, a prefetch lane that never blocks X-Plane, and generated night lighting. AutoOrtho offers broader platform support including Windows and an easier GUI-based setup.

---

## Further Reading

| Topic | Page | Focus |
|---|---|---|
| XPME | [XPME](xpme.md) | Closed-source freemium alternative, paid high-resolution tier |
| AutoOrtho | [AutoOrtho](autoortho.md) | Alternative streaming solution with wider platform support |
| Ortho4XP | [Ortho4XP](../orthophotography/ortho4xp.md#building-packages-for-ortho-streaming) | Building the mesh-only DSF/TER packages this layer draws on |
| Static + Streaming | [Static + Streaming](static_plus_streaming.md) | Combining local tiles with streaming |
| Scenery Components | [How X-Plane Builds the World](../aufbau_quellen/scenery_components.md) | scenery_packs.ini load order |
| Kernel Tuning | [Kernel Tuning](../../linux/system/systemtuning.md) | CPU governor, IRQ pinning, scheduler tuning |
| Filesystem | [Filesystem](../../linux/optimizations/filesystem.md) | NVMe/SSD optimization for cache performance |

---

## Sources

- [GitHub Repository](https://github.com/samsoir/xearthlayer)
- [Configuration Reference](https://github.com/samsoir/xearthlayer/blob/main/docs/configuration.md)
- [Package Management](https://github.com/samsoir/xearthlayer/blob/main/docs/package-management.md)
- [XEarthLayer Website](https://xearthlayer.app/)
- [Regional Scenery Packages](https://github.com/samsoir/xearthlayer-regional-scenery)
