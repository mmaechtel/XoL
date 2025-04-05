# AutoOrtho

AutoOrtho ist ein Tool für X-Plane, das Orthofotos in den Flugsimulator integriert. Es ermöglicht die Nutzung von hochauflösenden Luftbildern als Bodentexturen und verbessert damit die visuelle Realität in X-Plane deutlich.

## Installation

1. Laden Sie die neueste Version von AutoOrtho von der [offiziellen GitHub-Seite](https://github.com/kubilus1/autoortho) herunter
2. Entpacken Sie das Archiv in einen Ordner Ihrer Wahl
3. Stellen Sie sicher, dass Python 3.x installiert ist
4. Installieren Sie die erforderlichen Python-Pakete:
   ```bash
   pip install -r requirements.txt
   ```

## Grundlegende Verwendung

1. Starten Sie AutoOrtho über die Python-Datei:
   ```bash
   python autoortho.py
   ```

2. Wählen Sie im Hauptfenster:
   - Die Bildquelle (z.B. Bing, Google, Here)
   - Den Zielbereich

3. Klicken Sie auf "Start" um den Prozess zu starten

## Konfiguration

Die Konfigurationsdatei `.autoortho` wird im Home-Verzeichnis erstellt und kann mit einem Texteditor bearbeitet werden. Hier sind die wichtigsten Parameter:

```ini
# X-Plane Verzeichnis
xplane_path = /pfad/zum/xplane

# Cache-Verzeichnis für Orthofotos
cache_dir = /pfad/zum/cache

# Bildquelle (bing, google, here)
provider = bing

# Cache-Größe in GB
cache_size = 20

# Anzahl der Download-Threads
download_threads = 4

# Automatischer Start mit X-Plane
autostart = true

# Debug-Modus (true/false)
debug = false
```

### Wichtige Parameter-Erklärungen

- `xplane_path`: Pfad zum X-Plane Hauptverzeichnis
- `cache_dir`: Verzeichnis für den Orthofoto-Cache (empfohlen: schnelle SSD)
- `provider`: Bildquelle für die Orthofotos
- `cache_size`: Maximale Größe des Caches in GB
- `download_threads`: Anzahl der parallelen Downloads
- `autostart`: AutoOrtho automatisch mit X-Plane starten
- `debug`: Debug-Informationen in den Logs aktivieren

## Wichtige Hinweise

- AutoOrtho läuft als Hintergrunddienst und generiert Orthofotos während des Flugs
- Die Texturen werden in einem Cache gespeichert, um wiederholte Downloads zu vermeiden
- Eine stabile Internetverbindung ist für das Streaming der Orthofotos erforderlich
- Die Qualität der Orthofotos wird automatisch an die Flughöhe angepasst

## Fehlerbehebung

Bei Problemen:
1. Überprüfen Sie die Log-Dateien im AutoOrtho-Verzeichnis
2. Stellen Sie sicher, dass alle Python-Abhängigkeiten installiert sind
3. Überprüfen Sie die Internetverbindung für den Download der Bilddaten
4. Konsultieren Sie das [AutoOrtho-Forum](https://forums.x-plane.org/index.php?/forums/forum/406-autoortho/) für weitere Hilfe
