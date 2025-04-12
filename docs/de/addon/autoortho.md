# AutoOrtho

AutoOrtho ist ein Tool für X-Plane, das Orthofotos in den Flugsimulator integriert. Es ermöglicht die Nutzung von hochauflösenden Luftbildern als Bodentexturen und verbessert damit die visuelle Realität in X-Plane deutlich.

## Vergleich mit Ortho4XP

AutoOrtho und Ortho4XP sind beide Tools zur Integration von Orthofotos in X-Plane, unterscheiden sich jedoch grundlegend:

### AutoOrtho

* **Streaming-basiert**: Lädt Orthofotos während des Flugs nach Bedarf
* **Keine lokale Speicherung**: Benötigt keine großen lokalen Speicherkapazitäten
* **Dynamische Anpassung**: Passt die Qualität automatisch an die Flughöhe an
* **Einfache Installation**: Schneller Einstieg ohne komplexe Konfiguration
* **Regelmäßige Updates**: Automatische Aktualisierung der Bilddaten
* **Internetabhängig**: Benötigt eine stabile Internetverbindung
* **Flexibel**: Einfaches Wechseln zwischen verschiedenen Regionen

### Ortho4XP

* **Lokale Speicherung**: Erstellt und speichert Orthofotos lokal
* **Hohe Qualität**: Maximale Kontrolle über die Qualität der Texturen
* **Offline-Nutzung**: Keine Internetverbindung während des Flugs nötig
* **Komplexe Konfiguration**: Mehr Einstellungsmöglichkeiten für fortgeschrittene Nutzer
* **Hoher Speicherbedarf**: Benötigt viel Festplattenspeicher
* **Lange Generierungszeit**: Erstellung der Texturen kann Stunden dauern
* **Statisch**: Einmal erstellte Texturen bleiben unverändert

### Wann welches Tool verwenden?

**AutoOrtho ist ideal für:**

* Nutzer mit begrenztem Speicherplatz
* Gelegentliche Flüge in verschiedenen Regionen
* Nutzer, die keine komplexe Konfiguration wünschen
* Nutzer mit guter Internetverbindung

**Ortho4XP ist ideal für:**

* Nutzer mit ausreichend Speicherplatz
* Regelmäßige Flüge in bestimmten Regionen
* Nutzer, die maximale Kontrolle über die Qualität wünschen
* Nutzer ohne stabile Internetverbindung

## Installation und Verwendung

### Installation

1. Laden Sie die neueste Version von AutoOrtho von der [offiziellen GitHub-Seite](https://github.com/kubilus1/autoortho) herunter
2. Entpacken Sie das Archiv in einen Ordner Ihrer Wahl
3. Stellen Sie sicher, dass Python 3.x installiert ist
4. Installieren Sie die erforderlichen Python-Pakete:
   ```bash
   pip install -r requirements.txt
   ```

### Konfiguration

Die Konfigurationsdatei `.autoortho` wird im Home-Verzeichnis erstellt und kann mit einem Texteditor bearbeitet werden. Hier sind die wichtigsten Parameter, die an Ihr System angepasst werden können:

```ini
# X-Plane Verzeichnis
xplane_path = /pfad/zum/xplane

# Cache-Verzeichnis für Orthofotos
cache_dir = /pfad/zum/cache

# Bildanbieter (bing, google, here)
provider = bing

# Cache-Größe in GB
cache_size = 20

# Maximale Wartezeit für Bilder. Höhere Werte bedeuten bessere Qualität, aber mehr
# Ruckeln. Niedrigere Werte sind reaktiver auf Kosten gelegentlicher
# niedrigerer Qualität.
maxwait = 1.5

# Minimaler Zoom-Level. Dies erhöht nicht die maximale Qualität der Satellitenbilder
min_zoom = 14

# Automatischer Start mit X-Plane
autostart = true

# Debug-Modus (true/false)
debug = false
```

### Wichtige Parameter-Erklärungen

- `xplane_path`: Pfad zum X-Plane Hauptverzeichnis
- `cache_dir`: Verzeichnis für Orthofoto-Cache (empfohlen: schnelle SSD)
- `provider`: Bildquelle für Orthofotos (bing, google, here)
- `cache_size`: Maximale Cache-Größe in GB
- `maxwait`: Maximale Wartezeit für Bilder in Sekunden. Höhere Werte bedeuten bessere Qualität aber mehr Ruckeln. Niedrigere Werte sind reaktiver, können aber gelegentlich zu niedrigerer Qualität führen.
- `min_zoom`: Minimaler Zoom-Level für Satellitenbilder. Beeinflusst die minimale Qualität der angezeigten Bilder.
- `autostart`: AutoOrtho automatisch mit X-Plane starten
- `debug`: Debug-Informationen in den Logs aktivieren

### Grundlegende Verwendung

1. Starten Sie AutoOrtho über die Python-Datei:
   ```bash
   python autoortho.py
   ```

2. Wählen Sie im Hauptfenster:
   - Install Dirs
   - Die Bildquelle (z.B. Bing, Google, Here)
   - Den Download Zielbereich

3. Klicken Sie auf "Start" um den Prozess zu starten

## Integration mit Ortho4XP 1.4

AutoOrtho kann durch selbst erstellte Ortho4XP 1.4 Kacheln verbessert werden. Diese Methode bietet eine größere Kontrolle über die Qualität und das Aussehen der Orthofotos.

### Ortho4XP 1.4 Konfiguration

Für optimale Ergebnisse mit AutoOrtho verwenden Sie folgende Einstellungen in Ortho4XP 1.4:

| Parameter                  | Empfohlener Wert | Beschreibung |
|---------------------------|------------------|--------------|
| `skip_downloads`          | Aktiviert        | Kein Bilddownload nötig |
| `skip_converts`           | Aktiviert        | Kein DDS-Rendering nötig |
| `mask_zl`                 | 16               | Optimale Wasserübergänge |
| `use_masks_for_inland`    | Aktiviert        | Bessere Binnengewässer |
| `distance_masks_too`      | Aktiviert        | Saubere Küstenlinien |
| `custom_dem`              | Optional         | Höhere DEMs für feinere Meshes |
| `curvature_tol`           | 2.0–4.0          | Beeinflusst die Mesh-Komplexität |
| `road_banking_limit`      | 0.3              | Verhindert Build-Fehler |
| `apt_smoothing_pix`       | 8–16             | Glattere Landebahnen |
| `water_tech`              | "XP12"           | Verwendet XP12 Wassertechnologie |

### Kachel-Konsolidierung

Um die erstellten Kacheln mit AutoOrtho nutzbar zu machen, müssen sie in einem spezifischen Format konsolidiert werden. Hierfür kann ein Konsolidierungsskript verwendet werden:

```bash
#!/bin/bash

# Quell- und Zielpfade definieren
SRC="$HOME/xplane-ortho-work/tiles_source"
DST="$HOME/xplane-ortho-work/tiles_consolidated/zOrtho4XP_RegionName"

# Zielverzeichnis vorbereiten
rm -rf "$DST"
mkdir -p "$DST"

# Temporäre Dateien entfernen
find "$SRC" -type f -name "*.bak" -delete

# Relevante Daten kopieren
for TILE in "$SRC"/*; do
    if [ -d "$TILE" ]; then
        [ -d "$TILE/textures" ] && cp -r "$TILE/textures" "$DST/"
        [ -d "$TILE/terrain" ] && cp -r "$TILE/terrain" "$DST/"
        [ -d "$TILE/Earth nav data" ] && cp -r "$TILE/Earth nav data" "$DST/"
    fi
done
```

### Integration mit AutoOrtho

Nach der Erstellung der Kacheln:

1. Kopieren Sie den konsolidierten Ordner nach:
   ```
   ~/X-Plane 12/Custom Scenery/z_autoortho/scenery/
   ```

2. Starten Sie AutoOrtho neu

### Overlay-Integration

Für zusätzliche Details können Overlays generiert werden:

1. Erstellen Sie Overlays in Ortho4XP
2. Speichern Sie sie in einem Ordner namens `yOrtho4XP_RegionName`
3. Kopieren Sie den Ordner nach:
   ```
   ~/X-Plane 12/Custom Scenery/yOrtho4XP_RegionName/
   ```

### scenery_packs.ini Konfiguration

Die richtige Reihenfolge in der `scenery_packs.ini` ist wichtig:

```ini
SCENERY_PACK Custom Scenery/yOrtho4XP_RegionName/
SCENERY_PACK Custom Scenery/z_autoortho/scenery/zOrtho4XP_RegionName/
SCENERY_PACK Custom Scenery/z_autoortho/scenery/z_autoortho_xyz/
```

### Vorteile dieser Methode

- Größere Kontrolle über die Orthofoto-Qualität
- Optimierte Performance durch angepasste Mesh-Details
- Bessere Darstellung von Gewässern und Küstenlinien
- Möglichkeit zur Integration von Overlays für zusätzliche Details
- Vollständige Kontrolle über Zoom-Level und Dateigröße

## Wichtige Hinweise und Fehlerbehebung

AutoOrtho läuft als Hintergrunddienst und generiert Orthofotos während des Flugs. Die Texturen werden in einem Cache gespeichert, um wiederholte Downloads zu vermeiden. Eine stabile Internetverbindung ist für das Streaming der Orthofotos erforderlich. Die Qualität der Orthofotos wird automatisch an die Flughöhe angepasst.

Bei Problemen:
1. Überprüfen Sie die Log-Dateien im AutoOrtho-Verzeichnis
2. Stellen Sie sicher, dass alle Python-Abhängigkeiten installiert sind
3. Überprüfen Sie die Internetverbindung für den Download der Bilddaten
4. Konsultieren Sie das [AutoOrtho-Forum](https://forums.x-plane.org/index.php?/forums/forum/406-autoortho/) für weitere Hilfe

### Hinweis zur Verwendung mit SimHeaven

Bei Verwendung von [SimHeaven](https://simheaven.com/) sind die `yOrtho4XP`-Verzeichnisse nicht erforderlich, da SimHeaven bereits alle notwendigen Overlay-Daten enthält. In diesem Fall müssen weder die von Ortho4XP erstellten noch die von AutoOrtho generierten `yOrtho4XP`-Verzeichnisse in der `scenery_packs.ini` aufgeführt werden.


