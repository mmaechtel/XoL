# Research: Linux Swap & Memory Management für X-Plane

**Recherche-Datum:** 2026-02-21
**Quellen-Zeitraum:** 2025-2026 (Kernel-Docs als stabile Referenz)
**Status:** recherchiert

---

## 1. Swap-Mechanik im Linux-Kernel

### 1.1 Page Reclaim

Der Kernel verwaltet physischen Speicher in Pages (4 KiB). Bei Speicherknappheit greift **Page Reclaim** — der Kernel gibt Seiten frei:

- **File-backed Pages** (Page Cache): Clean Pages direkt verwerfbar, Dirty Pages werden zurückgeschrieben
- **Anonymous Pages** (Heap, Stack): Können **nur** in den Swap-Bereich ausgelagert werden

**Zwei Reclaim-Modi:**

| Modus | Auslöser | Verhalten |
|---|---|---|
| **kswapd** (asynchron) | Freier Speicher < Low Watermark | Hintergrund-Thread, blockiert keine Anwendungen |
| **Direct Reclaim** (synchron) | Freier Speicher < Min Watermark | Allokation blockiert, Prozess muss selbst Seiten freigeben → Latenzspitzen |

Quelle: [docs.kernel.org/admin-guide/mm/concepts.html](https://docs.kernel.org/admin-guide/mm/concepts.html)

### 1.2 Watermarks

| Watermark | Effekt |
|---|---|
| WMARK_HIGH | Genügend Speicher, kswapd schläft |
| WMARK_LOW | kswapd wird geweckt, Hintergrund-Reclaim |
| WMARK_MIN | Kritisch, Direct Reclaim, Allokationen blockiert |

Steuerung über:
- `vm.min_free_kbytes`: Legt WMARK_MIN fest
- `vm.watermark_scale_factor`: Abstand zwischen Watermarks (Default: 10 = 0,1% RAM)
- `vm.watermark_boost_factor`: Erhöhtes Reclaim bei Fragmentierung

Quelle: [docs.kernel.org/admin-guide/sysctl/vm.html](https://docs.kernel.org/admin-guide/sysctl/vm.html)

### 1.3 vm.swappiness — Details

Definiert das **relative I/O-Kosten-Verhältnis** zwischen Anonymous- und File-backed-Page-Reclaim.

**Interne Berechnung** (`mm/vmscan.c`):
```
anon_prio = swappiness
file_prio = 200 - swappiness
```

| Wert | Verhalten |
|---|---|
| 0 | Anonymous Pages werden **nicht** gescannt → nur File-Reclaim. Risiko: OOM trotz Swap |
| 60 (Default) | Moderate Präferenz für File-Reclaim (file_prio=140 vs. anon_prio=60) |
| 100 | Gleiche Gewichtung |
| 200 | Nur Anonymous Pages → maximales Swapping |

**Wichtig seit Kernel 3.5:** `swappiness=0` führt dazu, dass Anonymous Pages gar nicht mehr gescannt werden. Kann OOM-Kills auslösen, obwohl Swap verfügbar ist.

Quelle: [eklitzke.org/swappiness](https://eklitzke.org/swappiness), [docs.kernel.org/admin-guide/sysctl/vm.html](https://docs.kernel.org/admin-guide/sysctl/vm.html)

### 1.4 Multi-Gen LRU (MGLRU)

Seit Kernel 6.1, Default in vielen Distributionen. Statt zwei Listen (Active/Inactive) pro Typ verwendet MGLRU **mehrere Generationen**:

- Feingranulareres Aging
- Batch-Clearing von Accessed-Bits reduziert Lock-Contention
- Thrashing-Prevention via `min_ttl_ms`
- Reduzierter CPU-Verbrauch von kswapd

Konfiguration: `/sys/kernel/mm/lru_gen/enabled`

Quelle: [docs.kernel.org/admin-guide/mm/multigen_lru.html](https://docs.kernel.org/admin-guide/mm/multigen_lru.html)

### 1.5 Swap-In: Page Fault → Disk Read → RAM

1. **Page Fault:** MMU erkennt fehlendes Present-Bit, PTE enthält Swap Entry (Type + Offset)
2. **Swap Cache:** Prüfung ob Seite noch im Cache
3. **Disk Read:** Lesen vom Swap-Device, Readahead gemäß `vm.page-cluster` (Default: 8 Seiten = 32 KiB)
4. **RAM-Allokation + PTE-Update**

**Kernel 6.18 — Swap Table Modernisierung (2025):**
Neues Clustering mit C-Arrays statt XArray-Lookups → 5–20% Performance-Gewinn.

Quellen: [kernel.org/doc/html/latest/mm/swap-table.html](https://www.kernel.org/doc/html//latest/mm/swap-table.html), [lwn.net/Articles/1056405/](https://lwn.net/Articles/1056405/)

---

## 2. Swap-Konfiguration auf Debian 13 (Trixie)

### 2.1 Partition vs. Datei

| Eigenschaft | Swap-Partition | Swap-Datei |
|---|---|---|
| Performance | Minimal besser (kein FS-Overhead) | Praktisch identisch auf ext4/XFS |
| Flexibilität | Fix, Repartitionierung nötig | Größe leicht änderbar |
| Hibernate | Unkompliziert | Erfordert `resume_offset` |
| Btrfs | Nicht betroffen | Erfordert NOCOW, keine Kompression |

### 2.2 Einrichtung Swap-Partition

```bash
gdisk /dev/sdX          # Type-Code: 8200
mkswap /dev/sdXn
swapon /dev/sdXn
# fstab: UUID=<uuid> none swap sw 0 0
```

### 2.3 Einrichtung Swap-Datei

```bash
dd if=/dev/zero of=/swapfile bs=1M count=8192    # 8 GiB
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
# fstab: /swapfile none swap sw 0 0
```

**NICHT verwenden:** `fallocate` (erzeugt sparse Files, swapon lehnt ab).

### 2.4 Debian-Installer Default

Guided Partitioning erstellt Swap-Partition, Größe variabel (1,2 GiB bis RAM-Größe).
Faustregel: Swap = RAM, mindestens 512 MB.

Quelle: [debian.org/releases/trixie/amd64/apcs03.en.html](https://www.debian.org/releases/trixie/amd64/apcs03.en.html)

### 2.5 Empfohlene Größen

| RAM | Ohne Hibernate | Mit Hibernate |
|---|---|---|
| ≤ 2 GiB | 2x RAM | 3x RAM |
| 2–8 GiB | = RAM | 2x RAM |
| 8–64 GiB | 4–8 GiB | ≥ RAM |
| > 64 GiB | 4–8 GiB | ≥ RAM |

### 2.6 Swap-Prioritäten

- Unterschiedliche Prioritäten: Höchste zuerst, Fallback auf niedrigere
- Gleiche Prioritäten: Round-Robin (Striping über mehrere Devices)

```
UUID=<uuid1> none swap sw,pri=100 0 0    # Primär
UUID=<uuid2> none swap sw,pri=10  0 0    # Fallback
```

---

## 3. RAM-Kompression: zram vs. zswap

### 3.1 zram

Komprimiertes Block-Device im RAM als Swap-Device. Kein Disk-I/O.

**Algorithmen-Vergleich (Benchmark-Daten):**

| Algorithmus | IOPS (page-cluster=0) | Latenz (ns) | Kompression |
|---|---|---|---|
| lz4 | 2.033.515 | 1.708 | 2,6:1 |
| zstd | 668.715 | 5.714 | 3,4:1 |

**Konfiguration auf Debian 13:**

```bash
sudo apt install systemd-zram-generator
```

```ini
# /etc/systemd/zram-generator.conf
[zram0]
zram-size = min(ram / 2, 4096)
compression-algorithm = lz4
swap-priority = 100
```

**Optimale Kernel-Parameter für zram:**

```ini
vm.swappiness = 180          # Hoher Wert für In-Memory-Swap
vm.watermark_boost_factor = 0
vm.watermark_scale_factor = 125
vm.page-cluster = 0          # Nur 1 Seite pro Zugriff
```

Quellen: [docs.kernel.org/admin-guide/blockdev/zram.html](https://docs.kernel.org/admin-guide/blockdev/zram.html), [wiki.archlinux.org/title/Zram](https://wiki.archlinux.org/title/Zram), [notes.xeome.dev/notes/Zram](https://notes.xeome.dev/notes/Zram)

### 3.2 zswap

Komprimierter Write-Back-Cache **vor** dem Disk-Swap-Device. Benötigt immer ein physisches Swap-Device als Backend.

**Konfiguration:**

```
GRUB_CMDLINE_LINUX_DEFAULT="... zswap.enabled=1 zswap.compressor=zstd zswap.max_pool_percent=20"
```

| Parameter | Default | Beschreibung |
|---|---|---|
| max_pool_percent | 20 | Max. Anteil des RAM für Pool |
| accept_threshold_percent | 90 | Keine neuen Seiten über diesem Füllstand |
| shrinker_enabled | Y | Proaktives Eviction |

**Writeback:** Pool voll → LRU-Eviction auf Disk-Swap. Inkompressible Seiten → direkt auf Disk.

Quelle: [docs.kernel.org/admin-guide/mm/zswap.html](https://docs.kernel.org/admin-guide/mm/zswap.html)

### 3.3 Vergleich zram vs. zswap

| Merkmal | zram | zswap |
|---|---|---|
| Typ | Eigenständiges Swap-Device im RAM | Cache vor Disk-Swap |
| Benötigt Disk-Swap | Nein | Ja |
| Fallback bei Pool-Überlauf | OOM (ohne Backing-Device) | Schreibt auf Disk-Swap |
| Hibernation | Nicht möglich | Möglich |
| CPU-Overhead | Höher (alles im RAM komprimiert) | Niedriger (Cache-Funktion) |
| Gleichzeitiger Betrieb | Konflikt mit zswap! | Braucht Disk-Swap |

**WICHTIG:** zram und zswap dürfen nicht gleichzeitig aktiv sein. Bei zram-Nutzung: `zswap.enabled=0` als Kernel-Parameter.

### 3.4 Distributions-Defaults

| Distribution | Default |
|---|---|
| Debian 13 (Trixie) | Swap-Partition (klassisch), zswap/zram deaktiviert |
| Ubuntu 24.04 | Swap-Datei (klassisch) |
| Fedora 41/42 | **zram** (seit Fedora 33) |
| Pop!_OS | **zram** (lz4) |
| Arch Linux | Manuell, Wiki empfiehlt zram |

### 3.5 Empfehlungen nach RAM-Größe

| RAM | Empfehlung |
|---|---|
| 16 GB | zram (8 GB, lz4) + optionaler Disk-Swap als Fallback |
| 32 GB | zram (4–8 GB), Disk-Swap nur für Hibernate |
| 64 GB | zram (4 GB) oder kein Swap |

---

## 4. X-Plane 12 — Speicherverhalten und Swap-Impact

### 4.1 RAM-Verbrauch

| Konfiguration | Typischer Verbrauch |
|---|---|
| Basis (Standard-Szenerie) | 10–14 GB |
| Mit Addon-Flugzeugen + Custom Scenery | 16–24 GB |
| Mit Ortho-Streaming (AutoOrtho) | 20–30+ GB |

AutoOrtho allein kann bis zu 16 GB RAM beanspruchen. Community-Empfehlung: 32 GB DDR5 für 1440p, 64 GB DDR5 für 4K/VR.

Quellen: [x-plane.com/kb/x-plane-12-system-requirements/](https://www.x-plane.com/kb/x-plane-12-system-requirements/), [forums.x-plane.org: 16 to 32 GB RAM](https://forums.x-plane.org/forums/topic/326882-16-to-32-gb-ram/)

### 4.2 DSF-Szenerie-Laden

- Hintergrund-Loading auf Worker-Threads (seit X-Plane 9)
- 1–2 DSFs gleichzeitig im Flug, bis zu 4 beim Start
- DSF-Dateien komprimiert (7z) → CPU-Last beim Dekomprimieren + Disk-I/O

Quelle: [developer.x-plane.com/article/dsf-usage-in-x-plane/](https://developer.x-plane.com/article/dsf-usage-in-x-plane/)

### 4.3 VRAM-Management

X-Plane nutzt System-RAM **nicht** als Backup-VRAM. Stattdessen proaktive Textur-Herunterskalierung bei VRAM-Knappheit (unscharfe Texturen statt Stutter). System-RAM dient als Textur-Cache.

Quelle: [developer.x-plane.com: All Your VRAM Is Belonging To Us](https://developer.x-plane.com/2020/01/all-your-vram-is-belonging-to-us-and-plugins/)

### 4.4 Was passiert wenn X-Plane-Speicher geswapt wird

**Symptome:**
- Stutter und Frame-Drops bei jedem Swap-In (Page Fault → Disk-Latenz im Rendering-Thread)
- System-Freezes bei starkem Swapping (1–2 GB Transfer → Minuten auf HDD)
- OOM-Meldungen: "X-Plane is running very low on memory. Scenery loading is now disabled."

**Dreifache I/O-Last mit Ortho-Streaming:**
1. AutoOrtho/XEarthLayer Cache-Schreibvorgänge
2. Swap-I/O
3. DSF-Szenerie-Laden durch X-Plane

### 4.5 Swap auf derselben SSD vs. dedizierter SSD

**Selbe SSD:**
- Swap-I/O konkurriert mit X-Plane-Datenzugriffen (Texturen, DSF, Ortho-Cache)
- NVMe: In der Praxis bei gelegentlichem Swap unproblematisch (genug IOPS)
- SATA: Spürbar, da Queue-Tiefe gering (NCQ: max. 32 Commands)
- Hauptrisiko: **Tail-Latency** — einzelne Swap-Reads unter Last

**Dedizierte SSD:**
- Eliminiert I/O-Contention vollständig
- Für Desktop/Gaming selten nötig
- Sinnvoll bei Systemen mit 16 GB RAM und Ortho-Streaming

### 4.6 Latenz-Vergleich

| Medium | Random 4K Read Latenz | Faktor vs. RAM |
|---|---|---|
| DDR5 RAM | ~15 ns | 1x |
| zram (lz4) | ~1.700 ns | ~110x |
| NVMe SSD | ~15 µs | ~1.000x |
| SATA SSD | ~150 µs | ~10.000x |
| HDD | ~12 ms | ~800.000x |

### 4.7 OOM-Killer

- Linux über-allokiert Speicher (Default: Modus 0, heuristisch)
- OOM-Killer wählt Prozess mit höchstem `oom_score` → fast immer X-Plane
- X-Plane wird sofort per SIGKILL beendet — kein sauberes Shutdown
- In `dmesg`: `Out of memory: Kill process <PID> (X-Plane) score <num>`

---

## 5. Best Practices für X-Plane-Systeme

### 5.1 Kernel-Parameter

| Parameter | Disk-Swap | zram | Begründung |
|---|---|---|---|
| vm.swappiness | 10 | 180 | Minimiert Disk-I/O bzw. nutzt schnellen RAM-Swap |
| vm.vfs_cache_pressure | 50 | 50 | Bevorzugt Inode/Dentry-Cache für Szenerie-Dateien |
| vm.page-cluster | 0 | 0 | Kein Readahead bei Random-Access |
| vm.min_free_kbytes | ~1% RAM | ~1% RAM | Sicherheitspuffer gegen OOM |
| vm.compaction_proactiveness | 0 | 0 | Verhindert Latenzspitzen |

### 5.2 Empfehlung: zram mit lz4

Für X-Plane-Systeme (typisch 32 GB RAM):

```ini
# /etc/systemd/zram-generator.conf
[zram0]
zram-size = min(ram / 2, 4096)
compression-algorithm = lz4
swap-priority = 100
```

```ini
# /etc/sysctl.d/99-vm-zram-parameters.conf
vm.swappiness = 180
vm.watermark_boost_factor = 0
vm.watermark_scale_factor = 125
vm.page-cluster = 0
```

Kernel-Parameter: `zswap.enabled=0`

**Begründung:**
- lz4 liefert niedrigste Latenz (1.700 ns) bei ausreichender Kompression (2,6:1)
- Bei 32 GB RAM wird Swap selten aktiv — wenn doch, ist CPU-Overhead von lz4 vernachlässigbar
- Schützt vor OOM bei Szenerienwechseln oder parallelen Anwendungen
- Kein Disk-I/O → keine Konkurrenz mit X-Plane-Storage

### 5.3 RAM ist die einzige nachhaltige Lösung

| RAM | Einschätzung |
|---|---|
| 16 GB | Minimum. Mit Addons/AutoOrtho wird Swap nahezu unvermeidlich |
| 32 GB | Komfortabel. AutoOrtho + komplexe Addons können den Puffer aufbrauchen |
| 64 GB | Sicherheitsmarge für VR, 4K, Ortho-Streaming. Swap praktisch inaktiv |

---

## Quellenverzeichnis

### Kernel-Dokumentation
- [docs.kernel.org/admin-guide/mm/concepts.html](https://docs.kernel.org/admin-guide/mm/concepts.html)
- [docs.kernel.org/admin-guide/sysctl/vm.html](https://docs.kernel.org/admin-guide/sysctl/vm.html)
- [docs.kernel.org/admin-guide/mm/multigen_lru.html](https://docs.kernel.org/admin-guide/mm/multigen_lru.html)
- [docs.kernel.org/admin-guide/blockdev/zram.html](https://docs.kernel.org/admin-guide/blockdev/zram.html)
- [docs.kernel.org/admin-guide/mm/zswap.html](https://docs.kernel.org/admin-guide/mm/zswap.html)
- [kernel.org/doc/html/latest/mm/swap-table.html](https://www.kernel.org/doc/html//latest/mm/swap-table.html)

### LWN.net
- [lwn.net/Articles/1056405/](https://lwn.net/Articles/1056405/) — Modernizing Linux swapping
- [lwn.net/Articles/716296/](https://lwn.net/Articles/716296/) — VMA based swap readahead

### ArchWiki
- [wiki.archlinux.org/title/Swap](https://wiki.archlinux.org/title/Swap)
- [wiki.archlinux.org/title/Zram](https://wiki.archlinux.org/title/Zram)
- [wiki.archlinux.org/title/Zswap](https://wiki.archlinux.org/title/Zswap)

### Debian
- [wiki.debian.org/Swap](https://wiki.debian.org/Swap)
- [wiki.debian.org/ZRam](https://wiki.debian.org/ZRam)
- [wiki.debian.org/Zswap](https://wiki.debian.org/Zswap)
- [debian.org/releases/trixie/amd64/apcs03.en.html](https://www.debian.org/releases/trixie/amd64/apcs03.en.html)

### X-Plane
- [x-plane.com/kb/x-plane-12-system-requirements/](https://www.x-plane.com/kb/x-plane-12-system-requirements/)
- [developer.x-plane.com/article/dsf-usage-in-x-plane/](https://developer.x-plane.com/article/dsf-usage-in-x-plane/)
- [developer.x-plane.com: All Your VRAM Is Belonging To Us](https://developer.x-plane.com/2020/01/all-your-vram-is-belonging-to-us-and-plugins/)
- [x-plane.com/kb/configuring-x-plane-to-use-less-virtual-memory/](https://www.x-plane.com/kb/configuring-x-plane-to-use-less-virtual-memory/)

### Benchmarks / Vergleiche
- [notes.xeome.dev/notes/Zram](https://notes.xeome.dev/notes/Zram) — zram Performance Analysis
- [github.com/ublue-os/bazzite/issues/1570](https://github.com/ublue-os/bazzite/issues/1570) — lz4 vs zstd Gaming
- [github.com/CryoByte33/steam-deck-utilities](https://github.com/CryoByte33/steam-deck-utilities/blob/main/docs/tweak-explanation.md) — Gaming-Tuning
- [eklitzke.org/swappiness](https://eklitzke.org/swappiness) — Swappiness-Analyse
