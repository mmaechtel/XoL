### Important Parameters

All settings live in `Ortho4XP.cfg` in the Ortho4XP directory. When a tile is built, Ortho4XP writes the tile-specific subset of these keys into `Tiles/zOrtho4XP_+dd+ddd/Ortho4XP_+dd+ddd.cfg`, so an existing tile keeps the settings it was built with even if the global config changes later. The defaults below are the ones defined in `src/O4_Cfg_Vars.py`.

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

`min_angle` is the strongest single lever on mesh quality and one of the first values worth adjusting. Raising it forces better-shaped triangles and removes the thin slivers that cause shading artefacts and unstable runway surfaces; lowering it produces a coarser, cheaper mesh. Raising `min_angle` and lowering `curvature_tol` both increase the triangle count, so `limit_tris` acts as the ceiling — setting it explicitly is recommended whenever a high-resolution DEM is in use, because such a DEM can otherwise drive the triangle count far beyond what the tile needs.

**Roads**

| Parameter | Default | Description |
|---|---|---|
| `road_level` | `1` | How much of the OSM road network is levelled into the mesh, `0`–`5` |
| `road_banking_limit` | `0.5` | How much a road must be banked before it is levelled at all, in metres — measured as the height difference between a point on the road centreline and the nearest point at the road edge |
| `lane_width` | `4.0` | Width in metres used when buffering the road network for levelling |

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

`cover_extent` is the main lever on package size, and the useful range is wide — values from `0.5` to `6.0` are all plausible, a twelvefold difference in high-resolution area per airport. It also determines how often the scenery changes zoom level between the base texture and the airport texture.

**Masks and water**

| Parameter | Default | Description |
|---|---|---|
| `mask_zl` | `14` | Zoom level of the coastal transparency masks. Permitted values are only `14`, `15` and `16` |
| `masks_width` | `100` | Width of the mask transition zone, in metres. In older versions this was counted in ZL14 pixels, roughly a factor of 10 |
| `masking_mode` | `sand` | Which texture the mask blends towards — `sand`, `rocks` or `3steps` |
| `use_masks_for_inland` | `False` | Uses masks for inland water instead of the constant `ratio_water` transparency. Expensive in VRAM and, per the upstream hint, probably not worth the effort |
| `imprint_masks_to_dds` | `False` | Bakes the masks into the DDS textures. Doubles the file size of masked textures (DXT5 instead of DXT1) but lowers VRAM usage — a trade-off, not a clear improvement either way |
| `sea_smoothing_mode` | `zero` | How sea elevation is handled — see below |
| `water_smoothing` | `10` | Number of smoothing passes over inland water triangles |
| `ratio_water` | `0.25` | Transparency of the ortho overlay over inland water, `0`–`1`. At `0` the ortho image is fully opaque |
| `ratio_bathy` | `1.0` | Same principle for the bathymetry (sea bed) |
| `min_area` | `0.001` | Minimum size of a water body that is still modelled, in km². Contiguous water surfaces are merged **before** the area is computed |
| `max_area` | `200.0` | Water bodies above this size are masked like sea, in km² |
| `sea_texture_blur` | `0` | Blur radius in metres for layers of type `mask` in combined provider imagery, to tone down over-prominent wave and reflection patterns |
| `water_tech` | `XP11 + bathy` | Water rendering generation — set to `XP12` on X-Plane 12, see the callout below |

Inland water is drawn as a lower layer of X-Plane water with an ortho overlay of constant transparency on top; `ratio_water` controls that transparency. `masking_mode=3steps` turns the coastal transition into a staged one and expects `masks_width` as a list `[a,b,c]`, where `a` is the length in metres of a first transition from fully opaque imagery at the shoreline to `ratio_water` transparency, and `b` is the second transition zone.

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

    The setting is stored per tile, so tiles built before the change keep the old behaviour until they are rebuilt or their `Ortho4XP_+dd+ddd.cfg` is edited.

**Global settings versus per-tile settings**

Most of the parameters above are written into each tile's own config and can therefore differ from tile to tile. A few are only read from the global `Ortho4XP.cfg` and never appear in a tile config — among them `skip_downloads` and `skip_converts`, which suppress the imagery download and the DDS conversion. Both default to `False` and are the two settings that matter when Ortho4XP is used to produce mesh-only packages; see [Building packages for ortho streaming](#building-packages-for-ortho-streaming). Also global-only: `verbosity`, `cleaning_level`, `max_download_slots`, `max_convert_slots`, `overpass_server_choice`, `custom_scenery_dir`, `custom_overlay_src` and `custom_overlay_src_alternate`.

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

Every value moves in the direction of more detail: `curvature_tol=1.0` halves the tolerance and lets the mesh follow correspondingly finer terrain, `min_angle=15.0` keeps those extra triangles well-shaped, `mask_zl=16` is the finest permitted mask resolution and `masks_width=25` narrows the shoreline transition to match. `apt_smoothing_pix=4` blurs the elevation raster less over airports, so airport terrain keeps more of its real shape. `cover_zl=19` requires `mesh_zl` to be at least `19`. Build time and package size rise steeply; with a high-resolution `custom_dem`, add an explicit `limit_tris` so the triangle count stays bounded.

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

`curvature_tol=3.0` and `min_angle=5.0` both reduce the triangle count, and `mesh_zl=16` is the lowest permitted value, capping the imagery zoom level accordingly. `min_area=0.1` drops small ponds from the water model — a hundredfold increase over the default, which removes a large share of the water geometry and its masks. `cover_zl=16` matches the base zoom level plus one and `cover_extent=0.5` keeps the high-resolution zone minimal, so airports stay recognisable without adding much texture volume.

<!-- STREAMING PROFILE: wird separat eingefügt -->
