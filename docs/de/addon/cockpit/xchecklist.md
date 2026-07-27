---
description: "Xchecklist für X-Plane unter Linux — interaktive Checklisten mit Sprachausgabe über speech-dispatcher. Installation, TTS-Einrichtung und XLinSpeak-Integration."
---
# Xchecklist

Xchecklist ist ein Open-Source-[Plugin](../../glossary.md#plugin) für [X-Plane](../../glossary.md#x-plane), das interaktive Checklisten mit Sprachausgabe bietet. Unter Linux erfolgt die Sprachausgabe über speech-dispatcher — derselbe Stack, den auch [XLinSpeak](../tools/xlinspeak.md) nutzt.

## Hintergrund

- **Entwickler:** sparker256 (William Good), uglyDwarf (Michal Navratil)
- **Repository:** [github.com/sparker256/xchecklist](https://github.com/sparker256/xchecklist) (MIT-Lizenz)
- **Plattformen:** Windows, macOS, Linux (natives `lin.xpl`)
- **Kompatibilität:** X-Plane 10, 11, 12

Xchecklist wird aktiv weiterentwickelt; der Forum-Download enthält vorkompilierte Binaries für alle drei Plattformen. Das Plugin nutzt das XPLM SDK und benötigt weder FlyWithLua noch ein anderes Scripting-Framework.

## Funktionsumfang

- **Interaktive Checklisten:** 2D-Fenster und VR-Overlay mit automatischer Fortschrittsverfolgung für jede Flugphase
- **Sprachausgabe:** Eine Copilot-Stimme liest die Checklist-Items vor; der `sw_remark:`-Befehl ergänzt zusätzliche Zeilen, die gesprochen, aber nicht als Item angezeigt werden
- **Flugzeugspezifische Checklisten:** Eigene `clist.txt`-Dateien pro Flugzeug — Community-Checklisten für Zibo 737, ToLiss und viele weitere verfügbar
- **Companion-Tools:** Simon (TTS-Hilfsprozess für Sprachausgabe unter Linux/macOS) und Checker (Validierungstool für eigene Checklisten)

## Mehrwert in der Flugsimulation

Unter Windows und macOS können X-Plane-Plugins die plattformeigenen Sprach-Engines für Checklisten-Callouts nutzen. Unter Linux fehlt diese Integration — Xchecklist schließt die Lücke mit nativer TTS über speech-dispatcher und liefert hörbare Sprachausgabe ohne Windows-Abhängigkeiten. Zusammen mit der interaktiven Fortschrittsverfolgung ergibt sich ein vollständiger Checklisten-Workflow im Linux-Cockpit.

## Installation

**Download:** [Xchecklist — x-plane.org](https://forums.x-plane.org/files/file/20785-xchecklist-linwinmac/)

Die ZIP-Datei nach `Resources/plugins/` entpacken. Dadurch entsteht der Ordner `Xchecklist/` mit dem Linux-Binary unter `64/lin.xpl`.

Für den Grundbetrieb sind keine zusätzlichen Systempakete erforderlich. Für TTS-Unterstützung siehe den nächsten Abschnitt.

### Build aus Quellcode

Der Build aus Quellcode ist optional — der Forum-Download enthält bereits die vorkompilierten Binaries. Das GitHub-Repository liefert nur Quellcode; die dortigen Release-Tags wurden seit 2017 nicht mehr aktualisiert.

```bash
sudo apt install build-essential cmake git freeglut3-dev libudev-dev libopenal-dev libspeechd-dev
git clone https://github.com/sparker256/xchecklist.git
cd xchecklist
cmake -S ./src -B ./build -DCMAKE_BUILD_TYPE=RelWithDebInfo
cmake --build ./build
cp ./build/lin.xpl ./Xchecklist/64/
```

## Sprachausgabe unter Linux

Xchecklist startet einen Companion-Prozess (`simon`), der sich über `libspeechd` mit speech-dispatcher verbindet. Darüber laufen sowohl die gesprochenen Checklist-Items als auch die zusätzlichen `sw_remark:`-Zeilen. Das Plugin selbst ruft unter Linux kein `XPLMSpeakString()` auf — die gesamte Sprachausgabe läuft über den simon/speech-dispatcher-Mechanismus.

!!! tip "Empfohlene Einrichtung"

    [XLinSpeak](../tools/xlinspeak.md) zusammen mit Xchecklist installieren. Während Xchecklist die eigene Sprachausgabe über simon/speech-dispatcher übernimmt, fängt XLinSpeak `XPLMSpeakString()`-Aufrufe von anderen Plugins ab, die unter Linux sonst nur stumme Text-Overlays erzeugen würden.

### Voraussetzungen

```bash
sudo apt install speech-dispatcher
```

Das Standard-Backend espeak-ng funktioniert zuverlässig. Prüfen, ob speech-dispatcher läuft:

```bash
spd-say "checklist test"
```

Falls kein Audio zu hören ist, den speech-dispatcher-Dienst und die korrekte Audioausgabe überprüfen.

## Quellen

- [Xchecklist — GitHub](https://github.com/sparker256/xchecklist)
- [Xchecklist — forums.x-plane.org](https://forums.x-plane.org/files/file/20785-xchecklist-linwinmac/)
- [XLinSpeak — GitHub](https://github.com/sparker256/XLinSpeak)
- [speech-dispatcher — GitHub](https://github.com/brailcom/speechd)
