# Better Pushback (BetterPushbackC) -- Research Paper

**Recherche-Datum:** 2026-02-15
**Fokus:** Linux-Kompatibilität, Installation, bekannte Probleme, Wartungsstatus
**Referenzplattform:** Debian Stable/Testing, X-Plane 12

---

## 1. Was ist Better Pushback?

Better Pushback ist ein freies (CDDL 1.0) Plugin für X-Plane 11/12, das realistische Pushback-Operationen simuliert. Kernfunktionen:

- **Overhead-Planungsansicht:** Vogelperspektive auf das Vorfeld, in der per Mausklick eine Pushback-Route gezeichnet wird (Kurven, Geraden, Richtungswechsel)
- **Vollautomatischer Pushback:** Nach Routenplanung läuft der Pushback autonom -- der Pilot kann sich auf das Startup-Verfahren konzentrieren
- **Vorwärtsschleppen:** Neben Pushback kann das Flugzeug auch vorwärts geschleppt werden
- **3D-Schleppfahrzeug:** Animiertes Tug-Modell mit korrekter Physik-Simulation (Anlenkung, Radstand)
- **Mehrsprachige Ground Crew:** Sprachausgabe in verschiedenen Sprachen/Akzenten, simuliert lokales Bodenpersonal weltweit
- **Manueller Modus (nur Mod-Fork):** Pushback ohne Vorausplanung, Steuerung per Joystick-Buttons oder Tasten
- **Konfigurierbare Shortcuts:** "Magic Squares" als Schnellzugriff-Buttons (nur Mod-Fork)

**Quelle:** [GitHub README](https://github.com/skiselkov/BetterPushbackC/blob/master/README.md), [forums.x-plane.org](https://forums.x-plane.org/files/file/90556-better-pushback-for-x-plane-1112/)

---

## 2. Repository-Status und Wartung

### 2.1 Original-Repository (skiselkov)

| Eigenschaft | Wert |
|---|---|
| Repository | [skiselkov/BetterPushbackC](https://github.com/skiselkov/BetterPushbackC) |
| Status | **Archiviert** (15.12.2025, read-only) |
| Sprache | C (93,8%), CMake, Shell, Makefile |
| Lizenz | CDDL 1.0 (Common Development and Distribution License) |
| Stars | 501 |
| Forks | 141 |
| Letzte stabile Version | v0.48 (29.03.2023) -- Vulkan & Metal Support |
| Letzte Pre-Release | v0.52 (19.10.2024) -- X-Plane 12 beta 8 Crash-Fix |

**Bewertung:** Das Original-Repository wird nicht mehr gepflegt. Die X-Plane-12-Releases (v0.49--v0.52) blieben alle im Pre-Release-Status. Für X-Plane 12 sollte ein aktiv gepflegter Fork verwendet werden.

**Quelle:** [GitHub Releases](https://github.com/skiselkov/BetterPushbackC/releases)

### 2.2 Aktive Forks

#### olivierbutler/BetterPusbackMod (empfohlen)

| Eigenschaft | Wert |
|---|---|
| Repository | [olivierbutler/BetterPusbackMod](https://github.com/olivierbutler/BetterPusbackMod) |
| Status | **Aktiv gepflegt** |
| Letzte Version | V1.11 (07.10.2025) |
| Plattformen | Windows, Linux, macOS (Intel + ARM) |
| X-Plane 12 | Voll unterstützt, inkl. XP 12.2 |
| Releases | 19 Releases seit Fork-Beginn |
| Vertrieb | GitHub Releases + [forums.x-plane.org](https://forums.x-plane.org/files/file/90556-better-pushback-for-x-plane-1112/) |

**Wichtige Neuerungen gegenüber Original:**
- Manueller Push-Modus (kein Vorausplanen nötig)
- Tür-/GPU-/ASU-Checks vor Pushback-Start
- Magic-Squares-Shortcut-Buttons
- Kompatibilität mit X-Plane 12.2 Brake-Datarefs
- Setup-Fenster mit Preferences
- UFMC-Plugin-Exclusion (experimentell)

**Quelle:** [GitHub Releases olivierbutler](https://github.com/olivierbutler/BetterPusbackMod/releases)

#### qdljerry/BetterPushbackC_XP12

| Eigenschaft | Wert |
|---|---|
| Repository | [qdljerry/BetterPushbackC_XP12](https://github.com/qdljerry/BetterPushbackC_XP12) |
| Status | Letzte Aktivität Mai 2023 |
| Letzte Version | v0.52 (Fix: Tug disconnect in XP12) |

**Bewertung:** Weniger aktiv als olivierbutler-Fork, nur ein Release. Nicht empfohlen.

---

## 3. Linux-Kompatibilität

### 3.1 Grundsätzlich

Better Pushback liefert **native Linux-Binaries** (64-Bit) als `lin.xpl` im Verzeichnis `lin_x64/`. Die Plugin-Archive enthalten Builds für alle drei Plattformen (Windows, Linux, macOS) in einer einzigen ZIP-Datei. Es ist kein Proton/Wine nötig.

Das Plugin wird auf Linux gebaut -- Linux ist sogar die primäre Build-Plattform. Windows-Binaries werden per MinGW-Crosscompile von Linux aus erzeugt.

**Quelle:** [GitHub README](https://github.com/skiselkov/BetterPushbackC/blob/master/README.md)

### 3.2 Bibliotheksabhängigkeiten

Das Plugin basiert auf [libacfutils](https://github.com/skiselkov/libacfutils), einer Utility-Bibliothek für X-Plane-Plugin-Entwicklung. Libacfutils **bündelt** die meisten Abhängigkeiten statisch (zlib, libpng, libjpeg, curl, openal-soft). Dadurch sind die Laufzeitabhängigkeiten minimal.

Laut `ldd`-Analyse (GitHub Issue #220) benötigt das Linux-Binary nur:

- `libm.so.6` (Math-Library)
- `libc.so.6` (C Standard Library)
- `ld-linux-x86-64.so.2` (Dynamic Linker)

**OpenAL:** Die Bibliothek openal-soft ist in libacfutils eingebettet und wird **nicht** vom System geladen. Das Plugin erstellt einen eigenen OpenAL-Kontext (Private Context Approach), wie von Laminar Research für Linux-Plugins empfohlen.

**Quelle:** [GitHub Issue #220](https://github.com/skiselkov/BetterPushbackC/issues/220), [libacfutils](https://github.com/skiselkov/libacfutils), [X-Plane Developer: OpenAL](https://developer.x-plane.com/article/openal/)

### 3.3 Konfigurationspfade (Linux)

Alle Pfade relativ zum X-Plane-12-Installationsverzeichnis:

| Zweck | Pfad |
|---|---|
| Plugin-Verzeichnis | `Resources/plugins/BetterPushback/` |
| Linux-Binary | `Resources/plugins/BetterPushback/lin_x64/BetterPushback.xpl` |
| Konfigurationsdatei | `Output/preferences/BetterPushback.cfg` |
| Routen-Cache | `Output/caches/BetterPushback_routes.dat` |
| Airport-Cache | `Output/caches/BetterPushbackAirports.cache` |
| Dokumentation | `Resources/plugins/BetterPushback/readme.pdf` |

Typischer X-Plane-12-Pfad unter Linux (Steam):
`~/.local/share/Steam/steamapps/common/X-Plane 12/`

---

## 4. Installation auf Linux

### 4.1 Schritt-für-Schritt

1. **Download:** `BetterPushback.zip` von [GitHub Releases (olivierbutler-Fork)](https://github.com/olivierbutler/BetterPusbackMod/releases) herunterladen
2. **Alte Version entfernen:** Falls vorhanden, den Ordner `Resources/plugins/BetterPushback/` komplett löschen
3. **Entpacken:** ZIP-Datei nach `Resources/plugins/` entpacken -- es entsteht der Ordner `BetterPushback/`
4. **Starten:** X-Plane 12 starten, Plugin erscheint unter *Plugins > Better Pushback*

### 4.2 Hinweise

- **Keine Systemabhängigkeiten** notwendig (alle Libraries statisch gelinkt)
- **Nicht** das Repository klonen -- nur das Release-ZIP verwenden
- **Kein** `chmod +x` auf die `.xpl`-Datei nötig -- X-Plane lädt sie via `dlopen()`
- Bei Updates immer den gesamten `BetterPushback/`-Ordner ersetzen (nicht nur die Binary)

---

## 5. Bekannte Linux-spezifische Probleme

### 5.1 "undefined symbol: stat" (v0.52 Pre-Release, Original)

**Betroffen:** Originales skiselkov-Repository, v0.52 auf Ubuntu 20.04
**Symptom:** Plugin lädt nicht, Log zeigt `undefined symbol: stat`
**Ursache:** Vermutlich Kompilierungs-/Linking-Problem in der Pre-Release-Binary
**Lösung:** olivierbutler-Mod-Fork verwenden (Problem dort nicht reproduziert)
**Status:** Issue offen, Repository archiviert

**Quelle:** [GitHub Issue #434](https://github.com/skiselkov/BetterPushbackC/issues/434)

### 5.2 ALSOFT Real-Time-Priority-Warnung

**Betroffen:** Alle Linux-Distributionen (nicht BetterPushback-spezifisch)
**Symptom:** Log-Meldung `[ALSOFT] (EE) Failed to set real-time priority for thread: Operation not permitted (1)`
**Ursache:** openal-soft versucht, Realtime-Scheduling für Audio-Threads zu setzen. Standardmäßig fehlt die Berechtigung.
**Auswirkung:** Rein kosmetisch -- Audio funktioniert trotzdem
**Lösungen:**
- Ignorieren (kein funktionaler Einfluss)
- User zur `realtime`-Gruppe hinzufügen: `sudo usermod -aG realtime $(whoami)`
- Oder in `~/.config/alsoft.conf` deaktivieren:
  ```ini
  [general]
  rt-prio = 0
  ```
- Oder Umgebungsvariable: `ALSOFT_LOGLEVEL=0`

**Quelle:** [openal-soft Issue #554](https://github.com/kcat/openal-soft/issues/554), [BetterPusbackMod Issue #14](https://github.com/olivierbutler/BetterPusbackMod/issues/14)

### 5.3 Symlink-Problem

**Betroffen:** Linux, alle Versionen von BetterPushback
**Symptom:** Plugin lädt nicht, wenn das `BetterPushback/`-Verzeichnis ein Symlink ist (z.B. für Versionsverwaltung). Kein Fehler im Log.
**Workaround:** Plugin direkt im `Resources/plugins/`-Verzeichnis ablegen, keine Symlinks verwenden
**Status:** Offen (Januar 2026), keine Entwickler-Reaktion

**Quelle:** [BetterPusbackMod Issue #29](https://github.com/olivierbutler/BetterPusbackMod/issues/29)

### 5.4 Steam-Library-Konflikte

**Betroffen:** Fedora (und potenziell andere Distributionen mit eigener Steam-Paketierung)
**Symptom:** X-Plane crasht beim Laden des Plugins
**Ursache:** Steam bringt eigene Versionen von Systembibliotheken (z.B. libcurl) mit, die mit Plugins kollidieren können
**Lösung:** Steam neu installieren oder Steam Linux Runtime deaktivieren/aktivieren (je nach Fall)
**Hinweis:** Bei Steam-Runtime-Nutzung können andere Plugins durch CURL-Konflikte ausfallen

**Quelle:** [GitHub Issue #399](https://github.com/skiselkov/BetterPushbackC/issues/399)

### 5.5 Zibo 737 Interaktion

**Betroffen:** Linux (und andere Plattformen)
**Symptom:** BetterPushback reagiert nicht auf Befehle
**Ursache:** Konflikt mit Zibo 737 Plugin-Code, nicht BetterPushback selbst
**Lösung:** Zibo-737-Version aktualisieren

**Quelle:** [BetterPusbackMod Issue #14](https://github.com/olivierbutler/BetterPusbackMod/issues/14)

---

## 6. Flatpak-/Container-Hinweis

Wenn X-Plane 12 als Flatpak (z.B. Steam Flatpak) läuft, gelten zusätzliche Einschränkungen:
- Flatpak-Sandbox kann den Zugriff auf Dateisystem-Pfade einschränken
- Plugins, die mit externen Anwendungen kommunizieren, funktionieren möglicherweise nicht (Shared-Memory-Beschränkung)
- Generelle Empfehlung: Nativen X-Plane-12-Build verwenden, nicht den Proton-Build

---

## 7. Build-Hinweise (für Entwickler)

Falls das Plugin aus Quellcode gebaut werden muss (z.B. bei Linking-Problemen mit Pre-Built-Binaries):

- **Build-Plattform:** Linux oder macOS (Windows per Crosscompile)
- **Build-Voraussetzungen:** Dokumentiert in `qmake/build-win-lin`
- **Build-Befehl:** `./build_release` im Repository-Root
- **Abhängigkeit:** libacfutils (muss separat gebaut werden, ebenfalls archiviert auf GitHub)

**Quelle:** [GitHub README](https://github.com/skiselkov/BetterPushbackC/blob/master/README.md)

---

## 8. Zusammenfassung und Empfehlung

| Aspekt | Bewertung |
|---|---|
| Linux-Unterstützung | Nativ, keine Emulation/Kompatibilitätsschicht |
| Systemabhängigkeiten | Keine (alle Libraries statisch gelinkt) |
| X-Plane 12 Kompatibilität | Voll funktionsfähig (olivierbutler-Fork) |
| Empfohlene Version | [olivierbutler/BetterPusbackMod](https://github.com/olivierbutler/BetterPusbackMod) V1.11+ |
| Bekannte Linux-Probleme | Gering (Symlink-Bug, kosmetische ALSOFT-Warnung) |
| Wartungsstatus | Aktiv gepflegt (olivierbutler-Fork, letztes Release Okt 2025) |
| Lizenz | CDDL 1.0 (Open Source) |

**Empfehlung für XoL-Dokumentation:** Better Pushback ist eines der wenigen X-Plane-Plugins mit nativer Linux-Binary und ohne externe Abhängigkeiten. Die Installation ist trivial (ZIP entpacken). Die einzigen Linux-spezifischen Hinweise betreffen das Symlink-Verhalten und die kosmetische ALSOFT-Warnung. Der olivierbutler-Fork ist der empfohlene Download für X-Plane 12.

---

## Quellenverzeichnis

1. [skiselkov/BetterPushbackC -- GitHub](https://github.com/skiselkov/BetterPushbackC) (Original, archiviert 15.12.2025)
2. [BetterPushbackC Releases -- GitHub](https://github.com/skiselkov/BetterPushbackC/releases)
3. [olivierbutler/BetterPusbackMod -- GitHub](https://github.com/olivierbutler/BetterPusbackMod) (Aktiver Fork)
4. [BetterPusbackMod Releases -- GitHub](https://github.com/olivierbutler/BetterPusbackMod/releases)
5. [qdljerry/BetterPushbackC_XP12 -- GitHub](https://github.com/qdljerry/BetterPushbackC_XP12)
6. [skiselkov/libacfutils -- GitHub](https://github.com/skiselkov/libacfutils)
7. [OpenAL -- X-Plane Developer](https://developer.x-plane.com/article/openal/)
8. [GitHub Issue #220 -- 0.47 and Linux](https://github.com/skiselkov/BetterPushbackC/issues/220)
9. [GitHub Issue #399 -- Crash on Fedora](https://github.com/skiselkov/BetterPushbackC/issues/399)
10. [GitHub Issue #434 -- undefined symbol: stat](https://github.com/skiselkov/BetterPushbackC/issues/434)
11. [BetterPusbackMod Issue #14 -- Linux not responding](https://github.com/olivierbutler/BetterPusbackMod/issues/14)
12. [BetterPusbackMod Issue #29 -- Symlink problem](https://github.com/olivierbutler/BetterPusbackMod/issues/29)
13. [openal-soft Issue #554 -- RT priority warning](https://github.com/kcat/openal-soft/issues/554)
14. [Better Pushback -- forums.x-plane.org](https://forums.x-plane.org/files/file/90556-better-pushback-for-x-plane-1112/)
