# Ortho4XP

Ortho4XP is a powerful tool for creating orthophotos for X-Plane. It enables the generation of high-resolution ground textures from satellite imagery and elevation data.

## Sources

Ortho4XP is available in two main versions:

1. **Original version** by Oscar Pilote:
    * [GitHub Repository](https://github.com/oscarpilote/Ortho4XP)
    * The original version with basic features
    * [Binaries available](https://github.com/kubilus1/autoortho/releases/tag/0.7.2)

2. **Fork by shred86**:
    * [GitHub Repository](https://github.com/shred86/Ortho4XP)
    * [Detailed Documentation](https://github.com/shred86/Ortho4XP/wiki)
    * Contains numerous improvements and new features
    * [Binaries for various operating systems](https://github.com/shred86/Ortho4XP/wiki/Installation)

## Installation

Ortho4XP can be installed in two ways:

### Installation with Binaries (recommended)

1. Download the appropriate version for your operating system:
    * Original version: [Releases](https://github.com/kubilus1/autoortho/releases/tag/0.7.2)
    * shred86 fork: [Installation page](https://github.com/shred86/Ortho4XP/wiki/Installation)
2. Extract the archive
3. Run the executable file

### Manual Installation

1. Download your preferred version of Ortho4XP
2. Make sure Python 3.x is installed
3. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

### Alternative Installation for Linux

For Linux users, two alternative installation methods are available:
* Installation with Docker (see [Docker documentation](../docker.md))
* Installation with pyenv (see [pyenv documentation](../pyenv.md))

## Basic Usage

1. Start Ortho4XP using the Python file or executable:
    ```bash
    python Ortho4XP.py
    ```

2. In the main window, select:
    * The target area (Tile)
    * The desired zoom level (ZL)
    * The image source (e.g., Bing, Google, Here)

3. Click "Build" to start the process

## Features of the shred86 Fork

The shred86 fork offers numerous improvements over the original version:

### New Features

* Improved user interface with Dark Mode
* Extended configuration options
* Support for more image sources
* Improved error handling and logging
* Automatic updates

### Technical Improvements

* Optimized memory usage
* Faster processing
* Better error tolerance
* Extended compatibility with various systems

### Additional Features

* Batch processing of multiple tiles
* Extended mesh options
* Improved water masks
* Support for more elevation data sources
* Extended configuration files

## Important Notes

* Ortho4XP requires significant storage space for generated textures
* The quality of orthophotos depends on the chosen image source
* Processing can take several hours depending on area size and zoom level
* The shred86 fork offers better performance and more features
* Using binaries significantly simplifies the installation process
* For Linux users, Docker and pyenv provide flexible alternatives to direct installation

## Troubleshooting

If you encounter issues:
1. Check the log files in the Ortho4XP directory
2. Ensure all Python dependencies are installed
3. Consult the [shred86 fork documentation](https://github.com/shred86/Ortho4XP/wiki) for detailed guides
4. Visit the [X-Plane Forum](https://forums.x-plane.org/index.php?/forums/forum/310-ortho4xp/) for additional help

## Detailed Parameter Explanation

Ortho4XP offers a wide range of parameters that influence the quality and appearance of the generated orthophotos. Here is a detailed overview of the most important parameters:

### General Parameters

| Parameter | Default Value | Description |
|-----------|--------------|-------------|
| `custom_build_dir` | `Tiles` | Directory for generated tiles |
| `custom_overlay_src` | `Global Scenery` | Source for overlay data |
| `custom_overlay_dir` | `yOrtho4XP_Overlays` | Target directory for overlays |
| `custom_scenery_dir` | `Custom Scenery` | Target directory for finished tiles |

### Image Sources and Quality

| Parameter | Default Value | Description |
|-----------|--------------|-------------|
| `provider` | `BI` | Image source (BI=Bing, GO2=Google, ES=ESRI, etc.) |
| `zoomlevel` | `16` | Zoom level of satellite images (higher = more detailed) |
| `max_convert_slots` | `4` | Maximum number of parallel conversions |
| `max_download_slots` | `4` | Maximum number of parallel downloads |
| `use_decal_on_terrain` | `True` | Use decals on terrain |
| `terrain_casts_shadows` | `True` | Terrain casts shadows |

### Mesh Generation

| Parameter | Default Value | Description |
|-----------|--------------|-------------|
| `curvature_tol` | `3.0` | Tolerance for terrain curvature (lower = more detailed) |
| `min_area` | `0.1` | Minimum area for mesh triangulation |
| `max_area` | `0.5` | Maximum area for mesh triangulation |
| `mesh_zl` | `16` | Zoom level for mesh generation |
| `road_banking_limit` | `0.3` | Maximum road banking |
| `apt_smoothing_pix` | `8` | Smoothing parameter for airports |

### Water and Coastlines

| Parameter | Default Value | Description |
|-----------|--------------|-------------|
| `water_simplification` | `0.0` | Simplification of water bodies |
| `use_masks_for_inland` | `True` | Use masks for inland water |
| `distance_masks_too` | `True` | Consider coastline distances |
| `mask_zl` | `16` | Zoom level for water masks |
| `water_smoothing` | `3` | Smoothing of water transitions |

### Elevation Data

| Parameter | Default Value | Description |
|-----------|--------------|-------------|
| `custom_dem` | `None` | Custom elevation data source |
| `dem_source` | `ViewFinderPanorama` | Default elevation data source |
| `dem_resolution` | `1` | Resolution of elevation data in arcseconds |
| `use_experimental_water` | `False` | Experimental water representation |

### Performance Optimization

| Parameter | Default Value | Description |
|-----------|--------------|-------------|
| `skip_downloads` | `False` | Skip downloads (only with existing images) |
| `skip_converts` | `False` | Skip conversion |
| `skip_masks` | `False` | Skip mask creation |
| `skip_mesh` | `False` | Skip mesh generation |
| `skip_overlays` | `False` | Skip overlay creation |

### Advanced Options

| Parameter | Default Value | Description |
|-----------|--------------|-------------|
| `clean_bad_geometries` | `True` | Clean up bad geometries |
| `clean_bad_intersections` | `True` | Clean up bad intersections |
| `clean_bad_islands` | `True` | Clean up bad islands |
| `use_decal_on_terrain` | `True` | Use decals on terrain |
| `terrain_casts_shadows` | `True` | Terrain casts shadows |

### Recommended Settings for Different Use Cases

#### Standard Settings (good balance between quality and performance)
* `zoomlevel`: 16
* `curvature_tol`: 3.0
* `mesh_zl`: 16
* `mask_zl`: 16
* `water_smoothing`: 3

#### High-Resolution Settings (maximum quality)
* `zoomlevel`: 17
* `curvature_tol`: 2.0
* `mesh_zl`: 17
* `mask_zl`: 17
* `water_smoothing`: 5

#### Performance-Optimized Settings
* `zoomlevel`: 15
* `curvature_tol`: 4.0
* `mesh_zl`: 15
* `mask_zl`: 15
* `water_smoothing`: 2

### Important Notes About Parameters

1. **Zoom Level**: 
    * Higher values mean more detail but also larger files and longer processing time
    * Zoom level 16 is sufficient for most use cases
    * Zoom level 17+ requires significantly more storage space and processing time

2. **Mesh Parameters**:
    * `curvature_tol` affects terrain detail accuracy
    * Lower values create more detailed but also more complex meshes
    * Values below 2.0 can lead to performance issues

3. **Water Parameters**:
    * `water_smoothing` affects water transition quality
    * Higher values create smoother transitions but may lose detail
    * `mask_zl` should match `zoomlevel` for optimal results

4. **Performance Parameters**:
    * `max_convert_slots` and `max_download_slots` should be adjusted to CPU performance
    * Too high values can overload the system
    * Skip parameters are useful for reprocessing individual steps 