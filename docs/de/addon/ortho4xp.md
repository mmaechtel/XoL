# Ortho4XP

Ortho4XP ist ein leistungsstarkes Tool zur Erstellung von Orthofotos für X-Plane. Es ermöglicht die Generierung von hochauflösenden Bodentexturen aus Satellitenbildern und Höhendaten.

## Installation und Versionen

Ortho4XP ist in zwei Hauptversionen verfügbar:

1. **Originalversion** von Oscar Pilote:
    * [GitHub Repository](https://github.com/oscarpilote/Ortho4XP)
    * Die ursprüngliche Version mit grundlegenden Funktionen
    * [Binaries verfügbar](https://github.com/kubilus1/autoortho/releases/tag/0.7.2)

2. **Fork von shred86** (empfohlen):
    * [GitHub Repository](https://github.com/shred86/Ortho4XP)
    * [Detaillierte Dokumentation](https://github.com/shred86/Ortho4XP/wiki)
    * Enthält zahlreiche Verbesserungen und neue Funktionen
    * [Binaries für verschiedene Betriebssysteme](https://github.com/shred86/Ortho4XP/wiki/Installation)

### Installationsmethoden

1. **Mit Binaries (empfohlen)**:
    - Laden Sie die passende Version für Ihr Betriebssystem herunter
    - Entpacken Sie das Archiv
    - Führen Sie die ausführbare Datei aus

2. **Manuelle Installation**:
    - Laden Sie die gewünschte Version herunter
    - Stellen Sie sicher, dass Python 3.x installiert ist
    - Installieren Sie die erforderlichen Python-Pakete:
     ```bash
     pip install -r requirements.txt
     ```

3. **Alternative Installation für Linux**:
    - Installation mit Docker (siehe [Docker Dokumentation](../docker.md))
    - Installation mit pyenv (siehe [pyenv Dokumentation](../pyenv.md))

## Verwendung und Konfiguration

### Grundlegende Verwendung

1. Starten Sie Ortho4XP über die Python-Datei oder die ausführbare Datei:
   ```bash
   python Ortho4XP.py
   ```

2. Wählen Sie im Hauptfenster:
   - Den Zielbereich (Tile)
   - Die gewünschte Zoomstufe (ZL)
   - Die Bildquelle (z.B. Bing, Google, Here)

3. Klicken Sie auf "Build" um den Prozess zu starten

### Wichtige Parameter

| Parameter | Standardwert | Beschreibung |
|-----------|--------------|--------------|
| `custom_build_dir` | `Tiles` | Verzeichnis für die generierten Kacheln |
| `custom_overlay_src` | `Global Scenery` | Quelle für Overlay-Daten |
| `custom_overlay_dir` | `yOrtho4XP_Overlays` | Zielverzeichnis für Overlays |
| `custom_scenery_dir` | `Custom Scenery` | Zielverzeichnis für die fertigen Kacheln |
| `provider` | `BI` | Bildquelle (BI=Bing, GO2=Google, ES=ESRI) |
| `zoomlevel` | `16` | Zoom-Level der Satellitenbilder |
| `curvature_tol` | `3.0` | Toleranz für Geländekrümmung |
| `mesh_zl` | `16` | Zoom-Level für Mesh-Generierung |
| `mask_zl` | `16` | Zoom-Level für Wassermasken |
| `water_smoothing` | `3` | Glättung von Wasserübergängen |
| `road_banking_limit` | `0.3` | Maximale Straßenneigung |
| `apt_smoothing_pix` | `8` | Glättungsparameter für Flughäfen |

### Empfohlene Einstellungen

#### Standard-Einstellungen (gute Balance)

* `zoomlevel`: 16
* `curvature_tol`: 3.0
* `mesh_zl`: 16
* `mask_zl`: 16
* `water_smoothing`: 3

#### Hochauflösende Einstellungen

* `zoomlevel`: 17
* `curvature_tol`: 2.0
* `mesh_zl`: 17
* `mask_zl`: 17
* `water_smoothing`: 5

#### Performance-optimierte Einstellungen

* `zoomlevel`: 15
* `curvature_tol`: 4.0
* `mesh_zl`: 15
* `mask_zl`: 15
* `water_smoothing`: 2

## Wichtige Hinweise und Fehlerbehebung

### Allgemeine Hinweise

- Ortho4XP benötigt viel Speicherplatz für die generierten Texturen
- Die Qualität der Orthofotos hängt von der gewählten Bildquelle ab
- Die Verarbeitung kann je nach Gebietsgröße und Zoomstufe mehrere Stunden dauern
- Der shred86 Fork bietet bessere Performance und mehr Funktionen
- Die Verwendung der Binaries vereinfacht die Installation erheblich

### Performance-Optimierung

- `max_convert_slots` und `max_download_slots` sollten an die CPU-Leistung angepasst werden
- Zu hohe Werte können das System überlasten
- Skip-Parameter sind nützlich für die Wiederverarbeitung einzelner Schritte

### Fehlerbehebung

Bei Problemen:

1. Überprüfen Sie die Log-Dateien im Ortho4XP-Verzeichnis
2. Stellen Sie sicher, dass alle Python-Abhängigkeiten installiert sind
3. Konsultieren Sie die [Dokumentation des shred86 Forks](https://github.com/shred86/Ortho4XP/wiki)
4. Besuchen Sie das [X-Plane Forum](https://forums.x-plane.org/index.php?/forums/forum/310-ortho4xp/) 