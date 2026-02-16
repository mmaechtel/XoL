# Performance-Grundlagen

<div class="video-container" markdown>
<video controls width="100%" preload="metadata" aria-label="Video: Das Performance-Rätsel" poster="../assets/video/de/Das_Performance-Rätsel/Das_Performance-Rätsel.jpg">
  <source src="../assets/video/de/Das_Performance-Rätsel/Das_Performance-Rätsel.mp4" type="video/mp4">
</video>
</div>

## Einleitung

Szenerien laden langsam, Texturen fehlen beim Überflug, Mikroruckler tauchen ohne erkennbare Ursache auf — typische Symptome, die X-Plane-Nutzer unter Linux kennen. Die Ursache liegt selten an einer einzelnen Komponente. X-Plane ist ein Hybrid aus rechenintensiver Physiksimulation, massivem Daten-I/O und — bei Ortho-Streaming — kontinuierlichem Netzwerkverkehr. Drei Lastdimensionen konkurrieren dabei um gemeinsame Ressourcen, und das schwächste Glied bestimmt, was auf dem Bildschirm ankommt.

Dieses Kapitel erklärt die Grundlagen dieser Wechselwirkungen. Konkrete Optimierungsmaßnahmen finden sich in den spezialisierten Kapiteln, die am Ende verlinkt sind.

## Die drei Lastdimensionen

X-Plane beansprucht drei Hardware-Subsysteme gleichzeitig, die jeweils eigene Engpässe mitbringen:

| Lastdimension | Primäre Ressource | Typische Engpassquelle |
|---|---|---|
| CPU-Compute | Prozessorkerne, Cache, RAM | Taktfrequenz, IPC, Cache-Misses |
| Lokale E/A | Storage-Subsystem (SSD/[NVMe](glossary.md#nvme-non-volatile-memory-express)) | IOPS, Durchsatz, [Latenz](glossary.md#latenz) |
| Netzwerk-Streaming | Netzwerkkarte, WAN-Anbindung | Bandbreite, Jitter, Paketverlust |

**Das schwächste Glied bestimmt die Gesamtperformance — und dieses Glied wechselt dynamisch.** Beim Start einer Szenerie dominiert die lokale E/A (Texturen laden), im Flug die CPU (Physik und Rendering), beim Ortho-Streaming das Netzwerk. Keine dieser Dimensionen lässt sich isoliert betrachten.

## CPU-gebundene Performance

X-Planes Physikmodell basiert auf der [Blade Element Theory](glossary.md#blade-element-theory): Das Flugzeug wird in zahlreiche Segmente zerlegt, für die in Echtzeit Luftströmung und Kräfte berechnet werden. Diese Berechnung erfolgt im Hauptthread und ist daher stark von der Single-Core-Performance abhängig.

### IPC und Mikroarchitektur

Die reine Taktfrequenz einer CPU erzählt nur die halbe Geschichte. Entscheidend ist die Anzahl der Instruktionen pro Taktzyklus (IPC — Instructions per Cycle). Moderne Architekturen mit breiten Ausführungseinheiten und effizienter Sprungvorhersage erreichen bei gleicher Taktfrequenz deutlich mehr Berechnungen pro Zeiteinheit als ältere Generationen.

In X-Plane äußert sich niedrige IPC als hartes FPS-Limit: Selbst bei maximaler Taktfrequenz bleibt die Framerate unter dem erwarteten Wert, weil der Hauptthread pro Taktzyklus zu wenig Arbeit erledigt.

??? abstract "Hintergrund: Warum IPC wichtiger ist als Taktfrequenz"

    Ein Prozessorkern mit 5 GHz und niedriger IPC kann langsamer sein als einer mit 4,5 GHz und hoher IPC. Die IPC-Rate wird von der Breite der Ausführungseinheiten, der Tiefe des Out-of-Order-Pipelinings und der Effizienz der Sprungvorhersage bestimmt. X-Plane profitiert besonders von hoher IPC, da die Blade-Element-Berechnungen sequentielle Abhängigkeiten aufweisen, die sich nur begrenzt parallelisieren lassen.

### Cache-Hierarchie und Memory Wall

X-Plane arbeitet mit großen Datenstrukturen — Geländemeshes, Szenerie-Objekte, Texturmetadaten. Passen diese nicht in den L3-Cache, entstehen Cache-Misses, die den Prozessor zum Warten auf den Hauptspeicher zwingen. Bei voller Kernauslastung wird die Memory-Bandbreite zum Flaschenhals — ein als „Memory Wall" bekanntes Phänomen.

Das Symptom in X-Plane: FPS-Einbrüche in dicht bebauten Szenerien oder an komplexen Flughäfen, obwohl die CPU-Auslastung nicht bei 100 % liegt. Der Prozessor wartet auf Daten statt zu rechnen.

??? abstract "Hintergrund: Memory Wall"

    Auf einem typischen DDR5-System mit 35–50 GB/s Bandbreite pro Kanal (je nach Taktrate) kann ein einzelner Kern bereits mehrere GB/s an Speicherbandbreite fordern. Sind alle Kerne aktiv und greifen auf Daten außerhalb des L3-Cache zu, wird die gemeinsame Speicherbandbreite zum limitierenden Faktor. Mehr Kerne helfen in diesem Szenario nicht — sie verschärfen das Problem.

### Interrupt-Last und Kontextwechsel

Wenn der Hauptprozessor gleichzeitig [IRQ](glossary.md#irq-interrupt-request)-Anfragen von [NVMe](glossary.md#nvme-non-volatile-memory-express)-SSDs und der Netzwerkkarte verarbeiten muss, werden Rechenkerne aus ihren Berechnungsschleifen gerissen. Jeder Kontextwechsel kostet nicht nur CPU-Zyklen, sondern invalidiert auch Cache-Lines und stört das Pipelining. Ohne dediziertes IRQ-Pinning kann dies zu sporadischen Mikrorucklern führen — kurze [Frame-Time](glossary.md#frame-time)-Spikes, die sich nicht reproduzieren lassen.

Siehe [Systemtuning](system/systemtuning.md) für IRQ-Pinning und [CPU-Affinität](glossary.md#cpu-affinität)

## Lokale E/A-Performance

Die lokale E/A-Last entsteht beim Laden von Szenerie-Daten, Texturen, Meshes und Autogen-Objekten. Die Wahl des Speichermediums hat erheblichen Einfluss auf Ladezeiten und Nachladeruckler im Flug.

### Speichertypen im Vergleich

| Speichertyp | Seq. Lesen | Random 4K IOPS | Latenz |
|---|---|---|---|
| HDD (7200 RPM) | ~200 MB/s | ~100–200 | 5–10 ms |
| SATA SSD | ~550 MB/s | ~80.000–100.000 | 75–150 µs |
| NVMe SSD (PCIe 4.0) | ~7.000 MB/s | ~800.000–1.000.000 | 20–50 µs |
| NVMe SSD (PCIe 5.0) | ~12.000 MB/s | ~1.500.000+ | 15–40 µs |

Für X-Plane sind sowohl der sequentielle Durchsatz (große Texturdateien) als auch die IOPS (viele kleine Szenerie-Dateien) relevant. [NVMe](glossary.md#nvme-non-volatile-memory-express)-SSDs bieten beim sequentiellen Durchsatz einen Vorteil um den Faktor 10+ gegenüber SATA-SSDs; bei den IOPS ist der Abstand ähnlich groß.

### Dateisystem und I/O-Scheduler

Selbst mit schneller Hardware kann der I/O-Stack zum Engpass werden. Der [I/O-Scheduler](glossary.md#io-scheduler) beeinflusst die Latenz bei gemischten Lese-/Schreib-Workloads, und das Dateisystem — [Ext4](glossary.md#ext4-fourth-extended-filesystem), [Btrfs](glossary.md#btrfs-b-tree-filesystem) oder XFS — bringt unterschiedliche Journaling-Strategien mit.

Siehe [Dateisystem](optimizations/filesystem.md) für I/O-Scheduler, [noatime](glossary.md#noatime) und [TRIM](glossary.md#trim)-Konfiguration

### Page-Cache-Druck

Ein praxisrelevantes Problem bei großen Szenerie-Installationen: Wenn X-Plane massiv Daten liest, füllt sich der Linux-Page-Cache. Beginnt das System mit dem Dirty-Page-Writeback, kann die gesamte I/O-Pipeline blockieren — selbst wenn die SSD schnell genug wäre. Das äußert sich als plötzliche Ruckler beim Nachladen von Szenerien, die nichts mit CPU- oder GPU-Last zu tun haben.

## Netzwerk-Streaming

Netzwerk-I/O spielt in X-Plane eine wachsende Rolle. Drei typische Szenarien erzeugen kontinuierlichen Datenverkehr:

- **Ortho-Streaming:** [AutoOrtho](glossary.md#autoortho) streamt [Orthofotos](glossary.md#orthofotos) in Echtzeit vom Server, statt sie lokal vorzuhalten. Der Datenstrom muss schnell genug fließen, damit Texturen vor dem Überflug geladen sind.
- **Wetterdaten:** Echtzeit-Wetterservices liefern Windfelder, Wolkenschichten und Niederschlagsdaten über das Netzwerk.
- **VATSIM/Online-ATC:** Multiplayer-Netzwerke erzeugen bidirektionalen Datenverkehr für Positionsmeldungen und Sprachkommunikation.

### Die Illusion des konstanten Streams

Streaming-Software setzt voraus, dass Daten gleichmäßig fließen. In der Praxis stimmt das selten:

- **TCP-Congestion-Control:** Ein einzelnes verlorenes Paket kann den Durchsatz für mehrere Round-Trip-Times deutlich reduzieren. Der Flusskontroll-Algorithmus drosselt vorsorglich — auch wenn die Leitung eigentlich frei ist.
- **Jitter:** Selbst bei stabiler mittlerer Bandbreite schwankt die tatsächliche Datenrate erheblich. Typische Jitter-Werte auf WAN-Verbindungen liegen zwischen 1 und 50 ms.
- **Shared Bandwidth:** Bei Cloud-gehosteten Datenquellen teilen sich viele Nutzer dieselbe Infrastruktur. „Noisy Neighbors" können den verfügbaren Durchsatz unvorhersehbar reduzieren.

### Auswirkungen auf die Simulation

Stockt der Netzwerk-Stream, fehlen X-Plane die Texturdaten für den aktuellen Sichtbereich. Das Ergebnis: unscharfe oder fehlende Bodentexturen, Nachladeruckler und [Frame-Time](glossary.md#frame-time)-Spikes. Beim Ortho-Streaming macht sich jede Unterbrechung sofort visuell bemerkbar, da [AutoOrtho](glossary.md#autoortho) die Texturen über ein [FUSE](glossary.md#fuse-filesystem-in-userspace)-Dateisystem bereitstellt — X-Plane sieht einen I/O-Zugriff, der auf Netzwerkdaten wartet.

## Wechselwirkungen zwischen den Dimensionen

### Ressourcenkonkurrenz

Die drei Lastdimensionen teilen sich CPU-Zyklen und Memory-Bandbreite. Ein Beispiel: X-Plane berechnet Physik auf den Kernen 0–11, gleichzeitig laden Szenerie-Daten von der NVMe-SSD, und AutoOrtho empfängt Texturen aus dem Netzwerk. Ohne explizites IRQ-Pinning landen beide I/O-Pfade auf denselben Kernen. Der TCP-Stack interpretiert die Verarbeitungsverzögerung als Congestion und drosselt — der Stream stockt.

### PCIe-Bandbreitenverteilung

GPU, [NVMe](glossary.md#nvme-non-volatile-memory-express)-SSD und Netzwerkkarte teilen sich die verfügbaren PCIe-Lanes der CPU. Auf einem typischen Desktop-Prozessor kann die gleichzeitige Nutzung einer GPU (16 Lanes), einer NVMe-SSD (4 Lanes) und einer Netzwerkkarte die verfügbare PCIe-Kapazität ausreizen.

??? abstract "Hintergrund: PCIe-Bandbreite"

    PCIe 4.0 bietet ~2 GB/s pro Lane, PCIe 5.0 ~4 GB/s. Eine GPU mit 16 Lanes PCIe 4.0 hat theoretisch ~32 GB/s zur Verfügung, eine NVMe-SSD mit 4 Lanes ~8 GB/s. Wenn alle Geräte gleichzeitig hohe Last erzeugen, teilen sie sich die Bandbreite des Root-Complex — die Latenzen aller Geräte steigen.

### Der Dominoeffekt

Die gefährlichste Wechselwirkung ist eine Kettenreaktion bei Streaming-Aussetzern:

1. Der Netzwerk-Stream stockt (Jitter-Spike)
2. Der I/O-Thread blockiert beim Warten auf Daten
3. Kerne laufen leer — das OS nutzt sie für Hintergrundprozesse
4. Der Stream kommt zurück und liefert Daten im Burst
5. Aufgestaute Daten, neue Berechnungen und verschobene I/O-Operationen kollidieren

Dieses Muster kann das System kurzfristig überlasten und die nächsten Frames verzögern — ein selbstverstärkender Effekt, der sich als periodische Ruckler bemerkbar macht.

## Der Frame als Maßeinheit

Alle drei Lastdimensionen wirken sich auf dieselbe Messgröße aus: die [Frame Time](glossary.md#frame-time). Eine Frame Time von 33 ms entspricht ~30 [FPS](glossary.md#fps-frames-per-second), 16,6 ms entspricht ~60 FPS. Jeder Spike in einer der drei Dimensionen — ein Cache-Miss, ein I/O-Stall, ein Netzwerk-Aussetzer — schlägt direkt auf die Frame Time durch.

Warum gleichmäßige Frame Times wichtiger sind als hohe FPS und wie sich Frame-Time-Probleme mit dem Microprofiler diagnostizieren lassen, beschreiben die Kapitel [Systemtuning](system/systemtuning.md) und [X-Plane Performance](xplane/performance.md).

## Optimierungsansätze im Überblick

Die folgenden Strategien adressieren die beschriebenen Lastdimensionen. Jede wird in einem spezialisierten Kapitel detailliert behandelt.

**Caching und Prefetching**

- AutoOrtho puffert gestreamte Texturen lokal auf der [NVMe](glossary.md#nvme-non-volatile-memory-express)-SSD, bevor X-Plane sie anfordert — der wichtigste Schutz gegen Streaming-Aussetzer
- Cache-Größe und Prefetch-Verhalten lassen sich in AutoOrtho konfigurieren
- Dateisystem mit [noatime](glossary.md#noatime) und passendem [I/O-Scheduler](glossary.md#io-scheduler) entlasten den I/O-Pfad zusätzlich
- Siehe [AutoOrtho](addon/autoortho.md) und [Dateisystem](optimizations/filesystem.md)

**IRQ-Pinning und Thread-Affinität**

- Netzwerk-[IRQs](glossary.md#irq-interrupt-request) und I/O-Threads auf dedizierte CPU-Kerne legen, damit der X-Plane-Hauptthread ungestört rechnen kann
- [irqbalance](glossary.md#irqbalance) konfigurieren, um bestimmte Kerne von Interrupts freizuhalten
- Siehe [Systemtuning](system/systemtuning.md)

**Monitoring und Profiling**

- CPU-Auslastung pro Kern überwachen — Idle-Kerne bei laufender Simulation deuten auf I/O-Stalls hin
- I/O-Latenz und Netzwerk-Durchsatz parallel messen, um die aktive Engpassdimension zu identifizieren
- Siehe [System Monitoring](system/systemtools.md)

## Weiterführende Kapitel

| Thema | Seite | Schwerpunkt |
|---|---|---|
| System-Tuning | [Einführung](system/index.md) | Überblick und Video |
| CPU & Interrupts | [Tuning](system/systemtuning.md) | [CPU Governor](glossary.md#cpu-governor), IRQ-Pinning, [Kernel-Parameter](glossary.md#kernel-parameter) |
| Storage & Dateisystem | [Dateisystem](optimizations/filesystem.md) | I/O-Scheduler, Mount-Optionen, TRIM |
| Monitoring | [System Monitoring](system/systemtools.md) | CPU-, I/O- und Netzwerk-Analyse |
| X-Plane intern | [Performance](xplane/performance.md) | Microprofiler, FPS-Anzeige, Grafikeinstellungen |
| Ortho-Streaming | [AutoOrtho](addon/autoortho.md) | Cache-Konfiguration, Prefetching |
| GPU-Treiber | [Nvidia](optimizations/nvidia.md) | Treiberoptimierung, Persistence Mode |
| Kernel | [Liquorix](optimizations/liquorix.md) | Low-Latency-Kernel, Scheduler |
