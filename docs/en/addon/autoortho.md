# AutoOrtho

AutoOrtho is a tool for X-Plane that integrates orthophotos into the flight simulator. It enables the use of high-resolution aerial imagery as ground textures, significantly improving the visual reality in X-Plane.

## Comparison with Ortho4XP

AutoOrtho and Ortho4XP are both tools for integrating orthophotos into X-Plane, but they differ fundamentally:

### AutoOrtho

* **Streaming-based**: Loads orthophotos on demand during flight
* **No local storage**: Does not require large local storage capacity
* **Dynamic adjustment**: Automatically adjusts quality based on altitude
* **Easy installation**: Quick start without complex configuration
* **Regular updates**: Automatic updating of image data
* **Internet-dependent**: Requires a stable internet connection
* **Flexible**: Easy switching between different regions

### Ortho4XP

* **Local storage**: Creates and stores orthophotos locally
* **High quality**: Maximum control over texture quality
* **Offline usage**: No internet connection required during flight
* **Complex configuration**: More settings for advanced users
* **High storage requirements**: Requires significant disk space
* **Long generation time**: Texture creation can take hours
* **Static**: Once created, textures remain unchanged

### When to use which tool?

**AutoOrtho is ideal for:**

* Users with limited storage space
* Occasional flights in different regions
* Users who don't want complex configuration
* Users with good internet connection

**Ortho4XP is ideal for:**

* Users with sufficient storage space
* Regular flights in specific regions
* Users who want maximum control over quality
* Users without stable internet connection

## Installation and Usage

### Installation

1. Download the latest version of AutoOrtho from the [official GitHub page](https://github.com/kubilus1/autoortho)
2. Extract the archive to a folder of your choice
3. Make sure Python 3.x is installed
4. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

### Configuration

The configuration file `.autoortho` is created in your home directory and can be edited with a text editor. Here are the most important parameters that can be adjusted to your system:

```ini
# X-Plane directory
xplane_path = /path/to/xplane

# Cache directory for orthophotos
cache_dir = /path/to/cache

# Image provider (bing, google, here)
provider = bing

# Cache size in GB
cache_size = 20

# Maximum wait time for images. Higher values mean better quality but more
# stuttering. Lower values are more responsive at the cost of occasional
# lower quality.
maxwait = 1.5

# Minimum zoom level. This does not increase the maximum quality of satellite images
min_zoom = 14

# Automatic start with X-Plane
autostart = true

# Debug mode (true/false)
debug = false
```

### Important Parameter Explanations

- `xplane_path`: Path to the X-Plane main directory
- `cache_dir`: Directory for orthophoto cache (recommended: fast SSD)
- `provider`: Image source for orthophotos (bing, google, here)
- `cache_size`: Maximum cache size in GB
- `maxwait`: Maximum wait time for images in seconds. Higher values mean better quality but more stuttering. Lower values are more responsive but may occasionally result in lower quality.
- `min_zoom`: Minimum zoom level for satellite images. Affects the minimum quality of displayed images.
- `autostart`: AutoOrtho starts automatically with X-Plane
- `debug`: Enable debug information in logs

!!! warning "Autostart Function"
    :material-alert: **FIXME** - Please verify
    
    The autostart functionality of AutoOrtho needs to be verified. It is currently unclear whether the configuration in the `.autoortho` file is sufficient or if additional system services are required.

    **Note:** The following instructions are based on the assumption that the autostart function can be configured via the `.autoortho` file. This needs to be verified.

### Basic Usage

1. Start AutoOrtho using the Python file:
   ```bash
   python autoortho.py
   ```

2. In the main window, select:
    - Install Dirs
    - The image source (e.g., Bing, Google, Here)
    - The download target area

3. Click "Start" to begin the process

## Integration with Ortho4XP 1.4

AutoOrtho can be enhanced using custom Ortho4XP 1.4 tiles. This method provides greater control over the quality and appearance of orthophotos.

### Ortho4XP 1.4 Configuration

For optimal results with AutoOrtho, use the following settings in Ortho4XP 1.4:

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

### Tile Consolidation

To make the created tiles usable with AutoOrtho, they need to be consolidated in a specific format. A consolidation script can be used for this:

```bash
#!/bin/bash

# Define source and destination paths
SRC="$HOME/xplane-ortho-work/tiles_source"
DST="$HOME/xplane-ortho-work/tiles_consolidated/zOrtho4XP_RegionName"

# Prepare destination directory
rm -rf "$DST"
mkdir -p "$DST"

# Remove temporary files
find "$SRC" -type f -name "*.bak" -delete

# Copy relevant data
for TILE in "$SRC"/*; do
    if [ -d "$TILE" ]; then
        [ -d "$TILE/textures" ] && cp -r "$TILE/textures" "$DST/"
        [ -d "$TILE/terrain" ] && cp -r "$TILE/terrain" "$DST/"
        [ -d "$TILE/Earth nav data" ] && cp -r "$TILE/Earth nav data" "$DST/"
    fi
done
```

### Integration with AutoOrtho

After creating the tiles:

1. Copy the consolidated folder to:
   ```
   ~/X-Plane 12/Custom Scenery/z_autoortho/scenery/
   ```

2. Restart AutoOrtho

### Overlay Integration

For additional details, overlays can be generated:

1. Create overlays in Ortho4XP
2. Save them in a folder named `yOrtho4XP_RegionName`

### Integration of Sonny's LiDAR Data

[Sonny's LiDAR Digital Terrain Models](https://sonny.4lima.de) provide high-resolution terrain data for Europe that can significantly improve the quality of AutoOrtho. These datasets are based on precise LiDAR measurements and offer much better resolution than conventional satellite data.

#### Advantages of LiDAR Data
- Higher accuracy in forested areas
- Better representation of steep terrain
- More precise elevation information
- Optimized representation of valleys and gorges

#### Available Resolutions
- **0.5"** (only for Austria and Switzerland)
- **1"** (approx. 20-30m resolution)
- **3"** (approx. 60-90m resolution)
- **10m** (only for Austria and Switzerland)
- **20m** (20x20m resolution)
- **50m** (50x50m resolution)

#### Integration with AutoOrtho
1. Download the desired LiDAR data from [sonny.4lima.de](https://sonny.4lima.de)
2. Extract the files to the Ortho4XP directory

**Method 1: Individual Tiles**
- Use the LiDAR data as `custom_dem` in Ortho4XP
- This method is suitable for individual tiles or small areas
- The LiDAR data is only used for specific tiles

**Method 2: Larger Areas**
- Replace the DEM files in the Ortho4XP directory
- This method is suitable for larger regions
- Ortho4XP automatically uses the LiDAR data for all tiles in the region

3. Generate the tiles as usual
4. The improved terrain representation will be automatically adopted in AutoOrtho

!!! note "Note"
    The LiDAR data is available under the Creative Commons Attribution 4.0 (CC BY 4.0) license. Please observe the license terms and credit Sonny as the source.

## Important Notes and Troubleshooting

AutoOrtho runs as a background service and generates orthophotos during flight. The textures are stored in a cache to avoid repeated downloads. A stable internet connection is required for streaming orthophotos. The quality of orthophotos is automatically adjusted based on altitude.

If you encounter issues:

1. Check the log files in the AutoOrtho directory
2. Ensure all Python dependencies are installed
3. Verify your internet connection for image data downloads
4. Consult the [AutoOrtho Forum](https://forums.x-plane.org/index.php?/forums/forum/406-autoortho/) for additional help

When using [SimHeaven](https://simheaven.com/), the `yOrtho4XP` directories are not required as SimHeaven already contains all necessary overlay data.

