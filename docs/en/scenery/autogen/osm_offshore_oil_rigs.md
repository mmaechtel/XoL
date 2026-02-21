---
description: "OSM Offshore Oil Rigs places worldwide offshore oil platforms as heliports in X-Plane using OpenStreetMap position data."
---
# OSM Offshore Oil Rigs

OSM Offshore Oil Rigs is a scenery package for [X-Plane](../../glossary.md#x-plane) that places offshore oil platforms as heliports in oceans and seas worldwide. All position data is derived from the OpenStreetMap (OSM) database using the `man_made=offshore_platform` tag. The package uses X-Plane 12's built-in oil rig models — no custom 3D assets are included.

## Background

- **Type:** Scenery package (no plugin dependency)
- **Developer:** Saar Snagar (snagar.dev)
- **Distribution:** [x-plane.to](https://x-plane.to/file/1896/osm-offshore-oil-rigs) (Freeware)
- **Platforms:** Windows, macOS, Linux (standard scenery folder, platform-independent)
- **Compatibility:** X-Plane 12

The package is script-generated using the author's open-source [osm_to_xplane_dist](https://github.com/snagar/osm_to_xplane_dist) Python tool. At only 298 KB, it consists entirely of `apt.dat` heliport definitions and [DSF](../../glossary.md#dsf-distribution-scenery-format) references — each oil rig is registered as a heliport with coordinates, heading, and helipad dimensions derived from OSM.

??? abstract "Technical Background: apt.dat Heliport Format"

    X-Plane represents heliports in `apt.dat` files using Row Code 17 (heliport header) and Row Code 102 (helipad definition). Each helipad entry specifies latitude and longitude (8 decimal places), true heading, dimensions in meters, and surface type. The format supports an `is_oilrig` metadata key (Row Code 1302) to identify oil platform heliports specifically. The generation script extracts OSM nodes tagged `man_made=offshore_platform`, converts their coordinates, and filters against existing X-Plane oil rig positions to minimize overlaps.

## Features

- **Worldwide coverage** — oil platforms placed wherever OSM contains `man_made=offshore_platform` entries
- **OSM-based positioning** — real-world coordinates from the OpenStreetMap database
- **Mission-X integration** — oil rigs serve as helicopter mission targets for the [Mission-X](https://x-plane.to/file/135/mission-x) plugin (same author), enabling random cargo, medevac, and helicopter supply missions to offshore platforms
- **Minimal footprint** — 298 KB total, no custom 3D models, no plugin dependency

!!! note "OSM Data Coverage"

    OpenStreetMap coverage for offshore platforms varies by region. The North Sea (UK, Norway) and Gulf of Mexico are well-mapped due to active communities and public government data (e.g., the U.S. Bureau of Safety and Environmental Enforcement). Other regions — Persian Gulf, Southeast Asia, West Africa — have fewer entries despite high real-world platform density.

## Value in Flight Simulation

X-Plane's default scenery includes only a limited number of offshore oil platforms. For helicopter pilots, realistic offshore operations require destinations at real-world positions — oil rigs as approach targets for supply, crew transfer, and emergency missions. This package fills the gap by placing heliports at OSM-documented platform locations worldwide. Combined with Mission-X, it enables procedural helicopter missions to offshore targets. On Linux, the package installs as a standard scenery folder without plugin dependencies.

## Installation

**Download:** [x-plane.to](https://x-plane.to/file/1896/osm-offshore-oil-rigs)

1. Extract the contents into `X-Plane 12/`[Custom Scenery](../../glossary.md#custom-scenery)`/`
2. Launch and quit X-Plane to register the scenery in [scenery_packs.ini](../../glossary.md#scenery_packsini)
3. For manual ordering, place the entry **below** [GLOBAL_AIRPORTS](../../glossary.md#global-airports) to avoid overriding higher-quality airport scenery

**Mission-X users:** After installation, run **APT Data Optimization** from the Mission-X Setup screen to index the new heliports for mission generation.

!!! tip "Overlap Handling"

    The generation script filters against existing X-Plane oil rig positions, but some overlaps may remain. The author accepts reports of duplicate positions via the distribution page.

---

## Further Reading

| Topic | Page | Focus |
|---|---|---|
| Scenery Components | [How X-Plane Builds the World](../aufbau_quellen/scenery_components.md) | scenery_packs.ini load order and layer interaction |
| Scenery Sources | [Sources](../aufbau_quellen/scenery_sources.md) | Overview of scenery providers and databases |

---

## Sources

- [OSM Offshore Oil Rigs — x-plane.to](https://x-plane.to/file/1896/osm-offshore-oil-rigs)
- [osm_to_xplane_dist — GitHub](https://github.com/snagar/osm_to_xplane_dist)
- [Mission-X — x-plane.to](https://x-plane.to/file/135/mission-x)
- [Tag:man_made=offshore_platform — OpenStreetMap Wiki](https://wiki.openstreetmap.org/wiki/Tag:man_made=offshore_platform)
