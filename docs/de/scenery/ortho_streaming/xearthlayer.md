---
description: "XEarthLayer — Rust-basiertes Ortho-Streaming für X-Plane 12 unter Linux mit GPU-beschleunigter Kompression, adaptivem Prefetch, generierter Nachtbeleuchtung und Drei-Stufen-Cache."
---
# XEarthLayer

**XEarthLayer** ist eine in Rust geschriebene Alternative zu [AutoOrtho](../../glossary.md#autoortho) für das Streaming von [Orthofoto](../../glossary.md#orthofotos)-Texturen in X-Plane 12. Die Architektur ist von AutoOrtho beeinflusst, setzt jedoch auf eine performante Rust-Implementierung mit integrierter GPU-beschleunigter Kompression, adaptivem Prefetching, generierter Nachtbeleuchtung und einem Drei-Tier-Cache-System.

!!! note "Aktive Entwicklung"
    XEarthLayer ist ein junges Projekt in aktiver Entwicklung. Aktuelle Versionen laufen stabil, der Funktionsumfang kann sich zwischen Releases aber noch ändern.

## Funktionsweise

XEarthLayer nutzt ein **[FUSE](../../glossary.md#fuse-filesystem-in-userspace)-basiertes virtuelles Dateisystem** (siehe [Wie Ortho-Streaming funktioniert](how_streaming_works.md)), um Orthofoto-Texturen on demand bereitzustellen. Alle installierten Ortho-Pakete werden zu einem einzigen Mount, `zzXEL_ortho`, im Custom-Scenery-Ordner zusammengefasst; Overlay-Pakete werden in `yzXEL_overlay` verlinkt. Beim Zugriff auf eine Kachel durch X-Plane wird das Satellitenbild vom konfigurierten Kartenanbieter heruntergeladen, in das [DDS](../../glossary.md#dds-directdraw-surface)-Format (BC1/BC3) komprimiert und über das VFS an den Simulator ausgeliefert. Alle anderen Dateien (DSF, TER) werden unverändert aus dem Paket durchgereicht.

### DDS-Komprimierungs-Backends

XEarthLayer bietet drei Backends für die DDS-Texturkomprimierung, konfigurierbar über `compressor` in der `[texture]`-Sektion von `config.ini`:

| Backend | Beschreibung |
|---|---|
| **ISPC** (Standard) | Intel-ISPC-SIMD-Komprimierung, 5–10× schneller als das Software-Backend; vorkompilierte Kernel enthalten |
| **GPU** | GPU-beschleunigte Komprimierung über wgpu/WGSL Compute Shaders (zur Laufzeit wählbar via `texture.compressor = gpu`) |
| **Software** | Pure-Rust-Fallback, keine externen Abhängigkeiten |

Das GPU-Backend lagert die BC1/BC3-Komprimierung über Compute Shaders auf die Grafikkarte aus und entlastet so die CPU für X-Plane. Lohnend ist das auf Systemen mit integrierter und dedizierter GPU — etwa eine AMD-Radeon-iGPU auf einem Ryzen-Prozessor neben einer dedizierten NVIDIA-Karte —, auf denen die integrierte GPU die DDS-Komprimierung übernimmt, während die dedizierte GPU X-Plane rendert. Auf Systemen mit nur einer GPU konkurriert GPU-Encoding mit dem Simulator um dieselbe Karte; XEarthLayer protokolliert dann eine Warnung, und der Setup-Wizard bleibt bei ISPC. Die Auswahl des Adapters erfolgt über `gpu_device` in der `[texture]`-Sektion von `config.ini`:

| Wert | Wirkung |
|---|---|
| `integrated` (Standard) | Integrierte GPU verwenden |
| `discrete` | Dedizierte GPU verwenden |
| *Name-Teilstring* | Auswahl nach Adapternamen (z.B. `Radeon`, `RTX 5090`) |

Mit `xearthlayer diagnostics` lassen sich alle verfügbaren GPU-Adapter auflisten (unter Linux werden nur Vulkan-Adapter gelistet; Systeme, die ausschließlich OpenGL bieten, fallen auf ISPC zurück).

### Drei-Tier-Cache

XEarthLayer verwendet eine dreistufige Cache-Hierarchie:

- **Memory-Cache**: Zwischenpuffer im Arbeitsspeicher
- **DDS-Disk-Cache**: Kodierte DDS-Kacheln werden persistent auf Disk gespeichert und bilden die eigentliche Vorhalteschicht, sodass bei erneutem Besuch kein Re-Encoding nötig ist. Budget-Aufteilung konfigurierbar über `cache.dds_disk_ratio` (Standard 60:40 DDS zu Chunks; bei aktiver Nachtbeleuchtung bezogen auf die nach deren 5% verbleibenden 95%)
- **Chunk-Disk-Cache**: Rohe heruntergeladene Bild-Chunks

Wird die konfigurierte Cache-Größe erreicht, werden ältere Kacheln automatisch entfernt, um Platz für neue zu schaffen. Der Setup-Wizard dimensioniert den Disk-Cache dynamisch (Standard 25% des freien Speichers, Untergrenze 10 GB) und leitet das Memory-Cache-Budget aus dem verfügbaren RAM ab. Der Cache liegt standardmäßig in `~/.cache/xearthlayer/`; empfohlen ist über `cache.directory` eine schnelle NVMe oder SSD, die nicht das Systemlaufwerk ist. Kacheln mit fehlgeschlagenen Chunk-Downloads werden an X-Plane ausgeliefert, aber nicht gecacht.

### Adaptives Prefetch

XEarthLayers **adaptives Prefetching** stellt Szenerie vor dem Flugzeug in die Warteschlange, bevor X-Plane sie anfordert. Der Prefetch-Bereich wandert mit dem Flugzeug. Am Boden ist er ein Quadrat der Kantenlänge `box_extent` und liegt zentriert auf dem Flugzeug; im Reiseflug wächst er mit der Bodengeschwindigkeit bis `box_extent` und verschiebt sich in Flugrichtung. Prefetch läuft in **einer eigenen Spur** und tritt hinter X-Planes Kachelanfragen zurück, sodass es diese nie verzögert; außerdem pausiert es beim Laden der Szenerie, im Replay oder wenn die Telemetrie ausbleibt. Prefetch ist standardmäßig aktiv; `prefetch.enabled = false` oder `xearthlayer run --no-prefetch` schaltet es ab.

### Nachtbeleuchtung

Die regionalen Pakete enthalten Nacht-Rezepte, aus denen XEarthLayer die beleuchteten Texturen (`*_LIT.dds`) erzeugt, die X-Plane nachts anfordert — so bleiben Städte auf Ortho-Szenerie auch dort beleuchtet, wo X-Planes Autogen-Lichter nicht hinreichen. Die Texturen entstehen aus den Lit-Grafiken der lokalen X-Plane-Installation und NASA-VIIRS-Nachtlichtdaten; in der Nähe des Flugzeugs schaltet sich die Lichtschicht ab, dort übernehmen X-Planes eigene 3D-Lichter. Die Nachtbeleuchtung ist standardmäßig aktiv (`night.enabled`) und beansprucht 5% des Disk-Caches.

## Kartenquellen

XEarthLayer unterstützt folgende Kartenanbieter (Auswahl über `provider.type` oder im Setup-Wizard):

- Bing Maps (Standard)
- Google über GO2 (öffentliche Tile-Server, kein API-Key)
- Google Maps API (kostenpflichtiger API-Key)
- Apple Maps
- ArcGIS
- MapBox (Access-Token erforderlich)
- USGS (nur USA)

## Systemanforderungen

| Anforderung | Empfehlung |
|---|---|
| Betriebssystem | Linux x86_64 mit FUSE (vorkompilierte Binaries: glibc 2.34 oder neuer); macOS auf Apple Silicon mit macFUSE |
| Simulator | X-Plane 12 |
| GPU | 8 GB VRAM Minimum, 16+ GB empfohlen (für das X-Plane-Rendering) |
| Internetverbindung | ≥ 800 Mbps empfohlen |
| Speicher | SSD/NVMe für Disk-Cache |
| Build-Umgebung | Rust über rustup und FUSE-3-Header (nur bei Build aus Quellcode) |

!!! note "Plattformen"
    XEarthLayer läuft unter Linux und unter macOS (Apple Silicon). Einen Windows-Build gibt es nicht.

## Installation

Release-Builds stehen auf der [GitHub Releases-Seite](https://github.com/samsoir/xearthlayer/releases) als `.deb` (Debian/Ubuntu), `.rpm` (Fedora/RHEL) und `x86_64-linux.tar.gz`-Tarball bereit; unter Arch wird aus dem AUR gebaut. Pre-Releases erscheinen für Linux nur als Tarball.

```bash
# Im Download-Verzeichnis ausführen. Debian/Ubuntu: .deb von der Releases-Seite installieren
sudo dpkg -i xearthlayer_*_amd64.deb

# Andere Distributionen: Tarball nach ~/.local/bin entpacken
tar xzf xearthlayer-v*-x86_64-linux.tar.gz
mkdir -p ~/.local/bin
mv xearthlayer ~/.local/bin/
```

Alternativ lässt sich XEarthLayer aus dem Quellcode bauen. Rust sollte über [rustup](https://rustup.rs) installiert werden, da Distributionspakete meist zu alt sind; rustup übernimmt die im Repository festgelegte Toolchain-Version automatisch:

```bash
sudo apt install libfuse3-dev   # Fedora: sudo dnf install fuse3-devel
git clone https://github.com/samsoir/xearthlayer.git
cd xearthlayer
make install                    # Baut und installiert nach ~/.local/bin (GPU-Backend enthalten)
```

!!! warning "Umstieg von der vorherigen Paketgeneration"
    Die aktuelle Bibliothek ist eine neu gebaute Welt mit neuen Regionscodes. Alte und neue Pakete überlappen sich und dürfen nicht parallel installiert sein. Alle alten Pakete müssen **vor** der Installation neuer Pakete entfernt werden — auch bevor der Setup-Wizard den Paketmanager anbietet. Nach dem Aktualisieren des Programms ausführen:

    ```bash
    xearthlayer config upgrade
    xearthlayer packages remove --all --force
    xearthlayer packages remove --all --type overlay --force
    ```

Anschließend den Setup-Wizard starten:

```bash
xearthlayer setup
```

Der Setup-Wizard führt durch den [Custom Scenery](../../glossary.md#custom-scenery)-Ordner von X-Plane, den Paket-Speicherort, den Bildanbieter, die Cache-Dimensionierung und das Encoding-Backend (inklusive GPU-Adapter-Auswahl), erkennt SimHeaven X-World Pro und bietet zum Schluss an, den Paketmanager zu öffnen.

XEarthLayer folgt den XDG-Konventionen:

| Was | Standardpfad |
|---|---|
| Konfiguration | `~/.config/xearthlayer/config.ini` |
| Kachel-Cache | `~/.cache/xearthlayer/` |
| Pakete | `~/.local/share/xearthlayer/packages` |
| Logs | `~/.local/state/xearthlayer/` |

Temporäre Paket-Downloads landen in `~/.cache/xearthlayer/tmp` (nicht im System-`/tmp`, das oft RAM-basiert ist). Installationen mit dem älteren Layout unter `~/.xearthlayer` werden beim ersten Start automatisch migriert: Nur `config.ini` wird kopiert, Pakete und Cache bleiben an ihrem Ort, und deren alte Pfade werden in die neue Konfiguration eingetragen. Mit `xearthlayer migrate` lassen sich die Speicherorte anschließend überprüfen.

## Verwendung

XEarthLayer muss vor X-Plane gestartet werden, damit das virtuelle Dateisystem gemountet wird:

```bash
# Standard-Start
xearthlayer

# Start mit Cache-Vorwärmen für einen bestimmten Flughafen
xearthlayer run --airport KJFK
```

Position, Kurs und Geschwindigkeit des Flugzeugs bezieht XEarthLayer automatisch über die **X-Plane Web API** (Port 8086) — eine Konfiguration in X-Plane ist nicht nötig, solange die Web API nicht deaktiviert ist. Ein abweichender Port wird über `prefetch.web_api_port` gesetzt. Ohne Web API leitet XEarthLayer die Position aus den FUSE-Zugriffsmustern ab.

XEarthLayer sollte erst beendet werden, nachdem X-Plane geschlossen wurde — mit `q` im Dashboard oder Strg+C. Wird XEarthLayer bei laufendem X-Plane beendet, stürzt der Simulator ab.

## Regionale Pakete

XEarthLayer benötigt separate **[DSF](../../glossary.md#dsf-distribution-scenery-format)/TER-Pakete** (Distribution Scenery Format / Terrain), die die [Mesh](../../glossary.md#mesh)-Daten und Terrain-Definitionen für die jeweiligen Regionen enthalten. Die Bibliothek deckt die Welt in 17 Regionen ab (insgesamt rund 161 GB, Antarktis noch nicht verfügbar). Installieren, Aktualisieren und Entfernen übernimmt der interaktive **Paketmanager** im Terminal:

```bash
# Paketmanager öffnen (Tabs Local, Library, Progress, Settings)
xearthlayer packages

# Oder per Kommandozeile: eine oder mehrere Regionen installieren
xearthlayer packages install eu-west na-canada

# Installierte Pakete aktualisieren
xearthlayer packages update --all
```

Regionscodes sind hierarchisch aufgebaut (`EU-WEST`, `NA-CANADA-EAST`, `AS-CHINA-MONGOLIA` …); ein Präfix wählt alle darunterliegenden Pakete aus, `na-canada` installiert also beide Hälften Kanadas. Passende Overlay-Pakete (Straßen, Gebäude) werden nur dann zusammen mit den Ortho-Paketen installiert, wenn `packages.auto_install_overlays = true` gesetzt ist (Standard `false`). Downloads laufen parallel (`packages.concurrent_downloads`, 1–10, Standard 5), und das nächste Paket wird bereits heruntergeladen, während das vorherige installiert wird. Neue Pakete lassen sich bei laufendem XEarthLayer installieren und werden beim nächsten Start genutzt; Aktualisieren und Entfernen werden währenddessen abgelehnt.

Bei Nutzung von SimHeaven X-World Pro wird `packages.xworld_pro = true` gesetzt: XEarthLayer lässt dann auf den von X-World Pro abgedeckten Kontinenten die eigenen Overlays weg und prüft beim Start die Reihenfolge in `scenery_packs.ini`. `packages.disable_overlays = true` unterdrückt alle XEarthLayer-Overlays, ohne sie zu löschen.

Die Pakete stammen aus dem [XEarthLayer Regional Scenery Repository](https://github.com/samsoir/xearthlayer-regional-scenery) und werden mit OXO (Ortho4 XEarthLayer Orchestrator) erzeugt, einer Ortho4XP-basierten Build-Pipeline.

## CPU-Tuning

Auch mit dem effizienten ISPC-Backend bleibt die DDS-Komprimierung CPU-intensiv. XEarthLayer leitet seine interne Parallelität (Download-, Encoding- und Disk-I/O-Pools) aus der Zahl der logischen Kerne ab; diese Pool-Größen sind nicht konfigurierbar. Ältere Schlüssel wie `cpu_concurrent` oder `max_concurrent_jobs` in der `[executor]`-Sektion sind wirkungslos und werden von `xearthlayer config upgrade` entfernt.

!!! tip "GPU-Encoding als Alternative"
    Für Systeme mit einer zweiten GPU siehe [DDS-Komprimierungs-Backends](#dds-komprimierungs-backends).

### Das Problem

X-Plane ist stark Mainthread-gebunden. Wenn XEarthLayer alle Kerne sättigt, kommt es zu:

- **Thread-Überbelegung**: Mehr aktive Threads als verfügbare Kerne erzwingen ständige Context-Switches
- **Hyperthreading-Limitierung**: Threads auf demselben physischen Kern teilen sich Ausführungseinheiten, zusätzliche logische CPUs bringen daher nicht den Durchsatz zusätzlicher physischer Kerne
- **X-Plane-Stuttering**: Die Frametime steigt, weil der X-Plane-Mainthread um CPU-Zeit konkurriert

### Relevante Einstellungen

Zwei Einstellungen in `~/.config/xearthlayer/config.ini` steuern, wie viel CPU XEarthLayer beansprucht:

| Einstellung | Sektion | Standard | Funktion |
|---|---|---|---|
| `threads` | `[generation]` | Hälfte der CPU-Kerne | Worker-Threads für Tile-Generierung |
| `capacity_share` | `[prefetch]` | `0.35` (0.05–0.50) | Prefetch-Kapazität als Anteil der Kapazität für On-Demand-Anfragen |

**Faustregel**: Bei parallelem X-Plane-Betrieb sollte `threads` die Hälfte der *physischen* Kerne nicht überschreiten. Kostet Prefetch Framerate, wird `capacity_share` gesenkt — Prefetch konkurriert zwar nicht mehr mit X-Planes Kachelanfragen, aber weiterhin mit dem Simulator um CPU-Zeit.

---

## Vergleich mit AutoOrtho

| Dimension | XEarthLayer | AutoOrtho (ProgrammingDinosaur Fork) |
|---|---|---|
| Programmiersprache | Rust (+ optionale GPU Compute Shaders) | Python + native C-Pipeline |
| DDS-Komprimierung | ISPC SIMD (Standard) oder GPU-beschleunigt | C-basiert mit dediziertem Decode-Pool |
| Prefetch-Strategie | Geschwindigkeitsskalierte Box vor dem Flugzeug, eigene Prefetch-Spur | Positionsbasiert, optional entlang der SimBrief-Route |
| Cache-Eviction | Automatisch (ältere Kacheln werden entfernt) | Automatisch (ältere Kacheln werden entfernt) |
| X-Plane 12 Features | Regionale Mesh- und Terrain-Pakete (mit OXO erzeugt) sowie generierte Nachtbeleuchtung | Ja (Seasons integriert) |
| Plattform | Linux, macOS (Apple Silicon) | Windows, Linux, macOS (Apple Silicon) |
| Simulator | X-Plane 12 (X-Plane 11 ungetestet) | X-Plane 11.50+ und 12 |
| Installation | `.deb`/`.rpm`/Tarball, AUR oder aus Quellcode | Binary-Installer oder Python |
| Regionale Pakete | Integrierter Paketmanager (TUI und CLI) | Integrierte Overlay-Downloads |
| GUI | CLI mit Live-Dashboard und Paketmanager-TUI | GUI mit Konfigurationspanels |

XEarthLayer richtet sich an Linux-Nutzer, die maximale Streaming-Performance durch GPU-Offloading, eine Prefetch-Spur, die X-Plane nie blockiert, und generierte Nachtbeleuchtung suchen. AutoOrtho bietet breitere Plattformunterstützung einschließlich Windows und eine einfachere GUI-basierte Einrichtung.

---

## Weiterführende Kapitel

| Thema | Seite | Schwerpunkt |
|---|---|---|
| XPME | [XPME](xpme.md) | Closed-Source-Freemium-Alternative, hochauflösende Stufe kostenpflichtig |
| AutoOrtho | [AutoOrtho](autoortho.md) | Alternative Streaming-Lösung mit breiterer Plattformunterstützung |
| Ortho4XP | [Ortho4XP](../orthophotography/ortho4xp.md#pakete-fur-ortho-streaming-bauen) | Bau der Mesh-only-DSF/TER-Pakete, auf die dieser Layer aufsetzt |
| Statisch + Streaming | [Statisch + Streaming](static_plus_streaming.md) | Kombination lokaler Kacheln mit Streaming |
| Szenerie-Komponenten | [Wie X-Plane die Welt aufbaut](../aufbau_quellen/scenery_components.md) | scenery_packs.ini-Ladereihenfolge |
| Kernel-Tuning | [Kernel-Tuning](../../linux/system/systemtuning.md) | CPU-Governor, IRQ-Pinning, Scheduler-Tuning |
| Dateisystem | [Dateisystem](../../linux/optimizations/filesystem.md) | NVMe/SSD-Optimierung für Cache-Performance |

---

## Quellen

- [GitHub Repository](https://github.com/samsoir/xearthlayer)
- [Konfigurationsreferenz](https://github.com/samsoir/xearthlayer/blob/main/docs/configuration.md)
- [Paketverwaltung](https://github.com/samsoir/xearthlayer/blob/main/docs/package-management.md)
- [XEarthLayer Website](https://xearthlayer.app/)
- [Regionale Szenerie-Pakete](https://github.com/samsoir/xearthlayer-regional-scenery)
