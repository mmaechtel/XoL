---
description: "Linux Swap und Speicherverwaltung für X-Plane: Page-Reclaim-Mechanik, Swap-Konfiguration, zram-Kompression und Tuning-Empfehlungen für die Flugsimulation."
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

Diese Werte decken den aktiven Betrieb ab. Mit zram (siehe unten) kann Disk-Swap kleiner ausfallen oder ganz entfallen.

### Swap-Prioritäten

Bei mehreren konfigurierten Swap-Bereichen steuern Prioritäten die Reihenfolge:

- **Unterschiedliche Prioritäten:** Die höchste Priorität wird zuerst gefüllt. Niedrigere Prioritäten dienen als Fallback.
- **Gleiche Prioritäten:** Pages werden Round-Robin verteilt — effektives Striping über Geräte.

```
UUID=<uuid1>    none    swap    sw,pri=100    0    0
UUID=<uuid2>    none    swap    sw,pri=10     0    0
```

---

## RAM-Kompression: zram vs. zswap

Anstatt auf Festplatte zu swappen, kann der Kernel Pages komprimieren und im RAM behalten. Zwei Mechanismen stehen zur Verfügung:

### zram

zram erstellt ein **komprimiertes Block-Device im RAM**, das als Swap-Gerät dient. Pages werden beim Schreiben komprimiert und beim Lesen dekomprimiert — es findet kein Disk-I/O statt.

**Algorithmen-Vergleich**

| Algorithmus | IOPS | Latenz (ns) | Kompressionsrate |
|---|---|---|---|
| lz4 | 2.033.515 | 1.708 | 2,6:1 |
| zstd | 668.715 | 5.714 | 3,4:1 |

lz4 liefert 3x niedrigere Latenz und 3x höheren Durchsatz als zstd. Für latenzempfindliche Workloads wie Flugsimulation ist lz4 die bessere Wahl.

**Einrichtung auf Debian**

```bash
sudo apt install systemd-zram-generator
```

```ini title="/etc/systemd/zram-generator.conf"
[zram0]
zram-size = min(ram / 2, 4096)
compression-algorithm = lz4
swap-priority = 100
```

```bash
sudo systemctl daemon-reload
sudo systemctl start /dev/zram0
```

Überprüfung:

```bash
swapon --show
```

### zswap

zswap ist ein **komprimierter Write-Back-Cache** vor einem Disk-Swap-Gerät. Pages werden abgefangen, bevor sie auf die Festplatte geschrieben werden, im RAM-Pool komprimiert und erst auf das dahinterliegende Swap-Gerät geschrieben, wenn der Pool voll ist (LRU-Eviction).

- Erfordert eine konfigurierte Disk-Swap-Partition oder -Datei als Backend
- Standard-Poolgröße: 20 % des RAM
- Geringerer CPU-Overhead als zram (Cache-Funktion, kein vollständiges Swap-Device)

**Aktivierung** (in `/etc/default/grub`):

```
zswap.enabled=1 zswap.compressor=zstd zswap.max_pool_percent=20
```

```bash
sudo update-grub
```

### Vergleich

| Eigenschaft | zram | zswap | Disk-Swap |
|---|---|---|---|
| Typ | Komprimiertes Swap-Device im RAM | Komprimierter Cache vor Disk-Swap | Swap auf SSD/HDD |
| Erfordert Disk-Swap | Nein | Ja | — |
| Fallback bei Volllauf | OOM (ohne Backing-Device) | Schreibt auf Disk-Swap | OOM bei Erschöpfung |
| Latenz | ~1.700 ns (lz4) | ~1.700 ns (komprimierter Treffer) / ~15 µs (Disk-Fallback) | ~15 µs (NVMe) / ~150 µs (SATA) |
| CPU-Overhead | Höher (alle Pages komprimiert) | Niedriger (Cache-Funktion) | Keiner |

!!! warning "zram und zswap nicht gleichzeitig betreiben"
    Bei Verwendung von zram `zswap.enabled=0` in den Kernel-Parametern setzen. Andernfalls fängt zswap Pages ab, bevor sie zram erreichen, was zu kontraproduktiver Doppelkompression führt.

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
| zram (kein Disk-Swap) | Keinerlei I/O-Konkurrenz — Swap bleibt vollständig im RAM. |

### Latenz-Vergleich

| Medium | Random-4K-Read-Latenz | Faktor vs. RAM |
|---|---|---|
| DDR5 RAM | ~15 ns | 1x |
| zram (lz4) | ~1.700 ns | ~110x |
| NVMe SSD | ~15 µs | ~1.000x |
| SATA SSD | ~150 µs | ~10.000x |
| HDD | ~12 ms | ~800.000x |

zram mit lz4 ist ~10x langsamer als direkter RAM-Zugriff, aber ~10x schneller als NVMe — ein sinnvoller Mittelweg, der Disk-I/O vollständig vermeidet.

### OOM-Killer

Wenn sowohl RAM als auch Swap erschöpft sind, aktiviert der Kernel den OOM-Killer. Er wählt den Prozess mit dem höchsten Badness-Score (primär basierend auf dem Speicherverbrauch) — fast immer X-Plane.

- X-Plane wird sofort per `SIGKILL` (Signal 9) beendet — kein sauberes Herunterfahren, kein Speichern
- Das Kernel-Log (`dmesg`) zeigt: `Out of memory: Kill process <PID> (X-Plane-x86_64)`

zram wirkt als Sicherheitsnetz: Durch Kompression ungenutzter Pages im RAM wird die effektive Speicherkapazität erweitert und OOM-Situationen werden verzögert oder verhindert.

---

## Empfohlene Konfiguration

### zram mit lz4

Für X-Plane-Systeme bietet zram mit lz4-Kompression den besten Kompromiss aus Latenz und Sicherheit:

```ini title="/etc/systemd/zram-generator.conf"
[zram0]
zram-size = min(ram / 2, 4096)
compression-algorithm = lz4
swap-priority = 100
```

```ini title="/etc/sysctl.d/99-zram.conf"
vm.swappiness = 180
vm.watermark_boost_factor = 0
vm.watermark_scale_factor = 125
vm.page-cluster = 0
```

In `/etc/default/grub` eintragen (zswap deaktivieren):

```
zswap.enabled=0
```

```bash
sudo update-grub
sudo systemctl daemon-reload
sudo systemctl start /dev/zram0
sudo sysctl --system
```

!!! note "Warum swappiness=180?"
    Mit zram ist der Swap-Zugriff fast so schnell wie RAM (Mikrosekunden statt Millisekunden). Ein hoher swappiness-Wert signalisiert dem Kernel, dass Swap günstig ist — er lagert proaktiv ungenutzte Pages in komprimierten Swap aus und gibt RAM für den Page Cache frei. Das verbessert Szenerie-Laden und Datei-I/O. Werte über 100 sind nur für In-Memory-Swap (zram) geeignet, nicht für Disk-Swap.

!!! note "Warum page-cluster=0?"
    Der Standard `page-cluster=3` liest 8 Pages (32 KiB) pro Swap-Zugriff als Readahead. Bei zram muss jede Page einzeln dekomprimiert werden — Readahead bringt keinen Vorteil und erhöht die Latenz. `page-cluster=0` liest nur die angeforderte Page.

### Kernel-Parameter-Übersicht

| Parameter | zram | Disk-Swap | Wirkung |
|---|---|---|---|
| `vm.swappiness` | 180 | 10–20 | Steuert das Verhältnis von Anonymous- zu File-Page-Reclaim |
| `vm.page-cluster` | 0 | 0 | Pages pro Swap-In (2^n). 0 = einzelne Page |
| `vm.watermark_scale_factor` | 125 | 10 (Standard) | Abstand zwischen Watermarks. Höher = früheres kswapd |
| `vm.watermark_boost_factor` | 0 | 0 | Boost für Disk-Swap deaktivieren |
| `vm.vfs_cache_pressure` | 50 | 50 | Inode-/Dentry-Caches für Szenerie-Datei-Lookups bevorzugen |

### RAM-Dimensionierung

| RAM | Einschätzung |
|---|---|
| 16 GB | Minimum. Swap-Aktivität wahrscheinlich bei Addons oder Ortho-Streaming. zram essenziell. |
| 32 GB | Komfortabel für die meisten Konfigurationen. zram als Sicherheitsnetz für Szenerie-Übergänge. |
| 64 GB | Swap sollte unter normalen Bedingungen inaktiv bleiben. Minimale zram-Konfiguration ausreichend. |

!!! tip "RAM ist die nachhaltige Lösung"
    Swap-Tuning — ob festplattenbasiert oder mit zram — ist Schadensbegrenzung. Der einzige Weg, Swap-bedingte Performance-Einbußen zuverlässig zu vermeiden, ist ausreichend physischer RAM. Für X-Plane mit Ortho-Streaming sind 32 GB die praktische Basis.

---

## Weiterführende Kapitel

| Thema | Seite | Schwerpunkt |
|---|---|---|
| Kernel-Tuning | [Kernel-Tuning](systemtuning.md) | CPU-Governor, sysctl-Profile, Interrupt-Affinität |
| Monitoring | [Monitoring](systemtools.md) | Swap-Aktivität verifizieren mit btop, vmstat, swapon |
| CPU & RAM | [CPU & RAM](../../fundamentals/performance/cpu_ram.md) | Wenn RAM zum Engpass wird |
| Dateisystem | [Dateisystem](../optimizations/filesystem.md) | SSD-Optimierung, I/O-Scheduler, Mount-Optionen |
| Latenz | [Latenz und Vorhersagbarkeit](../../fundamentals/performance/latency.md) | Latenzquellen und Messung |
| Fallstudie | [Fallstudie Tuning](tuning_casestudy.md) | Praktische Auswirkung von Swap- und Speicher-Tuning mit realen Messdaten |

---

## Quellen

- [Memory Management Concepts — Linux Kernel Documentation](https://docs.kernel.org/admin-guide/mm/concepts.html)
- [/proc/sys/vm/ — Linux Kernel Documentation](https://docs.kernel.org/admin-guide/sysctl/vm.html)
- [zram block device — Linux Kernel Documentation](https://docs.kernel.org/admin-guide/blockdev/zram.html)
- [zswap — Linux Kernel Documentation](https://docs.kernel.org/admin-guide/mm/zswap.html)
- [Swap — Arch Wiki](https://wiki.archlinux.org/title/Swap)
- [Zram — Arch Wiki](https://wiki.archlinux.org/title/Zram)
- [Swap — Debian Wiki](https://wiki.debian.org/Swap)
