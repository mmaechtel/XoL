# GPU & VRAM

## Einleitung

Das Kapitel [CPU & RAM](cpu_ram.md) beschreibt, wie X-Plane seine Kerne nutzt und wie Ortho-Streaming-Tools als eigenständige Prozesse daneben laufen. Dieses Kapitel folgt den Daten auf ihrem Weg in den Grafikspeicher: Wie X-Plane [VRAM](../../glossary.md#vram-video-ram) verwaltet, warum sich GPU-Treiber unter Linux fundamental unterscheiden und wie sich die Auswirkungen auf die Frame Time messen lassen.

## Architektur: Vom Streaming-Tool zum VRAM

Alle verbreiteten Ortho-Streaming-Lösungen — [AutoOrtho](../../glossary.md#autoortho), XPME, XEarthLayer — folgen demselben Architekturprinzip:

```
Streaming-Tool                      X-Plane
┌─────────────────────┐            ┌──────────────────────┐
│ Tile-Download        │            │                      │
│ Tile-Decoding        │  FUSE     │ Texture Pager         │
│ Cache-Management     │ ───────►  │ (Disk → RAM → VRAM)  │
│ FUSE-Dateisystem     │ Dateien   │                      │
└─────────────────────┘            └──────────────────────┘
```

**Kein Streaming-Tool greift direkt auf den VRAM zu.** Die Tools stellen lediglich Bilddateien über ein [FUSE](../../glossary.md#fuse-filesystem-in-userspace)-Dateisystem bereit — aus Sicht von X-Plane sind das gewöhnliche [Custom-Scenery](../../glossary.md#custom-scenery)-Texturen. X-Plane liest diese über seinen eigenen Texture Pager ein und lädt sie in seinen VRAM-Pool. Die VRAM-Belastung ist daher bei allen Ortho-Lösungen identisch — X-Plane verarbeitet die Texturen stets auf dieselbe Weise.

Diese Architektur hat eine wichtige Konsequenz: Die Konfiguration des Streaming-Tools beeinflusst, *welche* Texturen bereitstehen und *wie schnell* sie verfügbar sind — aber die VRAM-Verwaltung liegt vollständig bei X-Plane.

## VRAM-Management

### Asynchrones Texture Paging

X-Plane lädt Texturen asynchron in drei Stufen:

1. **Disk → RAM:** Die Texturdatei wird von der SSD (oder dem FUSE-Dateisystem) in den Arbeitsspeicher gelesen
2. **RAM → GPU-Upload:** Die Textur wird dekomprimiert, Mipmaps werden generiert, dann erfolgt der Upload in den VRAM
3. **VRAM-Verwaltung:** X-Plane entscheidet anhand der Kameraposition, welche Texturen geladen bleiben und welche ausgelagert werden

Dieser Prozess läuft im Hintergrund, wie im Kapitel [CPU & RAM](cpu_ram.md) beschrieben. Reicht der VRAM nicht aus, skaliert X-Plane die Texturauflösung automatisch herunter — statt eines Absturzes erscheinen unscharfe Texturen.

### VRAM-Budgetierung

Der VRAM-Verbrauch setzt sich aus mehreren Komponenten zusammen:

| Komponente | Typischer Anteil | Einflussfaktor |
|---|---|---|
| Scenery-Texturen | Größter Anteil | [Zoom Level](../../glossary.md#zl-zoom-level), Sichtweite |
| Flugzeug-Texturen | Mehrere GB | Cockpit-Auflösung, Liveries |
| Rendering-Puffer | 1–3 GB | Schatten, Reflektionen, [HDR](../../glossary.md#hdr) |
| UI und Overlays | Gering | AviTab, Karten, Menüs |

[Orthofotos](../../glossary.md#orthofotos) beanspruchen den größten Anteil. Entscheidend ist der [Zoom Level](../../glossary.md#zl-zoom-level) (ZL): Jede ZL-Stufe vervierfacht die Datenmenge pro Fläche.

| Zoom Level | Bodenauflösung | Daten pro Fläche (relativ) |
|---|---|---|
| ZL 16 | ca. 2,4 m/Pixel | 1× |
| ZL 17 | ca. 1,2 m/Pixel | 4× |
| ZL 18 | ca. 0,6 m/Pixel | 16× |

Die VRAM-Anforderungen steigen exponentiell — nicht linear. Ein Flugzeug mit hochauflösendem Cockpit belegt bereits mehrere Gigabyte VRAM, bevor die erste Ortho-Textur geladen ist. Das gesamte Budget muss kalkuliert werden, nicht nur der Ortho-Anteil.

## GPU-Treiber und VRAM-Oversubscription

Wenn X-Plane mehr VRAM anfordert als physisch verfügbar ist, unterscheidet sich das Verhalten je nach GPU-Treiber-Stack erheblich. Dieses Verhalten — VRAM-Oversubscription — ist einer der relevantesten Unterschiede zwischen GPU-Herstellern und Betriebssystemen.

### Linux: Treiberabhängiges Verhalten

**Proprietäre NVIDIA-Treiber**

Bieten unter Linux kein transparentes Paging in den System-RAM. Bei VRAM-Überlauf reagiert X-Plane mit aggressivem Textur-Downscaling. Im Extremfall kommt es zu Stutter oder Device Loss. Dies ist die empfindlichste Kombination und erfordert sorgfältige VRAM-Budgetierung.

**[Mesa](../../glossary.md#mesa)/[RADV](../../glossary.md#radv) (AMD)**

Die Open-Source-Treiber bieten bessere Oversubscription durch den GTT-Mechanismus (Graphics Translation Table), der Texturen teilweise in den System-RAM auslagert. Toleranter als NVIDIA, aber bei starker Überzeichnung mit Performance-Einbrüchen.

**Mesa/ANV (Intel Arc)**

Bietet die beste Oversubscription unter Linux. Am tolerantesten gegenüber VRAM-Überlauf.

### Windows: WDDM-Paging

Unter Windows ermöglicht der WDDM-Treiber (Windows Display Driver Model) automatisches Paging zwischen VRAM und System-RAM — unabhängig vom GPU-Hersteller. Dieser architekturelle Unterschied erklärt, warum Ortho-Konfigurationen, die unter Windows problemlos funktionieren, unter Linux zu Problemen führen können.

### Device Loss vs. VRAM-Problem

Ein häufiges Missverständnis verdient Klarstellung:

| Symptom | Ursache | Maßnahme |
|---|---|---|
| Device Loss (GPU-Crash) | Shader- oder Treiberfehler | Treiber-Diagnostik, Treiber aktualisieren |
| Unscharfe Texturen | VRAM-Überlauf → Downscaling | Zoom Level reduzieren, Texture Quality senken |
| Out-of-Memory-Fehler | VRAM komplett erschöpft | VRAM-Budget reduzieren |

**Device Loss ist kein VRAM-Problem.** Ein Device Loss bedeutet, dass die GPU abgestürzt ist — ein fundamentaler Fehler im Shader oder Treiber. VRAM-Engpässe äußern sich durch Textur-Downscaling oder OOM-Fehler, nicht durch Abstürze. Die Unterscheidung ist für die Fehlerdiagnose entscheidend.

## Frame-Time-Perzentile

Durchschnittliche [FPS](../../glossary.md#fps-frames-per-second)-Werte verschleiern die tatsächliche Erfahrung. Aussagekräftiger sind Perzentil-Werte der [Frame Time](../../glossary.md#frame-time):

| Perzentil | Bedeutung | Typisches Erlebnis |
|---|---|---|
| P50 (Median) | 50 % aller Frames sind schneller | Grundsätzliche Flüssigkeit — so fühlt sich die Simulation *meistens* an |
| P95 | 95 % aller Frames sind schneller | Die gelegentlichen Ruckler — spürbar, aber selten |
| P99 | 99 % aller Frames sind schneller | Die schlimmsten Hänger — kurze Freezes beim Laden dichter Flughäfen oder neuer Ortho-Kacheln |

??? abstract "Hintergrund: Warum Durchschnitt trügt"

    Eine Simulation mit 40 FPS im Durchschnitt kann sich flüssig oder ruckelig anfühlen — je nach Verteilung. Liegt P99 bei 150 ms, bedeutet das: Etwa einmal pro Sekunde hängt ein einzelner Frame fast eine Sechstelsekunde. Der FPS-Counter zeigt "40", aber das Bild stockt spürbar. Erst die Perzentil-Werte offenbaren diese Ausreißer.

### Relevanz für VRAM und Ortho-Streaming

VRAM-Druck ist eine der Hauptursachen für schlechte P95/P99-Werte:

- **Textur-Nachladen:** Wenn neue Ortho-Kacheln in den VRAM geladen werden, entsteht ein kurzer Upload-Burst, der den Render-Thread verzögert
- **Downscaling-Entscheidungen:** Bei VRAM-Überlauf muss X-Plane entscheiden, welche Texturen herunterskaliert werden — diese Entscheidung kostet Frame Time
- **Cache-Misses:** Wenn eine Textur aus dem VRAM verdrängt wurde und erneut benötigt wird, muss sie komplett neu geladen werden

### Multi-Threading und Perzentile

Wie im Kapitel [CPU & RAM](cpu_ram.md) beschrieben, verbessert Multi-Threading die durchschnittlichen FPS oft nur geringfügig. Der entscheidende Gewinn liegt bei P95 und P99: Wenn das Scenery-Processing nicht mehr den Hauptthread blockiert, werden die schlimmsten Einzelframes kürzer.

Ohne Multi-Threading muss ein einzelner Kern alles abarbeiten — bei einem schweren Scenery-Chunk bleibt er stecken und erzeugt einen Stutter. Mit Multi-Threading verteilt sich die Last auf mehrere Kerne, und die Spitzen werden geglättet.

**Zusammengefasst:**

- **P50** (Durchschnitt) → kaum Veränderung durch Multi-Threading
- **P95** (gelegentliche Ruckler) → deutliche Verbesserung
- **P99** (schlimmste Hänger) → stärkste Verbesserung

## Praktische Konsequenzen

**Zoom Level konservativ wählen**

Der VRAM-Verbrauch steigt nicht linear, sondern exponentiell mit dem ZL. Ein Schritt von ZL 17 auf ZL 18 vervierfacht den Texturspeicherbedarf. Im Zweifel eine Stufe niedriger wählen und stabile Frame Times gewinnen.

**Texture Quality bewusst setzen**

Die X-Plane-Einstellung „Texture Quality" beeinflusst, wie viel VRAM für Nicht-Ortho-Texturen reserviert wird. „High" statt „Maximum" kann mehrere Gigabyte VRAM freigeben, die dann für Orthofotos zur Verfügung stehen.

**VRAM-Monitoring nutzen**

GPU-Monitoring-Tools zeigen die aktuelle VRAM-Auslastung in Echtzeit. Entscheidend ist nicht der Spitzenwert, sondern das Verhalten über Zeit: Steigt die Auslastung kontinuierlich an (mögliches Leak), pendelt sie sich ein (stabiler Betrieb), oder schlägt sie regelmäßig an die Grenze (Downscaling-Zone)?

Siehe [System Monitoring](../../linux/system/systemtools.md) für GPU-Monitoring-Tools.

**Gesamtbudget kalkulieren**

Nicht nur die Ortho-Texturen, sondern alle VRAM-Verbraucher berücksichtigen: Flugzeug, Rendering-Puffer, Overlays. Ein hochdetailliertes Cockpit-Flugzeug bei ZL 18 kann selbst eine GPU mit großem VRAM-Budget an die Grenze bringen.

## Weiterführend

| Thema | Seite |
|---|---|
| Threading-Modell und CPU-Budget | [CPU & RAM](cpu_ram.md) |
| Lastdimensionen und Wechselwirkungen | [Performance-Übersicht](performance_overview.md) |
| GPU-Treiber-Optimierung | [Nvidia](../../linux/optimizations/nvidia.md) |
| Ortho-Streaming-Konfiguration | [AutoOrtho](../../scenery/ortho_streaming/autoortho.md) |
| X-Plane Microprofiler | [X-Plane Performance](../../xplane/performance.md) |
| System Monitoring | [Monitoring](../../linux/system/systemtools.md) |
