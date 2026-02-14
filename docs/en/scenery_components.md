# How X-Plane Builds the World: Meshes, Orthos, and Autogen Explained

<div class="video-container" markdown>
<video controls width="100%" preload="metadata" poster="../assets/video/en/Mastering_scenery_packs/Mastering_scenery_packs.jpg">
  <source src="../assets/video/en/Mastering_scenery_packs/Mastering_scenery_packs.mp4" type="video/mp4">
</video>
</div>

X-Plane is known for its realistic landscapes that immerse users in a living world while flying. Three central building blocks make up the scenery: **Meshes**, **Orthos**, and **Autogen**. This chapter explains what these terms mean and how they work together to create the impressive landscapes in X-Plane.

## Meshes: The 3D Framework of the World

The X-Plane world can be imagined as a giant 3D puzzle. It all starts with the **Mesh**. A mesh is the basic shape of the landscape – the digital framework that defines heights and forms of the terrain. It determines how mountains, valleys, hills, or plains look.

- **What is a Mesh?** It consists of many small triangles (polygons) that together form a network – hence the name "Mesh" (English for network). These triangles define for X-Plane how high or low a point is and how steep a slope should be.
- **Example**: A mountain in X-Plane is defined by a mesh that describes its height, shape, and inclination. Without a mesh, the world would just be a flat plane.

The mesh is thus the first step: It gives the landscape its structure, but no colors or details yet.

## Orthos: The Satellite Images for Realism

The second building block is **Orthos**. While the mesh provides the shape, orthos provide the visual surface – like a giant photo glued onto the mesh.

- **What are Orthos?** Orthos are aerial or satellite images that show the earth from above. They contain details like houses, roads, forests, fields, or rivers. In X-Plane, they are placed as image files (e.g., .jpg or .png) on the mesh.
- **Why are they important?** Without orthos, the mesh would only look like gray, lifeless hills. Orthos bring the colors and patterns of the real world into play.
- **Example**: When flying over a city, thanks to orthos, one can see roofs, streets, and green spaces that look realistic.

Tools like **Ortho4XP** help download high-resolution ortho images and integrate them into X-Plane. This makes the scenery even more detailed.

## Autogen: The World Comes to Life

Mesh and orthos already create an impressive base, but something is still missing: depth. This is where **Autogen** comes into play. Autogen (short for "automatically generated") adds 3D objects to the landscape that make it come alive – like houses, trees, cars, or power poles.

- **What is Autogen?** X-Plane analyzes the landscape (mesh and ortho) and automatically places appropriate objects. It often uses data sources like OpenStreetMap to know where cities, forests, or roads are.
- **How does it work?** Autogen "reads" the scenery and distributes objects: trees in forest areas, houses in residential areas, factories in industrial zones. These objects come from libraries provided by X-Plane or add-ons.
- **Example**: In a village, thanks to autogen, one can see houses with gardens, trees along the roadside, and maybe a few parked cars. Without autogen, the landscape would be flat – just a satellite image without depth.

## Interaction: How Everything Comes Together

The three building blocks work hand in hand:

1. **Mesh**: Provides the 3D shape of the landscape, e.g., the height of a mountain or the depth of a valley.
2. **Ortho**: Delivers the realistic image that is placed on the mesh, e.g., forests or roads on the mountain.
3. **Autogen**: Adds the 3D objects, e.g., trees and houses that perfectly match the scenery.

The result is a world that not only looks real but feels real. When flying over a valley, the mesh forms the hills, the ortho shows green meadows and paths, and autogen scatters cows, trees, and small huts – and there one has the living scenery!

## Add-ons and the Next Level

Many X-Plane fans use add-ons to improve meshes, orthos, and autogen:

- **[Ortho4XP](addon/ortho4xp.md)**: Downloads high-resolution satellite images and adapts them to meshes.
- **[Ortho Streaming](addon/orthophotography_intro.md#ortho-streaming)**: Solutions like AutoOrtho, XEarthLayer, or XPME stream satellite imagery in real time from the internet — no pre-generation needed, instantly flyable worldwide.
- **Custom Sceneries**: Bring better meshes or regional autogen objects, e.g., typical half-timbered houses for Germany.
- **Autogen Libraries**: Expand the selection of objects to make the scenery even more realistic.

With such tools, the X-Plane world can be shaped in even more detail – perfect for everyone who wants to dive deep into scenery design.

# The Correct Order in scenery_packs.ini: Mesh, Orthos, Autogen, and More

The landscapes in X-Plane are created through the interaction of various components: meshes, orthos, autogen, and special sceneries like airports. For everything to be displayed correctly, the order in the `scenery_packs.ini` file is crucial. This chapter explains how the order should be structured, why it's important, and how to avoid errors.

## The Correct Order of Components

X-Plane loads sceneries from bottom to top in the `scenery_packs.ini`. This means: entries further down have higher priority and can overwrite entries further up. Based on the main components, the following order results (from bottom to top):

1. **Mesh Files (e.g., HD Mesh, UHD Mesh)**  
    - **Function**: Meshes form the 3D basic structure of the landscape, i.e., heights, valleys, and hills.  
    - **Why first?** They are the basis for everything else. Without a mesh, orthos and objects cannot be placed correctly.  
    - **Example**: `FlyTampa_Athens_3_mesh` or `SFD_EDDM_Munich_2_Mesh`.

2. **Ortho Sceneries**  
    - **Function**: Orthos are satellite or aerial images that are placed on the mesh to represent realistic textures like roads or forests.  
    - **Why after?** Orthos need the mesh to be correctly "stretched," but must be loaded before autogen so objects can be placed on them.  
    - **Example**: `z_ortho_California` or `zz_Ortho_SpainUHDv2_1`.

3. **Autogen Objects and Libraries**  
    - **Function**: Autogen adds 3D objects like buildings, trees, or vehicles that make the landscape come alive.  
    - **Why after?** Autogen is based on mesh and ortho to place objects correctly (e.g., houses on level ground, no trees on roads).  
    - **Example**: `simHeaven_X-World_Europe-6-scenery` or `simHeaven_X-World_Europe-7-forests`.

4. **Special Objects and Masts**  
    - **Function**: Special objects like radio masts, wind turbines, or other prominent structures.  
    - **Why after?** These objects should be above autogen to ensure they are visible.  
    - **Example**: `Usa_Radio_Masts_01` or `world_wind_turbines`.

5. **Global Airports**  
    - **Function**: Contains the standard airports of X-Plane.  
    - **Why after?** Must be above autogen and orthos, but below custom sceneries.  
    - **Example**: `*GLOBAL_AIRPORTS*`.

6. **Custom Sceneries and Landmarks**  
    - **Function**: Special sceneries like airports or landmarks (e.g., the Eiffel Tower) contain detailed objects and textures.  
    - **Why at the top?** They have the highest priority so they are not covered by other components.  
    - **Example**: `Aerosoft_EDDF_Frankfurt_3_Scenery` or `X-Plane Landmarks - Paris`.

### Example of a Correct Order

Here is an excerpt from a typical `scenery_packs.ini` (from top to bottom, i.e., in the order X-Plane loads them):

```ini
# Custom Airports and Landmarks (highest priority)
SCENERY_PACK Custom Scenery/Aerosoft-EGLL Airport London-Heathrow_1_DefaultStreets/
SCENERY_PACK Custom Scenery/Aerosoft-EGLL Airport London-Heathrow_2/
SCENERY_PACK Custom Scenery/Aerosoft_EDDF_Frankfurt_1_Parked_Cars/
SCENERY_PACK Custom Scenery/Aerosoft_EDDF_Frankfurt_2_Roads/
SCENERY_PACK Custom Scenery/Aerosoft_EDDF_Frankfurt_3_Scenery/
SCENERY_PACK Custom Scenery/X-Plane Landmarks - Berlin and Frankfurt/
SCENERY_PACK Custom Scenery/X-Plane Landmarks - London/
SCENERY_PACK Custom Scenery/X-Plane Landmarks - Paris/

# Global Airports (standard airports)
SCENERY_PACK *GLOBAL_AIRPORTS*

# Special Objects and Masts
SCENERY_PACK Custom Scenery/Usa_Radio_Masts_01/
SCENERY_PACK Custom Scenery/Usa_TV_Masts_0/
SCENERY_PACK Custom Scenery/world_wind_turbines/

# SimHeaven X-World (Autogen)
SCENERY_PACK Custom Scenery/simHeaven_X-World_Europe-1-vfr/
SCENERY_PACK Custom Scenery/simHeaven_X-World_Europe-2-regions/
SCENERY_PACK Custom Scenery/simHeaven_X-World_Europe-3-details/
SCENERY_PACK Custom Scenery/simHeaven_X-World_Europe-4-extras/
SCENERY_PACK Custom Scenery/simHeaven_X-World_Europe-5-footprints/
SCENERY_PACK Custom Scenery/simHeaven_X-World_Europe-6-scenery/
SCENERY_PACK Custom Scenery/simHeaven_X-World_Europe-7-forests/
SCENERY_PACK Custom Scenery/simHeaven_X-World_Europe-8-network/

# Ortho Sceneries
SCENERY_PACK Custom Scenery/z_ortho_California/
SCENERY_PACK Custom Scenery/z_ortho_Colorado/
SCENERY_PACK Custom Scenery/z_ortho_Florida/
SCENERY_PACK Custom Scenery/zz_Ortho_Alps_West/
SCENERY_PACK Custom Scenery/zz_Ortho_SpainUHDv2_1/

# Mesh Files (lowest priority)
SCENERY_PACK Custom Scenery/FlyTampa_Athens_3_mesh/
SCENERY_PACK Custom Scenery/FlyTampa_Amsterdam_4_mesh/
SCENERY_PACK Custom Scenery/KDEN-Denver International Airport_Mesh/
SCENERY_PACK Custom Scenery/SFD_EDDM_Munich_2_Mesh/
```

## The Special Role of Global Airports

The line `SCENERY_PACK *GLOBAL_AIRPORTS*` deserves special attention:

- **Position**: It should be **after** custom sceneries and landmarks, but **before** SimHeaven components and orthos.  
- **Function**: Global Airports contains the standard airports of X-Plane, often created by the community through the X-Plane Gateway.  
- **Why this position?**  
    - Custom Sceneries (e.g., a detailed EDDF or EGLL) can override the standard airports if they are higher in the list.  
    - Global Airports must be above SimHeaven components to ensure airports are not covered by autogen objects.  
    - At the same time, Global Airports must be above orthos and meshes so airports are correctly placed on the landscape.  
- **Important Note**: An incorrect position can lead to problems like "floating" airports, missing taxiways, or covered details.

## Why the Order is So Important

The correct order in the `scenery_packs.ini` is crucial for several reasons:

- **Overlay**: Entries further up (with higher priority) overwrite entries further down. An incorrectly placed entry can, for example, make an airport invisible or cover orthos.  
- **Correctness**: Only the right order ensures that objects are placed correctly – houses stand on the ground, not in the air, and airports fit the mesh.  
- **Performance**: A logical order helps X-Plane load sceneries more efficiently, which can improve loading times and performance.  

## Tips for Maintaining the scenery_packs.ini

To ensure sceneries are always displayed correctly, here are some practical tips:

- **Use Tools**: Programs like **[XOrganizer](addon/xorganizer.md)** can automatically optimize the order and detect conflicts.  
- **Create Backup**: Before changing the `scenery_packs.ini`, a backup copy should be created to be able to undo errors.  
- **Test**: After changes, a scenery should be loaded in X-Plane and checked to see if airports, orthos, and autogen are displayed correctly. Special attention should be paid to "floating" objects or missing details.  
- **Watch for Updates**: New sceneries or add-ons can disrupt the order. The file should be checked regularly, especially after installations. 