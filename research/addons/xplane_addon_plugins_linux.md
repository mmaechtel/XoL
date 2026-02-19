# X-Plane Addon-Plugins unter Linux — Research Paper

**Datum:** 2026-02-19
**Quellen:** 18 Primaerquellen verifiziert
**Zielseiten:** Neue Seiten oder Ergaenzung bestehender Addon-Seiten
**Themen:** Xchecklist, XP Walkaround, My FS Flights, Copilot-Plugins, Headtracking, Text-to-Speech

---

## Zusammenfassung

Recherche zu sechs Addon-Themenbloecken fuer X-Plane unter Linux. Ergebnisse: Xchecklist und XP Walkaround laufen nativ unter Linux (lin.xpl). My FS Flights ist bereits dokumentiert (KVM-Workaround). Fuer Copilot-Funktionalitaet gibt es vier Linux-kompatible Optionen (KPCrew, XAnimCopilot, Speedy Copilot, XFirstOfficer), alle kostenlos. Headtracking ist ueber OpenTrack + HeadTrack-Plugin geloest, ergaenzt die bestehende LinuxTrack-Seite. TTS hat zwei Schichten: XLinSpeak (bereits dokumentiert) fuer Plugin-Speech und Piper TTS Manager fuer hochwertige neuronale Sprachsynthese.

---

## 1. Xchecklist

### Steckbrief

| Eigenschaft | Wert |
|---|---|
| Entwickler | sparker256 (Bill Good), uglyDwarf (Michal Navratil) |
| Version | 1.53 (Januar 2026) |
| Lizenz | MIT (Open Source) |
| Plattform | Linux, Windows, macOS (native lin.xpl) |
| Kompatibilitaet | X-Plane 10, 11, 12 |
| Preis | Kostenlos |
| GitHub | [sparker256/xchecklist](https://github.com/sparker256/xchecklist) |
| Forum | [X-Plane.org](https://forums.x-plane.org/files/file/20785-xchecklist-linwinmac/) |

### Funktionen

- Interaktive Checklisten im 2D- und VR-Cockpit
- Text-to-Speech-Vorlesung von Checklist-Items (ueber `sw_remark:` Kommando)
- Anpassbare Checklisten pro Flugzeug via `clist.txt`-Dateien
- Companion-Tools: Simon (Checklisten-Editor), Checker (Validierung)
- Community-Checklisten fuer Zibo 737, ToLiss, viele weitere

### Linux-Spezifika

- **TTS via libspeechd:** Xchecklist nutzt speech-dispatcher fuer Sprachausgabe unter Linux — derselbe Stack wie XLinSpeak
- **Build-Abhaengigkeiten:** `build-essential cmake git freeglut3-dev libudev-dev libopenal-dev libspeechd-dev`
- **Build-Anleitung:**
  ```bash
  git clone https://github.com/sparker256/xchecklist.git
  cd xchecklist
  cmake -S ./src -B ./build -DCMAKE_BUILD_TYPE=RelWithDebInfo
  cmake --build ./build
  cp ./build/lin.xpl ./Xchecklist/64/
  ```
- Vorkompilierte Binaries in den GitHub-Releases enthalten (lin.xpl) — Build aus Quellcode optional
- Historischer Bug (v1.11a): Start-Problem unter Linux wegen fehlender Libraries — inzwischen behoben

### Querverweis zu XLinSpeak

Xchecklist nutzt `XPLMSpeakString()` fuer Sprachausgabe. Auf Linux ist XLinSpeak erforderlich, damit diese Aufrufe hoerbar werden (speech-dispatcher als Backend). Alternativ nutzt Xchecklist auch direkt libspeechd fuer eigene TTS-Ausgabe via `sw_remark:`.

### Quellen

| # | Quelle | Domain | Datum | Relevanz |
|---|--------|--------|-------|----------|
| 1 | GitHub Repository | github.com | 2026-01 | HOCH |
| 2 | GitHub Releases v1.53 | github.com | 2026-01 | HOCH |
| 3 | X-Plane.org Forum | forums.x-plane.org | laufend | MITTEL |

---

## 2. XP Walkaround

### Steckbrief

| Eigenschaft | Wert |
|---|---|
| Entwickler | VFRScenery |
| Version | 1.3 (Mai 2025) |
| Lizenz | Proprietaer (kommerziell) |
| Plattform | Windows, macOS, Linux (native lin.xpl) |
| Kompatibilitaet | X-Plane 11 und 12 |
| Preis | US$19.99 |
| Store | [X-Plane.org Store](https://store.x-plane.org/WalkAround-Plugin-for-X-Plane-12-and-11_p_1687.html) |

### Funktionen

- Pre-Flight Walkaround-Inspektion wie ein professioneller Pilot
- Kompatibel mit den meisten Flugzeugen und Hubschraubern
- Interaktion mit Aussen-Elementen: Chocks, Remove-before-flight-Tags, Tueren
- v1.3: Apple M2-Unterstuetzung, E-Taste zum Aufstehen, Leertaste+Klick-Interaktion
- Funktioniert mit Default-Aircraft und vielen Third-Party-Flugzeugen (ToLiss, FlightFactor, IXEG, Rotate MD-11, Aerobask)

### Linux-Spezifika

- Nativ fuer Linux kompiliert — keine besonderen Abhaengigkeiten dokumentiert
- Keine bekannten Linux-spezifischen Probleme in Foren oder Produktseiten
- Geschlossener Quellcode — kein Build aus Quellcode moeglich

### Kostenlose Alternative

**SimpleWalkaround** (kostenlos, [x-plane.to](https://x-plane.to/file/1877/simplewalkaround)): Aehnliche Funktionalitaet ohne SASL3-Abhaengigkeit. Linux-Support nicht explizit bestaetigt.

### Quellen

| # | Quelle | Domain | Datum | Relevanz |
|---|--------|--------|-------|----------|
| 1 | X-Plane.org Store | store.x-plane.org | 2025-05 | HOCH |
| 2 | X-Plane.org Forum | forums.x-plane.org | 2025 | MITTEL |

---

## 3. My FS Flights

**Bereits dokumentiert** unter `docs/{lang}/addon/kvm/myfs_flights.md`.

Windows-only mit KVM/QEMU-Workaround. Cloud-basiertes Flight-Tracking mit AI-Landing-Analyse. Keine Aenderungen noetig — die Seite ist aktuell.

---

## 4. Copilot-Plugins

### Uebersicht: Linux-Kompatibilitaet

| Plugin | Linux | Typ | XP12 | Preis | Flugzeuge |
|---|---|---|---|---|---|
| **KPCrew** | Ja (FlyWithLua) | Prozedur-basierter FO | Ja | Kostenlos (GPL-3.0) | Multi-Aircraft |
| **XAnimCopilot** | Ja | 3D-animierter FO | Ja | Kostenlos (CC BY-NC) | Nur 737 (Zibo/LevelUp) |
| **Speedy Copilot** | Ja (FlyWithLua) | Prozedur-basierter FO | Ja | Kostenlos | Nur 737 (Zibo/LevelUp) |
| **XFirstOfficer** | Wahrscheinlich (unbestaetigt) | Prozedur-basierter FO | Ja | Kostenlos | Multi-Aircraft |
| **SmartCopilot** | Ja | Shared Cockpit (kein AI-FO) | Ja | EUR 19.95+ | Alle |
| **X-CPL-Pilot** | Beta | Karriere-Simulation (kein FO) | Ja | Kostenlos | Alle |
| **JARDesign CoPilot** | Nein | 3D-animierter FO mit Sprache | Teilweise | USD 14.95 | Diverse |
| **PlaneCommand** | Nein | Sprachsteuerung | Unklar | USD 27 (Pro) | Alle |

### 4.1 KPCrew (Empfehlung)

| Eigenschaft | Wert |
|---|---|
| Entwickler | prokopiu |
| Version | 2.3-alpha10 (April 2025) |
| Plattform | Alle (FlyWithLua-basiert) |
| Preis | Kostenlos (GPL-3.0) |
| GitHub | [prokopiu/kpcrew](https://github.com/prokopiu/kpcrew) |

- Virtueller First Officer modelliert nach FS2Crew-Konzept
- Volle SOPs fuer Zibo B738, XP12 CitationX, A330-300, E-Jets, MD-82
- Default-Flow fuer ToLiss A319/A320/A321
- SimBrief-XML-Integration, METAR-Parsing
- Funktioniert unter Linux via FlyWithLua — keine zusaetzlichen Abhaengigkeiten
- **Alpha-Status**, aber aktiv entwickelt

### 4.2 XAnimCopilot

| Eigenschaft | Wert |
|---|---|
| Entwickler | Community |
| Version | 7.0 |
| Plattform | Windows, Linux, macOS |
| Preis | Kostenlos (CC BY-NC) |
| Download | [X-Plane.org Forum](https://forums.x-plane.org/files/file/68001-xanimcopilot-70-smart-animated-copilot-for-738-zibo737-ultimate/) |

- **3D-animierte Copilot-Figur** im rechten Sitz der 737
- Checklisten, Callouts, Prozeduren nach realen 737-Ablaeufen
- Sprachbefehl-Unterstuetzung
- Nur fuer Zibo B738 und LevelUp 737NG Series
- Wird als Aircraft-Plugin installiert (im `plugins/`-Ordner des Flugzeugs)

### 4.3 Speedy Copilot

- FlyWithLua-Skript fuer 737 Pilot-Monitoring-Aufgaben
- Nur Zibo B738 und LevelUp 737NG
- Funktioniert unter Linux via FlyWithLua
- Download: [X-Plane.org Forum](https://forums.x-plane.org/files/file/55510-speedy-copilot-737ng-series-for-zibo-and-levelup/)

### 4.4 XFirstOfficer

- Entwickler: ParrotSim
- Version: 1.9.0 (Procedure-Files bis Oktober 2025 aktualisiert)
- AI Virtual First Officer: Checklisten lesen, Schalter umlegen, Prozeduren ausfuehren
- Multi-Aircraft: Cessna 172 (Default), Community-Files fuer Zibo, ToLiss, iniBuilds A300, Felis B747, FlyJSim Q4XP
- **Linux-Support nicht explizit bestaetigt** — muesste als XPLM-Plugin lin.xpl haben, aber keine Bestaetigung in Dokumentation
- Download: [X-Plane.org Forum](https://forums.x-plane.org/files/file/55984-xfirstofficer-an-x-plane-copilot-plugin/)

### 4.5 SmartCopilot (Shared Cockpit, kein AI-FO)

- Sky4Crew, v3 (stabil) / v4 (Public Beta)
- **Shared Cockpit:** Zwei echte Piloten fliegen zusammen ueber Netzwerk
- Kein AI-Copilot — erfordert zweiten menschlichen Mitspieler
- Linux-Support: Ja
- Preis: EUR 19.95+ (v3), Abo-Modell geplant (v4)

### 4.6 Nicht Linux-kompatibel

- **JARDesign CoPilot:** Setzt Windows Speech Recognition voraus — fundamental inkompatibel mit Linux
- **PlaneCommand:** Nur Windows und macOS

### Quellen

| # | Quelle | Domain | Datum | Relevanz |
|---|--------|--------|-------|----------|
| 1 | KPCrew GitHub | github.com | 2025-04 | HOCH |
| 2 | XAnimCopilot Forum | forums.x-plane.org | laufend | HOCH |
| 3 | XFirstOfficer Forum | forums.x-plane.org | 2025-10 | MITTEL |
| 4 | SmartCopilot Website | sky4crew.com | 2025 | MITTEL |
| 5 | Speedy Copilot Forum | forums.x-plane.org | 2024 | MITTEL |

---

## 5. Headtracking

### Bestehende XoL-Dokumentation

- `docs/{lang}/addon/cockpit/linuxtrack.md` — LinuxTrack/X-IR Fork
- `docs/{lang}/addon/cockpit/xcamera.md` — XCamera (erwaehnt OpenTrack)

### 5.1 OpenTrack

| Eigenschaft | Wert |
|---|---|
| Version | 2026.1.0 (Dezember 2025) |
| Plattform | Windows, Linux, macOS (nativ) |
| Lizenz | ISC |
| GitHub | [opentrack/opentrack](https://github.com/opentrack/opentrack) |

**Linux-Build:**

```bash
sudo apt install build-essential cmake git libopencv-dev libproc2-dev qt6-base-private-dev qt6-tools-dev
git clone https://github.com/opentrack/opentrack
cd opentrack && cmake -B build && cd build && make -j$(nproc)
```

Auch verfuegbar via AUR (`opentrack`, `opentrack-git`) und Snap (`snap install opentrack`).

**Verbindung zu X-Plane:**

Zwei Methoden:

1. **OpenTrack X-Plane Plugin** (eingebaut, Shared Memory) — unter Linux/XP12 laut Community-Berichten unzuverlaessig
2. **UDP-Ausgabe an HeadTrack-Plugin** (empfohlen) — OpenTrack Output auf "UDP over network", IP `127.0.0.1`, Port `4242`

**Unterstuetzte Tracker (Linux-relevant):**

- **NeuralNet Tracker:** AI-basierte Kopfpositionserkennung ueber Webcam — kein Hardware noetig. Erfordert ONNX Runtime. Beste Zero-Hardware-Option.
- **PointTracker:** 3 IR-LEDs oder Reflexpunkte + IR-Kamera
- **ArUco-Papiermarker:** Gedruckter Marker vor Webcam
- **UDP-Relay:** Empfaengt Daten von SmoothTrack (Smartphone-App)

### 5.2 HeadTrack (X-Plane Plugin)

| Eigenschaft | Wert |
|---|---|
| Entwickler | amyinorbit |
| Version | 2209.1r2 (Oktober 2022) |
| Plattform | Windows, Linux, macOS |
| Lizenz | MIT |
| GitHub | [amyinorbit/headtrack](https://github.com/amyinorbit/headtrack) |

- Leichtgewichtiges X-Plane-Plugin, empfaengt 6DOF-Daten ueber **UDP Port 4242**
- Kein Bestandteil von X-Plane — separates Third-Party-Plugin
- Vorkompilierte lin_x64/htrack.xpl in Releases enthalten
- Konfigurations-GUI in X-Plane: Empfindlichkeit, Glaettung, Response-Kurven
- Urspruenglich fuer SmoothTrack entwickelt, funktioniert mit jedem UDP-kompatiblen Tracker

**Empfohlene Bridge** zwischen OpenTrack und X-Plane 12 unter Linux.

### 5.3 SmoothTrack (Smartphone)

- Smartphone-App (iOS/Android), $9.99
- Sendet Head-Tracking-Daten per WiFi/UDP
- **Linux-Anbindung:** SmoothTrack → WiFi/UDP → OpenTrack (Linux) → UDP:4242 → HeadTrack-Plugin
- Alternativ: Direkt an HeadTrack auf Port 4242 (ohne OpenTrack-Zwischenschritt)

### 5.4 AITrack

- **Nicht empfohlen fuer Linux:** Hauptprojekt Windows-only, Linux-Fork (mdk97/aitrack-linux) archiviert und nicht mehr gewartet
- **Ersetzt durch:** OpenTrack NeuralNet Tracker — gleiche Funktionalitaet (AI-Webcam-Tracking), nativ in OpenTrack integriert

### Empfohlener Linux-Stack

```
Input (eine Option waehlen):
  - OpenTrack NeuralNet Tracker (Webcam, keine Hardware)
  - PointTracker (IR-LEDs + Kamera)
  - SmoothTrack (Smartphone-App, $9.99)
       |
       v
OpenTrack (Linux, nativ gebaut)
  - Filter, Response-Kurven, Tuning
  - Output: "UDP over network" → 127.0.0.1:4242
       |
       v
HeadTrack-Plugin (amyinorbit) in X-Plane
  - Empfaengt UDP auf Port 4242
  - Feintuning ueber In-Sim-GUI
```

### Quellen

| # | Quelle | Domain | Datum | Relevanz |
|---|--------|--------|-------|----------|
| 1 | OpenTrack GitHub | github.com | 2025-12 | HOCH |
| 2 | OpenTrack Discussion #1836 (Linux Fix) | github.com | 2024 | HOCH |
| 3 | HeadTrack GitHub | github.com | 2022-10 | HOCH |
| 4 | SmoothTrack Website | smoothtrack.app | 2025 | MITTEL |
| 5 | AITrack Linux Fork (archiviert) | github.com | 2025 | GERING |

---

## 6. Text-to-Speech (TTS)

### Bestehende XoL-Dokumentation

- `docs/{lang}/addon/tools/xlinspeak.md` — XLinSpeak + speech-dispatcher
- `docs/{lang}/addon/kvm/sayintentions.md` — SayIntentions.AI (Windows-only, KVM-Workaround)

### Zwei-Schichten-Modell

Unter Linux gibt es zwei getrennte TTS-Ebenen:

1. **Low-Level Plugin-Speech** (`XPLMSpeakString()`) — geloest durch XLinSpeak + speech-dispatcher + espeak-ng. Qualitaet funktional, aber robotisch.
2. **High-Quality TTS** — geloest durch Piper TTS Manager + FlyWithLua + neuronale Sprachmodelle. Dramatisch bessere Qualitaet.

### X-Plane 12 Built-in ATC Audio

- Nutzt **voraufgezeichnete Audiodateien**, kein Runtime-TTS
- Vocabular wurde mit Cloud-basiertem TTS generiert und als WAV-Dateien ausgeliefert
- **Funktioniert identisch auf allen Plattformen** — kein TTS-Engine noetig
- Community kann Aussprachen ueber oeffentliche Spreadsheets verbessern (SSML-Standard)

### XLinSpeak (bereits dokumentiert)

- Interceptet `XPLMSpeakString()` per Binary Hooking
- Routet Text an speech-dispatcher → espeak-ng → Audioausgabe
- Erforderlich fuer: Xchecklist, 124thATC, DK Toliss Callout, andere Plugins
- **Piper als speech-dispatcher-Backend verursacht derzeit einen Crash** (bereits in XoL dokumentiert)

### 6.1 Piper TTS Manager (PTTSM) — NEU

| Eigenschaft | Wert |
|---|---|
| Entwickler | JT8D-17 (BK) |
| Plattform | Alle (FlyWithLua-basiert) |
| Lizenz | EUPL-1.2 |
| Status | Pre-Release / fruehe Entwicklung |
| GitHub | [JT8D-17/Piper-TTS-Manager-for-X-Plane](https://github.com/JT8D-17/Piper-TTS-Manager-for-X-Plane) |

**Funktionsweise:**

- FlyWithLua-Skript in X-Plane
- Ueberwacht eine Text-Eingabedatei per 1-Sekunden-Watchdog
- Plugin schreibt Text → PTTSM splittet in Actor + Dialog → Zuordnung zu Piper-Sprachmodell → WAV-Generierung → Wiedergabe
- Entwickelt fuer X-ATC-Chatter SimpleATC-Modul

**Abhaengigkeiten:**

- FlyWithLua NG+ (XP12, v2.8.1+)
- Piper TTS Binary ([TheLouisHong/piper Fork](https://github.com/TheLouisHong/piper/releases), Linux-Binary verfuegbar)
- Voice-Modelle (.onnx + .onnx.json) von [Hugging Face piper-voices](https://huggingface.co/rhasspy/piper-voices/tree/main)

**Bestaetigt auf Linux:** Arch Linux, Fedora 39, Ubuntu 22.04.

**Unterschied zu XLinSpeak:** PTTSM erzeugt Sprache ueber neuronale Netzwerk-Modelle (hohe Qualitaet, aehnlich Google TTS). XLinSpeak nutzt speech-dispatcher mit espeak-ng (niedrigere Qualitaet, robotisch). Beide loesen unterschiedliche Probleme — XLinSpeak fuer `XPLMSpeakString()`-Aufrufe, PTTSM fuer X-ATC-Chatter und eigene TTS-Pipelines.

### TTS-Optionen-Matrix

| Loesung | Typ | Linux | Qualitaet | Einsatz |
|---|---|:---:|:---:|---|
| X-Plane 12 Built-in ATC | Voraufgezeichnet | Ja | Gut | Standard-ATC |
| XLinSpeak + espeak-ng | speech-dispatcher Hook | Ja | Niedrig (robotisch) | Plugin-Speech |
| Piper TTS Manager | FlyWithLua + Piper Neural TTS | Ja | Hoch | X-ATC-Chatter, Custom TTS |
| SayIntentions.AI | Cloud AI ATC | **Nur Windows** | Sehr hoch | AI-gesteuertes ATC |
| Pilot2ATC | Standalone ATC App | **Nur Windows** | Mittel | ATC-Ersatz |

### Quellen

| # | Quelle | Domain | Datum | Relevanz |
|---|--------|--------|-------|----------|
| 1 | Piper TTS Manager GitHub | github.com | 2025 | HOCH |
| 2 | Piper TTS (rhasspy) | github.com | 2025 | HOCH |
| 3 | X-Plane Developer: ATC Speech | developer.x-plane.com | 2024 | MITTEL |
| 4 | XLinSpeak GitHub | github.com | 2025 | MITTEL |

---

## Gesamtquellen

| # | Quelle | Domain | Datum | Relevanz |
|---|--------|--------|-------|----------|
| 1 | Xchecklist GitHub | github.com | 2026-01 | HOCH |
| 2 | OpenTrack GitHub | github.com | 2025-12 | HOCH |
| 3 | HeadTrack GitHub | github.com | 2022-10 | HOCH |
| 4 | KPCrew GitHub | github.com | 2025-04 | HOCH |
| 5 | Piper TTS Manager GitHub | github.com | 2025 | HOCH |
| 6 | XP Walkaround Store | store.x-plane.org | 2025-05 | HOCH |
| 7 | XAnimCopilot Forum | forums.x-plane.org | laufend | HOCH |
| 8 | SmoothTrack Website | smoothtrack.app | 2025 | MITTEL |
| 9 | SmartCopilot Website | sky4crew.com | 2025 | MITTEL |
| 10 | XFirstOfficer Forum | forums.x-plane.org | 2025-10 | MITTEL |
| 11 | OpenTrack Discussion #1836 | github.com | 2024 | HOCH |
| 12 | Piper TTS (rhasspy) | github.com | 2025 | HOCH |
| 13 | X-Plane Developer: ATC Speech | developer.x-plane.com | 2024 | MITTEL |
| 14 | Speedy Copilot Forum | forums.x-plane.org | 2024 | MITTEL |
| 15 | X-CPL-Pilot Website | xcplpilot.com | 2026-01 | MITTEL |
| 16 | LinuxTrack X-IR GitHub | github.com | 2026-01 | HOCH |
| 17 | SimpleWalkaround | x-plane.to | 2024 | GERING |
| 18 | AITrack Linux Fork (archiviert) | github.com | 2025 | GERING |
