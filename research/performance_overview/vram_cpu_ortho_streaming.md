# CPU- und VRAM-Auslastung bei Ortho-Streaming — Konzeptbericht

**Ziel-Seite:** `docs/{lang}/fundamentals/` (neues Kapitel im Grundlagen-Abschnitt)
**Erstellt:** 2026-02-17
**Fokus:** Zeitlose Konzepte — keine Versionsnummern, keine spezifischen Treiber oder GPU-Modelle

---

## Kernkonzept: Wie Ortho-Streaming-Tools mit X-Plane interagieren

Alle verbreiteten Ortho-Streaming-Lösungen folgen demselben Architekturprinzip:

```
Streaming-Tool (CPU + RAM)          X-Plane (CPU + GPU)
┌─────────────────────┐            ┌──────────────────────┐
│ Tile-Download        │            │                      │
│ Tile-Decoding        │  FUSE     │ Texture Pager         │
│ Cache-Management     │ ───────►  │ (Disk → RAM → VRAM)  │
│ FUSE-Dateisystem     │ Dateien   │                      │
└─────────────────────┘            └──────────────────────┘
```

**Das Streaming-Tool greift niemals direkt auf den VRAM zu.** Es stellt lediglich Bilddateien über ein FUSE-Dateisystem bereit — aus Sicht von X-Plane sind das gewöhnliche Custom-Scenery-Texturen. X-Plane liest diese Dateien über seinen eigenen Texture Pager ein und lädt sie in seinen VRAM-Pool. Die VRAM-Belastung ist daher bei allen Ortho-Lösungen identisch, da X-Plane die Texturen stets auf dieselbe Weise verarbeitet.

Dieses Prinzip hat eine wichtige Konsequenz: Die Konfiguration des Streaming-Tools beeinflusst, *welche* Texturen bereitstehen und *wie schnell* sie verfügbar sind — aber die VRAM-Verwaltung liegt vollständig bei X-Plane.

---

## VRAM-Management in X-Plane

### Asynchrones Texture Paging

X-Plane lädt Texturen asynchron in drei Stufen:

1. **Disk → RAM:** Die Texturdatei wird von der SSD (oder dem FUSE-Dateisystem) in den Arbeitsspeicher gelesen
2. **RAM → GPU-Upload:** Die Textur wird dekomprimiert, Mipmaps werden generiert, dann erfolgt der Upload in den VRAM
3. **VRAM-Verwaltung:** X-Plane entscheidet anhand der Kameraposition, welche Texturen geladen bleiben und welche ausgelagert werden

Dieser Prozess läuft im Hintergrund, ohne den Render-Thread zu blockieren. Reicht der VRAM nicht aus, skaliert X-Plane die Texturauflösung automatisch herunter — statt eines Absturzes erscheinen unscharfe Texturen.

### VRAM-Budgetierung

Der VRAM-Verbrauch setzt sich aus mehreren Komponenten zusammen:

- **Scenery-Texturen:** Bodenabdeckung, Orthofotos, Autogen-Objekte
- **Flugzeug-Texturen:** Cockpit, Außenmodell, Liveries
- **Rendering-Puffer:** Schatten, Reflektionen, Post-Processing
- **UI und Overlays:** Menüs, AviTab, Karten

Orthofotos beanspruchen den größten Anteil. Entscheidend ist der Zoom-Level (ZL): Jede ZL-Stufe vervierfacht die Datenmenge pro Fläche. ZL 16 liefert eine Bodenauflösung von ca. 2,4 m/Pixel, ZL 17 ca. 1,2 m/Pixel, ZL 18 ca. 0,6 m/Pixel. Die VRAM-Anforderungen steigen entsprechend exponentiell.

**Faustregel:** Beim Ortho-Streaming muss das gesamte VRAM-Budget kalkuliert werden — nicht nur die Ortho-Texturen allein. Ein Flugzeug mit hochauflösendem Cockpit belegt bereits mehrere Gigabyte VRAM, bevor die erste Ortho-Textur geladen ist.

---

## GPU-Treiber und VRAM-Oversubscription

Wenn X-Plane mehr VRAM anfordert als physisch verfügbar ist, unterscheidet sich das Verhalten je nach GPU-Treiber-Stack erheblich. Dieses Verhalten — VRAM-Oversubscription — ist eines der relevantesten Unterschiede zwischen GPU-Herstellern und Betriebssystemen.

### Linux: Treiberabhängiges Verhalten

**Proprietäre NVIDIA-Treiber:** Bieten unter Linux kein transparentes Paging in den System-RAM. Bei VRAM-Überlauf reagiert X-Plane mit aggressivem Textur-Downscaling. Im Extremfall kommt es zu Stutter oder einem Device Loss. Dies ist die empfindlichste Kombination und erfordert sorgfältige VRAM-Budgetierung.

**Mesa/RADV (AMD):** Die Open-Source-Treiber bieten bessere Oversubscription durch den GTT-Mechanismus (Graphics Translation Table), der Texturen teilweise in den System-RAM auslagert. Das Verhalten ist toleranter als bei NVIDIA, führt aber bei starker Überzeichnung zu Performance-Einbrüchen.

**Mesa/ANV (Intel Arc):** Bietet die beste Oversubscription unter Linux. Am tolerantesten gegenüber VRAM-Überlauf, allerdings mit geringerer Verbreitung.

### Windows: WDDM-Paging

Unter Windows ermöglicht der WDDM-Treiber (Windows Display Driver Model) automatisches Paging zwischen VRAM und System-RAM — unabhängig vom GPU-Hersteller. Das Verhalten ist deutlich gutmütiger als unter Linux. Dieser architekturelle Unterschied erklärt, warum Ortho-Konfigurationen, die unter Windows problemlos funktionieren, unter Linux zu Problemen führen können.

### Device Loss vs. VRAM-Problem

Ein häufiges Missverständnis: **Device Loss ist kein VRAM-Problem.** Ein Device Loss bedeutet, dass die GPU abgestürzt ist — ausgelöst durch einen Shader- oder Treiberfehler. VRAM-Probleme äußern sich anders: durch Textur-Downscaling (unscharfe Texturen) oder Out-of-Memory-Fehlermeldungen. Die Unterscheidung ist für die Fehlerdiagnose entscheidend — ein Device Loss erfordert Treiber-Diagnostik, ein VRAM-Problem erfordert Anpassung der Grafikeinstellungen oder des Zoom-Levels.

---

## CPU-Budget: Wer verbraucht was?

Beim Ortho-Streaming laufen zwei unabhängige Prozesse parallel, die sich die CPU-Ressourcen teilen.

### X-Plane (Simulator-Prozess)

- **Hauptthread:** Physik (Blade Element Theory), Avionics, Plugin-Callbacks, Render-Vorbereitung — stark Single-Core-abhängig
- **Scenery-Threads:** Scenery-Daten laden, Objekt-Culling, Scenery-Processing — auf mehrere Kerne verteilbar
- **Texture Pager:** Asynchrones Laden und Hochladen von Texturen in den VRAM
- **Weitere:** Audio, Netzwerk (VATSIM), UI-Rendering

### Streaming-Tool (separater Prozess)

- **Tile-Download:** Netzwerk-I/O zum Herunterladen der Kartenkacheln
- **Tile-Decoding:** JPEG/PNG-Dekompression und DDS-Konvertierung — CPU-intensivster Schritt
- **Cache-Management:** Verwaltung des RAM- und Disk-Cache
- **FUSE-Overhead:** Jeder Dateizugriff durch X-Plane wird durch den FUSE-Layer geleitet

Typischerweise belegt das Streaming-Tool 1–3 CPU-Kerne und 1–4 GB RAM, abhängig von der Konfiguration. Der FUSE-Overhead ist messbar, aber gering.

### Das eigentliche Bottleneck

Die CPU-Belastung addiert sich, ist aber auf modernen Multi-Core-Systemen gut handhabbar. **Das primäre Bottleneck bei Ortho-Streaming ist fast immer der VRAM, nicht die CPU.** Die CPU wird erst dann zum limitierenden Faktor, wenn Single-Core-Performance oder Cache-Bandbreite erschöpft sind — ein Problem, das in der Seite [Performance](performance_overview.md) behandelt wird.

---

## Frame-Time-Perzentile: Was wirklich zählt

Durchschnittliche FPS-Werte verschleiern die tatsächliche Erfahrung. Aussagekräftiger sind Perzentil-Werte der Frame Time:

- **P50 (Median):** Wie sich die Simulation *meistens* anfühlt — 50 % aller Frames sind schneller, 50 % langsamer
- **P95:** Die gelegentlichen Ruckler — nur 5 % aller Frames brauchen länger als dieser Wert
- **P99:** Die schlimmsten Hänger — nur 1 % aller Frames überschreitet diesen Wert. Das sind die kurzen Freezes beim Laden dichter Flughäfen oder neuer Ortho-Kacheln

**Beispiel:** Eine Simulation mit 40 FPS im Durchschnitt kann sich flüssig anfühlen — oder ruckelig, je nach Verteilung. Liegt P99 bei 150 ms, bedeutet das: Etwa einmal pro Sekunde hängt ein einzelner Frame fast eine Sechstelsekunde. Der FPS-Counter zeigt "40", aber das Bild stockt spürbar.

### Relevanz für Ortho-Streaming und Multi-Threading

Die Verteilung von Scenery-Processing auf mehrere CPU-Kerne (Multi-Threading) ändert die durchschnittlichen FPS oft nur geringfügig. Der entscheidende Gewinn liegt bei den P95- und P99-Werten: Wenn das Scenery-Processing nicht mehr den Hauptthread blockiert, werden die schlimmsten Einzelframes kürzer. Ohne Multi-Threading muss ein einzelner Kern alles abarbeiten — bei einem schweren Scenery-Chunk bleibt dieser Kern kurz stecken und erzeugt einen Stutter. Mit Multi-Threading verteilt sich die Last, und die Spitzen werden geglättet.

**Kurzfassung:**

| Perzentil | Bedeutung | Auswirkung |
|---|---|---|
| P50 | Typisches Erlebnis | Grundsätzliche Flüssigkeit |
| P95 | Gelegentliche Ruckler | Sichtbare Mikrostutter |
| P99 | Schlimmste Hänger | Kurze Freezes, spürbare Unterbrechungen |

Multi-Threading verbessert vor allem P95/P99 — die Stutter-Spitzen — weniger den Durchschnitt.

---

## Zusammenspiel der Komponenten

### Der vollständige Datenpfad

```
Internet/CDN
    │
    ▼
Streaming-Tool (CPU: Download, Decode, Cache)
    │
    ▼  FUSE-Dateisystem
    │
X-Plane Texture Pager (CPU: Paging, Mipmap-Generierung)
    │
    ▼  GPU-Upload
    │
VRAM (GPU: Rendering)
```

Jede Stufe kann zum Engpass werden:

- **Netzwerk:** Unzureichende Bandbreite oder Jitter → Tiles fehlen → unscharfe Texturen
- **CPU (Streaming-Tool):** Überlastete Kerne → langsame Tile-Konvertierung → Nachladeruckler
- **CPU (X-Plane):** Hauptthread blockiert → Frame-Time-Spikes
- **VRAM:** Überlauf → Textur-Downscaling oder OOM-Fehler
- **Storage I/O:** Langsamer Cache-Zugriff → Verzögerungen im FUSE-Layer

### VRAM als dominanter Engpass

Bei den meisten Ortho-Setups ist der VRAM der limitierende Faktor. Die Gründe:

1. **Exponentielles Wachstum:** Jede ZL-Stufe vervierfacht den Texturspeicherbedarf
2. **Kein transparentes Paging unter Linux (NVIDIA):** Was nicht in den VRAM passt, wird herunterskaliert statt ausgelagert
3. **Kumulative Belegung:** Orthofotos + Flugzeugtexturen + Rendering-Puffer + Overlays teilen sich denselben Pool
4. **Keine Shared-Memory-Option:** Anders als unter Windows gibt es unter Linux keinen automatischen Fallback in den System-RAM

### Praktische Konsequenzen

- **Zoom-Level konservativ wählen:** Der VRAM-Verbrauch steigt nicht linear, sondern exponentiell mit dem ZL
- **Texture Quality bewusst setzen:** Die X-Plane-Einstellung "Texture Quality" beeinflusst, wie viel VRAM für Nicht-Ortho-Texturen reserviert wird
- **VRAM-Monitoring nutzen:** GPU-Monitoring-Tools zeigen die aktuelle Auslastung in Echtzeit — entscheidend für die Feinjustierung
- **Gesamtbudget kalkulieren:** Nicht nur die Ortho-Texturen, sondern alle VRAM-Verbraucher berücksichtigen

---

## Einordnung in den Grundlagen-Kontext

Dieser Bericht ergänzt die bestehende Seite [Performance](performance_overview.md), die die drei Lastdimensionen (CPU, I/O, Netzwerk) erklärt. Die hier behandelten Konzepte vertiefen speziell die Wechselwirkung zwischen GPU-Speicher und Ortho-Streaming — ein Thema, das in der Performance-Übersicht bewusst ausgespart wurde.

**Mögliche Kapitelstruktur für die Docs-Seite:**

1. Architektur: Streaming-Tool → FUSE → X-Plane VRAM-Pool
2. VRAM-Management: Asynchrones Paging, Downscaling, Budgetierung
3. Treiber-Unterschiede: Oversubscription unter Linux vs. Windows
4. CPU-Budget: Simulator vs. Streaming-Tool
5. Frame-Time-Perzentile: P50/P95/P99 und Multi-Threading
6. Zusammenspiel und praktische Konsequenzen
