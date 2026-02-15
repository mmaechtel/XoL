# AviTab

AviTab ist ein Open-Source-[Plugin](../glossary.md#plugin) für [X-Plane](../glossary.md#x-plane) 12, das ein Tablet im Cockpit darstellt — mit PDF-Viewer, Moving Map und Chart-Integration. Es wurde primär für VR entwickelt, funktioniert aber ebenso im 2D-Modus.

## Hintergrund

- **Entwickler:** Folke Will (fpw), Mitwirkende dave6502, mjh65
- **Repository:** [github.com/fpw/avitab](https://github.com/fpw/avitab) (Open Source, AGPL-3.0)
- **Plattformen:** Windows, macOS, Linux (native Binaries)
- **Kompatibilität:** X-Plane 11.20+ und X-Plane 12
- **Preis:** Kostenlos

Die Entwicklungsaktivität ist gering — der letzte Commit und das letzte Release (v0.7.1) stammen vom September 2024. Das Repository ist nicht archiviert, aber es gibt keine Anzeichen für baldige Updates.

## Funktionsumfang

- **PDF-Viewer:** Zeigt PDF-Karten und Checklisten aus dem `charts/`-Unterverzeichnis an
- **Moving Map:** Online-Karten (OpenTopoMap, OpenStreetMap) und Offline-Karten mit konfigurierbaren Tile-Servern
- **Navigraph-Integration:** IFR/VFR-Charts im Cockpit (nur mit Navigraph-Abo, nicht verfügbar bei Selbstkompilierung)
- **ChartFox-Integration:** Kostenlose Charts über Vatsim-Login
- **Airport-App:** Flughafeninformationen, Runway-Daten, lokale Charts
- **Routen-Overlay:** FMS-Dateien als Overlay auf der Moving Map
- **Aircraft-Integration:** Einige Flugzeuge (z.B. Zibo 737) haben ein 3D-Tablet-Modell mit AviTab-Integration
- **Standalone-Modus:** Kann auch als eigenständige Anwendung außerhalb von X-Plane laufen

### AviTab Browser (Ergänzungs-Plugin)

Das Plugin [AviTab Browser](https://github.com/rswilem/avitab-browser) von rswilem fügt einen vollwertigen Webbrowser zum AviTab hinzu. Es nutzt das in X-Plane 12 eingebettete Chromium Embedded Framework.

- **Lizenz:** GPL-3.0
- **Features:** Konfigurierbare Homepage, Hotkey-Websites, SimBrief-Flugplan-Download
- **Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/93812-avitab-browser-a-web-browser-addon-for-the-avitab-plugin/)

## Mehrwert in der Flugsimulation

AviTab löst das Problem, dass während des Flugs häufig Karten, Checklisten oder Handbücher nachgeschlagen werden müssen — insbesondere in VR, wo das Headset zum Ablesen externer Bildschirme abgenommen werden müsste. Über Custom Maps lassen sich eigene Tile-Server (z.B. ein lokaler TileServer-GL) einbinden. Die Aircraft-Integration ermöglicht bei unterstützten Flugzeugen ein direkt im 3D-Cockpit verbautes Tablet.

## Installation

**Download:** [github.com/fpw/avitab/releases](https://github.com/fpw/avitab/releases/tag/v0.7.1) oder [forums.x-plane.org](https://forums.x-plane.org/files/file/44825-avitab-vr-compatible-tablet-with-pdf-viewer-moving-maps-and-more/)

Die ZIP-Datei nach `Resources/plugins/` entpacken. Es entsteht der Ordner `AviTab/` mit der Linux-Binary unter `lin_x64/AviTab.xpl`.

Alle Abhängigkeiten sind statisch gelinkt — es werden keine zusätzlichen Systempakete benötigt.

**PDF-Charts ablegen:**

```bash
cp meine_charts/*.pdf /pfad/zu/X-Plane\ 12/Resources/plugins/AviTab/charts/
```

Unterordner werden unterstützt und als Verzeichnisstruktur im Plugin angezeigt.

### Custom Maps konfigurieren

Eigene Kartenquellen werden über die Datei `online-maps/mapconfig.json` im Plugin-Verzeichnis definiert:

```json
[
    {
        "name": "OpenTopoMap",
        "servers": ["a.tile.opentopomap.org", "b.tile.opentopomap.org"],
        "protocol": "https",
        "url": "{z}/{x}/{y}.png",
        "min_zoom_level": 1,
        "max_zoom_level": 17,
        "tile_width_px": 256,
        "tile_height_px": 256,
        "enabled": true
    }
]
```

### PDF-Crash auf Linux

!!! warning "PDF-Viewer auf bestimmten Distributionen nicht nutzbar"

    AviTab stürzt beim Öffnen von PDF-Dateien auf Linux-Systemen mit neuerer `lcms2`-Bibliothek ab (SIGSEGV in `cmsSignalError`). Die statisch gelinkte MuPDF-Bibliothek kollidiert mit der systemweiten `lcms2`-Version.

    **Betroffene Distributionen (bestätigt):**

    - Arch Linux / EndeavourOS
    - Ubuntu 24.04 / Kubuntu 24.10

    **Debian Bookworm** (lcms2 2.14) ist nicht betroffen. Distributionen mit lcms2 ≥ 2.16 könnten ebenfalls betroffen sein.

    **Workaround:** Ein Community-Mitglied hat den Crash durch Neukompilierung von AviTab mit einer neueren MuPDF-Version (1.26.11) behoben. Dies erfordert allerdings Selbstkompilierung — ein offizielles Update steht aus. Moving Map und andere Apps funktionieren unabhängig davon normal.

## Quellen

- [AviTab — GitHub](https://github.com/fpw/avitab)
- [AviTab v0.7.1 — Release Notes](https://github.com/fpw/avitab/releases/tag/v0.7.1)
- [AviTab Browser — GitHub](https://github.com/rswilem/avitab-browser)
- [Issue #232 — PDF-Crash auf Linux](https://github.com/fpw/avitab/issues/232)
- [AviTab — forums.x-plane.org](https://forums.x-plane.org/files/file/44825-avitab-vr-compatible-tablet-with-pdf-viewer-moving-maps-and-more/)
