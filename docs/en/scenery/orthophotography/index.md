---
title: Orthophotography for X-Plane 12
description: "Orthophotography for X-Plane: static tile generation with Ortho4XP and real-time streaming solutions for photorealistic ground textures on Linux."
---
# Orthophotography

Two approaches exist for photorealistic ground textures. Static generation with Ortho4XP creates DDS tiles in advance and stores them locally — up to zoom level 19 for maximum detail, but storage-intensive and limited to the regions prepared beforehand. Streaming solutions such as AutoOrtho or XEarthLayer deliver tiles at runtime via a virtual filesystem, without pre-generation, at the price of network load during flight. Ortho4XP generates not only textures but also high-resolution meshes, optionally enhanced with LiDAR data for more precise terrain representation.

[Concepts & Methods](orthophotography_intro.md) compares both approaches, explains the `scenery_packs.ini` setup, and matches them to player profiles by flying style and storage budget. [Ortho4XP](ortho4xp.md) is the hands-on guide for static tiles on Linux: installation, OrthoForge, parameter reference, and LiDAR. The streaming tools have their own section, [Ortho Streaming](../ortho_streaming/index.md), including the [Static + Streaming](../ortho_streaming/static_plus_streaming.md) combination of local tiles and on-demand imagery.

- **[Concepts & Methods](orthophotography_intro.md)** — Overview of static and streaming approaches
- **[Ortho4XP](ortho4xp.md)** — Generate static ortho tiles offline
