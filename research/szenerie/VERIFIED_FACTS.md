# Verifizierte Fakten (Quelle: /mnt/xplane_data/docker/Ortho4XP/src/O4_Cfg_Vars.py, Stand 2026-05-02)

NICHT erneut recherchieren — diese Werte sind bereits am Quellcode verifiziert.

## Existiert NICHT als Config-Key

`zoomlevel` (nur als Wort in hint-Texten), `provider`, `custom_build_dir`, `custom_overlay_dir`.
Ersatz: `default_zl` (Zoomlevel), `default_website` (Bildquelle).

## Defaults aus O4_Cfg_Vars.py

```
verbosity = 1
cleaning_level = 1
skip_downloads = False
skip_converts = False
max_download_slots = 1
max_convert_slots = 4
custom_scenery_dir = ""
custom_overlay_src = ""
custom_overlay_src_alternate = ""
apt_smoothing_pix = 8
road_level = 1
road_banking_limit = 0.5
lane_width = 4.0
min_area = 0.001
max_area = 200.0
mesh_zl = 19
curvature_tol = 2.0
apt_curv_tol = 0.5
apt_curv_ext = 0.5
coast_curv_tol = 1.0
coast_curv_ext = 0.5
limit_tris = 3.0
min_angle = 10.0
sea_smoothing_mode = "zero"
water_smoothing = 10
mask_zl = 14
masks_width = 100
masking_mode = "sand"
use_masks_for_inland = False
imprint_masks_to_dds = False
default_website = ""
default_zl = 16
cover_airports_with_highres = "False"
cover_extent = 1.0
cover_zl = 18
water_tech = "XP11 + bathy"
ratio_water = 0.25
ratio_bathy = 1.0
normal_map_strength = 1.0
terrain_casts_shadows = True
overlay_lod = 25000
use_decal_on_terrain = False
custom_dem = ""
fill_nodata = True
```

## Per-Tile vs. global

Die generierte `Tiles/zOrtho4XP_+dd+ddd/Ortho4XP_+dd+ddd.cfg` enthält diese Keys
(alle anderen sind ausschliesslich global in `Ortho4XP.cfg`):

apt_smoothing_pix, road_level, road_banking_limit, lane_width, max_levelled_segs,
water_simplification, min_area, max_area, clean_bad_geometries, mesh_zl, curvature_tol,
apt_curv_tol, apt_curv_ext, coast_curv_tol, coast_curv_ext, limit_tris, min_angle,
sea_smoothing_mode, water_smoothing, iterate, mask_zl, masks_width, masking_mode,
use_masks_for_inland, imprint_masks_to_dds, distance_masks_too, masks_use_DEM_too,
masks_custom_extent, cover_airports_with_highres, cover_extent, cover_zl, water_tech,
ratio_bathy, ratio_water, overlay_lod, sea_texture_blur, normal_map_strength,
terrain_casts_shadows, use_decal_on_terrain, custom_dem, fill_nodata, default_website,
default_zl, zone_list

**Bestätigt: `skip_downloads` und `skip_converts` sind NICHT per-Tile, nur global.**
Ebenso global: verbosity, cleaning_level, overpass_server_choice, max_download_slots,
max_convert_slots, check_tms_response, http_timeout, max_connect_retries,
max_baddata_retries, ovl_exclude_pol, ovl_exclude_net, custom_scenery_dir,
custom_overlay_src, custom_overlay_src_alternate.

## Reale Produktiv-Config (Streaming-Setup, XEarthLayer)

```
road_level=3        min_area=0.01       mesh_zl=19        curvature_tol=2.0
mask_zl=16          masks_width=25      masking_mode=rocks
use_masks_for_inland=True   distance_masks_too=True   imprint_masks_to_dds=False
cover_airports_with_highres=ICAO   cover_extent=6.0   cover_zl=18
water_tech=XP12     ratio_water=0.5    use_decal_on_terrain=True
skip_downloads=True skip_converts=True overpass_server_choice=DE
custom_overlay_src=<Pfad zur X-Plane 12 Global Scenery>
```

## OrthoForge / XPConnect (WebFetch 2026-08-03)

- OrthoForge-Seite: https://xpconnect.me/orthoforge/index.html
  (die auf der Seite bisher verlinkte URL https://xpconnect.me/orthoforge.html
  ist die von der Startseite referenzierte Variante — beide prüfen)
- Repo: https://codeberg.org/xbard/OrthoForge — GPL v3, Maintainer: xbard
- Aktuelle Version laut Website: v1.1
- Abstammung: englischer Fork von Roland (Ypsos)' Ortho4XP V3, inzwischen
  unabhängig, kein Upstream-Sync mehr. Credits: Oscar Pilote (Ortho4XP),
  Shred86 (1.40er-Linie), Roland/Ypsos (V3-Architektur)
- Plattformen: Linux, macOS, Windows über Python-3-venv; Linux-Prereqs über
  mitgelieferte Skripte oder Paketmanager (Fedora, Debian/Ubuntu, Arch)
- Features laut Website: pre-baked OSM-Daten + DEM-Mirrors (umgeht Rate-Limits),
  getrennte Land-/Seabed-Höhenquellen, progressive Airport-Zoomlevel nach
  Sehschärfe, Frozen-Water-Option, Xroads-Autogen-Roads-Tweaker (Linksverkehr),
  Farbnormalisierung, XP12-Terrain-Roughness, Auto-Backups mit Rollback,
  11-sprachiger Launcher, Security-Hardening (kein exec/eval, HMAC, TLS)
- XPConnect selbst = Multiplayer-Plattform für XP12 (Plugin, Live-ATC, Voice,
  Forum, Gallery). **Nicht Scope dieser Aufgabe** — nur die ortho-relevanten
  Dienste sind relevant:
    - https://xpconnect.me/orthoforge-data.html — Pre-baked OSM-Tiles
    - https://xpconnect.me/sonny.html — Sonny LiDAR DTM, UK/Irland
