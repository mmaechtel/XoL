# CPU & RAM

## Einleitung

Die [Performance-Übersicht](performance_overview.md) beschreibt, warum Single-Core-Performance, Cache-Hierarchie und Memory-Bandbreite für X-Plane entscheidend sind. Dieses Kapitel vertieft die Frage, wie X-Plane seine CPU-Kerne und den Arbeitsspeicher tatsächlich nutzt — insbesondere im Zusammenspiel mit Ortho-Streaming-Tools, die als eigenständige Prozesse neben dem Simulator laufen.

## X-Planes Threading-Modell

X-Plane verteilt seine Arbeit auf mehrere Threads mit unterschiedlichen Aufgaben:

**Hauptthread (Main Thread)**

- Physik ([Blade Element Theory](../../glossary.md#blade-element-theory)), Avionics, [Plugin](../../glossary.md#plugin)-Callbacks, Render-Vorbereitung
- Stark Single-Core-abhängig — die sequentielle Natur der Physikberechnung begrenzt die Parallelisierbarkeit
- Bestimmt die minimale [Frame Time](../../glossary.md#frame-time): Kein Frame kann schneller fertig werden als der Hauptthread braucht

**Scenery-Threads**

- Laden von [DSF](../../glossary.md#dsf-distribution-scenery-format)-Daten, Objekt-Culling, Scenery-Processing
- Auf mehrere Kerne verteilbar (Multi-Threading)
- Entlasten den Hauptthread von schweren Lade- und Verarbeitungsoperationen

**Texture Pager**

- Asynchrones Laden von Texturdaten: Disk → RAM → [VRAM](../../glossary.md#vram-video-ram)
- Läuft im Hintergrund, ohne den Render-Thread direkt zu blockieren
- Erzeugt I/O-Last auf Storage und Memory-Bandbreite

**Weitere Threads**

- Audio ([FMOD](../../glossary.md#fmod)), Netzwerk (VATSIM, Echtzeit-Wetter), UI-Rendering

### Der Hauptthread als Flaschenhals

Das zentrale Architekturprinzip: Der Hauptthread muss *jeden* Frame abschließen, bevor der nächste beginnen kann. Alle anderen Threads liefern dem Hauptthread zu — Scenery-Daten, Texturen, Netzwerkdaten. Wenn der Hauptthread auf Daten wartet, entsteht ein [Frame-Time](../../glossary.md#frame-time)-Spike. Wenn er mit Berechnungen überlastet ist, sinkt die Framerate gleichmäßig.

Deshalb profitiert X-Plane stärker von hoher Single-Core-Performance (IPC × Taktfrequenz) als von vielen Kernen. Mehr Kerne helfen bei den unterstützenden Threads, heben aber das Hauptthread-Limit nicht an.

## Multi-Threading für Scenery-Processing

Die Verteilung des Scenery-Processing auf mehrere CPU-Kerne ist eine der wirkungsvollsten Architekturänderungen der letzten X-Plane-Versionen.

### Vorher: Alles auf einem Kern

Ohne Multi-Threading verarbeitet ein einzelner Kern alle Scenery-Daten sequentiell. Bei einem schweren Scenery-Chunk — ein dichter Flughafen, ein neues Ortho-Tile — blockiert dieser Kern, und der Hauptthread muss warten. Das Ergebnis: ein einzelner langer Frame, der sich als Stutter bemerkbar macht.

### Nachher: Verteilung auf mehrere Kerne

Mit Multi-Threading wird die Scenery-Verarbeitung auf mehrere Kerne aufgeteilt. Schwere Chunks werden parallel abgearbeitet, ohne den Hauptthread zu blockieren. Die durchschnittlichen [FPS](../../glossary.md#fps-frames-per-second) ändern sich oft nur geringfügig — der entscheidende Gewinn liegt bei den schlimmsten Einzelframes (siehe [Frame-Time-Perzentile](gpu_vram.md#frame-time-perzentile)).

??? abstract "Hintergrund: Warum der Durchschnitt kaum steigt"

    Multi-Threading verschiebt Arbeit vom Hauptthread auf Hilfskerne. Wenn der Hauptthread vorher 90 % seiner Zeit mit Physik und nur 10 % mit Scenery verbracht hat, ändert Multi-Threading nur diese 10 %. Die durchschnittliche Frame Time sinkt minimal. Der Gewinn zeigt sich erst in den Extremfällen — den Frames, in denen der Scenery-Anteil ausnahmsweise 50 % oder mehr betrug. Genau diese Frames werden durch Multi-Threading drastisch verkürzt.

## CPU-Budget bei Ortho-Streaming

Beim Ortho-Streaming laufen zwei unabhängige Prozesse parallel auf derselben CPU:

### Simulator-Prozess (X-Plane)

Nutzt die oben beschriebenen Threads. Der Hauptthread beansprucht einen Kern nahezu vollständig, die Scenery- und Texture-Threads verteilen sich auf weitere Kerne.

### Streaming-Prozess (separates Programm)

Das Ortho-Streaming-Tool — ob [AutoOrtho](../../glossary.md#autoortho), XPME oder XEarthLayer — läuft als eigenständiger Prozess mit eigenen Aufgaben:

- **Tile-Download:** Netzwerk-I/O zum Herunterladen der Kartenkacheln von CDN-Servern
- **Tile-Decoding:** JPEG/PNG-Dekompression und Konvertierung in das [DDS](../../glossary.md#dds-directdraw-surface)-Format — der CPU-intensivste Schritt
- **Cache-Management:** Verwaltung des RAM- und Disk-Cache für bereits heruntergeladene Kacheln
- **[FUSE](../../glossary.md#fuse-filesystem-in-userspace)-Layer:** Stellt die konvertierten Texturen als virtuelles Dateisystem bereit, aus dem X-Plane liest

Typische Belegung: 1–3 CPU-Kerne und 1–4 GB RAM, abhängig von der Tool-Konfiguration (Anzahl der Download-Threads, Cache-Größe, Prefetch-Verhalten).

### Ressourcenkonkurrenz

Beide Prozesse teilen sich CPU-Zyklen, Cache und Memory-Bandbreite. Ohne explizites [IRQ](../../glossary.md#irq-interrupt-request)-Pinning können Netzwerk-Interrupts des Streaming-Tools auf denselben Kernen landen, die X-Planes Hauptthread nutzt. Die [Performance-Übersicht](performance_overview.md) beschreibt diesen Mechanismus und die Gegenmaßnahmen im Detail.

**Faustregel für Ortho-Streaming:** 6+ CPU-Kerne bieten genügend Spielraum für Simulator und Streaming-Tool nebeneinander. Bei 4 Kernen wird die Konkurrenz spürbar — insbesondere bei hohen Zoom-Leveln, die mehr Tiles pro Zeiteinheit erfordern.

## RAM als Zwischenstufe

Der Arbeitsspeicher (RAM) spielt eine dreifache Rolle:

1. **Staging-Bereich für Texturen:** Texturdaten werden von der SSD in den RAM geladen, dort dekomprimiert und aufbereitet, bevor sie in den [VRAM](../../glossary.md#vram-video-ram) hochgeladen werden
2. **Cache für das Streaming-Tool:** Das Ortho-Tool puffert heruntergeladene und konvertierte Tiles im RAM, bevor sie über [FUSE](../../glossary.md#fuse-filesystem-in-userspace) bereitgestellt werden
3. **Linux Page Cache:** Der Kernel cached Dateizugriffe automatisch im freien RAM — bei großen Szenerie-Installationen kann der Page Cache mehrere Gigabyte beanspruchen

### Wann RAM zum Engpass wird

RAM selbst ist selten das primäre Bottleneck. Kritisch wird es in zwei Szenarien:

- **Zu wenig freier RAM:** Wenn X-Plane, Streaming-Tool und Page Cache zusammen den verfügbaren Arbeitsspeicher ausschöpfen, beginnt das System mit Swapping. Die resultierenden I/O-Stalls sind um Größenordnungen langsamer als RAM-Zugriffe.
- **Memory-Bandbreite erschöpft:** Bei voller Kernauslastung konkurrieren alle Threads um die Speicherbandbreite. Das Symptom — FPS-Einbrüche trotz CPU-Auslastung unter 100 % — ist in der [Performance-Übersicht](performance_overview.md) als Memory Wall beschrieben.

**Empfehlung:** 32 GB RAM bieten ausreichend Spielraum für X-Plane mit Ortho-Streaming. 16 GB funktionieren, lassen aber wenig Reserven für den Page Cache und paralleles Streaming.

## Weiterführend

| Thema | Seite |
|---|---|
| Zusammenspiel der Lastdimensionen | [Performance-Übersicht](performance_overview.md) |
| VRAM-Management und Frame-Time-Analyse | [GPU & VRAM](gpu_vram.md) |
| IRQ-Pinning und CPU-Affinität | [Systemtuning](../../linux/system/systemtuning.md) |
| I/O-Scheduler und Dateisystem | [Dateisystem](../../linux/optimizations/filesystem.md) |
| Ortho-Streaming-Konfiguration | [AutoOrtho](../../scenery/ortho_streaming/autoortho.md) |
