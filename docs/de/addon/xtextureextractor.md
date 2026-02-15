# XTextureExtractor

XTextureExtractor extrahiert Cockpit-Instrumenten-Texturen aus [X-Plane](../glossary.md#x-plane) und streamt sie über das Netzwerk an externe Displays — Tablets, Monitore oder Raspberry Pis.

## Hintergrund

- **Entwickler:** Wayne Piekarski
- **Repository:** [github.com/waynepiekarski/XTextureExtractor](https://github.com/waynepiekarski/XTextureExtractor) (Open Source, GPL-3.0)
- **Plattformen:** Windows, macOS, Linux (native Binaries)
- **Kompatibilität:** X-Plane 11 und X-Plane 12 ([Vulkan](../glossary.md#vulkan-api) und OpenGL)
- **Preis:** Kostenlos

Das [Plugin](../glossary.md#plugin) wird gepflegt und unterstützt über 35 vorkonfigurierte Flugzeuge, darunter Zibo 737, ToLiss A320/A321, Flight Factor 757/767/777 und viele Laminar-Standardflugzeuge.

## Funktionsumfang

- **Textur-Extraktion:** Erkennt automatisch die Panel-Textur des aktuellen Flugzeugs und extrahiert einzelne Instrumente (HSI, ND, EICAS, CDU etc.)
- **Lokale Fenster:** Instrumente in separaten X-Plane-Fenstern anzeigen, auf externe Monitore verschieben, Positionen speichern
- **Netzwerk-Streaming:** Streamt PNG-kodierte Instrumenten-Frames über TCP an verbundene Clients
- **Aircraft-Definitionen:** Einfache `.tex`-Textdateien definieren Instrumentbereiche — eigene Flugzeuge können leicht ergänzt werden
- **Android-App:** [Google Play](https://play.google.com/store/apps/details?id=net.waynepiekarski.xtextureextractor) — zeigt 2 Panels gleichzeitig, automatische X-Plane-Erkennung
- **Java-Desktop-Client:** Plattformübergreifend (Windows, Linux, macOS, Raspberry Pi), im Download enthalten

### Einschränkungen

- Das Cockpit muss gerendert werden (Innenansicht erforderlich)
- Das Standard-Laminar-G1000 (C172 etc.) verwendet einen nicht-standardisierten Texturmechanismus und kann nicht erfasst werden

## Mehrwert in der Flugsimulation

XTextureExtractor ermöglicht Multi-Monitor-Setups ohne spezielle Hardware. Cockpit-Instrumente lassen sich auf ein Tablet neben dem Hauptbildschirm auslagern — besonders nützlich für Navigation Displays, EICAS oder CDUs, die im Vollbild-Cockpit schwer ablesbar sind. Über das Netzwerk-Streaming können auch entfernte Geräte als Instrumenten-Displays dienen.

## Installation

**Download:** [GitHub](https://github.com/waynepiekarski/XTextureExtractor) — die ZIP-Datei aus dem `Uploads/`-Verzeichnis herunterladen.

Den `Plugin-XTextureExtractor-x64-Release`-Ordner nach `Resources/plugins/` entpacken. Die Linux-Binary liegt unter `64/lin.xpl`.

Es werden keine zusätzlichen Systempakete benötigt. Es sind keine Linux-spezifischen Probleme bekannt.

### Netzwerk-Streaming

Der Plugin-Server lauscht auf TCP-Port **52500**. Für den Empfang auf externen Geräten muss dieser Port in der Firewall freigegeben werden. Die automatische Erkennung durch die Android-App nutzt den X-Plane-Beacon auf UDP-Multicast **239.255.1.1:49707**.

## Quellen

- [XTextureExtractor — GitHub](https://github.com/waynepiekarski/XTextureExtractor)
- [XTextureExtractor — Google Play](https://play.google.com/store/apps/details?id=net.waynepiekarski.xtextureextractor)
