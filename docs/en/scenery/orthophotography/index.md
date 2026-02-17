# Orthophotography

Two approaches exist for photorealistic ground textures: static generation with Ortho4XP creates DDS tiles in advance and stores them locally — up to zoom level 19 for maximum detail, but storage-intensive. Streaming solutions deliver tiles at runtime via a virtual filesystem, without pre-generation. Ortho4XP generates not only textures but also high-resolution meshes, optionally enhanced with LiDAR data for more precise terrain representation.

- **[Concepts & Methods](orthophotography_intro.md)** — Overview of static and streaming approaches
- **[Ortho4XP](ortho4xp.md)** — Generate static ortho tiles offline
