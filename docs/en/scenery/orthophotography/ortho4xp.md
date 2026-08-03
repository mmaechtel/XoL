---
description: "Ortho4XP generates high-resolution satellite ground textures for X-Plane. Installation, OrthoForge, parameter reference, mesh-only packages for ortho streaming, LiDAR integration, and Ortho Patches on Linux."
---
# Ortho4XP

Ortho4XP is a powerful tool for creating orthophotos for X-Plane. It enables the generation of high-resolution ground textures from satellite imagery and elevation data.

## Installation and Versions

Ortho4XP is available in several versions:

1. **Original version** by Oscar Pilote:
    - [GitHub Repository](https://github.com/oscarpilote/Ortho4XP)
    - The original version with basic features

2. **shred86's fork** (recommended):
    - [GitHub Repository](https://github.com/shred86/Ortho4XP)
    - [Detailed documentation](https://github.com/shred86/Ortho4XP/wiki)
    - Contains numerous improvements and new features
    - [Binaries for various operating systems](https://github.com/shred86/Ortho4XP/wiki/Installation)

3. **OrthoForge** (independently developed successor):
    - [Project page and documentation](https://xpconnect.me/orthoforge.html) — GPL v3, maintained by xbard
    - Started as the English fork of ORTHO4XP_V3 by Roland (Ypsos) and is now developed independently; changes are no longer synchronized with any upstream Ortho4XP branch. The project credits Oscar Pilote (original Ortho4XP), shred86 (1.40 line) and Roland/Ypsos (V3 architecture)
    - Targets X-Plane 12 — the XP12 water and material paths are the default, not an option

!!! warning "The OrthoForge source repository is being retired"

    The Codeberg repository states: *"Due to changes in Codeberg policy, this repo will soon be deleted and hosted at https://xpconnect.me/orthoforge.html"*. Use the project page as the entry point; any Codeberg link will break without notice.

**What OrthoForge does differently**

| Area | Difference |
|---|---|
| OSM download | Can pull pre-baked OpenStreetMap layers from a mirror instead of querying Overpass, which removes the rate-limit stalls that dominate large batch builds — see [Pre-baked OSM and DEM Data](#pre-baked-osm-and-dem-data) |
| Elevation | Land and seabed elevation are configured as separate sources (`custom_dem_search_dirs` / `custom_bathy_search_dirs`), so a high-resolution land dataset no longer has to be reconciled with bathymetry in one file |
| Airports | Airport coverage zoom is graduated rather than a single `cover_zl` step |
| XP12 terrain | Exposes the XP12 material parameters, including terrain roughness, in the tile configuration |

**Setup on Linux**

- `OrthoForge_Setup_Linux.sh` runs a guided setup; `setup_venv.sh` is the plain-shell alternative for distributions with a locked-down system pip (PEP 668) and needs no root
- Requires Python 3.10 or newer. The build runs from a virtual environment created with `--system-site-packages`, so it inherits system-installed tkinter and the optional GDAL bindings instead of rebuilding them
- Distribution packages needed beforehand: tkinter and Pillow's Tk bindings. GDAL is optional — the elevation path prefers rasterio
- Setup is documented for Fedora, Debian/Ubuntu, Arch and openSUSE Tumbleweed

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
    - Installation with Docker (see [Docker Documentation](../../linux/extensions/docker.md))
    - Installation with pyenv (see [pyenv Documentation](../../linux/extensions/pyenv.md))

## Usage and Configuration

### Basic Usage

1. Start Ortho4XP via the Python file or executable:

    ```bash
    python Ortho4XP.py
    ```

2. In the main window, select:
    - The target area (tile)
    - The desired zoom level (ZL)
    - The imagery source (e.g., Bing, Google, Here)

3. Click "Build" to start the process

### Important Parameters

All settings live in `Ortho4XP.cfg` in the Ortho4XP directory. When a tile is built, Ortho4XP writes the tile-specific subset of these keys into `Tiles/zOrtho4XP_+dd+ddd/Ortho4XP_+dd+ddd.cfg`, so an existing tile keeps the settings it was built with even if the global config changes later. The defaults below are the ones defined in `src/O4_Cfg_Vars.py`.

The parameters are grouped by the question they answer:

| Group | Answers |
|---|---|
| Directories and imagery source | Where tiles are written and which provider supplies the imagery |
| Mesh generation | How dense and how well-shaped the terrain triangles are |
| Roads | How much of the road network is flattened into the terrain |
| Terrain appearance | Shadows, decals and overlay draw distance |
| High-resolution airport coverage | Where the scenery switches to a higher zoom level |
| Masks and water | Coastlines, inland water and their transparency |
| Elevation | Which elevation dataset the mesh is built from |

**Directories and imagery source**

| Parameter | Default | Description |
|---|---|---|
| `custom_scenery_dir` | `""` | Target for the one-click creation and removal of symlinks from the Ortho4XP tiles — not a build target |
| `custom_overlay_src` | `""` | Source for overlay data. Select the directory one level **above** `Earth nav data` |
| `custom_overlay_src_alternate` | `""` | Fallback path, used when the first source has no data for a tile |
| `default_website` | `""` | Imagery source, e.g. `BI` (Bing), `GO2` (Google), `ES` (ESRI) |
| `default_zl` | `16` | Base zoom level of the ortho textures |

There is no `zoomlevel` and no `provider` key — those names appear in older documentation and in internal code, but a config file containing them is parsed without them taking effect. Use `default_zl` and `default_website` instead.

**Mesh generation**

| Parameter | Default | Description |
|---|---|---|
| `mesh_zl` | `19` | Mesh resolution, permitted values `16`–`20`. Also caps the imagery zoom level that can be used on the tile later |
| `min_angle` | `10.0` | Minimum triangle angle in degrees — the smallest angle for water triangles, the second-smallest for ordinary land triangles |
| `curvature_tol` | `2.0` | Terrain curvature tolerance. Higher values produce **fewer** triangles |
| `apt_curv_tol` | `0.5` | Curvature tolerance around airports |
| `apt_curv_ext` | `0.5` | Extent of the airport curvature zone, in km |
| `coast_curv_tol` | `1.0` | Curvature tolerance along coastlines |
| `coast_curv_ext` | `0.5` | Extent of the coastal curvature zone, in km |
| `limit_tris` | `3.0` | Upper bound on the triangle count of a tile, in millions. At `0` a hard limit of 5 million applies |
| `apt_smoothing_pix` | `8` | Strength of the Gaussian blur applied to the elevation raster for altitude queries over airports, in raster pixels |

`min_angle` is the strongest single lever on mesh quality and one of the first values worth adjusting. Raising it forces better-shaped triangles and removes the thin slivers that cause shading artifacts and unstable runway surfaces; lowering it produces a coarser, cheaper mesh. Raising `min_angle` and lowering `curvature_tol` both increase the triangle count, so `limit_tris` acts as the ceiling. Set it explicitly whenever a high-resolution DEM is in use — such a dataset can otherwise drive the count far beyond what the tile needs.

**Roads**

| Parameter | Default | Description |
|---|---|---|
| `road_level` | `1` | How much of the OSM road network is leveled into the mesh, `0`–`5` |
| `road_banking_limit` | `0.5` | How much a road must be banked before it is leveled at all, in meters — measured as the height difference between a point on the road centerline and the nearest point at the road edge |
| `lane_width` | `4.0` | Width in meters used when buffering the road network for leveling |

The `road_level` steps are cumulative:

- `0` — nothing
- `1` — motorways, primary and secondary roads, railway lines
- `2` — additionally tertiary roads
- `3` — additionally residential and unclassified roads
- `4` — additionally service roads
- `5` — additionally tracks

When changing between levels `2` and `5`, the cached `small_roads.osm` has to be discarded, otherwise the previously cached road set is reused.

**Terrain appearance**

| Parameter | Default | Description |
|---|---|---|
| `terrain_casts_shadows` | `True` | Only effective when scenery shadows are enabled in X-Plane's graphics settings. Terrain receives shadows even when it casts none |
| `use_decal_on_terrain` | `False` | Applies the `maquify_1_green_key.dcl` decal directive to all non-water terrains. Counteracts ortho blurriness at very low altitude, can be mildly distracting higher up |
| `normal_map_strength` | `1.0` | Ortho imagery already has shading baked in; this detunes the DSF normals against overshading. It also affects how X-Plane computes scenery shadows |
| `overlay_lod` | `25000` | Distance up to which overlay imagery (ortho over water) is drawn. Lower values help frame rate and VRAM; IFR flying needs higher values than VFR |

**High-resolution airport coverage**

| Parameter | Default | Description |
|---|---|---|
| `cover_airports_with_highres` | `False` | `ICAO` covers airports with an ICAO code at a higher zoom level, `Existing` reuses the airport zones already present in the tile |
| `cover_zl` | `18` | Zoom level used inside the high-resolution zone |
| `cover_extent` | `1.0` | Radius of the high-resolution zone around each airport, in km |

`cover_extent` is the main lever on package size, and the useful range is wide — values from `0.5` to `6.0` are all plausible, a twelvefold difference in radius and roughly a hundredfold in covered area per airport.

**Masks and water**

| Parameter | Default | Description |
|---|---|---|
| `mask_zl` | `14` | Zoom level of the coastal transparency masks. Permitted values are only `14`, `15` and `16` |
| `masks_width` | `100` | Width of the mask transition zone, in meters. In older versions this was counted in ZL14 pixels, roughly a factor of 10 |
| `masking_mode` | `sand` | Which texture the mask blends toward — `sand`, `rocks` or `3steps` |
| `use_masks_for_inland` | `False` | Uses masks for inland water instead of the constant `ratio_water` transparency. Expensive in VRAM and, per the upstream hint, probably not worth the effort |
| `imprint_masks_to_dds` | `False` | Bakes the masks into the DDS textures. Doubles the file size of masked textures (DXT5 instead of DXT1) but lowers VRAM usage — a trade-off, not a clear improvement either way |
| `sea_smoothing_mode` | `zero` | How sea elevation is handled — see below |
| `water_smoothing` | `10` | Number of smoothing passes over inland water triangles |
| `ratio_water` | `0.25` | Transparency of the ortho overlay over inland water, `0`–`1`. At `0` the ortho image is fully opaque |
| `ratio_bathy` | `1.0` | Same principle for the bathymetry (sea bed) |
| `min_area` | `0.001` | Minimum size of a water body that is still modeled, in km². Contiguous water surfaces are merged **before** the area is computed |
| `max_area` | `200.0` | Water bodies above this size are masked like sea, in km² |
| `sea_texture_blur` | `0.0` | Blur radius in meters for layers of type `mask` in combined provider imagery, to tone down over-prominent wave and reflection patterns |
| `water_tech` | `XP11 + bathy` | Water rendering generation — set to `XP12` on X-Plane 12, see the callout below |

Inland water is drawn as a lower layer of X-Plane water with an ortho overlay of constant transparency on top; `ratio_water` controls that transparency. `masking_mode=3steps` turns the coastal transition into a staged one and expects `masks_width` as a list `[a,b,c]`, where `a` is the length in meters of a first transition from fully opaque imagery at the shoreline to `ratio_water` transparency, and `b` is the second transition zone.

The `sea_smoothing_mode` values differ substantially:

- `zero` — all nodes of sea triangles are forced to elevation 0
- `mean` — each triangle is set individually to its own mean elevation
- `none` — positive elevations are kept, only negative ones are pulled to 0. Suitable from a DEM resolution of 10 m and finer, and avoids the unrealistic cliff edges the other modes can produce

**Elevation**

| Parameter | Default | Description |
|---|---|---|
| `custom_dem` | `""` | Path to an external elevation raster, replacing the default viewfinderpanoramas.org data |
| `fill_nodata` | `True` | Fills no-data values by nearest neighbour. When off they become 0 |

`custom_dem` is what separates a build using high-quality LiDAR-derived elevation from a stock build. The raster must be in EPSG:4326, requires GDAL, and does not have to match the tile boundary — areas it does not cover are mapped to elevation 0, which makes it usable for high-resolution data over individual islands. Switching `fill_nodata` off is the matching setting for rasters without ocean coverage or for partial LiDAR datasets. The datasets are region-specific and have to be obtained separately — see [LiDAR Data Integration](#lidar-data-integration) below.

!!! warning "Set `water_tech=XP12` on X-Plane 12"

    The default of `water_tech` is `XP11 + bathy`. A tile built with the default renders water the way X-Plane 11 did, even when it is loaded in X-Plane 12 — the difference is visible in reflections, wave motion and the transition at the shoreline. For X-Plane 12 the value has to be set explicitly:

    ```ini
    water_tech=XP12
    ```

    The setting is stored per tile, so tiles built before the change keep the old behavior until they are rebuilt or their `Ortho4XP_+dd+ddd.cfg` is edited.

**Global settings versus per-tile settings**

Most of the parameters above are written into each tile's own config and can therefore differ from tile to tile. A few are only read from the global `Ortho4XP.cfg` and never appear in a tile config.

The two that matter most are `skip_downloads` and `skip_converts`, which suppress the imagery download and the DDS conversion. Both default to `False`, and they are what turns Ortho4XP into a producer of mesh-only packages — see [Building Packages for Ortho Streaming](#building-packages-for-ortho-streaming). Also global-only: `verbosity`, `cleaning_level`, `max_download_slots`, `max_convert_slots`, `overpass_server_choice`, `custom_scenery_dir`, `custom_overlay_src` and `custom_overlay_src_alternate`.

!!! warning "Same key names in OrthoForge, different defaults"

    OrthoForge keeps the Ortho4XP key names unchanged (`default_zl`, `default_website`, `mesh_zl`, `mask_zl`, `curvature_tol`, `cover_zl`, `road_level`, `water_tech`, `custom_dem` and the rest) and only adds keys on top. The descriptions on this page therefore transfer — but the values do not:

    | Key | Ortho4XP | OrthoForge |
    |---|---|---|
    | `default_zl` | `16` | `18` |
    | `mesh_zl` | `19` | `20` |
    | `mask_zl` | `14` | `18` |
    | `cover_zl` | `18` | `19` |
    | `water_tech` | `XP11 + bathy` | `XP12` |

    Read the tables above as *what a parameter does*, not as *what it is set to*. The OrthoForge baseline means noticeably longer build times and larger tiles than the numbers here suggest.

### Recommended Settings

The profiles below are complete config fragments and can be pasted into `Ortho4XP.cfg` as they are. They set `water_tech=XP12` throughout, since the whole page assumes X-Plane 12.

#### Standard (balanced)

```ini
default_zl=16
default_website=BI
mesh_zl=19
min_angle=10.0
curvature_tol=2.0
mask_zl=14
masking_mode=sand
masks_width=100
cover_airports_with_highres=ICAO
cover_zl=18
cover_extent=1.0
min_area=0.001
apt_smoothing_pix=8
road_level=1
water_tech=XP12
```

This is the default set with high-resolution airport coverage switched on. `mesh_zl=19` leaves enough headroom that `cover_zl=18` is not capped, and `cover_extent=1.0` keeps the high-resolution zone on the airport itself rather than its surroundings.

#### High-Resolution

```ini
default_zl=17
default_website=BI
mesh_zl=19
min_angle=15.0
curvature_tol=1.0
mask_zl=16
masking_mode=rocks
masks_width=25
cover_airports_with_highres=ICAO
cover_zl=19
cover_extent=3.0
min_area=0.0005
apt_smoothing_pix=4
road_level=3
water_tech=XP12
```

Every value moves in the direction of more detail. `curvature_tol=1.0` halves the tolerance and lets the mesh follow correspondingly finer terrain, and `min_angle=15.0` keeps those extra triangles well-shaped. `mask_zl=16` is the finest permitted mask resolution, with `masks_width=25` narrowing the shoreline transition to match, and `apt_smoothing_pix=4` blurs the elevation raster less over airports so their terrain keeps more of its real shape.

`cover_zl=19` requires `mesh_zl` to be at least `19`. Build time and package size rise steeply — with a high-resolution `custom_dem`, add an explicit `limit_tris` so the triangle count stays bounded.

#### Performance-Optimized

```ini
default_zl=15
default_website=BI
mesh_zl=16
min_angle=5.0
curvature_tol=3.0
mask_zl=14
masking_mode=sand
masks_width=100
cover_airports_with_highres=ICAO
cover_zl=16
cover_extent=0.5
min_area=0.1
apt_smoothing_pix=16
road_level=1
water_tech=XP12
```

`curvature_tol=3.0` and `min_angle=5.0` both reduce the triangle count, and `mesh_zl=16` is the lowest permitted value, capping the imagery zoom level accordingly. `min_area=0.1` drops small ponds from the water model — a hundredfold increase over the default, which removes a large share of the water geometry and its masks. `cover_zl=16` matches the base zoom level plus one and `cover_extent=0.5` keeps the high-resolution zone minimal, so airports stay recognizable without adding much texture volume.

#### Ortho Streaming Package Settings

For packages that supply mesh and terrain definitions to a streaming layer instead of shipping their own textures:

```ini
default_zl=16
default_website=BI
mesh_zl=19
min_angle=10.0
curvature_tol=2.0
water_tech=XP12
cover_airports_with_highres=ICAO
cover_zl=17
cover_extent=0.5
imprint_masks_to_dds=False
skip_downloads=True
skip_converts=True
```

`default_zl=16` as the base keeps package size and tile count manageable; the streaming layer regenerates the imagery at runtime anyway, so a higher base zoom level buys nothing at build time. `default_website=BI` is not merely informational here: the provider code is written into every texture filename the terrain definitions request (`..._BI17.dds`), so it has to match what the streaming layer serves. `water_tech=XP12` is mandatory on X-Plane 12 regardless of profile. `skip_downloads` and `skip_converts` are the two settings that turn a normal build into a mesh-and-terrain-only build — see [Building Packages for Ortho Streaming](#building-packages-for-ortho-streaming).

## Building Packages for Ortho Streaming

With [ortho streaming](../ortho_streaming/index.md) the ground textures are produced on demand at runtime — the streaming layer downloads the imagery, encodes it to DDS and hands it to X-Plane through a virtual filesystem. A package built for such a setup therefore only has to supply what the streaming layer does **not** generate: the **mesh** and the **terrain definitions** (the `Earth nav data` DSF files and the `terrain` directory). Imagery download and DDS conversion are pure waste in this workflow.

Two settings switch them off:

```ini
skip_downloads=True
skip_converts=True
```

Both default to `False`. Left at the default, a package build downloads and converts gigabytes of imagery that the streaming layer replaces at runtime and that is discarded afterwards — hours of processing time and disk space for nothing.

A third setting belongs in the same group:

```ini
imprint_masks_to_dds=False
```

This is already the default, but it is worth stating explicitly: baking water masks into DDS files is pointless when the DDS files are created elsewhere. If a previously used configuration set it to `True` for a conventional build, reset it.

!!! warning "These two are global settings, not per-tile settings"

    `skip_downloads` and `skip_converts` exist only in the global `Ortho4XP.cfg`. They are **not** written to the generated per-tile `Tiles/zOrtho4XP_+dd+ddd/Ortho4XP_+dd+ddd.cfg` files and cannot be overridden there. Searching a per-tile config for them and finding nothing does not mean they are inactive — check the global config.

Most other build parameters, including `default_zl`, `cover_zl`, `cover_extent`, `mask_zl`, `masking_mode` and `water_tech`, *are* per-tile and are recorded in each tile's config, which makes a finished tile reproducible from its own directory.

### Which Parameters Still Matter

Skipping imagery does not make the imagery settings irrelevant — it makes them binding. `default_zl`, `cover_zl` and `default_website` are baked into the terrain definitions the build produces, and those definitions are the contract between the package and the streaming layer.

A `.ter` file from a tile built with `skip_downloads=True` and `skip_converts=True` — here one built at `default_zl=17` with `cover_zl=18`, not at the profile values above — looks like this:

```
A
800
TERRAIN

LOAD_CENTER 0.15381 32.71729 4891 4096
BASE_TEX_NOWRAP ../textures/65472_77440_BI17.dds
LOAD_CENTER_BORDER 0.15381 32.71729 4891 2048
BORDER_TEX ../textures/65472_77440_ZL17.png
DECAL_LIB lib/g10/decals/maquify_2_green_key.dcl
WET
NO_SHADOW
```

The `BASE_TEX_NOWRAP` path names the exact DDS file the streaming layer has to deliver at runtime — provider code and zoom level are part of the filename (`_BI17.dds`). The package does not merely suggest a resolution; it demands one specific file per terrain definition.

That is why the zoom-level choice is not arbitrary in a build without imagery, and why `default_website` must match what the streaming layer actually serves. A package built with `BI` asks for `_BI17.dds`, and a layer configured for a different provider will not answer that name.

The same tile shows what `cover_zl` does to that contract. Of its 752 `.ter` files, 559 reference `_BI17` and 193 reference `_BI18` — the base zoom level across most of the tile, the higher cover zoom level confined to the airport surroundings. Those are numbers from one observed tile, an illustration of the mechanism rather than a target ratio — the split depends entirely on `cover_extent` and on how many airports the tile contains.

Its `textures/` directory holds 118 files against those 752 terrain definitions. That is the expected picture of a mesh-only build: terrain definitions complete, imagery largely absent.

The mesh parameters (`mesh_zl`, `min_angle`, `curvature_tol`, `limit_tris`) and the mask parameters (`mask_zl`, `masks_width`, `masking_mode`) keep their full effect, because mesh and masks are exactly what the package contains.

### Values Observed in Production Configs

The streaming profile above is a conservative starting point. Real configurations in productive use with a streaming layer sit well away from it in places — the following values were observed in a working XEarthLayer setup:

| Parameter | Streaming profile | Observed in production |
|---|---|---|
| `cover_extent` | `0.5` | `6.0` |
| `cover_zl` | `17` | `18` |
| `mask_zl` | `14` (default) | `16` |
| `masking_mode` | `sand` (default) | `rocks` |
| `ratio_water` | `0.25` (default) | `0.5` |
| `road_level` | `1` (default) | `3` |
| `masks_width` | `100` (default) | `25` |

The widest spread is in `cover_extent`, the radius in kilometers around an airport that receives high-resolution coverage. Between `0.5` and `6.0` km the radius grows twelvefold and the covered surface roughly a hundredfold. That makes it the single strongest lever on package size, on the number of high-resolution texture requests a busy terminal area produces, and on how often the scenery changes zoom level between base and airport texture.

Which end of that range fits depends on the setup: `0.5` keeps packages small and is a reasonable default for wide-area coverage, while `6.0` suits a setup where a handful of home airports matter more than total package size.

The remaining differences follow the same logic: a higher `mask_zl` with a narrower `masks_width` produces finer but tighter coastlines, `masking_mode=rocks` suits alpine and rocky shorelines better than the `sand` default, and `road_level=3` adds secondary road networks at the cost of more vector data per tile.

These are configuration values seen in practice, not benchmark results. No package-size or frame-rate measurements were taken for this comparison, so the effects described here are directional, not quantified.

`cover_zl=17` on a `default_zl=16` base keeps the high-resolution zone one step above the base rather than two, so the scenery contains fewer and gentler scale changes. That is a package-size and consistency argument, not a remedy for visual artifacts — those usually originate in texture encoding rather than in the scenery package, and no zoom-level choice removes them.

### Where the Package Goes

How the finished tiles are placed alongside a streaming mount, and in which order they have to appear in `scenery_packs.ini`, is covered separately:

- [Static + Streaming](../ortho_streaming/static_plus_streaming.md) — consolidating mesh-only tiles into a single directory and setting the load order
- [XEarthLayer](../ortho_streaming/xearthlayer.md) — the regional DSF/TER packages this build process produces, and how they are installed
- [How Ortho Streaming Works](../ortho_streaming/how_streaming_works.md) — what the streaming layer contributes at runtime

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

### Pre-baked OSM and DEM Data

The OrthoForge project runs two supporting services that are useful independently of which builder is in use. Both are free and need no account.

**Pre-baked OpenStreetMap tiles**

- Ready-made OSM vector layers (airports, roads, coastline, water) in Ortho4XP's own cache format, at maximum road detail so they can still be filtered down locally
- Coverage is incomplete and grows over time, Europe first; tiles outside the baked area fall back to a normal Overpass query
- Delivered as bzip2-compressed OSM XML under `OSM_data/<block>/<tile>/`. For Ortho4XP, the files are dropped into `OSM_data` unchanged — not renamed, not unpacked — and the builder picks them up instead of calling Overpass
- Data remains © OpenStreetMap contributors, ODbL
- [Pre-baked OSM tiles](https://xpconnect.me/orthoforge-data.html)

**Sonny DTM mirror**

The same site hosts an authorised mirror of Sonny's elevation data, offered as standard SRTM-style `.hgt` tiles at 3″, 1″ and — for the United States, rebuilt from USGS 3DEP — 0.5″. Ortho4XP uses these exactly like the originals: unpack into `Elevation_data`, as described above. OrthoForge can point at them through `custom_dem_search_dirs`.

The mirror is a convenience copy limited to what the OrthoForge project has staged. [sonny.4lima.de](https://sonny.4lima.de) remains the canonical source with the complete coverage and the current updates — use it as the first address and treat the mirror as an alternative when a specific tile set is more convenient to pull from there. The data is CC BY 4.0 and attributed to Sonny either way.

## Ortho Patches for Sceneries

Many sceneries — both default and third-party — were originally designed for X-Plane's old, flat mesh model. In the `apt.dat` file, the flag `flatten 1` may be set. This flag causes the scenery itself, and often a larger surrounding area, to be rendered completely flat. This is counterproductive to the goal of creating a highly accurate and realistic ground mesh with Ortho4XP.

For some sceneries, special Ortho patches exist, provided either by the developer or by active X-Plane users. With these patches, the mesh model generated by Ortho4XP can be specifically adapted to the respective scenery. Additionally, modifications to the scenery may allow it to work correctly without using `flatten 1`.

If no such modifications or patches are available, manually removing the line with `flatten 1` from the relevant `apt.dat` file can often help adapt the scenery to the new, detailed ground model. However, minor artifacts may occur, such as objects not sitting exactly on the ground, occasionally floating slightly above or being partially sunk into the terrain.

## Important Notes and Troubleshooting

### General Notes

- Ortho4XP requires significant storage space for generated textures
- The quality of orthophotos depends on the chosen imagery source
- Processing may take several hours depending on area size and zoom level
- The shred86 fork offers better performance and more features
- Using the binaries significantly simplifies installation

### Performance Optimization

- Processing time heavily depends on the chosen zoom level and area size
- Too high zoom levels can overload the system
- `skip_downloads` and `skip_converts` are useful for reprocessing individual steps, and are the basis of mesh-only builds
- Using an SSD can significantly reduce processing time

### File Size Optimization

As Ortho4XP generates large amounts of textures, storage requirements can quickly increase. ImageMagick scales the finished DDS textures down in place:

```bash
mogrify -resize 2048x2048 *.dds
```

Halving the edge length quarters the file size, and 2048x2048 is a reasonable compromise between visual quality and storage requirements. The compression format and the alpha channel survive the operation — a DXT1 texture stays DXT1, a masked DXT5 texture keeps its alpha — and ImageMagick rebuilds the full mipmap chain for the new size.

That last point is the one that matters: X-Plane's `LOAD_CENTER` mechanism picks a mipmap level by distance, so a texture rescaled without a complete chain would break distance-based resolution. Verify it after a batch run rather than assuming it — `magick identify -verbose file.dds` reports the mipmap count, which should be one level per halving down to 1x1.

### Troubleshooting

In case of problems:

1. Check the log files in the Ortho4XP directory
2. Ensure all Python dependencies are installed
3. Consult the [shred86 fork documentation](https://github.com/shred86/Ortho4XP/wiki)
4. Visit the [X-Plane Forum](https://forums.x-plane.org/index.php?/forums/forum/310-ortho4xp/)

---

## Further Reading

| Topic | Page | Focus |
|---|---|---|
| AutoOrtho | [AutoOrtho](../ortho_streaming/autoortho.md) | Streaming alternative to static generation |
| XEarthLayer | [XEarthLayer](../ortho_streaming/xearthlayer.md) | Rust-based streaming alternative |
| XPME | [XPME](../ortho_streaming/xpme.md) | Closed-source freemium streaming, conflicts with Ortho4XP tiles |
| How Streaming Works | [How Ortho Streaming Works](../ortho_streaming/how_streaming_works.md) | What the streaming layer contributes at runtime |
| Static + Streaming | [Static + Streaming](../ortho_streaming/static_plus_streaming.md) | Combining Ortho4XP with streaming solutions |
| Scenery Components | [How X-Plane Builds the World](../aufbau_quellen/scenery_components.md) | scenery_packs.ini load order |
| Orthophotography | [Concepts & Methods](orthophotography_intro.md) | Overview of static and streaming approaches |
| Filesystem | [Filesystem](../../linux/optimizations/filesystem.md) | SSD performance for tile generation and storage |

---

## Sources

- [Ortho4XP](https://github.com/oscarpilote/Ortho4XP) — Oscar Pilote, original project
- [Ortho4XP fork and wiki](https://github.com/shred86/Ortho4XP/wiki) — shred86, installation and usage documentation
- [OrthoForge](https://xpconnect.me/orthoforge.html) — xbard, independently developed successor
- [Pre-baked OSM tiles](https://xpconnect.me/orthoforge-data.html) — OrthoForge project, OSM and DEM mirrors
- [Sonny's LiDAR Digital Terrain Models](https://sonny.4lima.de) — Sonny, elevation datasets for Europe
- [Ortho4XP forum](https://forums.x-plane.org/index.php?/forums/forum/310-ortho4xp/) — X-Plane.org, community support
