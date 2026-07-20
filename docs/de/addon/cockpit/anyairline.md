---
description: "AnyAirline für X-Plane 12 — Passagier-Kabinen-Immersion mit KI-Kabinendurchsagen, routenbezogenem Passagier-Manifest, Boarding-Ambiente und kostenloser Passagier-IFE-Karte. Linux-Connector inklusive."
---
# AnyAirline

AnyAirline ist ein Werkzeug für Passagier-Kabinen-Immersion in [X-Plane](../../glossary.md#x-plane) 12 (und Microsoft Flight Simulator 2020/2024). Statt die Kabine als generisches Soundboard zu behandeln, erzeugt es aus Route, Flugzeug und Airline ein Passagier-Manifest und legt routenbezogene Kabinendurchsagen, Boarding-Ambiente und eine Passagier-IFE-Karte über den Flug. Ein Desktop-Connector bindet den Simulator an; der Kabinen-Ablauf wird in einem Online-Workspace vorbereitet.

## Hintergrund

- **Entwickler:** AnyAirline
- **Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/100112-anyairline-ai-cabin-crew-passenger-ife-airline-immersion) · [anyairline.app](https://anyairline.app)
- **Plattformen:** Windows, Linux, macOS (Desktop-Connector, gepackte Runtime enthalten)
- **Kompatibilität:** X-Plane 12, MSFS 2020/2024 (Open Beta)
- **Konto:** Kostenloses AnyAirline-Konto erforderlich (Online-Workspace für Sync, Workshop und Credits)
- **Preismodell:** Freemium — lokale englische Stimme und Passagier-IFE-Karte sind kostenlos

## Funktionsumfang

- **Passagier-Manifest-Pipeline:** Erzeugt aus Route, Flugzeug und Airline benannte Passagiere, Kabinencrew-Rollen, ein echtes Sitzplan-Layout und Passagierkontext — wiederverwendet von Durchsagen und IFE-Ansicht
- **KI-Kabinendurchsagen:** Routenbezogene Gate-, Begrüßungs-, Sicherheits- und Service-Durchsagen; eine kostenlose lokale englische Stimme läuft offline ohne Credits, während kostenpflichtige Cloud-KI reichere Airline-Generierung und mehrsprachige Ausgabe (74 Sprachen) ergänzt
- **Drei Stimm-Modi:** Local AI (kostenlos, Englisch, offline), AI Lite und Full AI (Cloud, credit-basiert)
- **Kabinen-Ambiente:** Boarding- und Deboarding-Musik sowie Gate- und PA-Gongs rund um die Durchsagen
- **Passagier-IFE-Karte (kostenlos):** Zeigt Route, Flugzeugposition, ETA und Live-ähnliche Flugdaten, während der Connector dem Simulator folgt
- **Workshop-Asset-Bibliothek:** Geteilte Boarding-/Deboarding-Musik, Flughafen-Gongs, Sicherheitsmedien, Kabinen-Layouts und wiederverwendbare Flug-Templates (inklusive Cargo-Abläufe)
- **SimBrief-Integration:** Importiert ein OFP und nutzt Route, Flotte, Flugnummer, Zeitplan und Flughafenkontext zur Vorbereitung des Kabinen-Ablaufs

## Mehrwert in der Flugsimulation

AnyAirline füllt die Lücke der stillen Kabine, die die meisten Flugzeuge hinterlassen. Durch den Manifest-Ansatz beziehen sich Durchsagen und IFE-Karte auf die tatsächliche Route, Airline und Sitzaufteilung statt auf ein generisches Preset. Es ist **kein** Virtual-Airline-Management-, ACARS-, Dispatch- oder Logbuch-System — es legt eine Passagier-Kabinen-Ebene über diese Werkzeuge und ergänzt Kabinen-Sound-Plugins wie [KabinXP](kabinxp.md). Besonders für Linux-Setups relevant: Der Connector bringt einen offiziellen Linux-Build mit, sodass die Immersions-Ebene ohne Windows-Host funktioniert.

## Installation

**Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/100112-anyairline-ai-cabin-crew-passenger-ife-airline-immersion) · [anyairline.app](https://anyairline.app)

Ein kostenloses AnyAirline-Konto anlegen und anschließend den Desktop-Connector installieren — die lokale Brücke, die Simulator-Telemetrie und Audiowiedergabe übernimmt. Den Connector zusammen mit X-Plane starten und Durchsagen, Ambiente, Workshop-Medien und die IFE-Karte im Web-Workspace vorbereiten. Die kostenlose Stufe umfasst die lokale englische Kabinenstimme, Workshop-Zugriff und die Passagier-IFE-Karte; kostenpflichtige KI-Credits schalten Cloud-Stimmen, mehrsprachige Generierung und erweiterte Templates frei.

### Linux-Hinweise

Der Connector unterstützt Linux offiziell mit gepackter Python-Runtime (mindestens 8 GB RAM, Ubuntu 22.04/24.04 LTS oder ein kompatibles x64-Desktop-System). Anders als der Windows-Build bringt er FFmpeg nicht mit — `ffmpeg`, `ffprobe` und `espeak-ng` für die lokale Sprachausgabe lassen sich aus den Distributions-Repositorys nachinstallieren. Die Cloud-Funktionen laufen im browserbasierten Workspace und sind plattformunabhängig.

## Quellen

- [AnyAirline — forums.x-plane.org](https://forums.x-plane.org/files/file/100112-anyairline-ai-cabin-crew-passenger-ife-airline-immersion)
- [AnyAirline — offizielle Website](https://anyairline.app)
