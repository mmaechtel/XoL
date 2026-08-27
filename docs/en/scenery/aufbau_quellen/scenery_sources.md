---
description: "X-Plane scenery options — standard scenery with Gateway airports, SimHeaven X-World autogen, freeware, payware, and interactive WorldMaps."
---
# Scenery

Here you will find information about various scenery options for X-Plane.

## Overview

X-Plane offers various ways to use realistic scenery and landscapes. This section presents the most important options.

## Standard Scenery

X-Plane comes with an extensive collection of standard scenery:

- **Global Scenery**: Basic landscape data for the entire world
- **Default Airports**: Basic airports with basic buildings and runways ([X-Plane Gateway](https://gateway.x-plane.com/))
- **Autogen**: Automatically generated buildings and vegetation
- **Mesh**: Basic terrain data

The standard scenery provides a good foundation for the flight simulator, but can be significantly improved with additional scenery.

### X-Plane Gateway Server

The [X-Plane Gateway Server](https://gateway.x-plane.com/) provides a central platform for community-driven airport scenery development. On this platform, users can create and improve airports, share their work with the community, download airports created by other users, and participate in quality assurance. Airports published on the Gateway undergo review by Laminar Research and are integrated into future X-Plane updates. This system ensures continuous improvement of standard airports, enables a worldwide community of developers, provides quality control through Laminar Research, and guarantees regular airport updates. An overview of all available Gateway airports can be found in the [Gateway Scenery Map](https://x-plane.cleverest.eu/). It is also noted there from which version the airport is included with X-Plane. Before downloading, one should check whether the airport is not already included in the current X-Plane version.

## SimHeaven X-World

SimHeaven X-World represents a scenery extension that significantly improves X-Plane's standard scenery. The extension provides detailed buildings and cityscapes, realistic vegetation and trees, as well as improved road networks and highways. Particularly noteworthy are the correct building heights and shapes, as well as regional architectural styles that enable an authentic representation of various regions.

The extension covers various regions: X-World Europe offers detailed European cities and landscapes, X-World America encompasses North and South American regions, X-World Asia presents Asian cities and landscapes, X-World Africa shows African regions, and X-World Oceania represents Australia and Oceania.

Installation is done manually in the Custom Scenery directory. The extension is compatible with Ortho4XP and AutoOrtho, optimized for X-Plane 12, and is continuously developed through regular updates and improvements.

The classic X-World packages for X-Plane 11 and X-Plane 12 remain free downloads on [simheaven.com](https://simheaven.com/xp12-sceneries/) and continue to receive updates. Alongside them, SimHeaven now offers a commercial line, [X-World Pro](https://simheaven.com/x-world-pro/).

### X-World Pro

X-World Pro is a VFR-oriented scenery line for X-Plane 12, sold through the X-Plane.org store either per continent or as a discounted world bundle. The free packages are not discontinued — they stay available and keep being updated — but Pro is a separate line, not an add-on to them.

**What Pro adds over the free packages**

- The network is split into three layers (aerials, ships, roads) where the free line has a single combined one, and it brings dynamic shipping and regional rail traffic
- Road traffic density that adapts to the surroundings — urban or rural — and to the time of day
- A noticeably wider variety of objects, vegetation, and farmland/crop detail
- Animated effects such as chimney smoke, cooling-tower steam, fountains and geysers
- Landmarks placed worldwide as visual navigation references

Object placement is derived from OpenStreetMap plus global building-footprint datasets. The free line names Microsoft Building Footprints explicitly; the Pro manual only speaks of global building footprints.

A free test scenery covering roughly 15 tiles in the Ruhr area, Luxembourg, and parts of the Netherlands, Belgium, and France is available on the SimHeaven site. It is intended for checking frame rates and loading behaviour before buying.

**Installation**

Pro consists of the scenery layers plus a separate library package (`simHeaven_X-WORLD-Pro_Library`), which supplies vegetation and the referenced X-Plane 12 assets — and it is the only library Pro needs. Both are unpacked into `Custom Scenery/` and registered in [scenery_packs.ini](../../glossary.md#scenery_packsini) following the order the installer prints: own and regional airports first, then `GLOBAL_AIRPORTS`, then the X-World Pro layers, then libraries, then overlays, ortho, and mesh.

One choice concerns Ortho4XP users directly. The bridge layer ships in two variants — `…-01-bridges_O4XP-Mesh` and `…-01-bridges_XP12-Mesh`. Exactly one of them stays enabled: traffic routing follows the ground mesh, and the Ortho4XP mesh differs from the stock X-Plane 12 one, so the wrong variant leaves the traffic misaligned with the bridges.

!!! warning "Pro: run the bundled Linux script, do not build the links by hand"

    The Pro library ships `install_XWP_Linux_Mac.sh` alongside the Windows batch file. Run it once from inside `Custom Scenery/simHeaven_X-WORLD-Pro_Library/`. It creates `XP12_libs` pointing at the whole `Resources/default scenery` directory and links the modified season textures into `1200 forests` — a different and larger set of links than the free vegetation library needs. Building a `1200 forests` link by hand there produces a broken install.

!!! note "Free vegetation library: symlink by hand on Linux"

    The free `simHeaven_X-World_Vegetation_Library` does not ship X-Plane's forest definitions; it links to them. Windows users double-click `set_link_WIN.bat`, which creates a directory junction and does nothing on Linux. SimHeaven documents the manual equivalent:

    ```bash
    cd "X-Plane 12/Custom Scenery/simHeaven_X-World_Vegetation_Library"
    ln -sf "../../Resources/default scenery/1200 forests" "1200 forests"
    ```

    Without it the log fills with `Failed to find resource 'simheaven/forests/….for'` — an error message, not an aborted load. Copying the `1200 forests` folder instead works but wastes disk space and goes stale on X-Plane updates.

Pro and the free line are mutually exclusive: run one or the other per continent, never both. Both place their objects from the same OSM base, so having both active duplicates them.

## Freeware and Shareware

[x-plane.org](https://forums.x-plane.org/) offers an extensive selection of free and affordable scenery. The community provides a variety of airports, including improved versions of standard airports and historical airports. In the area of landscapes, improved terrain data, more detailed vegetation, and special regions are available.

Various tools are available for creating and managing scenery. [Ortho4XP](../orthophotography/ortho4xp.md) enables the creation of custom orthophoto scenery, while [AutoOrtho](../ortho_streaming/autoortho.md) provides automatic orthophoto scenery. [XRoad](../../addon/scenery_addons/xroad.md) offers improved road networks for a more realistic representation of infrastructure.

## Payware Scenery

For the highest quality and detail accuracy, numerous commercial scenery options are available. An almost complete overview can be found linked below.

## Resources

For better overview and planning of flight simulation, two self-created WorldMaps are available:

- **[WorldMap of Scenery](/Maps/airportmap.html)** – An interactive map with over 1800 scenery options for X-Plane 12. The map provides detailed information about each airport to facilitate the search for suitable scenery. The search is done via a 4-digit valid ICAO code, which means smaller airfields such as grass strips and helipads are not displayed - this would make the map too confusing in some places already. Direct download links were deliberately omitted because:
    - No purchase recommendations for specific shops should be given
    - Updating numerous links would be very time-consuming
    - The map focuses on X-Plane 12 scenery (XP11 scenery was only included if there are special adaptations that support XP12 scenery features)

    There is a help link in the agenda that explains the popup entries.

- **[WorldMap of Ortho Tiles](/Maps/scenerymap.html)** – An overview map of self-created and installed Ortho Tiles. The displayed Orthos were specifically created for addon scenery and provide high-resolution textures, often supplemented with Mesh Patches for additional details such as Runway Slopes. In addition to the self-created Orthos, official Ortho Patches from scenery manufacturers and community-created patches from the X-Plane.org forum are also used.

---

## Further Reading

| Topic | Page | Focus |
|---|---|---|
| Scenery Components | [How X-Plane Builds the World](scenery_components.md) | Mesh, ortho, autogen layers and scenery_packs.ini load order |
| Orthophotography | [Concepts & Methods](../orthophotography/orthophotography_intro.md) | Static vs. streaming approaches for ground textures |
| AutoOrtho | [AutoOrtho](../ortho_streaming/autoortho.md) | Real-time ortho streaming with global coverage |
| XEarthLayer | [XEarthLayer](../ortho_streaming/xearthlayer.md) | Rust-based streaming with adaptive prefetch |
| XOrganizer | [XOrganizer](../../addon/tools/xorganizer.md) | Scenery management and scenery_packs.ini editor |
| GPU & VRAM | [GPU & VRAM](../../fundamentals/performance/gpu_vram.md) | VRAM impact of scenery quality settings |