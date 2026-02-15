# XRoads

[XRoads](../glossary.md#xroads) is a scenery library for [X-Plane](../glossary.md#x-plane) 11 & 12 that hides standard road polygons in [Ortho4XP](../glossary.md#ortho4xp) orthophotos, making the actual roads from satellite images visible.

## Background

- **Type:** Scenery library (not a plugin)
- **Repository:** [github.com/melbo911/xroads](https://github.com/melbo911/xroads)
- **Source:** [forums.x-plane.org](https://forums.x-plane.org/index.php?/files/file/67227-xroads-transparent-roads-for-ortho4xp/) (community project)
- **Platforms:** Windows, macOS, Linux
- **Compatibility:** X-Plane 11 and X-Plane 12
- **Price:** Free

## Features

- **Transparent roads:** Hides road polygons from OSM databases, particularly for ZL17+ [orthophotos](../glossary.md#orthophotos)
- **Selective display:** Bridges, highways, expressways, and railway tracks remain visible
- **AI vehicle speed:** Reduced to 70% (adjustable via the `-v` parameter) for more realistic traffic conditions
- **Automatic library.txt:** Enables targeted control of transparent roads
- **Autogen fallback:** In areas without ortho tiles, standard roads remain visible

## Value in Flight Simulation

With ortho scenery at zoom level 17 or higher, the roads in the satellite imagery are detailed enough that the autogen road polygons overlaid by X-Plane become distracting — they often sit slightly offset from the real roads. XRoads solves this by making the overlaid polygons transparent. Bridges and highways are preserved, as they are often hard to distinguish in satellite imagery.

## Installation

**Download:** [XRoads](https://forums.x-plane.org/index.php?/files/file/67227-xroads-transparent-roads-for-ortho4xp/)

### Compiling on Linux

XRoads is distributed as source code and needs to be compiled on Linux. Prerequisites are `make` and a C compiler:

```bash
sudo apt install build-essential
```

Then in the XRoads directory:

```bash
make xroads
```

The generated executable is then applied to the ortho scenery to generate the `library.txt`. The resulting library is placed as a scenery folder in `Custom Scenery/`.

## Sources

- [XRoads — GitHub](https://github.com/melbo911/xroads)
- [XRoads — forums.x-plane.org](https://forums.x-plane.org/index.php?/files/file/67227-xroads-transparent-roads-for-ortho4xp/)
