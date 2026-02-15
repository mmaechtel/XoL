# ToLiss SimBrief Connector

Der ToLiss SimBrief Connector ist ein eigenständiges [Plugin](../glossary.md#plugin) von hotbso, das als Brücke zwischen SimBrief und der gesamten ToLiss-Flotte dient. Es ermöglicht den direkten Abruf des Operational Flight Plan (OFP) und die Übertragung von Flugdaten ins Cockpit — ohne manuelles Abtippen.

## Hintergrund

- **Entwickler:** hotbso (Holger Teutsch)
- **Repository:** [github.com/hotbso/toliss_simbrief](https://github.com/hotbso/toliss_simbrief) (Open Source, MIT-Lizenz)
- **Plattformen:** Windows, macOS, Linux (native Binaries)
- **Kompatibilität:** [X-Plane](../glossary.md#x-plane) 12, ToLiss-Flotte (A319, A320 CEO/NEO, A321 CEO/NEO, A330neo, A340-600)
- **Preis:** Kostenlos
- **Typ:** Eigenständiges X-Plane-Plugin (kein FlyWithLua-Skript)

hotbso ist auch der Entwickler von [openSAM](opensam.md) und [AutoDGS](autodgs.md).

!!! warning "Repository archiviert"

    Das GitHub-Repository wurde im August 2025 archiviert. Das Plugin funktioniert weiterhin mit aktuellen X-Plane-12- und ToLiss-Versionen, wird aber nicht mehr aktualisiert.

## Funktionsumfang

- **OFP-Abruf:** Operational Flight Plan direkt von simbrief.com abrufen
- **Datenanzeige:** Wesentliche Flugdaten (Route, Fuel, Payload, Wind, Alternates) im Plugin-Fenster anzeigen
- **Load & Fuel Transfer:** Treibstoff und Payload aus dem OFP direkt ins Flugzeug übertragen
- **FMS-Datei:** Flugplan als FMS-Datei laden
- **AviTab-PDF:** OFP als PDF nach [AviTab](avitab.md) herunterladen
- **Command-Bindings:** Exportierte Befehle (`tlsb/toggle`, `tlsb/fetch`, `tlsb/fetch_xfer`) lassen sich an Hardware-Buttons binden
- **VR-Unterstützung:** Fenster funktioniert in VR-Umgebungen

## Mehrwert in der Flugsimulation

Ohne den SimBrief Connector muss der OFP manuell abgerufen und die Daten einzeln ins Cockpit übertragen werden. Das Plugin reduziert diesen Prozess auf einen Klick. Zusammen mit AviTab steht der OFP als PDF direkt im Cockpit-Tablet bereit.

## Installation

**Download:** [GitHub Releases](https://github.com/hotbso/toliss_simbrief/releases)

Die ZIP-Datei nach `Resources/plugins/` entpacken. Es entsteht der Ordner `toliss_simbrief/` mit der Linux-Binary unter `lin_x64/toliss_simbrief.xpl`.

Es werden keine zusätzlichen Systempakete benötigt. Es sind keine Linux-spezifischen Probleme bekannt.

!!! info "Nicht zu verwechseln mit simbrief_hub"

    Der ToLiss SimBrief Connector ist ein eigenständiges Plugin, das direkt mit der SimBrief-API kommuniziert. Das separate Plugin [simbrief_hub](https://github.com/hotbso/simbrief_hub) stellt SimBrief-Daten als Datarefs für andere Plugins bereit (z.B. für [AutoDGS](autodgs.md) und [openSAM](opensam.md)).

## Quellen

- [ToLiss SimBrief Connector — GitHub](https://github.com/hotbso/toliss_simbrief)
- [hotbso — GitHub-Profil](https://github.com/hotbso)
