# GPU & VRAM

<div class="video-container" markdown>
<video controls width="100%" preload="metadata" poster="../../../assets/video/en/X-Plane_12_Performance/X-Plane_12_Performance.jpg">
  <source src="../../../assets/video/en/X-Plane_12_Performance/X-Plane_12_Performance.mp4" type="video/mp4">
</video>
</div>

## Introduction

The chapter [CPU & RAM](cpu_ram.md) describes how X-Plane uses its cores and how ortho streaming tools run as separate processes alongside the simulator. This chapter follows the data on its path into graphics memory: how X-Plane manages [VRAM](../../glossary.md#vram-video-ram), why GPU drivers on Linux differ fundamentally, and how the impact on frame time can be measured.

## Architecture: From Streaming Tool to VRAM

All common ortho streaming solutions — [AutoOrtho](../../glossary.md#autoortho), XPME, XEarthLayer — follow the same architectural principle:

```
Streaming Tool                     X-Plane
┌──────────────────────┐           ┌──────────────────────┐
│ Tile download        │           │                      │
│ Tile decoding        │  FUSE     │ Texture Pager        │
│ Cache management     │ ───────►  │ (Disk → RAM → VRAM)  │
│ FUSE filesystem      │  Files    │                      │
└──────────────────────┘           └──────────────────────┘
```

**No streaming tool accesses VRAM directly.** The tools merely provide image files through a [FUSE](../../glossary.md#fuse-filesystem-in-userspace) filesystem — from X-Plane's perspective, these are ordinary [custom scenery](../../glossary.md#custom-scenery) textures. X-Plane reads them through its own texture pager and loads them into its VRAM pool. The VRAM impact is therefore identical across all ortho solutions — X-Plane processes the textures in exactly the same way.

This architecture has an important consequence: the streaming tool's configuration determines *which* textures are available and *how quickly* they arrive — but VRAM management is entirely X-Plane's responsibility.

## VRAM Management

### Asynchronous Texture Paging

X-Plane loads textures asynchronously in three stages:

1. **Disk → RAM:** The texture file is read from the SSD (or FUSE filesystem) into system memory
2. **RAM → GPU upload:** The texture is decompressed, mipmaps are generated, then uploaded to VRAM
3. **VRAM management:** X-Plane decides based on camera position which textures stay loaded and which are evicted

This process runs in the background, as described in the [CPU & RAM](cpu_ram.md) chapter. When VRAM is insufficient, X-Plane automatically downscales texture resolution — instead of crashing, textures appear blurry.

### VRAM Budgeting

VRAM consumption consists of multiple components:

| Component | Typical Share | Influencing Factor |
|---|---|---|
| Scenery textures | Largest share | [Zoom level](../../glossary.md#zl-zoom-level), view distance |
| Aircraft textures | Several GB | Cockpit resolution, liveries |
| Rendering buffers | 1–3 GB | Shadows, reflections, [HDR](../../glossary.md#hdr) |
| UI and overlays | Small | AviTab, maps, menus |

[Orthophotos](../../glossary.md#orthophotos) consume the largest share. The decisive factor is the [zoom level](../../glossary.md#zl-zoom-level) (ZL): each ZL step quadruples the data per area.

| Zoom Level | Ground Resolution | Data per Area (relative) |
|---|---|---|
| ZL 16 | approx. 2.4 m/pixel | 1× |
| ZL 17 | approx. 1.2 m/pixel | 4× |
| ZL 18 | approx. 0.6 m/pixel | 16× |

VRAM requirements grow exponentially — not linearly. An aircraft with a high-resolution cockpit already occupies several gigabytes of VRAM before the first ortho texture is loaded. The entire budget must be calculated, not just the ortho portion.

## GPU Drivers and VRAM Oversubscription

When X-Plane requests more VRAM than is physically available, behavior differs significantly depending on the GPU driver stack. This behavior — VRAM oversubscription — is one of the most relevant differences between GPU vendors and operating systems.

### Linux: Driver-Dependent Behavior

**Proprietary NVIDIA Drivers**

Do not offer transparent paging to system RAM on Linux. When VRAM overflows, X-Plane responds with aggressive texture downscaling. In extreme cases, stutter or device loss may occur. This is the most sensitive combination and requires careful VRAM budgeting.

**[Mesa](../../glossary.md#mesa)/[RADV](../../glossary.md#radv) (AMD)**

The open-source drivers offer better oversubscription through the GTT mechanism (Graphics Translation Table), which partially offloads textures to system RAM. More tolerant than NVIDIA, but with performance drops under heavy oversubscription.

**Mesa/ANV (Intel Arc)**

Offers the best oversubscription on Linux. Most tolerant of VRAM overflow.

### Windows: WDDM Paging

On Windows, the WDDM driver (Windows Display Driver Model) enables automatic paging between VRAM and system RAM — regardless of GPU vendor. This architectural difference explains why ortho configurations that work fine on Windows can cause problems on Linux.

### Device Loss vs. VRAM Problem

A common misconception deserves clarification:

| Symptom | Cause | Action |
|---|---|---|
| Device loss (GPU crash) | Shader or driver bug | Driver diagnostics, update drivers |
| Blurry textures | VRAM overflow → downscaling | Reduce zoom level, lower texture quality |
| Out-of-memory error | VRAM completely exhausted | Reduce VRAM budget |

**Device loss is not a VRAM problem.** A device loss means the GPU has crashed — a fundamental error in the shader or driver. VRAM shortages manifest as texture downscaling or OOM errors, not crashes. The distinction is critical for troubleshooting.

## Frame Time Percentiles

Average [FPS](../../glossary.md#fps-frames-per-second) values obscure the actual experience. More meaningful are percentile values of [frame time](../../glossary.md#frame-time):

| Percentile | Meaning | Typical Experience |
|---|---|---|
| P50 (median) | 50% of all frames are faster | Basic smoothness — how the simulation *usually* feels |
| P95 | 95% of all frames are faster | Occasional stutters — noticeable but rare |
| P99 | 99% of all frames are faster | Worst hitches — brief freezes when loading dense airports or new ortho tiles |

??? abstract "Background: Why averages deceive"

    A simulation with 40 FPS on average can feel smooth or choppy — depending on the distribution. If P99 is at 150 ms, it means: roughly once per second, a single frame hangs for almost a sixth of a second. The FPS counter shows "40", but the image noticeably stutters. Only percentile values reveal these outliers.

### Relevance for VRAM and Ortho Streaming

VRAM pressure is one of the main causes of poor P95/P99 values:

- **Texture loading:** When new ortho tiles are uploaded to VRAM, a brief upload burst occurs that delays the render thread
- **Downscaling decisions:** During VRAM overflow, X-Plane must decide which textures to downscale — this decision costs frame time
- **Cache misses:** When a texture has been evicted from VRAM and is needed again, it must be fully reloaded

### Multi-Threading and Percentiles

As described in the [CPU & RAM](cpu_ram.md) chapter, multi-threading often improves average FPS only marginally. The decisive gain lies in P95 and P99: when scenery processing no longer blocks the main thread, the worst individual frames become shorter.

Without multi-threading, a single core must handle everything — when a heavy scenery chunk arrives, it stalls and produces a stutter. With multi-threading, the load is distributed across multiple cores, and the spikes are smoothed.

**In summary:**

- **P50** (average) → barely changes with multi-threading
- **P95** (occasional stutters) → significant improvement
- **P99** (worst hitches) → strongest improvement

## Practical Consequences

**Choose zoom levels conservatively**

VRAM consumption grows not linearly but exponentially with ZL. A step from ZL 17 to ZL 18 quadruples texture memory requirements. When in doubt, choose one level lower and gain stable frame times.

**Set texture quality deliberately**

X-Plane's "Texture Quality" setting affects how much VRAM is reserved for non-ortho textures. "High" instead of "Maximum" can free several gigabytes of VRAM that then become available for orthophotos.

**Use VRAM monitoring**

GPU monitoring tools show current VRAM utilization in real time. What matters is not the peak value but the behavior over time: does utilization rise continuously (possible leak), stabilize (stable operation), or regularly hit the limit (downscaling zone)?

See [System Monitoring](../../linux/system/systemtools.md) for GPU monitoring tools.

**Calculate the total budget**

Consider not just ortho textures but all VRAM consumers: aircraft, rendering buffers, overlays. A highly detailed cockpit aircraft at ZL 18 can push even a GPU with a large VRAM budget to its limits.

## Further Reading

| Topic | Page | Focus |
|---|---|---|
| Threading model and CPU budget | [CPU & RAM](cpu_ram.md) | Main thread, multi-threading, ortho CPU load |
| Load dimension interactions | [Performance Overview](performance_overview.md) | CPU, I/O, network bottlenecks |
| GPU driver optimization | [Nvidia](../../linux/optimizations/nvidia.md) | Persistence mode, driver tuning |
| Ortho streaming configuration | [AutoOrtho](../../scenery/ortho_streaming/autoortho.md) | Cache, prefetching, tile management |
| X-Plane Microprofiler | [X-Plane Performance](../../xplane/setup_diagnose/performance.md) | Frame time analysis, graphics settings |
| System Monitoring | [Monitoring](../../linux/system/systemtools.md) | GPU monitoring, VRAM tracking |
