# Lektorat: Linux Swap & Memory Management

**Datum:** 2026-02-21
**Research-Paper:** `research/systemtuning/swap_memory_management.md`
**Zielseite:** `docs/{lang}/linux/system/swap.md`
**Status:** geplant

---

## 1. Einordnung im Blog

### Wo gehört die Seite hin?

Die Seite gehört unter **Linux → System** zwischen `systemtuning.md` und `systemtools.md`. Begründung:

- `systemtuning.md` enthält bereits `vm.swappiness`, `vm.dirty_ratio`, `vm.vfs_cache_pressure` als nackte Konfigurationswerte **ohne Erklärung** → die Swap-Seite füllt diese Lücke
- Natürlicher Lesefluss: Latency (Motivation) → Kernel-Tuning (Konfiguration) → **Swap & Memory (Vertiefung)** → Monitoring (Verifikation)
- Swap ist Kernel-Level-Konfiguration (sysctl, zram) — gleiche Schicht wie CPU-Governor und IRQ-Affinity
- Nicht bei "Optimizations" (dort Treiber/Dateisysteme), nicht bei "Fundamentals" (dort Theorie)

**Querverweise:**

| Seite | Änderung |
|---|---|
| `systemtuning.md` | Bei vm.*-Blöcken Verweis auf swap.md für Hintergrund |
| `cpu_ram.md` | Im Abschnitt "When RAM Becomes the Bottleneck" Verweis auf swap.md |
| `filesystem.md` | SSD-I/O-Bezug → Verweis auf Swap-auf-SSD |
| `latency.md` | Bei "Memory/IO" optionaler Verweis |
| `begin.md` | Beim Swap-Partitionierungs-Punkt Verweis auf swap.md für Details |

### Relevanz-Bewertung

| Kriterium | Bewertung |
|---|---|
| Linux-spezifisch | Ja — zram, zswap, Kernel-Parameter sind Linux-exklusiv |
| X-Plane-relevant | Hoch — Speicherverbrauch 10–30+ GB, Swap-Impact auf FPS |
| Haltbarkeit | Gut — Kernel-Mechanik stabil, zram/zswap seit Jahren im Mainline |
| Zielgruppe | Erfahrene Linux-User (Blog-Zielgruppe) |
| Mehrwert | Hoch — konsolidiert verstreutes Wissen, X-Plane-spezifische Empfehlung fehlt überall |

---

## 2. Artikelstruktur

### Gliederung EN

```
# Swap & Memory Management

[Intro: 2-3 Sätze — warum Swap für X-Plane relevant ist]

## How Swap Works
  - Page Reclaim (kswapd vs. Direct Reclaim) — Fließtext mit Tabelle
  - Watermarks — Tabelle
  - vm.swappiness — was der Parameter wirklich steuert
    ??? abstract "Kernel-interne Berechnung"
        [Formel + Wertetabelle]

## Swap Configuration
  - Partition vs. File — Vergleichstabelle
  - Setup on Debian — Code-Blöcke (Partition + Datei)
  - Sizing — Tabelle (RAM-abhängig, nur aktiver Betrieb)

## RAM Compression: zram vs. zswap
  - zram — Funktionsweise, Algorithmen-Vergleich (Tabelle mit Benchmarks)
  - zswap — Funktionsweise, Unterschied zu zram
  - Comparison Table (zram vs. zswap vs. Disk-Swap)
  - Setup on Debian — Code-Blöcke
  !!! warning "zram + zswap Conflict"
      [Nicht gleichzeitig aktivieren]

## Impact on X-Plane
  - RAM consumption table (Base / Addons / Ortho-Streaming)
  - What happens when X-Plane pages get swapped — Symptome
  - I/O contention: same SSD vs. dedicated SSD — Tabelle + Fließtext
  - Latency comparison table (RAM → zram → NVMe → SATA → HDD)
  !!! warning "OOM-Killer"
      [X-Plane wird per SIGKILL beendet, kein sauberes Shutdown]

## Recommended Configuration
  - Empfehlung: zram mit lz4 — Code-Block (zram-generator.conf + sysctl)
  - Kernel parameters table (swappiness, vfs_cache_pressure, page-cluster, ...)
  - RAM sizing guide (16/32/64 GB)
  !!! tip "RAM ist die nachhaltige Lösung"
      [Swap-Tuning = Schadensbegrenzung]

---

## Further Reading
  [Tabelle mit Querverweisen]

---

## Sources
  [5-8 Quellen]
```

### Gliederung DE (identische Struktur)

```
# Swap & Speicherverwaltung

## Wie Swap funktioniert
## Swap-Konfiguration
## RAM-Kompression: zram vs. zswap
## Auswirkungen auf X-Plane
## Empfohlene Konfiguration

## Weiterführende Kapitel
## Quellen
```

---

## 3. Redaktionelle Bewertung

### Was übernommen wird

| Information | Quelle | Haltbarkeit |
|---|---|---|
| Page Reclaim Mechanik (kswapd, Direct Reclaim, Watermarks) | Kernel-Docs | Stabil |
| vm.swappiness Berechnung | Kernel-Source + eklitzke.org | Stabil seit Kernel 3.5 |
| zram Algorithmen-Benchmarks (lz4 vs. zstd) | xeome.dev, Bazzite #1570 | Stabil (Hardware-unabhängig) |
| zram/zswap Konfiguration Debian | wiki.debian.org | Stabil für Trixie-Zyklus |
| X-Plane RAM-Verbrauch | forums.x-plane.org, Laminar-Docs | Aktuell (XP 12.2) |
| Latenz-Vergleichswerte | Kernel-Docs, simplyblock.io | Stabil (Größenordnungen) |
| OOM-Killer Verhalten | Kernel-Docs | Stabil |

### Was NICHT übernommen wird

| Information | Grund |
|---|---|
| Kernel 6.18 Swap Table Modernisierung | Zu versionsspezifisch, noch nicht in Debian Stable |
| MGLRU Details | Zu tief für Zielgruppe, gehört eher in systemtuning.md |
| CryoUtilities Steam-Deck-Parameter | Steam-Deck-spezifisch, nicht direkt übertragbar |
| vm.page_lock_unfairness, transparent_hugepages | Gehören in systemtuning.md, nicht auf die Swap-Seite |
| Memory-Leak-Berichte aus Foren | Unbelegt, anekdotisch |
| cgroups/Memory Limits | Für X-Plane kontraproduktiv → nicht empfehlen |

### Versionsnummern

Gemäß Entscheidungsbaum in AUDIT_FLOW.md:
- Kernel-Versionen (6.1 für MGLRU, 3.5 für swappiness-Änderung): Nur in akademischen Blöcken (`??? abstract`)
- Debian 13 (Trixie): Als Referenzplattform nennen, keine Versionsnummer im Fließtext
- X-Plane 12: Im Kontext von RAM-Verbrauch nennen (ist die dokumentierte Version)

---

## 4. Textfluss-Plan

| Abschnitt | Elemente |
|---|---|
| How Swap Works | Fließtext → Tabelle (Watermarks) → Fließtext (swappiness) → Collapsible (Kernel-Formel) |
| Swap Configuration | Tabelle (Partition vs. File) → Code-Block → Tabelle (Sizing) |
| RAM Compression | Fließtext → Benchmark-Tabelle → Vergleichstabelle → Code-Block → Warning-Box |
| Impact on X-Plane | Tabelle (RAM) → Fließtext (Symptome) → Tabelle (Latenz) → Warning-Box (OOM) |
| Recommended Config | Code-Block → Tabelle (Parameter) → Tabelle (RAM-Sizing) → Tip-Box |

**Strukturelemente:** Fließtext, 7+ Tabellen, 2+ Code-Blöcke, 2 Warning-Boxen, 1 Tip-Box, 1 Collapsible — guter Textfluss-Wechsel.

---

## 5. Offene Fragen

1. **Überschneidung mit systemtuning.md:** Die bestehende Seite erwähnt `vm.swappiness` und `vm.vfs_cache_pressure` bereits kurz. Soll die neue Swap-Seite die kanonische Quelle werden, mit Verweis von systemtuning.md dorthin? Oder bleibt systemtuning.md die Übersicht mit Kurzfassung?

2. **Seitenname:** `swap.md` oder `swap_memory.md`? `swap.md` ist kürzer und eindeutig.

**Entschieden:** Kein Hibernate-Abschnitt — tangiert X-Plane nicht.

---

## 6. Nächste Schritte

Nach User-Freigabe:
1. EN-Seite schreiben (Struktur wie oben)
2. DE-Seite angleichen
3. mkdocs.yml Navigation updaten (Linux → System → Swap & Memory Management)
4. Querverweise in systemtuning.md, filesystem.md, cpu_ram.md ergänzen
5. Glossar-Einträge prüfen/ergänzen (zram, zswap, OOM-Killer, Page Reclaim?)
6. mkdocs build
