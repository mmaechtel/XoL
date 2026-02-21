# Lektorat: How Ortho Streaming Works

**Datum:** 2026-02-21
**Grundlage:** `research/szenerie/ortho_streaming_architecture.md`
**Zielseite:** `docs/{lang}/scenery/ortho_streaming/how_streaming_works.md`
**Vorlagen:** `autoortho.md`, `xearthlayer.md`, `scenery_components.md`

---

## 1. Motivation

Die bestehenden Seiten AutoOrtho und XEarthLayer erklären jeweils individuell, wie Ortho-Streaming funktioniert — mit Überschneidungen bei FUSE, Cache, DDS-Format und dem allgemeinen Pipeline-Konzept. Es fehlt eine **vorgelagerte Erklärungsseite**, die die gemeinsame technische Grundlage darstellt:

- Wie lädt X-Plane Texturen? (DSF → .ter → DDS)
- Was ist FUSE und wie fängt es Dateizugriffe ab?
- Wie sieht die Streaming-Pipeline aus (Request → Download → Konversion → Cache → Lieferung)?
- Warum ist Linux dabei im Vorteil?

Die Tool-spezifischen Seiten können dann auf die Grundlagen verweisen und sich auf ihre jeweiligen Besonderheiten konzentrieren.

---

## 2. Seitenstruktur (Plan)

```
# How Ortho Streaming Works

Einleitungssatz: Was ist Ortho-Streaming, warum existiert es (vs. statische Tiles)

## X-Plane's Texture Loading Chain / X-Planes Textur-Ladekette
- DSF → .ter → DDS dreistufige Referenzkette
- LOAD_CENTER für entfernungsabhängiges Laden
- DDS-Format: BC1/BC3-Kompression, Mipmaps
- .ter Base-Mesh-Ersetzung (nicht .pol Overlay)
→ Diagramm oder Code-Beispiel der Kette wäre ideal

## FUSE: The Virtual Filesystem / FUSE: Das virtuelle Dateisystem
- Was ist FUSE (Kernel-Modul + Userspace-Daemon + /dev/fuse)
- Request-Lebenszyklus (X-Plane → Kernel → FUSE-Daemon → Kernel → X-Plane)
- Wie Streaming-Tools FUSE nutzen (Mount in Custom Scenery, Regex-Matching, Request-Routing)
- Performance: 4 Context-Switches, aber irrelevant weil netzwerk-bound
??? abstract "Technical Background: FUSE Request Lifecycle"
  → Detaillierter Queue-basierter Ablauf (fc->pending, fc->processing, req->waitq)

## The Streaming Pipeline / Die Streaming-Pipeline
- Vollständiger Request-Flow als Diagramm/Listing
- Sparse DDS Allocation (Mipmap-Exploitation) — AutoOrthos Schlüssel-Innovation
- Cache-Architektur: L1 Memory → L2 Disk → L3 Network
→ Tabelle der Cache-Ebenen

## Value on Linux / Mehrwert unter Linux
- FUSE nativ im Kernel seit 2005
- Vergleichstabelle Linux FUSE vs Windows WinFSP/Dokan
- XEarthLayer als Linux-Only-Konsequenz

## When Loading Takes Longer / Wenn das Laden länger dauert
- Praxisnaher Abschnitt: Warum Ortho-Streaming manchmal langsam ist
- Tabelle oder Liste mit Ursache → Erklärung → Abhilfe
- 7 belegte Gründe:
  1. Cache leer (Erstbesuch in Region)
  2. Netzwerk/Server langsam oder überlastet
  3. Einstellungen geändert (Zoom-Level, Anbieter) → Cache ungültig
  4. Rate Limiting (HTTP 429) durch Kartenanbieter
  5. Hoher Zoom-Level → exponentiell mehr Tiles
  6. CPU-Konkurrenz zwischen DDS-Kompression und X-Plane
  7. Schneller Tiefflug → mehr Tiles/Sekunde als im Reiseflug
- Quellen: autoortho.md (HTTP 429), xearthlayer.md (CPU Tuning, Prefetch-Modi)

## Further Reading / Weiterführende Kapitel
- AutoOrtho → Tool-spezifische Konfiguration
- XEarthLayer → Rust-basierte Alternative mit adaptivem Prefetch
- Static + Streaming → Kombination beider Ansätze
- Scenery Components → scenery_packs.ini Ladereihenfolge

## Sources / Quellen
- X-Plane Developer Docs (DSF, .ter, Orthophotos)
- Linux Kernel FUSE Documentation
- AutoOrtho/XEarthLayer Projekt-Dokumentation
```

---

## 3. Kürzungen in bestehenden Seiten

### autoortho.md — Zu kürzen

| Abschnitt | Zeilen | Aktion |
|---|---|---|
| "How It Works" Absatz 1 (Streaming-System allgemein) | 12-14 | Kürzen: Nur AutoOrtho-Spezifika behalten, für Grundlagen auf neue Seite verweisen |
| "How It Works" Absatz 2 (FUSE/VFS allgemein) | 16 | Kürzen: FUSE-Erklärung entfernen, Link auf neue Seite |
| "How It Works" Absatz 3 (Overlays, SimHeaven) | 18 | Behalten: AutoOrtho-spezifisch (yOrtho Overlays) |
| "How It Works" Absatz 4 (Performance-Impact) | 20 | Behalten: AutoOrtho-spezifisch |
| System Requirements (FUSE-Erwähnung) | 42 | Kürzen: FUSE-Erklärung durch Link ersetzen |

**Vorgeschlagener neuer "How It Works"-Absatz:**

> AutoOrtho implements a [FUSE-based streaming system](how_streaming_works.md) for [orthophotos](../../glossary.md#orthophotos) based on the aircraft's position. Tiles for current and adjacent areas are preloaded from providers like Bing, using zoom levels up to ZL18. For the general streaming architecture (DSF → .ter → DDS chain, FUSE interception, cache system), see [How Ortho Streaming Works](how_streaming_works.md).

### xearthlayer.md — Minimal ändern

Die "How It Works"-Einleitung (Zeile 13) ist bereits kompakt und enthält kaum Redundanz. Änderung: Nur einen **Link auf die neue Seite** einfügen, keinen inhaltlichen Cut.

**Vorgeschlagener angepasster Einleitungssatz:**

> XEarthLayer uses a **[FUSE](../../glossary.md#fuse-filesystem-in-userspace)-based virtual file system** (see [How Ortho Streaming Works](how_streaming_works.md)) to provide orthophoto textures on demand. When X-Plane accesses a tile, the satellite image is downloaded from the configured map provider, converted to [DDS](../../glossary.md#dds-directdraw-surface) format (BC1/BC3 compression), and delivered to the simulator via the VFS.

**Hinweis:** Der "Two-Tier Cache"-Abschnitt bleibt in xearthlayer.md — er beschreibt XEL-spezifisches Caching-Verhalten (Memory + Disk mit eigenen Eviction-Regeln), das über die allgemeine Cache-Architektur der neuen Seite hinausgeht.

### orthophotography_intro.md — Minimal ändern

FUSE-Erwähnung (Zeile 30) um Link auf neue Seite ergänzen:

> "... via a virtual file system ([FUSE](../ortho_streaming/how_streaming_works.md))."

### scenery_components.md — Keine Änderung

Die Seite behandelt die Schichten-Architektur (Mesh/Ortho/Autogen) auf hoher Ebene. Die neue Seite geht tiefer auf die technische Kette ein, ohne die scenery_components-Seite zu ersetzen.

### ortho_streaming/index.md — Minimal ändern

Index bleibt clean: Nur eine kurze Übersicht was die Section enthält + Links. Neuen Link auf `how_streaming_works.md` als ersten Eintrag einfügen, sonst keine inhaltliche Erweiterung.

---

## 4. Informationsbewertung

| Information | Relevanz | Haltbarkeit | Aufnehmen? |
|---|---|---|---|
| DSF → .ter → DDS Kette | Hoch | Stabil (Core-API) | Ja |
| LOAD_CENTER Mechanismus | Hoch | Stabil (seit XP10) | Ja |
| BC1/BC3 DDS-Kompression | Hoch | Stabil (GPU-Standard) | Ja |
| Sparse DDS / Mipmap-Exploitation | Hoch | Stabil (AutoOrtho-Architektur) | Ja |
| FUSE Kernel-Architektur | Hoch | Stabil (Kernel seit 2005) | Ja |
| FUSE Request-Lifecycle (Queue-Details) | Mittel | Stabil | Ja, als klappbarer Block |
| Context-Switch-Overhead (4 vs 2) | Mittel | Stabil | Ja, kurz |
| FUSE vs WinFSP Vergleich | Hoch | Stabil | Ja, Tabelle |
| RFUSE/io_uring (2024) | Niedrig | Instabil (Forschung) | Nein — zu akademisch |
| FUSE3 vs FUSE2 Details | Niedrig | Instabil | Nein — zu technisch, wenig Mehrwert |
| Regex-Pattern für Dateinamen | Niedrig | Implementierungsdetail | Nein |
| XEarthLayer Linux-Only Begründung | Hoch | Stabil | Ja |

---

## 5. Versionsspezifische Inhalte

| Inhalt | Entscheidung | Begründung |
|---|---|---|
| „FUSE seit Kernel 2.6.14 (2005)" | Behalten | Stabile historische Tatsache, illustriert Reife |
| „seit XP10 LOAD_CENTER" | Meta-Formulierung | „X-Plane supports proximity-based texture loading" |
| „AutoOrtho Fork 2.0 C-Pipeline" | Verweis auf AutoOrtho-Seite | Tool-spezifisch |

---

## 6. Navigation und Querverweise

### mkdocs.yml

```yaml
# DE
- Ortho Streaming:
    - de/scenery/ortho_streaming/index.md
    - Funktionsweise: de/scenery/ortho_streaming/how_streaming_works.md    # NEU
    - AutoOrtho: de/scenery/ortho_streaming/autoortho.md
    - XEarthLayer: de/scenery/ortho_streaming/xearthlayer.md
    - Statisch + Streaming: de/scenery/ortho_streaming/static_plus_streaming.md

# EN
- Ortho Streaming:
    - en/scenery/ortho_streaming/index.md
    - How It Works: en/scenery/ortho_streaming/how_streaming_works.md    # NEU
    - AutoOrtho: en/scenery/ortho_streaming/autoortho.md
    - XEarthLayer: en/scenery/ortho_streaming/xearthlayer.md
    - Static + Streaming: en/scenery/ortho_streaming/static_plus_streaming.md
```

### Index-Seite (ortho_streaming/index.md)

Neuen Eintrag **vor** AutoOrtho und XEarthLayer einfügen:

```
- **[How Ortho Streaming Works](how_streaming_works.md)** — X-Plane's texture loading chain, FUSE virtual filesystem, and the streaming pipeline
```

### Querverweise von neuer Seite

| Ziel | Seite |
|---|---|
| AutoOrtho | `autoortho.md` |
| XEarthLayer | `xearthlayer.md` |
| Static + Streaming | `static_plus_streaming.md` |
| Scenery Components | `../aufbau_quellen/scenery_components.md` |
| Filesystem | `../../linux/optimizations/filesystem.md` |
| Glossar: FUSE | `../../glossary.md#fuse-filesystem-in-userspace` |
| Glossar: DDS | `../../glossary.md#dds-directdraw-surface` |
| Glossar: DSF | `../../glossary.md#dsf-distribution-scenery-format` |
| Glossar: Orthophotos | `../../glossary.md#orthophotos` |

---

## 7. Zusammenfassung der Änderungen

| Datei | Aktion | Umfang |
|---|---|---|
| `how_streaming_works.md` (EN) | **NEU** | ~120 Zeilen |
| `how_streaming_works.md` (DE) | **NEU** | ~120 Zeilen |
| `autoortho.md` (EN + DE) | Kürzen | "How It Works" auf ~3 Zeilen + Link |
| `xearthlayer.md` (EN + DE) | Kürzen | "How It Works" Zeile 13 kürzen + Link |
| `index.md` (ortho_streaming, EN + DE) | Erweitern | 1 Eintrag hinzufügen |
| `orthophotography_intro.md` (EN + DE) | Minimal | FUSE-Link ergänzen |
| `mkdocs.yml` | Erweitern | 2 Nav-Einträge |

**Keine Änderungen an:** `scenery_components.md`, `static_plus_streaming.md`, `glossary.md`
