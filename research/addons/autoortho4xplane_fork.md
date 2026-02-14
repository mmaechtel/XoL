# AutoOrtho4XPlane — ProgrammingDinosaur Fork: Research Report

**Datum:** 2026-02-14
**Quellen-Zeitraum:** 2025-08 bis 2026-02-14
**Primärquellen:** GitHub Repository, GitHub Releases, offizielle Dokumentation, X-Plane.org Forum

---

## 1. Projektübersicht

**Repository:** https://github.com/ProgrammingDinosaur/autoortho4xplane
**Maintainer:** Andres Hernandez (ProgrammingDinosaur)
**Lizenz:** Apache 2.0
**Fork von:** kubilus1/autoortho (letztes Original-Release: v0.7.2, 21. Januar 2024)
**Repository erstellt:** 25. April 2024
**Default Branch:** `develop`
**Sprachen:** Python (98%), C (2%), NSIS, Makefile, Shell
**Stars:** 97 | **Forks:** 4 | **Offene Issues:** 21
**Gesamte Commits:** ~1.072 (Stand Feb 2026)
**Letzte Aktivität:** 14. Februar 2026 (laufend aktiv)

**Top-Contributors:**
- kubilus1: 526 Commits (Original-Codebase)
- ProgrammingDinosaur: 491 Commits (Fork-Maintainer)
- karlrado: 28 Commits (UI, Settings, DataRef-Integration)
- jonaseberle: 7 Commits
- xlignieres: 5 Commits (erster Fork-Maintainer)

Quelle: https://github.com/ProgrammingDinosaur/autoortho4xplane

---

## 2. Aktuelle Version und Release-Historie

### Aktuelle Version: 2.0.4 (14. Februar 2026)

**Binaries für Linux:**
- `autoortho_linux_2.0.4_jammy.tar.gz` (Ubuntu 22.04, ~127 MB)
- `autoortho_linux_2.0.4_noble.tar.gz` (Ubuntu 24.04, ~126 MB)

Quelle: https://github.com/ProgrammingDinosaur/autoortho4xplane/releases/tag/2.0.4

### Vollständige Release-Timeline (nur stabile Releases)

| Version | Datum | Schwerpunkt |
|---------|-------|-------------|
| 1.0.1 | 20.08.2025 | Erster Fork-Release: PyQt6-UI, Settings-Tab, ZL17/ZL19, SimHeaven-Integration, Auto-Clean Cache |
| 1.1.0 | 22.08.2025 | Yandex Maps, SSL_CERT_DIR Auto-Set auf Linux, SimHeaven-Retrokompatibilität XP11 |
| 1.1.1–1.1.3 | 23–25.08.2025 | Bugfixes |
| 1.2.0 | 31.08.2025 | macOS-Kompatibilität (Apple Silicon), FUSE-Refactor, Custom Tiles Support, Auto-Update-Check |
| 1.2.2–1.2.7 | Sep 2025 | Diverse Bugfixes, Stabilitätsverbesserungen |
| 1.3.0 | 23.09.2025 | **Seasons-Support** (DSF XP11→XP12 Konvertierung, Saturation-Filter), Mac FUSE Workers Rework |
| 1.3.1–1.3.3 | Sep–Okt 2025 | Bugfixes |
| 1.4.0 | 07.11.2025 | **Missing-Chunks-Handling**: HTTP-Status-basiert, Fallback-Kaskade (Downscale/Upscale), Prioritätssystem via DataRef, Async JPEG Decode, MaxWait Suspend, Parallel JPEG Decoding, Logging Refactor |
| 1.4.1 | 11.11.2025 | Bugfixes |
| 1.5.0 | 10.12.2025 | **Nuitka→PyInstaller Migration** (Stabilität), Crash Handler, JPEG Decode Threads Optimierung |
| 1.5.1 | 18.12.2025 | Ubuntu 22.04 Build wieder hinzugefügt, Crash-Fixes |
| 1.6.0 | 30.12.2025 | **Dynamic Zoom Levels** (AGL-basiert), **Predictive Pre-fetching**, **SimBrief-Integration**, Performance-Tuning-Optionen, Time Exclusions |
| 1.6.1–1.6.3 | Jan 2026 | FUSE-Timeout-Fix, Download-Stall-Fix, macOS-Stabilität |
| **2.0.0** | **29.01.2026** | **C-Pipeline** (3x Ladezeiten-Verbesserung), **Cache Rework** (.aob2 Bundle-Format), Python 3.14, Buffer Pool, Pipeline-Modi |
| 2.0.1 | 30.01.2026 | py7zr→7zip Binary, macOS Seasons-Fix |
| 2.0.2 | 05.02.2026 | Memory Leaks in C-Code, Fixed Decoding Pool, macOS Memory Detection |
| 2.0.3 | 10.02.2026 | RAM-Spitzen reduziert, PrepareWorld-Ladezeit verbessert, Memory Leak bei Cache-Konsolidierung |
| **2.0.4** | **14.02.2026** | Global Memory Watcher, Scenery Installer GUI verbessert, ZIP-Extraktion 2x schneller |

Quelle: https://github.com/ProgrammingDinosaur/autoortho4xplane/releases

---

## 3. Architektur

### 3.1 Dual-Pipeline: C vs. Python

Seit Version 2.0.0 verfügt AutoOrtho über eine native C-Pipeline für DDS-Textur-Erstellung, die die Python-basierte Verarbeitung weitgehend ersetzt.

**Pipeline-Modi** (konfigurierbar in den Settings):

| Modus | Beschreibung |
|-------|-------------|
| **Auto** (Standard) | C-Pipeline; OS-abhängige Cache-Reads (Linux/macOS: Python, Windows: Native) |
| **Native** | Vollständig C für alle unterstützten Prozesse |
| **Hybrid** | C für alle Prozesse außer Cache-Reads (Python) |
| **Python** | Fallback auf 1.6.x-Verhalten (nur Python) |

**Performance der C-Pipeline** (laut Dokumentation):
- Cache Read: ~10x schneller
- JPEG Decode: ~8x schneller
- DDS Compression: ~12x schneller
- Gesamt-Tile-Build: ~10x schneller
- Gesamtverbesserung der Ladezeiten: ~3x (netzwerkabhängig)

**Ausnahme:** Apple Maps Downloads verwenden weiterhin Python-HTTP-Clients wegen dynamischer Token-Authentifizierung über DuckDuckGo-Proxy.

**Konfigurierbare Parameter (v2.0+):**
- Pre-Fetch Workers: Parallelität für vorausschauendes Tile-Download
- Tile Build Workers: Parallelität für Echtzeit-FUSE-Anfragen von X-Plane
- Buffer Pool Size: Vorab-allokierte DDS-Puffer (bestimmt gleichzeitige DDS-Builds, RAM-Verbrauch wird live angezeigt)
- Chunk Min Ratio: Akzeptable Quote fehlender Chunks bevor Fallback-Kette aktiviert wird

Quelle: https://github.com/ProgrammingDinosaur/autoortho4xplane/releases/tag/2.0.0

### 3.2 FUSE-basiertes virtuelles Dateisystem

AutoOrtho nutzt FUSE (Filesystem in Userspace) um Ortho-Tiles als reguläre Dateien im Custom Scenery-Verzeichnis von X-Plane bereitzustellen.

**Funktionsweise:**
1. AutoOrtho erstellt FUSE-Mounts unter `Custom Scenery/z_autoortho/`
2. X-Plane öffnet DDS-Texturdateien über reguläre Dateisystem-Aufrufe
3. FUSE fängt diese Aufrufe ab und leitet sie an AutoOrtho weiter
4. AutoOrtho baut die DDS-Textur on-the-fly aus heruntergeladenen/gecachten JPEG-Chunks

**Plattformspezifische FUSE-Implementierung:**
- **Linux:** libfuse/FUSE3 — läuft im selben Prozess
- **macOS:** MacFUSE oder FUSE-T — separate FUSE-Worker-Prozesse pro Mount (seit v1.3.0)
- **Windows:** WinFSP oder Dokan

Seit v1.2.0 wurden FUSE-Methoden refactored: Caching für wiederholte Aufrufe, Fehlerbehandlung (fail-fast), Beschränkung auf korrekte Ordner (terrain, textures, Earth Nav Data).

Quelle: https://programmingdinosaur.github.io/autoortho4xplane/

### 3.3 Tile-Streaming-Architektur

**Datenfluss (vereinfacht):**

1. X-Plane fordert DDS-Textur via FUSE-Mount an
2. AutoOrtho prüft Cache (seit v2.0: .aob2 Bundle-Dateien)
3. Bei Cache-Miss: Download der benötigten JPEG-Chunks vom Map-Provider
4. Chunks werden zu DDS-Textur assembliert (via C-Pipeline oder Python)
5. DDS wird an X-Plane zurückgegeben

**Cache-System (seit v2.0):**
- Neues `.aob2` Bundle-Format: konsolidiert alle Chunk-Daten pro DSF-Koordinate
- Pfadstruktur: `cache/bundles/<DSF-Koordinate 10°>/<spezifische DSF-Koordinate>/maptype`
- Einzelne JPEGs werden nach Konsolidierung automatisch gelöscht
- Verhindert Cache-Verzeichnisse mit tausenden kleinen Dateien (war besonders auf macOS problematisch)
- Periodische manuelle Bereinigung der JPEG-Reste über UI möglich

**Pre-Fetching-System (seit v1.6.0):**
- Berechnet Flugpfad basierend auf Position, Geschwindigkeit, Vertikalgeschwindigkeit
- Optional: SimBrief-Integration für exakte Flugplan-basierte Vorab-Downloads
- Konfigurierbar: Lookahead 1–60 Minuten (Standard: 10 Min)
- Low-Priority-Queue: stört nicht die Echtzeit-Tile-Anfragen

Quelle: https://programmingdinosaur.github.io/autoortho4xplane/performance/

---

## 4. Linux-spezifische Aspekte

### 4.1 Installation auf Debian/Ubuntu

**Voraussetzungen:**
- X-Plane 11.50+ oder X-Plane 12
- FUSE (fuse3 + libfuse2)
- Schnelle CPU, Breitband-Internet
- SSD empfohlen

**Binaries:** Seit v1.5.1 gibt es separate Linux-Builds:
- `autoortho_linux_*_jammy.tar.gz` — für Ubuntu 22.04 (Jammy) und kompatible
- `autoortho_linux_*_noble.tar.gz` — für Ubuntu 24.04 (Noble) und kompatible

Die Binaries sind PyInstaller-basiert (seit v1.5.0, vorher Nuitka) und bundlen alle Abhängigkeiten.

**Installation (Binary):**
```bash
# Download von GitHub Releases
tar xzf autoortho_linux_2.0.4_noble.tar.gz
chmod +x autoortho_lin.bin
./autoortho_lin.bin
```

**Installation (from Source, Debian 12):**
```bash
# System-Dependencies
sudo apt install -y fuse3 libfuse2 git curl build-essential libssl-dev zlib1g-dev \
  libbz2-dev libreadline-dev libsqlite3-dev wget llvm libncurses5-dev libncursesw5-dev \
  xz-utils tk-dev libffi-dev liblzma-dev python3-openssl

# pyenv + Python
curl https://pyenv.run | bash
# (.bashrc/.zshrc anpassen)
pyenv install 3.12.0
pyenv virtualenv 3.12.0 autoortho

# Repository
git clone https://github.com/ProgrammingDinosaur/autoortho4xplane.git ~/autoortho
cd ~/autoortho
pyenv activate autoortho
pip install --upgrade pip
pip install -r requirements.txt
```

**Hinweis:** v2.0.0 läuft auf Python 3.14, die Source-Installation erfordert ggf. neuere Python-Versionen.

Quelle: https://programmingdinosaur.github.io/autoortho4xplane/

### 4.2 FUSE-Konfiguration

**Pflicht-Konfiguration:**
```bash
# /etc/fuse.conf — Zeile entkommentieren oder hinzufügen:
user_allow_other
```

Ohne `user_allow_other` kann AutoOrtho die FUSE-Mounts nicht für X-Plane zugänglich machen.

**Empfehlung: File Descriptor Limit erhöhen:**
```bash
ulimit -S -n 8192
```

AutoOrtho öffnet viele kleine Dateien gleichzeitig; das Standard-Limit von 1024 kann zu Fehlern führen.

**Stale Mounts bereinigen:**
```bash
sudo umount -f AutoOrtho
```

Nötig wenn AutoOrtho unsauber beendet wurde und alte Mounts hängenbleiben.

Quelle: https://programmingdinosaur.github.io/autoortho4xplane/faq/

### 4.3 Linux-spezifische Besonderheiten

- **FUSE-Worker:** Linux und Windows nutzen In-Process FUSE-Worker (gleicher Prozess). Nur macOS benötigt separate Prozesse pro Mount (seit v1.3.0).
- **C-Pipeline Auto-Modus:** Auf Linux werden Cache-Reads über Python durchgeführt (nicht nativ), da native Cache-Reads auf Linux langsamer sind als auf Windows.
- **SSL-Zertifikate:** Seit v1.1.0 setzt AutoOrtho automatisch `SSL_CERT_DIR` auf Linux, falls nicht vorhanden (Issue #11).
- **libfuse:** Issue #170 dokumentiert `"Unable to find libfuse"` — gelöst durch Installation von `libfuse2`.
- **GLIBC-Kompatibilität:** Issue #146 dokumentiert `GLIBC_2.38 not found` auf Ubuntu 22.04 — gelöst durch separaten Jammy-Build (seit v1.5.1).
- **Executable Flags:** Issue #119 dokumentiert fehlende Executable-Flags auf `DSFTool` und `7zz` im Linux-Build — seit v1.3.3 behoben.

### 4.4 Bekannte Linux-Issues (aktuell offen)

Zum Zeitpunkt der Recherche (14.02.2026) gibt es **keine offenen Linux-spezifischen Issues**. Alle historischen Linux-Bugs sind geschlossen:

| Issue | Titel | Status |
|-------|-------|--------|
| #284 | Linux - 7zip Python module failing to load | Closed (v2.0.1) |
| #265 | [LINUX] Freezes when typing in simbrief user id field | Closed |
| #248 | Can't start on Bazzite Linux due to fuse mount error | Closed |
| #211 | Add Ubuntu 22.04 build | Closed (v1.5.1) |
| #189 | Suddenly requires root permission in Linux | Closed |
| #170 | OSError: Unable to find libfuse | Closed |
| #146 | GLIBC_2.38 not found on Ubuntu 22.04 | Closed (v1.5.0) |

Quelle: https://github.com/ProgrammingDinosaur/autoortho4xplane/issues

---

## 5. Features

### 5.1 Map-Provider

| Provider | Verfügbar seit | Anmerkungen |
|----------|---------------|-------------|
| **Bing** | Original (kubilus1) | Standard-Provider |
| **Google** | Original | — |
| **Here** | Original | — |
| **Yandex** | v1.1.0 (Fork) | Credits: nyuuzyou |
| **Apple Maps** | v1.0.1 (Fork) | Langsamer wegen Token-Auth über DuckDuckGo-Proxy, nur Python-HTTP |

Quelle: https://github.com/ProgrammingDinosaur/autoortho4xplane/releases/tag/1.0.1

### 5.2 Zoom-Level-System

**Statisch (Fixed Mode):**
- Max Zoom Level: bis ZL18 (Standard-Mesh), bis ZL19 mit Base-Mesh-Paketen
- Max Zoom Near Airports: separat konfigurierbar, bis ZL19

**Dynamisch (seit v1.6.0):**
- Zoom Level passt sich automatisch an AGL-Höhe (Above Ground Level) an
- Konfigurierbar: Höhenschwellen und zugehörige Zoom-Level
- Beispiel: ZL17/ZL18 unter 10.000 ft AGL, ZL16 darüber
- Berechnung via DataRef-Tracking oder SimBrief-Flugplan

**Ressourcen-Eskalation pro Zoom Level:**

| ZL | Chunks/Tile | Relative Ressourcen |
|----|-------------|-------------------|
| ZL14 | 16 | 1x |
| ZL15 | 64 | 4x |
| ZL16 | 256 | 16x |
| ZL17 | 1.024 | 64x |
| ZL18 | 4.096 | 256x |

Quelle: https://programmingdinosaur.github.io/autoortho4xplane/performance/

### 5.3 Cache Management

- **Bundle-Format (.aob2):** Seit v2.0.0, konsolidiert JPEG-Chunks in einzelne Dateien
- **Auto-Clean Cache:** Seit v1.0.1, bei Programmende
- **Delete All Cache Button:** Seit v1.4.0, in der UI (Beitrag von karlrado)
- **Ephemeral DDS Cache:** Konfigurierbar (Standard: 4096 MB), temporäre Vorab-DDS, wird bei Session-Ende gelöscht
- **Automatische JPEG-Bereinigung:** JPEGs werden nach Konsolidierung in .aob2 gelöscht

### 5.4 GUI

- **Framework:** PyQt6 (seit v1.0.1, ersetzt vorheriges Framework)
- **Tabs:** Setup, Scenery, Advanced Settings, Logs
- **Features:** Tooltips, Settings-Speicherung ohne manuelles File-Editing, Fortschrittsbalken bei Downloads, In-App SimBrief-Import
- **Live-Anzeige:** RAM-Nutzung bei Buffer-Pool-Konfiguration, Download-Statistiken

### 5.5 SimHeaven-Integration

- Automatische `scenery_packs.ini` Konfiguration (seit v1.0.1)
- Checkbox "SimHeaven Overlays": deaktiviert AutoOrtho-eigene Overlays zugunsten von SimHeavens
- Validierung: prüft ob passende SimHeaven X-World Pakete installiert sind
- Retrokompatibilität mit XP11 SimHeaven-Paketnamen (seit v1.1.0)

Quelle: https://github.com/ProgrammingDinosaur/autoortho4xplane/releases/tag/1.0.1

### 5.6 Seasons (seit v1.3.0)

- **DSF-Konvertierung:** In-App Konvertierung von XP11-Tiles zu XP12-Format (basiert auf hotbsos Script)
- **Saturation-Filter:** Jahreszeitenabhängige Farbsättigung der Ortho-Bilder (funktioniert auch mit XP11-Tiles)
- **Pro-Tile-Konfiguration:** Individuelle Saison-Einstellungen je Scenery-Paket
- **Backup:** Originale DSF-Tiles werden gesichert und können wiederhergestellt werden

### 5.7 SimBrief-Integration (seit v1.6.0)

- Import des Flugplans über SimBrief User ID
- **Pre-Fetching:** Chunks entlang der Route werden vorab heruntergeladen
- **Dynamic Zoom:** Erwartete AGL aus Flugplan bestimmt ZL pro Tile
- **Konfigurierbar:**
    - Route Consideration Radius: 10–200 nm (Standard: 50 nm)
    - Route Deviation Threshold: 5–100 nm (Standard: 40 nm)
    - Route Prefetch Radius: 10–150 nm (Standard: 40 nm)
- Fallback auf DataRef-basierte Berechnung wenn >40 nm off-route

### 5.8 Time Exclusions (seit v1.6.0)

- AutoOrtho-Tiles können zu konfigurierbaren Zeiten deaktiviert werden
- Nutzen: keine Ortho-Tile-Verarbeitung bei Nachtflügen
- Basiert auf lokaler Sim-Zeit via DataRef

Quelle: https://github.com/ProgrammingDinosaur/autoortho4xplane/releases/tag/1.6.0

---

## 6. Performance

### 6.1 Performance-Einstellungen (v2.0+)

**Time Budget System:**
- `tile_time_budget`: 60–600 Sekunden (Standard: 180s) — maximale aktive Verarbeitungszeit pro Tile
- `maxwait`: 0.1–10.0 Sekunden (Standard: 5.0s) — maximale Wartezeit pro einzelnen Chunk-Download
- `suspend_maxwait`: Startwert 10x erhöht während X-Plane-Ladebildschirm (Standard: an)

**Fallback-System:**
- `none`: Schnellste, grüne Patches bei fehlenden Tiles möglich
- `cache`: Cache + Mipmap-Skalierung, kein Netzwerk-Fallback (Standard)
- `full`: Cache + Mipmap + Netzwerk-Download niedrigerer Auflösung

**Pre-Fetching:**
- Konfigurierbar: 1–60 Minuten Lookahead (Standard: 10 Min)
- Bei 150 kts und 10 Min Lookahead: ~25 nm voraus

**Native Pipeline:**
- `native_pipeline_threads`: 0 = Auto-Detect (alle Kerne), N = manuell limitieren
- `ephemeral_dds_cache_mb`: Temp-DDS-Cache (Standard: 4096 MB)

Quelle: https://programmingdinosaur.github.io/autoortho4xplane/performance/

### 6.2 RAM-Nutzung

Die v2.0.x-Releases zeigen aktive Arbeit an RAM-Optimierung:
- v2.0.0: Buffer Pool mit vorab-allokiertem Speicher (konfigurierbar)
- v2.0.2: Memory Leaks in C-Code behoben, Fixed Decoding Pool
- v2.0.3: RAM-Spitzen reduziert, Memory Leak bei Cache-Konsolidierung behoben
- v2.0.4: Global Memory Watcher über mehrere Mounts hinweg

RAM-Nutzung hängt stark von Konfiguration ab (Buffer Pool Size, Zoom Level, Pre-Fetch Workers).

### 6.3 Empfohlene Konfigurationen (aus offizieller Doku)

**Stutter-freies Fliegen:**
```
tile_time_budget = 120
fallback_level = cache
prefetch_lookahead = 30
max_zoom_level = 16
```

**Maximale Qualität:**
```
tile_time_budget = 300
fallback_level = full
fallback_extends_budget = True
prefetch_lookahead = 60
max_zoom_level = 17
```

**Schwaches System:**
```
tile_time_budget = 180
fallback_level = none
prefetch_enabled = False
max_zoom_level = 15
```

Quelle: https://programmingdinosaur.github.io/autoortho4xplane/performance/

---

## 7. Bekannte Issues und Problemfelder

### 7.1 Offene Issues (Stand 14.02.2026, Top-Probleme)

| # | Titel | Erstellt | Kommentare |
|---|-------|----------|-----------|
| 329 | How to restore window display after running | 14.02.2026 | 5 |
| 327 | AO 2.0.4-rc-1 RAM usage | 13.02.2026 | 2 |
| 323 | Trouble with Troubleshooting | 12.02.2026 | 9 |
| 322 | Stuck on loading followed by crash (2.0.3) | 12.02.2026 | 2 |
| 317 | Blank/Empty Tiles Occasionally | 08.02.2026 | 1 |
| 304 | Stuck at "Preparing World" | 05.02.2026 | 4 |
| 302 | Slow Loading | 04.02.2026 | 3 |
| 291 | Increased stuttering in 2.0/2.0.1 | 31.01.2026 | 4 |
| 269 | BIG STUTTERING around 10-20min after takeoff | 11.01.2026 | 8 |
| 251 | AO crashes just before cruise on every flight | 02.01.2026 | 40 |

**Trends:**
- Seit v2.0.0 (C-Pipeline-Einführung) vermehrte RAM-/Memory-bezogene Reports
- Lange Ladezeiten bleiben wiederkehrendes Thema
- Stuttering bei längeren Flügen wird mehrfach berichtet
- Keine offenen Linux-spezifischen Bugs

Quelle: https://github.com/ProgrammingDinosaur/autoortho4xplane/issues

### 7.2 Historische Linux-Issues (alle geschlossen)

- **libfuse nicht gefunden** (#170) — `libfuse2` muss neben `fuse3` installiert sein
- **GLIBC-Inkompatibilität** (#146) — separater Ubuntu 22.04 (Jammy) Build seit v1.5.1
- **Root-Berechtigung plötzlich nötig** (#189) — behoben
- **FUSE-Mount-Fehler auf Bazzite Linux** (#248) — behoben
- **7zip Python-Modul auf Linux** (#284) — behoben in v2.0.1 (py7zr→7zip Binary)
- **Fehlende Executable-Flags** (#119) — behoben

---

## 8. Vergleichspunkte: AutoOrtho4XPlane vs. XEarthLayer vs. XPME

### 8.1 AutoOrtho4XPlane (ProgrammingDinosaur Fork)

- **Sprache:** Python (98%) + C (2%)
- **FUSE:** Ja (Linux: libfuse, macOS: MacFUSE/FUSE-T, Windows: WinFSP/Dokan)
- **Plattformen:** Linux, Windows, macOS (Apple Silicon)
- **Provider:** Bing, Google, Here, Yandex, Apple Maps
- **Max ZL:** ZL18 (Standard), ZL19 (mit Base Mesh)
- **Besonderheiten:** SimBrief-Integration, Seasons, Dynamic Zoom, C-Pipeline, .aob2 Cache-Format
- **GUI:** PyQt6 (vollständige Settings-UI)
- **Lizenz:** Apache 2.0
- **Aktive Entwicklung:** Ja (wöchentliche Releases)

### 8.2 XEarthLayer

- **Sprache:** Rust
- **FUSE:** Ja
- **Plattformen:** Linux, macOS
- **Provider:** Apple, ArcGIS, Bing, Google, MapBox, USGS
- **Besonderheiten:** Dual-Zone Pre-Fetching, Rust-basierte Performance/Memory Safety
- **GUI:** Eigenständige App (xearthlayer.app)
- **Lizenz:** Closed Source (kostenlos nutzbar)
- **Status:** Aktive Entwicklung

### 8.3 XPME (X-Plane Map Enhancement)

- **Ansatz:** Plugin-basiert (kein externes Tool)
- **FUSE:** Nein
- **Plattformen:** Windows, Linux, macOS
- **Provider:** Bing
- **Besonderheiten:** Einfachste Installation (Drag-and-Drop Plugin), geringste Konfiguration
- **Limitierungen:** Nur Bing, weniger Kontrollmöglichkeiten, niedrigere maximale Auflösung

### 8.4 Wesentliche Unterschiede

| Dimension | AutoOrtho4XPlane | XEarthLayer | XPME |
|-----------|-----------------|-------------|------|
| Architektur | Python+C, FUSE | Rust, FUSE | X-Plane Plugin |
| Setup-Aufwand | Mittel (FUSE + App) | Mittel (FUSE + App) | Gering (Plugin) |
| Konfigurierbarkeit | Sehr hoch | Mittel | Gering |
| Provider-Auswahl | 5 Provider | 6 Provider | 1 Provider |
| Max Zoom | ZL19 | variiert | niedriger |
| Seasons | Ja (seit v1.3.0) | Nein | Nein |
| SimBrief-Integration | Ja (seit v1.6.0) | Nein | Nein |
| Open Source | Ja (Apache 2.0) | Nein | Nein |
| X-Plane 11 Support | Ja | Nur XP12 | Nur XP12 |

---

## 9. Zusammenfassung und Bewertung

### Stärken

1. **Aktive Entwicklung:** 83 Releases in 6 Monaten, wöchentliche Updates
2. **Umfangreiche Features:** SimBrief, Seasons, Dynamic Zoom, C-Pipeline — alles Alleinstellungsmerkmale
3. **Gute Linux-Unterstützung:** Separate Builds für Ubuntu 22.04 und 24.04, alle Linux-Bugs geschlossen
4. **Open Source:** Apache 2.0, aktive Community-Beiträge (karlrado, hotbso)
5. **Performance-Fortschritt:** C-Pipeline bietet signifikante Verbesserung gegenüber reinem Python
6. **Umfangreiche Dokumentation:** Eigene Docs-Site mit Performance-Tuning-Guide und FAQ

### Schwächen / Risiken

1. **RAM-Management:** v2.0.x zeigt laufende Arbeit an Memory-Optimierung; RAM-Spitzen werden von Nutzern gemeldet
2. **Ladezeiten:** Wiederkehrendes Thema in Issues, stark konfigurationsabhängig
3. **Stuttering:** Mehrere Reports über Stutter nach 10–20 Min Flug, insbesondere seit v2.0
4. **Ein-Maintainer-Projekt:** Hauptsächlich ProgrammingDinosaur, karlrado als aktiver Co-Contributor
5. **Schnelle Release-Zyklen:** Viele RC-Versionen und schnelle Patches deuten auf aggressive Entwicklung mit Nachbesserungsbedarf

### Relevanz für XoL-Dokumentation

Die bestehende XoL-Seite (`docs/en/addon/autoortho.md`) referenziert bereits den Fork, ist aber in mehreren Bereichen veraltet:
- C-Pipeline und Pipeline-Modi sind erwähnt, aber Details fehlen
- Performance-Tuning-Optionen (Time Budget, Fallback System, Pre-Fetching) fehlen komplett
- Seasons-Feature nicht dokumentiert
- SimBrief-Integration nicht dokumentiert
- Dynamic Zoom nicht dokumentiert
- .aob2 Cache-Format nicht erklärt
- Linux-Binary-Builds (Jammy/Noble) nicht erwähnt
- `ulimit` und FUSE-Troubleshooting für Linux fehlen
- Vergleich mit XEarthLayer/XPME fehlt

---

## Quellen

1. GitHub Repository: https://github.com/ProgrammingDinosaur/autoortho4xplane
2. Releases: https://github.com/ProgrammingDinosaur/autoortho4xplane/releases
3. Offizielle Dokumentation: https://programmingdinosaur.github.io/autoortho4xplane/
4. FAQ: https://programmingdinosaur.github.io/autoortho4xplane/faq/
5. Performance Guide: https://programmingdinosaur.github.io/autoortho4xplane/performance/
6. X-Plane Forum Thread: https://forums.x-plane.org/forums/topic/334894-fork-of-autoortho-xlignieresautoortho4xplane-programmingdinosaurautoortho4xplane/
7. Original Repository (kubilus1): https://github.com/kubilus1/autoortho
8. XEarthLayer: https://github.com/samsoir/xearthlayer / https://xearthlayer.app/
