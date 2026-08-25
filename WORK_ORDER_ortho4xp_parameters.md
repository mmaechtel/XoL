# Work Order — Rework the Ortho4XP parameter documentation

**Files:** `docs/en/scenery/orthophotography/ortho4xp.md` (lead) and
`docs/de/scenery/orthophotography/ortho4xp.md` (mirror), 245 lines each.

**Goal:** turn the parameter section into a page that can be handed to a
scenery-package author as a reference — specifically the XEarthLayer developer,
who builds ortho packages for a streaming setup. Today the page cannot serve
that purpose: several documented defaults are wrong, two parameter names do not
exist, and the entire group of settings that matters for streaming is absent.

**Read first:** `docs/MARKDOWN_RULES.txt`, `SKILL_RULES.md`, `CLAUDE.md`.
EN is the lead version, DE is aligned afterwards, formatting identical in both.

---

## 1. Verified factual errors — fix these

All values below were read from the Ortho4XP source of the local install,
`/mnt/xplane_data/docker/Ortho4XP/src/O4_Cfg_Vars.py`, and cross-checked against
three real configs in production use. Verify them again against the source
before editing; do not take this table on trust.

### Parameter names that do not exist

| Page says | Reality |
|---|---|
| `zoomlevel` | The config key is **`default_zl`** (default `16`). `zoomlevel` appears in the code as an internal variable but is not a config key and cannot be set in `Ortho4XP.cfg`. |
| `provider` | **No such key.** The imagery source is **`default_website`** (default `""`, e.g. `BI`). |

Both appear in the parameter table and in all three "Recommended Settings"
profiles. Anyone copying them into a config file gets settings that are
silently ignored.

### Wrong default values in the parameter table

| Parameter | Page says | Actual default |
|---|---|---|
| `mesh_zl` | `16` | **`19`** |
| `curvature_tol` | `3.0` | **`2.0`** |
| `mask_zl` | `16` | **`14`** |
| `road_level` | `2` | **`1`** |
| `water_smoothing` | `3` | **`10`** |
| `road_banking_limit` | `0.3` | **`0.5`** |

Correct: `min_area` `0.001`, `apt_smoothing_pix` `8`.

`custom_build_dir` and `custom_overlay_dir` could not be found as config keys at
all — check whether they still exist in the current version, and drop them if
not.

## 2. Missing parameters that belong on the page

### The single most consequential omission: `min_angle`

Default `10.0`. It sets the minimum triangle angle in the mesh and is one of the
strongest levers on mesh quality — yet it is not mentioned anywhere. Document it
and note it is a common first adjustment.

### X-Plane 12 relevance: `water_tech`

Default is **`XP11 + bathy`**. For X-Plane 12 this must be set to `XP12`. All
three production configs examined set it explicitly. A reader on X-Plane 12 who
leaves the default gets X-Plane 11 water behaviour. This deserves its own
callout, not a table row.

### Terrain appearance

| Parameter | Default | Note |
|---|---|---|
| `terrain_casts_shadows` | `True` | |
| `use_decal_on_terrain` | `False` | Production configs set `True`; worth stating that the default is off. |
| `normal_map_strength` | `1.0` | |

### High-resolution airport coverage

| Parameter | Default | Note |
|---|---|---|
| `cover_airports_with_highres` | `"False"` | `ICAO` restricts high-res coverage to ICAO airports. |
| `cover_zl` | `18` | |
| `cover_extent` | `1.0` | Radius in km. Observed range in production configs: `0.5` to `6.0` — a twelvefold difference in high-res area. This is the main lever on package size and on how much zoom-level mixing the scenery contains. |

### Masks and water

| Parameter | Default |
|---|---|
| `masking_mode` | `"sand"` |
| `masks_width` | `100` |
| `imprint_masks_to_dds` | `False` |
| `sea_smoothing_mode` | `"zero"` |
| `ratio_water` | `0.25` |
| `limit_tris` | `3.0` |

### Elevation

`custom_dem` (default `""`) — path to an external elevation dataset. This is
what distinguishes a build using high-quality DEM data from a stock build. Worth
a sentence; the path is region-specific and must be obtained separately.

## 3. New section: building packages for ortho streaming

This is the part that makes the page referenceable for a streaming-package
author, and it does not exist today.

The key point: with ortho streaming the textures are generated on demand at
runtime, so Ortho4XP only needs to produce **mesh and terrain definitions** — no
imagery download, no DDS conversion. Two settings do this:

```
skip_downloads=True
skip_converts=True
```

Both default to `False`. Without them, a package build downloads and converts
gigabytes of imagery that is then discarded. Add `imprint_masks_to_dds=False`
(already the default) — baking masks into DDS files is pointless when the DDS
files are generated elsewhere.

Note these two are **global** settings in `Ortho4XP.cfg`, not per-tile settings,
so they do not appear in the per-tile `Ortho4XP_+dd+ddd.cfg` files.

Cross-link this section to `docs/{lang}/scenery/ortho_streaming/` and from those
pages back here.

## 4. Rework the "Recommended Settings" profiles

The three profiles (Standard / High-Resolution / Performance-Optimized) use the
two non-existent keys and are therefore not copy-pasteable. Rewrite them with
real key names, and add a fourth profile for streaming packages:

```
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

Rationale to state in the text, honestly:

- `default_zl=16` as a base keeps package size and tile count manageable, and a
  streaming layer regenerates the imagery anyway.
- `cover_zl=17` with `cover_extent=0.5` keeps the high-resolution zone one step
  above the base rather than two, and small. Fewer and gentler scale changes
  across the scenery.
- **Do not present this as a fix for visual artefacts.** A striping/terracing
  artefact on distant slopes was investigated at length in mid-2026 and traced
  to a texture encoder emitting an incomplete mipmap chain, not to zoom-level
  mixing. Zoom-level choices affect package size and where scale changes occur;
  they were not the cause. If the page touches this at all, say so plainly.

## 5. Constraints

- **EN first**, then align DE. Identical structure and formatting in both.
- Apply `docs/MARKDOWN_RULES.txt` — blank line after every heading including
  bold pseudo-headings, no trailing colons on headings followed by a list,
  4-space list indentation, `ini` code blocks for config snippets.
- Do not add the page to navigation — it already exists in `mkdocs.yml`.
- German uses the impersonal style (infinitive, passive), no "Sie".
- Sources section: official Ortho4XP sources only, 2024 or newer, 5-8 entries.
- Only Linux specifics where platform matters; the existing Windows/macOS
  file-size subsections predate that rule — leave them unless they conflict.
- Changelog in `docs/{lang}/index.md` **last**, one compressed entry, newest
  block on top, maximum three date blocks retained.

## 6. Verification before finishing

1. Re-read every default from `O4_Cfg_Vars.py` in the current Ortho4XP source.
   Do not rely on this work order — it was written against one local install and
   the upstream defaults may differ by version.
2. Confirm `zoomlevel` and `provider` really are not config keys, by grepping the
   config parser rather than the whole tree.
3. Check that every parameter named in a "Recommended Settings" profile actually
   appears in a real generated `Ortho4XP_+dd+ddd.cfg`.
4. `mkdocs build` must complete without warnings.
5. Diff EN against DE structurally — same headings, same tables, same order.

## 7. Out of scope

- The LiDAR integration section.
- The Ortho Patches section.
- Installation and version sections, beyond correcting anything that contradicts
  the parameter rework.
