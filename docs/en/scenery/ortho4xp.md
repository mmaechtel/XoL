# Ortho4XP

Ortho4XP is a powerful tool for creating orthophotos for X-Plane. It enables the generation of high-resolution ground textures from satellite imagery and elevation data.

## Installation and Versions

Ortho4XP is available in two main versions:

1. **Original version** by Oscar Pilote:
    * [GitHub Repository](https://github.com/oscarpilote/Ortho4XP)
    * The original version with basic features


2. **shred86's fork** (recommended):
    * [GitHub Repository](https://github.com/shred86/Ortho4XP)
    * [Detailed documentation](https://github.com/shred86/Ortho4XP/wiki)
    * Contains numerous improvements and new features
    * [Binaries for various operating systems](https://github.com/shred86/Ortho4XP/wiki/Installation)

### Installation Methods

1. **Using Binaries (recommended)**:
    - Download the appropriate version for your operating system
    - Extract the archive
    - Run the executable file

2. **Manual Installation**:
    - Download the desired version
    - Ensure Python 3.x is installed
    - Install required Python packages:
        ```bash
        pip install -r requirements.txt
        ```

3. **Alternative Installation for Linux**:
    - Installation with Docker (see [Docker Documentation](../extensions/docker.md))
    - Installation with pyenv (see [pyenv Documentation](../extensions/pyenv.md))

## Usage and Configuration

### Basic Usage

1. Start Ortho4XP via the Python file or executable:
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
|-----------|--------------|--------------|
| `custom_build_dir` | `Tiles` | Directory for generated tiles |
| `custom_overlay_src` | `Global Scenery` | Source for overlay data |
| `custom_overlay_dir` | `yOrtho4XP_Overlays` | Target directory for overlays |
| `custom_scenery_dir` | `Custom Scenery` | Target directory for finished tiles |
| `provider` | `BI` | Image source (BI=Bing, GO2=Google, ES=ESRI) |
| `zoomlevel` | `16` | Zoom level of satellite images |
| `curvature_tol` | `3.0` | Terrain curvature tolerance |
| `mesh_zl` | `16` | Zoom level for mesh generation |
| `mask_zl` | `16` | Zoom level for water masks |
| `water_smoothing` | `3` | Water transition smoothing |
| `road_banking_limit` | `0.3` | Maximum road banking |
| `apt_smoothing_pix` | `8` | Airport smoothing parameter |
| `road_level` | `2` | Which types of roads should be displayed |
| `min_area` | `0.001` | minimum size of water areas |

### Recommended Settings

#### Standard Settings (good balance)

* `zoomlevel`: 17
* `curvature_tol`: 2.0
* `mesh_zl`: 18
* `mask_zl`: 15
* `cover_zl`: 17
* `min_area`: 0.01
* `apt_smoothing_pix`: 16

#### High-Resolution Settings

* `zoomlevel`: 18
* `curvature_tol`: 1.3
* `mesh_zl`: 19
* `mask_zl`: 16
* `cover_zl`: 18
* `min_area`: 0.001
* `apt_smoothing_pix`: 8

#### Performance-Optimized Settings

* `zoomlevel`: 16
* `curvature_tol`: 3.0
* `mesh_zl`: 16
* `mask_zl`: 14
* `cover_zl`: 16
* `min_area`: 0.1
* `apt_smoothing_pix`: 32

## LiDAR Data Integration

Ortho4XP supports the integration of high-resolution LiDAR data for improved terrain representation. These data are particularly useful for areas with complex topography such as the Alps or other mountain regions.

### Available LiDAR Data

The LiDAR data from [sonny.4lima.de](https://sonny.4lima.de) offers high resolution and accuracy for various regions. These data can be integrated into Ortho4XP in two ways:

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
2. For Method 2, there are two options:

    - Extract the files into the Ortho4XP directory and sort the tiles into the appropriate directories under Elevation_data. Scripts like [this one](https://forum.aerosoft.com/index.php?/topic/175397-h%C3%B6hendaten-f%C3%BCr-ortho4xp/#findComment-1102723) can help
    - Or work with links under `Elevation_data`:
        - First, back up the old `Elevation_data`
        - Create a new `Elevation_data` and create directories like `+00-060` etc. in it as links to an extra directory (e.g., `GlobalElevationData`). The following script creates all necessary directories in the empty new `Elevation_data` as links to the directory `../GlobalElevationData`:
        ```bash
        #!/bin/bash

        # Target path for symbolic links
        TARGET_PATH="../GlobalElevationData"

        # Create target directory if it doesn't exist
        mkdir -p "$TARGET_PATH"

        # Function to create a link name
        create_link_name() {
            local lat=$1
            local lon=$2
            # Format latitude (+XX or -XX)
            if [ $lat -ge 0 ]; then
                lat_str=$(printf "+%02d" $lat)
            else
                lat_str=$(printf "%03d" $lat)
            fi
            # Format longitude (+YYY or -YYY)
            if [ $lon -ge 0 ]; then
                lon_str=$(printf "+%03d" $lon)
            else
                lon_str=$(printf "%04d" $lon)
            fi
            echo "${lat_str}${lon_str}"
        }

        # Generate all possible links
        for lat in $(seq -80 10 80); do    # Latitudes: -80° to +80° in 10° steps
            for lon in $(seq -180 10 180); do # Longitudes: -180° to +180° in 10° steps
                link_name=$(create_link_name $lat $lon)
                ln -s "$TARGET_PATH" "./$link_name"
            done
        done
        ```
        - Then copy all HGT files into the `GlobalElevationData` directory
3. Choose the desired integration method (Method 1 or 2)
4. Generate tiles as usual

The improved terrain representation is automatically incorporated into the generated tiles.

!!! note "Note"
    The LiDAR data is particularly useful for areas with complex topography such as the Alps or other mountain regions. It provides significantly higher resolution and accuracy than the standard DEM data.

## Ortho Patches for Sceneries

Many sceneries—both default and third-party—were originally designed for X-Plane's old, flat mesh model. In the `apt.dat` file, the flag `flatten 1` may be set. This flag causes the scenery itself, and often a larger surrounding area, to be rendered completely flat. This is counterproductive to the goal of creating a highly accurate and realistic ground mesh with Ortho4XP.

For some sceneries, special Ortho patches exist, provided either by the developer or by active X-Plane users. With these patches, the mesh model generated by Ortho4XP can be specifically adapted to the respective scenery. Additionally, modifications to the scenery may allow it to work correctly without using `flatten 1`.

If no such modifications or patches are available, manually removing the line with `flatten 1` from the relevant `apt.dat` file can often help adapt the scenery to the new, detailed ground model. However, minor artifacts may occur, such as objects not sitting exactly on the ground, occasionally floating slightly above or being partially sunk into the terrain.

## Important Notes and Troubleshooting

### General Notes

- Ortho4XP requires significant storage space for generated textures
- The quality of orthophotos depends on the chosen image source
- Processing may take several hours depending on area size and zoom level
- The shred86 fork offers better performance and more features
- Using the binaries significantly simplifies installation

### Performance Optimization

- Processing time heavily depends on the chosen zoom level and area size
- Too high zoom levels can overload the system
- Skip parameters are useful for reprocessing individual steps
- Using an SSD can significantly reduce processing time

### File Size Optimization

As Ortho4XP generates large amounts of textures, storage requirements can quickly increase. Various tools are available to optimize the file size of orthophotos:

#### Windows 11
[`texconv`](https://github.com/Microsoft/DirectXTex/wiki/Texconv) (DirectXTex, Microsoft) enables texture scaling to 2048x2048 pixels with the command `texconv.exe *.* -w 2048 -h 2048 -y`. The tool is registry-free and particularly suitable for batch processing.

#### macOS and Linux
ImageMagick provides a cross-platform solution. After installation (`brew install imagemagick` for macOS, `sudo apt-get install imagemagick` for Linux), DDS files can be scaled with `mogrify -resize 2048x2048 *.dds`.

These tools efficiently reduce file size while maintaining visual quality. The optimized size of 2048x2048 pixels offers a good compromise between quality and storage requirements.

### Troubleshooting

In case of problems:

1. Check the log files in the Ortho4XP directory
2. Ensure all Python dependencies are installed
3. Consult the [shred86 fork documentation](https://github.com/shred86/Ortho4XP/wiki)
4. Visit the [X-Plane Forum](https://forums.x-plane.org/index.php?/forums/forum/310-ortho4xp/) 