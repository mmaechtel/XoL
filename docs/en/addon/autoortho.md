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

The configuration file `.autoortho` is created in your home directory and can be edited with a text editor. Important parameters:

```ini
xplane_path = /path/to/xplane
cache_dir = /path/to/cache
provider = bing
cache_size = 20
maxwait = 1.5
min_zoom = 14
autostart = true
debug = false
```

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

AutoOrtho can be enhanced using custom Ortho4XP 1.4 tiles. For optimal results:

1. Use the following settings in Ortho4XP 1.4:
   - `skip_downloads` and `skip_converts` enabled
   - `mask_zl` set to 16
   - `use_masks_for_inland` and `distance_masks_too` enabled
   - `curvature_tol` between 2.0–4.0
   - `road_banking_limit` set to 0.3
   - `apt_smoothing_pix` between 8–16
   - `water_tech` set to "XP12"

2. Consolidate the tiles using this script:
   ```bash
   #!/bin/bash
   SRC="$HOME/xplane-ortho-work/tiles_source"
   DST="$HOME/xplane-ortho-work/tiles_consolidated/zOrtho4XP_RegionName"
   rm -rf "$DST"
   mkdir -p "$DST"
   find "$SRC" -type f -name "*.bak" -delete
   for TILE in "$SRC"/*; do
       if [ -d "$TILE" ]; then
           [ -d "$TILE/textures" ] && cp -r "$TILE/textures" "$DST/"
           [ -d "$TILE/terrain" ] && cp -r "$TILE/terrain" "$DST/"
           [ -d "$TILE/Earth nav data" ] && cp -r "$TILE/Earth nav data" "$DST/"
       fi
   done
   ```

3. Copy the consolidated folder to:
   ```
   ~/X-Plane 12/Custom Scenery/z_autoortho/scenery/
   ```

4. Configure the `scenery_packs.ini`:
   ```ini
   SCENERY_PACK Custom Scenery/yOrtho4XP_RegionName/
   SCENERY_PACK Custom Scenery/z_autoortho/scenery/zOrtho4XP_RegionName/
   SCENERY_PACK Custom Scenery/z_autoortho/scenery/z_autoortho_xyz/
   ```

## Important Notes and Troubleshooting

AutoOrtho runs as a background service and generates orthophotos during flight. The textures are stored in a cache to avoid repeated downloads. A stable internet connection is required for streaming orthophotos. The quality of orthophotos is automatically adjusted based on altitude.

If you encounter issues:
1. Check the log files in the AutoOrtho directory
2. Ensure all Python dependencies are installed
3. Verify your internet connection for image data downloads
4. Consult the [AutoOrtho Forum](https://forums.x-plane.org/index.php?/forums/forum/406-autoortho/) for additional help

When using [SimHeaven](https://simheaven.com/), the `yOrtho4XP` directories are not required as SimHeaven already contains all necessary overlay data.

