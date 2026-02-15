# My FS Flights

My FS Flights ist eine cloudbasierte Plattform für Flight Tracking und Fluganalyse, die Flüge automatisch aufzeichnet, detaillierte Reports erstellt und KI-gestütztes Feedback zur Landung liefert. Die Companion App ist **ausschließlich für Windows** verfügbar — unter Linux ist eine Windows-VM (KVM/QEMU) erforderlich, um sie parallel zu [X-Plane](../glossary.md#x-plane) auf dem Host zu betreiben.

## Hintergrund

- **Entwickler:** Agile Software Management Limited (York, UK)
- **Website:** [myfs.flights](https://myfs.flights/)
- **Plattformen:** Nur Windows 10+ (Microsoft Store oder Direktdownload)
- **Kompatibilität:** X-Plane 11/12, MSFS 2020/2024, Prepar3D v4–v6
- **Preis:** Free-Tier (10 Flüge/Monat), Pro (2 GBP/Monat), Ultimate (3 GBP/Monat)

## Funktionsumfang

- **Automatische Flugaufzeichnung:** Startet bei Triebwerksstart, endet beim Shutdown — keine Vorbereitung nötig
- **Detaillierte Flugreports:** Rund 10 Seiten pro Flug mit phasenweiser Analyse
- **KI-Landeanalyse:** Anflugbewertung, Gleitpfad-Tracking, Schwellenhöhe, Aufsetzgeschwindigkeit, Rollout-Bewertung
- **Startanalyse:** Bahnausrichtung, Startstrecke, Abhebegeschwindigkeit, Steigprofil
- **3D-Flugprofil:** Interaktive dreidimensionale Visualisierung des Flugwegs
- **Flugbuch:** Automatisch generierte Beschreibungen, persönliche Notizen, Tags, Screenshots
- **Statistik-Dashboard:** Flugzeit, Distanz, Ranglisten
- **Routenvorschläge:** Flugroutenempfehlungen mit SimBrief-Integration
- **Live Flight Sharing:** Echtzeit-Tracking über teilbaren Link

Flugreports und Dashboards sind über jeden Browser zugänglich. Nur die Datenerfassung erfordert die Windows-App.

## KVM-Setup

Da My FS Flights keinen Linux-Build bietet, muss die App in einer Windows-VM laufen. Die automatische Simulatorerkennung setzt voraus, dass die VM Netzwerkzugang zum X-Plane-Host hat.

**Voraussetzungen**

- Windows 10+ Guest in KVM/QEMU (siehe [Docker & Virtualisierung](../docker.md) für KVM-Grundlagen)
- Bridged oder NAT-Netzwerk mit Host-Zugriff
- X-Plane auf dem Linux-Host

**Verbindung**

Der genaue Mechanismus, über den My FS Flights die Verbindung zu X-Plane herstellt, ist nicht öffentlich dokumentiert. X-Plane sendet seine Präsenz per UDP-Multicast (Beacon auf 239.255.1.1:49707). Bei Bridged Networking befindet sich die Windows-VM im selben Netzwerksegment wie der Host, was die Erkennung der X-Plane-Instanz ermöglicht.

!!! warning "Unter Linux nicht getestet"

    Dieses KVM-Setup ist auf Basis der Tool-Architektur dokumentiert. Ob My FS Flights eine X-Plane-Instanz auf dem Linux-Host zuverlässig erkennt und verbindet, wurde nicht unabhängig verifiziert. Rückmeldungen sind willkommen.

## Quellen

- [My FS Flights — Offizielle Website](https://myfs.flights/)
- [My FS Flights — Microsoft Store](https://apps.microsoft.com/detail/9pgb7ngn6l24)
- [What is My FS Flights? — Blog](https://blog.myfs.flights/posts/about-my-fs-flights/)
