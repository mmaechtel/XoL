# XLinSpeak

XLinSpeak ist ein Linux-only [Plugin](../glossary.md#plugin), das Text-to-Speech (TTS) für X-Plane-Plugins nachrüstet. Unter Windows und macOS nutzt X-Plane die plattformeigenen Sprach-Engines — unter Linux fehlt diese Anbindung. XLinSpeak schließt diese Lücke über speech-dispatcher.

## Hintergrund

- **Entwickler:** uglyDwarf (Michal), XP12-Fork: sparker256 (William Good)
- **Repository:** [github.com/sparker256/XLinSpeak](https://github.com/sparker256/XLinSpeak) (XP12)
- **Original:** [github.com/uglyDwarf/x-plane_plugins](https://github.com/uglyDwarf/x-plane_plugins/tree/master/XLinSpeak)
- **Plattform:** Nur Linux
- **Kompatibilität:** X-Plane 12 (sparker256-Fork)
- **Preis:** Kostenlos

X-Plane 12 verwendet für das eingebaute ATC voraufgezeichnete Audiodateien, die auch unter Linux funktionieren. XLinSpeak wird primär für **Plugin-generierte Sprache** benötigt — etwa XChecklist-Ansagen, 124thATC oder andere Plugins, die `XPLMSpeakString()` aufrufen.

## Funktionsumfang

- **Binary Hooking:** Fängt X-Planes interne Sprach-Funktionen auf Maschinencode-Ebene ab und leitet den Text an speech-dispatcher weiter
- **Transparente Integration:** Funktioniert automatisch mit allen Plugins, die X-Planes Sprachausgabe nutzen
- **Keine Konfiguration:** Vollständig automatisch nach der Installation — kein UI nötig

## Mehrwert in der Flugsimulation

Ohne XLinSpeak bleibt Linux-Nutzern bei Plugin-Sprachausgabe nur der Textoverlap auf dem Bildschirm — keine Audioausgabe. Das Plugin stellt die Gleichwertigkeit mit Windows und macOS her, sodass Checklisten-Ansagen, ATC-Plugins und andere sprachgesteuerte Erweiterungen auch unter Linux hörbar sind.

## Installation

**Download:** [sparker256/XLinSpeak](https://github.com/sparker256/XLinSpeak)

Die vorkompilierte Binary befindet sich im Repository unter `XLinSpeak/lin_x64/XLinSpeak.xpl`. Den Ordner `XLinSpeak` nach `Resources/plugins/` kopieren.

### Voraussetzung: speech-dispatcher

```bash
sudo apt install speech-dispatcher
```

Der Standard-Backend espeak-ng funktioniert zuverlässig. Piper als alternatives TTS-Backend verursacht derzeit einen Absturz.

### Build aus Quellcode

```bash
sudo apt install libspeechd-dev nasm gcc
cd XLinSpeak/src
make
```

## Quellen

- [XLinSpeak XP12 — GitHub](https://github.com/sparker256/XLinSpeak)
- [XLinSpeak Original — GitHub](https://github.com/uglyDwarf/x-plane_plugins/tree/master/XLinSpeak)
- [Native Speech Synthesis for Linux — X-Plane.org Forum](https://forums.x-plane.org/forums/topic/114358-native-speech-synthesis-for-linux/)
