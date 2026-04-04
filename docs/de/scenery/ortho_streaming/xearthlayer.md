---
description: "XEarthLayer ist ein Rust-basiertes Ortho-Streaming-Tool für X-Plane 12 unter Linux mit GPU-beschleunigter Kompression, adaptivem Prefetch, zweistufigem Cache und CPU-Tuning."
---
# XEarthLayer

**XEarthLayer** ist eine in Rust geschriebene Alternative zu [AutoOrtho](../../glossary.md#autoortho) für das Streaming von [Orthofoto](../../glossary.md#orthofotos)-Texturen in X-Plane 12. Das Projekt ist inspiriert von AutoOrtho, setzt jedoch auf eine performante Rust-Implementierung mit optionaler GPU-beschleunigter Kompression, adaptivem Prefetching und einem Zwei-Tier-Cache-System.

!!! note "Aktive Entwicklung"
    XEarthLayer ist ein junges Projekt in aktiver Entwicklung. Aktuelle Versionen laufen stabil, der Funktionsumfang kann sich zwischen Releases aber noch ändern.

## Funktionsweise

XEarthLayer nutzt ein **[FUSE](../../glossary.md#fuse-filesystem-in-userspace)-basiertes virtuelles Dateisystem** (siehe [Wie Ortho-Streaming funktioniert](how_streaming_works.md)), um Orthofoto-Texturen on demand bereitzustellen. Beim Zugriff auf eine Kachel durch X-Plane wird das Satellitenbild vom konfigurierten Kartenanbieter heruntergeladen, in das [DDS](../../glossary.md#dds-directdraw-surface)-Format (BC1/BC3) komprimiert und über das VFS an den Simulator ausgeliefert.

### DDS-Komprimierungs-Backends

XEarthLayer bietet drei Backends für die DDS-Texturkomprimierung, konfigurierbar über `compressor` in der `[texture]`-Sektion von `config.ini`:

| Backend | Beschreibung |
|---|---|
| **ISPC** (Standard) | Intel ISPC-optimierte SIMD-Komprimierung — deutlich schneller als die ursprüngliche Pure-Rust-Implementierung |
| **GPU** | GPU-beschleunigte Komprimierung über wgpu/WGSL Compute Shaders (erfordert `--features gpu-encode` Build-Flag) |
| **Software** | Pure-Rust-Fallback, keine externen Abhängigkeiten |

Das GPU-Backend lagert die BC1/BC3-Komprimierung über Compute Shaders auf die Grafikkarte aus und entlastet so die CPU für X-Plane. Bei mehreren GPUs kann über `gpu_device` in der `[texture]`-Sektion ein spezifisches Gerät ausgewählt werden.

Alle Backends nutzen eine **Streaming-Mipmap-Architektur**, die Mipmaps progressiv generiert statt sie im Speicher zu puffern, was den Peak-Speicherverbrauch deutlich reduziert.

### Zwei-Tier-Cache

XEarthLayer verwendet ein zweistufiges Cache-System:

1. **Memory-Cache**: Häufig genutzte Kacheln werden im Arbeitsspeicher vorgehalten für minimale Latenz
2. **Disk-Cache**: Alle heruntergeladenen und konvertierten Kacheln werden persistent in regionsbasierten Unterverzeichnissen gespeichert, mit parallelem Scanning für schnellen Start

Wird die konfigurierte Cache-Größe erreicht, werden ältere Kacheln automatisch entfernt, um Platz für neue zu schaffen.

### Adaptives Prefetch

XEarthLayers **adaptives Prefetching** nutzt ein Boundary-Driven-Modell: Ein `SceneryWindow` verfolgt die Flugzeugposition relativ zu DSF-Kachelgrenzen, ein `BoundaryMonitor` erkennt Grenzübertritte auf Reihen- und Spaltenachsen. Bei einem Grenzübertritt werden Kacheln mit asymmetrischer Tiefe vorgeladen — typischerweise 3 Reihen tief und 3–4 Spalten breit, angepasst an die Flugrichtung.

Das System kalibriert sich selbst und passt die Prefetch-Strategie an die verfügbare Bandbreite und die aktuelle Flugphase an. On-Demand-Anfragen von X-Plane haben durch **Priority Scheduling** immer Vorrang vor Prefetch (On-Demand-Jobs laufen mit höherer Priorität als Prefetch). Ein **ressourcenbasierter Circuit Breaker** pausiert Prefetch, wenn die Auslastung der Ressourcenpools (CPU, Netzwerk, Disk-I/O) sichere Schwellwerte übersteigt — so wird sichergestellt, dass die aktuell sichtbaren Kacheln immer zuerst geladen werden.

## Kartenquellen

XEarthLayer unterstützt folgende Kartenanbieter:

- Bing Maps
- Google Maps
- Apple Maps
- ArcGIS
- MapBox
- USGS

## Systemanforderungen

| Anforderung | Empfehlung |
|---|---|
| Betriebssystem | Linux (FUSE erforderlich) |
| Simulator | X-Plane 12.3 oder neuer |
| GPU (optional) | 4 GB VRAM Minimum, 12+ GB empfohlen (für GPU-Encoding-Backend) |
| Internetverbindung | ≥ 500 Mbps empfohlen |
| Speicher | SSD für Disk-Cache |
| Build-Umgebung | Rust Toolchain (nur bei Build aus Quellcode) |

!!! note "Nur Linux"
    XEarthLayer ist derzeit ausschließlich für Linux verfügbar. Windows- und macOS-Unterstützung sind nicht implementiert.

## Installation

Auf der [GitHub Releases-Seite](https://github.com/samsoir/xearthlayer/releases) stehen vorkompilierte Pakete bereit (`.deb`, `.rpm`, `.tar.gz`).

Installation auf Debian:

```bash
# Aktuelles .deb-Paket von der Releases-Seite herunterladen und installieren
sudo dpkg -i xearthlayer_<version>_amd64.deb

# Einrichtung
xearthlayer setup
```

Alternativ kann XEarthLayer auch aus dem Quellcode gebaut werden (erfordert Rust Toolchain):

```bash
git clone https://github.com/samsoir/xearthlayer.git
cd xearthlayer
make release            # Standard-Build (ISPC + Software Backends)
# make release-gpu      # Build mit GPU-Encoding-Backend
make install            # Installiert nach ~/.local/bin
xearthlayer setup
```

Die Einrichtung konfiguriert das Cache-Verzeichnis und die Verknüpfung mit dem [Custom Scenery](../../glossary.md#custom-scenery)-Ordner von X-Plane. Temporäre Dateien werden in `~/.xearthlayer/tmp` abgelegt (nicht im System-`/tmp`, das oft RAM-basiert ist und zu Speicherengpässen führen kann).

## Verwendung

XEarthLayer muss vor X-Plane gestartet werden, damit das virtuelle Dateisystem gemountet wird:

```bash
# Standard-Start
xearthlayer

# Start mit Cache-Vorwärmen für einen bestimmten Flughafen
xearthlayer run --airport KJFK
```

Für das adaptive Prefetching muss in X-Plane die **ForeFlight-Telemetrie** aktiviert sein (UDP-Port 49002), damit XEarthLayer die Flugzeugposition und -geschwindigkeit empfangen kann. Alternativ kann XEarthLayer die Positionsdaten von Online-Netzwerken (VATSIM, IVAO, PilotEdge) über deren REST-APIs beziehen.

## Regionale Pakete

XEarthLayer benötigt separate **[DSF](../../glossary.md#dsf-distribution-scenery-format)/TER-Pakete** (Digital Surface Format / Terrain), die die [Mesh](../../glossary.md#mesh)-Daten und Terrain-Definitionen für die jeweiligen Regionen enthalten. Fertige Pakete können direkt über die CLI installiert werden:

```bash
# Verfügbare Pakete anzeigen
xearthlayer packages list

# Paket installieren (z. B. Europa)
xearthlayer packages install eu

# Installierte Pakete aktualisieren
xearthlayer packages update
```

Paket-Downloads laufen parallel (konfigurierbar 1–10 gleichzeitige Teile, Standard 5) mit Fortschrittsanzeige pro Teil und automatischem Retry bei Fehlern.

Die Pakete stammen aus dem [XEarthLayer Regional Scenery Repository](https://github.com/samsoir/xearthlayer-regional-scenery) und basieren auf dem [Shred86 Ortho4XP-Fork](https://github.com/shred86/Ortho4XP).

## CPU-Tuning

XEarthLayer nutzt standardmäßig **alle verfügbaren CPU-Kerne** für die parallele Tile-Generierung. Auch mit dem effizienteren ISPC-Backend bleibt die DDS-Komprimierung CPU-intensiv. Das ist optimal, wenn XEarthLayer allein läuft — kann aber zu Engpässen führen, wenn gleichzeitig X-Plane aktiv ist.

!!! tip "GPU-Encoding als Alternative"
    Mit dem GPU-Encoding-Backend wird die DDS-Komprimierung auf die Grafikkarte ausgelagert. Das reduziert die CPU-Last, kann aber zu GPU-Engpässen führen, da X-Plane selbst GPU-intensiv ist. Der Trade-off hängt vom verfügbaren VRAM und der GPU-Auslastung ab.

### Das Problem

X-Plane ist stark Mainthread-gebunden. Wenn XEarthLayer alle Kerne sättigt, kommt es zu:

- **Thread-Überbelegung**: Mehr aktive Threads als verfügbare Kerne erzwingen ständige Context-Switches
- **Hyperthreading-Limitierung**: Zwei CPU-intensive Threads auf demselben physischen Kern erreichen zusammen nur ca. 120–130% der Leistung eines einzelnen Threads
- **X-Plane-Stuttering**: Die Frametime steigt, weil der X-Plane-Mainthread um CPU-Zeit konkurriert

### Relevante Einstellungen

Drei Einstellungen in `~/.xearthlayer/config.ini` steuern die CPU-Nutzung:

| Einstellung | Sektion | Standard | Funktion |
|---|---|---|---|
| `threads` | `[generation]` | Anzahl CPUs | Worker-Threads für Tile-Generierung |
| `cpu_concurrent` | `[executor]` | ~CPUs × 1,25 | Gleichzeitige DDS-Encoding-Operationen (wirkungsvollster Hebel) |
| `max_concurrent_jobs` | `[control_plane]` | CPUs × 2 | Maximale gleichzeitige Tile-Jobs insgesamt |

### Empfohlene Werte

**Faustregel**: Bei parallelem X-Plane-Betrieb auf die Hälfte der *physischen* Kerne beschränken.

| Szenario | `threads` | `cpu_concurrent` | `max_concurrent_jobs` |
|---|---|---|---|
| XEL allein (Default) | 16 | 20 | 32 |
| XEL + X-Plane | 6–8 | 6–8 | 12–16 |
| XEL + X-Plane + Streaming | 4 | 4 | 8 |

*Beispielwerte für ein System mit 16 logischen CPUs (8 Kerne + Hyperthreading)*

---

## Vergleich mit AutoOrtho

| Dimension | XEarthLayer | AutoOrtho (ProgrammingDinosaur Fork) |
|---|---|---|
| Programmiersprache | Rust (+ optionale GPU Compute Shaders) | Python + native C-Pipeline |
| DDS-Komprimierung | ISPC SIMD (Standard) oder GPU-beschleunigt | C-basiert mit dediziertem Decode-Pool |
| Prefetch-Strategie | Boundary-Driven (adaptive Tiefe) | Umgebungsbasiert |
| Cache-Eviction | Automatisch (ältere Kacheln werden entfernt) | Automatisch (ältere Kacheln werden entfernt) |
| X-Plane 12 Features | Vollständig (Seasons, regionale Texturen — über Ortho4XP-basierte DSF/TER-Pakete) | Ja (Seasons integriert) |
| Plattform | Nur Linux | Windows, Linux, macOS (Apple Silicon) |
| Simulator | Nur X-Plane 12 | X-Plane 11.50+ und 12 |
| Installation | Binary-Pakete oder aus Quellcode | Binary-Installer oder Python |
| Regionale Pakete | Integrierte CLI-Installation (`xearthlayer packages install`) | Integrierte Overlay-Downloads |
| SimBrief-Integration | In Entwicklung | Ja |
| GUI | CLI mit Live-Dashboard | GUI mit Konfigurationspanels |

XEarthLayer richtet sich an Linux-Nutzer, die maximale Streaming-Performance durch GPU-Offloading und Boundary-Driven-Prefetch suchen. AutoOrtho bietet breitere Plattformunterstützung, Seasons und eine einfachere GUI-basierte Einrichtung.

---

## Weiterführende Kapitel

| Thema | Seite | Schwerpunkt |
|---|---|---|
| AutoOrtho | [AutoOrtho](autoortho.md) | Alternative Streaming-Lösung mit breiterer Plattformunterstützung |
| Ortho4XP | [Ortho4XP](../orthophotography/ortho4xp.md) | Statische Ortho-Kachel-Generierung für Offline-Nutzung |
| Statisch + Streaming | [Statisch + Streaming](static_plus_streaming.md) | Kombination lokaler Kacheln mit Streaming |
| Szenerie-Komponenten | [Wie X-Plane die Welt aufbaut](../aufbau_quellen/scenery_components.md) | scenery_packs.ini-Ladereihenfolge |
| Kernel-Tuning | [Kernel-Tuning](../../linux/system/systemtuning.md) | CPU-Governor, IRQ-Pinning, Scheduler-Tuning |
| Dateisystem | [Dateisystem](../../linux/optimizations/filesystem.md) | NVMe/SSD-Optimierung für Cache-Performance |

---

## Quellen

- [GitHub Repository](https://github.com/samsoir/xearthlayer)
- [XEarthLayer Website](https://xearthlayer.app/)
- [Regionale Szenerie-Pakete](https://github.com/samsoir/xearthlayer-regional-scenery)
