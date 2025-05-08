# AutoOrtho + zOrtho4XP

!!! info "Work in Progress"
    This documentation is still under development and not complete. The described methods and settings are continuously being reviewed and updated.

The combination of AutoOrtho with zOrtho4XP offers an optimal solution for X-Plane users who want to benefit from both real-time streaming and high-quality local orthophotos. This guide explains how both systems can work together effectively.

## Basic Concept

The combination is based on a hybrid approach where AutoOrtho is used for general worldwide coverage and zOrtho4XP for selected high-quality regions. This enables quick availability of orthophotos worldwide, highest quality in preferred flight areas, optimized storage usage, and flexibility in image source selection.

## Installation and Configuration

### Prerequisites

For the successful combination of AutoOrtho and zOrtho4XP you need

- A working AutoOrtho installation
- zOrtho4XP (Version 1.4 or higher)
- Sufficient SSD storage for zOrtho4XP tiles
- Python 3.x for zOrtho4XP

### Recommended zOrtho4XP Settings

For optimal results with AutoOrtho, use the following settings in zOrtho4XP 1.4

| Parameter                  | Recommended Value | Description |
|---------------------------|------------------|--------------|
| `skip_downloads`          | Enabled          | No image download needed |
| `skip_converts`           | Enabled          | No DDS rendering needed |
| `mask_zl`                 | 16               | Optimal water transitions |
| `use_masks_for_inland`    | Enabled          | Better inland waters |
| `distance_masks_too`      | Enabled          | Clean coastlines |
| `custom_dem`              | Optional         | Higher DEMs for finer meshes |
| `curvature_tol`           | 2.0–4.0          | Affects mesh complexity |
| `road_banking_limit`      | 0.3              | Prevents build errors |
| `apt_smoothing_pix`       | 8–16             | Smoother runways |
| `water_tech`              | "XP12"           | Uses XP12 water technology |

### Setup

The setup is done in two main steps. First, create the zOrtho4XP tiles for your preferred flight areas. Choose zoom levels 17-19 for maximum quality and enable overlays. You can choose between Bing and Google as image sources.

The correct structure of scenery_packs.ini is crucial for the interaction of both systems

```
SCENERY_PACK Custom Scenery/yAutoOrtho_Overlays/
SCENERY_PACK Custom Scenery/zOrtho4XP_+47+011/
SCENERY_PACK Custom Scenery/zOrtho4XP_+48+011/
SCENERY_PACK Custom Scenery/z_ao_eur/
SCENERY_PACK Custom Scenery/z_autoortho/
```

## Optimal Usage

### Regional Prioritization

Optimal usage requires clear prioritization of regions. For frequently used airports, zOrtho4XP tiles with ZL17-19 in a 50km radius are recommended. Main flight routes benefit from tiles with ZL16-17, which are created as corridors along the route. For all other areas, AutoOrtho provides coverage with ZL16 as standard.

### Performance Optimization

Effective performance optimization is based on two main aspects: cache management and graphics settings. The AutoOrtho cache should be between 20-30 GB, while zOrtho4XP tiles are managed as needed. Regular cache cleanup is important. For graphics settings, maximum textures, high object density, and minimal reflections are recommended.

## Troubleshooting

### Common Problems

The most common problems occur with overlapping tiles when multiple ortho sources are present for the same region. This can be resolved by clear prioritization in scenery_packs.ini. Performance issues often arise from too many high-resolution tiles and can be solved by reducing zOrtho4XP coverage. Storage issues with large zOrtho4XP tiles require selective tile creation.

## Best Practices

A successful combination requires careful planning, regular maintenance, and continuous optimization. Identify your main flight areas and plan zOrtho4XP coverage considering available storage space. Maintenance includes regular cache cleanup, checking scenery_packs.ini, and updating both systems. Optimization is achieved by adjusting zoom levels, balancing quality and performance, and regular review of settings.

## New Meshes for AutoOrtho

zOrtho4XP can be used not only for high-quality orthophotos but also as a mesh generator for AutoOrtho. This enables improved terrain representation in combination with AutoOrtho textures.

### Benefits

Using zOrtho4XP as a mesh generator offers several advantages

- Higher terrain resolution
- Better representation of mountains and valleys
- More precise airport smoothing
- Optimized performance through local mesh data

### Setup

The setup is done in three main steps. First, generate the meshes with zOrtho4XP. Start zOrtho4XP, select the desired region, and enable the "Build Mesh" option. Disable "Build Overlays" and "Build Imagery". Set the mesh level to 1-2 for more detailed terrain and disable image downloads (skip_downloads enabled).

In the second step, merge the directories. For each zOrtho4XP tile, three directories are created: `Earth Nav Data`, `terrain`, and `textures`. These must be merged into a new directory starting with `aa_` (e.g., `aa_zortho4xp_meshes`). Save the merged directory under

```
Custom Scenery/z_autoortho/scenery/aa_zortho4xp_meshes/
```

The structure should match the existing `ao_` directories.

The scenery_packs.ini must have the following structure

```
...
SCENERY_PACK Custom Scenery/yAutoOrtho_Overlays/
SCENERY_PACK Custom Scenery/z_autoortho/scenery/aa_zortho4xp_meshes/
SCENERY_PACK Custom Scenery/z_ao_eur/
...
SCENERY_PACK Custom Scenery/z_autoortho/
```

**Important**: The `aa_` directory must be placed directly before the `ao_` directories so that AutoOrtho searches for meshes there first.

### Best Practices

Successful use of zOrtho4XP as a mesh generator requires careful planning, regular maintenance, and continuous optimization. Identify areas with complex terrain and plan mesh levels based on flight altitude. Consider available storage space. Maintenance includes regular checking of mesh quality, updating as needed, and performance monitoring. Optimization is achieved by adjusting mesh levels, balancing detail and performance, and regional prioritization.

## Increasing Mesh Resolution

As already described in zOrtho4XP, LiDAR data can be used to improve the resolution and accuracy of the terrain. The LiDAR data from [sonny.4lima.de](https://sonny.4lima.de) offers high resolution and accuracy for various regions. This data can be integrated into zOrtho4XP in two ways:

### 2. zOrtho4XP as Mesh Generator for AutoOrtho

This method uses zOrtho4XP to create high-resolution meshes that are then used by AutoOrtho for texturing:

1. **LiDAR Data Integration**:
    - Visit [sonny.4lima.de](https://sonny.4lima.de)
    - Select the desired region
    - Download the .hgt files

2. **zOrtho4XP Configuration**:
    - Set `custom_dem` to the path of the LiDAR data
    - Enable `use_masks_for_inland`
    - Adjust `curvature_tol` (1.0-2.0 for higher resolution)
    - Higher mesh levels (3-4) for detailed terrain
    - **Important**: Disable image downloads (skip_downloads enabled)

3. **Merge Directories**:
    - For each zOrtho4XP tile, three directories are created:
        - `Earth Nav Data`
        - `terrain`
        - `textures`
    - These directories must be merged into a new directory
    - The new directory should start with `aa_` (e.g., `aa_zortho4xp_meshes`)
    - Save the merged directory under:
     ```
     Custom Scenery/z_autoortho/scenery/aa_zortho4xp_meshes/
     ```
    - The structure should match the existing `ao_` directories

4. **scenery_packs.ini Structure**:
   ```
   SCENERY_PACK Custom Scenery/yAutoOrtho_Overlays/
   SCENERY_PACK Custom Scenery/z_autoortho/scenery/aa_zortho4xp_meshes/
   SCENERY_PACK Custom Scenery/z_ao_eur/
   SCENERY_PACK Custom Scenery/z_autoortho/
   ```
   **Important**: The `aa_` directory must be placed directly before the `ao_` directories so that AutoOrtho searches for meshes there first.

5. **AutoOrtho Usage**:
    - AutoOrtho automatically uses the created meshes
    - Better terrain representation through higher resolution
    - Optimized performance through local mesh data

### Benefits of the Combination

The combination of AutoOrtho with zOrtho4XP as a mesh generator offers several advantages

- Higher terrain resolution
- Better representation of mountains and valleys
- More precise airport smoothing
- Optimized performance through local mesh data

## Conclusion

The combination of AutoOrtho and zOrtho4XP offers the best solution for X-Plane users who want both worldwide coverage and highest quality in preferred regions. With careful planning and regular maintenance, both systems can work together harmoniously and provide an optimal flight experience. 