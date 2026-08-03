<!-- BLOCK 1 — new section. Placement: after "### Recommended Settings" (i.e. after the
     fourth profile from BLOCK 2), before "## LiDAR Data Integration". Preceded by a `---`. -->

---

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

A `.ter` file from a tile built with `skip_downloads=True` and `skip_converts=True` looks like this:

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

The `BASE_TEX_NOWRAP` path names the exact DDS file the streaming layer has to deliver at runtime — provider code and zoom level are part of the filename (`_BI17.dds`). The package does not merely suggest a resolution; it demands one specific file per terrain definition. That is why the zoom-level choice is not arbitrary in a build without imagery, and why `default_website` must match what the streaming layer actually serves: a package built with `BI` asks for `_BI17.dds`, and a layer configured for a different provider will not answer that name.

The same tile shows what `cover_zl` does to that contract. Of its 752 `.ter` files, 559 reference `_BI17` and 193 reference `_BI18` — the base zoom level across most of the tile, the higher cover zoom level confined to the airport surroundings. Those are numbers from one observed tile, an illustration of the mechanism rather than a target ratio; the split depends entirely on `cover_extent` and on how many airports the tile contains. Its `textures/` directory holds 118 files against those 752 terrain definitions, which is the expected picture of a mesh-only build: terrain definitions complete, imagery largely absent.

The mesh parameters (`mesh_zl`, `min_angle`, `curvature_tol`, `limit_tris`) and the mask parameters (`mask_zl`, `masks_width`, `masking_mode`) keep their full effect, because mesh and masks are exactly what the package contains.

### Values Observed in Production Configs

The profile below is a conservative starting point. Real configurations in productive use with a streaming layer sit well away from it in places — the following values were observed in a working XEarthLayer setup:

| Parameter | Streaming profile | Observed in production |
|---|---|---|
| `cover_extent` | `0.5` | `6.0` |
| `cover_zl` | `17` | `18` |
| `mask_zl` | `14` (default) | `16` |
| `masking_mode` | `sand` (default) | `rocks` |
| `ratio_water` | `0.25` (default) | `0.5` |
| `road_level` | `1` (default) | `3` |
| `masks_width` | `100` (default) | `25` |

The widest spread is in `cover_extent`, the radius in kilometres around an airport that receives high-resolution coverage. Between `0.5` and `6.0` km the covered area grows roughly twelvefold in radius and far more in surface, which makes it the single strongest lever on package size and on the number of high-resolution texture requests a busy terminal area produces. `0.5` keeps packages small and is a reasonable default for wide-area coverage; `6.0` is a choice for a setup where a handful of home airports matter more than total package size.

The remaining differences follow the same logic: a higher `mask_zl` with a narrower `masks_width` produces finer but tighter coastlines, `masking_mode=rocks` suits alpine and rocky shorelines better than the `sand` default, and `road_level=3` adds secondary road networks at the cost of more vector data per tile.

!!! note "No measured figures"

    These are configuration values seen in practice, not benchmark results. No package-size or frame-rate measurements were taken for this comparison, so the effects described here are directional, not quantified.

`cover_zl=17` on a `default_zl=16` base keeps the high-resolution zone one step above the base rather than two, so the scenery contains fewer and gentler scale changes. That is a package-size and consistency argument, not a remedy for visual artefacts — those usually originate in texture encoding rather than in the scenery package, and no zoom-level choice removes them.

### Where the Package Goes

How the finished tiles are placed alongside a streaming mount, and in which order they have to appear in `scenery_packs.ini`, is covered separately:

- [Static + Streaming](../ortho_streaming/static_plus_streaming.md) — consolidating mesh-only tiles into a single directory and setting the load order
- [XEarthLayer](../ortho_streaming/xearthlayer.md) — the regional DSF/TER packages this build process produces, and how they are installed
- [How Ortho Streaming Works](../ortho_streaming/how_streaming_works.md) — what the streaming layer contributes at runtime

---

<!-- BLOCK 2 — fourth profile. Placement: under "### Recommended Settings",
     after "#### Performance-Optimized Settings". -->

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

`default_zl=16` as the base keeps package size and tile count manageable; the streaming layer regenerates the imagery at runtime anyway, so a higher base zoom level buys nothing at build time. `cover_zl=17` with `cover_extent=0.5` keeps the high-resolution zone one step above the base instead of two, and keeps it small. `default_website=BI` is not merely informational here: the provider code is written into every texture filename the terrain definitions request (`..._BI17.dds`), so it has to match what the streaming layer serves. `water_tech=XP12` is mandatory on X-Plane 12 regardless of profile. `skip_downloads` and `skip_converts` are the two settings that turn a normal build into a mesh-and-terrain-only build — see [Building Packages for Ortho Streaming](#building-packages-for-ortho-streaming).

<!-- RUECKLINKS -->

## Missing back-links into this section

To be set by whoever edits `docs/{lang}/scenery/ortho_streaming/` — none of these exist today:

Nothing in `ortho_streaming/` was changed by this draft. The items below are for whoever
edits those pages.

1. `ortho_streaming/static_plus_streaming.md`, section "Ortho4XP Settings for Mesh-Only Generation" — **strongest content overlap, must be resolved rather than left duplicated.** Concretely:
    - Lines 67–77: the introductory sentence and the six-row parameter table. Replace with a one-sentence pointer to `../orthophotography/ortho4xp.md#building-packages-for-ortho-streaming`, which now holds the authoritative parameter facts.
    - Line 78 ("The remaining parameters are detailed in the Ortho4XP chapter") already links to the page root and becomes redundant once the deep link is in place — fold the two together.
    - **Check before rewriting:** the table rows "Build Mesh", "Build Overlays", "Build Imagery" and "Mesh level 1–2" have **no counterpart in `O4_Cfg_Vars.py`**. They are presumably GUI build-step checkboxes rather than config keys, and "Mesh level 1–2" does not correspond to `mesh_zl` (default `19`) or to any other key found. Verify what these refer to in the current Ortho4XP UI before deciding whether to keep, reword or drop them — do not silently delete a row that describes a real GUI control, and do not carry an invented parameter forward into the new section.
2. `ortho_streaming/static_plus_streaming.md`, "Further Reading" table (line 122), Ortho4XP row — points at the page root; deep-link to the new section instead.
3. `ortho_streaming/xearthlayer.md`, section "Regional Packages" (lines 129–144) — states the packages are Ortho4XP-based DSF/TER packages but does not say how such a package is built. Add a link to `../orthophotography/ortho4xp.md#building-packages-for-ortho-streaming`.
4. `ortho_streaming/xearthlayer.md`, "Further Reading" table (line 210), Ortho4XP row — described as "Static ortho tile generation for offline use", which is the opposite of the streaming use case. Reword and point at the new section.
5. `ortho_streaming/index.md` — the intro paragraph mentions combining with local Ortho4XP tiles but has no link into `orthophotography/`. A bullet or sentence pointing at the new section would close the loop.

## To verify at assembly time

- The anchor `../ortho_streaming/how_streaming_works.md#dds-compression`, used in the artefact subsection, is unverified. It was taken from the `### DDS Compression` heading at line 149 of that file. Confirm with `mkdocs build`.
- The anchor `#building-packages-for-ortho-streaming`, used in the fourth profile and in the back-link items above, depends on the exact final heading text.
