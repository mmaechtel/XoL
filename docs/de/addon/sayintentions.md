# SayIntentions.AI

SayIntentions.AI ist ein KI-basiertes Air Traffic Control (ATC) System für Flugsimulatoren. Der Pilot kommuniziert per Mikrofon mit der KI-gesteuerten Flugsicherung — das System nutzt Spracherkennung und große Sprachmodelle (LLM) für natürliche, dynamische Antworten. Der SayIntentions Client ist **ausschließlich für Windows** verfügbar — unter Linux ist eine Windows-VM (KVM/QEMU) mit UDP-Port-Forwarding erforderlich, um den Client parallel zu [X-Plane](../glossary.md#x-plane) auf dem Host zu betreiben.

## Hintergrund

- **Entwickler:** SayAgain Solutions, LLC
- **Website:** [sayintentions.ai](https://www.sayintentions.ai/)
- **Plattformen:** Nur Windows 10/11
- **Kompatibilität:** X-Plane 11/12, MSFS 2020/2024, Prepar3D v5/v6
- **Preis:** Premium $18.95/Monat (oder ~$16.25/Monat jährlich); Entourage (ohne ATC) $49.95 einmalig; 24h kostenlose Testphase

## Funktionsumfang

- **AI ATC:** 24/7 weltweite Abdeckung an ~88.000 Flughäfen, vollständige IFR/VFR-Unterstützung
- **Natürliche Sprachkommunikation:** Pilot spricht frei per Mikrofon, KI antwortet dynamisch (keine Menü-Auswahl)
- **650+ KI-Stimmen:** Regional unterschiedliche Akzente in 15 Sprachen
- **ACARS/CPDLC:** Text-basierte Kommunikation zwischen Pilot und ATC
- **AI Co-Pilot:** Übernimmt Funkkommunikation und Checklisten
- **Traffic Injection:** Kommerzieller und GA-Verkehr aus realen Flugplänen
- **Taxi-Arrows:** Visuelle Rollhilfe im Simulator

Die Kommunikation mit X-Plane erfolgt über DataRefs und UDP (Port 49000).

## KVM-Setup

Da der SayIntentions Client nicht unter Linux läuft und Wine/Proton nicht praktikabel ist (Mikrofon-Zugriff, Windows-spezifische APIs), muss der Client in einer Windows-VM betrieben werden.

Ein Community-Projekt für macOS ([SayIntentionsForMac](https://github.com/paulfisher53/SayIntentionsForMac)) demonstriert den Ansatz mit einer Windows-VM und UDP-Port-Forwarding. Dieses Prinzip lässt sich auf KVM/QEMU übertragen.

**Voraussetzungen**

- Windows 10+ Guest in KVM/QEMU (siehe [Docker & Virtualisierung](../docker.md) für KVM-Grundlagen)
- Bridged oder NAT-Netzwerk mit Host-Zugriff
- Mikrofon-Passthrough an die VM (für Spracherkennung)
- X-Plane auf dem Linux-Host

**Verbindung**

Der SayIntentions Client kommuniziert mit X-Plane über UDP Port 49000. Bei Bridged Networking befindet sich die Windows-VM im selben Netzwerksegment wie der Host. Die UDP-Kommunikation muss zwischen VM und nativem X-Plane weitergeleitet werden — das [SayIntentionsForMac](https://github.com/paulfisher53/SayIntentionsForMac)-Projekt stellt dafür `sudppipe.exe` und eine Dummy-`X-Plane.exe` bereit, um den Client auf die Host-IP umzuleiten. Dieses Setup wurde erfolgreich mit einer KVM-VM und nativem X-Plane auf dem Linux-Host getestet.

## Quellen

- [SayIntentions.AI — Offizielle Website](https://www.sayintentions.ai/)
- [SayIntentions.AI — Pricing](https://www.sayintentions.ai/pricing)
- [SayIntentions.AI — Features Overview](https://sayintentionsai.freshdesk.com/support/solutions/articles/154000219433)
- [SayIntentionsForMac — GitHub (Community-Workaround)](https://github.com/paulfisher53/SayIntentionsForMac)
