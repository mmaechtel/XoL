---
description: "XLinSpeak ergänzt Sprachausgabe für X-Plane-Plugins unter Linux via speech-dispatcher. Dazu Piper TTS Manager für hochwertige neuronale Sprachsynthese."
---
# XLinSpeak

XLinSpeak ist ein Linux-only [Plugin](../../glossary.md#plugin), das Text-to-Speech (TTS) für [X-Plane](../../glossary.md#x-plane)-Plugins nachrüstet. Unter Windows und macOS nutzt X-Plane die plattformeigenen Sprach-Engines — unter Linux fehlt diese Anbindung. XLinSpeak schließt diese Lücke über speech-dispatcher.

## Hintergrund

- **Entwickler:** uglyDwarf (Michal), XP12-Fork: sparker256 (William Good)
- **Repository:** [github.com/sparker256/XLinSpeak](https://github.com/sparker256/XLinSpeak) (XP12)
- **Original:** [github.com/uglyDwarf/x-plane_plugins](https://github.com/uglyDwarf/x-plane_plugins/tree/master/XLinSpeak)
- **Plattform:** Nur Linux
- **Kompatibilität:** X-Plane 12 (sparker256-Fork)

X-Plane 12 verwendet für das eingebaute ATC vorgenerierte Audiodateien, die auch unter Linux funktionieren. XLinSpeak wird primär für **Plugin-generierte Sprache** benötigt — etwa [Xchecklist](../cockpit/xchecklist.md)-Ansagen, 124thATC oder andere Plugins, die `XPLMSpeakString()` aufrufen.

## Funktionsumfang

- **Binary Hooking:** Fängt X-Planes interne Sprach-Funktionen auf Maschinencode-Ebene ab und leitet den Text an speech-dispatcher weiter
- **Transparente Integration:** Funktioniert automatisch mit allen Plugins, die X-Planes Sprachausgabe nutzen
- **Keine Konfiguration:** Vollständig automatisch nach der Installation — kein UI nötig

## Mehrwert in der Flugsimulation

Ohne XLinSpeak bleibt Linux-Nutzern bei Plugin-Sprachausgabe nur das Text-Overlay auf dem Bildschirm — keine Audioausgabe. Das Plugin stellt die Gleichwertigkeit mit Windows und macOS her, sodass Checklisten-Ansagen, ATC-Plugins und andere sprachgesteuerte Erweiterungen auch unter Linux hörbar sind.

## Installation

**Download:** [sparker256/XLinSpeak](https://github.com/sparker256/XLinSpeak)

Die vorkompilierte Binary befindet sich im Repository unter `XLinSpeak/lin_x64/XLinSpeak.xpl`. Den Ordner `XLinSpeak` nach `Resources/plugins/` kopieren.

### Voraussetzung: speech-dispatcher

```bash
sudo apt install speech-dispatcher
```

Das Standard-Backend espeak-ng funktioniert zuverlässig. Piper als alternatives speech-dispatcher-Backend ist derzeit unzuverlässig (Konfigurationsprobleme, Hänger) — das ist ein anderes Problem als der unten beschriebene Piper TTS Manager, der speech-dispatcher vollständig umgeht.

### Build aus Quellcode

```bash
sudo apt install libspeechd-dev nasm gcc
cd XLinSpeak/src
make
```

---

## Alternative: Piper TTS Manager

Piper TTS Manager (PTTSM) ist ein FlyWithLua-Skript, das hochwertige neuronale Sprachsynthese für X-Plane bereitstellt. Während XLinSpeak `XPLMSpeakString()`-Aufrufe abfängt und über espeak-ng ausgibt (funktional, aber robotisch), nutzt PTTSM neuronale Piper-Sprachmodelle — mit einer Sprachqualität vergleichbar mit Cloud-basierten TTS-Diensten.

- **Entwickler:** JT8D-17 (BK)
- **Repository:** [github.com/JT8D-17/Piper-TTS-Manager-for-X-Plane](https://github.com/JT8D-17/Piper-TTS-Manager-for-X-Plane) (EUPL-1.2)
- **Status:** Keine versionierten Releases
- **Plattform:** Alle (FlyWithLua-basiert)

PTTSM überwacht eine Text-Eingabedatei und generiert WAV-Audio über Piper, sobald neuer Text erscheint. Es wurde für das SimpleATC-Modul von X-ATC-Chatter entwickelt und unterstützt mehrere Sprachmodelle, die verschiedenen Akteuren zugeordnet werden können.

### Abhängigkeiten

- [FlyWithLua](../scripting/flywithlua.md) NG+ für X-Plane 12
- Piper-TTS-Binary — Linux-Build verfügbar bei [OHF-Voice/piper1-gpl](https://github.com/OHF-Voice/piper1-gpl/releases) (Nachfolger des archivierten rhasspy/piper)
- Sprachmodelle (`.onnx` + `.onnx.json`) von [Hugging Face piper-voices](https://huggingface.co/rhasspy/piper-voices/tree/main)


!!! note "XLinSpeak und PTTSM lösen unterschiedliche Probleme"

    XLinSpeak fängt X-Planes interne Sprachfunktionen ab — benötigt für Plugins, die `XPLMSpeakString()` aufrufen. PTTSM stellt eine eigene TTS-Pipeline bereit für Plugins, die Text in eine Datei schreiben (wie X-ATC-Chatter). Beide können ohne Konflikte parallel laufen.

### TTS-Optionen unter Linux

| Lösung | Mechanismus | Qualität | Einsatzbereich |
|--------|-------------|----------|----------------|
| XLinSpeak + espeak-ng | Hookt `XPLMSpeakString()` → speech-dispatcher | Funktional (robotisch) | Plugin-Sprache ([Xchecklist](../cockpit/xchecklist.md), 124thATC) |
| Piper TTS Manager | FlyWithLua + neuronale Piper-Modelle | Hoch (natürlich) | X-ATC-Chatter, eigene TTS |
| X-Plane 12 eingebautes ATC | Vorgenerierte Audiodateien | Gut | Standard-ATC (alle Plattformen) |

## Quellen

- [XLinSpeak XP12 — GitHub](https://github.com/sparker256/XLinSpeak)
- [XLinSpeak Original — GitHub](https://github.com/uglyDwarf/x-plane_plugins/tree/master/XLinSpeak)
- [Native Speech Synthesis for Linux — X-Plane.org Forum](https://forums.x-plane.org/forums/topic/114358-native-speech-synthesis-for-linux/)
- [Piper TTS Manager — GitHub](https://github.com/JT8D-17/Piper-TTS-Manager-for-X-Plane)
- [Piper TTS — GitHub](https://github.com/OHF-Voice/piper1-gpl) (Nachfolger des archivierten rhasspy/piper)
