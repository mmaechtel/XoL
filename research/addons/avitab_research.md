# AviTab — Research Paper

**Datum:** 2026-02-15
**Status:** recherchiert
**Quellen-Zeitraum:** 2024–2026

---

## 1. Was ist AviTab?

AviTab ist ein Open-Source-Plugin für X-Plane (11.20+ und 12), das ein Tablet im Cockpit darstellt. Es wurde primär für VR-Nutzung entwickelt, funktioniert aber ebenso im normalen 2D-Fenster-Modus. Das Plugin löst das Problem, dass Piloten während des Flugs häufig PDF-Karten, Checklisten oder Handbücher nachschlagen müssen — ohne das VR-Headset abzunehmen.

### Kernfunktionen

- **PDF-Viewer:** Zeigt PDF-Dateien aus dem `charts/`-Unterverzeichnis des Plugin-Ordners an (inkl. Unterordner)
- **Moving Map:** Online-Karten (OpenTopoMap, OpenStreetMap, konfigurierbare Quellen) und Offline-Karten
- **Navigraph-Integration:** Anzeige von IFR/VFR-Charts direkt im Cockpit (nur mit Navigraph-Abo, nicht verfügbar bei Selbstkompilierung)
- **ChartFox-Integration:** Kostenlose Charts über Vatsim-Login (neue API seit v0.7.1)
- **Airport-App:** Flughafeninformationen, Runway-Daten, lokale Charts
- **Routen-Overlay:** FMS-Dateien als Overlay auf der Moving Map
- **Aircraft-Integration:** Einige Flugzeuge (z.B. Zibo 737-800X) haben ein 3D-Tablet-Modell mit AviTab-Integration
- **Standalone-Modus:** Kann auch als eigenständige Anwendung außerhalb von X-Plane laufen (höhere Auflösung)
- **Multiplayer-Overlay:** Andere Flugzeuge auf der Karte anzeigen (TCAS-Datarefs)
- **Custom Maps:** Über `online-maps/mapconfig.json` eigene Tile-Server konfigurierbar

### Ergänzungs-Plugin: AviTab Browser

Ein separates Plugin von einem anderen Entwickler (rswilem) fügt einen vollwertigen Webbrowser zum AviTab hinzu. Es nutzt das in X-Plane 12 eingebettete Chromium Embedded Framework (CEF).

- **Repo:** https://github.com/rswilem/avitab-browser
- **Aktuelle Version:** 1.0.5 (2026-02-07)
- **Lizenz:** GPL-3.0
- **Features:** Konfigurierbare Homepage, Hotkey-Websites, SimBrief-Flugplan-Download, Geolocation aus dem Simulator
- **Linux-Support:** Ja, ab XP12 (nutzt das eingebettete CEF von X-Plane 12)
- **Quelle:** [GitHub rswilem/avitab-browser](https://github.com/rswilem/avitab-browser), [forums.x-plane.org Download-Seite](https://forums.x-plane.org/files/file/93812-avitab-browser-a-web-browser-addon-for-the-avitab-plugin/)

---

## 2. Repository-Status und Wartung

| Eigenschaft | Wert |
|---|---|
| **Repository** | https://github.com/fpw/avitab |
| **Hauptentwickler** | fpw (Folke Will) |
| **Sprache** | C (mit C++17) |
| **Lizenz** | AGPL-3.0 |
| **Stars** | 340 |
| **Forks** | 65 |
| **Offene Issues** | 45 |
| **Letzter Commit** | 2024-08-31 |
| **Letztes Release** | v0.7.1 (2024-09-01) |
| **Archiviert** | Nein |

### Wartungszustand

Das Repository ist **nicht archiviert**, aber die Entwicklungsaktivität ist **gering**. Der letzte Commit und das letzte Release stammen vom September 2024. Es gibt 45 offene Issues (Stand Februar 2026), darunter mehrere Feature-Requests und Bugreports aus 2025. Der Hauptentwickler (fpw, 540 Commits) antwortet sporadisch auf Issues. Aktive Beiträger sind dave6502 (72 Commits) und mjh65 (45 Commits).

**Bewertung:** Funktionsfähig, aber langsame Wartung. Keine Anzeichen für baldige neue Releases. Community-Beiträge (PRs) werden angenommen, aber es dauert.

### Quelle

- [GitHub fpw/avitab](https://github.com/fpw/avitab)
- [GitHub Releases](https://github.com/fpw/avitab/releases)

---

## 3. Aktuelle Version und X-Plane 12 Kompatibilität

### Version 0.7.1 (2024-09-01)

Änderungen in v0.7.1:

- Custom Online-Maps konfigurierbar (OpenStreetMap etc. via `mapconfig.json`)
- Stamen-Kartenquelle entfernt (nicht mehr kostenlos)
- Routen-Overlay: FMS-Dateien auf Moving Map anzeigbar
- Neue ChartFox-API (alte wird eingestellt, erfordert jetzt Vatsim-Login)
- Navigraph-Kompatibilität repariert (neue API-Vorbereitung)
- Georeferenzierte ChartFox-Charts
- Nicht-PDF-Charts korrekt verarbeitet (z.B. deutsche Charts)
- Kartenposition/-Zoom als Datarefs für andere Plugins verfügbar

### X-Plane 12 Kompatibilität

- Offiziell getestet und kompatibel mit X-Plane 12
- **Bekanntes Problem mit XP 12.1.4+:** Multiplayer-Flugzeuge wurden zeitweise nicht auf der AviTab-Karte angezeigt (Issue #215). Wurde in X-Plane 12.3.0 beta 2 behoben — war ein X-Plane-seitiges Problem.
- **Flicker-Problem:** Einige Nutzer berichten, dass AviTab 0.7.1 schwarz bleibt oder flackert (Issue #224, offen seit Juli 2025). Betrifft nicht nur Linux.

### Download

- GitHub Release: https://github.com/fpw/avitab/releases/tag/v0.7.1
- Direkter Download: https://folko.solhost.org/avitab/AviTab-0.7.1.zip
- forums.x-plane.org: https://forums.x-plane.org/files/file/44825-avitab-vr-compatible-tablet-with-pdf-viewer-moving-maps-and-more/

---

## 4. Linux-Kompatibilität

### Grundsätzlich

AviTab unterstützt Linux nativ. Das Release enthält vorkompilierte Linux-Binaries (`lin_x64/AviTab.xpl`). Alle Abhängigkeiten werden statisch gelinkt (`-static-libgcc -static-libstdc++`), daher gibt es keine externen Laufzeitabhängigkeiten außer OpenGL (`libGL`).

### Bekannte Linux-spezifische Probleme

#### PDF-Crash auf Linux (KRITISCH)

**Status:** Offen, ungelöst (Stand Februar 2026)

AviTab stürzt auf Linux-Systemen ab, wenn PDF-, JPG- oder PNG-Dateien geöffnet werden. Der Crash tritt als SIGSEGV in der `lcms2`-Bibliothek auf:

```
SIGSEGV in cmsSignalError → cmsOpenIOhandlerFromMem → fz_new_icc_profile
```

**Betroffene Distributionen (bestätigt):**

- Arch Linux / EndeavourOS (Kernel 6.12.x, X-Plane 12.3.0)
- Ubuntu 24.04 / Kubuntu 24.10
- Arch mit GNOME Wayland

**Ursache:** Die in AviTab statisch gelinkte MuPDF-Bibliothek kollidiert mit der systemweiten `lcms2`-Bibliothek. AviTab bündelt eine eigene MuPDF-Version, die intern `lcms2` über die Systemversion aufruft. Bei neueren `lcms2`-Versionen (z.B. 2.17 auf Arch) kommt es zu einem Speicherzugriffsfehler bei der ICC-Profil-Verarbeitung.

**Chronologie:**

1. **November 2024:** Erstmals gemeldet mit XP 12.1.3b1 (Issue #213). Wurde als X-Plane-Beta-Bug identifiziert und in einer späteren Beta behoben.
2. **Oktober/November 2025:** Erneut aufgetreten, diesmal unabhängig von X-Plane-Betas. Auf Arch Linux (Issue #232) und in einem separaten Forum-Thread gemeldet.
3. Das Problem besteht weiterhin und scheint mit neueren `lcms2`-Systemversionen zusammenzuhängen.

**Workaround:** Keiner bekannt. PDF-Viewer-Funktionalität ist auf betroffenen Systemen nicht nutzbar. Map und andere Apps funktionieren normal.

**Quellen:**

- [GitHub Issue #213](https://github.com/fpw/avitab/issues/213) — XP12.1.3b1 PDF crash
- [GitHub Issue #232](https://github.com/fpw/avitab/issues/232) — Crashes when loading PDF files
- [forums.x-plane.org — Arch Linux AviTab CTD](https://forums.x-plane.org/forums/topic/337151-arch-linux-avitab-ctd-when-open-pdf-files/)
- [forums.x-plane.org — Crashing on Linux when opening PDF files](https://forums.x-plane.org/forums/topic/339214-crashing-on-linux-when-opening-pdf-files/)

#### Wayland

Keine expliziten Wayland-Probleme dokumentiert. X-Plane selbst läuft unter Wayland (via XWayland oder nativ seit XP12), und AviTab rendert innerhalb des X-Plane-Fensters — es öffnet kein eigenes Fenster. Daher ist Wayland-Kompatibilität primär eine X-Plane-Angelegenheit.

Ein Nutzer berichtet den PDF-Crash auch unter "Arch GNOME Wayland", aber der Crash ist auf `lcms2` zurückzuführen, nicht auf Wayland.

---

## 5. Installation auf Linux

### Vorkompiliertes Plugin (empfohlen)

```bash
# Download
wget https://folko.solhost.org/avitab/AviTab-0.7.1.zip

# Entpacken
unzip AviTab-0.7.1.zip

# In Plugin-Verzeichnis verschieben
mv AviTab /pfad/zu/X-Plane\ 12/Resources/plugins/
```

### Verzeichnisstruktur nach Installation

```
X-Plane 12/Resources/plugins/AviTab/
├── lin_x64/
│   └── AviTab.xpl          # Linux-Plugin-Binary
├── mac_x64/
│   └── AviTab.xpl          # macOS-Binary
├── win_x64/
│   └── AviTab.xpl          # Windows-Binary
├── charts/                  # PDF-Charts hier ablegen
├── online-maps/
│   └── mapconfig.json       # Custom Map-Konfiguration
├── config.json              # Plugin-Konfiguration
├── icons/
└── res/                     # Ressourcen
```

### Charts/PDFs ablegen

PDF-Dateien in den `charts/`-Ordner kopieren:

```bash
cp meine_charts/*.pdf /pfad/zu/X-Plane\ 12/Resources/plugins/AviTab/charts/
```

Unterordner werden unterstützt und als Verzeichnisstruktur im Plugin angezeigt.

### AviTab Browser (optional)

```bash
# Download von GitHub Releases
wget https://github.com/rswilem/avitab-browser/releases/download/v1.0.5/avitab-browser-linux.zip

# Entpacken und in Plugin-Verzeichnis verschieben
unzip avitab-browser-linux.zip
mv avitab-browser /pfad/zu/X-Plane\ 12/Resources/plugins/
```

**Voraussetzung:** AviTab muss bereits installiert sein.

---

## 6. Konfiguration

### config.json

Minimale Konfiguration im Plugin-Root:

```json
{
    "AviTab": {
        "logToStdOut": false,
        "loadNavData": true
    }
}
```

- `logToStdOut`: Log-Ausgabe auf stdout (nützlich beim Starten von X-Plane aus dem Terminal)
- `loadNavData`: X-Plane-Navigationsdaten laden (für Airport-App, Map-Overlays)

### Custom Online-Maps (mapconfig.json)

Datei: `online-maps/mapconfig.json`

```json
[
    {
        "name": "OpenTopoMap",
        "servers": ["a.tile.opentopomap.org", "b.tile.opentopomap.org", "c.tile.opentopomap.org"],
        "protocol": "https",
        "copyright": "Map Data (c) OpenStreetMap, SRTM - Map Style (c) OpenTopoMap (CC-BY-SA)",
        "url": "{z}/{x}/{y}.png",
        "min_zoom_level": 1,
        "max_zoom_level": 17,
        "tile_width_px": 256,
        "tile_height_px": 256,
        "enabled": true
    },
    {
        "name": "OpenStreetMap",
        "servers": ["tile.openstreetmap.org"],
        "protocol": "https",
        "copyright": "Map tiles (c) OpenStreetMap (ODbL)",
        "url": "{z}/{x}/{y}.png",
        "min_zoom_level": 1,
        "max_zoom_level": 17,
        "tile_width_px": 256,
        "tile_height_px": 256,
        "enabled": false
    }
]
```

Eigene Tile-Server (z.B. lokaler TileServer-GL) können hier ergänzt werden.

### Aircraft-Integration (AviTab.json)

Einige Flugzeuge unterstützen ein 3D-Tablet im Cockpit. Dafür muss eine `AviTab.json` im Aircraft-Root-Ordner liegen, die die Bildschirmkoordinaten des Tablet-Panels definiert. Dies ist aircraft-spezifisch und wird vom Aircraft-Entwickler bereitgestellt.

---

## 7. Kompilierung auf Linux (aus Quellcode)

### Voraussetzungen

**Debian/Ubuntu:**

```bash
sudo apt-get install cmake make git patch autoconf automake libtool libglfw3-dev
```

**Fedora:**

```bash
sudo dnf install autoconf automake libtool m4 gettext automake-wrapper glfw-devel cmake make git patch
```

### Build-Schritte

```bash
# Repository mit Submodules klonen
git clone --recurse-submodules https://github.com/fpw/avitab

cd avitab

# Abhängigkeiten bauen (MuPDF, curl, mbedtls, libgeotiff, QuickJS etc.)
./build_dependencies.sh

# Build-Verzeichnis erstellen
mkdir build && cd build

# CMake konfigurieren
cmake -G 'Unix Makefiles' ..

# Plugin kompilieren
make avitab_plugin

# ODER Standalone-Version
make AviTab-standalone
```

### Statisch gelinkte Bibliotheken

AviTab bündelt alle Abhängigkeiten als statische Bibliotheken (via `build_dependencies.sh`):

| Bibliothek | Zweck |
|---|---|
| MuPDF + mupdf-third | PDF-Rendering |
| curl + mbedtls | HTTPS-Kommunikation (Navigraph, ChartFox, Maps) |
| sqlite3 | Navigationsdatenbank |
| libgeotiff + libtiff + libproj | Georeferenzierung |
| detex | Texturkompression |
| QuickJS | JavaScript-Engine (Scripting) |
| LVGL (LittlevGL) | GUI-Toolkit |
| nlohmann/json | JSON-Parsing |
| stb | Bildverarbeitung |

### Einschränkung bei Selbstkompilierung

Die Navigraph-Integration ist bei selbstkompilierten Versionen **nicht verfügbar** (erfordert geheime API-Keys, die nur im offiziellen Build enthalten sind).

### Quellen

- [GitHub Wiki — Compiling](https://github.com/fpw/avitab/wiki/Compiling)
- [GitHub Issue #217 — Fedora compiling instructions](https://github.com/fpw/avitab/issues/217)
- [build_dependencies.sh](https://github.com/fpw/avitab/blob/master/build_dependencies.sh)
- [CMakeLists.txt](https://github.com/fpw/avitab/blob/master/src/CMakeLists.txt)

---

## 8. Zusammenfassung der Linux-Bewertung

### Stärken

- Native Linux-Unterstützung mit vorkompiliertem Binary
- Keine externen Laufzeitabhängigkeiten (außer libGL)
- Statisches Linking minimiert Kompatibilitätsprobleme
- Open Source (AGPL-3.0), kann selbst kompiliert werden
- Funktioniert in VR und 2D, unter X11 und Wayland
- AviTab Browser als Ergänzung ebenfalls Linux-kompatibel

### Schwächen / Risiken

- **PDF-Crash auf Linux:** Kritischer, ungelöster Bug auf Distributionen mit neuerer `lcms2` (Arch, aktuelle Ubuntu-Versionen). Die Kernfunktion PDF-Viewer ist auf diesen Systemen nicht nutzbar.
- **Langsame Wartung:** Letzter Commit September 2024, 45 offene Issues. Keine Anzeichen für baldiges Update.
- **lcms2-Inkompatibilität:** Das statisch gelinkte MuPDF kollidiert mit dynamisch gelinktem System-lcms2. Ein Fix müsste entweder lcms2 ebenfalls statisch linken oder MuPDF auf eine neuere Version aktualisieren.
- **Flicker-Problem:** Einige Nutzer berichten schwarzes/flackerndes Tablet (Issue #224), plattformübergreifend.

### Empfehlung für XoL-Dokumentation

AviTab ist relevant für die XoL-Dokumentation als eines der wichtigsten freien X-Plane-Plugins. Der PDF-Crash ist Linux-spezifisch und dokumentationswürdig. Folgende Aspekte sollten abgedeckt werden:

1. Installation (einfach, Copy-Paste)
2. Charts-Pfad und Konfiguration
3. Bekannter PDF-Crash auf Linux mit Distributionsliste
4. AviTab Browser als Ergänzung
5. Custom Maps Konfiguration
6. Hinweis auf Wartungszustand

**Debian-spezifisch:** Auf Debian Stable (Bookworm) ist lcms2 in Version 2.14 — diese Version ist möglicherweise noch nicht betroffen. Debian Testing/Trixie hat lcms2 2.16. Dies sollte getestet werden, bevor eine pauschale Warnung geschrieben wird.

---

## Quellen (chronologisch)

1. [GitHub fpw/avitab — Repository](https://github.com/fpw/avitab) — Hauptquelle
2. [GitHub Releases — v0.7.1](https://github.com/fpw/avitab/releases/tag/v0.7.1) — 2024-09-01
3. [GitHub Issue #213 — XP12.1.3b1 PDF crash](https://github.com/fpw/avitab/issues/213) — 2024-11
4. [GitHub Issue #215 — XP 12.1.4 compatibility](https://github.com/fpw/avitab/issues/215) — 2025-02
5. [GitHub Issue #217 — Fedora compiling](https://github.com/fpw/avitab/issues/217) — 2025-05
6. [GitHub Issue #224 — Flicker](https://github.com/fpw/avitab/issues/224) — 2025-07
7. [GitHub Issue #232 — PDF crash Linux](https://github.com/fpw/avitab/issues/232) — 2025-11
8. [GitHub rswilem/avitab-browser](https://github.com/rswilem/avitab-browser) — Ergänzungs-Plugin
9. [forums.x-plane.org — AviTab Download](https://forums.x-plane.org/files/file/44825-avitab-vr-compatible-tablet-with-pdf-viewer-moving-maps-and-more/) — Offizielle Download-Seite
10. [forums.x-plane.org — AviTab Browser](https://forums.x-plane.org/files/file/93812-avitab-browser-a-web-browser-addon-for-the-avitab-plugin/)
11. [forums.x-plane.org — Arch Linux CTD](https://forums.x-plane.org/forums/topic/337151-arch-linux-avitab-ctd-when-open-pdf-files/) — 2025-10
12. [forums.x-plane.org — Linux PDF crash](https://forums.x-plane.org/forums/topic/339214-crashing-on-linux-when-opening-pdf-files/) — 2025-11
13. [GitHub Wiki — Compiling](https://github.com/fpw/avitab/wiki/Compiling) — Build-Anleitung
