# Draft C — OrthoForge and the ortho-related xpconnect.me services (EN)

Target file: `docs/en/scenery/orthophotography/ortho4xp.md`

Three separate building blocks. Each is marked with its insertion point.

---

<!-- BAUSTEIN 1 -->

**Insertion point:** replaces list item 3 under `## Installation and Versions`
(current lines 24-29, `3. **OrthoForge** (independently developed successor):`).

The numbered list ends with this item, so the warning box, the table and the two
`**bold**` blocks below follow *after* the list, at section level — they do not sit
inside item 3 and therefore cannot break its numbering.

```markdown
3. **OrthoForge** (independently developed successor):
    * [Project page and documentation](https://xpconnect.me/orthoforge.html) — GPL v3,
      maintained by xbard
    * Started as the English fork of Roland (Ypsos)'s ORTHO4XP_V3 and is now developed
      independently; changes are no longer synchronised with any upstream Ortho4XP branch.
      The project credits Oscar Pilote (original Ortho4XP), shred86 (1.40 line) and
      Roland/Ypsos (V3 architecture).
    * Targets X-Plane 12 — the XP12 water and material paths are the default, not an option

!!! warning "The source repository is being retired"
    The Codeberg repository states: *"Due to changes in Codeberg policy, this repo will
    soon be deleted and hosted at https://xpconnect.me/orthoforge.html"*. Use the project
    page as the entry point; any Codeberg link will break without notice.

**What is relevant on Linux**

The differences that actually change a build are these:

| Area | What OrthoForge does differently |
|---|---|
| OSM download | Can pull pre-baked OpenStreetMap layers from a mirror instead of querying Overpass, which removes the rate-limit stalls that dominate large batch builds (see [Pre-baked OSM and DEM data](#pre-baked-osm-and-dem-data) below) |
| Elevation | Land and seabed elevation are configured as separate sources (`custom_dem_search_dirs` / `custom_bathy_search_dirs`), so a high-resolution land DTM no longer has to be reconciled with bathymetry in one dataset |
| Airports | Airport coverage zoom is graduated rather than a single `cover_zl` step, driven by screen resolution and field of view |
| XP12 terrain | Exposes the XP12 material parameters, including terrain roughness, in the tile configuration |

**Setup on Linux**

* `OrthoForge_Setup_Linux.sh` runs a guided setup; `setup_venv.sh` is the plain-shell
  alternative for distributions with a locked-down system pip (PEP 668) and needs no root
* The build runs from a Python 3 virtual environment created with `--system-site-packages`,
  so it inherits system-installed tkinter and the optional GDAL bindings instead of
  rebuilding them; the remaining dependencies come from `requirements.txt`
* Distribution packages needed beforehand: tkinter and Pillow's Tk bindings. GDAL is
  optional — the elevation path prefers rasterio and works without the osgeo bindings
* Setup is documented for Fedora, Debian/Ubuntu, Arch and openSUSE Tumbleweed
```

**Notes on wording**

* Codeberg is no longer linked at all. The retirement notice is quoted verbatim, so the
  reader can find the successor host even if the repository is already gone. If the
  repository is wanted as a secondary link anyway, it belongs inside the warning box, not
  in the bullet list.
* Version number v1.1 deliberately omitted (CLAUDE.md "Versionsnummern minimieren").
* No Python version number in the prose — see the evidence note below; the setup scripts
  pick an interpreter themselves, so the number has no practical consequence for the reader.
* The 11-language launcher, the Qt/Tk theme picker and the gallery are marketing surface
  and are left out entirely; the Xroads road tweaker and frozen-water option are left out
  as well, since neither is Linux-specific and both would need their own explanation.
* The anchor `#pre-baked-osm-and-dem-data` refers to the new subsection from Baustein 3.

**Evidence — Python version (decision needed)**

The documentation *does* state a minimum verbatim, in the "System requirements" table on
<https://xpconnect.me/orthoforge/installation.html>:

> Python | 3.10 | 3.12 or 3.13 (3.14 also works, see note)

(column headers: Minimum | Recommended). Verified against the raw HTML, not only via a
summarising fetch. Two further verbatim statements from the same page:

> OrthoForge is smoke-tested on Fedora 44 with Python 3.13.

> `./setup_venv.sh # prefers python3.13, then 3.12, then python3`

So "Python 3.10 minimum" is quotable, and the source is the surviving host, not the dying
repository. It is nevertheless left out of the draft above because the setup scripts
resolve the interpreter themselves and a reader never has to act on the number.
Re-adding it is a one-line change if wanted.

---

<!-- BAUSTEIN 2 -->

**Insertion point:** directly after the `### Important Parameters` table
(current line 83, after the `min_area` row), before `### Recommended Settings`.

```markdown
!!! warning "Same key names in OrthoForge — different defaults"
    OrthoForge keeps the Ortho4XP key names unchanged (`default_zl`, `default_website`,
    `mesh_zl`, `mask_zl`, `curvature_tol`, `cover_zl`, `road_level`, `water_tech`,
    `custom_dem` and the rest) and only adds keys on top. The values documented on this
    page therefore transfer — but they are not what OrthoForge is set to. Its shipped
    configuration starts from a far more aggressive baseline:

    | Key | Ortho4XP default | OrthoForge default |
    |---|---|---|
    | `default_zl` | 16 | 18 |
    | `mesh_zl` | 19 | 20 |
    | `mask_zl` | 14 | 18 |
    | `cover_zl` | 18 | 19 |
    | `water_tech` | `XP11 + bathy` | `XP12` |

    Read the tables on this page as *what the parameter does*, not as *what it is set to*.
    Anyone moving between the two tools should check the actual values in the running
    configuration — the OrthoForge baseline means noticeably longer build times and
    larger tiles than the numbers here suggest.
```

**Evidence**

Verified against `OrthoForge.cfg.example` in the repository (98 keys, fetched raw) and the
`cfg-reference.html` page of the project documentation (121 keys). Confirmed identical key
names: `verbosity`, `cleaning_level`, `overpass_server_choice`, `skip_downloads`,
`skip_converts`, `max_convert_slots`, `custom_scenery_dir`, `custom_overlay_src`,
`apt_smoothing_pix`, `road_level`, `road_banking_limit`, `lane_width`,
`max_levelled_segs`, `min_area`, `max_area`, `mesh_zl`, `curvature_tol`,
`apt_curv_tol`, `apt_curv_ext`, `coast_curv_tol`, `coast_curv_ext`, `limit_tris`,
`min_angle`, `sea_smoothing_mode`, `water_smoothing`, `iterate`, `mask_zl`,
`masks_width`, `masking_mode`, `use_masks_for_inland`, `imprint_masks_to_dds`,
`distance_masks_too`, `masks_use_DEM_too`, `masks_custom_extent`,
`cover_airports_with_highres`, `cover_extent`, `cover_zl`, `water_tech`,
`ratio_bathy`, `ratio_water`, `overlay_lod`, `sea_texture_blur`,
`normal_map_strength`, `terrain_casts_shadows`, `use_decal_on_terrain`,
`custom_dem`, `fill_nodata`, `default_website`, `default_zl`, `zone_list`.

Not present in Ortho4XP: `custom_dem_search_dirs`, `custom_bathy_search_dirs`,
`osm_data_source`, `dem_data_source`, `bathy_data_source`, `coastal_foam_*`,
`cnorm_*`, `water_tint_*`, `xroads_*`, `frozen_water`, `terrain_super_roughness`,
`gpu_acceleration`, `link_after_build`, `colour_reference_cube`.

Further differing defaults, not shown in the box to keep it readable
(Ortho4XP → OrthoForge): `curvature_tol` 2.0 → 1.0, `limit_tris` 3.0 → 50.0,
`min_angle` 10.0 → 0.5, `road_level` 1 → 3, `apt_smoothing_pix` 8 → 16,
`cover_extent` 1.0 → 5.0, `ratio_water` 0.25 → 0.75, `overlay_lod` 25000 → 15000,
`use_masks_for_inland` False → True, `imprint_masks_to_dds` False → True,
`use_decal_on_terrain` False → True, `fill_nodata` True → False,
`default_website` "" → `BI`, `sea_smoothing_mode` zero → mean, `water_smoothing` 10 → 2,
`masks_width` 100 → `[25]`, `max_area` 200.0 → 101.0, `lane_width` 4.0 → 2.0,
`cover_airports_with_highres` "False" → True.

Ortho4XP side of the comparison from `O4_Cfg_Vars.py` (VERIFIED_FACTS.md);
OrthoForge side from `OrthoForge.cfg.example`.

---

<!-- BAUSTEIN 3 -->

**Insertion point:** inside `## LiDAR Data Integration`. The existing
`### Available LiDAR Data` block about sonny.4lima.de and the `### Integration Steps`
stay as they are; the following is added as a new subsection **after**
`### Integration Steps` and its closing `!!! note "Note"` box (current line 188),
before `## Ortho Patches for Sceneries`.

```markdown
### Pre-baked OSM and DEM Data

The OrthoForge project runs two supporting services that are useful independently of
which builder is in use. Both are free and need no account.

**Pre-baked OpenStreetMap tiles**

* Ready-made OSM vector layers (airports, roads, coastline, water) in Ortho4XP's own
  cache format, at maximum road detail so they can still be filtered down locally
* Coverage is incomplete and grows over time, Europe first; tiles outside the baked
  area fall back to a normal Overpass query
* Delivered as bzip2-compressed OSM XML under `OSM_data/<block>/<tile>/`. For Ortho4XP,
  the files are dropped into `OSM_data` unchanged — not renamed, not unpacked — and the
  builder picks them up instead of calling Overpass. OrthoForge fetches them during the
  build once the pre-baked source is enabled in its configuration
* Data remains © OpenStreetMap contributors, ODbL
* [Pre-baked OSM tiles](https://xpconnect.me/orthoforge-data.html)

**Sonny DTM mirror**

The same site hosts an authorised mirror of Sonny's elevation data, offered as standard
SRTM-style `.hgt` tiles at 3″, 1″ and — for the United States, rebuilt from USGS 3DEP —
0.5″. Ortho4XP uses these exactly like the originals: unpack into `Elevation_data`, as
described above. OrthoForge can point at them through `custom_dem_search_dirs` or fetch
them with its own download helper.

!!! tip "Which Sonny source to use"
    The mirror is a convenience copy limited to what the OrthoForge project has staged.
    [sonny.4lima.de](https://sonny.4lima.de) remains the canonical source with the
    complete coverage and the current updates — use it as the first address and treat
    the mirror as an alternative when a specific tile set is more convenient to pull
    from there. The data is CC BY 4.0 and attributed to Sonny either way.
```

**Notes on wording**

* The existing sonny.4lima.de text is untouched; the mirror is explicitly subordinated
  to it so the primary source keeps its position.
* The US 0.5″ tiles are not Sonny's data but the project's own USGS 3DEP bakes — worded
  accordingly ("rebuilt from USGS 3DEP") rather than attributed to Sonny.
* No coverage numbers or file counts are quoted; the pre-baked set is explicitly a
  moving target.
