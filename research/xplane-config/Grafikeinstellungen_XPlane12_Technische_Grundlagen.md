# Technische Grundlagen der X-Plane 12 Grafikeinstellungen: Rendering-Architektur, Einstellungsparameter und Performance-Charakteristik

## Zusammenfassung (Abstract)

Die vorliegende Arbeit dokumentiert die technischen Grundlagen der Grafikeinstellungen in X-Plane 12 unter besonderer Berucksichtigung der Linux-Plattform. Im Zentrum stehen drei Themenkomplexe: (1) die Rendering-Architektur mit Vulkan als primarer Grafik-API und der Zink-basierten OpenGL-Kompatibilitatsschicht, (2) die verfugbaren Grafikeinstellungen mit ihren jeweiligen Auswirkungen auf Bildqualitat und Performance, sowie (3) die Rendering-Einstellungen fur Objektdichte, Vegetation und Verkehr. Die Analyse stutzt sich ausschliesslich auf offizielle Quellen von Laminar Research (developer.x-plane.com, x-plane.com), die Vulkan-Spezifikation und Mesa-Dokumentation. Ziel ist die Schaffung einer verifizierten Wissensbasis fur die Dokumentationsseite zur X-Plane-Konfiguration.

---

## 1. Grafik-API: Vulkan vs. OpenGL in X-Plane 12

### 1.1 Vulkan als primare Rendering-API

X-Plane 12 verwendet Vulkan (unter Linux und Windows) bzw. Metal (unter macOS) als **ausschliessliche Rendering-API** fur die eigene Rendering-Engine. Ben Supnik (Laminar Research) stellte dies unmissverstandlich klar:

> "X-Plane 12 uses Vulkan/Metal as its renderer, always."
> -- Quelle: [X-Plane 12 Early Access Is Here](https://developer.x-plane.com/2022/09/x-plane-12-early-access-is-here/)

Dies stellt eine fundamentale Veranderung gegenuber X-Plane 11 dar, wo Vulkan ab Version 11.50 (2020) als **optionale** Alternative zu OpenGL eingefuhrt wurde. In X-Plane 11 war ein Checkbox in den Grafikeinstellungen vorhanden: "Use Metal/Vulkan driver for faster rendering". In X-Plane 12 ist Vulkan nicht mehr optional -- die gesamte Engine rendert nativ uber Vulkan.

**Hardwareanforderung:** X-Plane 12 setzt eine **Vulkan 1.3-fahige GPU** voraus. Die minimalen Anforderungen sind:

| GPU-Hersteller | Minimale Hardware | Minimaler Treiber |
|---|---|---|
| NVIDIA | GeForce 900er Serie (Desktop) oder 965M/970M/980M (Mobile) -- Maxwell Gen 2+ | Treiber Version 510+ |
| AMD | Radeon RX 500 oder neuer | Adrenaline 22.2.1+ |
| Intel | Arc GPUs (ab X-Plane 12.3.0) | Nicht spezifiziert |

Zusatzlich wird mindestens 2 GB VRAM vorausgesetzt (Minimum), empfohlen werden 8 GB VRAM.

Quellen:
- [X-Plane 12 System Requirements](https://www.x-plane.com/kb/x-plane-12-system-requirements/)
- [X-Plane 12 Early Access Is Here](https://developer.x-plane.com/2022/09/x-plane-12-early-access-is-here/)

### 1.2 Technische Vorteile von Vulkan

Vulkan bietet gegenuber OpenGL wesentliche architektonische Vorteile, die fur X-Plane 12 relevant sind:

**Geringerer CPU-Overhead:** Vulkan reduziert den Driver-Overhead erheblich, indem es dem Entwickler explizite Kontrolle uber GPU-Ressourcen gibt. Dies ist besonders relevant, da X-Plane traditionell CPU-limitiert ist.

**GPU-Driven Rendering:** X-Plane 12 nutzt Vulkan-Compute-Shader fur GPU-seitige Entscheidungen. Das neue Vegetationssystem beispielsweise fuhrt LOD-Entscheidungen und Culling direkt auf der GPU aus:

> "LOD decisions are also done on the GPU on an individual, per-tree basis, so the GPU is quite literally creating its own optimized workload."
> -- Quelle: [Next Generation Trees and OpenGL](https://developer.x-plane.com/2021/08/next-generation-trees-and-opengl/)

**Render-Graph-Architektur:** Ab X-Plane 12.06 verwendet die Engine einen Node-Graph fur die Rendering-Pipeline, der VRAM-Wiederverwendung uber Pipeline-Stufen hinweg ermoglicht:

> "The rendering system [was converted] from hand-coded to a node graph structure. This allows the simulator to double-book VRAM used to render the main frame."
> -- Quelle: [X-Plane 12.06 Is Full of Many Things](https://developer.x-plane.com/2023/07/x-plane-12-06-is-full-of-many-things/)

**Indirekte Draw-Calls:** Das neue Vegetationssystem nutzt Compute-Shader und indirekte Draw-Calls, eine Technik die OpenGL nicht leisten kann:

> "There is no next generation future for OpenGL, as it just isn't possible to support it."
> -- Quelle: [Next Generation Trees and OpenGL](https://developer.x-plane.com/2021/08/next-generation-trees-and-opengl/)

### 1.3 Warum Vulkan unter Linux bevorzugt wird

Auf der Linux-Plattform bietet Vulkan zusatzliche Vorteile gegenuber OpenGL:

**Mesa/RADV fur AMD-GPUs:** Der RADV Vulkan-Treiber (Teil des Mesa-Projekts) ist der empfohlene Treiber fur AMD-GPUs unter Linux. X-Plane 12 erfordert Mesa-Treiber Version 22.0 oder neuer. RADV liefert konsistent bessere Performance als der alternative AMDVLK-Treiber. Mesa 25.0 brachte Vulkan 1.4-Support fur RADV.

Quellen:
- [RADV -- The Mesa 3D Graphics Library](https://docs.mesa3d.org/drivers/radv.html)
- [X-Plane 12 System Requirements](https://www.x-plane.com/kb/x-plane-12-system-requirements/)

**NVIDIA unter Linux:** NVIDIA-Nutzer benotigen den proprietaren Treiber (Version 510+). Der Open-Source-Treiber Nouveau unterstutzt kein Vulkan in ausreichendem Umfang fur X-Plane 12.

Quelle: [X-Plane 12 System Requirements](https://www.x-plane.com/kb/x-plane-12-system-requirements/)

**Intel Arc (experimentell):** Intel Arc GPUs werden ab X-Plane 12.3.0 unterstutzt. Integrierte Intel-Grafik (HD Graphics, UHD Graphics, Iris Xe) wird aufgrund fehlender Treiber-Features oder unzureichender Performance nicht unterstutzt.

Quelle: [X-Plane 12 System Requirements](https://www.x-plane.com/kb/x-plane-12-system-requirements/)

### 1.4 OpenGL-Kompatibilitat: Die Zink-Schicht

Obwohl X-Plane 12 selbst ausschliesslich uber Vulkan rendert, existieren tausende Plugins, die OpenGL-Zeichenaufrufe verwenden. Laminar Research lost dieses Kompatibilitatsproblem durch den Einsatz von **Zink**, einem Open-Source-Treiber aus dem Mesa-Projekt.

**Funktionsweise:** Zink ubersetzt OpenGL-Befehle von Plugins in Vulkan-Kommandos und fuhrt diese auf demselben Vulkan-Device aus, das X-Plane nutzt:

> "There is exactly one Vulkan instance and device, shared by both X-Plane and Zink."
> -- Quelle: [Addressing Plugin Flickering](https://developer.x-plane.com/2023/02/addressing-plugin-flickering/)

**Performance-Vorteil gegenuber nativer Interop:** Die fruhere Methode (natives Vulkan/OpenGL-Interop) fuhrte zu erheblichem Overhead:

> "The native approach [adds] almost 10ms per frame in overhead -- or as bad as 30ms per frame in some cases."
> -- Quelle: [Addressing Plugin Flickering](https://developer.x-plane.com/2023/02/addressing-plugin-flickering/)

Mit Zink-Interop steigt die FPS in Testszenarien von 50 auf 80 FPS -- ein Gewinn von 30 FPS.

**Plugin-Flickering-Fix fur AMD:** Die Hauptmotivation fur Zink war das schwerwiegende Plugin-Flickering auf AMD-GPUs. Die native Vulkan/OpenGL-Interoperabilitat war fehlerhaft:

> "Driver support for this [Vulkan/OpenGL interop] is flaky at best."
> -- Quelle: [Addressing Plugin Flickering](https://developer.x-plane.com/2023/02/addressing-plugin-flickering/)

**Verfugbarkeit:** Zink ist auf Windows und Linux verfugbar (nicht auf macOS). Fur NVIDIA wird mindestens Treiberversion 23.2.1 benotigt. In X-Plane 12.1.0 wurde Zink zunachst fur NVIDIA-Karten deaktiviert (Beta 4), dann in Beta 6 wieder aktiviert, mit Fallback-UI bei Initialisierungsproblemen.

Quellen:
- [Addressing Plugin Flickering](https://developer.x-plane.com/2023/02/addressing-plugin-flickering/)
- [X-Plane 12 now uses the open source Zink driver](https://www.gamingonlinux.com/2023/02/x-plane-12-now-uses-the-open-source-zink-driver-to-help-plugins/)
- [X-Plane 12.1.0 Release Notes](https://www.x-plane.com/kb/x-plane-12-1-0-release-notes/)

### 1.5 Wann OpenGL noch relevant sein kann

Trotz der Vulkan-Architektur kann ein Fallback auf OpenGL sinnvoll sein:

- **Plugin-Inkompatibilitat:** Einige altere Plugins funktionieren nicht korrekt uber die Zink-Ubersetzungsschicht. In solchen Fallen kann OpenGL-Rendering notwendig sein.
- **GPU-Debugging:** Fur die Fehlersuche bei Rendering-Problemen kann der `--debug_gl` Kommandozeilenparameter verwendet werden, um Debug-OpenGL-Kontexte zu aktivieren.
- **Bekannte Zink-Bugs:** Es existieren Mesa-Bugs, etwa bei `GL_FRAMEBUFFER_SRGB`, die zu verschwindendem Rendering fuhren konnen.

Quelle: [Addressing Plugin Flickering](https://developer.x-plane.com/2023/02/addressing-plugin-flickering/)

**KEINE VERLASSLICHE QUELLE GEFUNDEN:** Fur einen expliziten `--force_opengl` Kommandozeilenparameter in X-Plane 12 konnte keine offizielle Dokumentation gefunden werden. Die offizielle Kommandozeilen-Dokumentation listet ausschliesslich OpenGL-bezogene Hardware-Flags auf (z.B. `--no_threaded_ogl`, `--no_glsl`), aber keinen Vulkan/OpenGL-Umschalter.

Quelle: [Command Line Options](https://developer.x-plane.com/article/command-line-options/)

### 1.6 Versionshistorie: Rendering-Anderungen nach Version

| Version | Wesentliche Rendering-Anderungen |
|---|---|
| 12.00 (Sep 2022) | Vulkan/Metal als exklusiver Renderer, FSR 1.0, HDR-Pipeline, volumetrische Wolken |
| 12.06 (Jul 2023) | Render-Graph-Architektur, Cloud-Shader-Neuschreib, VRAM-Optimierung |
| 12.1.0 (Feb 2024) | FXAA-Checkbox, MSAA-Verbesserungen, Zink-Stabilisierung, RCAS-Slider, Depth of Field |
| 12.1.2 | Boots-Rendering, World Objects Density-Steuerung |
| 12.2.0 (Apr 2025) | Tone-Mapping-Wechsel zu AgX, Exposure Fusion, Cloud-Rendering-Overhaul, SSAO-Rekalibrierung, Shader-Compiler-Neuschreib |
| 12.3.0 | Exposure-Fusion-Fix fur AMD, Tree-Lighting, Intel Arc-Support |
| 12.4.0 (Dez 2025) | Multi-Core-Szenerie-Verarbeitung, FXAA exkludiert Cockpit-Displays, AGX-Tonemapper-Update, VR-spezifische Grafikeinstellungen |

Quellen:
- [X-Plane 12.00 Release Notes](https://www.x-plane.com/kb/x-plane-12-00-release-notes/)
- [X-Plane 12.1.0 Release Notes](https://www.x-plane.com/kb/x-plane-12-1-0-release-notes/)
- [X-Plane 12.2.0 Release Notes](https://www.x-plane.com/kb/x-plane-12-2-0-release-notes/)
- [X-Plane 12.3.0 Release Notes](https://www.x-plane.com/kb/x-plane-12-3-0-release-notes/)
- [X-Plane 12.4.0 Release Notes](https://www.x-plane.com/kb/x-plane-12-4-0-release-notes/)
- [What's New in 12.4.0](https://www.x-plane.com/2025/12/whats-new-in-12-4-0/)

---

## 2. Grafikeinstellungen im Detail

### 2.1 HDR-Rendering-Pipeline (Always-On)

X-Plane 12 verwendet eine **vollstandig HDR-basierte Rendering-Pipeline**, die sich fundamental von X-Plane 11 unterscheidet. HDR ist kein optionaler Effekt mehr, sondern die Grundlage der gesamten Rendering-Architektur:

> "X-Plane 12's rendering pipeline is entirely HDR, from start to finish, using 16-bit floating point encoding to hold a much wider dynamic range of luminance."
> -- Quelle: [Threshold: Laminar Follows Up on X-Plane 12 Development](https://www.thresholdx.net/news/lrskle)

**Photometrisches Rendering:** X-Plane 12 verwendet echte physikalische Lichteinheiten (Nits, cd/m^2) statt der 0-255-Wertebereiche des fruheren Low-Dynamic-Range-Systems. Dies ermoglicht:

- Unbegrenzte Anzahl von Lichtquellen mit realistischen Schatten
- Screen Space Reflections (SSR)
- Dynamische Belichtungsanpassung (Auto-Exposure)
- Bloom-Effekte mit physikalisch korrekten HDR-Werten
- Atmospharisches Scattering

**Tone Mapping:** Das Tone-Mapping wandelt die HDR-Daten fur die Darstellung auf Standard-Monitoren um:
- 12.00-12.1.x: Benutzerdefiniertes ACES-Blend-Verfahren
- 12.2.0: Wechsel zu **AgX** fur verbesserte Farbgenauigkeit bei hellen und gesattigten Szenen
- 12.4.0: Weiteres AGX-Tonemapper-Update mit erweitertem Farbumfang

**Exposure Fusion (ab 12.2.0):** Balanciert helle und dunkle Bildbereiche gleichzeitig -- lost das lang bestehende "dunkles Cockpit"-Problem.

Quellen:
- [Threshold: Laminar Follows Up](https://www.thresholdx.net/news/lrskle)
- [X-Plane 12.2.0 Release Notes](https://www.x-plane.com/kb/x-plane-12-2-0-release-notes/)
- [What's New in X-Plane 12.2.0](https://www.x-plane.com/2025/04/whats-new-in-x-plane-12-2-0/)

### 2.2 Texture Quality (Texturqualitat)

Der Texture-Quality-Slider steuert die maximale Auflosung der Texturen, die in den VRAM geladen werden. Texturen sind die Bildkarten, die uber Terrain, Gebaude und Flugzeuge gelegt werden.

**Funktionsweise:**
- Niedrige Einstellungen: Texturen erscheinen "blurry and blocky", verbrauchen aber wenig VRAM
- Hohe Einstellungen: Scharfe, detaillierte Texturen, hoher VRAM-Verbrauch
- X-Plane zeigt die aktuelle VRAM-Nutzung an: "Total size of all loaded textures at current settings: xxx meg"

**Kritischer VRAM-Schwellenwert:** Wenn die geladenen Texturen den verfugbaren VRAM der Grafikkarte uberschreiten, kommt es zu einem **abrupten Performance-Einbruch** (nicht graduell). Empfehlung: Immer etwas "Padding" lassen, da verschiedene Flugzeuge und Szenerien unterschiedlich viel VRAM beanspruchen.

**Kalibrierungsmethode (offiziell empfohlen):**
1. Texture Quality auf niedrigste Stufe setzen
2. X-Plane neu starten, Framerate notieren
3. Slider eine Stufe erhohen, neu starten
4. Wiederholen, bis die Framerate einbricht -- dann eine Stufe zuruckgehen

**KEINE VERLASSLICHE QUELLE GEFUNDEN:** Exakte VRAM-Verbrauchszahlen (in GB) pro Einstellungsstufe (Low/Medium/High) werden von Laminar Research nicht offiziell dokumentiert. Der Verbrauch hangt stark von Auflosung, installierten Szenerien und Flugzeugen ab.

Quellen:
- [Configuring the Rendering Options](https://www.x-plane.com/kb/configuring-the-rendering-options/)
- [Setting the Rendering Options for Best Performance](https://www.x-plane.com/kb/setting-the-rendering-options-for-best-performance/)

### 2.3 Antialiasing

X-Plane 12 bietet drei Antialiasing-Methoden, die teilweise kombinierbar sind:

#### 2.3.1 MSAA (Multisample Anti-Aliasing)

MSAA rendert die Szene mehrfach pro Frame an den Kanten und blendet die Ergebnisse zusammen. Verfugbare Stufen: **2x, 4x, 8x**.

- **Performance-Impact:** Signifikant -- 4x MSAA entspricht annahernd dem Rendering bei vierfacher Auflosung. Hauptsachlich GPU-belastend, kaum CPU-Impact.
- **VRAM:** 2x verdoppelt, 4x vervierfacht den Framebuffer-Bedarf.
- **Ab 12.1.0:** MSAA-Resolve erfolgt im "scene-referred color space" fur verbesserte visuelle Treue.
- **Ab 12.1.0:** Coverage to Alpha wird auf alpha-getesteten Oberflachen aktiviert wenn MSAA aktiv ist, was die Qualitat transparenter Texturen (z.B. Vegetation, Zaune) verbessert.

#### 2.3.2 FXAA (Fast Approximate Anti-Aliasing)

FXAA ist ein Post-Processing-Filter, der als Nachbearbeitungsschritt auf das fertig gerenderte Bild angewendet wird.

- **Performance-Impact:** Sehr gering ("high quality, inexpensive")
- **Ab 12.1.0:** Eigener Checkbox "Enable FXAA Antialiasing" -- unabhangig von MSAA ein-/ausschaltbar
- **Ab 12.1.0:** FXAA ist **immer aktiviert**, wenn MSAA ausgewahlt ist
- **Ab 12.4.0:** FXAA **exkludiert Cockpit-Displays** -- die Instrumente bleiben scharf und lesbar, wahrend die Aussenszene geglattet wird

#### 2.3.3 SSAA (Supersampling Anti-Aliasing)

SSAA rendert die gesamte Szene bei hoherer Auflosung und skaliert dann herunter. Dies liefert die hochste Qualitat, aber auch den hochsten Performance-Impact.

- **8x Supersampling:** Eliminiert Shimmer auf transparenten Texturen (Vegetation, Zaune) nahezu vollstandig
- **Performance-Impact:** Massiv -- deutlich hoher als MSAA bei vergleichbarer Stufe

#### 2.3.4 Kombination FXAA + MSAA

Durch Kombination von FXAA mit MSAA (z.B. FXAA + 8x MSAA) kann ein sehr gutes AA-Ergebnis mit vergleichsweise moderatem Performance-Verlust erzielt werden. Ben Supnik bemerkte, dass die offizielle FXAA-Integrationsleitlinie davon abrat, zeigte sich aber offen fur Experimente.

Quellen:
- [X-Plane 12.1.0 Release Notes](https://www.x-plane.com/kb/x-plane-12-1-0-release-notes/)
- [Two Pain Relief Fixes Coming Soon](https://developer.x-plane.com/2023/09/two-pain-relief-fixes-coming-soon/)
- [What's New in 12.4.0](https://www.x-plane.com/2025/12/whats-new-in-12-4-0/)
- [Configuring the Rendering Options](https://www.x-plane.com/kb/configuring-the-rendering-options/)

### 2.4 Anisotrope Filterung

Anisotrope Filterung verbessert die Scharfe von Texturen in schragen Blickwinkeln (z.B. Start-/Landebahnen in der Perspektive).

- **Verfugbare Stufen:** Konfigurierbar, empfohlen 8x oder 16x
- **Performance-Impact:** "Minimal effect on most machines and moderate impact on some"
- **Empfehlung:** 8x-16x empfohlen, da signifikante visuelle Verbesserung bei geringen Kosten

Quelle: [Configuring the Rendering Options](https://www.x-plane.com/kb/configuring-the-rendering-options/)

### 2.5 Shadow Quality (Schattenqualitat)

X-Plane verwendet **Cascaded Shadow Maps (CSM)** -- ein Verfahren, das die Szene in Entfernungszonen aufteilt und fur jede Zone eine Schattenmap mit angepasster Auflosung berechnet.

**Verfugbare Stufen (historisch, X-Plane 10/11):**
- **Static:** Flacher, unveranderlicher Flugzeugschatten auf dem Boden
- **Overlay:** Schattenposition variiert mit der Sonnenposition
- **3-D on Aircraft:** Flugzeug wirft Schatten auf sich selbst und den Boden
- **Global:** Alle Objekte, Baume etc. werfen Schatten auf alles -- **massiver Performance-Impact**

**X-Plane 12 Neuerungen:**
- Shadow Quality ist ein **eigener Slider** (neu in XP12, vorher Teil von Visual Effects)
- **Checkbox "Draw shadows on scenery":** Aktiviert/deaktiviert Szenerieschatten
- **Ab 12.1.0:** Geglaattete Schattenrander, verbesserte Cloud-Schattenqualitat
- **Ab 12.2.0:** Schatten berucksichtigen Wolkendichte und Erdkrummung; Wolken werfen Schatten aufeinander und zwischen Schichten; Bodenschatten korrekt ausgerichtet mit Wolkenbedeckung

**Performance-Impact:** Schatten sind sowohl CPU- als auch GPU-intensiv. Bei aktivierten globalen Schatten wird jedes Objekt mehrfach gerendert (einmal fur die Szene, zusatzlich fur jede Schattenmap-Kaskade). Der Performance-Verlust betrug in Tests ca. 10 FPS.

**Empfehlung:** Medium-Einstellung wird als hochstes praktikables Niveau vor signifikantem Performance-Einbruch empfohlen.

Quellen:
- [Configuring the Rendering Options](https://www.x-plane.com/kb/configuring-the-rendering-options/)
- [X-Plane 12.2.0 Release Notes](https://www.x-plane.com/kb/x-plane-12-2-0-release-notes/)
- [X-Plane 12.1.0 Release Notes](https://www.x-plane.com/kb/x-plane-12-1-0-release-notes/)

### 2.6 Ambient Occlusion (SSAO)

Ambient Occlusion Quality (SSAO) ist ein in X-Plane 12 eigenstandiger Einstellungsparameter, der aus dem fruheren Visual-Effects-Slider herausgelost wurde.

**Technische Implementierung:** X-Plane nutzt intern **Horizon-Based Ambient Occlusion (HBAO)**, nicht klassisches SSAO. Der Effekt simuliert weiche Schatten in Kanten, Ritzen und dort, wo Objekte aufeinandertreffen.

**Einschrankung:** SSAO wirkt **ausschliesslich auf Aussenbereiche** -- Szenerie und als "exterior" markierte Flugzeugobjekte. Cockpit-Interieurs sind nicht betroffen, da:
1. Die Skalierung fur Innen- und Aussenbereich zu unterschiedlich ist
2. Die meisten Flugzeuge bereits gebackene Ambient Occlusion in den Cockpit-Texturen haben
3. SSAO nur bei hoheren Rendereinstellungen verfugbar ist

**Ab 12.2.0:** SSAO wurde fur Baume, Gebaude und Flugzeuge rekalibriert.

**Performance-Impact:** Offiziell als "dirt cheap effect" beschrieben, in der Praxis vernachlassigbar.

Quellen:
- [Screen Space Ambient Occlusion Only Affects Exterior Stuff](https://developer.x-plane.com/2017/02/screen-space-ambient-occlusion-only-affects-exterior-stuff/)
- [X-Plane 12.2.0 Release Notes](https://www.x-plane.com/kb/x-plane-12-2-0-release-notes/)

### 2.7 Reflection Quality (Reflexionsqualitat)

X-Plane 12 verwendet mehrere Reflexionstechnologien:

**Water Reflection Detail:** Steuert, wie grundlich Wasserreflexionen uber Pixel-Shader berechnet werden. Dies hat einen **signifikanten Performance-Impact** in der Nahe von Wasserflachen, da Reflexionen das doppelte Rendering von Objekten erfordern (einmal fur die Szene, einmal fur die Reflexion).

**Screen Space Reflections (SSR):** X-Plane 12 reserviert VRAM fur SSR als Teil der HDR-Pipeline. SSR erzeugt Reflexionen auf glatten Oberflachen (Flugzeughaut, Glas) basierend auf dem bereits gerenderten Bild.

**Ab 12.2.0:**
- Genauere Wasserreflexionen besonders bei Sonnenuntergang
- Verbessertes PBR-Material: genauere Reflexionen auf Oberflachen -- Glas und glanzende Materialien moglicherweise anpassungsbedurftig
- Wolkenschatten auf Wasser sichtbar (bereits ab 12.1.0)

**Ab 12.3.0:** Verbesserte Cubemap-Platzierung fur naturlichere Cockpit-Reflexionen.

**KEINE VERLASSLICHE QUELLE GEFUNDEN:** Exakte Aufschlusselung der Reflexions-Qualitatstufen (Low/Medium/High) und deren GPU-Kosten ist nicht offiziell dokumentiert.

Quellen:
- [Configuring the Rendering Options](https://www.x-plane.com/kb/configuring-the-rendering-options/)
- [X-Plane 12.2.0 Release Notes](https://www.x-plane.com/kb/x-plane-12-2-0-release-notes/)
- [X-Plane 12.3.0 Release Notes](https://www.x-plane.com/kb/x-plane-12-3-0-release-notes/)
- [X-Plane 12 Early Access Is Here](https://developer.x-plane.com/2022/09/x-plane-12-early-access-is-here/)

### 2.8 Volumetrische Wolken (Cloud Quality)

Cloud Quality ist ein **neuer Einstellungsparameter in X-Plane 12**, der in fruheren Versionen nicht existierte.

**Rendering-Technik:** X-Plane 12 rendert Wolken als dynamische 3D-Volumina (volumetrisches Rendering) statt als 2D-Sprites. Dazu wird ein Ray-Marching-Verfahren verwendet, bei dem Strahlen durch das Wolkenvolumen geschossen werden, um Dichte, Licht und Schatten zu berechnen.

**Performance-Impact:** Wolken sind der **teuerste einzelne Teil des Renderers**:

> "Clouds are probably the single most expensive part of the renderer."
> -- Quelle: [X-Plane 12 Early Access Is Here](https://developer.x-plane.com/2022/09/x-plane-12-early-access-is-here/)

Dichtere Wolkenschichten oder Overcast-Bedingungen erfordern mehr Berechnungen und reduzieren die FPS signifikant.

**Versionshistorie der Wolken-Rendering-Verbesserungen:**
- **12.06:** Cloud-Shader komplett neu geschrieben -- schneller, weniger Artefakte. Eigener Rendering-Pfad fur Cirrus-Wolken. "Minecraft-Wolken" (kubische Artefakte) adressiert.
- **12.1.0:** Crash-Fix beim Vulkan Memory Allocator bei aktiviertem volumetrischen Nebel
- **12.2.0:** **Kompletter Overhaul** -- verbesserte Schattendetails innerhalb von Wolken, Wolken werfen Schatten aufeinander und zwischen Schichten, neuer Cloud-Shaping-Algorithmus fur naturlichere Formationen, Wolken innerhalb von 1 km werden als voll-3D-Objekte gerendert
- **12.3.0:** Weitere Verbesserungen der Wolken-Performance

Quellen:
- [X-Plane 12 Early Access Is Here](https://developer.x-plane.com/2022/09/x-plane-12-early-access-is-here/)
- [X-Plane 12.06 Is Full of Many Things](https://developer.x-plane.com/2023/07/x-plane-12-06-is-full-of-many-things/)
- [X-Plane 12.2.0 Release Notes](https://www.x-plane.com/kb/x-plane-12-2-0-release-notes/)
- [What's New in X-Plane 12.2.0](https://www.x-plane.com/2025/04/whats-new-in-x-plane-12-2-0/)

### 2.9 FSR (FidelityFX Super Resolution)

X-Plane 12 integriert **AMD FidelityFX Super Resolution (FSR) 1.0** als Upscaling-Technologie. FSR ist Open-Source und funktioniert auf allen GPU-Herstellern (AMD, NVIDIA, Intel).

> "FSR lets us render the world faster and then scale the result up to 4K -- it's a great option for users who want to fly in 4K but keep their framerates up."
> -- Quelle: [X-Plane 12 Development Update -- March 4th, 2022](https://developer.x-plane.com/2022/03/x-plane-12-development-update-march-4th-2022/)

**Funktionsweise:**
1. **EASU (Edge-Adaptive Spatial Upsampling):** Rendert die 3D-Szene bei niedrigerer Auflosung als der Monitor
2. **RCAS (Robust Contrast-Adaptive Sharpening):** Scharfungspass, der Details im hochskalierten Bild extrahiert

**Bedienung:** Ein Slider in den Grafikeinstellungen steuert die Render-Auflosung. Slider nach links = niedrigere interne Auflosung = mehr Performance, weniger Bildqualitat. Slider ganz rechts = native Auflosung (kein FSR).

**Ab 12.1.0:** RCAS-Slider mit Beschreibungen im Einstellungsmenu exponiert.

**VR-Unterstutzung:** FSR funktioniert auch in VR.

**Einschrankungen:**
- X-Plane 12 verwendet FSR 1.0, **nicht** FSR 2.x oder 3.x
- FSR 1.0 ist ein rein raumlicher Upscaler (kein temporales Upscaling, keine Frame Generation)
- Fehlende Motion Vectors in der Engine verhindern die Integration von FSR 2.x/3.x
- Sichtbarer Qualitatsverlust gegenuber nativer Auflosung, insbesondere bei Text und feinen Details
- DLSS (NVIDIA) wird **nicht** unterstutzt

**KEINE VERLASSLICHE QUELLE GEFUNDEN:** Fur konkrete FSR 3.x-Plane in zukunftigen Versionen gibt es keine offizielle Zusage. Die Dezember-2025-Roadmap erwahnt keine Upscaling-Technologie-Updates.

Quellen:
- [X-Plane 12 Development Update -- March 4th, 2022](https://developer.x-plane.com/2022/03/x-plane-12-development-update-march-4th-2022/)
- [X-Plane 12 Early Access Is Here](https://developer.x-plane.com/2022/09/x-plane-12-early-access-is-here/)
- [X-Plane 12.1.0 Release Notes](https://www.x-plane.com/kb/x-plane-12-1-0-release-notes/)

### 2.10 Rendering Resolution (Rendering-Auflosung)

Rendering Resolution ist ein **neuer Einstellungsparameter in X-Plane 12**. Dieser Slider ist eng mit FSR verknupft -- er bestimmt die interne Rendering-Auflosung als Anteil der Monitor-Auflosung:

- **100%:** Native Auflosung (kein Upscaling)
- **< 100%:** Niedrigere interne Auflosung, anschliessend FSR-Upscaling auf Monitorauflosung

Dies spart sowohl GPU-Rechenzeit als auch VRAM auf Kosten der Bildqualitat.

Quelle: [X-Plane 12 Early Access Is Here](https://developer.x-plane.com/2022/09/x-plane-12-early-access-is-here/)

### 2.11 Ubersicht: Einstellungsparameter in X-Plane 12

Die folgende Tabelle fasst die in X-Plane 12 verfugbaren Grafikeinstellungen zusammen. Neu in X-Plane 12 (gegenuber X-Plane 11) sind mit [NEU] markiert:

| Einstellung | Typ | Primar | Anmerkung |
|---|---|---|---|
| Texture Quality | Slider | GPU (VRAM) | Maximale Texturauflosung |
| Antialiasing (MSAA) | Auswahl (2x/4x/8x) | GPU | Multisample-Kantenglaattung |
| FXAA | Checkbox | GPU (gering) | Post-Processing-Filter, ab 12.1.0 separat |
| Anisotropic Filtering | Slider | GPU (gering) | Texturqualitat in schragen Winkeln |
| Shadow Quality [NEU] | Slider | CPU + GPU | Schattenauflosung und -detail |
| Draw Shadows on Scenery | Checkbox | CPU + GPU | Aktiviert Szenerieschatten |
| Ambient Occlusion (SSAO) [NEU] | Slider | GPU (gering) | Weiche Kontaktschatten |
| Cloud Quality [NEU] | Slider | GPU | Volumetrische Wolkenqualitat |
| Reflection Detail | Slider | CPU + GPU | Wasserreflexionsberechnung |
| Rendering Resolution [NEU] | Slider | GPU | Interne Renderauflosung (FSR) |
| RCAS Sharpening [NEU] | Slider | GPU (gering) | Scharfung nach FSR-Upscaling |
| Rendering Distance | Slider | CPU + GPU | Sichtweite fur 3D-Objekte |
| World Objects Density | Slider | CPU | Dichte von Gebauden, Strassen, Autos |
| Vegetation Density [NEU] | Slider | GPU | Baumdichte |
| Draw Parked Aircraft | Checkbox | CPU | Statische Flugzeuge an Gates |
| Visual Effects | Slider | GPU | Gesamtqualitat visueller Effekte |

Quellen: Zusammenstellung aus allen oben genannten Release Notes und offizieller Dokumentation.

---

## 3. Rendering-Einstellungen: Objekte, Vegetation und Verkehr

### 3.1 World Objects Density (Objektdichte)

In X-Plane 11 wurden vier separate Slider (Tree Density, Object Density, Road Density, Number of Cars) zu einem einzigen **"Number of World Objects"**-Slider konsolidiert:

> "This has been consolidated down into a single 'number of world objects' 3-d slider. The idea is to balance all 3-d so that CPU time is spent efficiently and the rendering looks plausible."
> -- Quelle: [Where Have All My Settings Gone](https://developer.x-plane.com/2017/01/where-have-all-my-settings-gone/)

**Performance-Impact:** Dieser Slider hat den **grossten Einfluss auf die Framerate** aller Einstellungen. Er ist primaer CPU-limitiert:

> "Number of objects will have the greatest effect on simulator's performance."
> -- Quelle: [Configuring the Rendering Options](https://www.x-plane.com/kb/configuring-the-rendering-options/)

**Skalierungsverhalten:** Eine Verdopplung der Detaildistanz rendert **vierfach so viele Objekte** (quadratische Skalierung uber die Flache).

**X-Plane 12 Erganzung:** In X-Plane 12 wurde Vegetation als separater Slider herausgelost (siehe 3.2), wahrend World Objects weiterhin Gebaude, Strassen und Autos steuert.

Quellen:
- [Where Have All My Settings Gone](https://developer.x-plane.com/2017/01/where-have-all-my-settings-gone/)
- [Configuring the Rendering Options](https://www.x-plane.com/kb/configuring-the-rendering-options/)

### 3.2 Vegetation Density

Vegetation Density ist ein **neuer, eigenstandiger Slider in X-Plane 12**, der von World Objects getrennt wurde.

**Technische Architektur:** Das Vegetationssystem wurde fur X-Plane 12 vollstandig neu geschrieben. Es ist GPU-zentrisch und basiert auf Compute-Shadern:

- **GPU-Culling:** Compute-Shader reduzieren die Baumliste auf sichtbare Elemente
- **GPU-LOD:** LOD-Entscheidungen erfolgen pro einzelnem Baum auf der GPU
- **Indirect Draw Calls:** Die GPU generiert ihre eigene optimierte Arbeitslast
- **Wind-Animation:** Komplett auf der GPU uber Compute-Shader, ohne CPU-Belastung
- **Multi-Tier-LOD:** Nahbereich = komplexe 3D-Baume, Mittelbereich = vereinfachte 3D-Modelle, Ferne = Billboard-Sprites

> "The new vegetation engine is designed to use very little CPU processing, and instead moves the majority of the work to the GPU."
> -- Quelle: [Next Generation Trees and OpenGL](https://developer.x-plane.com/2021/08/next-generation-trees-and-opengl/)

**Performance-Impact:** Primaer GPU-belastend, kaum CPU-Impact. Das System kann potenziell Millionen von Baumen verarbeiten.

**Erfordert Vulkan/Metal:** Das neue Vegetationssystem benotigt zwingend Vulkan oder Metal -- es kann nicht unter OpenGL ausgefuhrt werden.

Quellen:
- [Next Generation Trees and OpenGL](https://developer.x-plane.com/2021/08/next-generation-trees-and-opengl/)
- [The Autogen Is Really Fast](https://developer.x-plane.com/2016/03/the-autogen-is-really-fast/)

### 3.3 Rendering Distance (Sichtweite)

Der Rendering-Distance-Slider steuert, wie weit entfernte 3D-Objekte in hohem Detail gerendert werden.

**Performance-Charakteristik:**
- **Quadratische Skalierung:** Verdopplung der Distanz = vierfache Objektanzahl
- **Sowohl CPU als auch GPU:** Mehr Objekte bedeuten mehr CPU-Arbeit (Szenen-Management) und mehr GPU-Arbeit (Rendering)

> "Lowering [world detail distance] may improve frame rate on slower systems."
> -- Quelle: [Configuring the Rendering Options](https://www.x-plane.com/kb/configuring-the-rendering-options/)

Quelle: [Configuring the Rendering Options](https://www.x-plane.com/kb/configuring-the-rendering-options/)

### 3.4 Autogen (Automatisch generierte Gebaude)

Das Autogen-System generiert prozedurale Gebaude, Strassen und urbane Strukturen. Es nutzt intensiv GPU-Instancing:

> "It hits the instancing path almost all of the time and as a result it can draw a lot of autogen at reasonable fps."
> -- Quelle: [The Autogen Is Really Fast](https://developer.x-plane.com/2016/03/the-autogen-is-really-fast/)

**Performance-Multiplikatoren:** Aktivierte Schatten und Wasserreflexionen multiplizieren die Rendering-Kosten von Autogen erheblich, da jedes Objekt fur jede Schattenmap-Kaskade und Reflexion erneut gerendert werden muss.

Quelle: [The Autogen Is Really Fast](https://developer.x-plane.com/2016/03/the-autogen-is-really-fast/)

### 3.5 Wasser- und Wolkeneffekte

**Wasser:** Die Wasserreflexionsberechnung verwendet Pixel-Shader und hat einen **signifikanten Performance-Impact** in der Nahe von Wasserflachen. Empfehlung: Reflection Detail auf Low halten, wenn Performance priorisiert wird.

**Ab 12.1.0:** Wolkenschatten auf Wasser sichtbar; Turbiditatmodell korrigiert fur standortbasierte Wasserklarheitsvariationen.

**Volumetrischer Nebel:** Erzeugt lokale Dichtevariationen fur graduelles Verblassen von Objekten. Signifikanter Framerate-Impact auf alteren Systemen.

Quellen:
- [Configuring the Rendering Options](https://www.x-plane.com/kb/configuring-the-rendering-options/)
- [X-Plane 12.1.0 Release Notes](https://www.x-plane.com/kb/x-plane-12-1-0-release-notes/)

### 3.6 AI-Aircraft und Flight Models

**Number of Other Aircraft:** Wird unter Aircraft > Aircraft and Situations > Other Aircraft eingestellt. Jedes AI-Flugzeug erfordert zusatzliche CPU-Zyklen fur Physikberechnung.

**Flight Models per Frame:** Kann im General-Tab auf eine niedrigere Anzahl (empfohlen: 2) gesetzt werden. Dies begrenzt, fur wie viele Flugzeuge pro Frame die volle Physik-Simulation berechnet wird.

> "Removing all other aircraft provides maximum speed, as X-Plane will only have to calculate physics on your aircraft."
> -- Paraphrasiert aus: [Setting the Rendering Options for Best Performance](https://www.x-plane.com/kb/setting-the-rendering-options-for-best-performance/)

**Performance-Impact:** Hauptsachlich CPU-belastend. Auf den meisten Computern sind die objektbezogenen Einstellungen CPU-limitiert und haben einen "huge impact on frame rate".

**AI-Only-Optimierung:** Einige Flugzeuge bieten spezielle "AI-Only"-Performance-Modes, die weniger FPS kosten als die Verwendung des Standard-X-Plane-12-Flugzeugs als AI.

**Parked Aircraft Checkbox:** "Draw parked aircraft" zeigt statische Flugzeuge an Gates an. Dies ist CPU-belastend und sollte bei Performance-Problemen deaktiviert werden.

Quellen:
- [Setting the Rendering Options for Best Performance](https://www.x-plane.com/kb/setting-the-rendering-options-for-best-performance/)
- [Configuring the Rendering Options](https://www.x-plane.com/kb/configuring-the-rendering-options/)

### 3.7 Multi-Core-Szenerie-Verarbeitung (ab 12.4.0)

Ab Version 12.4.0 nutzt X-Plane **mehrere CPU-Kerne** fur die Szenerievorbereitung:

> "Scenery processing now uses multi-core technology."
> -- Quelle: [What's New in 12.4.0](https://www.x-plane.com/2025/12/whats-new-in-12-4-0/)

**Gemessene Performance-Verbesserungen:**
- P1 (Best Case): 28% CPU-Zeitreduktion
- P95 (anspruchsvoll): 33% Verbesserung
- P99 (Worst Case): 38% Verbesserung
- Alpha-Tester: 7.9% bis 15.8% Verbesserung (hardwareabhangig)

**Einschrankung:** GPU-limitierte Systeme profitieren kaum von dieser Anderung.

Quelle: [What's New in 12.4.0](https://www.x-plane.com/2025/12/whats-new-in-12-4-0/)

---

## 4. Zusammenfassung der CPU- vs. GPU-Lastverteilung

| Primar CPU | Primar GPU | CPU + GPU |
|---|---|---|
| World Objects Density | Texture Quality (VRAM) | Shadow Quality |
| AI Aircraft / Flight Models | Antialiasing (MSAA) | Reflection Detail |
| Parked Aircraft | Cloud Quality | Rendering Distance |
| | Vegetation Density | |
| | Rendering Resolution (FSR) | |
| | SSAO | |
| | FXAA | |
| | Anisotropic Filtering | |

**Allgemeine Empfehlung (offizielle Optimierungsreihenfolge):**
1. Texture Quality an VRAM anpassen (kalibrieren)
2. Visual Effects erhohen
3. Erst danach Antialiasing und Szenerieschatten erhohen
4. World Objects zuletzt erhohen (grosster CPU-Impact)

Quelle: [Configuring the Rendering Options](https://www.x-plane.com/kb/configuring-the-rendering-options/)

---

## 5. Lucken und nicht belegte Punkte

Die folgenden Punkte konnten trotz umfangreicher Recherche nicht durch offizielle Primarquellen belegt werden:

1. **Visual Effects Stufen im Detail:** Was genau sich pro Stufe (Low/Medium/High/Ultra) andert, ist nicht offiziell dokumentiert. Bekannt ist nur, dass HDR ab den oberen zwei Stufen aktiviert ist (X-Plane 10/11) -- in X-Plane 12 ist HDR ohnehin immer aktiv. Der Visual-Effects-Slider wurde in X-Plane 12 stark reduziert, da SSAO und Shadow Quality als eigene Slider herausgelost wurden.

2. **Exakte VRAM-Verbrauchszahlen pro Texture-Quality-Stufe:** Werden nicht offiziell dokumentiert, da sie stark von installierten Szenerien, Flugzeugen und Monitorauflosung abhangen.

3. **Exakte Reflection-Quality-Stufen:** Die genaue Aufschlusselung der Reflexions-Qualitatstufen und deren GPU-Kosten ist nicht offiziell dokumentiert.

4. **FSR 2.x/3.x Roadmap:** Es gibt keine offizielle Zusage fur die Integration neuerer FSR-Versionen oder DLSS.

5. **Kommandozeilenparameter fur Vulkan/OpenGL-Umschaltung:** Es konnte kein offizieller `--force_opengl` Parameter fur X-Plane 12 nachgewiesen werden.

6. **Cloud Quality Stufen im Detail:** Was genau die einzelnen Positionen des Cloud-Quality-Sliders bewirken, ist nicht offiziell aufgeschlusselt.

---

## Quellenverzeichnis

### Offizielle Laminar Research Dokumentation
- [X-Plane 12 System Requirements](https://www.x-plane.com/kb/x-plane-12-system-requirements/)
- [Configuring the Rendering Options](https://www.x-plane.com/kb/configuring-the-rendering-options/)
- [Setting the Rendering Options for Best Performance](https://www.x-plane.com/kb/setting-the-rendering-options-for-best-performance/)
- [X-Plane 12 Desktop Manual](https://www.x-plane.com/manuals/desktop/)
- [Command Line Options](https://developer.x-plane.com/article/command-line-options/)

### Laminar Research Developer Blog
- [X-Plane 12 Early Access Is Here (Sep 2022)](https://developer.x-plane.com/2022/09/x-plane-12-early-access-is-here/)
- [X-Plane 12 Development Update -- March 4th, 2022](https://developer.x-plane.com/2022/03/x-plane-12-development-update-march-4th-2022/)
- [X-Plane 12.06 Is Full of Many Things (Jul 2023)](https://developer.x-plane.com/2023/07/x-plane-12-06-is-full-of-many-things/)
- [Addressing Plugin Flickering (Feb 2023)](https://developer.x-plane.com/2023/02/addressing-plugin-flickering/)
- [Two Pain Relief Fixes Coming Soon (Sep 2023)](https://developer.x-plane.com/2023/09/two-pain-relief-fixes-coming-soon/)
- [Next Generation Trees and OpenGL (Aug 2021)](https://developer.x-plane.com/2021/08/next-generation-trees-and-opengl/)
- [The Autogen Is Really Fast (Mar 2016)](https://developer.x-plane.com/2016/03/the-autogen-is-really-fast/)
- [Where Have All My Settings Gone (Jan 2017)](https://developer.x-plane.com/2017/01/where-have-all-my-settings-gone/)
- [Screen Space Ambient Occlusion Only Affects Exterior Stuff (Feb 2017)](https://developer.x-plane.com/2017/02/screen-space-ambient-occlusion-only-affects-exterior-stuff/)
- [FXAA: Your New Friend (Sep 2011)](https://developer.x-plane.com/2011/09/fxaa-your-new-friend/)
- [Plugin Guidance for OpenGL Drawing](https://developer.x-plane.com/article/plugin-guidance-for-opengl-drawing/)

### Release Notes
- [X-Plane 12.00 Release Notes](https://www.x-plane.com/kb/x-plane-12-00-release-notes/)
- [X-Plane 12.1.0 Release Notes](https://www.x-plane.com/kb/x-plane-12-1-0-release-notes/)
- [X-Plane 12.1.2 Release Notes](https://www.x-plane.com/kb/x-plane-12-1-2-release-notes/)
- [X-Plane 12.2.0 Release Notes](https://www.x-plane.com/kb/x-plane-12-2-0-release-notes/)
- [X-Plane 12.3.0 Release Notes](https://www.x-plane.com/kb/x-plane-12-3-0-release-notes/)
- [X-Plane 12.4.0 Release Notes](https://www.x-plane.com/kb/x-plane-12-4-0-release-notes/)
- [What's New in X-Plane 12.2.0 (Apr 2025)](https://www.x-plane.com/2025/04/whats-new-in-x-plane-12-2-0/)
- [What's New in 12.4.0 (Dez 2025)](https://www.x-plane.com/2025/12/whats-new-in-12-4-0/)
- [X-Plane Roadmap Update -- December 2025](https://www.x-plane.com/2025/12/x-plane-roadmap-update-december-2025/)

### Externe technische Quellen
- [RADV -- The Mesa 3D Graphics Library](https://docs.mesa3d.org/drivers/radv.html)
- [Threshold: Laminar Follows Up on X-Plane 12 Development](https://www.thresholdx.net/news/lrskle)
- [GamingOnLinux: X-Plane 12 now uses the open source Zink driver](https://www.gamingonlinux.com/2023/02/x-plane-12-now-uses-the-open-source-zink-driver-to-help-plugins/)
- [How to enable Vulkan & Metal in X-Plane](https://x-plane.helpscoutdocs.com/article/100-flying-with-vulkan-metal)
