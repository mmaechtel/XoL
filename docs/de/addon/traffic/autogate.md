---
description: "AutoGate steuert animierte Fluggastbrücken und Andocksysteme für ältere X-Plane-Szenerien mit dem AutoGate-Toolkit. Legacy-Plugin für XP12."
---
# AutoGate

AutoGate ist ein [Plugin](../../glossary.md#plugin) für [X-Plane](../../glossary.md#x-plane), das animierte Jetways und Docking Guidance Systems für Szenerien bereitstellt, die mit dem AutoGate-Toolkit erstellt wurden.

## Hintergrund

- **Original:** [Marginal/AutoGate](https://github.com/Marginal/AutoGate) von Jonathan Harris (2006–2017, nicht mehr gepflegt)
- **XP12-Fork:** [hotbso/AutoGate](https://github.com/hotbso/AutoGate) (X-Plane 12 kompatibel)
- **Lizenz:** Plugin-Code LGPL-2.1, 3D-Objekte/Texturen CC-BY 3.0
- **Plattformen:** Windows, macOS und Linux (der XP12-Fork liefert native Binaries für alle drei)
- **Kompatibilität:** X-Plane 12 (hotbso-Fork)

!!! warning "Legacy-Plugin"

    AutoGate befindet sich im Wartungsmodus. Für neue Szenerien wird **[openSAM](opensam.md)** empfohlen. AutoGate ist nur noch für ältere Szenerie-Pakete relevant, die mit dem AutoGate-Toolkit erstellt wurden.

## Funktionsumfang

- **Jetways und DGS:** Zwei Jetway-Typen (Glas, Stahl) und vier DGS-Typen (Safedock2S, SafedockT2, Safegate und Marshaller)
- **Andocken bei Beacon-Aus:** Der Jetway dockt an, sobald der Beacon abgeschaltet wird und sich das Flugzeug innerhalb von 0,5 m der Stoppposition befindet

## Mehrwert in der Flugsimulation

AutoGate war das erste Open-Source-Jetway-System für X-Plane und hat den Grundstein für openSAM gelegt. Einige ältere Custom-Szenerien setzen AutoGate-Assets ein. Für diese Szenerien bleibt der hotbso-Fork die einzige X-Plane-12-kompatible Option. AutoGate kann parallel zu [openSAM](opensam.md) und [AutoDGS](autodgs.md) betrieben werden.

## Installation

**Download:** [GitHub Releases (hotbso-Fork)](https://github.com/hotbso/AutoGate/releases)

Die ZIP-Datei nach `Resources/plugins/` entpacken. Die Linux-Binary linkt gegen OpenAL; es muss sichergestellt werden, dass `libopenal1` installiert ist.

## Quellen

- [AutoGate — GitHub (hotbso-Fork für XP12)](https://github.com/hotbso/AutoGate)
- [AutoGate — GitHub (Original von Marginal)](https://github.com/Marginal/AutoGate)
