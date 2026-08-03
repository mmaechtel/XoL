---
description: "Combine Ortho4XP static tiles with AutoOrtho streaming in X-Plane. Setup guide for scenery_packs.ini priority, mesh-only generation, and LiDAR data."
---
# Combining Static Orthophotos with Streaming

This combination is particularly suited for **hybrid players** — users who want to enjoy their home airports in highest quality while also occasionally exploring new regions. For an overview of the different player profiles, see the [Introduction to Orthophotography](../orthophotography/orthophotography_intro.md#which-system-suits-which-player-profile).

The principle is simple: **Ortho4XP** generates high-resolution, local tiles (up to ZL19) for preferred flight areas, while a **streaming solution** (e.g., AutoOrtho) handles global coverage for all other regions. X-Plane's scenery prioritization ensures that local Ortho4XP tiles automatically take precedence over streamed textures.

The benefits of this combination:

- **Home regions** in maximum resolution without internet dependency
- **Spontaneous flying** anywhere in the world without pre-generation
- **Optimized storage usage** — local storage is only used for the most important regions

## Setup

### 1. Generate Ortho4XP tiles

First, generate Ortho4XP tiles for your preferred flight areas. Recommended settings:

- **Zoom level 17–19** for maximum quality
- **Enable overlays** unless [SimHeaven](../aufbau_quellen/scenery_sources.md) is used
- Image sources include **Bing** and **Google**

### 2. Configure scenery_packs.ini

The correct order in the `scenery_packs.ini` is crucial — Ortho4XP tiles must be listed **before** the streaming entries so they take priority. The following example shows the configuration using AutoOrtho (for other streaming solutions, adjust the directory names accordingly):

```
SCENERY_PACK Custom Scenery/yAutoOrtho_Overlays/
SCENERY_PACK Custom Scenery/zOrtho4XP_+47+011/
SCENERY_PACK Custom Scenery/zOrtho4XP_+48+011/
SCENERY_PACK Custom Scenery/z_ao_eur/
SCENERY_PACK Custom Scenery/z_autoortho/
```

## Recommended Coverage Strategy

| Area | Ortho source | Zoom level | Note |
|---|---|---|---|
| Home airports (50 km radius) | Ortho4XP | ZL17–19 | Maximum quality for approach and surroundings |
| Main flight routes | Ortho4XP | ZL16–17 | Corridors along the route |
| All other areas | Streaming | ZL16 (default) | Automatic, no preparation needed |

## Troubleshooting

**Overlapping tiles**: When multiple ortho sources exist for the same region, the order in the `scenery_packs.ini` determines priority. Ortho4XP entries should always be listed before streaming entries.

**Performance issues**: Too many high-resolution Ortho4XP tiles can increase loading times. In this case, reduce coverage to the most important regions or use lower zoom levels.

## Using Ortho4XP Meshes with Streaming

Ortho4XP can generate not only textures but also **meshes** — more precise elevation models. These meshes can be combined with streamed textures to achieve better terrain representation without having to store local texture data.

!!! note "Examples shown using AutoOrtho"
    The following directory structures and `scenery_packs.ini` entries refer to AutoOrtho. The principle is identical for other streaming solutions — adjust directory names accordingly.

### Benefits

- Higher resolution terrain representation
- More precise topographic features (mountains, valleys, coastlines)
- Improved airport topography through Ortho Patches

### Ortho4XP Settings for Mesh-Only Generation

To generate meshes only without textures, set the following parameters in Ortho4XP:

| Parameter | Value | Description |
|---|---|---|
| `skip_downloads` | Enabled | Skips image download |
| `skip_converts` | Enabled | Skips DDS rendering |
| Build Mesh | Enabled | Generates the elevation model |
| Build Overlays | Disabled | No overlays needed |
| Build Imagery | Disabled | No textures needed |
| Mesh level | 1–2 | Higher value = more detailed terrain |

The remaining parameters are detailed in the [Ortho4XP chapter](../orthophotography/ortho4xp.md#important-parameters); the settings specific to mesh-only builds are covered under [Building Packages for Ortho Streaming](../orthophotography/ortho4xp.md#building-packages-for-ortho-streaming).

### Directory Structure

Ortho4XP generates three directories per tile (e.g., `zOrtho4XP_+51+00`): `Earth Nav Data`, `terrain`, and `textures`. Since AutoOrtho mounts each directory individually at startup, adding them separately would increase initialization time.

Therefore, the contents of all tiles are consolidated into a single directory:

```
Custom Scenery/z_autoortho/scenery/aa_zortho4xp_meshes/
```

- The `aa_` prefix ensures the directory is read before the `ao_` directories
- Name conflicts during copying can be safely overwritten (identical masks)

The `scenery_packs.ini` is adjusted accordingly:

```
SCENERY_PACK Custom Scenery/yAutoOrtho_Overlays/
SCENERY_PACK Custom Scenery/z_autoortho/scenery/aa_zortho4xp_meshes/
SCENERY_PACK Custom Scenery/z_ao_eur/
SCENERY_PACK Custom Scenery/z_autoortho/
```

The `aa_` directory must be listed **before** the `ao_` directories so that Ortho4XP meshes take priority.

## Increasing Mesh Resolution with LiDAR Data

As described in the [Ortho4XP chapter](../orthophotography/ortho4xp.md), LiDAR data can further improve the resolution and accuracy of terrain representation. The LiDAR data from [sonny.4lima.de](https://sonny.4lima.de) offers high resolution for various regions.

See [LiDAR Data Integration](../orthophotography/ortho4xp.md#lidar-data-integration) in the Ortho4XP chapter.

## Conclusion

The combination of static generation and streaming provides a flexible solution for X-Plane users who want both highest quality in preferred regions and worldwide coverage. The key lies in the targeted selection of Ortho4XP regions and the correct prioritization in the `scenery_packs.ini`.

---

## Further Reading

| Topic | Page | Focus |
|---|---|---|
| AutoOrtho | [AutoOrtho](autoortho.md) | Streaming configuration and cache management |
| XEarthLayer | [XEarthLayer](xearthlayer.md) | Alternative streaming solution |
| Ortho4XP | [Ortho4XP](../orthophotography/ortho4xp.md#building-packages-for-ortho-streaming) | Parameter reference, mesh-only package builds and LiDAR integration |
| Scenery Components | [How X-Plane Builds the World](../aufbau_quellen/scenery_components.md) | scenery_packs.ini load order and priority rules |
| Filesystem | [Filesystem](../../linux/optimizations/filesystem.md) | Storage optimization for local tiles and cache |
| GPU & VRAM | [GPU & VRAM](../../fundamentals/performance/gpu_vram.md) | VRAM impact of combined ortho sources |
