# X-Plane 12 Einstellungsprofile und Linux-Performance: Eine praxisorientierte Analyse

## Zusammenfassung (Abstract)

Diese Arbeit untersucht drei zentrale Aspekte der X-Plane 12 Performance-Optimierung unter Linux: (1) empfohlene Einstellungsprofile nach GPU-Klasse auf Basis offizieller Laminar-Research-Dokumentation und unabhaengiger Benchmarks, (2) Linux-spezifische Performance-Aspekte einschliesslich Vulkan-Treiberverhalten, Mesa/RADV vs. NVIDIA-proprietaer, Compositor-Impact und relevanter Umgebungsvariablen, sowie (3) die Performance-relevante Versionshistorie von X-Plane 12.0 bis 12.4. Alle Aussagen sind mit Primaerquellen belegt; Punkte ohne zuverlaessige Quelle sind explizit gekennzeichnet.

---

## 1. Systemanforderungen und GPU-Klassen

### 1.1 Offizielle Systemanforderungen (Laminar Research)

Die folgenden Angaben stammen direkt von der offiziellen X-Plane 12 Systemanforderungsseite:

**Minimum:**
- CPU: Intel Core i3/i5/i7/i9 mit 4+ Kernen oder AMD Ryzen 3/5/7/9
- RAM: 8 GB
- GPU: Vulkan-1.3-faehige Grafikkarte mit mindestens 2 GB VRAM
- NVIDIA: 900er Serie Desktop oder neuer (Maxwell 2. Gen+), Treiber 510+
- AMD: Radeon RX 500 oder neuer, Adrenaline 22.2.1+
- Intel: Arc GPUs (ab X-Plane 12.3.0)
- Speicher: 25 GB

**Empfohlen:**
- CPU: Intel Core i5-12600K oder AMD Ryzen 5 3500 oder besser
- RAM: 16-24 GB oder mehr
- GPU: DirectX-12-faehige Karte mit mindestens 8 GB VRAM (GeForce RTX 3070 oder besser, AMD-Aequivalent, oder Intel Arc B580)

**Linux-spezifisch:**
- Offiziell unterstuetzt und getestet: nur Ubuntu LTS
- NVIDIA: proprietaerer Treiber erforderlich (Minimum 510, aktuell empfohlen: 580er-Serie)
- AMD: Mesa 22.0 oder neuer (RADV Vulkan-Treiber)

Quelle: https://www.x-plane.com/kb/x-plane-12-system-requirements/

### 1.2 GPU-Klassen und Leistungsfaehigkeit

#### OpenBenchmarking.org Benchmark-Daten (Phoronix Test Suite)

Die folgenden Werte stammen aus 92 oeffentlichen Benchmark-Ergebnissen der Phoronix Test Suite (Test pts/xplane12), gemessen bei 1920x1080, High-Preset. Die Ergebnisse stammen ueberwiegend von Linux-Systemen:

| GPU | FPS (1080p High) | Anzahl Ergebnisse |
|-----|-------------------|-------------------|
| NVIDIA RTX 4090 | 177 | 3 |
| AMD RX 7900 XTX | 149 | 3 |
| AMD RX 7900 XT | 127 | 3 |
| NVIDIA RTX 4080 | 127 | 3 |
| AMD RX 6800 XT | 92 (+/-1) | 5 |
| AMD RX 7800 XT | 91 | 4 |
| AMD RX 7700 XT | 79 | 3 |
| AMD RX 6700 XT | 64 (+/-2) | 5 |
| AMD RX 7600 | 51 | 3 |
| NVIDIA RTX 2060 SUPER | 44 | 3 |
| AMD RX 6600 | 40 (+/-2) | 5 |

Gesamtbereich: 25-222 FPS, Median: 70 FPS.

Quelle: https://openbenchmarking.org/test/pts/xplane12

**Einordnung der in der Aufgabenstellung genannten GPU-Klassen:**

| Klasse | GPUs | VRAM | Erwartete FPS (1080p High) | Einschaetzung |
|--------|------|------|---------------------------|---------------|
| Einstieg | GTX 1070 / RX 580 | 6-8 GB | ~35-50 FPS | Spielbar mit reduzierten Settings |
| Mittelklasse | RTX 3060 / RX 6700 XT | 8-12 GB | ~50-70 FPS | Komfortabel bei High-Preset |
| Oberklasse | RTX 4070/4080 / RX 7800 XT | 12-16 GB | ~90-130 FPS | Maximale Settings moeglich |

Hinweis: Die GTX 1070 und RX 580 sind nicht direkt in den OpenBenchmarking-Daten enthalten. Die Schaetzung basiert auf der relativen GPU-Leistung gegenueber den gemessenen Karten. Die RTX 3060 ist ebenfalls nicht direkt gelistet, aber die RTX 2060 SUPER erreicht 44 FPS; die RTX 3060 liegt generationsbedingt ca. 20-30% darueber. **Keine exakte Quelle fuer diese Extrapolationen vorhanden.**

### 1.3 VRAM-Verbrauch und Texture Paging

X-Plane 12 verwendet ein dynamisches Texture-Paging-System unter Vulkan, das sich grundlegend von OpenGL unterscheidet:

**Funktionsweise:**
- X-Plane ueberwacht kontinuierlich den freien VRAM
- Bei Knappheit werden Texturen stufenweise verkleinert (Downsampling), priorisiert nach Distanz zum Flugzeug
- Jede Halbierung der Texturaufloesung reduziert den Speicherverbrauch um ca. 77%
- Die Prioritaetsreihenfolge: User-Aircraft > nahe Szenerie > entfernte Elemente
- Die Texturaufloesung wird basierend auf der Flugzeugposition (nicht Kameraposition) gesteuert

**VRAM-Budgetierung (Richtlinien fuer die Einstellungswahl):**

| Verfuegbarer VRAM | Empfohlene Nutzung |
|--------------------|--------------------|
| 2 GB | Niedrigste Texturaufloesung, 1080p |
| 4 GB | HDR mit mittlerer Texturqualitaet, 1080p |
| 6 GB | HDR mit hoher Texturqualitaet, bis 1440p |
| 8 GB+ | Hohe/maximale Texturen, bis 4K |
| 12-16 GB | Maximale Settings + umfangreiche Third-Party-Addons |

**Wichtiger Hinweis:** Der tatsaechlich nutzbare VRAM liegt typischerweise 1-2 GB unter dem Nennwert der Karte, da Betriebssystem und Desktop-Compositor ebenfalls VRAM belegen.

**Drittanbieter-Addon VRAM-Verbrauch:**
Aircraft-Addons mit "non-pageable" Texturen koennen erheblich VRAM beanspruchen. Beispiel: Das Zibo 737 Mod belegt allein ca. 1,49 GB an nicht paginierbaren Texturen.

**Diagnose-Werkzeug:** Die aktuelle VRAM-Belegung kann im Rendering-Options-Dialog abgelesen werden unter "Total size of all loaded textures at current settings".

Quellen:
- https://developer.x-plane.com/2020/01/all-your-vram-is-belonging-to-us-and-plugins/
- https://developer.x-plane.com/2020/05/fighting-blurry-textures/

---

## 2. Rendering-Einstellungen im Detail

### 2.1 Kategorisierung: GPU-limitiert vs. CPU-limitiert

Die Rendering-Optionen in X-Plane 12 lassen sich in zwei Kategorien einteilen:

**GPU-limitierte Einstellungen (linke Seite des Settings-Dialogs):**
- Visual Effects (Low/Medium/High/Maximum) -- Schatten, Lichtreflexionen, HDR
- Texture Quality -- VRAM-Verbrauch, Texturschaerfe
- Antialiasing -- vergleichbar mit Verdopplung der Bildschirmaufloesung
- Shadow Quality -- insbesondere "Draw shadows on scenery"
- Water Reflections -- Pixel-Shader-Berechnungen
- Cloud Puffs -- Anzahl und Groesse der Wolkenpuffs

**CPU-limitierte Einstellungen (rechte Seite des Settings-Dialogs):**
- Number of Objects -- **groesster CPU-Impact**; World Detail Distance skaliert quadratisch
- Number of Roads und Cars
- Reflection Detail
- AI-Traffic-Dichte
- Draw Distance / World Detail Distance -- Verdopplung rendert 4x so viele Objekte

Quelle: https://www.x-plane.com/kb/setting-the-rendering-options-for-best-performance/

### 2.2 Optimierungsstrategie nach offizieller Empfehlung

Laminar Research empfiehlt folgende Vorgehensweise:

1. Alle Slider auf Minimum, alle Checkboxen aus
2. Bottleneck identifizieren: CPU-Zeit vs. GPU-Zeit im FPS-Display vergleichen -- der hoehere Wert ist der Flaschenhals
3. Settings der nicht-limitierenden Komponente schrittweise erhoehen
4. Texturaufloesung inkrementell erhoehen (Neustart noetig), bis FPS sinken -- dann eine Stufe zurueck
5. Visual Effects als naechstes erhoehen
6. Antialiasing und Scenery Shadows erst zuletzt, wenn noch FPS-Headroom vorhanden

**Frame-Time statt FPS:** Laminar Research empfiehlt intern die Nutzung von Frame-Times statt FPS. Die Anzeige zeigt `cpu`, `gpu` und `frame` (tatsaechliche Zeit inkl. System-Overhead). Die Differenz zwischen Frame-Time und CPU/GPU-Zeit repraesentiert "driver and general system overhead".

Quellen:
- https://www.x-plane.com/kb/setting-the-rendering-options-for-best-performance/
- https://developer.x-plane.com/2025/12/a-very-quick-performance-primer/

### 2.3 Empfohlene Einstellungsprofile nach GPU-Klasse

Die folgenden Profile sind aus den offiziellen Empfehlungen und den Benchmark-Daten abgeleitet. **Es existieren keine offiziellen GPU-klassenspezifischen Profile von Laminar Research.** Die Zusammenstellung basiert auf der Kombination aus offizieller Setting-Dokumentation und unabhaengigen Benchmark-Ergebnissen.

#### Profil 1: "Einstieg -- Erstmal fliegen" (GTX 1070 / RX 580 Klasse, 6-8 GB VRAM)

| Einstellung | Wert | Begruendung |
|-------------|------|-------------|
| Visual Effects | Medium | HDR aktiviert fuer grundlegende Lichteffekte |
| Texture Quality | Medium | VRAM-schonend bei 6-8 GB Karten |
| Antialiasing | FXAA | Geringer GPU-Impact, gute Kantenglattung |
| Number of Objects | Medium | CPU-Last begrenzen |
| Shadow Quality | Static/Overlay | Keine globalen Schatten |
| Cloud Quality | Medium | Reduzierte Wolkenpuffs |
| Water Reflections | Minimal | GPU-intensiv, niedrig halten |
| World Detail Distance | Low-Default | Quadratische Skalierung beachten |
| Aufloesung | 1080p | Hoehere Aufloesung ueberfordert diese GPU-Klasse |

**Erwartete Performance:** ~30-45 FPS an Standardflughaefen, ~25-35 FPS an komplexen Flughaefen.

#### Profil 2: "Komfort" (RTX 3060 / RX 6700 XT Klasse, 8-12 GB VRAM)

| Einstellung | Wert | Begruendung |
|-------------|------|-------------|
| Visual Effects | High | Volle HDR-Qualitaet |
| Texture Quality | High | 8-12 GB VRAM ermoeglicht hohe Texturen |
| Antialiasing | FXAA + 4x MSAA | Guter Kompromiss Qualitaet/Performance |
| Number of Objects | High | CPU-limitiert, bei modernem 6-Kerner kein Problem |
| Shadow Quality | 3D on Aircraft | Keine globalen Szenerie-Schatten |
| Cloud Quality | High | Volumetrische Wolken |
| Water Reflections | Medium | Bei Fluessen/Kueste sichtbar |
| World Detail Distance | Default | Alle vorgesehenen Objekte sichtbar |
| Aufloesung | 1080p-1440p | 1440p bei 12 GB VRAM moeglich |

**Erwartete Performance:** ~45-65 FPS bei 1080p an Standardflughaefen, ~35-50 FPS an komplexen Flughaefen.

#### Profil 3: "Hochqualitaet / Screenshots" (RTX 4070/4080 / RX 7800 XT Klasse, 12-16 GB VRAM)

| Einstellung | Wert | Begruendung |
|-------------|------|-------------|
| Visual Effects | Maximum | Alle visuellen Effekte |
| Texture Quality | Maximum | 12-16 GB VRAM erlaubt Maximum |
| Antialiasing | FXAA + 4x MSAA | Maximale Kantenglattung |
| Number of Objects | Maximum | Alle Szenerie-Details sichtbar |
| Shadow Quality | Global | Globale Schatten auf Szenerie |
| Cloud Quality | Maximum | Maximale Wolkendetails |
| Water Reflections | High | Volle Reflexionsberechnung |
| World Detail Distance | High | Maximale Sichtweite |
| Aufloesung | 1440p-4K | 4K bei RTX 4080 / RX 7800 XT+ |

**Erwartete Performance:** ~60-90 FPS bei 1440p, ~40-60 FPS bei 4K. An sehr komplexen Flughaefen mit Addons tiefer.

### 2.4 Typische FPS-Szenarien

Basierend auf offiziellen Richtlinien und Benchmark-Daten:

| Szenario | GPU-Impact | CPU-Impact | Anmerkung |
|----------|-----------|-----------|-----------|
| En-Route, FL350, default Scenery | Niedrig | Niedrig | Hoechste FPS, wenig Objekte |
| Anflug auf mittleren Flughafen | Mittel | Mittel | Steigender Objektcount |
| Grossflughafen (EDDF, KLAX) | Hoch | Hoch | Maximale Belastung |
| Ortho-Scenery (Ortho4XP/AutoOrtho) | Hoch (VRAM) | Niedrig | VRAM-Verbrauch durch hochaufloesende Bodentexturen |
| Nachtflug, viele Lichter | Hoch | Niedrig | Seit 12.2 Tile-basiertes Light-Rendering |
| Bewolkt / Gewitter | Hoch | Niedrig | Volumetrische Wolken, Cloud Shadows |

**Offizieller FPS-Zielbereich:** Laminar Research nennt 20 FPS als absolute Untergrenze, 25-35 FPS als "ideal range" fuer fluessiges Fliegen.

Quelle: https://www.x-plane.com/kb/setting-the-rendering-options-for-best-performance/

---

## 3. Linux-spezifische Performance-Aspekte

### 3.1 Vulkan unter Linux: Architektur

X-Plane 12 nutzt Vulkan als primaere Grafik-API auf Windows und Linux. OpenGL wird ueber Zink (OpenGL-to-Vulkan-Translation) fuer Plugin-Kompatibilitaet bereitgestellt.

**Treiberlandschaft Linux:**
- **NVIDIA:** Proprietaerer Treiber erforderlich (kein Nouveau-Support fuer Vulkan in X-Plane). Minimum: Treiber 510+. Aktuell empfohlen: 580er-Serie (enthielt einen X-Plane-spezifischen Bugfix fuer Workstation-GPUs).
- **AMD:** Mesa RADV mit ACO-Shader-Compiler (Standard seit Mesa 20+). Minimum: Mesa 22.0. AMD hat AMDVLK im September 2025 offiziell eingestellt und konzentriert alle Ressourcen auf RADV.
- **Intel Arc:** Unterstuetzt ab X-Plane 12.3.0 mit ANV-Treiber.

Quellen:
- https://www.x-plane.com/kb/x-plane-12-system-requirements/
- https://github.com/GPUOpen-Drivers/AMDVLK/discussions/416
- https://www.phoronix.com/news/AMDVLK-Discontinued

### 3.2 RADV vs. NVIDIA proprietaer -- Performance-Unterschiede

**Direkte X-Plane 12 Linux-Benchmarks zwischen RADV und NVIDIA fehlen.** Es gibt keine systematische Vergleichsstudie, die unter kontrollierten Bedingungen beide Treiberplattformen mit X-Plane 12 gegenueberstellt.

Indirekte Hinweise aus den OpenBenchmarking-Daten:
- AMD RX 7900 XTX (RADV): 149 FPS vs. NVIDIA RTX 4080 (proprietaer): 127 FPS bei 1080p High
- AMD RX 6800 XT (RADV): 92 FPS -- kein direkter NVIDIA-Vergleich in derselben Leistungsklasse verfuegbar

**Historischer Kontext (X-Plane 11, Phoronix):**
Phoronix testete X-Plane 11.50 mit Vulkan auf Ubuntu 20.04 mit 23 GPUs (15 NVIDIA, 8 AMD). RADV mit ACO-Compiler wurde als essentiell fuer akzeptable Shader-Kompilierungszeiten beschrieben. Detaillierte FPS-Vergleiche befinden sich auf den Folgeseiten des Artikels.

Quelle: https://www.phoronix.com/review/xplane-11-vulkan

**Allgemeine Einschaetzung 2025/2026:**
- RADV hat in vielen Spielen und Anwendungen hoehere Frameraten als AMDVLK geliefert, was AMDs Entscheidung zur Konsolidierung begruendete
- RADV profitiert von Valves aktiver Mitarbeit (Steam Deck)
- NVIDIA proprietaer bleibt stabil und ausgereift fuer Vulkan-Workloads

Quelle: https://www.archyde.com/2025-end-year-benchmark-radv-overtakes-discontinued-amdvlk-in-vulkan-and-ray-tracing-performance-on-rx-9070-series/

### 3.3 Zink -- OpenGL-to-Vulkan-Translation

X-Plane 12 liefert Zink als Uebersetzungsschicht mit, um Plugin-OpenGL-Rendering in native Vulkan-Befehle umzuwandeln:

**Zweck:** Vermeidung der instabilen nativen OpenGL/Vulkan-Interop, insbesondere auf AMD-Hardware.

**Performance-Auswirkung:**
- Ohne Zink (native Interop): bis zu 10 ms pro Frame zusaetzliche Last, in Extremfaellen bis zu 30 ms
- Mit Zink: deutliche Verbesserung. Ein Nutzer berichtete von 32 FPS auf 73 FPS in der Aussenansicht
- FPS-Vergleich aus der Entwicklerdokumentation: Native Vulkan/OpenGL Interop = 50 FPS, Zink Interop = 80 FPS (30 FPS Gewinn)

**Plattformsupport:**
- Linux und Windows: Zink verfuegbar
- macOS: nicht verfuegbar (Metal-basiert)
- NVIDIA: ab 12.1.0 wieder aktiviert (war zuvor wegen Crashes deaktiviert)
- AMD: Hauptnutzniesser, da native OpenGL/Vulkan-Interop besonders problematisch war

**Bekannte Einschraenkungen:**
- Shared OpenGL Contexts fuer Hintergrundverarbeitung "not 100% stable"
- `GL_FRAMEBUFFER_SRGB` Enable/Disable kann zu verschwindenden Rendering-Artefakten fuehren

**Debug-Modus:** `--debug_gl` aktiviert OpenGL-Debug-Callbacks fuer Plugin-Entwickler.

Quellen:
- https://developer.x-plane.com/2023/02/addressing-plugin-flickering/
- https://www.gamingonlinux.com/2023/02/x-plane-12-now-uses-the-open-source-zink-driver-to-help-plugins/

### 3.4 Relevante Umgebungsvariablen

#### 3.4.1 Mesa/RADV (AMD GPUs)

| Variable | Werte | Effekt | Relevanz fuer X-Plane |
|----------|-------|--------|----------------------|
| `MESA_SHADER_CACHE_DIR` | Pfad | Speicherort des On-Disk Shader-Cache (Standard: `~/.cache/mesa_shader_cache`) | Kann auf schnellere SSD umgeleitet werden |
| `MESA_SHADER_CACHE_MAX_SIZE` | z.B. `2G` | Maximale Groesse des Shader-Cache (Standard: 1 GB) | Mehr Cache = weniger Rekompilierung |
| `MESA_SHADER_CACHE_DISABLE` | `true`/`false` | Shader-Cache deaktivieren | Nur fuer Debugging |
| `MESA_VK_WSI_PRESENT_MODE` | `fifo`, `relaxed`, `mailbox`, `immediate` | Ueberschreibt Swapchain-Praesentation | `mailbox` = Tearing-frei mit niedriger Latenz; `immediate` = niedrigste Latenz, aber Tearing |
| `RADV_PERFTEST` | Komma-getrennte Flags | Experimentelle Optimierungen | Nicht fuer Produktivbetrieb empfohlen |
| `RADV_TEX_ANISO` | 1-16 | Erzwingt anisotrope Filterung | Kann Texturqualitaet bei Distanz verbessern |
| `RADV_FORCE_VRS` | `2x2`, `2x1`, `1x2` | Variable Rate Shading erzwingen | 10-30% FPS-Gewinn auf RDNA2+, aber reduzierte Bildqualitaet |

**ACO-Shader-Compiler:** ACO ist seit Mesa 20+ der Standard-Shader-Compiler fuer RADV. Er kompiliert SPIR-V ueber NIR mit Optimierungen. LLVM dient nur noch als Backup fuer Testing/Hardware-Bringup.

**RADV_FORCE_VRS Detail:**
Variable Rate Shading rendert Bloecke von z.B. 2x2 Pixeln gemeinsam statt jeden Pixel einzeln. Benchmarks zeigen 10-20% FPS-Gewinn in vielen Spielen, bis zu 30% in Einzelfaellen. Unterstuetzt auf RDNA2 (RX 6000) und neuer. VRS wird automatisch deaktiviert, wenn die visuelle Qualitaet zu stark leiden wuerde. **Nicht spezifisch mit X-Plane 12 getestet -- keine Quelle fuer X-Plane-spezifische VRS-Ergebnisse vorhanden.**

Quellen:
- https://docs.mesa3d.org/envvars.html
- https://docs.mesa3d.org/drivers/radv.html
- https://www.phoronix.com/review/radeon-radv-vrs

#### 3.4.2 NVIDIA (proprietaerer Treiber)

| Variable | Werte | Effekt | Relevanz fuer X-Plane |
|----------|-------|--------|----------------------|
| `__GL_THREADED_OPTIMIZATIONS` | `0`/`1` | OpenGL-CPU-Arbeit in Worker-Thread auslagern | **Nur OpenGL**, nicht Vulkan. Fuer X-Plane 12 (Vulkan) irrelevant |
| `__GL_YIELD` | `NOTHING`/`USLEEP` | CPU-Yield-Verhalten bei OpenGL-Waits | **Nur OpenGL**, nicht Vulkan |

**Wichtig:** Die `__GL_*`-Variablen betreffen ausschliesslich OpenGL. X-Plane 12 nutzt primaer Vulkan, daher sind diese Variablen fuer die Haupt-Rendering-Pipeline nicht relevant. Sie koennten theoretisch Plugin-Rendering ueber Zink beeinflussen, aber dafuer gibt es keine Dokumentation.

Quelle: https://download.nvidia.com/XFree86/Linux-x86_64/435.17/README/openglenvvariables.html

### 3.5 Shader-Kompilierung und -Cache

X-Plane 12 verwendet **zwei separate Shader-Cache-Systeme:**

**1. X-Plane-eigener Shader-Cache:**
- Speicherort: `<X-Plane-Installationspfad>/Output/shadercache/vulkan/`
- Enthaelt vorkompilierte Vulkan-Pipeline-Objekte
- Kann bei Problemen (Crashes, Performance-Anomalien) geloescht werden -- wird beim naechsten Start neu aufgebaut
- Neuaufbau kann mehrere Minuten dauern

**2. Mesa Shader-Cache (nur AMD/Intel):**
- Standard-Speicherort: `~/.cache/mesa_shader_cache/` (folgt XDG-Konventionen)
- Ueberschreibbar mit `MESA_SHADER_CACHE_DIR`
- Standard-Maximum: 1 GB (ueberschreibbar mit `MESA_SHADER_CACHE_MAX_SIZE`)
- Cacht von ACO kompilierte Shader auf Treiberebene
- NVIDIA proprietaer hat einen eigenen internen Shader-Cache

**ACO bei AMD:**
ACO (AMD COmpiler) ist der Standard-Shader-Compiler in RADV. Der Kompilierungspfad: SPIR-V -> NIR -> Optimierungspasses -> ACO -> GPU-nativer Code. ACO wurde als essenziell fuer akzeptable Shader-Kompilierungszeiten beschrieben (Phoronix X-Plane 11 Benchmark).

Quellen:
- https://docs.mesa3d.org/envvars.html
- https://docs.mesa3d.org/drivers/radv.html

### 3.6 Compositor-Impact: X11 vs. Wayland

**Aktueller Stand:**
X-Plane 12 hat **keine native Wayland-Unterstuetzung**. Es laeuft unter Wayland-Sitzungen ueber XWayland.

**Performance-Auswirkungen:**
- Unter X11 koennen Fullscreen-Anwendungen den Compositor umgehen (Compositor-Bypass), was den Overhead eliminiert
- Unter Wayland/XWayland gibt es keinen Compositor-Bypass fuer XWayland-Fenster -- es erfolgt eine zusaetzliche Kopie
- Phoronix-Tests (2023) zeigten, dass X-Plane auf NVIDIA-Hardware unter X.Org besser performte als unter Wayland/GNOME 43

**Empfehlung:** Fuer maximale Performance X11-Sitzung verwenden. Unter Wayland ist XWayland funktional, aber mit potenziellem Overhead.

**Bekannte Wayland-Probleme mit X-Plane 12:**
- 12.1.4: Fehler beim Fenstergroesse-aendern unter Wayland (behoben)
- Fullscreen-Verhalten kann unter XWayland unzuverlaessig sein
- Cursor-Capture kann problematisch sein

Quellen:
- https://www.phoronix.com/review/wayland-nv-amd-2023/4
- https://www.x-plane.com/kb/x-plane-12-1-0-release-notes/ (12.1.4 Wayland-Fix)

### 3.7 Bekannte Linux-spezifische Performance-Probleme

| Problem | Version | Status | Referenz |
|---------|---------|--------|----------|
| Haengt bei IPv6-Abfrage (Kernel 6.9.0) | 12.1.0 | Behoben | XPD-15378 |
| Startet nur im Fenstermodus statt Vollbild | 12.1.0 | Behoben | XPD-14462 |
| Zink-Crash mit Plugins (AMD) | 12.1.0 | Behoben | XPD-15411, 15415, 15416 |
| X-Plane startet nicht mit AMD GPU | 12.2.0 | Behoben | Release Notes 12.2.0 |
| Wasser/Vegetation falsch auf AMD GPUs | 12.2.0 | Behoben | XPD-16632 |
| Kein Vollbild auf manchen Linux-Installationen | 12.2.0 | Behoben | XPD-16610 |
| Startet nicht auf Ubuntu 24.10 mit NVIDIA | 12.2.0 | Behoben | XPD-16457 |
| Exposure Fusion fehlerhaft auf AMD GPUs | 12.3.0 | Behoben | XPD-17267 |
| Screenshot-Fehler mit AMD GPUs | 12.3.0 | Behoben | Release Notes 12.3.0 |
| Wayland: Fenstergroesse-Fehler | 12.1.4 | Behoben | Release Notes 12.1.4 |
| Steam-Snap-Paket auf Linux | 12.2.1 | Behoben (Snap unsupported) | XPD-16840 |
| Zink GPU-Auswahl bei Multi-GPU | 12.4.0 | Hinzugefuegt | Release Notes 12.4.0 |
| Ubuntu 20.04 LTS Support | 12.1.3 | Entfallen | Release Notes 12.1.3 |

Quellen:
- https://www.x-plane.com/kb/x-plane-12-1-0-release-notes/
- https://www.x-plane.com/kb/x-plane-12-2-0-release-notes/
- https://www.x-plane.com/kb/x-plane-12-3-0-release-notes/
- https://www.x-plane.com/kb/x-plane-12-4-0-release-notes/

### 3.8 Linux vs. Windows Performance

**Es existieren keine systematischen X-Plane 12 Benchmarks, die Linux und Windows direkt vergleichen.** Die OpenBenchmarking-Daten stammen ueberwiegend von Linux-Systemen, aber ohne kontrollierte Windows-Gegenueberstellung.

Allgemeine Einschaetzung basierend auf der Vulkan-Architektur:
- Vulkan als Cross-Platform-API bietet auf beiden Plattformen aequivalenten Low-Level-GPU-Zugriff
- NVIDIA-proprietaerer Treiber: aehnliche Codebasis fuer Windows und Linux
- AMD RADV (Linux) vs. AMD Adrenaline (Windows): unterschiedliche Codebasis, aber beide ausgereift
- Zink-Performance kann zwischen Plattformen variieren

**Keine zuverlaessige Quelle fuer einen quantitativen Linux-vs-Windows-Vergleich mit X-Plane 12 verfuegbar.**

---

## 4. X-Plane 12 Versionshistorie (Performance-relevant)

### 4.1 Version 12.0.x (Initial Release, 2022-2023)

**Rendering-System:**
- Vulkan als primaere Grafik-API
- Async-Compute-Optimierung
- Tone-Mapping: GPU-Blending zu CPU-Readback verschoben

**Bekannte Probleme:**
- Zink-Crashes auf Linux mit AMD und Mesa 23.1.x
- Zink permanent deaktiviert fuer NVIDIA (wegen Crashes)
- RDNA 3 GPUs: Zink-Rendering fehlerhaft

**VRAM:** Mindestanforderung als 2 GB kommuniziert (Warnung wurde spaeter angepasst).

Quelle: https://www.x-plane.com/kb/x-plane-12-00-release-notes/

### 4.2 Version 12.1.0 (2024) -- Stabilitaets-Update

**Performance-Verbesserungen:**
- VRAM-Streaming: Hintergrund-Threads blockierten Main-Thread -> Stutter behoben (XPD-15525)
- Render-Graph: massiv verbesserte Rebuild-Zeiten
- Modern Collector: weniger Draw Calls, korrekte Layer-Sortierung (XPD-15655)
- FP16-Dekompression fuer Wasser optimiert (XPD-14749): 5% Main-Thread-Anteil eliminiert
- Water FFT: unnoetige Device-Memory-Streams entfernt (XPD-15652)

**Zink-Meilenstein:**
- Zink fuer NVIDIA wieder aktiviert (Beta 6)
- Zink-Crashes auf Linux behoben (XPD-15411)

**Linux-Fixes:**
- IPv6-Haenger bei Kernel 6.9.0 behoben
- Vollbild-Start behoben
- XLua-Crash (moeglicherweise Linux-only) behoben
- Steam-CTD bei Locale-Setup behoben

**Rendering:**
- FXAA immer mit MSAA aktiviert
- Smoothed Shadows
- Cloud Shadows auf Wasser

Quelle: https://www.x-plane.com/kb/x-plane-12-1-0-release-notes/

### 4.3 Version 12.1.2 (Oktober 2024)

**Kritischer Performance-Fix:**
- Gebaeude wurden beim zweiten Ueberfliegen derselben Region doppelt gezeichnet -> "huge performance impact" behoben

Quelle: https://www.x-plane.com/kb/x-plane-12-1-2-release-notes/

### 4.4 Version 12.1.3-12.1.4 (Ende 2024 / Anfang 2025)

**12.1.3:**
- Verbessertes VRAM-Handling bei GPU-VRAM-Knappheit
- DMABUF-Rendering deaktiviert (Workaround fuer libwebkit2gtk + NVIDIA)
- Ubuntu 20.04 LTS Support entfallen

**12.1.4:**
- Wayland-Fenstergroesse-Fehler behoben
- Keine signifikanten Performance-Aenderungen

Quellen:
- https://www.x-plane.com/kb/x-plane-12-1-3-release-notes/
- https://www.x-plane.com/kb/x-plane-12-1-4-release-notes/

### 4.5 Version 12.2.0 (April 2025) -- Graphics Update

**Groesstes grafisches Update seit Release:**

**Shader-Compiler:**
- Neuer Shader-Compiler mit "significantly better resource allocation"
- Statische Descriptor-Sets reduzieren pro-Frame Datenverarbeitung

**VRAM-Management:**
- Ueberarbeitetes VRAM-Allokationssystem
- Priorisierung kleinerer Speicheranfragen vor groesseren
- Fuenf Allokationsversuche vor Fehlschlag
- Reduziert unscharfe Texturen und Leistungseinbrueche

**Cloud-Rendering (komplett ueberarbeitet):**
- Neues volumetrisches Wolkensystem mit verbessertem Schattendetail
- Wolken werfen Schatten aufeinander und zwischen Schichten
- Neuer Cloud-Shaping-Algorithmus
- High-Quality-Rendering-Radius um Kamera (kein Cloud-Pixeling mehr nah am Flugzeug)

**Lichtrendering:**
- Tile-basiertes Lichtrendering (besonders bei Nacht und grossen Flughaefen)
- GPU-Last wird in Kacheln aufgeteilt fuer bessere Thread-Verteilung

**Tone-Mapping:**
- AgX Tone-Mapper ersetzt Custom-ACES-Blend
- Exposure Fusion fuer Innenansichten (Balance hell/dunkel)
- Rekalibrierte Rayleigh-, Ozon-, Mie-Streuung

**Allgemein:**
- Micro-Stutters bei niedrigen Flughoehen behoben
- CPU-Spikes bei Real-World-Weather behoben (XPD-16532)
- GPU wechselte zwischen zwei Texturskalen (XPD-16437) -> behoben

**Linux-Fixes:**
- AMD GPU: X-Plane startete nicht -> behoben
- AMD GPU: Wasser/Vegetation fehlerhaft -> behoben (XPD-16632)
- Kein Vollbild auf manchen Installationen -> behoben (XPD-16610)
- Ubuntu 24.10 + NVIDIA: Start-Problem -> behoben (XPD-16457)
- Inkrementeller Host-Memory-Leak bei NVIDIA ohne ReBar -> behoben

Quellen:
- https://www.x-plane.com/kb/x-plane-12-2-0-release-notes/
- https://www.x-plane.com/2025/04/whats-new-in-x-plane-12-2-0/

### 4.6 Version 12.3.0 (September 2025) -- Weather Update

**Performance:**
- Cloud-Rendering-Performance verbessert
- Replay-System-Performance verbessert
- TrackIR-Performance verbessert
- Wheel-Smoke-Partikel optimiert
- Stutter durch X1000 behoben (XPD-17118)
- Control Pad verursacht nicht mehr massiven Performance-Einbruch (XPD-17269)
- Frame-Limiting gegen Stutter bei Swapchain-Acquisition (XPD-17244)

**Job-System (Grundstein fuer Multi-Core):**
- Neues Job-System eingefuehrt, das Frame-Arbeit als individuelle Jobs mit Abhaengigkeiten beschreibt
- System "figured out the optimal way to dispatch them" statt manueller C++-Koordination
- Basis fuer die Multi-Core-Szenerieverarbeitung in 12.4

**AMD-Fixes:**
- Screenshot-Funktionalitaet auf AMD GPUs
- Exposure Fusion auf AMD GPUs (XPD-17267)

**Intel-Fixes:**
- Crash mit Intel ARC GPUs behoben

**Neue Features mit Performance-Impact:**
- Echtzeit-Wetterradar (WXR) mit 3D-Cloud-Scanning
- NEXRAD und WXR APIs

Quellen:
- https://www.x-plane.com/kb/x-plane-12-3-0-release-notes/
- https://www.x-plane.com/2025/09/whats-new-in-12-3-0/

### 4.7 Version 12.4.0 (Dezember 2025, Beta) -- C-Check Update

**Multi-Core Szenerieverarbeitung (Hauptfeature):**
- X-Plane nutzt jetzt mehrere CPU-Kerne fuer Szenerie-Vorbereitung
- Scene-Graph-Traversal (bis zu 75% der Frame-Time) parallelisiert
- Parallelisiert: Shadow-Rendering Traversal, Main-Scene Traversal, Panel/Avionics Updates

**Interne Benchmark-Ergebnisse:**
| Metrik | Vorher | Nachher | Verbesserung |
|--------|--------|---------|-------------|
| P1 (Best Case) CPU-Zeit | 20,8 ms | 15,0 ms | 28% |
| Durchschnitt | 30,1 ms | 21,6 ms | 28% |
| P99 (Worst Case) | 49,7 ms | 30,8 ms | 38% |

**Variabilitaet in der Praxis:**
- Alpha-Tester: Ergebnisse reichen von +15,8% Gewinn bis -24,4% Regression
- GPU-limitierte Systeme: kein Vorteil (Multi-Threading betrifft nur CPU)
- "Foundational work" -- explizit als Grundstein fuer weitere Optimierungen beschrieben

**Einschraenkungen:**
- Das tatsaechliche Zeichnen der Szene ist weiterhin single-threaded
- Main-Thread erstellt einen Command Buffer nach Abschluss des parallelen Traversals
- Multi-Monitor: Sequentielles Traversal pro Monitor (theoretisch groesseres Potential)

**Weitere Performance-Aenderungen:**
- AMD X3D CPUs: spezifische Optimierungen
- Avionics Pop-Out: FPS-Penalty eliminiert
- Cockpit-Displays von FXAA ausgenommen (Lesbarkeit ohne Performance-Kosten)
- VSync-Probleme behoben

**Linux:**
- GPU-Auswahl fuer Zink bei Multi-GPU-Systemen hinzugefuegt

**Geplante Zukunft:**
- Paralleles Rendering (nicht nur Traversal)
- Gleichzeitiges Multi-Monitor-Processing
- Simultanes Shadow/Main Rendering mit sequentieller GPU-Submission

Quellen:
- https://www.x-plane.com/kb/x-plane-12-4-0-release-notes/
- https://www.x-plane.com/2025/12/whats-new-in-12-4-0/
- https://developer.x-plane.com/2025/12/the-glorious-multi-core-future-is-now-the-boring-present/

### 4.8 Roadmap 2026

Laut offizieller Roadmap (Dezember 2025):
- **Multi-Threading:** Weitere Ausbauschritte geplant (paralleles Rendering, Multi-Monitor)
- **Next-Gen Scenery:** Hoechste Prioritaet, aber massives Projekt (DSF-System ist ca. 20 Jahre alt)
- **X-Plane Store:** In-App-Kaeufe (eingefuehrt 12.3.2), Ausbau geplant
- **Besseres Anti-Aliasing:** In Entwicklung
- **Flight Model Improvements:** Angekuendigt

Keine Linux-spezifischen Features in der Roadmap erwaehnt.

Quelle: https://www.x-plane.com/2025/12/x-plane-roadmap-update-december-2025/

---

## 5. X-Plane Performance-Monitoring und -Diagnose

### 5.1 Integriertes FPS-Display

X-Plane zeigt drei Metriken:
- `cpu`: CPU-Frame-Time in Millisekunden
- `gpu`: GPU-Frame-Time in Millisekunden
- `frame`: Tatsaechliche Frame-Time (inkl. System-Overhead)

**Interpretation:** Der hoehere Wert von `cpu` und `gpu` ist der Flaschenhals. Die Differenz `frame - max(cpu, gpu)` ist Treiber-/System-Overhead.

**Umrechnung:** FPS = 1000 / frame_time_ms (z.B. 16,6 ms = 60 FPS, 33,3 ms = 30 FPS)

### 5.2 Built-in Frame Rate Test

X-Plane bietet einen automatisierten Benchmark-Modus:
- Aufruf: `--fps_test=N` (N = dreistelliger Code: Hunderterstelle=Viewpoint, Zehnerstelle=Wetter, Einerstelle=Qualitaet)
- Laeuft 90 Sekunden in drei 30-Sekunden-Phasen
- Ergebnisse werden in Log.txt geschrieben
- `--require_fps=N` fuer automatisierte Pass/Fail-Tests

Quelle: https://www.x-plane.com/kb/frame-rate-test/

### 5.3 Linux-Monitoring-Tools

| Tool | GPU-Typ | Funktion |
|------|---------|----------|
| `nvidia-smi` | NVIDIA | GPU-Auslastung, VRAM, Temperatur |
| `radeontop` | AMD | GPU-Auslastung, VRAM |
| `intel_gpu_top` | Intel | GPU-Auslastung |
| `MangoHud` | Alle | In-Game Overlay (FPS, Frame-Time, GPU/CPU-Metriken) |
| `htop` | -- | CPU-Auslastung pro Kern |
| `GALLIUM_HUD` | Mesa | Echtzeit-Performance-Metriken (Mesa-spezifisch) |
| `MESA_SHADER_CACHE_SHOW_STATS=true` | Mesa | Hit/Miss-Statistiken fuer Shader-Cache |

---

## 6. Zusammenfassung der Luecken

Folgende Punkte konnten trotz umfangreicher Recherche nicht mit zuverlaessigen Primaerquellen belegt werden:

1. **Keine offiziellen GPU-klassenspezifischen Einstellungsprofile** von Laminar Research -- die Profile in Abschnitt 2.3 sind Ableitungen
2. **Keine systematischen Linux-vs-Windows-Benchmarks** fuer X-Plane 12
3. **Keine systematischen RADV-vs-NVIDIA-Benchmarks** spezifisch fuer X-Plane 12
4. **Keine exakten VRAM-Verbrauchszahlen pro Einstellungsstufe** -- der Verbrauch variiert stark nach Szenerie und Addons
5. **Keine X-Plane-spezifischen Tests** von RADV_FORCE_VRS (Variable Rate Shading)
6. **Keine offiziellen FPS-Angaben** von Laminar Research fuer bestimmte GPU/Setting-Kombinationen (nur "25-35 FPS ideal range")
7. **Keine Dokumentation** zum Zusammenspiel von NVIDIA-Umgebungsvariablen und Zink in X-Plane

---

## Quellenverzeichnis

### Offizielle X-Plane-Dokumentation
- System Requirements: https://www.x-plane.com/kb/x-plane-12-system-requirements/
- Rendering Options Best Performance: https://www.x-plane.com/kb/setting-the-rendering-options-for-best-performance/
- Configuring Rendering Options: https://www.x-plane.com/kb/configuring-the-rendering-options/
- Frame Rate Test: https://www.x-plane.com/kb/frame-rate-test/
- Virtual Memory: https://www.x-plane.com/kb/configuring-x-plane-to-use-less-virtual-memory/
- Linux Troubleshooting: https://www.x-plane.com/kb/linux-troubleshooting/
- Desktop Manual: https://www.x-plane.com/manuals/desktop/

### X-Plane Release Notes
- 12.00: https://www.x-plane.com/kb/x-plane-12-00-release-notes/
- 12.1.0: https://www.x-plane.com/kb/x-plane-12-1-0-release-notes/
- 12.1.2: https://www.x-plane.com/kb/x-plane-12-1-2-release-notes/
- 12.1.3: https://www.x-plane.com/kb/x-plane-12-1-3-release-notes/
- 12.1.4: https://www.x-plane.com/kb/x-plane-12-1-4-release-notes/
- 12.2.0: https://www.x-plane.com/kb/x-plane-12-2-0-release-notes/
- 12.2.1: https://www.x-plane.com/kb/x-plane-12-2-1-release-notes/
- 12.3.0: https://www.x-plane.com/kb/x-plane-12-3-0-release-notes/
- 12.4.0: https://www.x-plane.com/kb/x-plane-12-4-0-release-notes/

### X-Plane Developer Blog
- Addressing Plugin Flickering (Zink): https://developer.x-plane.com/2023/02/addressing-plugin-flickering/
- VRAM Management: https://developer.x-plane.com/2020/01/all-your-vram-is-belonging-to-us-and-plugins/
- Fighting Blurry Textures: https://developer.x-plane.com/2020/05/fighting-blurry-textures/
- Performance Primer: https://developer.x-plane.com/2025/12/a-very-quick-performance-primer/
- Multi-Core Future: https://developer.x-plane.com/2025/12/the-glorious-multi-core-future-is-now-the-boring-present/

### X-Plane Blog Posts (Whats New)
- Whats New 12.2.0: https://www.x-plane.com/2025/04/whats-new-in-x-plane-12-2-0/
- Whats New 12.3.0: https://www.x-plane.com/2025/09/whats-new-in-12-3-0/
- Whats New 12.4.0: https://www.x-plane.com/2025/12/whats-new-in-12-4-0/
- Roadmap Dezember 2025: https://www.x-plane.com/2025/12/x-plane-roadmap-update-december-2025/

### Linux/Mesa/Vulkan
- Mesa Environment Variables: https://docs.mesa3d.org/envvars.html
- RADV Documentation: https://docs.mesa3d.org/drivers/radv.html
- NVIDIA OpenGL Environment Variables: https://download.nvidia.com/XFree86/Linux-x86_64/435.17/README/openglenvvariables.html
- AMDVLK Discontinued: https://github.com/GPUOpen-Drivers/AMDVLK/discussions/416
- AMDVLK Confirmed End: https://www.phoronix.com/news/AMDVLK-Discontinued
- RADV VRS Benchmarks: https://www.phoronix.com/review/radeon-radv-vrs

### Benchmarks
- OpenBenchmarking X-Plane 12: https://openbenchmarking.org/test/pts/xplane12
- Phoronix X-Plane 11 Vulkan: https://www.phoronix.com/review/xplane-11-vulkan
- Phoronix Wayland vs X11: https://www.phoronix.com/review/wayland-nv-amd-2023/4
- RADV vs AMDVLK Benchmarks: https://www.archyde.com/2025-end-year-benchmark-radv-overtakes-discontinued-amdvlk-in-vulkan-and-ray-tracing-performance-on-rx-9070-series/

### Community-Quellen (informativ, nicht als Primaerquelle)
- GamingOnLinux Zink: https://www.gamingonlinux.com/2023/02/x-plane-12-now-uses-the-open-source-zink-driver-to-help-plugins/
- Phoronix Zink: https://www.phoronix.com/news/X-Plane-Zink-Shipping
