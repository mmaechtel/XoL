# Introduction to Orthophotography in Flight Simulation

Orthophotography represents a central component of modern flight simulation environments, as it enables high-resolution and realistic ground textures. This section explains the methodological approaches for integrating high-quality orthophotos into the X-Plane flight simulation software.

## Significance of Orthophotography

In flight simulation, precise terrain representation is essential to ensure realistic landing and flight conditions. X-Plane includes a standard global elevation model ("mesh") by default, whose resolution is often limited due to storage constraints. This elevation model, which is described in detail in the "Components" menu of the scenery settings, forms the basis for terrain representation. Through the use of specific add-ons, both the precision of the mesh and the quality of the projected ground textures can be significantly improved. The primary goal is to increase topographic accuracy, with the visual optimization of the scenery resulting as a secondary benefit.

## Methods for Integrating Orthophotos

Several approaches are available for implementing orthophotos in X-Plane:

1. **[Ortho4XP](ortho4xp.md)**: A powerful tool for generating orthophoto scenery. Ortho4XP creates an elevation model (mesh) for defined geographic sections ("tiles") based on publicly available satellite data, such as LIDAR data. The accuracy of the mesh is adjustable and can be increased by using high-resolution LIDAR data. The corresponding chapter explains not only the functionality and operation of Ortho4XP but also how such high-resolution data sources can be utilized.

2. **[AutoOrtho](autoortho.md)**: An innovative solution for dynamic streaming of orthophotos. While Ortho4XP stores large amounts of satellite imagery, AutoOrtho pursues a data-saving approach by loading the image data for projection onto the mesh on demand. This significantly reduces storage requirements.

3. **[Combination](autoortho_plus_zortho.md)**: To further optimize AutoOrtho's resolution, the more precise meshes from Ortho4XP can be combined with AutoOrtho's streaming technology. This procedure is described in detail in a specific chapter.

Through the presented methods, a flexible and efficient integration of orthophotos into X-Plane is enabled, which significantly increases both the topographic precision and the visual quality of the flight simulation. 