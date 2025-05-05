## XRoads

[XRoads](../glossary.md#xroads) is a library for [X-Plane](../glossary.md#x-plane) 11 & 12 that improves the realism of [Ortho4XP](../glossary.md#ortho4xp) orthophotos. The library hides standard road polygons from databases such as OSM, particularly for ZL17+ orthos. This makes the actual roads from satellite images visible, while bridges, highways, expressways, and railway tracks remain displayed. The speed of AI vehicles is reduced to 70% of the original speed (adjustable via the "-v" parameter), which leads to more realistic traffic conditions. An automatically generated library.txt enables targeted control of transparent roads. In areas without ortho tiles, the autogen roads remain visible.

Download: [XRoads](https://forums.x-plane.org/index.php?/files/file/67227-xroads-transparent-roads-for-ortho4xp/)

### Installation on Linux

For creating the executable, the XRoads directory is entered and the command `make xroads` is executed. With installed Makefile and C-compiler packages, the executable is generated with this call. 