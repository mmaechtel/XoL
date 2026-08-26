## XEarthLayer v0.4.3 — Three-Tier Cache & GPU Device Selection

XEarthLayer hat in den letzten Tagen zwei Updates bekommen (v0.4.2 + v0.4.3), die zusammen einen großen Sprung machen:

**Three-Tier Cache** — Zwischen Memory-Cache und Chunk-Disk liegt jetzt ein DDS-Disk-Cache. Kodierte Tiles werden auf Disk persistiert, statt bei Memory-Eviction neu komprimiert zu werden (~3,5 ms NVMe-Read vs ~50–200 ms Re-Encode). Spürbar weniger Stutter bei langen Flügen.

**GPU Device Selection** — Wer eine iGPU (z.B. AMD Radeon auf Ryzen) neben einer dedizierten NVIDIA hat: XEarthLayer kann die iGPU für die DDS-Komprimierung nutzen, während die dGPU X-Plane rendert. Default ist `gpu_device = integrated`. GPU-Encoding ist jetzt ohne spezielles Build-Flag in jedem Binary enthalten.

**Speed-proportionales Prefetch** — Die Prefetch-Box skaliert mit der Bodengeschwindigkeit (3,5° bei 40 kt bis 6,5° bei 450 kt+). Im Anflug ~45% weniger Over-Fetching.

**CPU-Concurrency auf 50%** — Der Default für parallele Encoding-Jobs ist jetzt die Hälfte der logischen Kerne statt alle. Deutlich weniger Konkurrenz mit X-Plane out of the box.

Wie schon in früheren Versionen liefern die regionalen Pakete ein höher aufgelöstes Mesh als X-Planes Default — basierend auf dem Shred86 Ortho4XP-Fork. Wer noch mehr will, kann zusätzlich LiDAR-Daten (z.B. von sonny.4lima.de) einbinden.

**Fazit:** Mit dem DDS-Disk-Cache, GPU-Offloading auf die iGPU und den konservativeren CPU-Defaults kommt man jetzt an den Punkt, an dem hochauflösende Orthos im Flug keine Stutters mehr verursachen — X-Plane läuft smooth durch, auch auf langen Strecken mit ständig wechselnder Szenerie. Mit eigenen LiDAR-Daten und ZL19 sind Anflüge mit konstanten 60 FPS minimum ein Traum — inkl. aller Addons die X-Plane so hergibt, 3rd-Party-Szenerien, SimHeaven und Co.!

Die XoL-Doku ist aktualisiert:
:flag_gb: <https://xol.emvisio.de/en/scenery/ortho_streaming/xearthlayer.html>
:flag_de: <https://xol.emvisio.de/scenery/ortho_streaming/xearthlayer.html>
