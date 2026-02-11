# XOrganizer unter Wine auf Linux

## Zusammenfassung

XOrganizer (v3, aktuell 3.5.0) ist eine Windows-only .NET-Anwendung zur Verwaltung von X-Plane-Szenerien, Plugins und Profilen. Kein nativer Linux-Support, kein geplanter. Wine-Kompatibilität ist aufgrund von WPF-Abhängigkeit, .NET-Installationsproblemen und Pfad-Separator-Konflikten **praktisch nicht gegeben**. Als native Linux-Alternative existiert Scenery Pack Organiser (Python), das die Kernfunktion (scenery_packs.ini sortieren) abdeckt, aber nicht die erweiterten Features (Profile, Konfliktanalyse, Plugin-Management).

## Technischer Hintergrund

### Framework und Runtime

- **.NET Framework 4.6.1+** (v2), **.NET 4.7** (ab v2.5.0), vermutlich **.NET 4.7/4.8** (v3)
- **64-bit only** mit paralleler Verarbeitung
- **UI-Framework: sehr wahrscheinlich WPF** (Windows Presentation Foundation) — belegt durch .NET 4.7 Upgrade speziell für DPI-Skalierungsprobleme, was ein WPF-spezifisches Feature ist (per-monitor DPI awareness ab .NET 4.6.2+)
- Internes Datenbankformat (proprietär, komplett neu in v2)

### Dateistruktur

XOrganizer ist eine **portable Anwendung** — kein Installer, keine Registry-Einträge.

```
XOrganizer/                     (frei wählbarer Ordner, NICHT in X-Plane)
    xOrganizer.exe              (Hauptprogramm, 64-bit)
    XoData/XoData.xml           (Konfiguration)
    XoProfiles/                 (Profilmodul)
    XoBackup/                   (bis zu 50 Backups)
    XoUtilities/                (Hilfsdateien)
    XoSceneryUserRules.txt      (benutzerdefinierte Sortierregeln)
```

**Zugriff auf X-Plane-Verzeichnis:**

- Liest/schreibt `Custom Scenery/scenery_packs.ini`
- Liest Aircraft-Ordner, Plugin-Ordner, Preferences
- Muss in einem **separaten Ordner** installiert sein (nicht innerhalb X-Plane)
- Erkennt X-Plane-Installation über Vorhandensein von `X-Plane.exe` im Root-Ordner

### Versionsgeschichte

| Version | Datum | Relevante Änderungen |
|---------|-------|---------------------|
| V3.5.0 | Juni 2025 | X-Plane Map Enhancement Support |
| V3.4.0 | August 2024 | Scenery Coverage, Aircraft Livery Search |
| V3.0 | September 2022 | X-Plane 12 Support (separates Produkt von V2) |
| V2.5.0 | ~2021 | Upgrade auf .NET 4.7 |
| V2.3.0 | ~2019 | 64-bit Architektur, parallele Verarbeitung |

V2 (XP10/XP11) und V3 (XP12) sind getrennte Produkte.

## Aktueller Stand: Wine-Kompatibilität

### Kein WineHQ-AppDB-Eintrag

XOrganizer ist nicht in der WineHQ Application Database gelistet. Kein ProtonDB-Eintrag, kein Lutris-Installationsskript.

### Forum-Berichte

**Einziger teilweiser Erfolg (v2, 2017):**

Ein User im X-Plane.org-Forum berichtete, XOrganizer v2 mit `winetricks dotnet45` unter Wine zum Laufen gebracht zu haben. Kein vollständiger Schritt-für-Schritt-Bericht.

**Gescheiterte Versuche:**

- Wine Mono (eingebauter .NET-Ersatz) reicht **nicht** — XOrganizer braucht das echte Microsoft .NET Framework
- Pterosaur.org.uk-Guide-Autor: "I have not so far been able to get it to run on Linux"
- Aktueller Thread (Februar 2025, "xOrganizer for Linux"): keine Lösung

**Für v3 (X-Plane 12) existieren keine bestätigten Erfolgsberichte unter Wine.**

### Technische Blocker

#### 1. WPF-Abhängigkeit (Hauptproblem)

Wine's WPF-Support ist **unvollständig und unzuverlässig**:

- Ein Rendering-Ansatz (WPF über D3D9) wurde wegen Darstellungsfehlern "in scheinbar allen WPF-Anwendungen" zurückgenommen
- WineHQ-Forum bestätigt: ".NET 4.0 and WPF application — does not work"
- Intel-GPUs unter Wine für WPF "basically unusable", NVIDIA am besten
- Portierung auf .NET Core wäre nötig, aber XOrganizer ist Closed-Source

**Wenn XOrganizer WPF nutzt (sehr wahrscheinlich), funktioniert es unter Wine nicht.**

#### 2. .NET 4.6.1+ in 64-bit Wine Prefix

- XOrganizer erfordert ein **64-bit Wine Prefix** (`WINEARCH=win64`)
- `winetricks dotnet461` auf 64-bit Prefix hat bekannte Probleme: `mscoree.dll` wird nicht gefunden
- `winetricks dotnet48` funktioniert je nach Wine-Version unterschiedlich
- Winetricks Issues #971 und #812 dokumentieren 64-bit .NET-Installationsprobleme

#### 3. Pfad-Separator-Problem (Funktionaler Deal-Breaker)

Selbst wenn XOrganizer unter Wine starten würde:

- `scenery_packs.ini` auf Linux nutzt **Forward Slashes**: `Custom Scenery/KSFO_Demo_Area/`
- Eine Windows-Anwendung unter Wine schreibt **Backslashes**: `Custom Scenery\KSFO_Demo_Area\`
- X-Plane auf Linux erkennt Einträge mit Backslashes **nicht**
- Nachbearbeitung per `sed -i 's|\\|/|g' scenery_packs.ini` wäre nach jeder XOrganizer-Änderung nötig

#### 4. X-Plane.exe-Erkennung

- XOrganizer prüft auf `X-Plane.exe` im Root-Ordner
- Auf Linux heißt die Binary `X-Plane` (ohne `.exe`)
- **Workaround:** `touch /pfad/zu/X-Plane\ 12/X-Plane.exe` (leere Dummy-Datei)

### Theoretischer Installationsversuch

Falls jemand es trotzdem versuchen will:

```bash
# 1. Dediziertes 64-bit Wine Prefix
export WINEPREFIX=~/.wine-xorganizer
export WINEARCH=win64
wineboot --init

# 2. Windows 10 setzen
winecfg   # Windows Version auf "Windows 10"

# 3. .NET Framework installieren
winetricks dotnet48   # oder dotnet461, beides fragil

# 4. Dummy X-Plane.exe erstellen
touch "/pfad/zu/X-Plane 12/X-Plane.exe"

# 5. XOrganizer starten
wine /pfad/zu/xOrganizer.exe
```

**Erwartetes Ergebnis:** .NET-Installation schlägt fehl oder GUI rendert nicht (WPF-Problem).

## Konfiguration unter Debian

Nicht anwendbar — XOrganizer funktioniert unter Wine auf Linux nicht zuverlässig genug für produktiven Einsatz.

## X-Plane-Spezifika

### Kernfunktionen von XOrganizer

- **Scenery-Verwaltung:** Automatische Kategorisierung (Airports, Overlays, Ortho, Mesh), Drag-and-Drop-Sortierung, Konfliktanalyse
- **Plugin-Management:** Aktivieren/Deaktivieren, Konfigurationsverwaltung
- **Profilmanagement:** Regionsbasierte Profile, flugplanbasierte automatische Profilierung
- **scenery_packs.ini:** Lesen, Sortieren, Schreiben — das Kernstück der Anwendung

### Developer-Statement zu Linux

Der Entwickler (MH1212) hat in einem dedizierten Forum-Thread (201 Antworten, 44.5k Views) erklärt, warum kein Mac/Linux-Support geplant ist. Hauptgründe: .NET-Framework-Abhängigkeit, Ressourcen für Mehrplattform-Entwicklung.

## Native Linux-Alternative: Scenery Pack Organiser

### iy4vet/SceneryPacksOrganiser (Empfohlen)

**Repository:** github.com/iy4vet/SceneryPacksOrganiser

Python-basierter, plattformübergreifender Scenery-Sortierer. Arbeitet nativ auf Linux.

**Funktionen:**

- Automatisches Sortieren aller Scenery Packs in `scenery_packs.ini`
- 13-stufige Sortier-Hierarchie: Custom Airports > Default Airports > Prefab Airports > Global Airports > Scenery Plugins > Libraries > SimHeaven Overlays > Custom Overlays > Default Overlays > AutoOrtho Overlays > Orthophotos > AutoOrtho Regions > Terrain Meshes
- `SCENERY_PACK_DISABLED`-Tags werden übernommen
- ICAO-Flughafenkonflikte erkennen
- Fehlerhafte Pakete warnen (Ordner-in-Ordner)
- Backup vor Änderung (`scenery_packs.ini.bak`)
- XP10/11 und XP12 Global Airports gleichzeitig

**Installation auf Linux:**

```bash
pip install py7zr pyyaml
python3 organiser.py
```

**Version:** 3.1r1 (Dezember 2024), aktiv gepflegt (91 Commits), GPL v2.

### Was der Alternative fehlt

Im Vergleich zu XOrganizer hat Scenery Pack Organiser **nicht:**

- Profilmanagement (regionsbasierte Scenery-Konfigurationen)
- Flugplanbasierte automatische Profilierung
- Visuelle Konfliktanalyse mit Karte
- Plugin-Management
- Drag-and-Drop-GUI
- Scenery Coverage Ansicht
- Backup-Verwaltung (über die einzelne .bak-Datei hinaus)

## Diagnose und Fehlerbehebung

Nicht anwendbar — Wine-Setup scheitert an WPF/NET-Kombination.

## Quellen

- [XOrganizer Official Site](https://www.4xplane.nl/xorganizer/) — Offizielle Projektseite
- [XOrganizer Manual V2.4.0 (PDF)](https://www.4xplane.nl/wp-content/uploads/2021/01/xOrganizer-Manual-V2.4.0-1.pdf) — Dokumentiert .NET-Anforderungen und Wine/Mac-Hinweise
- [Forum: Xorganizer on Wine](https://forums.x-plane.org/forums/topic/133061-xorganizer-on-wine/) — Einziger teilweiser Erfolg (v2, 2017)
- [Forum: xOrganizer for Linux](https://forums.x-plane.org/forums/topic/327186-xorganizer-for-linux/) — Aktueller Thread (Feb 2025), keine Lösung
- [Forum: Can XOrganizer work on Wine or Bottles?](https://forums.x-plane.org/forums/topic/332419-can-xorganizer-work-on-wine-or-bottles/) — 2025, keine bestätigte Lösung
- [Forum: No Mac/Linux version](https://forums.x-plane.org/index.php?/forums/topic/172160-suggestions-requests-and-explanation-for-no-maclinux-version/) — Developer-Statement
- [WineHQ: .NET 4.0 and WPF - does not work](https://forum.winehq.org/viewtopic.php?f=2&t=16710)
- [Winetricks Issue #971: dotnet461 64-bit](https://github.com/Winetricks/winetricks/issues/971)
- [Scenery Pack Organiser (iy4vet)](https://github.com/iy4vet/SceneryPacksOrganiser) — Native Linux-Alternative
- [XOrganizer V3 Announcement (Threshold)](https://www.thresholdx.net/news/xoxpv3)
- [Paul's X-Plane Pages: XOrganizer](https://www.pterosaur.org.uk/Xplane12/01-XP_Setup/01-Basic_Setup/Problem_Solving/XOrganzer.htm) — Bestätigt Wine-Probleme
