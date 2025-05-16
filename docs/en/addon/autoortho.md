# AutoOrtho

Visual quality of landscapes is crucial for Visual Flight Rules (VFR) flights in flight simulators. While X-Plane provides standard textures, these are often perceived as outdated. AutoOrtho addresses this issue by integrating satellite imagery in real-time, providing detailed representation of infrastructure, vegetation, and other terrain features. The current version 0.7.2, released on January 28, 2024, optimizes integration with X-Plane and reduces common issues such as scenery conflicts or performance problems.

## How It Works

AutoOrtho implements a streaming system for orthophotos based on the aircraft's position and renders them as textures in X-Plane. The system operates through several key mechanisms:

- The real-time streaming system loads satellite images in tiles from providers like Bing, using a zoom level of up to 16 (ZL16) to balance detail and loading time. Tiles for current and adjacent areas are preloaded to ensure seamless transitions, requiring a stable internet connection of at least 100 Mbps.

- A virtual file system (WinFSP/Dokan on Windows, FUSE on Linux) manages the tiles in a local cache on SSD and represents them as scenery files in the z_autoortho folder of the Custom Scenery directory.

AutoOrtho delivers 2D orthophotos without 3D objects. For buildings and vegetation, SimHeaven (X-World) is recommended, utilizing OpenStreetMap data. Overlays adapt the images to the X-Plane terrain mesh and contain essential information such as airport flattening, traffic infrastructure, and railway lines. When using SimHeaven X-World, the yOrtho overlays are redundant.

The streaming process impacts CPU, RAM (up to 64 GB), and disk performance. While SSDs minimize bottlenecks, frame drops can occur with slow connections or underpowered hardware.

## Installation and Configuration

### System Requirements

The system requires X-Plane 11.50+ or X-Plane 12, running on Windows, Linux (with FUSE), or macOS (experimental). Dependencies include WinFSP/Dokan (Windows), FUSE (Linux), and optionally Python 3.x for source code. Hardware requirements include 16 GB RAM, SSD storage, and a fast internet connection (≥100 Mbps).

### Installation Process

AutoOrtho is downloaded from GitHub (kubilus1/autoortho), either as a binary or installer. Windows users install WinFSP/Dokan and launch autoortho_win.exe, while Linux users require FUSE, and macOS users should follow experimental instructions.

The GUI requires the X-Plane main directory and Custom Scenery directory. Regional overlays (few GB) are installed via the "Scenery" tab. The scenery_packs.ini is configured with the following structure:

```
SCENERY_PACK Custom Scenery/yAutoOrtho_Overlays/
SCENERY_PACK Custom Scenery/z_ao_eur/
SCENERY_PACK Custom Scenery/z_autoortho/
```

The z_autoortho entry is placed at the end to give priority to other scenery. The current version restores placeholder directories to ensure a stable order. AutoOrtho must be started before X-Plane to mount the virtual file system, and the scenery_packs.ini should be write-protected or managed by a tool like xOrganizer.

The yAutoOrtho_Overlays directory is only needed if SimHeaven is not used.

### Important Configuration Parameters

The AutoOrtho configuration can be adjusted in the `.autoortho` configuration file. Here are the most important parameters:

- `xplane_path`: Path to the X-Plane main directory
- `cache_dir`: Directory for orthophoto cache (recommended: fast SSD)
- `provider`: Image source for orthophotos (bing, google, here)
- `cache_size`: Maximum cache size in GB
- `maxwait`: Maximum wait time for images in seconds. Higher values mean better quality but more stuttering. Lower values are more responsive but may occasionally result in lower quality.
- `min_zoom`: Minimum zoom level for satellite images. Affects the minimum quality of displayed images.
- `autostart`: Start AutoOrtho automatically with X-Plane
- `debug`: Enable debug information in logs

Example configuration file:
```ini
xplane_path = /home/user/X-Plane-12
cache_dir = /home/user/.autoortho-data/cache
provider = bing
cache_size = 20
maxwait = 2
min_zoom = 14
autostart = true
debug = false
```

For optimal experience, SimHeaven X-World adds 3D objects and autogen, while xOrganizer/xToolbox simplifies scenery management. vStates offers an alternative for pre-made orthophotos.

### Comparison with Ortho4XP

AutoOrtho and Ortho4XP serve different purposes in the X-Plane ecosystem. AutoOrtho streams data in real-time from Bing/USGS, requiring minimal storage (few GB cache) but constant internet connection. It operates at ZL16, which provides a good balance of detail and performance. In contrast, Ortho4XP uses prepared local tiles from Bing/Google, requiring hundreds of GB of storage but supporting up to ZL19 for maximum detail.

AutoOrtho's performance may show occasional stuttering and places higher demands on CPU/RAM, while Ortho4XP offers more stable performance with locally stored data. Setup is simpler with AutoOrtho after initial configuration, while Ortho4XP requires time-consuming tile creation but offers more detailed scenery for specific regions.

### Common Issues and Solutions

Users may encounter several common issues when using AutoOrtho:

1. **Initialization Errors**:
    - Cause: Incorrect WinFSP/Dokan installation or faulty scenery_packs.ini configuration
    - Solution: Reinstall/configure WinFSP/Dokan. Correct scenery_packs.ini.

2. **FUSE Problems** (Linux):
    - Log entry: `FUSE error: Failed to mount filesystem`
    - Cause: Missing fuse3 installation or permission issues
    - Solution: Install fuse3 and check permissions (Linux: ls -l /dev/fuse)

3. **Python Module Issues**:
    - Log entry: `ModuleNotFoundError: No module named 'pyfuse3'`
    - Cause: Missing dependencies
    - Solution: Install missing dependencies in the virtual environment

4. **Performance Problems**:
    - Cause: Slow connections or underpowered hardware
    - Solution: Use an SSD and reduced graphics settings

5. **Airport Topography Problems**:
    - Cause: Lack of automatic airport flattening or missing Ortho Patches for airport scenery
    - Solution: Implement Ortho Patches or the flatten 1 parameter in apt.dat and check airport scenery prioritization

6. **Network Issues**:
    - Log entry: `HTTP 429: Too Many Requests`
    - Cause: Bing blacklisting
    - Solution: Use VPN or switch to USGS sources

7. **Scenery Conflicts**:
    - Log entry: `Warning: z_autoortho not found in scenery_packs.ini`
    - Cause: Incorrect scenery order
    - Solution: Correct scenery order in scenery_packs.ini

8. **Memory Issues**:
    - Log entry: `MemoryError: Out of memory`
    - Cause: High RAM usage
    - Solution: Reduce cache size, lower X-Plane graphics settings

9. **Crashes**:
    - Cause: RAM overload or add-on conflicts
    - Solution: Disable add-ons, increase RAM, or reduce cache size

### Log Analysis

The user can analyze the autoortho.log using various methods:

- View the entire log:
    ```bash
    cat ~/.autoortho-data/autoortho.log | less
    ```

- Monitor log in real-time:
    ```bash
    tail -f ~/.autoortho-data/autoortho.log
    ```

- Search for specific errors:
    ```bash
    grep -i "error" ~/.autoortho-data/autoortho.log
    ```

For more detailed log information, the debug mode can be enabled in the `.autoortho` configuration file:

```ini
# Debug mode
debug = true
```

## Linux-specific Installation

### Installation Example: AutoOrtho on Debian 12 with pyenv

This section provides a detailed walkthrough of installing AutoOrtho using the Python version on a Debian 12 system. The example demonstrates how to set up an isolated Python environment with pyenv and includes comprehensive troubleshooting using the autoortho.log file.

### System Requirements

The example system runs Debian 12 (Bookworm) with X-Plane 12, featuring an SSD, 32 GB RAM, and a stable 200 Mbps internet connection. Required dependencies include:

- fuse3 for the virtual filesystem
- git, build-essential, libssl-dev, zlib1g-dev for pyenv and Python
- Python 3.8+ (managed via pyenv)
- A few GB of SSD storage for overlays and cache

### Step-by-Step Installation

1. **System Preparation**:
    The user updates the system and installs basic dependencies:

    ```bash
    sudo apt update && sudo apt upgrade -y
    sudo apt install -y fuse3 libfuse2 git curl build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev wget llvm libncurses5-dev libncursesw5-dev \
    xz-utils tk-dev libffi-dev liblzma-dev python3-openssl
    ```

2. **pyenv Setup**:
    After installing pyenv, the user configures their environment:

    ```bash
    curl https://pyenv.run | bash
    ```

    Add to ~/.bashrc:
    ```bash
    export PATH="$HOME/.pyenv/bin:$PATH"
    eval "$(pyenv init --path)"
    eval "$(pyenv init -)"
    ```

    Install Python 3.10.13:
    ```bash
    pyenv install 3.10.13
    pyenv global 3.10.13
    ```

3. **AutoOrtho Installation**:
    Clone the repository and set up the virtual environment:

    ```bash
    git clone https://github.com/kubilus1/autoortho.git ~/autoortho
    cd ~/autoortho
    git checkout v0.7.2

    pyenv virtualenv 3.10.13 autoortho
    pyenv activate autoortho
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

4. **X-Plane Configuration**:
    Configure the scenery_packs.ini with the correct order:

    ```
    SCENERY_PACK Custom Scenery/yAutoOrtho_Overlays/
    SCENERY_PACK Custom Scenery/z_ao_eur/
    SCENERY_PACK Custom Scenery/z_autoortho/
    ```

    Make the file read-only:
    ```bash
    chmod 444 ~/X-Plane-12/Custom\ Scenery/scenery_packs.ini
    ```

## Conclusion

This installation example shows how to set up AutoOrtho in a Python environment on Debian 12. The Python version offers flexibility through source code access, while the autoortho.log file provides detailed insights into system operation. With proper configuration and optimization, users can enjoy high-quality orthophotos in X-Plane 12, enhanced by 3D objects from SimHeaven.

The combination of AutoOrtho with SimHeaven X-World creates a comprehensive scenery solution that provides both detailed orthophotos and precise 3D objects. While AutoOrtho handles ground textures, SimHeaven adds buildings, trees, and other 3D elements based on OpenStreetMap data.

## Resources

- [GitHub Repository](https://github.com/kubilus1/autoortho)
- [X-Plane.org Forum](https://forums.x-plane.org/forums/forum/802-autoortho-streaming-ortho-imagery-for-x-plane/)

