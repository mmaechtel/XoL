# Research: Ortho-Streaming-Architektur in X-Plane 12

**Recherche-Datum:** 2026-02-21
**Ziel-Docs-Seite:** `docs/{lang}/scenery/ortho_streaming/how_streaming_works.md`
**Position in Navigation:** Ortho Streaming → erste Seite (vor AutoOrtho und XEarthLayer)

---

## 1. X-Planes Textur-Ladekette (gesichert, HIGH confidence)

### DSF → .ter → DDS

X-Plane teilt die Welt in 1° × 1°-Kacheln, gespeichert als DSF-Dateien (Distribution Scenery Format). Die Textur-Ladekette verläuft dreistufig:

1. **DSF-Datei** enthält ein DEFN/TERT-Atom mit Terrain-Typ-Pfaden (Index-basiert). DSF-Befehle referenzieren Terrain-Typen nur per Index-Nummer.

2. **`.ter`-Dateien** (Terrain Type) sind Textdateien, die das Rendering von Terrain-Patches steuern:
    - `BASE_TEX <dateiname>` — primäre Terrain-Textur (Pflicht)
    - `LIT_TEX <dateiname>` — Nacht-Overlay
    - `PROJECTED <h_scale> <v_scale>` — automatische Texturprojektion
    - `LOAD_CENTER <lat> <lon> <size_m> <tex_size_px>` — entfernungsabhängiges Laden

3. **DDS-Texturen** — die eigentlichen Bilddaten, referenziert durch die `.ter`-Datei. Pfade werden **relativ zur `.ter`-Datei** aufgelöst.

**Quelle:** [DSF Usage In X-Plane](https://developer.x-plane.com/article/dsf-usage-in-x-plane/), [Terrain Type (.ter) File Format](https://developer.x-plane.com/article/terrain-type-ter-file-format-specification/)

### LOAD_CENTER: Entfernungsabhängiges Laden

Die `LOAD_CENTER`-Direktive ermöglicht **entfernungsabhängige Auflösungsverwaltung**:
- Textur wird in variabler Auflösung geladen, abhängig von der Flugzeugentfernung
- Höchste Auflösung nur in der Nähe des angegebenen Zentrums
- Progressive Degradation bei größerer Entfernung
- Spart VRAM, da entfernte Texturen nicht in voller Auflösung gehalten werden
- DDS-Format wird empfohlen, weil „reloads at lower resolution are fast" — PNG erfordert volles Laden + CPU-Skalierung

**Quelle:** [Three Things You Need for Fast Orthophotos](https://developer.x-plane.com/2011/03/three-things-you-need-for-fast-orthophotos/)

### Ortho-Ansätze: .ter vs .pol

- **`.ter` Base-Mesh-Ersetzung**: Ersetzt das Terrain-Mesh mit Ortho-Texturen. Statisches Paging, kein Mesh-Duplikat. **Von AutoOrtho/XEarthLayer verwendet.**
- **`.pol` Draped Polygon Overlay**: Legt Ortho-Texturen über bestehendes Mesh. Nur nahe dem Flugzeug gerendert, permanenter CPU-Aufwand, verdoppelt VRAM. Nicht für große Flächen geeignet.

**Quelle:** [Three Things You Need for Fast Orthophotos](https://developer.x-plane.com/2011/03/three-things-you-need-for-fast-orthophotos/)

---

## 2. FUSE als Brücke (gesichert, HIGH confidence)

### Architektur

FUSE (Filesystem in Userspace) besteht aus drei Komponenten:

1. **`fuse.ko`** — Kernel-Modul, registriert die Dateisystem-Typen `fuse`, `fuseblk`, `fusectl` beim Linux-VFS
2. **`libfuse`** — Userspace-Bibliothek mit der API für Dateisystemoperationen
3. **`fusermount`** — Mount-Utility für unprivilegierte Mounts (automatisch `nosuid` und `nodev`)

Kommunikation zwischen Kernel und Userspace-Daemon über **`/dev/fuse`** Character Device.

**Quelle:** [FUSE — Linux Kernel Documentation](https://www.kernel.org/doc/html/next/filesystems/fuse/fuse.html)

### Vollständiger Request-Lebenszyklus

Wenn X-Plane eine Datei auf einem FUSE-Mount liest:

**Phase 1 — Request-Initiierung:**
1. X-Plane ruft `read()` syscall auf
2. Kernel-VFS routet zum FUSE-Handler (`fuse_read()`)
3. Request wird auf `fc->pending` Queue gestellt
4. Userspace-Daemon wird aufgeweckt

**Phase 2 — Userspace-Verarbeitung:**
1. FUSE-Daemon liest von `/dev/fuse` via `sys_read()`
2. Request wird von `fc->pending` entfernt, nach `fc->processing` verschoben
3. Daemon führt die eigentliche Arbeit aus (Satellitenbild herunterladen, DDS konvertieren)

**Phase 3 — Antwort:**
1. Daemon schreibt Ergebnis via `sys_write()` nach `/dev/fuse`
2. Kernel findet Request in `fc->processing`, weckt den wartenden X-Plane-Thread
3. Daten werden an X-Plane zurückgegeben

**Context-Switch-Overhead:**
- Natives Dateisystem: 2 Context-Switches pro Operation
- FUSE: 4 Context-Switches pro Operation
- **Für Ortho-Streaming irrelevant**: Bottleneck ist Netzwerk-Latenz (50–200ms), nicht Dateisystem-Latenz (Mikrosekunden)

**Quelle:** [FUSE — Linux Kernel Documentation](https://www.kernel.org/doc/html/next/filesystems/fuse/fuse.html), [To FUSE or Not to FUSE (USENIX FAST'17)](https://www.usenix.org/system/files/conference/fast17/fast17-vangoor.pdf)

### Wie AutoOrtho/XEarthLayer FUSE nutzen

1. Tool mountet ein virtuelles Dateisystem im Custom Scenery-Verzeichnis
2. Szenerie-Pakete (DSF + .ter Dateien) verweisen auf Texturen in diesem FUSE-Mount
3. X-Plane lädt DSF → folgt der .ter-Kette → Texturpfad resolves ins FUSE-Verzeichnis
4. FUSE-Daemon fängt den `read()`-Aufruf ab
5. Dateiname wird per Regex geparst: `{row}_{col}_{maptype}_{zoomlevel}.dds`
6. Request wird an Cache/Download-System geroutet statt ans echte Dateisystem

**AutoOrtho:** Python-basiert (refuse-Bibliothek, Fork von fusepy), `allow_other=True` damit X-Plane als separater Prozess zugreifen kann.
**XEarthLayer:** Rust-basiert, nutzt `fuse3` v0.8 als primäre FUSE-Bibliothek mit async Tokio-Runtime (`fuser` v0.14 nur für Legacy-Typdefinitionen). Kein Python-GIL → echte parallele FUSE-Request-Verarbeitung + async I/O.

**Beide Tools erfordern:** `user_allow_other` in `/etc/fuse.conf` muss aktiviert sein, damit X-Plane (als separater Prozess) auf den FUSE-Mount zugreifen kann.

**Quelle:** [AutoOrtho FUSE-Quellcode](https://github.com/kubilus1/autoortho/blob/main/autoortho/autoortho_fuse.py), [XEarthLayer GitHub](https://github.com/samsoir/xearthlayer)

---

## 3. Die Streaming-Pipeline (gesichert, HIGH confidence)

### Vollständiger Request-Flow

```
X-Plane lädt DSF-Kachel
  → DSF referenziert .ter-Terrain-Definition (per Index)
    → .ter spezifiziert BASE_TEX mit LOAD_CENTER
      → Texturpfad resolves ins FUSE-Mount
        → FUSE fängt read() ab
          → Dateiname wird geparst → Cache-Lookup
            → L1 Memory-Cache: Hit → sofortige Rückgabe
            → L2 Disk-Cache: Hit → laden, in L1 schieben, zurückgeben
            → L3 Network: Download von Kartenanbieter
              → JPEG/PNG-Tiles herunterladen
                → Tiles zusammenfügen (stitching)
                  → DDS-Kompression (BC1/BC3) mit Mipmaps
                    → In L1 + L2 cachen
                      → DDS-Bytes an FUSE read() zurückgeben
                        → Kernel liefert Daten an X-Plane
                          → X-Plane uploaded Textur an GPU (Vulkan)
```

### DDS-Format und Mipmap-Exploitation

- **BC1 (DXT1)**: 4 Bit/Pixel, nur RGB. Verwendet für Standard-Ortho-Texturen. 8:1 Kompressionsrate.
- **BC3 (DXT5)**: 8 Bit/Pixel, RGBA mit Alpha. Für Texturen mit Transparenz (Wassergrenzen, Terrain-Übergänge).

**AutoOrthos Schlüssel-Innovation — Sparse DDS Allocation:**
DDS-Dateien enthalten mehrere Kopien der gleichen Textur in progressiv halbierten Auflösungen (Mipmaps). Eine 4096×4096-Basistextur hat Mip-Level bei 2048, 1024, 512 usw. X-Planes LOAD_CENTER-Mechanismus fordert nur das Mipmap-Level an, das zur Flugzeugentfernung passt.

AutoOrtho nutzt dies aus: Statt alle Mipmap-Level zu speichern, werden **nur die tatsächlich angeforderten Levels** heruntergeladen und gespeichert. Das reduziert Download-Volumen und Speicherverbrauch dramatisch gegenüber Ortho4XP.

Wenn X-Plane `read()` mit bestimmtem Offset und Länge aufruft, berechnet AutoOrtho, welches Mipmap-Level angefragt wird, und holt nur das entsprechende Zoom-Level vom Satellitenanbieter.

**Quelle:** [AutoOrtho Approach](https://kubilus1.github.io/autoortho/latest/details/), [AutoOrtho Continued Approach](https://programmingdinosaur.github.io/autoortho4xplane/details/)

### Cache-Architektur

| Ebene | Medium | Verhalten |
|-------|--------|-----------|
| L1 — Memory | RAM | Häufig verwendete Tiles, LRU-Eviction bei Limit |
| L2 — Disk | SSD | Persistent, sparse DDS-Dateien, automatische Eviction bei Größenlimit |
| L3 — Network | Internet | Download von Kartenanbieter bei Cache-Miss |

---

## 4. Linux-Vorteile (gesichert, HIGH confidence)

### FUSE als natives Linux-Feature

- FUSE ist seit **Kernel 2.6.14 (2005)** im Linux-Kernel enthalten
- Kein Drittanbieter-Treiber, keine Kernel-Erweiterung, keine Admin-Rechte zum Mounten
- `/dev/fuse` universell verfügbar auf allen Distributionen
- Einzige Konfiguration: `user_allow_other` in `/etc/fuse.conf` auskommentieren

### Vergleich Linux FUSE vs Windows WinFSP/Dokan

| Aspekt | Linux (FUSE) | Windows (WinFSP/Dokan) |
|--------|-------------|----------------------|
| Kernel-Integration | Mainline seit 2005 | Drittanbieter-Treiber, separate Installation |
| Installation | Null — bereits im Kernel | WinFSP/Dokan installieren (Admin-Rechte) |
| Antivirus-Interferenz | Keine | Windows Defender scannt FUSE-Mounts → I/O-Overhead |
| Symlinks | Nativ, trivial | Erhöhte Rechte oder Developer Mode nötig |
| Stabilität | Ausgereift, stark getestet | AutoOrtho-Doku warnt vor „filesystem variations" und „intrusive malware detection" |

### XEarthLayer als Linux-Only-Konsequenz

XEarthLayer ist bewusst Linux-only:
1. FUSE-Reife auf Linux macht plattformübergreifende Abstraktion unnötig
2. Rust + `fuse3`-Crate mit async Tokio-Runtime bietet saubere Linux-FUSE-Anbindung
3. Kein Python-GIL → echte parallele FUSE-Request-Verarbeitung + async I/O
4. X-Plane 12 Vulkan läuft nativ auf Linux → kompletter nativer Stack

**Quelle:** [XEarthLayer GitHub](https://github.com/samsoir/xearthlayer), [WinFSP GitHub](https://github.com/winfsp/winfsp), [AutoOrtho FAQ](https://kubilus1.github.io/autoortho/latest/faq/)

---

## 5. Quellenübersicht

| Quelle | Typ | Confidence |
|--------|-----|------------|
| [DSF Usage In X-Plane](https://developer.x-plane.com/article/dsf-usage-in-x-plane/) | Primär (Laminar) | HIGH |
| [Terrain Type (.ter) File Format](https://developer.x-plane.com/article/terrain-type-ter-file-format-specification/) | Primär (Laminar) | HIGH |
| [Three Things You Need for Fast Orthophotos](https://developer.x-plane.com/2011/03/three-things-you-need-for-fast-orthophotos/) | Primär (Laminar) | HIGH |
| [FUSE — Linux Kernel Documentation](https://www.kernel.org/doc/html/next/filesystems/fuse/fuse.html) | Primär (Kernel.org) | HIGH |
| [AutoOrtho Approach](https://kubilus1.github.io/autoortho/latest/details/) | Primär (Projekt-Doku) | HIGH |
| [AutoOrtho Continued Approach](https://programmingdinosaur.github.io/autoortho4xplane/details/) | Primär (Fork-Doku) | HIGH |
| [XEarthLayer GitHub](https://github.com/samsoir/xearthlayer) | Primär (Repository) | HIGH |
| [AutoOrtho FUSE-Quellcode](https://github.com/kubilus1/autoortho/blob/main/autoortho/autoortho_fuse.py) | Primär (Quellcode) | HIGH |
| [To FUSE or Not to FUSE (USENIX FAST'17)](https://www.usenix.org/system/files/conference/fast17/fast17-vangoor.pdf) | Akademisch | HIGH |
| [RFUSE (USENIX FAST'24)](https://www.usenix.org/system/files/fast24-cho.pdf) | Akademisch | HIGH |
| [WinFSP GitHub](https://github.com/winfsp/winfsp) | Referenz | MEDIUM-HIGH |
