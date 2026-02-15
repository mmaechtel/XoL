# Performance-Analyse von Simulationssoftware mit CPU-, E/A- und Netzwerk-Streaming-Anforderungen

*Einfluss von Hardware-Komponenten auf die Gesamtperformance bei hybriden Workloads mit lokalem und netzwerkbasiertem I/O*

---

## 1. Einleitung

Moderne Simulationssoftware vereint hochkomplexe numerische Berechnungen mit massivem Datendurchsatz. Ob in der Finite-Elemente-Analyse, der Strömungsmechanik (CFD), der Wettervorhersage oder der Echtzeit-Physiksimulation – die Anforderungen an die zugrundeliegende Hardware sind vielschichtig und stehen in permanenter Wechselwirkung zueinander. Anders als bei rein CPU-gebundenen oder rein I/O-gebundenen Anwendungen müssen solche Systeme häufig alle Ressourcen gleichzeitig und in hohem Maße beanspruchen.

Dieser Beitrag analysiert die verschiedenen Performance-Dimensionen einer solchen Software: die CPU-Last durch numerische Berechnungen, die lokale Ein-/Ausgabe (E/A) beim Laden und Speichern großer Datensätze, sowie den kontinuierlichen Netzwerk-I/O-Stream, der durch Cloud-basierte Datenquellen oder verteilte Simulationsknoten entsteht. Besonderes Augenmerk liegt auf der Tatsache, dass die vermeintlich „konstanten" Datenströme über das Internet in der Praxis alles andere als gleichmäßig sind – und welche Konsequenzen das für die Systemarchitektur hat.

---

## 2. Architekturüberblick: Drei Lastdimensionen

Eine typische Simulationsanwendung mit Streaming-Anforderungen lässt sich in drei primäre Lastdimensionen unterteilen, die jeweils unterschiedliche Hardware-Subsysteme beanspruchen und sich gegenseitig beeinflussen:

| Lastdimension | Primäre Ressource | Typische Engpassquelle |
|---|---|---|
| CPU-Compute | Prozessorkerne, Cache, RAM | Taktfrequenz, IPC, Cache-Misses, NUMA-Latenzen |
| Lokale E/A | Storage-Subsystem (SSD/NVMe) | IOPS, sequentieller Durchsatz, Latenz, Dateisystem-Overhead |
| Netzwerk-Streaming | NIC, WAN-Anbindung | Bandbreite, Latenz, Jitter, Paketverlust, TCP-Congestion |

Das Kernproblem bei Simulationssoftware ist, dass keine dieser Dimensionen isoliert betrachtet werden kann. Ein CPU-Kern, der auf Daten vom Netzwerk wartet, ist ebenso verschwendete Rechenleistung wie ein NVMe-Laufwerk, das idle bleibt, weil die CPU mit einem Berechnungsschritt beschäftigt ist. Die Gesamtperformance wird stets durch das schwächste Glied in dieser Kette limitiert – und dieses schwächste Glied wechselt je nach Simulationsphase dynamisch.

---

## 3. CPU-gebundene Performance

### 3.1 Anforderungsprofil

Der Berechnungskern einer Simulation – ob es sich um die Lösung partieller Differentialgleichungen, die Matrixinversion oder Monte-Carlo-Methoden handelt – stellt intensive Anforderungen an die Prozessorarchitektur. Dabei spielen mehrere Faktoren eine Rolle, die weit über die reine Taktfrequenz hinausgehen.

**Instructions per Cycle (IPC) und Mikroarchitektur:** Moderne Simulationen profitieren stark von breiten Ausführungseinheiten, tiefem Out-of-Order-Pipelining und effizienter Sprungvorhersage. Ein Prozessor mit hoher IPC-Rate (wie aktuelle Zen-5- oder Golden-Cove-Kerne) kann bei gleicher Taktfrequenz deutlich mehr Berechnungen pro Zeiteinheit abschließen als ältere Architekturen. Die Wahl zwischen wenigen schnellen Kernen und vielen langsameren Kernen hängt direkt vom Parallelisierungsgrad der Simulation ab.

**SIMD-Vektorisierung:** Viele numerische Kernroutinen lassen sich vektorisieren und profitieren enorm von breiten SIMD-Einheiten. AVX-512-Instruktionen (bei Intel) oder die entsprechenden Erweiterungen bei AMD können den Durchsatz für Fließkommaoperationen im Idealfall vervielfachen. In der Praxis wird der theoretische Gewinn allerdings häufig durch Thermal-Throttling reduziert – insbesondere wenn alle Kerne gleichzeitig AVX-512-Last fahren und die TDP-Grenzen erreicht werden.

**Cache-Hierarchie und Speicherbandbreite:** Simulationen arbeiten häufig mit großen, mehrdimensionalen Datenstrukturen (Gitter, Meshes, Partikelfelder). Passt der aktive Datensatz nicht in den L3-Cache, entstehen Cache-Misses, die den Prozessor zum Warten auf den Hauptspeicher zwingen. Auf einem typischen DDR5-System mit ca. 50 GB/s Bandbreite pro Kanal kann ein einzelner Kern bereits mehrere GB/s an Speicherbandbreite fordern. Bei voller Kernauslastung wird die Memory-Bandbreite häufig zum Flaschenhals – ein Phänomen, das als „Memory Wall" bekannt ist.

### 3.2 NUMA-Effekte in Mehrsockel-Systemen

In Workstation- und Server-Umgebungen mit mehreren CPU-Sockeln kommt die NUMA-Problematik (Non-Uniform Memory Access) zum Tragen. Greift ein Prozessorkern auf Speicher zu, der physisch am anderen Sockel angebunden ist, erhöht sich die Zugriffslatenz um den Faktor 1,5 bis 3. Für Simulationssoftware, die große zusammenhängende Speicherbereiche durchläuft, kann eine falsche NUMA-Allokation die effektive Rechenleistung drastisch reduzieren.

Abhilfe schaffen NUMA-aware Memory-Allocator und Thread-Pinning-Strategien (z. B. über `numactl` oder `hwloc`), die sicherstellen, dass Threads möglichst auf denselben NUMA-Knoten zugreifen, auf dem ihre Daten liegen.

### 3.3 CPU-Last unter konkurrierendem I/O

Ein oft unterschätzter Effekt: Wenn der Hauptprozessor gleichzeitig I/O-Interrupts verarbeiten muss – sei es von lokalen NVMe-Geräten oder von der Netzwerkkarte – werden Rechenkerne aus ihren Berechnungsschleifen gerissen. Jeder Kontextwechsel kostet nicht nur CPU-Zyklen, sondern invalidiert auch Cache-Lines und stört das Pipelining. In Systemen ohne dedizierte I/O-Kerne (d. h. ohne explizites IRQ-Pinning) kann dies zu sporadischen, schwer reproduzierbaren Performance-Einbrüchen führen.

---

## 4. Lokale E/A-Performance

### 4.1 Speichertypen und ihre Charakteristik

Die lokale E/A-Last entsteht durch das Laden von Eingabedaten (Geometrien, Randbedingungen, Anfangszustände), das Schreiben von Zwischenergebnissen (Checkpoints) und die Ausgabe finaler Simulationsergebnisse. Je nach Speichertechnologie ergeben sich fundamental unterschiedliche Performance-Profile:

| Speichertyp | Seq. Lesen | Seq. Schreiben | Random 4K IOPS | Latenz |
|---|---|---|---|---|
| HDD (7200 RPM) | ~200 MB/s | ~180 MB/s | ~100–200 | 5–10 ms |
| SATA SSD | ~550 MB/s | ~520 MB/s | ~80.000–100.000 | 50–100 µs |
| NVMe SSD (PCIe 4.0) | ~7.000 MB/s | ~5.000 MB/s | ~800.000–1.000.000 | 10–20 µs |
| NVMe SSD (PCIe 5.0) | ~12.000 MB/s | ~10.000 MB/s | ~1.500.000+ | 8–15 µs |

Für Simulationen, die kontinuierlich Checkpoints schreiben (um bei einem Absturz nicht von vorne beginnen zu müssen), ist der sequentielle Schreibdurchsatz entscheidend. Für Simulationen, die viele kleine Dateien oder Metadaten lesen (z. B. Multi-Physics-Kopplungen mit Tausenden von Parameterdateien), dominieren dagegen die IOPS und die Zugriffslatenz.

### 4.2 Dateisystem und I/O-Scheduler

Selbst mit schneller Hardware kann der I/O-Stack auf Betriebssystemebene zum Engpass werden. Dateisysteme wie ext4 oder XFS haben unterschiedliche Journaling-Strategien und Allocation-Algorithmen, die sich bei großen Dateien oder vielen gleichzeitigen Schreibvorgängen unterschiedlich verhalten. Der Linux-I/O-Scheduler (z. B. `mq-deadline` vs. `none` für NVMe) beeinflusst ebenfalls die Latenz und den Durchsatz bei gemischten Lese-/Schreib-Workloads.

Ein praxisrelevantes Problem ist der Page-Cache-Druck: Wenn die Simulation große Dateien schreibt, füllt sich der Linux-Page-Cache, und das System beginnt mit dem „Dirty-Page-Writeback". Dieser Hintergrundprozess kann die gesamte I/O-Pipeline blockieren und zu ruckartigen Latenz-Spikes führen – selbst wenn die SSD eigentlich schnell genug wäre.

### 4.3 Zusammenspiel mit der CPU-Last

Lokale E/A ist nie kostenlos für die CPU. Selbst mit Direct-I/O (O_DIRECT) und asynchronen I/O-Frameworks wie `io_uring` bleiben Systemcall-Overhead, DMA-Setup und Interrupt-Verarbeitung. Bei typischen Simulationsworkloads, die Dutzende Gigabyte pro Stunde an Checkpoints schreiben, kann der I/O-bezogene CPU-Overhead zwischen 2 % und 8 % der verfügbaren Rechenleistung ausmachen – ein scheinbar kleiner Wert, der sich über lange Simulationsläufe aber signifikant summiert.

---

## 5. Netzwerk-Streaming: Die unterschätzte Variable

### 5.1 Warum Streaming?

Viele moderne Simulationsumgebungen sind auf kontinuierliche Datenströme über das Netzwerk angewiesen. Typische Szenarien umfassen das Streaming von Echtzeit-Eingabedaten (z. B. Sensordaten, Wetterdaten, Marktdaten), den Zugriff auf Cloud-basierte Datensätze, die zu groß für lokale Speicherung sind, die Kommunikation zwischen verteilten Simulationsknoten (MPI, gRPC) sowie die Echtzeit-Visualisierung von Ergebnissen auf Remote-Clients.

In all diesen Fällen wird ein „konstanter" Datenstrom vorausgesetzt. Die Architektur der Simulationssoftware rechnet damit, dass zu jedem Zeitschritt die benötigten Daten verfügbar sind. Was in der Theorie einfach klingt, ist in der Praxis hochgradig problematisch.

### 5.2 Die Illusion des konstanten Streams

Die grundlegende Annahme vieler Streaming-Architekturen – dass Daten mit konstanter Rate fließen – bricht in der Realität regelmäßig zusammen. Die Ursachen hierfür sind vielfältig:

**TCP-Congestion-Control:** TCP-basierte Streams (und die meisten Simulationsdaten werden über TCP oder TLS/TCP übertragen) unterliegen den Algorithmen der Flusskontrolle. Cubic, BBR oder Reno reagieren auf Paketverlust und Latenzänderungen mit teilweise drastischen Anpassungen des Sendefensters. Ein einzelner verlorener Paket kann den Durchsatz für mehrere Round-Trip-Times halbieren.

**Jitter und Latenz-Schwankungen:** Selbst bei stabiler mittlerer Bandbreite schwankt die tatsächliche Datenrate erheblich. Typische Jitter-Werte auf WAN-Verbindungen liegen zwischen 1 und 50 ms, bei transatlantischen Verbindungen oder unter Last auch deutlich höher. Für eine Simulation, die alle 10 ms einen neuen Datenblock erwartet, kann ein Jitter-Spike von 100 ms eine ganze Kaskade von Zeitschritt-Verzögerungen auslösen.

**Shared-Bandwidth-Effekte:** In Unternehmensnetzwerken und insbesondere bei Cloud-gehosteten Datenquellen teilen sich viele Nutzer dieselbe physische Infrastruktur. „Noisy Neighbors" auf demselben Switch, in derselben Verfügbarkeitszone oder auf demselben physischen Host können den verfügbaren Durchsatz unvorhersehbar reduzieren.

**BGP-Routing-Änderungen:** Das Internet-Routing ist dynamisch. Wenn sich der Pfad zwischen Datenquelle und Simulationssystem ändert (etwa durch einen BGP-Update oder einen Peering-Wechsel), können Latenz und Durchsatz sprunghaft variieren – ohne dass an der lokalen Infrastruktur irgendetwas geändert wurde.

**WAN-Optimierer und Proxies:** In vielen Enterprise-Umgebungen durchlaufen Datenströme Firewalls, WAN-Optimierer oder SSL-Inspection-Proxies. Diese Geräte führen eigene Pufferung und Verarbeitung durch und können den Fluss zusätzlich verzögern oder Micro-Bursts verursachen.

### 5.3 Auswirkungen auf die Simulation

Wenn der Netzwerk-Stream einbricht oder stockt, ergeben sich je nach Simulationstyp unterschiedliche Konsequenzen:

**Bei zeitkritischen Simulationen (Echtzeit oder nahe Echtzeit):** Ein Streaming-Aussetzer führt direkt zu einem fehlenden Zeitschritt. Entweder muss die Simulation mit interpolierten Daten weiterrechnen (Genauigkeitsverlust) oder sie muss pausieren (Latenzverlust). Beides ist in Produktionsumgebungen inakzeptabel.

**Bei Batch-Simulationen mit Remote-Daten:** Stockt der Stream, blockiert der I/O-Thread, der auf Daten wartet. Wenn die Architektur keine ausreichende Entkopplung zwischen I/O und Compute vorsieht, propagiert dieser Stall direkt zu den Rechenkerne, die dann idle laufen. Die CPU-Auslastung fällt ab, obwohl nominell genug Rechenleistung vorhanden wäre.

**Bei verteilten Simulationen (MPI über WAN):** Bereits minimale Latenz-Schwankungen zwischen den Knoten führen zu Synchronisationsverlusten. In einem Bulk-Synchronous-Parallel-Modell (BSP) wartet der schnellste Knoten auf den langsamsten – und der langsamste ist typischerweise derjenige mit der schlechtesten Netzwerkverbindung.

### 5.4 Hardware-Einfluss auf die Netzwerk-Performance

Die Netzwerk-Interface-Card (NIC) und ihre Integration in das System beeinflussen die erzielbare Streaming-Performance erheblich:

| Aspekt | Einfluss |
|---|---|
| Ringbuffer-Größe der NIC | Bestimmt die Fähigkeit, Burst-Traffic zu absorbieren, bevor Pakete verworfen werden |
| Interrupt-Coalescing | Reduziert CPU-Overhead, erhöht aber die Latenz; Trade-off muss für Simulationen konfiguriert werden |
| Offloading (TSO, GRO, Checksum) | Entlastet die CPU von Protokollverarbeitung; bei Simulationen mit kleinen Paketen weniger effektiv |
| RSS / Flow-Steering | Verteilt Paketverarbeitung auf mehrere Kerne; bei Single-Flow-Streams limitiert |
| RDMA / RoCE | Umgeht den Kernel-Netzwerk-Stack komplett; bietet minimale Latenz, aber begrenzte WAN-Tauglichkeit |

Ein häufiger Praxisfehler: Der Einsatz von 10-GbE- oder 25-GbE-NICs wird als Lösung für Bandbreitenprobleme betrachtet, obwohl der eigentliche Engpass in der WAN-Verbindung liegt. Eine schnelle NIC hilft nur dann, wenn auch die End-to-End-Pfadkapazität mithalten kann.

---

## 6. Wechselwirkungen zwischen den Lastdimensionen

### 6.1 Ressourcenkonkurrenz

Die drei Lastdimensionen konkurrieren um gemeinsame Ressourcen, insbesondere um CPU-Zyklen und um die Memory-Bandbreite. Ein konkretes Beispiel: Eine Simulationssoftware führt gleichzeitig numerische Berechnungen auf den Kernen 0–14 durch, schreibt Checkpoint-Daten über io_uring auf eine lokale NVMe-SSD (Kern 15) und empfängt einen Streaming-Datenstrom über TCP (Kernel-Softirq auf Kern 15 oder IRQ-affined Kern).

In diesem Szenario teilen sich der I/O-Thread und der Netzwerk-Stack denselben physischen Kern. Wenn ein großer Checkpoint geschrieben wird und gleichzeitig ein Netzwerk-Burst ankommt, konkurrieren beide um die Ausführungszeit auf diesem Kern. Das Resultat: der Netzwerkpuffer läuft voll, Pakete werden verzögert verarbeitet, der TCP-Stack interpretiert das als Congestion, drosselt den Senderate – und der eigentlich konstante Stream stockt.

### 6.2 PCIe-Bandbreitenverteilung

Ein weiterer, oft übersehener Engpass ist die PCIe-Busarchitektur. NVMe-SSDs, GPUs und Netzwerkkarten teilen sich die verfügbaren PCIe-Lanes der CPU. Auf einem typischen Desktop-Prozessor mit 24 PCIe-5.0-Lanes kann die gleichzeitige Nutzung einer GPU (16 Lanes), einer NVMe-SSD (4 Lanes) und einer 25-GbE-NIC (4 Lanes) die PCIe-Root-Complex-Kapazität ausreizen. Die resultierende Bandbreitenkonkurrenz äußert sich in erhöhten Latenzen auf allen drei Geräten.

In Server-Umgebungen mit dediziertem PCIe-Switching oder CXL-Anbindung (Compute Express Link) ist dieses Problem entschärft, aber nicht eliminiert. Die Topologie des PCIe-Baums – welche Geräte an welchem Root-Port hängen – hat einen messbaren Einfluss auf die erreichbaren simultanen Durchsätze.

### 6.3 Der Dominoeffekt bei Streaming-Ausfällen

Die gefährlichste Wechselwirkung tritt auf, wenn ein Streaming-Aussetzer eine Kettenreaktion auslöst: Der Netzwerk-Stream stockt (Jitter-Spike oder Bandbreiten-Einbruch), der I/O-Thread blockiert beim Warten auf Netzwerkdaten, die Simulationskerne laufen leer und werden idle, das Betriebssystem nutzt die frei werdenden Kerne für Hintergrundprozesse (Cron, Log-Rotation, Page-Reclaim), der Netzwerk-Stream kommt zurück und liefert Daten im Burst, nun müssen gleichzeitig die aufgestauten Daten verarbeitet, neue Berechnungen gestartet und verschobene I/O-Operationen nachgeholt werden. Dieses „Thundering Herd"-Muster kann das System kurzfristig überlasten und die nächsten Simulationsschritte erneut verzögern – ein selbstverstärkender Effekt.

---

## 7. Strategien zur Performance-Optimierung

### 7.1 Architekturelle Entkopplung

Die wichtigste Maßnahme ist die Entkopplung von Compute, lokaler E/A und Netzwerk-I/O durch asynchrone Pipelines mit ausreichend dimensionierten Puffern. Ring-Buffer zwischen Netzwerk-Empfänger und Berechnungskern fangen kurze Streaming-Unterbrechungen ab, ohne dass der Compute-Thread blockiert. Die Tiefe dieser Puffer muss auf Basis der erwarteten Jitter-Verteilung dimensioniert werden – nicht auf Basis des Durchschnitts, sondern des 99. Perzentils.

### 7.2 Dediziertes IRQ- und Thread-Pinning

Durch explizites Pinning von Netzwerk-IRQs und I/O-Threads auf dedizierte CPU-Kerne (die nicht für Simulationsberechnungen verwendet werden) lässt sich die Interferenz zwischen den Lastdimensionen drastisch reduzieren. Auf einem 16-Kern-System könnte eine sinnvolle Aufteilung so aussehen: Kerne 0–11 für Simulationsberechnungen, Kerne 12–13 für lokale E/A (io_uring-Worker), Kerne 14–15 für Netzwerk-Softirqs und Streaming-Empfänger.

### 7.3 Adaptives Streaming mit Rückstaukontrolle

Anstatt einen festen Streaming-Datentakt anzunehmen, sollte die Software ein adaptives Modell implementieren. Dieses überwacht die aktuelle Netzwerk-Performance (RTT, Durchsatz, Jitter) in Echtzeit und passt die Simulationsschrittweite oder den Prefetch-Horizon dynamisch an. Wenn die Streaming-Rate sinkt, wird proaktiv mehr voraus-gepuffert; wenn sie stabil ist, wird der Puffer abgebaut, um Speicher freizugeben. Das Konzept ist vergleichbar mit dem Adaptive-Bitrate-Streaming (ABR) in der Videoübertragung, adaptiert auf den Kontext numerischer Datenströme.

### 7.4 Speicher-Tiering und lokales Caching

Für Cloud-basierte Datenquellen empfiehlt sich ein lokaler Cache-Layer, der häufig benötigte Datensätze auf der NVMe-SSD vorhält. Eine LRU- oder LFU-basierte Eviction-Strategie sorgt dafür, dass das begrenzte lokale Speichervolumen optimal genutzt wird. Bei vorhersagbaren Zugriffsmustern (z. B. zeitliche Sequenzen in Wettersimulationen) kann ein Prefetch-Algorithmus Daten proaktiv vom Netzwerk auf die SSD ziehen, bevor sie benötigt werden.

### 7.5 Monitoring und Profiling

Ohne kontinuierliches Monitoring bleibt die Performance-Analyse Spekulation. Folgende Metriken sollten im laufenden Betrieb erfasst werden:

| Metrik | Werkzeug (Linux) | Relevanz |
|---|---|---|
| CPU-Auslastung pro Kern | `perf`, `mpstat`, `htop` | Erkennung von Idle-Kernen durch I/O-Stalls |
| Cache-Miss-Rate | `perf stat` (LLC-misses) | Memory-Bandbreiten-Engpass |
| I/O-Latenz und IOPS | `iostat`, `bpftrace`, `blktrace` | Lokale Storage-Engpässe |
| Netzwerk-Durchsatz und Jitter | `ss`, `nstat`, `tc`, Prometheus+Grafana | Streaming-Stabilität |
| IRQ-Verteilung | `/proc/interrupts`, `irqtop` | Erkennung von IRQ-Stürmen |
| PCIe-Bandbreite | `pcm`, Intel VTune | Bus-Konkurrenz |

---

## 8. Hardware-Empfehlungen im Überblick

Basierend auf den analysierten Performance-Dimensionen ergeben sich folgende Richtlinien für die Hardware-Auswahl:

**Prozessor:** Hohe Single-Thread-Performance (IPC × Taktfrequenz) ist für die meisten Simulationen wichtiger als eine extrem hohe Kernzahl. AVX-512-Unterstützung ist vorteilhaft, sofern die Software vektorisiert ist. Für verteilte Simulationen sind ausreichend Kerne für dedizierte I/O-Threads einzuplanen – also mindestens 2–4 Kerne über dem Bedarf der reinen Berechnung.

**Arbeitsspeicher:** Ausreichend Kapazität für den gesamten aktiven Datensatz plus Ring-Buffer plus Page-Cache. ECC-RAM ist bei langen Simulationsläufen Pflicht. Die Speicherbandbreite (Anzahl der Speicherkanäle) ist häufig relevanter als die Gesamtkapazität – ein Quad-Channel-Setup mit 128 GB übertrifft ein Dual-Channel-Setup mit 256 GB in den meisten Simulationen.

**Storage:** NVMe-SSDs der aktuellen Generation (PCIe 4.0 oder 5.0) sind für Checkpoint-I/O und lokales Caching quasi Pflicht. Für maximale Zuverlässigkeit bei intensivem Schreibbetrieb sind Enterprise-Grade-SSDs mit hoher DWPD-Spezifikation (Drive Writes Per Day) empfehlenswert.

**Netzwerk:** Für LAN-basierte verteilte Simulationen empfehlen sich 25-GbE- oder 100-GbE-NICs mit RDMA-Fähigkeit. Für WAN-Streaming ist die NIC-Geschwindigkeit selten der Engpass – hier sind stabile, niedrig-latente Internetanbindungen und ein gut konfigurierter TCP-Stack wesentlich wichtiger.

---

## 9. Fazit

Die Performance von Simulationssoftware mit CPU-, E/A- und Streaming-Anforderungen ist ein Zusammenspiel aus mindestens drei Hardware-Dimensionen, deren Wechselwirkungen komplexer sind als die Summe ihrer Einzelkomponenten. Der vermeintlich „konstante" Netzwerk-Stream erweist sich in der Praxis als die volatilste und unberechenbarste Komponente: TCP-Congestion, Jitter, Shared Bandwidth und Routing-Änderungen untergraben jede Annahme von Gleichmäßigkeit.

Die zentrale Erkenntnis dieses Beitrags lautet: Maximale Einzelkomponenten-Performance (schnellste CPU, schnellste SSD, schnellste NIC) garantiert nicht die beste Gesamtperformance. Entscheidend ist vielmehr die architekturelle Entkopplung der drei Lastdimensionen durch asynchrone Pipelines, ausreichend dimensionierte Puffer und dedizierte Hardware-Ressourcen für jeden I/O-Pfad. Nur wenn die Software in der Lage ist, die inhärente Variabilität des Netzwerk-Streamings zu absorbieren, ohne die Berechnung zu blockieren, kann die volle Leistung der zugrunde liegenden Hardware auch tatsächlich abgerufen werden.
