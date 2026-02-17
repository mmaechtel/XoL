# AutoOrtho

Visual quality of landscapes is crucial for **Visual Flight Rules (VFR)** flights in flight simulators. While X-Plane provides standard textures, these are often perceived as outdated. **AutoOrtho** addresses this limitation through **real-time integration** of satellite imagery, enabling precise representation of infrastructure, vegetation, and other terrain features. The last version released by kubilus1, version 0.7.2 (January 21, 2024), optimized integration with X-Plane and minimized typical problems such as **scenery conflicts** or **performance issues**.

There is now an active fork at [https://github.com/ProgrammingDinosaur/autoortho4xplane](https://github.com/ProgrammingDinosaur/autoortho4xplane) where AutoOrtho continues to be developed.

## How It Works

AutoOrtho implements a streaming system for orthophotos based on the aircraft's position and renders them as textures in X-Plane. The system operates through several key mechanisms:

- The real-time streaming system loads satellite images in tiles from providers like Bing, using a zoom level of up to 18 (ZL18) to balance detail and loading time. Tiles for current and adjacent areas are preloaded to ensure seamless transitions, requiring a stable internet connection of at least 100 Mbps.

- A virtual file system (WinFSP/Dokan on Windows, FUSE on Linux) manages the tiles in a local cache on SSD and represents them as scenery files in the z_autoortho folder of the Custom Scenery directory.

AutoOrtho delivers 2D orthophotos without 3D objects. For buildings and vegetation, SimHeaven (X-World) is recommended, utilizing OpenStreetMap data. Overlays adapt the images to the X-Plane terrain mesh and contain essential information such as airport flattening, traffic infrastructure, and railway lines. When using SimHeaven X-World, the yOrtho overlays are redundant.

The streaming process impacts CPU, RAM (up to 64 GB), and disk performance. While SSDs minimize bottlenecks, frame drops can occur with slow connections or underpowered hardware.

### Enhanced Features of the Fork (Version 2.0)

The [ProgrammingDinosaur Fork](https://github.com/ProgrammingDinosaur/autoortho4xplane) builds upon the original codebase and has evolved with version 2.0 into a standalone continuation with significant improvements:

- **C pipeline for texture processing**: New native C implementation with up to 3x improvement in loading times compared to the Python pipeline. Four pipeline modes available: Auto (automatic selection), Native (pure C), Hybrid (C + Python), and Python (fallback)
- **.aob2 bundle format**: New compact data format for scenery packages
- **Increased zoom levels and resolution** for X-Plane 12
- **New user interface** with modern frameworks
- **Revised installer** with safety checks for target locations
- **Improved scenery download experience** (faster and more user-friendly)
- **macOS compatibility** (Apple Silicon only)
- **Extended map providers**: Bing, Google, Here, Yandex, and Apple Maps
- **Automatic scenery_packs.ini configuration** for use with SimHeaven

## Installation and Configuration

### System Requirements

The system requires X-Plane 11.50+ or X-Plane 12, running on Windows, Linux (with FUSE), or macOS (Apple Silicon). Dependencies include WinFSP/Dokan (Windows), FUSE (Linux), and optionally Python 3.x for source code. Hardware requirements include 16 GB RAM, SSD storage, and a fast internet connection (≥100 Mbps).

**Note**: The [ProgrammingDinosaur Fork](https://github.com/ProgrammingDinosaur/autoortho4xplane) provides full macOS compatibility for Apple Silicon processors and enhanced features for X-Plane 12.

### Installation Process

AutoOrtho is downloaded from GitHub (kubilus1/autoortho), either as a binary or installer. For the latest features and improvements, the [ProgrammingDinosaur Fork](https://github.com/ProgrammingDinosaur/autoortho4xplane) is recommended, which provides a revised installer with safety checks. Windows users install WinFSP/Dokan and launch autoortho_win.exe, while Linux users require FUSE, and macOS users (Apple Silicon) should follow the appropriate instructions.

The GUI requires the X-Plane main directory and Custom Scenery directory. Regional overlays (few GB) are installed via the "Scenery" tab. The [ProgrammingDinosaur Fork](https://github.com/ProgrammingDinosaur/autoortho4xplane) provides automatic scenery_packs.ini configuration for use with SimHeaven. Manual configuration follows this structure:

```
SCENERY_PACK Custom Scenery/yAutoOrtho_Overlays/
SCENERY_PACK Custom Scenery/z_ao_eur/
SCENERY_PACK Custom Scenery/z_autoortho/
```

The z_autoortho entry is placed at the end to give priority to other scenery. The current version restores placeholder directories to ensure a stable order. AutoOrtho must be started before X-Plane to mount the virtual file system, and the scenery_packs.ini should be write-protected or managed by a tool like xOrganizer.

The yAutoOrtho_Overlays directory is only needed if SimHeaven is not used.

### Configuration

The [ProgrammingDinosaur Fork](https://github.com/ProgrammingDinosaur/autoortho4xplane) provides a modern GUI for all configuration settings, enabling easy setup without manual file editing. The most important settings include:

- **X-Plane Path**: Directory of the X-Plane installation folder
- **Cache Directory**: Storage location for orthophoto cache (recommended: fast SSD)
- **Map Provider**: Choice between Bing, Google, Here, Yandex, and Apple Maps
- **Cache Size**: Maximum cache size in GB — when the limit is reached, older tiles are automatically removed
- **Wait Time**: Balance between quality and responsiveness
- **Zoom Level**: Minimum and maximum zoom for satellite images
- **Autostart**: Automatic startup with X-Plane
- **Debug Mode**: Enhanced logging information

For advanced configurations, the `.autoortho` configuration file can still be manually edited if desired.

For optimal experience, SimHeaven X-World adds 3D objects and autogen, while xOrganizer/xToolbox simplifies scenery management. vStates offers an alternative for pre-made orthophotos.

## Comparison with Ortho4XP

AutoOrtho and Ortho4XP pursue architecturally different approaches, each optimized for different player profiles.

| Dimension | AutoOrtho | Ortho4XP |
|---|---|---|
| Data acquisition | On-demand streaming at runtime | Pre-generated (offline) |
| Storage requirements | Cache with automatic eviction (limit configurable) | Permanent per region (1–8 GB at ZL17) |
| Internet required | Yes (on cache miss) | No (after generation) |
| Max zoom level | Up to ZL18 (Fork 2.0) | Up to ZL19 |
| Spontaneity | Instantly flyable, worldwide | Pre-generation required (30 min to hours) |
| Visual consistency | Progressive loading on first visit | Immediate full quality |
| Offline capability | Only cached regions | Full |

**Which system is a better fit?**

- **Habitual player** (recurring home airports): Ortho4XP offers structural advantages here — after one-time generation, the entire dataset is stored locally, cache hit rate is 100%, and there are no runtime dependencies on network or map servers.

- **Explorative player** (constantly new destinations): AutoOrtho is the better choice — no pre-generation needed, spontaneous flights anywhere in the world. Ortho4XP would lead to an ever-growing dataset that is rarely reused.

- **Hybrid player**: The [combination of both systems](static_plus_streaming.md) offers the best of both worlds.

!!! info "Cache Behavior"
    AutoOrtho features automatic cache eviction: When the configured cache size is reached, older tiles are automatically removed to make room for new ones. In contrast to Ortho4XP, where generated tiles remain permanently on disk, AutoOrtho self-regulates its storage consumption.

### Common Issues and Solutions

For basic installation and configuration issues (initialization errors, FUSE problems, Python module issues, performance problems), please refer to the current documentation of the [ProgrammingDinosaur Fork](https://github.com/ProgrammingDinosaur/autoortho4xplane), as these issues have been resolved or simplified in the newer version.

Additional specific issues when using AutoOrtho:

1. **Airport Topography Problems**:
    - Cause: Lack of automatic airport flattening or missing Ortho Patches for airport scenery
    - Solution: Implement Ortho Patches or the flatten 1 parameter in apt.dat and check airport scenery prioritization

2. **Network Issues**:
    - Log entry: `HTTP 429: Too Many Requests`
    - Cause: Bing blacklisting
    - Solution: Use VPN or switch to USGS sources

3. **Scenery Conflicts**:
    - Log entry: `Warning: z_autoortho not found in scenery_packs.ini`
    - Cause: Incorrect scenery order
    - Solution: Correct scenery order in scenery_packs.ini

4. **Memory Issues**:
    - Log entry: `MemoryError: Out of memory`
    - Cause: High RAM usage
    - Solution: Reduce cache size, lower X-Plane graphics settings

5. **Crashes**:
    - Cause: RAM overload or add-on conflicts
    - Solution: Disable add-ons, increase RAM, or reduce cache size

### Log Analysis

The autoortho.log can be analyzed using various methods:

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

For more detailed log information, the debug mode can be enabled in settings or the `.autoortho` configuration file:

```ini
# Debug mode
debug = true
```

## Linux-specific Installation

### Installation Example: AutoOrtho on Debian 12 with pyenv

This section provides a detailed walkthrough of installing AutoOrtho using the Python version on a Debian 12 system. The example demonstrates how to set up an isolated Python environment with pyenv and includes comprehensive troubleshooting using the autoortho.log file.

**Note**: For the latest features, the [ProgrammingDinosaur Fork](https://github.com/ProgrammingDinosaur/autoortho4xplane) is recommended, which provides an improved GUI and enhanced compatibility.

### System Requirements

The example system runs Debian 12 (Bookworm) with X-Plane 12, featuring an SSD, 32 GB RAM, and a stable 200 Mbps internet connection. Required dependencies include:

- fuse3 for the virtual filesystem
- git, build-essential, libssl-dev, zlib1g-dev for pyenv and Python
- Python 3.12+ (managed via pyenv) - recommended for ProgrammingDinosaur Fork
- A few GB of SSD storage for overlays and cache

### Step-by-Step Installation

1. **System Preparation**:
    Update the system and install basic dependencies:

    ```bash
    sudo apt update && sudo apt upgrade -y
    sudo apt install -y fuse3 libfuse2 git curl build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev wget llvm libncurses5-dev libncursesw5-dev \
    xz-utils tk-dev libffi-dev liblzma-dev python3-openssl
    ```

2. **pyenv Setup**:
    After installing pyenv, configure the environment:

    ```bash
    curl https://pyenv.run | bash
    ```

    Add to ~/.bashrc:
    ```bash
    export PATH="$HOME/.pyenv/bin:$PATH"
    eval "$(pyenv init --path)"
    eval "$(pyenv init -)"
    ```

    Install Python 3.12.0:
    ```bash
    pyenv install 3.12.0
    pyenv global 3.12.0
    ```

3. **AutoOrtho Installation**:
    Clone the repository and set up the virtual environment:

    ```bash
    # For the ProgrammingDinosaur Fork (recommended):
    git clone https://github.com/ProgrammingDinosaur/autoortho4xplane.git ~/autoortho
    cd ~/autoortho

    pyenv virtualenv 3.12.0 autoortho
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

---

## Further Reading

| Topic | Page | Focus |
|---|---|---|
| XEarthLayer | [XEarthLayer](xearthlayer.md) | Rust-based streaming alternative with adaptive prefetch |
| Ortho4XP | [Ortho4XP](../orthophotography/ortho4xp.md) | Static ortho tile generation for offline use |
| Static + Streaming | [Static + Streaming](static_plus_streaming.md) | Combining local tiles with streaming |
| Scenery Components | [How X-Plane Builds the World](../aufbau_quellen/scenery_components.md) | scenery_packs.ini load order and layer interaction |
| Filesystem | [Filesystem](../../linux/optimizations/filesystem.md) | I/O optimization for cache and SSD performance |
| XOrganizer | [XOrganizer](../../addon/tools/xorganizer.md) | Scenery management and scenery_packs.ini editor |

---

## Sources

- [GitHub Repository (Original)](https://github.com/kubilus1/autoortho)
- [GitHub Repository (ProgrammingDinosaur Fork)](https://github.com/ProgrammingDinosaur/autoortho4xplane)
- [X-Plane.org Forum](https://forums.x-plane.org/forums/forum/802-autoortho-streaming-ortho-imagery-for-x-plane/)

