# How X-Plane Builds the World

<div class="video-container" markdown>
<video controls width="100%" preload="metadata" aria-label="Video: Mastering Scenery Packs" poster="../assets/video/en/Mastering_scenery_packs/Mastering_scenery_packs.jpg">
  <source src="../assets/video/en/Mastering_scenery_packs/Mastering_scenery_packs.mp4" type="video/mp4">
</video>
</div>

X-Plane ships with a scenery that looks plausible from altitude, but it is far from photorealistic. With the right add-ons, however, the visual quality can be transformed dramatically. To get there, it helps to understand the three layers that make up X-Plane's scenery system: the terrain **Mesh** defines elevation, **Orthos** provide satellite imagery as ground textures, and **Autogen** populates the landscape with 3D objects.

## Meshes

The mesh is the terrain's elevation model — a network of triangles (a Triangulated Irregular Network, or TIN) that defines heights and slopes. Each triangle vertex carries a coordinate with longitude, latitude, and elevation. Together, these triangles shape mountains, valleys, and plains.

Mesh data is stored in X-Plane's DSF (Distribution Scenery Format) files. The default mesh ships with the simulator; higher-resolution alternatives (e.g., HD Mesh Scenery) can be installed as scenery packs.

The mesh provides structure only — no textures or objects.

## Orthos

Orthos (orthophotos) are aerial or satellite images projected onto the mesh as ground textures. They replace X-Plane's procedural land classes with photorealistic imagery — roads, fields, forests, and buildings become visible from altitude.

X-Plane uses DDS (DirectDraw Surface) textures internally. Source images from map providers (JPEG, PNG) are converted to GPU-compressed DDS format (DXT1/BC1 or DXT5/BC3) before X-Plane can use them.

Tools like **[Ortho4XP](addon/ortho4xp.md)** generate these DDS tiles offline, while streaming solutions deliver them on demand (see below).

## Autogen

Autogen (automatically generated scenery) adds 3D objects — buildings, trees, vehicles, power lines — to the landscape. X-Plane reads placement information from its DSF scenery files and distributes objects accordingly: trees in forest areas, buildings in residential zones, factories in industrial areas.

The placement data in X-Plane's default scenery is derived from OpenStreetMap and other geographic datasets during Laminar Research's scenery build pipeline. This data is baked into the DSF files — X-Plane does not query OSM at runtime. Third-party add-ons like SimHeaven X-World use OSM data separately to generate more detailed autogen coverage.

## How the Layers Interact

The three layers build on each other in a fixed order:

1. **Mesh** — defines elevation and terrain shape
2. **Ortho** — projects satellite imagery onto the mesh surface
3. **Autogen** — places 3D objects based on land use data

Each layer depends on the one below it. Orthos need the mesh to be projected correctly, and autogen needs both mesh and ortho data to place objects at the right positions and elevations.

## Add-ons

Several add-ons extend the default scenery layers:

- **[Ortho4XP](addon/ortho4xp.md)** — generates high-resolution ortho tiles offline from satellite imagery
- **[Ortho Streaming](addon/orthophotography_intro.md#ortho-streaming)** — AutoOrtho, XEarthLayer, and XPME stream satellite imagery on demand, no pre-generation needed
- **Custom Sceneries** — higher-resolution meshes or regional autogen objects (e.g., SimHeaven X-World)
- **Autogen Libraries** — additional object sets for more varied building and vegetation placement

---

## The scenery_packs.ini Load Order

The landscapes in X-Plane are created through the interaction of various components: meshes, orthos, autogen, and special sceneries like airports. For everything to be displayed correctly, the order in the `scenery_packs.ini` file is crucial.

## The Correct Order of Components

X-Plane processes `scenery_packs.ini` from top to bottom. Entries listed higher in the file have higher priority and override entries below them. The following list describes the layers from lowest priority (bottom of the file) to highest (top):

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

### The Special Role of Global Airports

The line `SCENERY_PACK *GLOBAL_AIRPORTS*` deserves special attention:

- **Position**: It should be **below** custom sceneries and landmarks, but **above** SimHeaven components, orthos, and meshes.
- **Function**: Global Airports contains the standard airports of X-Plane, often created by the community through the X-Plane Gateway.
- **Why this position?**
    - Custom sceneries (e.g., a detailed EDDF or EGLL) override the standard airports because they are listed higher.
    - Global Airports must be above SimHeaven components to ensure airports are not covered by autogen objects.
    - At the same time, Global Airports must be above orthos and meshes so airports are correctly placed on the landscape.
- **Important Note**: An incorrect position can lead to "floating" airports, missing taxiways, or covered details.

---

## Why the Order Matters

The order in `scenery_packs.ini` directly affects visual correctness:

- **Overlay**: Entries higher in the file override entries below them. An incorrectly placed entry can make an airport invisible or cover orthos with autogen objects.
- **Correctness**: Only the right order ensures that objects are placed correctly — houses stand on the ground, not in the air, and airports align with the mesh.

---

## Tips for Maintaining scenery_packs.ini

- **Use Tools**: Programs like **[XOrganizer](addon/xorganizer.md)** can automatically optimize the order and detect conflicts.
- **Create Backup**: Before changing `scenery_packs.ini`, create a backup copy to be able to undo errors.
- **Test**: After changes, load a scenery in X-Plane and check whether airports, orthos, and autogen are displayed correctly. Pay special attention to "floating" objects or missing details.
- **Watch for Updates**: New sceneries or add-ons can disrupt the order. Check the file regularly, especially after installations.

---

## Sources

- [X-Plane Scenery Developer Documentation](https://developer.x-plane.com/article/dsf-usage-in-x-plane/) — DSF file format and scenery structure
- [X-Plane Manual — Custom Scenery](https://www.x-plane.com/manuals/) — scenery_packs.ini load order