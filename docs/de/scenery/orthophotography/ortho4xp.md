# Ortho4XP

Ortho4XP ist ein leistungsstarkes Tool zur Erstellung von Orthofotos für X-Plane. Es ermöglicht die Generierung von hochauflösenden Bodentexturen aus Satellitenbildern und Höhendaten.

## Installation und Versionen

Ortho4XP ist in zwei Hauptversionen verfügbar:

1. **Originalversion** von Oscar Pilote:
    * [GitHub Repository](https://github.com/oscarpilote/Ortho4XP)
    * Die ursprüngliche Version mit grundlegenden Funktionen


2. **Fork von shred86** (empfohlen):
    * [GitHub Repository](https://github.com/shred86/Ortho4XP)
    * [Detaillierte Dokumentation](https://github.com/shred86/Ortho4XP/wiki)
    * Enthält zahlreiche Verbesserungen und neue Funktionen
    * [Binaries für verschiedene Betriebssysteme](https://github.com/shred86/Ortho4XP/wiki/Installation)

### Installationsmethoden

1. **Mit Binaries (empfohlen)**:
    - Die passende Version für das Betriebssystem herunterladen
    - Das Archiv entpacken
    - Die ausführbare Datei ausführen

2. **Manuelle Installation**:
    - Die gewünschte Version herunterladen
    - Sicherstellen, dass Python 3.x installiert ist
    - Die erforderlichen Python-Pakete installieren:
        ```bash
        pip install -r requirements.txt
        ```

3. **Alternative Installation für Linux**:
    - Installation mit Docker (siehe [Docker Dokumentation](../../extensions/docker.md))
    - Installation mit pyenv (siehe [pyenv Dokumentation](../../extensions/pyenv.md))

## Verwendung und Konfiguration

### Grundlegende Verwendung

1. Ortho4XP über die Python-Datei oder die ausführbare Datei starten:
   ```bash
   python Ortho4XP.py
   ```

2. Im Hauptfenster auswählen:
    - Den Zielbereich (Tile)
    - Die gewünschte Zoomstufe (ZL)
    - Die Bildquelle (z.B. Bing, Google, Here)

3. Auf "Build" klicken, um den Prozess zu starten

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
| `road_level` | `2` | Welche Arten von Strassen sollen dargestellt werden |
| `min_area` | `0.001` | minimale Größe von Wasserflächen |

### Empfohlene Einstellungen

#### Standard-Einstellungen (gute Balance)

* `zoomlevel`: 17
* `curvature_tol`: 2.0
* `mesh_zl`: 18
* `mask_zl`: 15
* `cover_zl`: 17
* `min_area`: 0.01
* `apt_smoothing_pix`: 16

#### Hochauflösende Einstellungen

* `zoomlevel`: 18
* `curvature_tol`: 1.3
* `mesh_zl`: 19
* `mask_zl`: 16
* `cover_zl`: 18
* `min_area`: 0.001
* `apt_smoothing_pix`: 8

#### Performance-optimierte Einstellungen

* `zoomlevel`: 16
* `curvature_tol`: 3.0
* `mesh_zl`: 16
* `mask_zl`: 14
* `cover_zl`: 16
* `min_area`: 0.1
* `apt_smoothing_pix`: 32

## Integration von LiDAR-Daten

Ortho4XP unterstützt die Integration von hochauflösenden LiDAR-Daten für eine verbesserte Geländedarstellung. Diese Daten sind besonders für Gebiete mit komplexer Topographie wie die Alpen oder andere Bergregionen nützlich.

### Verfügbare LiDAR-Daten

Die LiDAR-Daten von [sonny.4lima.de](https://sonny.4lima.de) bieten eine hohe Auflösung und Genauigkeit für verschiedene Regionen. Diese Daten können in Ortho4XP auf zwei Arten integriert werden:

**Methode 1: Einzelne Kacheln**
- Die LiDAR-Daten als `custom_dem` in Ortho4XP verwenden
- Diese Methode eignet sich für einzelne Kacheln oder kleine Bereiche
- Die LiDAR-Daten werden nur für spezifische Kacheln verwendet

**Methode 2: Größere Bereiche**
- Die DEM-Dateien im Ortho4XP-Verzeichnis ersetzen
- Diese Methode eignet sich für größere Regionen
- Ortho4XP verwendet die LiDAR-Daten automatisch für alle Kacheln in der Region

### Schritte zur Integration

1. Die gewünschten LiDAR-Daten von [sonny.4lima.de](https://sonny.4lima.de) herunterladen
2. Für Methode 2 gibt es nun zwei Möglichkeiten:

    - Die Dateien in das Ortho4XP-Verzeichnis entpacken und die Kacheln entsprechend in die Verzeichnisse unter Elevation_data sortieren. Dabei helfen Skripte wie z.B. [hier](https://forum.aerosoft.com/index.php?/topic/175397-h%C3%B6hendaten-f%C3%BCr-ortho4xp/#findComment-1102723) 
    - Oder mit Links unter `Elevation_data` arbeiten:
        - Zuerst das alte `Elevation_data` sichern
        - Neues `Elevation_data` anlegen und darin die Verzeichnisse `+00-060` usw. als Links auf ein extra Verzeichnis (z.B. `GlobalElevationData`) anlegen. Folgendes Skript erstellt im neuen leeren `Elevation_data` alle nötigen Verzeichnisse als Links auf das Verzeichnis `../GlobalElevationData`:
        ```bash
        #!/bin/bash

        # Zielpfad für symbolische Links
        TARGET_PATH="../GlobalElevationData"

        # Zielverzeichnis erstellen, falls nicht vorhanden
        mkdir -p "$TARGET_PATH"

        # Funktion zum Erstellen eines Linknamens
        create_link_name() {
          local lat=$1
          local lon=$2
          # Breitengrad formatieren (+XX oder -XX)
          if [ $lat -ge 0 ]; then
            lat_str=$(printf "+%02d" $lat)
          else
            lat_str=$(printf "%03d" $lat)
          fi
          # Längengrad formatieren (+YYY oder -YYY)
          if [ $lon -ge 0 ]; then
            lon_str=$(printf "+%03d" $lon)
          else
            lon_str=$(printf "%04d" $lon)
          fi
          echo "${lat_str}${lon_str}"
        }

        # Alle möglichen Links generieren
        for lat in $(seq -80 10 80); do    # Breitengrade: -80° bis +80° in 10°-Schritten
          for lon in $(seq -180 10 180); do # Längengrade: -180° bis +180° in 10°-Schritten
            link_name=$(create_link_name $lat $lon)
            ln -s "$TARGET_PATH" "./$link_name"
          done
        done
        ```
        - Dann in das `GlobalElevationData`-Verzeichnis alle HGT-Dateien kopieren
3. Die gewünschte Integrationsmethode wählen (Methode 1 oder 2)
4. Die Kacheln wie gewohnt generieren

Die verbesserte Geländedarstellung wird automatisch in den generierten Kacheln übernommen.

!!! note "Hinweis"
    Die LiDAR-Daten sind besonders nützlich für Gebiete mit komplexer Topographie wie die Alpen oder andere Bergregionen. Sie bieten eine deutlich höhere Auflösung und Genauigkeit als die standardmäßig verfügbaren DEM-Daten.

## Ortho Patches für Szenerien

Viele Szenerien – sowohl Standard- als auch Third-Party-Szenerien – sind ursprünglich auf das alte, flache Mesh-Modell von X-Plane ausgelegt. In der Datei `apt.dat` kann hierfür das Flag `flatten 1` gesetzt sein. Dieses Flag sorgt dafür, dass die Szenerie selbst und häufig auch größere Teile der Umgebung vollständig flach dargestellt werden. Das steht im Widerspruch zu dem Ziel, mit Ortho4XP ein möglichst genaues und realistisches Bodenmesh zu erzeugen.

Für einige Szenerien existieren spezielle Ortho Patches, die entweder vom Hersteller selbst oder von aktiven X-Plane-Nutzern bereitgestellt werden. Mithilfe dieser Patches kann das Mesh-Modell mit Ortho4XP gezielt an die jeweilige Szenerie angepasst werden. Zudem erlauben Modifikationen an der Szenerie, auf das Setzen von `flatten 1` zu verzichten und dennoch eine korrekte Darstellung zu erreichen.

Falls keine solchen Modifikationen oder Patches verfügbar sind, kann oft auch das manuelle Entfernen der Zeile mit `flatten 1` in der entsprechenden `apt.dat`-Datei helfen. Dadurch wird die Szenerie an das neue, detaillierte Bodenmodell angepasst. Es können dabei jedoch kleinere Artefakte auftreten, wie etwa Objekte, die nicht mehr exakt auf dem Boden stehen, sondern gelegentlich leicht in der Luft schweben oder im Boden versinken.

## Wichtige Hinweise und Fehlerbehebung

### Allgemeine Hinweise

- Ortho4XP benötigt viel Speicherplatz für die generierten Texturen
- Die Qualität der Orthofotos hängt von der gewählten Bildquelle ab
- Die Verarbeitung kann je nach Gebietsgröße und Zoomstufe mehrere Stunden dauern
- Der shred86 Fork bietet bessere Performance und mehr Funktionen
- Die Verwendung der Binaries vereinfacht die Installation erheblich

### Performance-Optimierung

- Die Verarbeitungszeit hängt stark von der gewählten Zoomstufe und der Gebietsgröße ab
- Zu hohe Zoomstufen können das System überlasten
- Skip-Parameter sind nützlich für die Wiederverarbeitung einzelner Schritte
- Die Verwendung einer SSD kann die Verarbeitungszeit deutlich reduzieren

### Optimierung der Dateigröße

Da Ortho4XP große Mengen an Texturen generiert, kann der Speicherplatzbedarf schnell ansteigen. Um die Dateigröße der Orthofotos zu optimieren, stehen verschiedene Tools zur Verfügung:

#### Windows 11
[`texconv`](https://github.com/Microsoft/DirectXTex/wiki/Texconv) (DirectXTex, Microsoft) ermöglicht die Skalierung von Texturen auf 2048x2048 Pixel mit dem Befehl `texconv.exe *.* -w 2048 -h 2048 -y`. Das Tool ist registrierungsfrei und eignet sich besonders für die Batch-Verarbeitung.

#### macOS und Linux
ImageMagick bietet eine plattformübergreifende Lösung. Nach der Installation (`brew install imagemagick` für macOS, `sudo apt-get install imagemagick` für Linux) können DDS-Dateien mit `mogrify -resize 2048x2048 *.dds` skaliert werden.

Diese Tools reduzieren die Dateigröße effizient, während die visuelle Qualität erhalten bleibt. Die optimierte Größe von 2048x2048 Pixel bietet einen guten Kompromiss zwischen Qualität und Speicherplatzbedarf.

### Fehlerbehebung

Bei Problemen:

1. Die Log-Dateien im Ortho4XP-Verzeichnis überprüfen
2. Sicherstellen, dass alle Python-Abhängigkeiten installiert sind
3. Die [Dokumentation des shred86 Forks](https://github.com/shred86/Ortho4XP/wiki) konsultieren
4. Das [X-Plane Forum](https://forums.x-plane.org/index.php?/forums/forum/310-ortho4xp/) besuchen 