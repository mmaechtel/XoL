# Ortho4XP

Ortho4XP ist ein leistungsstarkes Tool zur Erstellung von Orthofotos für X-Plane. Es ermöglicht die Generierung von hochauflösenden Bodentexturen aus Satellitenbildern und Höhendaten.

## Quellen

Ortho4XP ist in zwei Hauptversionen verfügbar:

1. **Originalversion** von Oscar Pilote:
    * [GitHub Repository](https://github.com/oscarpilote/Ortho4XP)
    * Die ursprüngliche Version mit grundlegenden Funktionen
    * [Binaries verfügbar](https://github.com/kubilus1/autoortho/releases/tag/0.7.2)

2. **Fork von shred86**:
    * [GitHub Repository](https://github.com/shred86/Ortho4XP)
    * [Detaillierte Dokumentation](https://github.com/shred86/Ortho4XP/wiki)
    * Enthält zahlreiche Verbesserungen und neue Funktionen
    * [Binaries für verschiedene Betriebssysteme](https://github.com/shred86/Ortho4XP/wiki/Installation)

## Installation

Ortho4XP kann auf zwei Arten installiert werden:

### Installation mit Binaries (empfohlen)

1. Laden Sie die passende Version für Ihr Betriebssystem herunter:
    * Originalversion: [Releases](https://github.com/kubilus1/autoortho/releases/tag/0.7.2)
    * shred86 Fork: [Installationsseite](https://github.com/shred86/Ortho4XP/wiki/Installation)
2. Entpacken Sie das Archiv
3. Führen Sie die ausführbare Datei aus

### Manuelle Installation

1. Laden Sie die gewünschte Version von Ortho4XP herunter
2. Stellen Sie sicher, dass Python 3.x installiert ist
3. Installieren Sie die erforderlichen Python-Pakete:
    ```bash
    pip install -r requirements.txt
    ```

### Alternative Installation für Linux

Für Linux-Benutzer stehen zwei alternative Installationsmethoden zur Verfügung:
* Installation mit Docker (siehe [Docker Dokumentation](../docker.md))
* Installation mit pyenv (siehe [pyenv Dokumentation](../pyenv.md))

## Grundlegende Verwendung

1. Starten Sie Ortho4XP über die Python-Datei oder die ausführbare Datei:
    ```bash
    python Ortho4XP.py
    ```

2. Wählen Sie im Hauptfenster:
    * Den Zielbereich (Tile)
    * Die gewünschte Zoomstufe (ZL)
    * Die Bildquelle (z.B. Bing, Google, Here)

3. Klicken Sie auf "Build" um den Prozess zu starten

## Besonderheiten des shred86 Forks

Der Fork von shred86 bietet zahlreiche Verbesserungen gegenüber der Originalversion:

### Neue Funktionen

* Verbesserte Benutzeroberfläche mit Dark Mode
* Erweiterte Konfigurationsmöglichkeiten
* Unterstützung für mehr Bildquellen
* Verbesserte Fehlerbehandlung und Logging
* Automatische Updates

### Technische Verbesserungen

* Optimierte Speichernutzung
* Schnellere Verarbeitung
* Bessere Fehlertoleranz
* Erweiterte Kompatibilität mit verschiedenen Systemen

### Zusätzliche Features

* Batch-Verarbeitung mehrerer Tiles
* Erweiterte Mesh-Optionen
* Verbesserte Wassermasken
* Unterstützung für mehr Höhendatenquellen
* Erweiterte Konfigurationsdateien

## Wichtige Hinweise

* Ortho4XP benötigt viel Speicherplatz für die generierten Texturen
* Die Qualität der Orthofotos hängt von der gewählten Bildquelle ab
* Die Verarbeitung kann je nach Gebietsgröße und Zoomstufe mehrere Stunden dauern
* Der shred86 Fork bietet bessere Performance und mehr Funktionen
* Die Verwendung der Binaries vereinfacht die Installation erheblich
* Für Linux-Benutzer bieten Docker und pyenv flexible Alternativen zur direkten Installation

## Fehlerbehebung

Bei Problemen:
1. Überprüfen Sie die Log-Dateien im Ortho4XP-Verzeichnis
2. Stellen Sie sicher, dass alle Python-Abhängigkeiten installiert sind
3. Konsultieren Sie die [Dokumentation des shred86 Forks](https://github.com/shred86/Ortho4XP/wiki) für detaillierte Anleitungen
4. Besuchen Sie das [X-Plane Forum](https://forums.x-plane.org/index.php?/forums/forum/310-ortho4xp/) für weitere Hilfe

## Detaillierte Parameter-Erklärung

Ortho4XP bietet eine Vielzahl von Parametern, die die Qualität und das Erscheinungsbild der generierten Orthofotos beeinflussen. Hier ist eine detaillierte Übersicht der wichtigsten Parameter:

### Allgemeine Parameter

| Parameter | Standardwert | Beschreibung |
|-----------|--------------|--------------|
| `custom_build_dir` | `Tiles` | Verzeichnis für die generierten Kacheln |
| `custom_overlay_src` | `Global Scenery` | Quelle für Overlay-Daten |
| `custom_overlay_dir` | `yOrtho4XP_Overlays` | Zielverzeichnis für Overlays |
| `custom_scenery_dir` | `Custom Scenery` | Zielverzeichnis für die fertigen Kacheln |

### Bildquellen und Qualität

| Parameter | Standardwert | Beschreibung |
|-----------|--------------|--------------|
| `provider` | `BI` | Bildquelle (BI=Bing, GO2=Google, ES=ESRI, etc.) |
| `zoomlevel` | `16` | Zoom-Level der Satellitenbilder (höher = detaillierter) |
| `max_convert_slots` | `4` | Maximale Anzahl paralleler Konvertierungen |
| `max_download_slots` | `4` | Maximale Anzahl paralleler Downloads |
| `use_decal_on_terrain` | `True` | Verwendung von Decals auf dem Terrain |
| `terrain_casts_shadows` | `True` | Terrain wirft Schatten |

### Mesh-Generierung

| Parameter | Standardwert | Beschreibung |
|-----------|--------------|--------------|
| `curvature_tol` | `3.0` | Toleranz für Geländekrümmung (niedriger = detaillierter) |
| `min_area` | `0.1` | Minimale Fläche für Mesh-Triangulation |
| `max_area` | `0.5` | Maximale Fläche für Mesh-Triangulation |
| `mesh_zl` | `16` | Zoom-Level für Mesh-Generierung |
| `road_banking_limit` | `0.3` | Maximale Straßenneigung |
| `apt_smoothing_pix` | `8` | Glättungsparameter für Flughäfen |

### Wasser und Küsten

| Parameter | Standardwert | Beschreibung |
|-----------|--------------|--------------|
| `water_simplification` | `0.0` | Vereinfachung von Wasserflächen |
| `use_masks_for_inland` | `True` | Verwendung von Masken für Binnengewässer |
| `distance_masks_too` | `True` | Berücksichtigung von Küstenabständen |
| `mask_zl` | `16` | Zoom-Level für Wassermasken |
| `water_smoothing` | `3` | Glättung von Wasserübergängen |

### Höhendaten

| Parameter | Standardwert | Beschreibung |
|-----------|--------------|--------------|
| `custom_dem` | `None` | Benutzerdefinierte Höhendatenquelle |
| `dem_source` | `ViewFinderPanorama` | Standard-Höhendatenquelle |
| `dem_resolution` | `1` | Auflösung der Höhendaten in Bogensekunden |
| `use_experimental_water` | `False` | Experimentelle Wasserdarstellung |

### Performance-Optimierung

| Parameter | Standardwert | Beschreibung |
|-----------|--------------|--------------|
| `skip_downloads` | `False` | Überspringen des Downloads (nur bei vorhandenen Bildern) |
| `skip_converts` | `False` | Überspringen der Konvertierung |
| `skip_masks` | `False` | Überspringen der Maskenerstellung |
| `skip_mesh` | `False` | Überspringen der Mesh-Generierung |
| `skip_overlays` | `False` | Überspringen der Overlay-Erstellung |

### Erweiterte Optionen

| Parameter | Standardwert | Beschreibung |
|-----------|--------------|--------------|
| `clean_bad_geometries` | `True` | Bereinigung fehlerhafter Geometrien |
| `clean_bad_intersections` | `True` | Bereinigung fehlerhafter Schnittpunkte |
| `clean_bad_islands` | `True` | Bereinigung fehlerhafter Inseln |
| `use_decal_on_terrain` | `True` | Verwendung von Decals auf dem Terrain |
| `terrain_casts_shadows` | `True` | Terrain wirft Schatten |

### Empfohlene Einstellungen für verschiedene Anwendungsfälle

#### Standard-Einstellungen (gute Balance zwischen Qualität und Performance)
* `zoomlevel`: 16
* `curvature_tol`: 3.0
* `mesh_zl`: 16
* `mask_zl`: 16
* `water_smoothing`: 3

#### Hochauflösende Einstellungen (maximale Qualität)
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

### Wichtige Hinweise zu den Parametern

1. **Zoom-Level**: 
    * Höhere Werte bedeuten mehr Details, aber auch größere Dateien und längere Verarbeitungszeit
    * Zoom-Level 16 ist für die meisten Anwendungsfälle ausreichend
    * Zoom-Level 17+ erfordert erheblich mehr Speicherplatz und Verarbeitungszeit

2. **Mesh-Parameter**:
    * `curvature_tol` beeinflusst die Detailgenauigkeit des Geländes
    * Niedrigere Werte erzeugen detailliertere, aber auch komplexere Meshes
    * Werte unter 2.0 können zu Performance-Problemen führen

3. **Wasserparameter**:
    * `water_smoothing` beeinflusst die Qualität der Wasserübergänge
    * Höhere Werte erzeugen weichere Übergänge, aber können Details verlieren
    * `mask_zl` sollte dem `zoomlevel` entsprechen für optimale Ergebnisse

4. **Performance-Parameter**:
    * `max_convert_slots` und `max_download_slots` sollten an die CPU-Leistung angepasst werden
    * Zu hohe Werte können das System überlasten
    * Skip-Parameter sind nützlich für die Wiederverarbeitung einzelner Schritte 