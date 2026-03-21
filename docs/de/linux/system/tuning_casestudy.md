---
description: "Tuning-Fallstudie für X-Plane unter Linux: Drei Schritte von Mikrorucklern zu stabilen Framezeiten — Watermark-Tuning, IO-Latenz und NVMe-Powermanagement mit realen Messdaten."
---
# Fallstudie: Mikroruckler eliminieren

Die Seite [Kernel-Tuning](systemtuning.md) stellt allgemeine Tuning-Profile für Standard- und Liquorix-Kernel bereit. Diese Seite geht einen Schritt weiter: Sie zeigt, wie sich speicherbedingte Ruckler **diagnostizieren** lassen, **warum** bestimmte Parameteränderungen helfen und **welche messbare Wirkung** sie haben — basierend auf systematischen Messungen (16 Runs) an einem Testsystem mit X-Plane, Ortho-Streaming und einer parallel laufenden KVM-Maschine.

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

Die folgenden drei Schritte wurden inkrementell auf dem Testsystem angewendet. Jeder Schritt adressiert einen spezifischen Engpass, und Messungen bestätigen die Wirkung vor dem nächsten Schritt.

### Schritt 1: Watermark-Tuning — kswapd Vorlauf geben

**Problem:** Der Standard-Wert von `vm.min_free_kbytes` ist zu klein für Workloads, die Speicher in großen Schüben allozieren (Szenerie-Laden, Ortho-Tile-Dekompression). kswapd wacht zu spät auf, und Direct Reclaim übernimmt — wobei Anwendungs-Threads blockiert werden.

**Lösung:** Der Kernel verwaltet drei [Watermarks](swap.md#watermarks) pro Speicherzone: WMARK_HIGH (kswapd schläft), WMARK_LOW (kswapd wacht auf) und WMARK_MIN (Direct Reclaim). Der Abstand zwischen LOW und MIN ist der kswapd-Vorlauf — je größer, desto unwahrscheinlicher wird Direct Reclaim.

Zwei Parameter steuern dies:

- `vm.min_free_kbytes` setzt WMARK_MIN — die Notreserve. Aber es verschiebt auch alle Watermarks nach oben und sperrt RAM für den Userspace.
- `vm.watermark_scale_factor` setzt den **Abstand** zwischen den Watermarks unabhängig von der Notreserve.

Die zentrale Erkenntnis: `min_free_kbytes` konservativ (1 GB) und `watermark_scale_factor` aggressiv (500) einsetzen, um maximalen kswapd-Vorlauf bei minimalem RAM-Verlust zu erreichen:

```
ANSATZ A: min_free_kbytes=3GB, watermark_scale_factor=125
  WMARK_MIN  = 3,0 GB  (gesperrt — verschwendet)
  WMARK_LOW  = 4,2 GB  (kswapd wacht auf)
  WMARK_HIGH = 5,4 GB
  Vorlauf    = 1,2 GB

ANSATZ B: min_free_kbytes=1GB, watermark_scale_factor=500
  WMARK_MIN  = 1,0 GB  (nur 1 GB gesperrt)
  WMARK_LOW  = 5,8 GB  (kswapd wacht FRÜHER auf)
  WMARK_HIGH = 10,6 GB (MEHR Vorlauf)
  Vorlauf    = 4,8 GB
```

Ansatz B liefert 4x mehr kswapd-Vorlauf bei 2 GB weniger verschwendetem RAM.

**Gemessene Wirkung**

| Watermark-Tuning | Direct Reclaim Main Thread | Max Latenz | FPS < 25 |
|---|---|---|---|
| Default (min_free=66 MB) | 12.472 Events | 80 ms | 6,9% |
| min_free=2 GB, wsf=125 | 0 (kurze Flüge) | 0 ms | 3,1% |
| min_free=2 GB, wsf=125 | 20.515 (Europa 90 min) | 80 ms | 3,8% |
| min_free=3 GB, wsf=125 | 0 (Europa 150 min) | 0 ms | 3,6% |

Die Tabelle oben zeigt, dass ausreichender Watermark-Abstand Direct Reclaim eliminiert — `min_free_kbytes=3GB` mit `wsf=125` erreichte selbst bei 150-minütigen Flügen null Events. Die finale Konfiguration (`min_free_kbytes=1GB`, `watermark_scale_factor=500`) bietet den gleichen Schutz bei weniger RAM-Verschwendung: der kswapd-Vorlauf ist sogar größer (4,8 GB vs. 1,2 GB), während die Notreserve von 3 GB auf 1 GB sinkt.

**Vollständige sysctl-Konfiguration**

```ini title="/etc/sysctl.d/99-xplane-tuning.conf"
vm.min_free_kbytes = 1048576
vm.watermark_scale_factor = 500
vm.swappiness = 8
vm.page_cluster = 0
vm.vfs_cache_pressure = 100
vm.dirty_background_ratio = 3
vm.dirty_ratio = 10
```

```bash
sudo sysctl --system
```

| Parameter | Standard | Optimiert | Wirkung |
|---|---|---|---|
| `vm.min_free_kbytes` | ~67 MB | 1 GB | Notreserve — kswapd wacht mit Vorlauf auf |
| `vm.watermark_scale_factor` | 10 | 500 | kswapd-Vorlauf ~4,8 GB statt ~96 MB |
| `vm.swappiness` | 60 | 8 | Swap nur bei echtem Druck — heiße Anonymous Pages schützen |
| `vm.page_cluster` | 3 | 0 | Einzel-Page-Swap-Reads — NVMe hat keinen Seek-Overhead, Readahead verschwendet RAM bei Speicherdruck |
| `vm.vfs_cache_pressure` | 100 | 100 | Standard — kein Tuning nötig |
| `vm.dirty_background_ratio` | 10% | 3% | Writeback startet ab ~2,9 GB statt ~9,4 GB |
| `vm.dirty_ratio` | 20% | 10% | Hard-Limit bei ~9,6 GB statt ~18,8 GB |

Details zur Interaktion von [Watermarks](swap.md#watermarks) und [kswapd](swap.md#page-reclaim) auf der Swap-Seite.

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

**Gemessene Wirkung:** Durchschnittliche Write-Latenz sank von 36–47 ms auf 1,8 ms. TLB-Shootdowns (ein Nebeneffekt von übermäßigem Page-Remapping) fielen in vmstat auf null.

### Schritt 3: NVMe-Powermanagement — Aufwach-Latenz eliminieren

**Problem:** NVMe-SSDs im Energiesparmodus haben Aufwachlatenzen im Millisekundenbereich — länger als ein kompletter Frame bei 60 Hz. Block-Tracing zeigte ein charakteristisches 10–11-ms-Muster, das mit Frame-Drops korrelierte.

**Lösung:** NVMe Autonomous Power State Transitions (APST) deaktivieren, um die Laufwerke im latenzärmsten Betriebszustand zu halten.

In `/etc/default/grub` den Parameter `GRUB_CMDLINE_LINUX_DEFAULT` erweitern:

```
nvme_core.default_ps_max_latency_us=0
```

```bash
sudo update-grub
```

Neustart erforderlich.

!!! note "Laufzeitänderungen"
    Der sysfs-Parameter `/sys/module/nvme_core/parameters/default_ps_max_latency_us` wirkt nur auf **neu initialisierte** NVMe-Geräte. Für bereits aktive Geräte per-Device PM QOS verwenden:
    ```bash
    for dev in /sys/class/nvme/nvme*/device/power/pm_qos_latency_tolerance_us; do echo 0 | sudo tee "$dev"; done
    ```
    Die GRUB-Methode ist der zuverlässigste Weg.

**Gemessene Wirkung:** 97% der langsamen I/O-Events (>5 ms) wurden eliminiert. Das charakteristische 10–11-ms-Muster im Block-Tracing verschwand vollständig.

---

## Ergebniszusammenfassung

Die kombinierte Wirkung aller drei Schritte, gemessen auf dem Testsystem (Gleichgewichtsphasen-Werte aus einer mehrstündigen Sitzung):

| Metrik | Ausgangszustand | Nach Tuning | Veränderung |
|---|---|---|---|
| Direct Reclaim (max) | 75.000 Pages/s | 0/s (Gleichgewicht) | Eliminiert |
| Alloc Stalls (max) | 1.000/s | 0/s (Gleichgewicht) | Eliminiert |
| Dirty Pages (Durchschnitt) | 502 MB | 2,4 MB | -99% |
| NVMe Write-Latenz (Durchschnitt) | 36 ms | 6 ms | -83% |
| NVMe Write-Latenz (max, Gleichgewicht) | 260 ms | 44 ms | -83% |
| NVMe Write-Volumen | 25 GB/Sitzung | 3,6 GB/Sitzung | -86% |

!!! tip "Verallgemeinerbare Erkenntnisse"
    Die konkreten Werte hängen von System und Workload ab, aber die **Prinzipien** sind allgemein übertragbar:

    1. **kswapd Vorlauf geben via watermark_scale_factor** — wirksamer als `min_free_kbytes` zu erhöhen, das RAM verschwendet
    2. **Software-Overhead auf NVMe entfernen** — Multi-Queue-Hardware profitiert nicht von einem Software-Scheduler
    3. **NVMe-Energiesparen deaktivieren** — Aufwachlatenzen verursachen messbare Frame-Drops
    4. **Vorher und nachher messen** — aggregierte Zähler aus `/proc/vmstat` reichen aus, um zu bestätigen, ob eine Änderung die beabsichtigte Wirkung hatte

### Praxisnotizen: Lehren aus dem Tuning-Prozess

Die drei Schritte oben sind als saubere Progression dargestellt, aber der tatsächliche Tuning-Prozess umfasste 16 Messläufe und revidierte Schlussfolgerungen. Einige Beobachtungen:

- **Parameter interagieren nichtlinear.** Eine Parameteränderung kann Schlussfolgerungen über andere Parameter invalidieren. Bei signifikanten Änderungen immer das Gesamtset neu evaluieren.
- **Das Drei-Phasen-Muster ist konsistent.** Jeder Run zeigte das gleiche Aufwärm- → Aufbau- → Gleichgewichtsmuster. Tuning beeinflusst primär die Dauer und Schwere der Aufbauphase. Wenn das System im Gleichgewicht stabil ist, aber in den ersten 30–60 Minuten stottert, auf Watermark-Tuning fokussieren statt auf CPU- oder GPU-Optimierung.
- **NVMe-Power-State-Latenz ist real und messbar.** Die Deaktivierung von APST (`pm_qos_latency_tolerance_us=0`) eliminierte 97% der langsamen I/O-Events (>5 ms). Das ist eine Low-Effort-/High-Impact-Änderung für jede latenzsensitive NVMe-Workload — nicht nur für Flugsimulation.

---

## Weiterführende Kapitel

| Thema | Seite | Schwerpunkt |
|---|---|---|
| Kernel-Tuning | [Kernel-Tuning](systemtuning.md) | Zwei Tuning-Profile — Standardkernel vs. Liquorix |
| Swap & Speicherverwaltung | [Swap & Speicherverwaltung](swap.md) | Page Reclaim, Watermarks, Swappiness |
| Monitoring | [Monitoring](systemtools.md) | Werkzeuge zur Messung jeder hier referenzierten Metrik |
| Latenz | [Latenz und Vorhersagbarkeit](../../fundamentals/performance/latency.md) | Warum Latenz wichtiger ist als Durchsatz |
| Dateisystem | [Dateisystem](../optimizations/filesystem.md) | IO-Scheduler, Mount-Optionen, SSD-Tuning |

---

## Quellen

- [/proc/sys/vm/ — Linux Kernel Documentation](https://docs.kernel.org/admin-guide/sysctl/vm.html) — vm.min_free_kbytes, Dirty Ratios, Swappiness, Watermark-Parameter
- [Memory Management Concepts — Linux Kernel Documentation](https://docs.kernel.org/admin-guide/mm/concepts.html) — Page Reclaim, Watermarks, kswapd-Verhalten
- [Block layer: Writeback Throttling — LWN](https://lwn.net/Articles/682582/) — WBT-Mechanismus und wann er zu deaktivieren ist
- [Solid State Drive/NVMe — Arch Wiki](https://wiki.archlinux.org/title/Solid_state_drive/NVMe) — NVMe-Energieverwaltung (APST)
