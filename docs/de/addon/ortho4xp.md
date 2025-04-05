# Ortho4XP

Ortho4XP ist ein leistungsstarkes Tool zur Erstellung von Orthofotos für X-Plane. Es ermöglicht die Generierung von hochauflösenden Bodentexturen aus Satellitenbildern und Höhendaten.

## Quellen

Ortho4XP ist in zwei Hauptversionen verfügbar:

1. **Originalversion** von Oscar Pilote:
   
   - [GitHub Repository](https://github.com/oscarpilote/Ortho4XP)
   - Die ursprüngliche Version mit grundlegenden Funktionen
   - [Binaries verfügbar](https://github.com/kubilus1/autoortho/releases/tag/0.7.2)

2. **Fork von shred86**:
   
   - [GitHub Repository](https://github.com/shred86/Ortho4XP)
   - [Detaillierte Dokumentation](https://github.com/shred86/Ortho4XP/wiki)
   - Enthält zahlreiche Verbesserungen und neue Funktionen
   - [Binaries für verschiedene Betriebssysteme](https://github.com/shred86/Ortho4XP/wiki/Installation)

## Installation

Ortho4XP kann auf zwei Arten installiert werden:

### Installation mit Binaries (empfohlen)

1. Laden Sie die passende Version für Ihr Betriebssystem herunter:
   - Originalversion: [Releases](https://github.com/kubilus1/autoortho/releases/tag/0.7.2)
   - shred86 Fork: [Installationsseite](https://github.com/shred86/Ortho4XP/wiki/Installation)
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
- Installation mit Docker (siehe [Docker Dokumentation](../docker.md))
- Installation mit pyenv (siehe [pyenv Dokumentation](../pyenv.md))

## Grundlegende Verwendung

1. Starten Sie Ortho4XP über die Python-Datei oder die ausführbare Datei:
   ```bash
   python Ortho4XP.py
   ```

2. Wählen Sie im Hauptfenster:
   - Den Zielbereich (Tile)
   - Die gewünschte Zoomstufe (ZL)
   - Die Bildquelle (z.B. Bing, Google, Here)

3. Klicken Sie auf "Build" um den Prozess zu starten

## Besonderheiten des shred86 Forks

Der Fork von shred86 bietet zahlreiche Verbesserungen gegenüber der Originalversion:

### Neue Funktionen

- Verbesserte Benutzeroberfläche mit Dark Mode
- Erweiterte Konfigurationsmöglichkeiten
- Unterstützung für mehr Bildquellen
- Verbesserte Fehlerbehandlung und Logging
- Automatische Updates

### Technische Verbesserungen

- Optimierte Speichernutzung
- Schnellere Verarbeitung
- Bessere Fehlertoleranz
- Erweiterte Kompatibilität mit verschiedenen Systemen

### Zusätzliche Features

- Batch-Verarbeitung mehrerer Tiles
- Erweiterte Mesh-Optionen
- Verbesserte Wassermasken
- Unterstützung für mehr Höhendatenquellen
- Erweiterte Konfigurationsdateien

## Wichtige Hinweise

- Ortho4XP benötigt viel Speicherplatz für die generierten Texturen
- Die Qualität der Orthofotos hängt von der gewählten Bildquelle ab
- Die Verarbeitung kann je nach Gebietsgröße und Zoomstufe mehrere Stunden dauern
- Der shred86 Fork bietet bessere Performance und mehr Funktionen
- Die Verwendung der Binaries vereinfacht die Installation erheblich
- Für Linux-Benutzer bieten Docker und pyenv flexible Alternativen zur direkten Installation

## Fehlerbehebung

Bei Problemen:
1. Überprüfen Sie die Log-Dateien im Ortho4XP-Verzeichnis
2. Stellen Sie sicher, dass alle Python-Abhängigkeiten installiert sind
3. Konsultieren Sie die [Dokumentation des shred86 Forks](https://github.com/shred86/Ortho4XP/wiki) für detaillierte Anleitungen
4. Besuchen Sie das [X-Plane Forum](https://forums.x-plane.org/index.php?/forums/forum/310-ortho4xp/) für weitere Hilfe 