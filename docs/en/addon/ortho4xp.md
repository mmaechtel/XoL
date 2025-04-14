# Ortho4XP

Ortho4XP is a powerful tool for creating orthophotos for X-Plane. It enables the generation of high-resolution ground textures from satellite imagery and elevation data.

## Installation and Versions

Ortho4XP is available in two main versions:

1. **Original version** by Oscar Pilote:
    * [GitHub Repository](https://github.com/oscarpilote/Ortho4XP)
    * The original version with basic features
    * [Binaries available](https://github.com/kubilus1/autoortho/releases/tag/0.7.2)

2. **Fork by shred86** (recommended):
    * [GitHub Repository](https://github.com/shred86/Ortho4XP)
    * [Detailed Documentation](https://github.com/shred86/Ortho4XP/wiki)
    * Contains numerous improvements and new features
    * [Binaries for various operating systems](https://github.com/shred86/Ortho4XP/wiki/Installation)

### Installation Methods

1. **With Binaries (recommended)**:
    - Download the appropriate version for your operating system
    - Extract the archive
    - Run the executable file

2. **Manual Installation**:
    - Download your preferred version
    - Make sure Python 3.x is installed
    - Install the required Python packages:
     ```bash
     pip install -r requirements.txt
     ```

3. **Alternative Installation for Linux**:
    - Installation with Docker (see [Docker documentation](../docker.md))
    - Installation with pyenv (see [pyenv documentation](../pyenv.md))

## Usage and Configuration

### Basic Usage

1. Start Ortho4XP using the Python file or executable:
   ```bash
   python Ortho4XP.py
   ```

2. In the main window, select:
   - The target area (Tile)
   - The desired zoom level (ZL)
   - The image source (e.g., Bing, Google, Here)

3. Click "Build" to start the process

### Important Parameters

| Parameter | Default Value | Description |
|-----------|--------------|-------------|
| `custom_build_dir` | `Tiles` | Directory for generated tiles |
| `custom_overlay_src` | `Global Scenery` | Source for overlay data |
| `custom_overlay_dir` | `yOrtho4XP_Overlays` | Target directory for overlays |
| `custom_scenery_dir` | `Custom Scenery` | Target directory for finished tiles |
| `provider` | `BI` | Image source (BI=Bing, GO2=Google, ES=ESRI) |
| `zoomlevel` | `16` | Zoom level of satellite images |
| `curvature_tol` | `3.0` | Tolerance for terrain curvature |
| `mesh_zl` | `16` | Zoom level for mesh generation |
| `mask_zl` | `16` | Zoom level for water masks |
| `water_smoothing` | `3` | Smoothing of water transitions |
| `road_banking_limit` | `0.3` | Maximum road banking |
| `apt_smoothing_pix` | `8` | Smoothing parameter for airports |

### Recommended Settings

#### Standard Settings (good balance)

* `zoomlevel`: 16
* `curvature_tol`: 3.0
* `mesh_zl`: 16
* `mask_zl`: 16
* `water_smoothing`: 3

#### High-Resolution Settings

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

## LiDAR Data Integration

Ortho4XP supports the integration of high-resolution LiDAR data for improved terrain representation. This data is particularly useful for areas with complex topography such as the Alps or other mountain regions.

### Available LiDAR Data

The LiDAR data from [sonny.4lima.de](https://sonny.4lima.de) provides high resolution and accuracy for various regions. This data can be integrated into Ortho4XP in two ways:

**Method 1: Individual Tiles**
- Use the LiDAR data as `custom_dem` in Ortho4XP
- This method is suitable for individual tiles or small areas
- The LiDAR data is only used for specific tiles

**Method 2: Larger Areas**
- Replace the DEM files in the Ortho4XP directory
- This method is suitable for larger regions
- Ortho4XP automatically uses the LiDAR data for all tiles in the region

### Integration Steps

1. Download the desired LiDAR data from [sonny.4lima.de](https://sonny.4lima.de)
2. Extract the files to the Ortho4XP directory
3. Choose the desired integration method (Method 1 or 2)
4. Generate the tiles as usual

The improved terrain representation will be automatically adopted in the generated tiles.

!!! note "Note"
    The LiDAR data is particularly useful for areas with complex topography such as the Alps or other mountain regions. It provides significantly higher resolution and accuracy than the default DEM data.

## Important Notes and Troubleshooting

### General Notes

- Ortho4XP requires significant storage space for generated textures
- The quality of orthophotos depends on the chosen image source
- Processing can take several hours depending on area size and zoom level
- The shred86 fork offers better performance and more features
- Using binaries significantly simplifies the installation process

### Performance Optimization

- Processing time depends heavily on the chosen zoom level and area size
- Too high zoom levels can overload the system
- Skip parameters are useful for reprocessing individual steps
- Using an SSD can significantly reduce processing time

### Troubleshooting

If you encounter issues:
1. Check the log files in the Ortho4XP directory
2. Ensure all Python dependencies are installed
3. Consult the [shred86 fork documentation](https://github.com/shred86/Ortho4XP/wiki)
4. Visit the [X-Plane Forum](https://forums.x-plane.org/index.php?/forums/forum/310-ortho4xp/) 