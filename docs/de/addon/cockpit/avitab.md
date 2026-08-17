---
description: "AviTab für X-Plane unter Linux — Open-Source-Cockpit-Tablet mit PDF-Viewer, Moving Map, Navigraph-Charts und eigenen Tile-Servern."
---
# AviTab

AviTab ist ein Open-Source-[Plugin](../../glossary.md#plugin) für [X-Plane](../../glossary.md#x-plane) 12, das ein Tablet im Cockpit darstellt — mit PDF-Viewer, Moving Map und Chart-Integration. Es wurde primär für VR entwickelt, funktioniert aber ebenso im 2D-Modus.

## Hintergrund

- **Entwickler:** Folke Will (fpw), Mitwirkende dave6502, mjh65
- **Repository:** [github.com/TeamAvitab/avitab](https://github.com/TeamAvitab/avitab) (Open Source, AGPL-3.0; gepflegter Fork des archivierten fpw/avitab)
- **Plattformen:** Windows, macOS, Linux (native Binaries)
- **Kompatibilität:** X-Plane 11.20+ und X-Plane 12

Das ursprüngliche Repository [fpw/avitab](https://github.com/fpw/avitab) ist archiviert (schreibgeschützt, Issue-Tracker deaktiviert), nachdem sich Folke Will aus der Pflege zurückgezogen hat. Die Entwicklung wird unter [TeamAvitab/avitab](https://github.com/TeamAvitab/avitab) fortgeführt, wo regelmäßig Releases erscheinen.

## Funktionsumfang

- **PDF-Viewer:** Zeigt PDF-Karten und Checklisten aus dem `charts/`-Unterverzeichnis an
- **Moving Map:** Online-Karten (OpenTopoMap, OpenStreetMap) und Offline-Karten mit konfigurierbaren Tile-Servern
- **Navigraph-Integration:** IFR/VFR-Charts im Cockpit (nur mit Navigraph-Abo, nicht verfügbar bei Selbstkompilierung)
- **ChartFox-Integration:** Kostenlose Charts über Vatsim-Login
- **Airport-App:** Flughafeninformationen, Runway-Daten, lokale Charts
- **Routen-Overlay:** FMS-Dateien als Overlay auf der Moving Map
- **Aircraft-Integration:** Einige Flugzeuge (z.B. Zibo 737) haben ein 3D-Tablet-Modell mit AviTab-Integration; die Panel-Integration unter X-Plane 12 setzt voraus, dass das Flugzeug den aktuellen Integrationsmodus nutzt
- **Standalone-Modus:** Kann auch als eigenständige Anwendung außerhalb von X-Plane laufen

### AviTab Browser (Ergänzungs-Plugin)

Das Plugin [AviTab Browser](https://github.com/rswilem/avitab-browser) von rswilem fügt einen vollwertigen Webbrowser zum AviTab hinzu. Es nutzt das in X-Plane 12 eingebettete Chromium Embedded Framework.

- **Lizenz:** GPL-3.0
- **Features:** Konfigurierbare Homepage, Hotkey-Websites, SimBrief-Flugplan-Download
- **Download:** [forums.x-plane.org](https://forums.x-plane.org/files/file/93812-avitab-browser-a-web-browser-addon-for-the-avitab-plugin/)

!!! tip "Little Navmap als Moving Map im AviTab Browser"
    [Little Navmap](../tools/littlexpconnect.md) bringt einen eigenen Webserver mit (`Tools > Run Web Server`, Standardport 8965). Dessen Kartenseite zeigt die von Little XpConnect gelieferte Flugzeugposition und hält das Flugzeug auf Wunsch zentriert (`Center on aircraft` plus Auto-Refresh) — eine Moving Map mit der kompletten Little-Navmap-Karte inklusive Flugplan, ganz ohne zusätzlichen Tile-Server. Wird der AviTab Browser auf diese Seite gerichtet, erscheint sie auf dem Cockpit-Tablet.

    Konfiguration in `Resources/plugins/avitab-browser/config.ini` (die Datei wird beim ersten Start mit Standardwerten angelegt); ein funktionierendes Linux-Beispiel:

    ```ini
    [browser]
    homepage=http://localhost:8965
    hide_addressbar=yes

    [statusbar]
    icon_1=navigation
    url_1=http://localhost:8965
    ```

    `homepage` öffnet die Karte direkt, das `statusbar`-Lesezeichen holt sie nach dem Surfen auf anderen Seiten mit einem Tipp zurück. Läuft Little Navmap auf einem anderen Rechner, ist `localhost` durch dessen Adresse zu ersetzen — der Webserver ist von jedem Gerät im lokalen Netz erreichbar.

## Mehrwert in der Flugsimulation

AviTab löst das Problem, dass während des Flugs häufig Karten, Checklisten oder Handbücher nachgeschlagen werden müssen — insbesondere in VR, wo das Headset zum Ablesen externer Bildschirme abgenommen werden müsste. Über Custom Maps lassen sich eigene Tile-Server (z.B. ein lokaler TileServer-GL) einbinden. Die Aircraft-Integration ermöglicht bei unterstützten Flugzeugen ein direkt im 3D-Cockpit verbautes Tablet.

## Installation

**Download:** [github.com/TeamAvitab/avitab/releases](https://github.com/TeamAvitab/avitab/releases/latest) oder [forums.x-plane.org](https://forums.x-plane.org/files/file/44825-avitab-vr-compatible-tablet-with-pdf-viewer-moving-maps-and-more/)

Die ZIP-Datei entpacken und den enthaltenen Ordner `Avitab/` nach `Resources/plugins/` kopieren. Die Linux-Binary liegt unter `Avitab/lin_x64/Avitab.xpl`.

Alle Abhängigkeiten sind statisch gelinkt — es werden keine zusätzlichen Systempakete benötigt.

**PDF-Charts ablegen:**

```bash
cp my_charts/*.pdf /path/to/X-Plane\ 12/Resources/plugins/Avitab/charts/
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

## Quellen

- [AviTab — GitHub (TeamAvitab-Fork)](https://github.com/TeamAvitab/avitab)
- [AviTab — Release Notes](https://github.com/TeamAvitab/avitab/releases)
- [AviTab Browser — GitHub](https://github.com/rswilem/avitab-browser)
- [AviTab — forums.x-plane.org](https://forums.x-plane.org/files/file/44825-avitab-vr-compatible-tablet-with-pdf-viewer-moving-maps-and-more/)
