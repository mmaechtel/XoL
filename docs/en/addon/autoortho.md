# AutoOrtho

AutoOrtho is a tool for X-Plane that integrates orthophotos into the flight simulator. It enables the use of high-resolution aerial imagery as ground textures, significantly improving the visual reality in X-Plane.

## Differences from Ortho4XP

AutoOrtho and Ortho4XP are both tools for integrating orthophotos into X-Plane, but they differ fundamentally in their operation and application:

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

### When to Use Which Tool?

**AutoOrtho is ideal for:**

* Users with limited storage space
* Occasional flyers in various regions
* Users who don't want complex configuration
* Users with good internet connection

**Ortho4XP is ideal for:**

* Users with sufficient storage space
* Regular flights in specific regions
* Users who want maximum control over quality
* Users without stable internet connection

## Installation

1. Download the latest version of AutoOrtho from the [official GitHub page](https://github.com/kubilus1/autoortho)
2. Extract the archive to a folder of your choice
3. Make sure Python 3.x is installed
4. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Basic Usage

1. Start AutoOrtho using the Python file:
   ```bash
   python autoortho.py
   ```

2. In the main window, select:
   - Install Dirs
   - The image source (e.g., Bing, Google, Here)
   - The download target area

3. Click "Start" to begin the process

## Configuration

The configuration file `.autoortho` is created in your home directory and can be edited with a text editor. Here are the most important parameters that can be adjusted according to your system:

```ini
# X-Plane directory
xplane_path = /path/to/xplane

# Cache directory for orthophotos
cache_dir = /path/to/cache

# Image provider (bing, google, here)
provider = bing

# Cache size in GB
cache_size = 20

# max time to wait for images.  higher numbers mean better quality, but more
# stutters.  lower numbers will be more responsive at the expense of
# ocassional low quality tiles.
maxwait = 1.5

# minimum zoom level to allow.  this will not increase the max quality of satellite imagery
min_zoom = 14

# Autostart with X-Plane
autostart = true

# Debug mode (true/false)
debug = false
```

### Important Parameter Explanations

- `xplane_path`: Path to the X-Plane main directory
- `cache_dir`: Directory for orthophoto cache (recommended: fast SSD)
- `provider`: Image source for orthophotos (bing, google, here)
- `cache_size`: Maximum cache size in GB
- `maxwait`: Maximum wait time for images in seconds. Higher values mean better quality but more stuttering. Lower values are more responsive but may occasionally result in lower quality tiles.
- `min_zoom`: Minimum zoom level for satellite imagery. Affects the minimum quality of displayed images.
- `autostart`: Start AutoOrtho automatically with X-Plane
- `debug`: Enable debug information in logs

## Important Notes

- AutoOrtho runs as a background service and generates orthophotos during flight
- Textures are stored in a cache to avoid repeated downloads
- A stable internet connection is required for streaming orthophotos
- The quality of orthophotos is automatically adjusted based on altitude

## Troubleshooting

If you encounter issues:
1. Check the log files in the AutoOrtho directory
2. Ensure all Python dependencies are installed
3. Verify your internet connection for image data downloads
4. Consult the [AutoOrtho Forum](https://forums.x-plane.org/index.php?/forums/forum/406-autoortho/) for additional help

## Improving Ortho Maps with Ortho4XP 1.4

AutoOrtho can be enhanced using custom Ortho4XP 1.4 tiles. This method provides greater control over the quality and appearance of orthophotos.

### Ortho4XP 1.4 Configuration

For optimal results with AutoOrtho, use the following settings in Ortho4XP 1.4:

| Parameter                  | Recommended Value | Description |
|---------------------------|------------------|-------------|
| `skip_downloads`          | Enabled          | No imagery download needed |
| `skip_converts`           | Enabled          | No DDS rendering needed |
| `mask_zl`                 | 16               | Optimal water transitions |
| `use_masks_for_inland`    | Enabled          | Better inland water bodies |
| `distance_masks_too`      | Enabled          | Clean coastlines |
| `custom_dem`              | Optional         | Higher DEMs for finer meshes |
| `curvature_tol`           | 2.0–4.0          | Affects mesh complexity |
| `road_banking_limit`      | 0.3              | Prevents build errors |
| `apt_smoothing_pix`       | 8–16             | Smoother runways |
| `water_tech`              | "XP12"           | Uses XP12 water technology |

### Tile Consolidation

To make the created tiles usable with AutoOrtho, they need to be consolidated in a specific format. A consolidation script can be used for this purpose:

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
3. Copy the folder to:
   ```
   ~/X-Plane 12/Custom Scenery/yOrtho4XP_RegionName/
   ```

### scenery_packs.ini Configuration

The correct order in `scenery_packs.ini` is important:

```ini
SCENERY_PACK Custom Scenery/yOrtho4XP_RegionName/
SCENERY_PACK Custom Scenery/z_autoortho/scenery/zOrtho4XP_RegionName/
SCENERY_PACK Custom Scenery/z_autoortho/scenery/z_autoortho_xyz/
```

### Benefits of This Method

- Greater control over orthophoto quality
- Optimized performance through adjusted mesh details
- Better representation of water bodies and coastlines
- Ability to integrate overlays for additional details
- Complete control over zoom levels and file size

### Note on Using with SimHeaven

When using [SimHeaven](https://simheaven.com/), the `yOrtho4XP` directories are not required as SimHeaven already contains all necessary overlay data. In this case, neither the Ortho4XP-created nor the AutoOrtho-generated `yOrtho4XP` directories need to be listed in the `scenery_packs.ini`.

