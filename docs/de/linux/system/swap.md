---
description: "Linux Swap und Speicherverwaltung für X-Plane: Page-Reclaim-Mechanik, Watermark-Tuning, Swap-Konfiguration und Tuning-Empfehlungen für die Flugsimulation."
---
# Swap & Speicherverwaltung

[X-Plane](../../glossary.md#x-plane) mit Addons und Ortho-Streaming kann 20–30 GB RAM verbrauchen. Wenn der physische Speicher erschöpft ist, beginnt der Linux-Kernel zu swappen — Speicherseiten auf die Festplatte auszulagern. Bei einer Echtzeit-Rendering-Anwendung verursacht jedes Swap-In einen Page Fault, der den Rendering-Thread blockiert. Ein Verständnis der Kernel-Speicherverwaltung und die richtige Swap-Konfiguration verhindern Stotterer, Frame-Drops und OOM-Kills.

## Wie Swap funktioniert

### Page Reclaim

Der Kernel verwaltet physischen Speicher in **Pages** (je 4 KiB). Wenn der freie Speicher unter definierte Schwellwerte fällt, muss der Kernel Pages zurückgewinnen. Er unterscheidet zwei Kategorien:

- **File-backed Pages** (Page Cache): Zwischengespeicherte Daten von Dateien auf der Festplatte. Clean Pages lassen sich sofort verwerfen, da die Daten auf der Festplatte existieren. Dirty Pages müssen zuerst zurückgeschrieben werden.
- **Anonymous Pages** (Heap, Stack, private Mappings): Haben kein Dateisystem-Backing. Diese lassen sich **nur** durch Schreiben auf Swap zurückgewinnen — ohne Swap sind sie unwiederbringlich und der Prozess wird beendet.

Reclaim läuft in zwei Modi:

| Modus | Auslöser | Verhalten |
|---|---|---|
| **kswapd** (async) | Freier Speicher < Low Watermark | Hintergrund-Thread, blockiert keine Anwendungen |
| **Direct Reclaim** (sync) | Freier Speicher < Min Watermark | Der allozierende Prozess wird blockiert, bis Pages freigegeben sind — verursacht Latenzspitzen |

Wenn auch Direct Reclaim scheitert, aktiviert der Kernel den **OOM-Killer**.

### Watermarks

Der Kernel definiert drei Schwellwerte pro Speicherzone:

| Watermark | Wirkung |
|---|---|
| WMARK_HIGH | Genügend Speicher verfügbar. kswapd schläft. |
| WMARK_LOW | kswapd erwacht und beginnt mit Hintergrund-Reclaim. |
| WMARK_MIN | Kritisch. Direct Reclaim wird ausgelöst. Allokationen werden blockiert. |

Die Watermarks werden gesteuert durch:

- `vm.min_free_kbytes`: Setzt WMARK_MIN (Standard: systemabhängig, typisch einige zehn MB)
- `vm.watermark_scale_factor`: Abstand zwischen den Watermarks (Standard: 10 = 0,1 % des RAM)

### vm.swappiness

Die vereinfachte Erklärung „steuert, wie aggressiv das System swappt" ist unvollständig. `vm.swappiness` definiert das **relative I/O-Kostenverhältnis** zwischen dem Auslagern anonymer Pages und dem Zurückgewinnen dateibasierter Pages.

**Wertebereich:** 0–200 (Standard: 60)

| Wert | Verhalten |
|---|---|
| 0 | Anonymous Pages werden **nicht** gescannt — nur dateibasierte Pages werden zurückgewonnen. Risiko: OOM-Kills trotz verfügbarem Swap. |
| 60 (Standard) | Moderate Bevorzugung von File-Reclaim. |
| 100 | Gleichgewichtung zwischen anonymen und dateibasierten Pages. |
| 200 | Dateibasierte Pages werden nicht gescannt — der Kernel lagert nur Anonymous Pages aus und bewahrt den File Cache. |

??? abstract "Kernel-interne Berechnung"

    Der Kernel berechnet die Scan-Prioritäten in `mm/vmscan.c`:

    ```
    anon_prio = swappiness
    file_prio = 200 - swappiness
    ```

    Diese Prioritäten fließen als Gewichtungsfaktoren in die Scan-Entscheidung ein. Das Verhältnis bestimmt, wie viele anonyme vs. dateibasierte Pages pro Scan-Zyklus geprüft werden. Bei `swappiness=0` werden Anonymous Pages nie gescannt — der Kernel fällt erst auf Swap zurück, wenn freie Pages unter die High Watermark fallen und keine dateibasierten Pages mehr rückgewinnbar sind.

!!! warning "swappiness=0 ist riskant"
    `swappiness=0` kann OOM-Kills verursachen, selbst wenn Swap-Speicher verfügbar ist, weil der Kernel Anonymous Pages nicht rechtzeitig scannt. Werte zwischen 1 und 10 sind sicherer für Konfigurationen mit wenig Swap.

---

## Swap-Konfiguration

### Partition vs. Datei

| Eigenschaft | Swap-Partition | Swap-Datei |
|---|---|---|
| Performance | Geringfügig besser (kein Dateisystem-Overhead) | Praktisch identisch auf ext4/XFS |
| Flexibilität | Feste Größe, Umpartitionierung nötig | Größe leicht anpassbar |
| Einrichtungsaufwand | Erfordert dedizierte Partition | Auf bestehender Partition erstellbar |

Auf ext4-Systemen sind beide Optionen gleichwertig. Swap-Dateien bieten mehr Flexibilität.

### Einrichtung auf Debian

**Swap-Partition**

```bash
# Partition mit gdisk erstellen (Typ-Code: 8200)
sudo mkswap /dev/sdXn
sudo swapon /dev/sdXn
```

Eintrag in `/etc/fstab` (UUID per `blkid /dev/sdXn` ermitteln):

```
UUID=<uuid>    none    swap    sw    0    0
```

**Swap-Datei**

```bash
sudo dd if=/dev/zero of=/swapfile bs=1M count=8192    # 8 GiB
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

Eintrag in `/etc/fstab`:

```
/swapfile    none    swap    sw    0    0
```

!!! warning "Kein fallocate verwenden"
    `fallocate` erstellt Dateien mit vorallozierten, aber ungeschriebenen Extents. Der Kernel meldet diese als Lücken, weshalb `swapon` die Datei ablehnt. Für Swap-Dateien `dd` verwenden.

### Dimensionierung

| RAM | Empfohlener Swap |
|---|---|
| 16 GB | 8–16 GB |
| 32 GB | 4–8 GB |
| 64 GB | 4 GB |

### Swap-Prioritäten

Bei mehreren konfigurierten Swap-Bereichen steuern Prioritäten die Reihenfolge:

- **Unterschiedliche Prioritäten:** Die höchste Priorität wird zuerst gefüllt. Niedrigere Prioritäten dienen als Fallback.
- **Gleiche Prioritäten:** Pages werden Round-Robin verteilt — effektives Striping über Geräte.

```
UUID=<uuid1>    none    swap    sw,pri=100    0    0
UUID=<uuid2>    none    swap    sw,pri=10     0    0
```

---

## Auswirkungen auf X-Plane

### RAM-Verbrauch

| Konfiguration | Typischer Verbrauch |
|---|---|
| Basisinstallation (Standard-Szenerie) | 10–14 GB |
| Mit Addon-Flugzeugen + Custom Scenery | 16–24 GB |
| Mit Ortho-Streaming (AutoOrtho/XEarthLayer) | 20–30+ GB |

[AutoOrtho](../../glossary.md#autoortho) allein kann bis zu 16 GB RAM verbrauchen. Auf einem 32-GB-System kann Swap-Aktivität bei Szenerie-Übergängen oder bei parallel laufenden Anwendungen auftreten.

### Was passiert, wenn X-Plane-Pages geswappt werden

Jedes Swap-In löst einen **Major Page Fault** aus: Der Rendering-Thread wird blockiert, während der Kernel die Page vom Swap-Gerät liest. Auf [NVMe](../../glossary.md#nvme-non-volatile-memory-express) dauert ein einzelnes Swap-In ~15 µs — schnell genug für gelegentliches Swapping. Auf SATA akkumulieren sich ~150 µs pro Page Fault zu sichtbarem Stottern. Auf HDD verursachen ~12 ms pro Fault sekundenlange Einfrierungen.

Bei aktivem Ortho-Streaming konkurrieren drei I/O-Ströme auf demselben Speichergerät:

1. **AutoOrtho/XEarthLayer** Cache-Schreibvorgänge ([FUSE](../../glossary.md#fuse-filesystem-in-userspace)-basiert)
2. **Swap-I/O** (Pages werden gelesen/geschrieben)
3. **DSF-Szenerie-Laden** durch X-Plane (Hintergrund-Threads)

### Gleiche SSD vs. dedizierte SSD

| Konfiguration | Auswirkung |
|---|---|
| Swap auf derselben NVMe wie X-Plane | Unproblematisch bei gelegentlichem Swapping. NVMe liefert genügend IOPS. Risiko: Tail-Latenz unter hoher Last. |
| Swap auf derselben SATA-SSD | Spürbar — Queue Depth begrenzt (NCQ: max. 32 Befehle). Swap konkurriert direkt mit Szenerie-Laden. |
| Swap auf dedizierter SSD | Eliminiert I/O-Konkurrenz vollständig. Für Desktop-/Gaming-Systeme selten nötig. |

### Latenz-Vergleich

| Medium | Random-4K-Read-Latenz | Faktor vs. RAM |
|---|---|---|
| DDR5 RAM | ~15 ns | 1x |
| NVMe SSD | ~15 µs | ~1.000x |
| SATA SSD | ~150 µs | ~10.000x |
| HDD | ~12 ms | ~800.000x |

### OOM-Killer

Wenn sowohl RAM als auch Swap erschöpft sind, aktiviert der Kernel den OOM-Killer. Er wählt den Prozess mit dem höchsten Badness-Score (primär basierend auf dem Speicherverbrauch) — fast immer X-Plane.

- X-Plane wird sofort per `SIGKILL` (Signal 9) beendet — kein sauberes Herunterfahren, kein Speichern
- Das Kernel-Log (`dmesg`) zeigt: `Out of memory: Kill process <PID> (X-Plane-x86_64)`

---

## Empfohlene Konfiguration

### Watermark-Tuning

Die wirksamste Maßnahme gegen speicherbedingte Ruckler ist Watermark-Tuning. Statt `min_free_kbytes` auf große Werte zu setzen (was RAM verschwendet), `watermark_scale_factor` verwenden, um kswapd mehr Vorlauf zu geben:

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

!!! note "Warum watermark_scale_factor=500?"
    Der Standard `watermark_scale_factor=10` erzeugt auf einem 96-GB-System nur ~96 MB Abstand zwischen den Watermarks. Bei 500 wächst der kswapd-Vorlauf auf ~4,8 GB — kswapd wacht deutlich früher auf und verhindert, dass Burst-Allokationen (Szenerie-Laden, Ortho-Tile-Dekompression) die Min-Watermark durchbrechen und Direct Reclaim auf Anwendungs-Threads auslösen. Siehe [Fallstudie Tuning](tuning_casestudy.md#schritt-1-watermark-tuning-kswapd-vorlauf-geben) für detaillierte Messdaten.

!!! note "Warum swappiness=8?"
    Mit Disk-Swap auf NVMe kostet jedes Swap-In ~15 µs — ein Page Fault, der den Rendering-Thread blockiert. Niedrige Swappiness signalisiert dem Kernel, dass Swap teuer ist: Er sollte bevorzugt dateibasierte Pages zurückgewinnen (die ohne I/O verwerfbar sind) statt Anonymous Pages auszulagern. Der große Page Cache (typisch 30–40 GB während des Flugs) bietet reichlich rückgewinnbare Pages, bevor Swap nötig wird.

### Kernel-Parameter-Übersicht

| Parameter | Wert | Wirkung |
|---|---|---|
| `vm.min_free_kbytes` | 1048576 (1 GB) | Notreserve — kswapd wacht mit Vorlauf auf |
| `vm.watermark_scale_factor` | 500 | kswapd-Vorlauf ~4,8 GB statt ~96 MB |
| `vm.swappiness` | 8 | Swap nur bei echtem Druck — heiße Anonymous Pages schützen |
| `vm.page_cluster` | 0 | Einzel-Page-Swap-Reads — NVMe hat keinen Seek-Overhead |
| `vm.vfs_cache_pressure` | 100 | Standard — kein Tuning nötig |
| `vm.dirty_background_ratio` | 3 | Writeback startet ab ~2,9 GB statt ~9,4 GB |
| `vm.dirty_ratio` | 10 | Hard-Limit bei ~9,6 GB statt ~18,8 GB |

### RAM-Dimensionierung

| RAM | Einschätzung |
|---|---|
| 16 GB | Minimum. Swap-Aktivität wahrscheinlich bei Addons oder Ortho-Streaming. Ausreichende Swap-Partition essenziell. |
| 32 GB | Komfortabel für die meisten Konfigurationen. Swap als Sicherheitsnetz für Szenerie-Übergänge. |
| 64 GB | Swap sollte unter normalen Bedingungen inaktiv bleiben. |

!!! tip "RAM ist die nachhaltige Lösung"
    Swap-Tuning ist Schadensbegrenzung. Der einzige Weg, Swap-bedingte Performance-Einbußen zuverlässig zu vermeiden, ist ausreichend physischer RAM. Für X-Plane mit Ortho-Streaming sind 32 GB die praktische Basis.

### Praxisnotizen: Dirty-Ratio-Tuning

Die Einstellungen `dirty_background_ratio` und `dirty_ratio` interagieren mit der Speicherkonfiguration auf nicht offensichtliche Weise. Während ausgedehnter Tests (16 Messläufe über mehrere Wochen mit Ortho-Streaming auf NVMe) ergaben sich folgende Beobachtungen:

- **Zu aggressives Writeback schadet auf Systemen mit viel RAM.** Mit `dirty_background_ratio=1` auf einem 96-GB-System feuert der Writeback-Daemon bei ~960 MB Dirty — praktisch jeder Tile-Cache-Schreibvorgang löst einen Flush-Zyklus aus. Das verbraucht CPU-Zyklen und I/O-Bandbreite, die mit X-Planes Rendering konkurrieren. Anheben auf `dirty_background_ratio=3` (~2,9 GB Schwelle) ließ NVMe Schreibvorgänge effizient bündeln, ohne permanentes Flushing.
- **Der dirty_ratio-Spielraum zählt mehr als der Absolutwert.** Bei `dirty_ratio=5` (~4,8 GB) war die Lücke zwischen Background- (960 MB) und synchronem (4,8 GB) Writeback zu schmal — parallele DDS-Tile-Generierung konnte sie bei Schreibschüben durchbrechen. Verbreiterung auf `dirty_ratio=10` (~9,6 GB) eliminierte Write-Stalls auf NVMe vollständig.
- **Diese Werte sind nicht universell.** Sie wurden für ein System mit drei NVMe-SSDs im RAID0 optimiert, das >6 GB/s sequentielle Schreibrate erreichen kann. Systeme mit SATA-SSDs oder einzelner NVMe benötigen möglicherweise engere Limits, um I/O-Queue-Aufstau zu verhindern.

Die empfohlenen Werte in [Profil B](systemtuning.md#profil-b-liquorix-kernel) (`dirty_background_ratio=3`, `dirty_ratio=10`) spiegeln diese Balance wider.

---

## Weiterführende Kapitel

| Thema | Seite | Schwerpunkt |
|---|---|---|
| Kernel-Tuning | [Kernel-Tuning](systemtuning.md) | CPU-Governor, sysctl-Profile, Interrupt-Affinität |
| Monitoring | [Monitoring](systemtools.md) | Swap-Aktivität verifizieren mit btop, vmstat, swapon |
| CPU & RAM | [CPU & RAM](../../fundamentals/performance/cpu_ram.md) | Wenn RAM zum Engpass wird |
| Dateisystem | [Dateisystem](../optimizations/filesystem.md) | SSD-Optimierung, I/O-Scheduler, Mount-Optionen |
| Latenz | [Latenz und Vorhersagbarkeit](../../fundamentals/performance/latency.md) | Latenzquellen und Messung |
| Fallstudie | [Fallstudie Tuning](tuning_casestudy.md) | Praktische Auswirkung von Watermark- und Speicher-Tuning mit realen Messdaten |

---

## Quellen

- [Memory Management Concepts — Linux Kernel Documentation](https://docs.kernel.org/admin-guide/mm/concepts.html)
- [/proc/sys/vm/ — Linux Kernel Documentation](https://docs.kernel.org/admin-guide/sysctl/vm.html)
- [Swap — Arch Wiki](https://wiki.archlinux.org/title/Swap)
- [Swap — Debian Wiki](https://wiki.debian.org/Swap)
