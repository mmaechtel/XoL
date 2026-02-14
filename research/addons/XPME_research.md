# Research: X-Plane Map Enhancement (XPME)

**Datum:** 2026-02-14
**Autor:** Claude (Recherche-Skill)
**Status:** Recherche abgeschlossen

---

## 1. Was ist XPME?

**Vollständiger Name:** X-Plane Map Enhancement (kurz: XPME)
**Autor:** derekhe (GitHub-Profil: https://github.com/derekhe)
**Projekttyp:** Closed-Source / Proprietär (Freemium-Modell)
**Website:** https://www.aiflygo.com/
**GitHub (nur Releases):** https://github.com/derekhe/xplane-map-enhancement-release
**X-Plane.to:** https://x-plane.to/file/1559/x-plane-map-enhancement

XPME ist eine Streaming-Lösung für Satelliten-Orthophotos in X-Plane 11 und 12. Die Software ersetzt die Standard-Bodentexturen durch hochauflösende Satellitenbilder, die in Echtzeit von verschiedenen Kartenanbietern geladen werden. XPME ist eine Portierung des älteren MSFS Map Enhancement (https://github.com/derekhe/msfs2020-map-enhancement), das derselbe Entwickler seit Dezember 2021 für Microsoft Flight Simulator pflegt.

### Abgrenzung zu AutoOrtho und XEarthLayer

| Merkmal | AutoOrtho (PD Fork) | XEarthLayer | XPME |
|---|---|---|---|
| **Sprache** | Python + C | Rust | .NET (C#) + Electron |
| **Quellcode** | Open Source | Open Source | Closed Source |
| **Lizenz** | Frei | Frei | Freemium (~30 USD/Jahr für Pro) |
| **FUSE** | Ja | Ja | Ja (FUSE3 auf Linux, WinFSP auf Windows, macfuse auf Mac) |
| **Eigene GUI** | Ja (Web-basiert) | Nein (CLI) | Ja (Electron-basiert) |
| **Plattformen** | Windows, Linux, macOS | Nur Linux | Windows, macOS, Linux (seit Feb 2026) |
| **Map-Anbieter (frei)** | Bing, Google, Here, Yandex, Apple | Bing, Google, Apple, ArcGIS, MapBox, USGS | Bing, ArcGIS, Google |
| **Pro-Anbieter** | -- | -- | Zusätzliche Quellen mit höherer Auflösung, Farbkorrektur |
| **Prefetch** | Tile-basiert | Adaptiv (Ring + Track-Prediction) | Preload-Feature (nur Pro) |
| **Saisons** | Nein | Nein | Ja (ab v4.2.0, standort-/datumsbasiert) |
| **Nachttexturen** | Nein | Nein | Ja (ab v4.1.4) |
| **Base-Package** | Regionaler Overlay-Download | CLI-basierter Package-Install | VHD-basierter Download über GUI |
| **Sim-Unterstützung** | X-Plane 11/12 | X-Plane 12 | X-Plane 11/12 + MSFS |

**Kernunterschied:** XPME basiert auf einer .NET/Electron-Architektur mit einem "Sidecar"-Prozess (C#/.NET Backend), während AutoOrtho und XEarthLayer native FUSE-Implementierungen nutzen. XPME bietet eine ausgereifte GUI, Saisonwechsel und Nachttexturen -- Features, die die anderen beiden nicht haben.

---

## 2. Versionen und Release-Historie

### Eckdaten

| Meilenstein | Version | Datum |
|---|---|---|
| Repo erstellt | -- | 2024-02-09 |
| Erster Release (Windows only) | v1.0.0 | 2024-04-03 |
| Neues UI, verbessertes Laden | 2.0.0 | 2024-07-29 |
| High-Res Bodentexturen (Z8192) | 3.0.0 | 2025-03-14 |
| Neues UI, EOX Cloudless, 10% Perf. | 4.0.0 | 2025-11-23 |
| Saisonwechsel-Feature | 4.2.0 | 2026-01-21 |
| **Erster Linux-Release** (Test) | 4.2.3 | 2026-02-04 |
| **Aktueller Release** | 4.2.5 | 2026-02-08 |

### Gesamtzahl Releases: 82 (Stand: 2026-02-14)

### Release-Kadenz
Die Entwicklung ist hochaktiv. Allein im Januar/Februar 2026 wurden 12 Releases veröffentlicht. Der Entwicklungszyklus ist rapid mit häufigen Bugfix-Releases.

**Quelle:** https://github.com/derekhe/xplane-map-enhancement-release/releases

---

## 3. Architektur

### Technologie-Stack

- **Frontend/GUI:** Electron-basierte Desktop-Anwendung
- **Backend ("Sidecar"):** C# / .NET 10.0 (ASP.NET Core)
- **Dateisystem-Layer:** FUSE3 (Linux), WinFSP (Windows), macfuse (macOS)
- **Download-Manager:** aria2 (externer Prozess)
- **Paketformate:** AppImage + .deb (Linux), .dmg (macOS), .exe-Installer (Windows)

### Funktionsweise

1. **Base-Package:** XPME verwendet vorbereitete "Base Packages" im VHD-Format (Virtual Hard Disk), die per Region heruntergeladen werden. Diese enthalten DSF-Mesh-Daten, die auf Ortho4XP basieren. Die VHD-Dateien werden via FUSE/WinFSP gemountet.

2. **Satellitenbilder-Streaming:** Zur Laufzeit lädt XPME Satelliten-Tiles von den konfigurierten Kartenanbietern und projiziert diese auf das Terrain-Mesh. Die Tiles werden als DDS-Texturen verarbeitet.

3. **Scenery-Integration:** Die gemounteten VHD-Dateien erscheinen als reguläre Scenery-Ordner in X-Planes `Custom Scenery/`-Verzeichnis. Die Namenskonvention folgt dem AutoOrtho-Schema:
   - `yAutoOrtho_Overlays/` (Overlay-Daten)
   - `z_ao_eur/` (Europa), `z_ao_na/` (Nordamerika), etc.

4. **scenery_packs.ini:** XPME platziert seine Einträge automatisch. Wie bei AutoOrtho und XEarthLayer müssen die Streaming-Einträge am Ende der Datei stehen.

### Base-Package Regionen

| Region | Prefix | Ungefähre Größe (VHD) |
|---|---|---|
| Overlays | yAutoOrtho_Overlays | ~7 GB |
| Afrika | z_ao_afr | ~11 GB |
| Asien | z_ao_asi | ~27 GB |
| Australien/Pazifik | z_ao_aus_pac | ~5 GB |
| Europa | z_ao_eur | ~12 GB |
| Nordamerika | z_ao_na | ~20 GB |
| Südamerika | z_ao_sa | ~7 GB |

**Hinweis:** Base Packages werden innerhalb der XPME-GUI heruntergeladen ("Downloader"-Tab). Die VHD-Dateien müssen auf SSD liegen; HDD wird explizit abgeraten.

**Quelle:** https://github.com/derekhe/xplane-map-enhancement-release/releases/tag/basepackage-v2

---

## 4. Linux-Support

### Status: Frühe Beta (seit 2026-02-04)

#### Timeline

| Datum | Ereignis |
|---|---|
| 2024-08-23 | Erste Anfrage (Issue #48): "Will it be version for linux in future?" |
| 2024-08-24 | Entwickler lehnt ab: "Aha, no way." |
| 2025-11-16 | Entwickler öffnet Issue wieder, erwägt Linux wenn genug Nachfrage |
| 2026-01-14 | macOS-Version veröffentlicht, Linux-Support angekündigt |
| 2026-02-01 | Entwickler: "Today fixed several critical issues on linux and I think it is ready to be release soon." |
| 2026-02-04 | **Erster Linux-Test-Release (v4.2.3)** -- getestet auf Ubuntu 24.04 |
| 2026-02-08 | **v4.2.5 mit Linux-Binaries** (AppImage + .deb) |

**Quelle:** https://github.com/derekhe/xplane-map-enhancement-release/issues/48

#### Download-Formate (Linux)

| Format | Dateiname | Größe |
|---|---|---|
| AppImage | `xplane-map-enhancement-4.2.5.AppImage` | ~202 MB |
| Debian-Paket | `xplane-map-enhancement_4.2.5_amd64.deb` | ~141 MB |

#### Linux-Abhängigkeiten

Laut offizieller Dokumentation (https://www.aiflygo.com/docs/xplane-map-enhancement/download/):

```bash
sudo apt install libfuse3-dev aria2 dotnet-runtime-10.0 aspnetcore-runtime-10.0
```

**Kritisches Problem: .NET 10.0 Verfügbarkeit**

.NET 10.0 ist die aktuelle Preview-Version von Microsoft. Sie ist **nicht** in den Standard-Repositorys von Debian oder Fedora enthalten. Installation erfordert das Microsoft-APT-Repository:

```bash
# Debian 12
wget https://packages.microsoft.com/config/debian/12/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb
rm packages-microsoft-prod.deb
sudo apt-get update
sudo apt-get install -y dotnet-runtime-10.0 aspnetcore-runtime-10.0
```

Ein Nutzer auf Nobara Linux (Fedora-basiert) berichtet, dass der C#-Sidecar mit Exit Code 150 fehlschlägt, weil .NET 10.0 dort nicht verfügbar ist (Issue #48, Kommentar vom 2026-02-09). Der Nutzer schlägt vor, auf .NET 8.0 LTS zurückzubauen.

**Quelle:** https://learn.microsoft.com/en-us/dotnet/core/install/linux-debian

#### Getestete Distributionen

- **Ubuntu 24.04** -- vom Entwickler getestet und bestätigt
- **Nobara Linux (Fedora-basiert)** -- .NET 10.0-Problem gemeldet (Issue #48)
- **Debian Stable/Testing** -- nicht explizit getestet, sollte mit Microsoft-Repo funktionieren

---

## 5. Features

### Kostenlose Version (Free)

- Kartenanbieter: Bing, ArcGIS, Google Maps
- Echtzeit-Streaming von Satellitenbildern
- Base-Package-Download (VHD-basiert, regionenweise)
- GUI mit Map-Umschaltung während des Flugs
- Automatische scenery_packs.ini-Konfiguration
- Cache-Management

### Pro-Version (~30 USD/Jahr)

- Höhere Bildauflösung
- Zusätzliche Kartenquellen (Apple Maps, proprietäre Quellen)
- Farbkorrektur und Bildverbesserung (proprietäre Algorithmen)
- **Preload-Feature** (Vorab-Caching, reduziert Stottern)
- Nachttexturen (seit v4.1.4)
- Saisonale Texturen basierend auf Standort und Datum (seit v4.2.0)
- High-Resolution-Modus mit 8192er Bodentextur-Auflösung (seit v3.0.0)

### Lizenzierung

- Ein Gerät pro Lizenz
- Nicht übertragbar
- 7 Tage Rückgaberecht
- Läuft nach Ablauf ab, muss erneuert werden
- Hardware-Wechsel kann Lizenz invalidieren

**Quelle:** https://www.aiflygo.com/docs/license/

---

## 6. Installation auf Debian (vorläufig)

**Warnung:** Linux-Support ist in früher Beta. Die Installationsanleitung basiert auf den verfügbaren Informationen vom 2026-02-14 und kann sich ändern.

### Voraussetzungen

- Debian 12 (Bookworm) oder neuer
- X-Plane 12
- SSD für Base Packages und Cache (HDD wird ausdrücklich abgeraten)
- Stabile Internetverbindung

### Schritt 1: Microsoft .NET Repository hinzufügen

```bash
wget https://packages.microsoft.com/config/debian/12/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb
rm packages-microsoft-prod.deb
sudo apt-get update
```

### Schritt 2: Abhängigkeiten installieren

```bash
sudo apt-get install -y libfuse3-dev aria2 dotnet-runtime-10.0 aspnetcore-runtime-10.0
```

### Schritt 3: XPME installieren

Option A -- .deb-Paket:
```bash
sudo dpkg -i xplane-map-enhancement_4.2.5_amd64.deb
```

Option B -- AppImage:
```bash
chmod +x xplane-map-enhancement-4.2.5.AppImage
./xplane-map-enhancement-4.2.5.AppImage
```

### Schritt 4: Konfiguration

1. XPME starten
2. Einstellungen öffnen (Zahnrad-Icon)
3. X-Plane-Pfad und Base-Package-Pfad setzen
4. Gewünschte Regionen über "Downloader"-Tab herunterladen
5. Kartenanbieter auswählen (Bing/ArcGIS für schnellsten Start)

### Schritt 5: X-Plane starten

1. XPME muss **vor** X-Plane gestartet werden
2. X-Plane starten, Flughafen wählen
3. Ladefortschritt in XPME-Oberfläche beobachten (10.000-20.000 Items typisch)
4. **Reihenfolge beim Beenden:** Erst X-Plane schließen, dann in XPME "Stop" klicken

---

## 7. Performance

### Allgemeine Anforderungen

- **CPU:** Hoch während des Ladens (Bildverarbeitung ist rechenintensiv)
- **RAM:** Versionen ab 4.0.2 verbrauchen laut Nutzerberichten viel RAM
- **Netzwerk:** Stabile Verbindung erforderlich; Netzwerk-Timeouts über 10 Sekunden verursachen temporäres Einfrieren
- **Storage:** SSD zwingend empfohlen; HDD verursacht Performance-Probleme

### Vergleich mit AutoOrtho

Nutzer auf den X-Plane-Foren berichten, dass XPME "viel besser" als AutoOrtho lade, insbesondere dass die Tiles schneller erscheinen. Dies könnte an der VHD-basierten Architektur liegen, die weniger Overhead beim Dateisystem-Zugriff erzeugt.

**Hinweis:** Es gibt keine belastbaren Benchmark-Vergleiche. Die Nutzerberichte sind subjektiv und stammen überwiegend von Windows-Nutzern. Auf Linux gibt es noch keine verlässlichen Performance-Daten, da der Support erst wenige Tage alt ist.

**Quellen:**
- https://forums.x-plane.org/forums/topic/328157-autoortho-vs-map-enhancement/
- https://forums.x-plane.org/forums/topic/321428-map-enhancement-vs-autoortho-quick-comparison/

---

## 8. Bekannte Probleme und Einschränkungen

### Linux-spezifisch

1. **.NET 10.0-Abhängigkeit:** .NET 10.0 ist noch Preview-Software und nicht in Standard-Repos enthalten. Fedora/Nobara-Nutzer können die Abhängigkeit aktuell nicht aus Paketquellen installieren. (Issue #48, 2026-02-09)

2. **Nur auf Ubuntu 24.04 getestet:** Andere Distributionen sind ungetestet. Debian-Kompatibilität wahrscheinlich, aber nicht bestätigt.

3. **AppImage benötigt --no-sandbox:** Laut Nutzerbericht startet die Electron-GUI nur mit `--no-sandbox` Flag.

### Allgemein (alle Plattformen)

| Problem | Beschreibung | Quelle |
|---|---|---|
| CTD bei fehlenden Terrain-Dateien | Crash to Desktop wenn Base-Package-Dateien fehlen | Issue #366 |
| Download-Probleme | Base-Package-Downloads frieren ein oder schlagen fehl | Issues #354, #367, #368 |
| Nachttexturen-Bugs | Funktionieren teilweise nicht mit Pro-Version | Issue #365 |
| Bäume auf Runways | Ohne SimHeaven-Overlays erscheinen Bäume auf Landebahnen | FAQ |
| Ortho4XP-Konflikt | Ortho4XP muss entfernt werden, da es die XPME-Texturen überschreibt | FAQ |
| SimHeaven-Interaktion | Kann zu fehlenden Gebäuden auf Orthos führen | Issue #190 |
| Hoher RAM-Verbrauch | Seit Version 4.0.2 erhöhter Speicherverbrauch | x-plane.to Bewertungen |
| Prozess-Bereinigung | X-Plane-Prozess bleibt nach Schließen manchmal aktiv | FAQ |

**Quelle:** https://github.com/derekhe/xplane-map-enhancement-release/issues

---

## 9. Entwicklungsaktivität

### Repository-Statistiken (Stand 2026-02-14)

| Metrik | Wert |
|---|---|
| GitHub-Sterne | 89 |
| Forks | 8 |
| Offene Issues | 24 |
| Commits (Release-Repo) | 26 |
| Contributors | 2 (derekhe + Copilot) |
| Releases gesamt | 82 |
| Repo erstellt | 2024-02-09 |
| Downloads (x-plane.to) | ~30.900 |
| Bewertung (x-plane.to) | 4.3/5 |

### Entwicklungstempo

- **Sehr aktiv:** 12 Releases allein im Januar/Februar 2026
- **Solo-Entwickler:** Praktisch ein Ein-Mann-Projekt (derekhe), mit Copilot als zweiter Contributor
- **Herkunft:** Der Entwickler pflegt auch das MSFS2020 Map Enhancement (seit 2021), die X-Plane-Variante ist eine Portierung davon
- **Plattform-Expansion:** Windows (seit v1.0.0, April 2024) → macOS (Januar 2026) → Linux (Februar 2026)

### Bewertung der Nachhaltigkeit

- (+) Sehr aktive Entwicklung mit schnellen Bugfixes
- (+) Kommerzielles Modell (Pro-Lizenz) bietet finanzielle Motivation
- (+) Dual-Plattform (MSFS + X-Plane) erweitert die Nutzerbasis
- (-) Ein-Mann-Projekt: Bus-Faktor 1
- (-) Closed Source: Kein Community-Fork möglich bei Projektende
- (-) .NET 10.0-Abhängigkeit auf Linux problematisch (Preview-Runtime)
- (-) Linux-Support ist brandneu und untested

---

## 10. X-Plane Integration

### scenery_packs.ini

XPME konfiguriert die `scenery_packs.ini` automatisch bei der Installation. Die Einträge folgen dem AutoOrtho-Namensschema:

```ini
SCENERY_PACK Custom Scenery/yAutoOrtho_Overlays/
SCENERY_PACK Custom Scenery/z_ao_afr/
SCENERY_PACK Custom Scenery/z_ao_asi/
SCENERY_PACK Custom Scenery/z_ao_aus_pac/
SCENERY_PACK Custom Scenery/z_ao_eur/
SCENERY_PACK Custom Scenery/z_ao_na/
SCENERY_PACK Custom Scenery/z_ao_sa/
```

Diese Einträge müssen am **Ende** der `scenery_packs.ini` stehen (gleiche Regel wie AutoOrtho/XEarthLayer).

### Overlays

XPME liefert eigene Overlays mit (`yAutoOrtho_Overlays`). SimHeaven X-World wird ergänzend empfohlen für Gebäude, Vegetation und Infrastruktur. Ohne SimHeaven können visuelle Artefakte auftreten (z.B. Bäume auf Landebahnen).

### Kompatibilität

- **Ortho4XP:** Muss deinstalliert werden -- überschreibt XPME-Texturen
- **AutoOrtho:** Gleichzeitiger Betrieb nicht empfohlen (gleiche Ordnernamen)
- **XEarthLayer:** Theoretisch koexistierbar (unterschiedliche Präfixe: `zzXEL_` vs `z_ao_`), aber in der Praxis nicht sinnvoll
- **SimHeaven X-World:** Kompatibel und empfohlen

---

## 11. Zusammenfassung und Einordnung für XoL

### Stärken

1. **Feature-Umfang:** Saisonwechsel und Nachttexturen sind einzigartig unter den Streaming-Lösungen
2. **GUI:** Benutzerfreundliche Oberfläche mit Map-Umschaltung, Download-Manager, Monitoring
3. **Cross-Platform:** Einzige Ortho-Streaming-Lösung, die auch MSFS unterstützt
4. **Schnelles Laden:** Nutzerberichte deuten auf schnellere Tile-Ladezeiten als AutoOrtho hin

### Schwächen

1. **Linux-Support extrem jung:** Erst seit 10 Tagen verfügbar (Stand 2026-02-14), nur auf Ubuntu 24.04 getestet
2. **Closed Source:** Kein Einblick in den Code, keine Community-Patches möglich
3. **.NET 10.0-Abhängigkeit:** Preview-Runtime, nicht in Distro-Repos, erfordert Microsoft-Paketquelle
4. **Kommerzielle Lizenz:** Pro-Features kosten ~30 USD/Jahr, gerätgebunden
5. **VHD-Format:** Nicht POSIX-nativ; NTFS-Abhängigkeit auf Windows (Linux-Verhalten unklar)

### Empfehlung für Dokumentation

XPME sollte in der XoL-Dokumentation erwähnt werden, aber mit klarem Hinweis auf den sehr frühen Linux-Support-Status. Eine eigene Seite ist sinnvoll, sobald der Linux-Support stabil ist. Aktuell reicht die Erwähnung in `orthophotography_intro.md` (bereits vorhanden) plus ein Hinweis auf den Beta-Status.

**Priorität:** Beobachtend. Kein vollständiges Kapitel schreiben, solange keine stabilen Linux-Releases und Debian-Testergebnisse vorliegen.

---

## Quellen

1. GitHub Release-Repository: https://github.com/derekhe/xplane-map-enhancement-release
2. Offizielle Website: https://www.aiflygo.com/
3. Download-Anleitung: https://www.aiflygo.com/docs/xplane-map-enhancement/download/
4. FAQ: https://www.aiflygo.com/docs/xplane-map-enhancement/faq/
5. Lizenz: https://www.aiflygo.com/docs/license/
6. Linux-Issue #48: https://github.com/derekhe/xplane-map-enhancement-release/issues/48
7. X-Plane.to Listing: https://x-plane.to/file/1559/x-plane-map-enhancement
8. Base Package v2: https://github.com/derekhe/xplane-map-enhancement-release/releases/tag/basepackage-v2
9. .NET auf Debian: https://learn.microsoft.com/en-us/dotnet/core/install/linux-debian
10. Forum-Thread (X-Plane.org): https://forums.x-plane.org/forums/topic/302105-take-x-plane-scenery-to-new-heights-with-map-enhancement/
11. Forum-Thread (AVSIM): https://www.avsim.com/forums/topic/674423-map-enhancement-or-ortho4xp/
12. MSFS-Vorgänger: https://github.com/derekhe/msfs2020-map-enhancement
