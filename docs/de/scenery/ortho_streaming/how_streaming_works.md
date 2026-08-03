---
description: "Wie Ortho-Streaming in X-Plane funktioniert: die DSF→.ter→DDS-Texturkette, FUSE als virtuelles Dateisystem, Streaming-Pipeline, Cache-Architektur und Linux-Vorteile."
---
# Wie Ortho-Streaming funktioniert

Ortho-Streaming ersetzt X-Planes Standard-Bodentexturen durch Satellitenbilder — zur Laufzeit heruntergeladen statt vorab generiert und lokal gespeichert. Tools wie [AutoOrtho](autoortho.md) und [XEarthLayer](xearthlayer.md) erreichen dies, indem sie X-Planes Texturanfragen über ein virtuelles [FUSE](../../glossary.md#fuse-filesystem-in-userspace)-Dateisystem abfangen und an Online-Kartenanbieter weiterleiten. Diese Seite erklärt die gemeinsame technische Architektur beider Tools.

## X-Planes Textur-Ladekette

[X-Plane](../../glossary.md#x-plane) unterteilt die Welt in 1° × 1°-Kacheln, gespeichert als [DSF](../../glossary.md#dsf-distribution-scenery-format)-Dateien (Distribution Scenery Format). Texturen werden über eine dreistufige Referenzkette geladen:

1. **DSF-Datei** — enthält Terrain-Typ-Pfade als indizierte Referenzen. DSF-Befehle verweisen auf Terrain-Typen nur per Indexnummer.
2. **`.ter`-Datei** (Terrain Type) — eine Textdatei, die das Rendering eines Terrain-Patches steuert. Wichtige Direktiven:
    - `BASE_TEX <Dateiname>` — primäre Terrain-Textur (Pflicht)
    - `LIT_TEX <Dateiname>` — Nacht-Overlay
    - `LOAD_CENTER <lat> <lon> <size_m> <tex_size_px>` — entfernungsabhängiges Laden
3. **[DDS](../../glossary.md#dds-directdraw-surface)-Textur** — die eigentlichen Bilddaten, referenziert durch die `.ter`-Datei. Pfade werden relativ zum Speicherort der `.ter`-Datei aufgelöst.

Die `LOAD_CENTER`-Direktive ermöglicht **entfernungsabhängige Auflösungsverwaltung**: Texturen werden in variabler Auflösung geladen, abhängig von der Flugzeugentfernung — volle Auflösung nur in der Nähe des angegebenen Zentrums. Bei größerer Entfernung reduziert der Simulator die Texturauflösung progressiv — das spart VRAM ohne sichtbaren Qualitätsverlust in der Höhe. Das DDS-Format ist hier entscheidend, weil seine Mipmap-Struktur partielles Laden erlaubt; PNG würde vollständige Dekompression mit anschließender CPU-seitiger Skalierung erfordern.

Streaming-Tools nutzen diese Kette aus: Die `.ter`-Dateien verweisen auf Texturpfade innerhalb eines FUSE-Mounts, sodass jeder Texturlesevorgang zur Streaming-Gelegenheit wird.

??? abstract "Technischer Hintergrund: .ter vs .pol für Orthophotos"
    X-Plane unterstützt zwei Methoden zur Anwendung von Orthophotos:

    - **`.ter` Base-Mesh-Ersetzung**: Ersetzt die Terrain-Mesh-Texturen direkt. Statisches Paging, keine Mesh-Duplizierung. Diese Methode verwenden AutoOrtho und XEarthLayer.
    - **`.pol` Draped-Polygon-Overlay**: Projiziert Orthophotos auf das bestehende Mesh. Wird nur in Flugzeugnähe gerendert, verursacht permanenten CPU-Overhead und verdoppelt den VRAM-Verbrauch. Für großflächige Abdeckung nicht geeignet.

    Laminar Research empfiehlt `.ter`-Ersetzung für Orthophoto-Szenerie.

---

## FUSE: Das virtuelle Dateisystem

[FUSE](../../glossary.md#fuse-filesystem-in-userspace) (Filesystem in Userspace) ist die Brücke zwischen X-Planes Dateizugriffen und den Streaming-Tools. Es besteht aus drei Komponenten:

- **`fuse.ko`** — Kernel-Modul, das den Dateisystemtyp `fuse` bei Linux' VFS-Schicht registriert
- **`libfuse`** — Userspace-Bibliothek mit der API für Dateisystemoperationen
- **`fusermount`** — Mount-Utility für unprivilegierte Mounts (wendet automatisch `nosuid` und `nodev` an)

Die Kommunikation zwischen Kernel und Userspace-Daemon läuft über das `/dev/fuse` Character Device.

### Wie Streaming-Tools FUSE nutzen

1. Das Streaming-Tool mountet ein virtuelles Dateisystem im [Custom-Scenery](../../glossary.md#custom-scenery)-Verzeichnis
2. Szenerie-Pakete (DSF + `.ter`-Dateien) referenzieren Texturen an Pfaden innerhalb dieses FUSE-Mounts
3. X-Plane lädt eine DSF → folgt der `.ter`-Kette → der Texturpfad zeigt ins FUSE-Verzeichnis
4. Der FUSE-Daemon fängt den `read()`-Aufruf ab
5. Der Dateiname wird geparst, um Kachelkoordinaten, Kartenanbieter und Zoom-Level zu extrahieren
6. Die Anfrage wird an das Cache-/Download-System statt an ein reales Dateisystem geroutet

Beide Tools erfordern, dass `user_allow_other` in `/etc/fuse.conf` aktiviert ist, damit X-Plane (als separater Prozess) auf den FUSE-Mount zugreifen kann.

??? abstract "Technischer Hintergrund: FUSE-Request-Lebenszyklus"
    Wenn X-Plane eine Datei auf einem FUSE-Mount liest, durchläuft die Anfrage diesen Weg:

    **Phase 1 — Request-Initiierung:**

    1. X-Plane ruft den `read()`-Syscall auf
    2. Kernel-VFS routet zum FUSE-Handler
    3. Die Anfrage wird in die Pending-Queue gestellt
    4. Der Userspace-Daemon wird aufgeweckt

    **Phase 2 — Userspace-Verarbeitung:**

    1. Der FUSE-Daemon liest von `/dev/fuse`
    2. Die Anfrage wird von der Pending- in die Processing-Queue verschoben
    3. Der Daemon führt die eigentliche Arbeit aus (Satellitenbild herunterladen, nach DDS konvertieren)

    **Phase 3 — Antwort:**

    1. Der Daemon schreibt das Ergebnis zurück nach `/dev/fuse`
    2. Der Kernel weckt den wartenden X-Plane-Thread
    3. Die Daten werden an X-Plane zurückgegeben

    **Context-Switch-Overhead:** Eine native Dateisystemoperation erfordert 2 Context-Switches; FUSE erfordert 4. Für Ortho-Streaming ist dieser Overhead irrelevant — der Engpass ist die Netzwerklatenz (50–200 ms), nicht die Dateisystemlatenz (Mikrosekunden).

### FUSE-Congestion-Engpass

Der Linux-FUSE-Treiber begrenzt gleichzeitige asynchrone Anfragen über zwei Kernel-Parameter:

| Parameter | Standard | Wirkung |
|-----------|----------|---------|
| `max_background` | 12 | Maximale Anzahl gleichzeitiger Hintergrund-Anfragen (asynchron). Neue Hintergrund-Anfragen blockieren, wenn das Limit erreicht ist. |
| `congestion_threshold` | 9 (¾ von `max_background`) | Oberhalb dieses Werts reduziert der Kernel Readahead und überspringt opportunistisches Writeback — spekulative I/O wird gedrosselt, bevor das harte Limit greift. |

X-Plane lädt DSF-Kacheln auf Hintergrund-Threads und kann an DSF-Kachelgrenzen viele Tiles parallel anfordern. Seit X-Plane 12.4 mit Multi-Thread-Szenerieverarbeitung verarbeitet der Simulator mehr Tiles gleichzeitig — was den Druck auf FUSE an Kachelgrenzen deutlich erhöht.

Die niedrigen FUSE-Standardwerte erzeugen einen Engpass: Nur 12 Hintergrund-Anfragen können gleichzeitig in Bearbeitung sein. Ist diese Obergrenze erreicht, blockieren weitere Hintergrund-Lesezugriffe, bis ein Slot frei wird. Gleichzeitig reduziert `congestion_threshold` (9) bereits vorher das Kernel-Readahead — der effektive Durchsatz sinkt also schon vor dem harten Limit.

!!! warning "Typische Symptome"
    - Reproduzierbare Frame-Einbrüche an DSF-Kachelgrenzen (alle 1° Breite/Länge)
    - GPU- und CPU-Auslastung bleiben während des Rucklers niedrig
    - Die Streaming-Pipeline könnte ~50 Tiles/Sekunde verarbeiten — erreicht diesen Durchsatz aber nie

**Abhilfe:**

`max_background` lässt sich über einen lokalen Crate-Patch auf 64–128 anheben — ohne Kernel-Modifikation. Das FUSE-Kernel-Modul akzeptiert Werte bis 65535 für `max_background` (unprivilegierte Prozesse bis `max_user_bgreq`, Standard 256); nur die Userspace-Bibliothek muss gepatcht werden. Ein entsprechender [Patch wird in XEarthLayer Issue #67](https://github.com/samsoir/xearthlayer/issues/67) verfolgt.

??? abstract "Technischer Hintergrund: Warum das passiert"
    Das Rust-Crate `fuse3`, das XEarthLayer verwendet, kompiliert diese Limits als Konstanten:

    ```rust
    pub const DEFAULT_MAX_BACKGROUND: u16 = 12;
    pub const DEFAULT_CONGESTION_THRESHOLD: u16 = DEFAULT_MAX_BACKGROUND * 3 / 4; // = 9
    ```

    Diese Werte entsprechen den Linux-Kernel-Standardwerten, sind aber über die API des Crates nicht zur Laufzeit konfigurierbar — ein lokaler Crate-Patch ist erforderlich.

    AutoOrtho v2.1.1 ([ProgrammingDinosaur-Fork](https://github.com/ProgrammingDinosaur/autoortho4xplane)) unterliegt denselben Kernel-Standardwerten. Es nutzt mfusepy, das sowohl libfuse2 als auch libfuse3 unterstützt. Beide libfuse-Versionen erlauben `max_background` als Mount-Option (`-o max_background=N`) oder programmatisch im `init()`-Callback — AutoOrtho nutzt jedoch keinen der beiden Wege und bleibt beim Kernel-Default von 12.

---

## Die Streaming-Pipeline

Wenn X-Plane eine Terrain-Textur benötigt, sieht der vollständige Anfrageablauf so aus:

```
X-Plane lädt DSF-Kachel
  → DSF referenziert .ter-Terrain-Definition (per Index)
    → .ter spezifiziert BASE_TEX mit LOAD_CENTER
      → Texturpfad zeigt ins FUSE-Mount
        → FUSE fängt read() ab
          → Dateiname geparst → Cache-Lookup
            → L1 Memory-Cache: Treffer → sofortige Rückgabe
            → L2 Disk-Cache: Treffer → laden, nach L1 befördern, zurückgeben
            → L3 Network: Download vom Kartenanbieter
              → JPEG/PNG-Tiles herunterladen
                → Tiles zusammenfügen (Stitching)
                  → DDS-Kompression (BC1/BC3) mit Mipmaps
                    → In L1 + L2 Cache speichern
                      → DDS-Bytes über FUSE read() zurückgeben
                        → Kernel liefert Daten an X-Plane
                          → X-Plane lädt Textur auf GPU hoch
```

### Cache-Architektur

Beide Streaming-Tools verwenden einen mehrstufigen Cache, um redundante Downloads zu minimieren:

| Ebene | Medium | Verhalten |
|-------|--------|-----------|
| L1 — Memory | RAM | Häufig verwendete Tiles, LRU-Eviction bei konfiguriertem Limit |
| L2 — Disk | SSD | Persistente Speicherung, automatische Eviction bei Erreichen des Größenlimits |
| L3 — Network | Internet | Download vom Kartenanbieter bei Cache-Miss |

Ein aufgewärmter Cache (gefüllt nach dem ersten Besuch einer Region) sorgt dafür, dass nachfolgende Flüge nahezu verzögerungsfrei laden — Tiles werden von SSD oder RAM geliefert, ohne Netzwerkanfragen.

### DDS-Kompression

Das DDS-Format nutzt GPU-native Blockkompression:

- **BC1 (DXT1)**: 4 Bit/Pixel, nur RGB. Standard-Kompression für Ortho-Texturen. 8:1 Kompressionsrate.
- **BC3 (DXT5)**: 8 Bit/Pixel, RGBA mit Alphakanal. Für Texturen mit Transparenz (Wassergrenzen, Terrain-Übergänge).

Beide Formate enthalten **Mipmaps** — progressiv halbierte Kopien derselben Textur (4096 → 2048 → 1024 → 512 → ...). X-Planes `LOAD_CENTER`-Mechanismus fordert nur das Mipmap-Level an, das zur Flugzeugentfernung passt. AutoOrtho nutzt dies aus, indem **nur die tatsächlich angeforderten Mipmap-Level** heruntergeladen und gespeichert werden — das reduziert sowohl Download-Volumen als auch Speicherverbrauch drastisch gegenüber vorgenerierten Ansätzen.

---

## Mehrwert unter Linux

FUSE ist seit 2005 Teil des Linux-Kernels. Kein Drittanbieter-Treiber, keine Kernel-Erweiterung, keine Administrator-Rechte zum Mounten erforderlich — `/dev/fuse` ist universell auf allen Distributionen verfügbar. Der einzige Konfigurationsschritt: `user_allow_other` in `/etc/fuse.conf` auskommentieren.

| Aspekt | Linux (FUSE) | Windows (WinFSP/Dokan) |
|--------|-------------|----------------------|
| Kernel-Integration | Mainline-Kernel-Modul | Drittanbieter-Treiber, separate Installation |
| Installation | Keine — bereits im Kernel | WinFSP- oder Dokan-Installer (Admin-Rechte erforderlich) |
| Antivirus-Interferenz | Keine | Windows Defender scannt FUSE-Mounts → I/O-Overhead |
| Symlinks | Nativ, trivial | Erhöhte Rechte oder Developer Mode erforderlich |
| Stabilität | Ausgereift, intensiv getestet | AutoOrtho-Dokumentation warnt vor „filesystem variations" und „intrusive malware detection" |

XEarthLayer ist eine direkte Konsequenz dieses Linux-Vorteils: Die Rust-Implementierung mit async Tokio-Runtime nutzt das `fuse3`-Crate für saubere, native FUSE-3-Integration — ohne die plattformübergreifenden Abstraktionsschichten, die eine Windows-Portierung erfordern würde. Zusammen mit X-Plane 12s nativem Vulkan-Renderer auf Linux läuft der gesamte Stack ohne Kompatibilitätsschichten.

---

## Wenn das Laden länger dauert

Ortho-Streaming liefert Satellitenbilder in Echtzeit — doch manchmal erscheinen Tiles sichtbar verzögert oder unscharfe Texturen bleiben länger als erwartet bestehen. Die häufigsten Gründe:

| Ursache | Erklärung | Abhilfe |
|---------|-----------|---------|
| Leerer Cache (Erstbesuch) | Für diese Region existieren keine gecachten Tiles. Jede Textur löst einen Netzwerk-Download aus. | Die Region einmal in Reiseflughöhe überfliegen, um den Cache aufzuwärmen. XEarthLayer unterstützt `--airport`-Vorwärmung. |
| Langsames oder überlastetes Netzwerk | Kartenserver antworten langsam oder die lokale Bandbreite reicht nicht aus. | Verbindungsgeschwindigkeit prüfen. Ggf. Kartenanbieter wechseln. |
| Einstellungen geändert | Änderungen am Zoom-Level oder Kartenanbieter machen bestehende Cache-Einträge ungültig. | Nach Einstellungsänderungen mit langsameren Ladezeiten rechnen, bis sich der Cache neu füllt. |
| Rate Limiting (HTTP 429) | Kartenanbieter drosseln Clients, die in kurzer Zeit zu viele Anfragen senden. | Auf einen anderen Kartenanbieter wechseln oder VPN nutzen. AutoOrtho protokolliert dies als `HTTP 429: Too Many Requests`. |
| Hoher Zoom-Level | Höherer Zoom bedeutet exponentiell mehr Tiles pro Fläche. ZL18 benötigt 4× mehr Tiles als ZL17. | Maximalen Zoom-Level reduzieren, wenn das Laden nicht mitkommt. |
| CPU-Konkurrenz | DDS-Kompression konkurriert mit X-Plane um CPU-Zeit, was beides verlangsamt. | Worker-Threads begrenzen (XEarthLayer: `cpu_concurrent`, AutoOrtho: Konfiguration). Siehe [XEarthLayer CPU-Tuning](xearthlayer.md#cpu-tuning). |
| Schneller Tiefflug | Niedrige Höhe + hohe Geschwindigkeit erfordern mehr Tiles pro Sekunde als Reiseflug in großer Höhe. | Erwartetes Verhalten — der Cache füllt sich im Flug. Prefetching hilft (besonders XEarthLayers adaptive Modi). |
| FUSE-Congestion | Der FUSE-Treiber begrenzt gleichzeitige Hintergrund-Anfragen standardmäßig auf 12. An DSF-Grenzen erreichen parallele Kachelanfragen diese Obergrenze — weitere Lesezugriffe blockieren. | FUSE-Userspace-Bibliothek patchen, um `max_background` anzuheben — siehe [FUSE-Congestion-Engpass](#fuse-congestion-engpass). |

!!! tip "Der Cache ist der beste Verbündete"
    Nach dem ersten Besuch einer Region laden nachfolgende Flüge nahezu vollständig aus dem Disk- oder Memory-Cache. Das anfängliche „langsame" Erlebnis ist ein einmaliger Aufwand pro Region und Zoom-Level.

---

## Weiterführende Kapitel

| Thema | Seite | Schwerpunkt |
|-------|-------|-------------|
| AutoOrtho | [AutoOrtho](autoortho.md) | Streaming-Konfiguration, Fork-Features, Ortho4XP-Vergleich |
| XPME | [XPME](xpme.md) | Closed-Source-Freemium-Alternative mit eigenen Basispaketen |
| XEarthLayer | [XEarthLayer](xearthlayer.md) | Rust-basiertes Streaming mit adaptivem Prefetch und CPU-Tuning |
| Statisch + Streaming | [Statisch + Streaming](static_plus_streaming.md) | Kombination lokaler Ortho4XP-Tiles mit Streaming |
| Ortho4XP | [Pakete für Ortho-Streaming bauen](../orthophotography/ortho4xp.md#pakete-fur-ortho-streaming-bauen) | Mesh-only-DSF/TER-Pakete für einen Streaming-Layer bauen |
| Szenerie-Komponenten | [Wie X-Plane die Welt aufbaut](../aufbau_quellen/scenery_components.md) | scenery_packs.ini-Ladereihenfolge und Schicht-Interaktion |
| Dateisystem | [Dateisystem](../../linux/optimizations/filesystem.md) | I/O-Optimierung für SSD-Cache-Performance |

---

## Quellen

- [DSF Usage In X-Plane](https://developer.x-plane.com/article/dsf-usage-in-x-plane/) — Laminar Research Developer Documentation
- [Terrain Type (.ter) File Format](https://developer.x-plane.com/article/terrain-type-ter-file-format-specification/) — Laminar Research Developer Documentation
- [Three Things You Need for Fast Orthophotos](https://developer.x-plane.com/2011/03/three-things-you-need-for-fast-orthophotos/) — Laminar Research Developer Blog
- [FUSE — Linux Kernel Documentation](https://www.kernel.org/doc/html/next/filesystems/fuse/fuse.html) — Kernel.org
- [AutoOrtho Technical Details](https://kubilus1.github.io/autoortho/latest/details/) — AutoOrtho Project Documentation
- [XEarthLayer Repository](https://github.com/samsoir/xearthlayer) — GitHub
