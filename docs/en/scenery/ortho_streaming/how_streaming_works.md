---
description: "How ortho streaming works in X-Plane: the DSF→.ter→DDS texture chain, FUSE virtual filesystem, streaming pipeline, cache architecture, and Linux advantages."
---
# How Ortho Streaming Works

Ortho streaming replaces X-Plane's default ground textures with satellite imagery — downloaded on demand at runtime instead of pre-generated and stored locally. Tools like [AutoOrtho](autoortho.md) and [XEarthLayer](xearthlayer.md) achieve this by intercepting X-Plane's texture requests through a [FUSE](../../glossary.md#fuse-filesystem-in-userspace) virtual filesystem and routing them to online map providers. This page explains the underlying architecture that both tools share.

## X-Plane's Texture Loading Chain

[X-Plane](../../glossary.md#x-plane) divides the world into 1° × 1° tiles stored as [DSF](../../glossary.md#dsf-distribution-scenery-format) files (Distribution Scenery Format). Textures are loaded through a three-stage reference chain:

1. **DSF file** — contains terrain type paths as indexed references. DSF commands point to terrain types by index number only.
2. **`.ter` file** (Terrain Type) — a text file that controls how a terrain patch is rendered. Key directives:
    - `BASE_TEX <filename>` — primary terrain texture (required)
    - `LIT_TEX <filename>` — night overlay
    - `LOAD_CENTER <lat> <lon> <size_m> <tex_size_px>` — proximity-based texture loading
3. **[DDS](../../glossary.md#dds-directdraw-surface) texture** — the actual image data, referenced by the `.ter` file. Paths are resolved relative to the `.ter` file location.

The `LOAD_CENTER` directive enables **proximity-based resolution management**: textures are loaded at variable resolution depending on aircraft distance, with full resolution only near the specified center point. At greater distances, the simulator progressively degrades texture resolution — saving VRAM without visible quality loss at altitude. DDS format is essential here because its mipmap structure allows partial loading; PNG would require full decompression followed by CPU-side rescaling.

Streaming tools exploit this chain: the `.ter` files point to texture paths inside a FUSE mount, so every texture read becomes a streaming opportunity.

??? abstract "Technical Background: .ter vs .pol for Orthophotos"
    X-Plane supports two methods for applying orthophotos:

    - **`.ter` base mesh replacement**: Replaces the terrain mesh textures directly. Static paging, no mesh duplication. This is the method used by AutoOrtho and XEarthLayer.
    - **`.pol` draped polygon overlay**: Projects orthophotos on top of existing mesh. Only rendered near the aircraft, incurs permanent CPU overhead, and doubles VRAM consumption. Not suitable for large-area coverage.

    Laminar Research recommends `.ter` replacement for orthophoto scenery.

---

## FUSE: The Virtual Filesystem

[FUSE](../../glossary.md#fuse-filesystem-in-userspace) (Filesystem in Userspace) is the bridge between X-Plane's file reads and the streaming tools. It consists of three components:

- **`fuse.ko`** — kernel module that registers the `fuse` filesystem type with Linux's VFS layer
- **`libfuse`** — userspace library providing the filesystem operation API
- **`fusermount`** — mount utility for unprivileged mounts (automatically applies `nosuid` and `nodev`)

Communication between kernel and userspace daemon runs through the `/dev/fuse` character device.

### How Streaming Tools Use FUSE

1. The streaming tool mounts a virtual filesystem in the [Custom Scenery](../../glossary.md#custom-scenery) directory
2. Scenery packages (DSF + `.ter` files) reference textures at paths inside this FUSE mount
3. X-Plane loads a DSF → follows the `.ter` chain → texture path resolves into the FUSE directory
4. The FUSE daemon intercepts the `read()` call
5. The filename is parsed to extract tile coordinates, map provider, and zoom level
6. The request is routed to the cache/download system instead of a real filesystem

Both tools require `user_allow_other` in `/etc/fuse.conf` to be enabled, so X-Plane (running as a separate process) can access the FUSE mount.

??? abstract "Technical Background: FUSE Request Lifecycle"
    When X-Plane reads a file on a FUSE mount, the request follows this path:

    **Phase 1 — Request initiation:**

    1. X-Plane calls `read()` syscall
    2. Kernel VFS routes to the FUSE handler
    3. Request is placed on the pending queue
    4. The userspace daemon is woken up

    **Phase 2 — Userspace processing:**

    1. The FUSE daemon reads from `/dev/fuse`
    2. Request moves from pending to processing queue
    3. The daemon performs the actual work (download satellite image, convert to DDS)

    **Phase 3 — Response:**

    1. Daemon writes the result back to `/dev/fuse`
    2. Kernel wakes the waiting X-Plane thread
    3. Data is returned to X-Plane

    **Context switch overhead:** A native filesystem operation requires 2 context switches; FUSE requires 4. For ortho streaming this overhead is irrelevant — the bottleneck is network latency (50–200 ms), not filesystem latency (microseconds).

---

## The Streaming Pipeline

When X-Plane needs a terrain texture, the complete request flow looks like this:

```
X-Plane loads DSF tile
  → DSF references .ter terrain definition (by index)
    → .ter specifies BASE_TEX with LOAD_CENTER
      → Texture path resolves into FUSE mount
        → FUSE intercepts read()
          → Filename parsed → cache lookup
            → L1 Memory cache: hit → immediate return
            → L2 Disk cache: hit → load, promote to L1, return
            → L3 Network: download from map provider
              → Download JPEG/PNG tiles
                → Stitch tiles together
                  → DDS compression (BC1/BC3) with mipmaps
                    → Store in L1 + L2 cache
                      → Return DDS bytes via FUSE read()
                        → Kernel delivers data to X-Plane
                          → X-Plane uploads texture to GPU
```

### Cache Architecture

Both streaming tools use a multi-tier cache to minimize redundant downloads:

| Tier | Medium | Behavior |
|------|--------|----------|
| L1 — Memory | RAM | Frequently used tiles, LRU eviction at configured limit |
| L2 — Disk | SSD | Persistent storage, automatic eviction when size limit is reached |
| L3 — Network | Internet | Download from map provider on cache miss |

A warm cache (filled after the first visit to a region) makes subsequent flights feel nearly instantaneous — tiles are served from SSD or RAM without any network requests.

### DDS Compression

The DDS format uses GPU-native block compression:

- **BC1 (DXT1)**: 4 bits/pixel, RGB only. Standard compression for ortho textures. 8:1 compression ratio.
- **BC3 (DXT5)**: 8 bits/pixel, RGBA with alpha channel. Used for textures with transparency (water edges, terrain transitions).

Both formats include **mipmaps** — progressively halved copies of the same texture (4096 → 2048 → 1024 → 512 → ...). X-Plane's `LOAD_CENTER` mechanism requests only the mipmap level matching the aircraft's distance. AutoOrtho exploits this by downloading and storing **only the actually requested mipmap levels** — dramatically reducing both download volume and storage compared to pre-generated approaches.

---

## Value on Linux

FUSE has been part of the Linux kernel since 2005. No third-party driver, no kernel extension, no administrator privileges required for mounting — `/dev/fuse` is universally available on all distributions. The only configuration step: uncomment `user_allow_other` in `/etc/fuse.conf`.

| Aspect | Linux (FUSE) | Windows (WinFSP/Dokan) |
|--------|-------------|----------------------|
| Kernel integration | Mainline kernel module | Third-party driver, separate installation |
| Installation | None — already in the kernel | WinFSP or Dokan installer (admin rights required) |
| Antivirus interference | None | Windows Defender scans FUSE mounts → I/O overhead |
| Symlinks | Native, trivial | Elevated privileges or Developer Mode required |
| Stability | Mature, extensively tested | AutoOrtho documentation warns of "filesystem variations" and "intrusive malware detection" |

XEarthLayer is a direct consequence of this Linux advantage: its Rust implementation with async Tokio runtime uses the `fuse3` crate for clean, native FUSE 3 integration — without the cross-platform abstraction layers that a Windows port would require. Combined with X-Plane 12's native Vulkan renderer on Linux, the entire stack runs without compatibility layers.

---

## When Loading Takes Longer

Ortho streaming delivers satellite imagery in real time — but sometimes tiles visibly pop in or blurry textures persist longer than expected. The most common reasons:

| Cause | Explanation | Mitigation |
|-------|-------------|------------|
| Empty cache (first visit) | No cached tiles exist for this region. Every texture triggers a network download. | Fly the area once at cruise altitude to warm the cache. XEarthLayer supports `--airport` pre-warming. |
| Slow or overloaded network | Map servers respond slowly, or local bandwidth is insufficient. | Check connection speed. Consider switching map providers. |
| Settings changed | Changing zoom level or map provider invalidates existing cache entries. | Expect slower loading after settings changes until the cache refills. |
| Rate limiting (HTTP 429) | Map providers throttle clients that send too many requests in a short period. | Switch to a different map provider or use a VPN. AutoOrtho logs this as `HTTP 429: Too Many Requests`. |
| High zoom level | Higher zoom means exponentially more tiles per area. ZL18 requires 4× more tiles than ZL17. | Reduce maximum zoom level if loading cannot keep up. |
| CPU contention | DDS compression competes with X-Plane for CPU time, causing both to slow down. | Limit worker threads (XEarthLayer: `cpu_concurrent`, AutoOrtho: configuration). See [XEarthLayer CPU Tuning](xearthlayer.md#cpu-tuning). |
| Fast low-level flight | Low altitude + high speed demands more tiles per second than cruise flight at high altitude. | Expected behavior — the cache fills as you fly. Prefetching helps (especially XEarthLayer's adaptive modes). |

!!! tip "Cache is your best friend"
    After the first visit to a region, subsequent flights load almost entirely from disk or memory cache. The initial "slow" experience is a one-time cost per region and zoom level.

---

## Further Reading

| Topic | Page | Focus |
|-------|------|-------|
| AutoOrtho | [AutoOrtho](autoortho.md) | Streaming configuration, fork features, Ortho4XP comparison |
| XEarthLayer | [XEarthLayer](xearthlayer.md) | Rust-based streaming with adaptive prefetch and CPU tuning |
| Static + Streaming | [Static + Streaming](static_plus_streaming.md) | Combining local Ortho4XP tiles with streaming |
| Scenery Components | [How X-Plane Builds the World](../aufbau_quellen/scenery_components.md) | scenery_packs.ini load order and layer interaction |
| Filesystem | [Filesystem](../../linux/optimizations/filesystem.md) | I/O optimization for SSD cache performance |

---

## Sources

- [DSF Usage In X-Plane](https://developer.x-plane.com/article/dsf-usage-in-x-plane/) — Laminar Research Developer Documentation
- [Terrain Type (.ter) File Format](https://developer.x-plane.com/article/terrain-type-ter-file-format-specification/) — Laminar Research Developer Documentation
- [Three Things You Need for Fast Orthophotos](https://developer.x-plane.com/2011/03/three-things-you-need-for-fast-orthophotos/) — Laminar Research Developer Blog
- [FUSE — Linux Kernel Documentation](https://www.kernel.org/doc/html/next/filesystems/fuse/fuse.html) — Kernel.org
- [AutoOrtho Technical Details](https://kubilus1.github.io/autoortho/latest/details/) — AutoOrtho Project Documentation
- [XEarthLayer Repository](https://github.com/samsoir/xearthlayer) — GitHub
