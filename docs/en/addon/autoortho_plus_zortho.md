# AutoOrtho + zOrtho4XP

!!! info "Work in Progress"
    This documentation is in the development phase and is not complete. The described methods and settings are continuously evaluated and updated.

The integration of **AutoOrtho** with **Ortho4XP** provides an optimal solution for **X-Plane** users who want to benefit from both real-time streaming and high-quality local orthophotos. This guide explains the effective implementation of both systems.

The combination is based on a **hybrid approach** where **AutoOrtho** is used for global coverage and **zOrtho4XP** for selected high-quality regions. This enables quick availability of orthophotos worldwide, highest quality in preferred flight areas, optimized storage usage, and flexibility in image source selection.

### Setup

The implementation is done in two main steps. First, the **Ortho4XP tiles** are generated for the preferred flight areas. Here, **zoom levels** 17-19 are recommended for maximum quality, with **overlays** to be activated unless [**SimHeaven**](../scenery.md) is used. As image source, you can choose between **Bing** and **Google**.

The correct structure of the `scenery_packs.ini` is essential for the interoperability of both systems:

```
SCENERY_PACK Custom Scenery/yAutoOrtho_Overlays/
SCENERY_PACK Custom Scenery/zOrtho4XP_+47+011/
SCENERY_PACK Custom Scenery/zOrtho4XP_+48+011/
SCENERY_PACK Custom Scenery/z_ao_eur/
SCENERY_PACK Custom Scenery/z_autoortho/
```

### Optimal Usage

Efficient usage requires precise **prioritization** of regions. For frequently visited airports, **zOrtho4XP tiles** with **ZL**17-19 in a 50km radius are recommended. Main flight routes benefit from tiles with **ZL**16-17, which are implemented as corridors along the route. For all other areas, **AutoOrtho** provides coverage with **ZL**16 as standard.

A successful integration requires systematic planning, regular maintenance, and continuous optimization. The identification of main flight areas and planning of **zOrtho4XP coverage** considering available storage space is crucial. Maintenance includes regular **cache cleanup**, validation of the `scenery_packs.ini`, and updating both systems. Optimization is achieved through adjustment of **zoom levels**, balancing quality and performance, and regular review of the configuration.

### Troubleshooting

The most common problems occur with overlapping **tiles** when multiple **ortho sources** are present for the same region. This can be resolved by precise **prioritization** in the `scenery_packs.ini`. Performance issues often result from an excessive number of high-resolution **tiles** and can be optimized by reducing **zOrtho4XP coverage** or with alternative **settings** when generating the tiles.

## New Meshes for AutoOrtho

**zOrtho4XP** can be used not only for high-quality **orthophotos** but also as a **mesh generator** for **AutoOrtho**. This enables improved **terrain representation** in combination with **AutoOrtho textures**.

### Benefits

The implementation of **zOrtho4XP** as a **mesh generator** offers the following advantages for **AutoOrtho**:

- Increased resolution of **terrain representation**
- More precise representation of **topographic features**
- Improved **topographic representation** through **Ortho Patches**

### Recommended Ortho4XP Settings

For optimal results with **AutoOrtho**, the following parameters in **Ortho4XP 1.4** are essential:

| Parameter                  | Recommended Value | Description |
|---------------------------|------------------|--------------|
| `skip_downloads`          | Enabled          | Disables image download |
| `skip_converts`           | Enabled          | Disables DDS rendering |

The remaining parameters are detailed in the [**Ortho4XP chapter**](ortho4xp.md).

### Setup

The implementation is done in three main steps:

1. **Mesh Generation**:
    - Initialize **zOrtho4XP**
    - Select the desired region
    - Enable the "**Build Mesh**" option
    - Disable "**Build Overlays**" and "**Build Imagery**"
    - Configure the **mesh level** to 1-2 for more detailed terrain
    - Disable image downloads (`skip_downloads` enabled)

2. **Directory Structure**:
    - **Ortho4XP** generates three directories per tile (e.g., `zOrtho4XP_+51+00`):
        - `Earth Nav Data`
        - `terrain`
        - `textures`
    - Separate integration of these directories into the **AutoOrtho configuration directory** and the `scenery_packs.ini` would significantly increase initialization time, as **AutoOrtho** mounts each directory at startup.
    - Therefore, the contents of these three directories per tile are consolidated into a single directory (e.g., `aa_zortho4xp_meshes`).
    - In case of name conflicts during the copy process, files can be safely overwritten as they are identical **masks**.
    - The new directory should start with `aa_` (e.g., `aa_zortho4xp_meshes`) to ensure correct reading order.
    - Store the consolidated directory under `z_autoortho/scenery`:
       ```
       Custom Scenery/z_autoortho/scenery/aa_zortho4xp_meshes/
       ```
    - The structure thus matches the existing `ao_` directories

3. **scenery_packs.ini Configuration**:
   ```
   SCENERY_PACK Custom Scenery/yAutoOrtho_Overlays/
   SCENERY_PACK Custom Scenery/z_autoortho/scenery/aa_zortho4xp_meshes/
   SCENERY_PACK Custom Scenery/z_ao_eur/
   SCENERY_PACK Custom Scenery/z_autoortho/
   ```
   **Important**: The `aa_` directory must be placed before the `ao_` directories to ensure correct **mesh prioritization**.

### Best Practices

Effective use of **zOrtho4XP** as a **mesh generator** requires:

- Systematic planning of **mesh levels** based on flight altitude
- Consideration of available **storage capacity**
- Regular **quality control** of **meshes**
- Demand-oriented updates
- Continuous **performance monitoring**
- Optimization of **mesh levels**
- Balanced ratio between **detail level** and performance
- Regional **prioritization**

## Increasing Mesh Resolution

As described in the [**Ortho4XP chapter**](ortho4xp.md), **LiDAR data** can be implemented to improve the resolution and accuracy of **terrain representation**. The **LiDAR data** from [sonny.4lima.de](https://sonny.4lima.de) offers high resolution and precision for various regions.

### LiDAR Integration

See chapter [**LiDAR Data Integration**](ortho4xp.md#Integration of LiDAR Data) in the **Ortho4XP section**.

## Conclusion

The integration of **AutoOrtho** and **zOrtho4XP** provides an optimal solution for **X-Plane** users who want both global coverage and highest quality in preferred regions. Through systematic planning and regular maintenance, both systems can be effectively integrated and provide an optimal flight experience. 