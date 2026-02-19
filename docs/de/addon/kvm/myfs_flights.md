---
description: "My FS Flights: Cloud-basiertes Flug-Tracking und KI-Landeanalyse für X-Plane unter Linux, betrieben in einer Windows-KVM/QEMU-VM."
---
# My FS Flights

My FS Flights ist eine cloudbasierte Plattform für Flight Tracking und Fluganalyse, die Flüge automatisch aufzeichnet, detaillierte Reports erstellt und KI-gestütztes Feedback zur Landung liefert. Die Companion App ist **ausschließlich für Windows** verfügbar — unter Linux ist eine Windows-VM (KVM/QEMU) erforderlich, um sie parallel zu [X-Plane](../../glossary.md#x-plane) auf dem Host zu betreiben.

## Hintergrund

- **Entwickler:** Agile Software Management Limited (York, UK)
- **Website:** [myfs.flights](https://myfs.flights/)
- **Plattformen:** Nur Windows 10+ (Microsoft Store oder Direktdownload)
- **Kompatibilität:** X-Plane 11/12, MSFS 2020/2024, Prepar3D v4–v6

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

- Windows 10+ Guest in KVM/QEMU (siehe [Docker & Virtualisierung](../../linux/extensions/docker.md) für KVM-Grundlagen)
- Bridged oder NAT-Netzwerk mit Host-Zugriff
- X-Plane auf dem Linux-Host

**Verbindung**

Im My FS Flights Plugin lässt sich die Ziel-IP-Adresse direkt in den Einstellungen konfigurieren. Damit kann eine Verbindung zu einer X-Plane-Instanz auf einem anderen Rechner hergestellt werden — oder vom KVM-Guest zu X-Plane auf dem Linux-Host.

!!! tip "Mit KVM und X-Plane unter Linux getestet"

    Die Verbindung zwischen My FS Flights in einer KVM-Windows-VM und X-Plane auf dem Linux-Host ist getestet und funktioniert zuverlässig.

## Quellen

- [My FS Flights — Offizielle Website](https://myfs.flights/)
- [My FS Flights — Microsoft Store](https://apps.microsoft.com/detail/9pgb7ngn6l24)
- [What is My FS Flights? — Blog](https://blog.myfs.flights/posts/about-my-fs-flights/)
