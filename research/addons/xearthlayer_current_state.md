# XEarthLayer -- Aktueller Stand (Recherche)

Recherche-Datum: 2026-04-27 (aktualisiert, Erstrecherche 2026-02-14)

## 1. Version und Release-Historie

### Aktuelle Version

**v0.4.4** -- veröffentlicht am 17. April 2026

### Vollständige Release-Chronologie

| Version | Datum | Highlights |
|---------|-------|------------|
| v0.4.4 | 2026-04-17 | Long-Haul-Prefetch-Fix (Dead-State auf Flügen >2 h, mit 9-h-LOWW-Log verifiziert), `max_concurrent_jobs`-Default auf `num_cpus/2` halbiert, Drei-Tier-Cache-Metriken im TUI getrennt (Memory/DDS-Disk/Chunks), Ground- und Cruise-Prefetch in einer `PrefetchBox` vereinheitlicht |
| v0.4.3 | 2026-04-07 | Config-Audit (15 Keys entfernt, CPU-Concurrency auf 50%), Prefetch-InProgress-Deadstate-Fix (3-Layer-Protection), TUI-Metriken-Fixes |
| v0.4.2 | 2026-04-06 | DDS-Disk-Cache-Tier (3-Tier-Hierarchie), Speed-proportionale Prefetch-Box, Stale-Telemetry-Safe-Mode, GPU-Encoding built-in (kein Feature-Flag mehr), fuse3 0.9.0, Version-Update-Check |
| v0.4.1 | 2026-03-29 | Streaming-Mipmap-Architektur (Peak-Memory -21% bis -44%), parallele Paket-Downloads, Temp-Dir nach ~/.xearthlayer/tmp |
| v0.4.0 | 2026-03-21 | X-Plane Web API Telemetrie (ersetzt ForeFlight UDP), Sliding Prefetch Box, Debug Map, GPU Pipeline Overlap |
| v0.3.1 | 2026-03-07 | GPU-beschleunigtes DDS-Encoding, ISPC-SIMD als Standard, Boundary-Driven Prefetch, Online-Netzwerk-Unterstützung |
| v0.3.0 | 2026-02-05 | Adaptive Prefetch System, Job Executor Framework (kompletter Rewrite des Execution Core), Aircraft Position & Telemetry Modul, Scene Tracker, Self-Contained Cache Services |
| v0.2.12 | 2026-01-10 | Consolidated FUSE Mounting (Single Mount Point), Tile Patches Support, Circuit Breaker für Prefetch, Ring-Based Radial Prefetching |
| v0.2.10 | 2026-01-02 | Setup Wizard, Default-to-Run, Coverage Map Generator, Zoom Level Deduplication, Coverage Gap Analysis |
| v0.2.9 | 2025-12-28 | Disk Cache Eviction Daemon, SceneryIndex Persistent Cache, Cold-Start Prewarm (`--airport`), Dashboard Loading State |
| v0.2.8 | 2025-12-27 | Heading-Aware Prefetch, Multi-Zoom Prefetch (ZL12), Config Auto-Upgrade, Pipeline Control Plane, ForeFlight UDP Listener |
| v0.2.7 | 2025-12-21 | Storage-Aware Disk I/O Profiles (auto/hdd/ssd/nvme), Shared CPU Limiter mit Over-Subscription, Deadlock-Fix |
| v0.2.6 | 2025-12-19 | Apple Maps, ArcGIS, MapBox, USGS (4 neue Provider), Disk I/O Concurrency Limiting, `--debug` Flag |
| v0.2.5 | 2025-12-16 | CI-Workflow vereinfacht, atomarer Release-Prozess |

Quelle: https://github.com/samsoir/xearthlayer/releases

### Entwicklungsgeschwindigkeit

14 Releases in ca. 17 Wochen (16. Dez 2025 bis 17. Apr 2026). Das Projekt ist in einer Phase sehr aktiver Entwicklung.

---

## 2. Architektur

### Technologie-Stack

- **Sprache:** Rust (Edition 2021)
- **Lizenz:** MIT
- **FUSE-Bibliotheken:** `fuse3` v0.8 (primär, async mit Tokio-Runtime) + `fuser` v0.14 (Legacy-Typdefinitionen)
- **Async Runtime:** Tokio v1 (Multi-Threaded)
- **HTTP Client:** reqwest v0.12 (mit rustls-tls)
- **Caching:** moka v0.12 (async LRU), DashMap v6.1
- **Bildverarbeitung:** image v0.25
- **Parallelisierung:** rayon v1.10

Quelle: https://github.com/samsoir/xearthlayer/blob/main/xearthlayer/Cargo.toml

### FUSE Virtual File System

XEarthLayer erstellt ein FUSE-Dateisystem, das X-Plane als reguläres Scenery-Verzeichnis sieht. Ab v0.2.12 nutzt es einen **Single Mount Point** (`zzXEL_ortho`), in dem alle regionalen Pakete und Patches über einen `OrthoUnionIndex` zusammengeführt werden. Patches haben dabei immer Vorrang vor regionalen Paketen (Priority-Based Collision Resolution).

### 8-Stufen-Tile-Pipeline

1. **Request**: X-Plane fordert eine DSF-Datei an
2. **Image Resource**: DSF-Dekodierung erzeugt Textur-Anfragen
3. **Cache Check**: Erst Memory-Cache, dann Disk-Cache
4. **Download**: Fehlende Tile-Chunks vom Satellitenprovider laden
5. **Assembly**: 256 Image-Chunks zu 4096x4096 DDS-Bild zusammensetzen
6. **Encode**: BC1/BC3-DDS-Kompression mit Mipmaps
7. **Cache**: Fertiges DDS in Memory-Cache, Chunks auf Disk
8. **Serve**: DDS-Textur an X-Plane ausliefern

Quelle: https://xearthlayer.app/docs/how-it-works/

### Zwei-Tier-Cache

1. **Memory-Cache**: Fertige DDS-Texturen im RAM, < 10 ms Zugriffszeit
2. **Disk-Cache**: Image-Chunks persistent auf Disk, reduziert Downloads bei Wiederbesuch

LRU-Eviction über In-Memory-Index. Garbage Collection läuft als Executor-Job (async, cancellable).

### Adaptives Prefetch-System (Stand v0.4.4)

- **Self-Calibration**: Misst Tile-Generation-Throughput beim initialen Scene Load
- **Flight Phase Detection**: Ground (< 40 kt Groundspeed) vs. Cruise (> 40 kt)
- **Unified PrefetchBox (seit v0.4.4)**: Ground und Cruise teilen einen Code-Pfad — Ground nutzt fixe Extent mit symmetrischer Bias (0.5), Cruise nutzt geschwindigkeitsproportionale Extent mit Heading-Bias (0.8); ersetzt die alte ring-basierte `GroundStrategy` (746 Zeilen Code entfernt)
- **Drei Modi**: Aggressive (> 30 tiles/sec), Opportunistic (10-30 tiles/sec), Disabled (< 10 tiles/sec)
- **Circuit Breaker**: Pausiert Prefetch automatisch, wenn X-Plane aktiv Szenen lädt (> 50 FUSE-Requests/sec)
- **Long-Haul-Stabilität (Fix in v0.4.4, Issue #172)**: Drei zusammenwirkende Bugs (vorzeitiges `mark_in_progress`, unvollständiger `cached_tiles`-Shadow-Set tracked nur ~6% der gecachten Tiles, Chunk- vs. Tile-Coords im DDS-Disk-Lookup) verursachten permanente Dead-States nach >2 h Flugzeit; behoben durch authoritative DDS-Disk-Cache-Queries und mit 9-h-LOWW-Log verifiziert
- **Debug-Map SSOT (seit v0.4.4)**: Coordinator publiziert Bounds einmal pro Cycle als `BoxBoundsSnapshot`, Debug-Map liest verbatim — keine Drift mehr zwischen Anzeige und Realität. Region-Farben GeoIndex-authoritativ: gelb (InProgress) bis Tile-Verifikation, dann grün (Prefetched), neu orange (Mixed) wenn FUSE Tiles aus prefetchter Region geliefert hat

### Job Executor Framework (neu in v0.3.0)

- Async, non-blocking Execution ersetzt die Legacy-`spawn_blocking`-Pipeline
- **Priority Scheduling**: ON_DEMAND (100) > PREFETCH (0) > HOUSEKEEPING (-50)
- **Resource Pools**: Semaphore-basierte Concurrency Limits nach Typ (Network, CPU, DiskIO)
- **Request Coalescing**: Gleichzeitige Anfragen für dieselbe Kachel teilen sich einen Job
- **Cancellation Support** via CancellationToken
- **Stall Detection Watchdog**
- Modularer Aufbau: core, config, submitter, active_job, lifecycle, dispatch, signals, watchdog

Quelle: https://github.com/samsoir/xearthlayer/releases/tag/v0.3.0

---

## 3. Linux-spezifische Aspekte

### Betriebssystem

**Nur Linux** (amd64). macOS möglicherweise bei Community-Interesse; Windows unwahrscheinlich.

Quelle: https://xearthlayer.app/docs/faq/

### Distributionspakete

Auf der GitHub Releases-Seite stehen vier Installationsformate bereit:

| Format | Ziel-Distribution | v0.3.0 Dateigröße | Downloads (Stand 14.02.2026) |
|--------|-------------------|-------------------|------------------------------|
| `.deb` | Debian/Ubuntu | 4,6 MB | 9 |
| `.rpm` | Fedora/RHEL (fc43) | 5,7 MB | 6 |
| AUR | Arch Linux | 636 Bytes (PKGBUILD) | 6 |
| `.tar.gz` | Generisch | 7,7 MB | 4 |

Installation Debian/Ubuntu:
```bash
wget https://github.com/samsoir/xearthlayer/releases/download/v0.3.0/xearthlayer_0.3.0-1_amd64.deb
sudo dpkg -i xearthlayer_0.3.0-1_amd64.deb
xearthlayer setup
```

Quelle: https://github.com/samsoir/xearthlayer/releases/tag/v0.3.0

### Build from Source

```bash
git clone https://github.com/samsoir/xearthlayer.git
cd xearthlayer
make release
make install    # Installiert nach ~/.local/bin (kein sudo nötig)
xearthlayer setup
```

**Voraussetzungen:**
- Rust Toolchain (via rustup.rs)
- FUSE-Entwicklungsbibliotheken (für `fuse3` v0.8)
- Make, Standard-Entwicklungstools

Der Makefile enthält ein `make init`-Target, das fehlende Rust-Toolchain-Komponenten automatisch installiert. Optionale Dev-Tools: cargo-watch, cargo-tarpaulin, cargo-deb.

Quelle: https://github.com/samsoir/xearthlayer/blob/main/Makefile

### FUSE-Version

Das Projekt verwendet `fuse3` v0.8 (Rust-Crate) mit async Tokio-Runtime und unprivileged features. Auf Systemebene wird FUSE3 benötigt (libfuse3-dev auf Debian). Die genaue Mindest-FUSE-Version ist nicht dokumentiert.

### Disk I/O Auto-Detection (Linux-spezifisch)

XEarthLayer erkennt den Speichertyp automatisch über `/sys/block/<device>/queue/rotational`:

| Profil | Gleichzeitige I/O-Ops | Erkennung |
|--------|----------------------|-----------|
| HDD | 1-4 | `rotational = 1` |
| SSD | 32-64 | Fallback |
| NVMe | 128-256 | `rotational = 0` + NVMe-Erkennung |

Quelle: https://github.com/samsoir/xearthlayer/releases/tag/v0.2.7

---

## 4. Features

### Kartenanbieter

| Provider | Kosten | Abdeckung | Anmerkung |
|----------|--------|-----------|-----------|
| Bing Maps | Kostenlos | Global | Standard |
| Google Maps | Kostenlos (GO2) oder API | Global | |
| Apple Maps | Kostenlos | Global | Auto-Token via DuckDuckGo MapKit JWT |
| ArcGIS | Kostenlos | Global | Kein API-Key nötig |
| MapBox | Token nötig | Global | Kostenloser Access Token ausreichend |
| USGS | Kostenlos | Nur USA | Hervorragende Qualität |

Konfiguration über `provider.name` in `~/.xearthlayer/config.ini`.

Quelle: https://xearthlayer.app/docs/configuration/, https://github.com/samsoir/xearthlayer/releases/tag/v0.2.6

### Regionale Pakete

Pakete werden über ein separates Repository bereitgestellt: https://github.com/samsoir/xearthlayer-regional-scenery

Aktuell verfügbare Regionen (Stand Feb 2026):

| Region | Paket-ID | Aktuelle Version | Datum |
|--------|----------|-----------------|-------|
| Europe | `eu` | v0.1.1 | 2026-01-04 |
| North America | `na` | v0.2.3 | 2026-01-07 |
| South America | `sa` | v0.2.0 | 2026-01-11 |
| Oceania | `oc` | v0.2.0 | 2026-01-18 |
| Asia - Part 3 | `as3` | v0.1.0 | 2026-01-24 |
| Africa - Part 2 | `af2` | v0.1.0 | 2026-01-25 |

Die Pakete enthalten DSF/TER-Dateien (Digital Surface Format / Terrain) und basieren auf dem Shred86 Ortho4XP-Fork.

Quelle: https://github.com/samsoir/xearthlayer-regional-scenery/releases

### CLI-Befehle

**Setup und Konfiguration:**
- `xearthlayer setup` -- Interaktiver Einrichtungsassistent (erkennt X-Plane, Hardware)
- `xearthlayer init` -- Default-Config erstellen
- `xearthlayer config list` -- Einstellungen anzeigen
- `xearthlayer config set <key> <value>` -- Einstellung ändern
- `xearthlayer config upgrade` -- Config auf neue Version migrieren

**Paketverwaltung:**
- `xearthlayer packages check` -- Verfügbare Pakete prüfen
- `xearthlayer packages install <region>` -- Region installieren
- `xearthlayer packages list` -- Installierte Pakete anzeigen
- `xearthlayer packages update [region]` -- Pakete aktualisieren
- `xearthlayer packages remove <region>` -- Paket entfernen

**Betrieb:**
- `xearthlayer` oder `xearthlayer run` -- Service starten mit Dashboard
- `xearthlayer run --airport KJFK` -- Start mit Cache Pre-Warming
- `xearthlayer run --debug` -- Debug-Logging aktivieren

**Cache und Szenen-Index:**
- `xearthlayer cache stats` -- Cache-Nutzung anzeigen
- `xearthlayer cache clear` -- Cache leeren
- `xearthlayer scenery-index status` -- Index-Status
- `xearthlayer scenery-index update` -- Index neu aufbauen
- `xearthlayer scenery-index clear` -- Index-Cache löschen
- `xearthlayer diagnostics` -- System-Diagnose

**Publishing (für Paket-Ersteller):**
- `xearthlayer publish init/add/build/release`
- `xearthlayer publish coverage [--dark] [--geojson]`
- `xearthlayer publish dedupe`
- `xearthlayer publish gaps`

Quellen: https://github.com/samsoir/xearthlayer, https://xearthlayer.app/docs/getting-started/

### ForeFlight-Telemetrie

XEarthLayer empfängt Flugdaten über das ForeFlight/XGPS2-Protokoll auf UDP-Port 49002. Einrichtung: In X-Plane unter Settings die Option "Send to ForeFlight" aktivieren. Ohne Telemetrie fällt das System auf Dead-Reckoning aus FUSE-Requests zurück.

### Tile Patches (ab v0.2.12)

Benutzerdefinierte Mesh-/Höhendaten aus Airport-Addons können als Patches eingebunden werden:
- Ablage in `~/.xearthlayer/patches/`
- Patches mit `Earth nav data/`-Ordner (DSF-Dateien) werden automatisch erkannt
- Patches haben immer Vorrang vor regionalen Paketen

### Real-Time Dashboard

Terminal-basiertes TUI-Dashboard mit:
- Cache-Statistiken und Download-Metriken
- GPS-Status und Telemetrie-Quelle (UDP/FUSE/None)
- Prefetch-Modus-Anzeige
- Active Tiles Queue (nach Fortschritt sortiert)
- System Health (Healthy/Degraded/Critical)

---

## 5. CPU-Tuning

### Drei-Stufen-Hierarchie

| Einstellung | Sektion | Default | Funktion |
|-------------|---------|---------|----------|
| `threads` | `[generation]` | `num_cpus` | Worker-Threads für Tile-Generierung |
| `cpu_concurrent` | `[executor]` | `num_cpus / 2` (seit v0.4.3) | Gleichzeitige CPU-intensive Ops (DDS-Encoding) |
| `max_concurrent_jobs` | `[executor]` | `num_cpus / 2` (seit v0.4.4, vorher `ceil(num_cpus × 0.75)`) | Maximale gleichzeitige Tile-Jobs |

**Effektivster Hebel**: `cpu_concurrent` -- begrenzt BC1/BC3-Kompression (ca. 0,2 s pro 4096x4096 Tile).

### Resource-Pool-Architektur

- **Ebene 1**: Control Plane (`max_concurrent_jobs`) -- Gesamtzahl aktiver Tile-Jobs
- **Ebene 2**: Executor (`max_concurrent_tasks = 128`) -- Alle Tasks zusammen
- **Ebene 3**: Resource Pools:
    - Network Pool (`network_concurrent = min(num_cpus * 16, 256)`) -- HTTP/TLS
    - CPU Pool (`cpu_concurrent`) -- Assembly + DDS-Encode
    - Disk Pool (profilabhängig) -- Cache I/O

### Empfohlene Werte (16 logische CPUs, 8 Kerne + HT)

| Szenario | `threads` | `cpu_concurrent` | `max_concurrent_jobs` |
|----------|-----------|------------------|-----------------------|
| XEL allein (Default ab v0.4.4) | 16 | 8 | 8 |
| XEL + X-Plane | 6-8 | 6-8 | 8 |
| XEL + X-Plane + Streaming | 4 | 4 | 4 |
| XEL im Hintergrund | 2 | 2 | 2 |

Faustregel: Bei parallelem X-Plane-Betrieb auf die Hälfte der physischen Kerne beschränken.

### Weitere Executor-Einstellungen (v0.3.0)

```ini
[executor]
max_concurrent_tasks = 128     # Obergrenze aller Tasks
job_channel_capacity = 256     # Job-Channel-Kapazität
tile_generation_limit = 40     # Max gleichzeitige DDS-Generierung
```

Quellen: Source-Code-Analyse (Cargo.toml), Release Notes v0.2.7, v0.3.0

---

## 6. Performance

### Systemanforderungen (Website)

| Tier | CPU | RAM | GPU VRAM | Storage | Internet |
|------|-----|-----|----------|---------|----------|
| Minimum | 4 Kerne | 2 GB | 4 GB | 50 GB | 100 Mbps |
| Recommended | 8 Kerne | 32 GB | 12 GB | 100 GB | 500 Mbps |
| Ultimate | 16 Kerne | 64 GB | 24 GB | 250 GB+ | 1 Gbps |

Quelle: https://xearthlayer.app (Homepage)

Hinweis: Die README nennt "800 Mbps recommended", die Website-Tabelle nennt 500 Mbps als "Recommended" und 1 Gbps als "Ultimate". Die 800-Mbps-Zahl scheint eine ältere Angabe zu sein, die in der differenzierteren Tier-Tabelle aufgegangen ist.

### Performance-Kennzahlen (Website)

| Metrik | Wert |
|--------|------|
| Scene Load (cached) | 1-2 Minuten |
| Cache Hit Latenz | < 10 ms |
| Cold Download (pro Tile, 1 Gbit+) | 1-2 Sekunden |

Quelle: https://xearthlayer.app/docs/how-it-works/

### Vergleich mit AutoOrtho

Kein formaler Benchmark vorhanden. Aus den Quellen ergeben sich folgende strukturelle Unterschiede:

| Dimension | XEarthLayer | AutoOrtho (ProgrammingDinosaur Fork v2.0) |
|-----------|-------------|-------------------------------------------|
| Sprache | Rust | Python + C-Pipeline (ab 2.0) |
| Prefetch | Adaptiv (Ground/Cruise, self-calibrating) | Einfach (proximity-based, Simbrief) |
| Circuit Breaker | Ja (pausiert bei Scene Load) | Nein |
| Cache-Eviction | Automatisch, LRU mit GC-Job | Automatisch |
| Plattform | Nur Linux | Windows, Linux, macOS |
| Simulator | Nur X-Plane 12 | X-Plane 11.50+ und 12 |
| GUI | Keine (CLI + TUI-Dashboard) | Moderne GUI |
| Regionale Pakete | Separate DSF/TER-Pakete nötig | Integrierte Overlay-Downloads |
| Provider | 6 (Bing, Google, Apple, ArcGIS, MapBox, USGS) | 5+ (Bing, Google, Here, Yandex, Apple) |
| Job Scheduling | Priority-based (ON_DEMAND > PREFETCH) | Nicht dokumentiert |

XEarthLayer positioniert sich als performantere, Linux-exklusive Alternative. AutoOrtho bietet breitere Plattformunterstützung und einfachere Einrichtung.

Quellen: https://github.com/samsoir/xearthlayer, https://github.com/ProgrammingDinosaur/autoortho4xplane, https://xearthlayer.app/docs/faq/

### Cache-Empfehlungen

- Disk-Cache: mindestens 50 GB, ideal 100 GB+
- Memory-Cache: ca. 15 GB bei Systemen mit 32 GB RAM (Default: 2 GB)
- Texturformat: BC1 (schneller als BC3, kein Alpha-Kanal nötig)
- Datenverbrauch: 6-10 GB initiales Cache-Setup, 3-5 GB pro Breitengrad Flugstrecke

Quelle: https://xearthlayer.app/docs/faq/

---

## 7. Bekannte Probleme und Limitierungen

### Plattform-Limitierungen

- **Nur Linux** (amd64) -- kein Windows, kein macOS
- **Nur X-Plane 12** -- X-Plane 11 theoretisch kompatibel, aber nicht getestet; Pakete nur für XP12
- **Keine GUI** -- nur CLI und Terminal-Dashboard
- **ForeFlight-Telemetrie nötig** für adaptives Prefetching (Fallback: Dead-Reckoning)

### Offene Issues (Stand 14. Feb 2026)

| Issue | Titel | Datum |
|-------|-------|-------|
| #53 | X-Plane FUSE requests trigger network calls for pre-cached tiles | 2026-02-07 |
| #51 | Excessive tile processing/prefetching despite DDS tiles present in patches | 2026-02-07 |

Dazu zwei offene PRs (#52, #54) die diese Issues adressieren.

Quelle: https://github.com/samsoir/xearthlayer/issues

### Kürzlich behobene Bugs

- **#46**: Lange Startup-Zeit / Cache-Indexing in v0.3.0 (behoben: Region-basiertes Disk-Cache-Layout)
- **#45**: Inkonsistentes Overlay-Symlink-Management
- **#38**: `ls` in FUSE-gemounteten Verzeichnissen schlug fehl (behoben in v0.3.0)
- **#39**: Prefetch lud bereits installierte Ortho-Tiles erneut herunter (behoben in v0.3.0)
- **#21**: Unerwartet schlechte Performance beim Laden gecachter Imagery (behoben in v0.2.7)
- **#14**: X-Plane Crash beim Start mit XEarthLayer (behoben in v0.2.6)

### Bekannte Troubleshooting-Szenarien (FAQ)

- **Magenta Tiles**: Timeout-Fehler durch langsame Downloads oder Systemüberlastung. Lösung: Concurrent-Settings um 50% reduzieren.
- **Weiße Tiles**: FUSE-Prozess durch OOM-Killer beendet. Lösung: Kernel-Logs prüfen, Swap hinzufügen.
- **Szenen laden nicht**: XEarthLayer muss vor X-Plane gestartet werden (XP indexiert Scenery beim Start).

Quelle: https://xearthlayer.app/docs/faq/

---

## 8. Entwicklungsaktivität

### Repository-Statistiken

| Metrik | Wert |
|--------|------|
| Stars | 10 |
| Forks | 2 |
| Offene Issues | 4 (davon 2 PRs) |
| Erstellt | 18. Nov 2025 |
| Letztes Update | 10. Feb 2026 |
| Lizenz | MIT |
| Sprache | Rust |
| Contributors | 2 (samsoir: 334 Commits, mmaechtel: 1 Commit) |
| Releases | 8 (v0.2.5 bis v0.3.0) |
| Gesamt-Issues/PRs | 55 (51 geschlossen, 4 offen) |

Quelle: https://github.com/samsoir/xearthlayer

### Entwicklungshistorie

- **Sommer 2025**: Projektstart nach Systemmigration von Windows zu Linux. Autor Sam de Freyssinet versuchte zunächst AutoOrtho zu reparieren und entschied sich dann für eine Neuimplementierung in Rust.
- **November 2025**: Erstes öffentliches Repository
- **Dezember 2025**: Intensive Feature-Entwicklung (6 Releases in 2 Wochen). Provider-Erweiterung, Prefetch-System, Cache-Eviction, Control Plane.
- **Januar 2026**: Setup Wizard, regionale Pakete (EU, NA, SA, OC, AS3, AF2), Consolidated FUSE Mounting, Patches-Support.
- **Februar 2026**: v0.3.0 Major Release mit Adaptive Prefetch System und Job Executor Framework. Community-Standards (CONTRIBUTING, SECURITY POLICY).

### Autor

Sam de Freyssinet -- Software Engineering Director aus Kalifornien. Flugsimulations-Enthusiast seit Microsoft Flight Simulator 2.0. Seit 2016 auch realer Pilot.

Quelle: https://xearthlayer.app/docs/about/

### Community

- GitHub: Bug Reports und Code-Beiträge
- Discord: User Support
- YouTube: Tutorials und Development Updates
- Ko-fi: Spenden

### AI-gestützte Entwicklung

Das Projekt nutzt Claude (Anthropic) für AI-Paired-Programming und Dokumentation. Ein `CLAUDE.md` ist im Repository enthalten.

---

## 9. Offene Fragen für die Dokumentation

1. **FUSE-Mindestversion**: Nicht explizit dokumentiert. `fuse3` v0.8 wird als Crate verwendet -- welche libfuse3-Version ist auf Systemebene erforderlich?
2. **Paket-Größen**: Die konkreten Download-Größen der regionalen Pakete (EU, NA etc.) sind nicht dokumentiert.
3. **800 Mbps vs. 500 Mbps**: Die README nennt 800 Mbps, die Website-Tabelle 500 Mbps als "Recommended". Die Angabe in der existierenden XoL-Docs-Seite sollte konsistent mit der aktuellen Website sein.
4. **X-Plane 12.3 Minimum**: Die Website-Homepage nennt "X-Plane 12.3 or later", die README nur "X-Plane 12". Klärung nötig.
5. **Keine formalen Benchmarks**: Es existiert kein publizierter Vergleichstest XEarthLayer vs. AutoOrtho.
6. **macOS/Windows-Zeitplan**: FAQ sagt "may be added with community interest" -- keine konkreten Pläne.

---

## Quellenverzeichnis

1. GitHub Repository: https://github.com/samsoir/xearthlayer
2. GitHub Releases: https://github.com/samsoir/xearthlayer/releases
3. GitHub Issues: https://github.com/samsoir/xearthlayer/issues
4. Regional Scenery Repository: https://github.com/samsoir/xearthlayer-regional-scenery
5. Website: https://xearthlayer.app
6. Website Docs (Getting Started): https://xearthlayer.app/docs/getting-started/
7. Website Docs (How It Works): https://xearthlayer.app/docs/how-it-works/
8. Website Docs (Configuration): https://xearthlayer.app/docs/configuration/
9. Website Docs (FAQ): https://xearthlayer.app/docs/faq/
10. Website Docs (About): https://xearthlayer.app/docs/about/
11. AutoOrtho Fork: https://github.com/ProgrammingDinosaur/autoortho4xplane
