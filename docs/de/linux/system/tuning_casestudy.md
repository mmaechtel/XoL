---
description: "Tuning-Fallstudie für X-Plane unter Linux: Vier Schritte von Mikrorucklern zu stabilen Framezeiten — Memory Pressure, IO-Latenz, Swap-Ziel und Watermark-Tuning mit realen Messdaten."
---
# Fallstudie: Mikroruckler eliminieren

Die Seite [Kernel-Tuning](systemtuning.md) stellt allgemeine Tuning-Profile für Standard- und Liquorix-Kernel bereit. Diese Seite geht einen Schritt weiter: Sie zeigt, wie sich speicherbedingte Ruckler **diagnostizieren** lassen, **warum** bestimmte Parameteränderungen helfen und **welche messbare Wirkung** sie haben — basierend auf systematischen Messungen an einem Testsystem mit X-Plane, Ortho-Streaming und einer parallel laufenden KVM-Maschine.

!!! note "Verhältnis zu den Tuning-Profilen"
    Die sysctl-Werte in dieser Fallstudie sind aggressiver als [Profil B](systemtuning.md#profil-b-liquorix-kernel) — sie wurden für einen schweren Workload mit gleichzeitigem Ortho-Streaming, Addon-Szenerie und einem KVM-Gast optimiert. Profil B ist ein sicherer Ausgangspunkt; die Werte hier zeigen, wie weit die Parameter getrieben werden können, wenn Messungen den Bedarf bestätigen.

## Das Problem: Frame-Drops während des Flugs

### Was der Pilot sieht

Ein Flug beginnt flüssig bei 40+ FPS. Nach 15–20 Minuten — typischerweise beim Überqueren von Szenerie-Kachelgrenzen oder wenn [Ortho-Streaming](../../scenery/ortho_streaming/how_streaming_works.md) eine neue Region lädt — friert das Bild für 1–2 Sekunden ein. Die FPS fallen auf einstellige Werte, erholen sich kurz und ruckeln erneut. Das Muster wiederholt sich alle 10–15 Minuten, immer bei Szenerieübergängen. Zwischen den Episoden ist die Leistung normal.

Diese Mikroruckler entstehen nicht durch unzureichende GPU- oder CPU-Leistung. Sie haben ihren Ursprung im **Speichersubsystem** — der Kernel kann Daten nicht schnell genug liefern, weil die Speicherverwaltung falsch konfiguriert ist.

### Was das System tut

Jedes sichtbare Symptom entspricht einem konkreten Kernel-Mechanismus:

| Symptom | Kernel-Ursache | Mechanismus |
|---|---|---|
| 1–2 Sekunden Freeze | [Direct Reclaim](swap.md#page-reclaim) | Der allozierende Prozess wird blockiert, während der Kernel synchron Speicher freigibt |
| FPS fallen auf einstellige Werte | Alloc Stalls | Threads warten auf Speicher-Allokation — Render-Thread kann keine Frames einreichen |
| Ruckeln bei Szenerieübergängen | [kswapd](swap.md#page-reclaim) überlastet | Hintergrund-Reclaim kommt mit der Allokationsrate nicht nach |
| Periodisches Muster (alle 10–15 Min) | Szenerie-Kachel-Laden | X-Plane + Ortho-Streaming fordern gleichzeitig große Speichermengen an |

Auf dem Testsystem im Ausgangszustand waren die Auswirkungen messbar: Direct Reclaim erreichte bis zu 75.000 Pages/s, Alloc Stalls stiegen auf über 1.000/s, und Dirty Pages akkumulierten durchschnittlich 500 MB mit Spitzen über 1 GB.

---

## Monitoring: Was messen und warum

### Wichtige Kernel-Metriken

Vor dem Tuning muss identifiziert werden, **welches** Subsystem das Problem verursacht. Der Kernel stellt die relevanten Zähler über `/proc/vmstat` und `/proc/meminfo` bereit:

| Metrik | Quelle | Was sie verrät |
|---|---|---|
| `allocstall_normal` | /proc/vmstat | Blockierte Threads, die auf Speicher warten — die direkte Stotter-Ursache |
| `pgsteal_direct` | /proc/vmstat | Synchron zurückgewonnene Pages — jedes Event blockiert einen Prozess |
| `pgscan_kswapd` | /proc/vmstat | Hintergrund-Reclaim-Aktivität — hohe Werte zeigen Memory Pressure an |
| `nr_dirty` | /proc/vmstat | Ausstehende Dirty Pages — Akkumulation zeigt Writeback-Engpass |
| `nr_free_pages` | /proc/vmstat | Aktuell freier Speicher — niedrige Werte lösen Reclaim aus |
| `MemAvailable` | /proc/meminfo | Verfügbarer Speicher ohne Swapping — der praktische Spielraum |
| `SwapUsed` | /proc/meminfo | Aktuelle Swap-Nutzung — steigende Werte während des Flugs zeigen Druck an |

GPU-Metriken (Auslastung, VRAM, Leistungsaufnahme) via NVML ergänzen die Kernel-Daten — sinkende GPU-Auslastung bei laufendem Prozess zeigt an, dass das CPU-/Speichersubsystem die GPU aushungert.

??? abstract "Fortgeschritten: Tracing pro Prozess"

    Aggregierte Zähler zeigen, **dass** Reclaim stattfindet, aber nicht **welcher Prozess** es ausgelöst hat. Für gezielte Diagnose bieten Kernel-Tracepoints Zuordnung pro Event:

    - `vmscan:mm_vmscan_direct_reclaim_begin/end` — Dauer jedes Direct-Reclaim-Events, markiert mit dem auslösenden Prozess. Zeigt, ob X-Planes Render-Thread betroffen ist oder ein Hintergrundprozess.
    - `block:block_rq_issue/complete` (gefiltert auf Latenz >5 ms) — identifiziert NVMe-IO-Ausreißer, die mit Frame-Drops korrelieren.

    Zugriff auf diese Tracepoints erfolgt über `bpftrace` oder `perf` (siehe [Monitoring](systemtools.md) für Tool-Details). Die Kernaussage: Wenn der Render-Thread in Direct-Reclaim-Events auftaucht, sind die Ruckler speicherbedingt.

### Drei-Phasen-Muster

Eine typische Flugsitzung zeigt drei unterscheidbare Phasen:

| Phase | Dauer | Verhalten |
|---|---|---|
| **Aufwärmphase** | Erste 5–10 Min | Initiales Szenerie-Laden, hohe Allokationsrate, etwas Reclaim-Aktivität ist normal |
| **Aufbauphase** | 10–30 Min | Szenerieübergänge erzeugen periodische Memory-Pressure-Spitzen — hier treten die Ruckler auf |
| **Gleichgewichtsphase** | Nach 30+ Min | Cache ist warm, Allokationen stabilisieren sich, Reclaim-Aktivität sinkt auf nahezu null |

Das Tuning sollte auf die **Aufbauphase** abzielen — die Gleichgewichtsphase ist auch bei suboptimalen Einstellungen typischerweise in Ordnung. Messungen sollten mindestens 60 Minuten abdecken, um den Übergang zwischen den Phasen zu erfassen.

---

## Tuning-Schritte: Vom Chaos zur Stabilität

Die folgenden vier Schritte wurden inkrementell auf dem Testsystem angewendet. Jeder Schritt adressiert einen spezifischen Engpass, und Messungen bestätigen die Wirkung vor dem nächsten Schritt.

### Schritt 1: Memory Pressure — kswapd Vorlauf geben

**Problem:** Der Standard-Wert von `vm.min_free_kbytes` ist zu klein für Workloads, die Speicher in großen Schüben allozieren (Szenerie-Laden, Ortho-Tile-Dekompression). kswapd wacht zu spät auf, und Direct Reclaim übernimmt — wobei Anwendungs-Threads blockiert werden.

**Lösung:** Die freie Speicherreserve erhöhen, damit kswapd früher mit dem Reclaim beginnt, bevor Direct Reclaim ausgelöst wird. Gleichzeitig die Dirty-Page-Limits straffen, um Writeback-Stürme zu verhindern.

```ini title="/etc/sysctl.d/99-xplane-tuning.conf"
vm.min_free_kbytes = 1048576
vm.dirty_background_ratio = 1
vm.dirty_ratio = 5
vm.dirty_expire_centisecs = 1500
vm.dirty_writeback_centisecs = 500
```

```bash
sudo sysctl --system
```

| Parameter | Standard | Optimiert | Wirkung |
|---|---|---|---|
| `vm.min_free_kbytes` | ~67 MB | 1 GB | kswapd wacht mit 1 GB Vorlauf statt 67 MB auf |
| `vm.dirty_background_ratio` | 10% | 1% | Writeback startet ab ~940 MB statt ~9,4 GB |
| `vm.dirty_ratio` | 20% | 5% | Hard-Limit bei ~4,7 GB statt ~18,8 GB |
| `vm.dirty_expire_centisecs` | 3000 | 1500 | Dirty Pages nach 15s statt 30s geflusht |
| `vm.dirty_writeback_centisecs` | 500 | 500 | Flush-Thread-Intervall (unverändert) |

Details zur Interaktion von [Watermarks](swap.md#watermarks) und [kswapd](swap.md#page-reclaim) auf der Swap-Seite.

**Gemessene Wirkung:** Direct Reclaim fiel von 75.000 Pages/s auf null während des normalen Flugs. Dirty Pages sanken von durchschnittlich 502 MB auf 33 MB. Die wirksamste Einzelmaßnahme.

### Schritt 2: IO-Latenz — Software-Overhead auf NVMe entfernen

**Problem:** Der Standard-IO-Scheduler (`kyber` oder `mq-deadline`) und Write-Back Throttling (WBT) fügen softwareseitige Warteschlangenverzögerungen hinzu. Auf NVMe-Laufwerken mit Hardware-Multi-Queue-Unterstützung ist dieser Overhead unnötig und erhöht die Write-Latenz — besonders bei Btrfs-Metadata-Commits.

**Lösung:** IO-Scheduler auf `none` setzen und WBT deaktivieren. NVMe-Laufwerke übernehmen die Queue-Verwaltung in Hardware.

| Parameter | Standard | Optimiert | Wirkung |
|---|---|---|---|
| IO-Scheduler | `kyber` oder `mq-deadline` | `none` | Software-Scheduler umgehen — direkter Hardware-Queue-Zugriff |
| WBT (`wbt_lat_usec`) | 2000 µs | 0 (deaktiviert) | Keine Write-Drosselung — NVMe handhabt Stau intern |
| Readahead | Variiert | 256 KB | Ausgewogener Kompromiss für gemischte sequentielle/zufällige IO |

Diese Einstellungen lassen sich persistent per udev-Regeln anwenden:

```ini title="/etc/udev/rules.d/60-nvme-tuning.rules"
ACTION=="add|change", KERNEL=="nvme[0-9]*n1", ATTR{queue/scheduler}="none"
ACTION=="add|change", KERNEL=="nvme[0-9]*n1", ATTR{queue/wbt_lat_usec}="0"
ACTION=="add|change", KERNEL=="nvme[0-9]*n1", ATTR{queue/read_ahead_kb}="256"
```

!!! note "Nur für NVMe"
    Der Scheduler `none` ist nur für [NVMe](../../glossary.md#nvme-non-volatile-memory-express)-Laufwerke sicher, da diese das Queuing in Hardware verwalten. SATA-SSDs und HDDs profitieren weiterhin von einem Software-Scheduler (`mq-deadline` oder `bfq`).

**Gemessene Wirkung:** Durchschnittliche Write-Latenz sank von 36–47 ms auf 1,8 ms. Die p95-Latenz fiel von 260–312 ms auf unter 50 ms. TLB-Shootdowns (ein Nebeneffekt von übermäßigem Page-Remapping) fielen in vmstat auf null.

### Schritt 3: Swap-Ziel — zram statt NVMe

**Problem:** Wenn Swap auf derselben NVMe wie X-Plane-Daten und Ortho-Caches liegt, konkurrieren drei IO-Ströme: Swap-Pages, Szenerie-Dateien und Ortho-Kacheln. Bei Memory Pressure sättigt Swap-IO das Laufwerk und blockiert das Szenerie-Laden — sichtbar als sekundenlange DSF-Ladezeiten.

**Lösung:** [zram](swap.md#zram) als primäres Swap-Device verwenden. zram komprimiert Pages im RAM — es findet keine Disk-IO statt. Die NVMe-Swap-Partition dient nur als Notfall-Fallback.

| Konfiguration | Latenz | IO-Kontention |
|---|---|---|
| Swap auf gleicher NVMe | ~15 µs + Queue-Wartezeit | Konkurriert mit Szenerie- und Ortho-IO |
| Swap auf dedizierter NVMe | ~15 µs | Eliminiert |
| **zram (lz4)** | **~1,7 µs** | **Keine — vollständig im RAM** |

Für die zram-Einrichtung und den Vergleich mit zswap siehe [zram](swap.md#zram).

**Gemessene Wirkung:** NVMe-Swap wurde nie angesprochen — zram absorbierte 100% des Swap-Traffics. Das Write-Volumen auf der zuvor umkämpften NVMe sank um 86%. Die DSF-Worst-Case-Ladezeit verbesserte sich von 63 Sekunden auf 22 Sekunden.

### Schritt 4: Swap-Readahead und zram-Tuning

**Problem:** Der Standard-Wert `vm.page-cluster=3` veranlasst den Kernel, 8 Pages (32 KiB) pro Swap-Zugriff als Readahead zu lesen. Bei zram muss jede Page einzeln dekomprimiert werden — Readahead bringt keinen Vorteil und erhöht die Latenz.

**Lösung:** Page-Cluster auf 0 setzen (Einzel-Page-Reads). Dieser Wert wurde als Teil des sysctl-Tunings in den Testruns gemessen.

Das Testsystem verwendete `vm.swappiness=1` mit zram — eine konservative Einstellung, die Anonymous-Page-Scanning minimiert. Die [Swap-Seite](swap.md#empfohlene-konfiguration) empfiehlt `swappiness=180` für zram-Konfigurationen, was idle Pages proaktiv in komprimierten Swap verschiebt, um RAM für den Page Cache freizugeben. Beide Ansätze sind valide — die Wahl hängt vom Workload ab:

| Einstellung | Verhalten | Geeignet für |
|---|---|---|
| `swappiness=1` (getestet) | Vermeidet Swapping fast vollständig, reclaimed zuerst File Pages | Systeme mit ausreichend RAM, wo Swap als Sicherheitsnetz dient |
| `swappiness=180` (empfohlen für zram) | Komprimiert idle Pages proaktiv, gibt RAM für File Cache frei | Systeme unter anhaltendem Speicherdruck durch Ortho-Streaming |

Zusätzliche zram-spezifische Parameter aus der [Swap-Seite](swap.md#empfohlene-konfiguration):

```ini title="/etc/sysctl.d/99-zram.conf"
vm.page-cluster = 0
vm.watermark_boost_factor = 0
vm.watermark_scale_factor = 125
```

```bash
sudo sysctl --system
```

`watermark_boost_factor=0` deaktiviert einen Mechanismus, der für rotierende Festplatten entworfen wurde (irrelevant für zram). `watermark_scale_factor=125` vergrößert den Abstand zwischen den Watermarks und gibt kswapd mehr Zeit zum Reclaim, bevor Direct Reclaim einsetzt.

**Gemessene Wirkung (page-cluster=0):** Teil des gesamten sysctl-Tunings, das ab Schritt 1 angewendet wurde. Die kombinierten Gleichgewichtsphasen-Ergebnisse nach allen Schritten zeigt die Zusammenfassung unten.

---

## Ergebniszusammenfassung

Die kombinierte Wirkung aller vier Schritte, gemessen während einer 90-minütigen Flugsitzung auf dem Testsystem:

| Metrik | Ausgangszustand | Nach Tuning | Veränderung |
|---|---|---|---|
| Direct Reclaim (max) | 75.000 Pages/s | 0/s (Gleichgewicht) | Eliminiert |
| Alloc Stalls (max) | 1.000/s | 0/s (Gleichgewicht) | Eliminiert |
| Dirty Pages (Durchschnitt) | 502 MB | 2,4 MB | -99% |
| NVMe Write-Latenz (Durchschnitt) | 36 ms | 6 ms | -83% |
| NVMe Write-Latenz (p95) | 260 ms | 44 ms | -83% |
| Swap auf NVMe | Aktiv (1,1 GB Churn/5 Min) | Inaktiv (zram absorbiert 100%) | Eliminiert |
| DSF-Ladezeit (Worst Case) | 63 s | 22 s | -65% |
| NVMe Write-Volumen | 25 GB/Sitzung | 3,6 GB/Sitzung | -86% |

!!! tip "Verallgemeinerbare Erkenntnisse"
    Die konkreten Werte hängen von System und Workload ab, aber die **Prinzipien** sind allgemein übertragbar:

    1. **kswapd Vorlauf geben** — `min_free_kbytes` sollte zur Burst-Allokationsrate passen, nicht dem Systemstandard entsprechen
    2. **Swap von Daten-IO trennen** — zram eliminiert die Kontention vollständig, ohne dedizierte SSD
    3. **Software-Overhead auf NVMe entfernen** — Multi-Queue-Hardware profitiert nicht von einem Software-Scheduler
    4. **Vorher und nachher messen** — aggregierte Zähler aus `/proc/vmstat` reichen aus, um zu bestätigen, ob eine Änderung die beabsichtigte Wirkung hatte

---

## Weiterführende Kapitel

| Thema | Seite | Schwerpunkt |
|---|---|---|
| Kernel-Tuning | [Kernel-Tuning](systemtuning.md) | Zwei Tuning-Profile — Standardkernel vs. Liquorix |
| Swap & Speicherverwaltung | [Swap & Speicherverwaltung](swap.md) | Page Reclaim, Watermarks, zram-Setup, Swappiness |
| Monitoring | [Monitoring](systemtools.md) | Werkzeuge zur Messung jeder hier referenzierten Metrik |
| Latenz | [Latenz und Vorhersagbarkeit](../../fundamentals/performance/latency.md) | Warum Latenz wichtiger ist als Durchsatz |
| Dateisystem | [Dateisystem](../optimizations/filesystem.md) | IO-Scheduler, Mount-Optionen, SSD-Tuning |

---

## Quellen

- [/proc/sys/vm/ — Linux Kernel Documentation](https://docs.kernel.org/admin-guide/sysctl/vm.html) — vm.min_free_kbytes, Dirty Ratios, Swappiness, Watermark-Parameter
- [Memory Management Concepts — Linux Kernel Documentation](https://docs.kernel.org/admin-guide/mm/concepts.html) — Page Reclaim, Watermarks, kswapd-Verhalten
- [zram block device — Linux Kernel Documentation](https://docs.kernel.org/admin-guide/blockdev/zram.html) — Komprimierter Swap im RAM
- [Block layer: Writeback Throttling — LWN](https://lwn.net/Articles/682582/) — WBT-Mechanismus und wann er zu deaktivieren ist
- [Zram — Arch Wiki](https://wiki.archlinux.org/title/Zram) — Praktische Einrichtung und Tuning-Empfehlungen
