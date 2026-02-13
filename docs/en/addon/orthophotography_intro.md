# Introduction to Orthophotography in Flight Simulation

Orthophotography represents a central component of modern flight simulation environments, as it enables high-resolution and realistic ground textures. This section explains the methodological approaches for integrating high-quality orthophotos into the X-Plane flight simulation software.

## Significance of Orthophotography

In flight simulation, precise terrain representation is essential to ensure realistic landing and flight conditions. X-Plane includes a standard global elevation model ("mesh") by default, whose resolution is often limited due to storage constraints. This elevation model, which is described in detail in the "Components" menu of the scenery settings, forms the basis for terrain representation. Through the use of specific add-ons, both the precision of the mesh and the quality of the projected ground textures can be significantly improved. The primary goal is to increase topographic accuracy, with the visual optimization of the scenery resulting as a secondary benefit.

## Methods for Integrating Orthophotos

Two fundamentally different approaches have been established for integrating orthophotos into X-Plane:

### Static Generation

With this approach, orthophoto tiles are fully downloaded before the flight, converted to DDS textures, and permanently stored on the local hard drive. X-Plane reads these tiles like regular scenery data — no internet connection is required at runtime. The data must be managed manually and grows with each generated region.

- **[Ortho4XP](ortho4xp.md)**: The established tool for static generation of orthophoto scenery. Ortho4XP creates both textures and an elevation model (mesh) for defined geographic sections ("tiles") based on publicly available remote sensing data (e.g., SRTM elevation data or high-resolution LIDAR data). Supports zoom levels up to ZL19 for maximum detail.

### Ortho Streaming

With this approach, orthophoto textures are downloaded on demand from map servers at runtime and delivered to X-Plane via a virtual file system (FUSE). Once loaded, tiles are stored in a local cache; when the configured limit is reached, older tiles are automatically removed. This approach requires a stable internet connection but enables spontaneous flying without pre-generation.

- **[AutoOrtho](autoortho.md)**: The first and most widely used streaming solution for X-Plane. The active [ProgrammingDinosaur Fork](https://github.com/ProgrammingDinosaur/autoortho4xplane) (version 2.0) offers a C pipeline for faster loading, a modern GUI, and supports Windows, Linux, and macOS.

- **[XEarthLayer](xearthlayer.md)**: A Rust-based alternative with adaptive prefetching that switches between ground-level ring prefetch and cruise-mode track prediction. Currently only available for Linux and X-Plane 12.

- **[X-Plane Map Enhancement](https://github.com/derekhe/xplane-map-enhancement-release)** (XPME): A streaming solution with its own user interface that projects satellite imagery directly onto the terrain. Available for Windows, macOS, and Linux (.deb and AppImage).

### Placement in scenery_packs.ini

All three streaming solutions share a common requirement: their entries belong at the **very bottom** of the `scenery_packs.ini`.

The reason lies in X-Plane's priority logic. Entries higher up in the file have higher priority and are loaded first. Local scenery — whether custom airports, SimHeaven autogen, or local Ortho4XP tiles — sits higher in the file and is therefore always used first. Only when no local scenery exists for a particular area does X-Plane fall through to the streaming entries further down and load satellite imagery from the internet.

This fallback principle has a key advantage: local tiles that were painstakingly generated at high resolution are never overwritten by streamed images. At the same time, worldwide coverage is provided for all areas where no local data exists.

The following example shows a typical `scenery_packs.ini` using AutoOrtho for Europe:

```ini
# Custom Airports and Landmarks
SCENERY_PACK Custom Scenery/Aerosoft_EDDF_Frankfurt_3_Scenery/
SCENERY_PACK Custom Scenery/X-Plane Landmarks - Paris/

# Standard Airports
SCENERY_PACK *GLOBAL_AIRPORTS*

# Autogen (SimHeaven X-World)
SCENERY_PACK Custom Scenery/simHeaven_X-World_Europe-6-scenery/
SCENERY_PACK Custom Scenery/simHeaven_X-World_Europe-7-forests/

# Local Ortho4XP tiles (optional)
SCENERY_PACK Custom Scenery/zOrtho4XP_+48+011/
SCENERY_PACK Custom Scenery/zOrtho4XP_+47+011/

# Mesh files
SCENERY_PACK Custom Scenery/SFD_EDDM_Munich_2_Mesh/

# Ortho Streaming (at the very bottom — fallback for missing local data)
SCENERY_PACK Custom Scenery/yAutoOrtho_Overlays/
SCENERY_PACK Custom Scenery/z_ao_eur/
SCENERY_PACK Custom Scenery/z_autoortho/
```

For **XEarthLayer**, regional packages are installed via the CLI (`xearthlayer packages install eu`). The entries use the `zzXEL_` prefix and are also placed at the end of the file:

```ini
# XEarthLayer Ortho Streaming (at the very bottom)
SCENERY_PACK Custom Scenery/zzXEL_eu_ortho/
```

**XPME** automatically places its entries in `scenery_packs.ini` during installation. The principle is identical: streaming entries must be at the end so that local scenery takes priority.

### Combination

For selected regions, high-resolution Ortho4XP tiles can be combined with AutoOrtho's global streaming coverage. This procedure is described in detail in the [AutoOrtho + Ortho4XP](static_plus_streaming.md) chapter.

## Which System Suits Which Player Profile?

Choosing the right system largely depends on your individual flying behavior:

- **Regular flyer** (recurring home airports and routes): **Static generation** offers the greatest advantage here. After a one-time generation of home regions, all textures are stored locally. Maximum quality without internet dependency and no latency fluctuations.

- **Explorative player** (constantly changing destinations): **Streaming solutions** are the better choice. They eliminate time-consuming pre-generation and allow spontaneous flights to any region worldwide. Storage consumption remains stable through automatic cache eviction.

- **Hybrid player** (home airports + occasional exploration): The **[combination of static generation and streaming](static_plus_streaming.md)** offers the best of both worlds. Local tiles for home regions in highest quality, streaming for flexible global coverage.
