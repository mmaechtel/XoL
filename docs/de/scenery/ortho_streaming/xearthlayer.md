---
description: "XEarthLayer ist ein Rust-basiertes Ortho-Streaming-Tool für X-Plane 12 unter Linux mit adaptivem Prefetch, zweistufigem Cache und CPU-Tuning."
---
# XEarthLayer

**XEarthLayer** ist eine in Rust geschriebene Alternative zu AutoOrtho für das Streaming von Orthofoto-Texturen in X-Plane 12. Das Projekt ist inspiriert von AutoOrtho, setzt jedoch auf eine performante Rust-Implementierung mit adaptivem Prefetching und einem Zwei-Tier-Cache-System.

!!! warning "Frühe Entwicklungsphase"
    XEarthLayer befindet sich in aktiver Entwicklung. Funktionsumfang und Stabilität können sich zwischen Versionen erheblich ändern.

## Funktionsweise

XEarthLayer nutzt ein **FUSE-basiertes virtuelles Dateisystem**, um Orthofoto-Texturen on demand bereitzustellen. Beim Zugriff auf eine Kachel durch X-Plane wird das Satellitenbild vom konfigurierten Kartenanbieter heruntergeladen, in das DDS-Format (BC1/BC3-Kompression) konvertiert und über das VFS an den Simulator ausgeliefert.

### Zwei-Tier-Cache

XEarthLayer verwendet ein zweistufiges Cache-System:

1. **Memory-Cache**: Häufig genutzte Kacheln werden im Arbeitsspeicher vorgehalten für minimale Latenz
2. **Disk-Cache**: Alle heruntergeladenen und konvertierten Kacheln werden persistent auf der Festplatte gespeichert

Wird die konfigurierte Cache-Größe erreicht, werden ältere Kacheln automatisch entfernt, um Platz für neue zu schaffen.

### Adaptives Prefetch

Ein Kernfeature von XEarthLayer ist das **adaptive Prefetching**, das zwischen zwei Modi umschaltet:

- **Ground-Mode (Ring-Prefetch)**: Bei niedriger Flughöhe und geringer Geschwindigkeit werden Kacheln in konzentrischen Ringen um die aktuelle Position vorgeladen — optimal für Anflugsituationen und bodennahes Fliegen
- **Cruise-Mode (Track-Prediction)**: Bei höherer Geschwindigkeit und Flughöhe sagt das System die voraussichtliche Flugroute voraus und lädt Kacheln entlang des prognostizierten Flugpfads vor

Das System kalibriert sich selbst und passt die Prefetch-Strategie an die verfügbare Bandbreite und die aktuelle Flugphase an. Ein **Circuit-Breaker-Mechanismus** sorgt dafür, dass Prefetch-Anfragen zurückgestellt werden, wenn die On-Demand-Anfragen von X-Plane Vorrang benötigen — so wird sichergestellt, dass die aktuell sichtbaren Kacheln immer zuerst geladen werden.

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
| Simulator | X-Plane 12 |
| Internetverbindung | ≥ 800 Mbps empfohlen |
| Speicher | SSD für Disk-Cache |
| Build-Umgebung | Rust Toolchain (nur bei Build aus Quellcode) |

!!! note "Nur Linux"
    XEarthLayer ist derzeit ausschließlich für Linux verfügbar. Windows- und macOS-Unterstützung sind nicht implementiert.

## Installation

Auf der [GitHub Releases-Seite](https://github.com/samsoir/xearthlayer/releases) stehen vorkompilierte Pakete bereit (`.deb`, `.rpm`, `.tar.gz`, AUR).

Installation auf Debian:

```bash
# .deb-Paket herunterladen und installieren
sudo dpkg -i xearthlayer_0.3.0-1_amd64.deb

# Einrichtung
xearthlayer setup
```

Alternativ kann XEarthLayer auch aus dem Quellcode gebaut werden (erfordert Rust Toolchain):

```bash
git clone https://github.com/samsoir/xearthlayer.git
cd xearthlayer
make release
make install    # Installiert nach ~/.local/bin
xearthlayer setup
```

Die Einrichtung konfiguriert das Cache-Verzeichnis und die Verknüpfung mit dem Custom-Scenery-Ordner von X-Plane.

## Verwendung

XEarthLayer muss vor X-Plane gestartet werden, damit das virtuelle Dateisystem gemountet wird:

```bash
# Standard-Start
xearthlayer

# Start mit Cache-Vorwärmen für einen bestimmten Flughafen
xearthlayer run --airport KJFK
```

Für das adaptive Prefetching muss in X-Plane die **ForeFlight-Telemetrie** aktiviert sein (UDP-Port 49002), damit XEarthLayer die Flugzeugposition und -geschwindigkeit empfangen kann.

## Regionale Pakete

XEarthLayer benötigt separate **DSF/TER-Pakete** (Digital Surface Format / Terrain), die die Mesh-Daten und Terrain-Definitionen für die jeweiligen Regionen enthalten. Fertige Pakete können direkt über die CLI installiert werden:

```bash
# Verfügbare Pakete anzeigen
xearthlayer packages list

# Paket installieren (z. B. Europa)
xearthlayer packages install eu

# Installierte Pakete aktualisieren
xearthlayer packages update
```

Die Pakete stammen aus dem [XEarthLayer Regional Scenery Repository](https://github.com/samsoir/xearthlayer-regional-scenery) und basieren auf dem [Shred86 Ortho4XP-Fork](https://github.com/shred86/Ortho4XP).

## CPU-Tuning

XEarthLayer nutzt standardmäßig **alle verfügbaren CPU-Kerne** für die parallele Tile-Generierung und DDS-Kompression. Das ist optimal, wenn XEarthLayer allein läuft — führt aber zu Problemen, wenn gleichzeitig X-Plane aktiv ist.

### Das Problem

X-Plane ist stark Mainthread-gebunden. Wenn XEarthLayer alle Kerne sättigt, kommt es zu:

- **Thread-Überbelegung**: Mehr aktive Threads als verfügbare Kerne erzwingen ständige Context-Switches
- **Hyperthreading-Limitierung**: Zwei CPU-intensive Threads auf demselben physischen Kern erreichen zusammen nur ca. 120–130% der Leistung eines einzelnen Threads
- **X-Plane-Stuttering**: Die Frametime steigt, weil der X-Plane-Mainthread um CPU-Zeit konkurriert

### Relevante Einstellungen

Drei Einstellungen in `~/.xearthlayer/config.ini` bilden eine Hierarchie:

| Einstellung | Sektion | Standard | Funktion |
|---|---|---|---|
| `threads` | `[generation]` | Anzahl CPUs | Worker-Threads für Tile-Generierung |
| `cpu_concurrent` | `[executor]` | CPUs × 1,25 | Gleichzeitige CPU-intensive Operationen (DDS-Encoding) |
| `max_concurrent_jobs` | `[control_plane]` | CPUs × 2 | Maximale gleichzeitige Tile-Jobs insgesamt |

Der wirkungsvollste Hebel ist `cpu_concurrent` — er begrenzt die DDS-Encoding-Operationen (BC1/BC3-Kompression), die den größten CPU-Anteil ausmachen.

### Empfohlene Werte

**Faustregel**: Bei parallelem X-Plane-Betrieb auf die Hälfte der *physischen* Kerne beschränken.

| Szenario | `threads` | `cpu_concurrent` | `max_concurrent_jobs` |
|---|---|---|---|
| XEL allein (Default) | 16 | 20 | 32 |
| XEL + X-Plane | 6–8 | 6–8 | 12–16 |
| XEL + X-Plane + Streaming | 4 | 4 | 8 |
| XEL im Hintergrund | 2 | 2 | 4 |

*Beispielwerte für ein System mit 16 logischen CPUs (8 Kerne + Hyperthreading)*

```ini
# ~/.xearthlayer/config.ini — Beispiel für XEL + X-Plane
[generation]
threads = 6

[executor]
cpu_concurrent = 6

[control_plane]
max_concurrent_jobs = 12
```

!!! tip "Netzwerk ist oft der Flaschenhals"
    Bei langsamer Internetverbindung bringt eine Reduktion der CPU-Threads kaum Performanceverlust, da die Threads ohnehin auf Downloads warten. Das Prefetch-System passt sich automatisch an den niedrigeren Durchsatz an.

Zusätzlich beeinflusst das Disk-I/O-Profil die CPU-Last indirekt:

| `disk_io_profile` | Gleichzeitige I/O-Ops | Empfohlen für |
|---|---|---|
| `hdd` | 1–4 | Klassische Festplatten |
| `ssd` | 32–64 | SATA/AHCI SSDs |
| `nvme` | 128–256 | NVMe-Laufwerke |
| `auto` (Default) | Automatisch erkannt | Die meisten Systeme |

---

## Vergleich mit AutoOrtho

| Dimension | XEarthLayer | AutoOrtho (ProgrammingDinosaur Fork) |
|---|---|---|
| Programmiersprache | Rust | Python (+ C-Pipeline in 2.0) |
| Prefetch-Strategie | Adaptiv (Ground/Cruise-Modi) | Einfach (Umgebungsbasiert) |
| Cache-Eviction | Automatisch (ältere Kacheln werden entfernt) | Automatisch (ältere Kacheln werden entfernt) |
| Plattform | Nur Linux | Windows, Linux, macOS |
| Simulator | Nur X-Plane 12 | X-Plane 11.50+ und 12 |
| Installation | Binary-Pakete oder aus Quellcode | Binary oder Python |
| Regionale Pakete | Separate DSF/TER-Pakete nötig | Integrierte Overlay-Downloads |
| GUI | Keine | Moderne GUI verfügbar |

XEarthLayer richtet sich an Linux-Nutzer, die maximale Streaming-Performance suchen und bereit sind, eine Rust-Build-Umgebung einzurichten. AutoOrtho bietet die breitere Plattformunterstützung und einfachere Einrichtung.

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
