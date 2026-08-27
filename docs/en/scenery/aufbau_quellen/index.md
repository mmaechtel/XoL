---
title: X-Plane Scenery Structure and Sources
description: "X-Plane scenery structure explained: mesh, orthophotos, autogen layers, scenery_packs.ini load order, and available scenery sources."
---
# Structure & Sources

X-Plane's scenery consists of three layers: the mesh defines terrain shape, orthophotos project satellite imagery as ground textures, and autogen populates the landscape with 3D objects. Airports sit on top as their own priority level. Every scenery package belongs to one of these levels, and `scenery_packs.ini` decides which package wins where they overlap: entries listed higher take priority. Floating airports, invisible scenery, or autogen objects covering runways usually point to a wrong order rather than to a broken package.

Start with [Components](scenery_components.md) for the layer model, the load-order rules, and a worked `scenery_packs.ini` example. [Sources](scenery_sources.md) then surveys where scenery comes from: the standard scenery with Gateway airports, SimHeaven X-World for denser autogen, freeware and payware, plus interactive world maps for coverage checks. The [Orthophotography](../orthophotography/index.md) and [Ortho Streaming](../ortho_streaming/index.md) sections build on this foundation.

- **[Components](scenery_components.md)** — Load order and scenery_packs.ini
- **[Sources](scenery_sources.md)** — Overview of available scenery options
