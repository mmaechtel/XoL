# Erste Schritte mit X-Plane unter Linux

Diese Anleitung führt Sie durch die ersten Schritte, um X-Plane unter Linux optimal einzurichten. Sie richtet sich an Linux-erfahrene Benutzer und baut auf einer bestehenden Linux-Installation auf.

## Systemvoraussetzungen

X-Plane 12 ist ein anspruchsvoller Flugsimulator, der erhebliche Systemressourcen benötigt, besonders für realistische Simulationen in hohen Auflösungen. Im Gegensatz zu vielen anderen Anwendungen nutzt X-Plane intensiv Single-Core-Performance und stellt hohe Anforderungen an die Grafikkarte.

### Empfohlene Anforderungen
- **CPU**: Aktuelle Generation mit hoher Single-Core-Performance (Intel Core i7/i9 oder AMD Ryzen 7/9)
  - *Warum?* X-Plane nutzt hauptsächlich einen CPU-Kern für die Flugphysik-Berechnungen. Eine hohe Single-Core-Geschwindigkeit ist entscheidend für flüssige Framerates.
  
- **RAM**: 32 GB oder mehr
  - *Warum?* Speicherhungrige Addons, detaillierte Szenerien und Orthofotos können den RAM-Verbrauch drastisch erhöhen.
  
- **Grafikkarte**: Hochleistungs-GPU mit mindestens 8 GB VRAM (z.B. NVIDIA RTX 3080/4080 oder höher)
  - *Warum?* Insbesondere für 4K-Auflösung oder Multi-Monitor-Setups benötigen Sie viel Grafikleistung und VRAM. Hochauflösende Texturen und komplexe Beleuchtungseffekte fordern selbst High-End-GPUs.
  
- **Speicherplatz**: 250 GB oder mehr SSD-Speicher (NVMe empfohlen)
  - *Warum?* Die Basisinstallation benötigt bereits etwa 70 GB, und Orthofotos können schnell Hunderte von GB belegen. SSD-Geschwindigkeit reduziert Nachladezeiten während des Flugs.
  
- **Netzwerk**: Schnelle Internetverbindung für Ortho-Streaming und Kartenaktualisierungen
  - *Warum?* Echtzeitdaten wie Wetter und Luftverkehr sowie Streaming-Orthofotos benötigen eine zuverlässige Verbindung.

### Hardware-Optimierungen
- SSD/NVMe-Laufwerk für Betriebssystem und X-Plane Installation
- Dedizierte Grafikkarte mit aktuellen Treibern
- Multiple Monitore für erweitertes Cockpit-Setup
- Gutes Kühlsystem, da X-Plane CPU und GPU stark belastet

*Hinweis: Selbst bei Einhaltung dieser Empfehlungen ist zu beachten, dass X-Plane durch seine Single-Core-Limitierung auch auf High-End-Hardware Performanceeinschränkungen haben kann. Die empfohlenen Optimierungen in dieser Dokumentation helfen, das Beste aus der vorhandenen Hardware herauszuholen.*

## Debian Linux installieren

Diese Dokumentation geht davon aus, dass Sie Debian Linux in der aktuellen Stable-Version bereits installiert haben und mit einer funktionierenden grafischen Benutzeroberfläche arbeiten. Falls Sie Debian noch installieren müssen, finden Sie hier die wichtigsten Ressourcen:

### Offizielle Installationsquellen
- [Debian-Hauptserver](https://www.debian.org/) - Hier finden Sie immer die aktuelle Stable-Version
- [Weltweite Debian-Spiegelserver](https://www.debian.org/mirror/list) - Wählen Sie einen Server in Ihrer Nähe für schnellere Downloads
- [Debian-Netzwerkinstallation](https://www.debian.org/distrib/netinst) - Minimale ISO für Netzwerkinstallation (empfohlen)

### Wahl der richtigen Version
- Verwenden Sie stets die aktuelle **Stable**-Version von Debian für maximale Stabilität
- Die Stable-Version wird auf der [Debian-Hauptseite](https://www.debian.org/) prominent angezeigt
- Für X-Plane-Performance immer die 64-Bit-Version (amd64) wählen

### Tipps für die Installation
- Wählen Sie während der Installation die Desktop-Umgebung "GNOME" oder "KDE Plasma" für beste Kompatibilität
- Aktivieren Sie bei der Partitionierung mindestens 8 GB Swap-Speicher
- Richten Sie separate Partitionen für `/` (root, mindestens 50 GB) und `/home` (restlicher Speicher) ein
- Installieren Sie den GRUB-Bootloader auf dem Hauptlaufwerk

### Nach der Installation
Nach erfolgreicher Installation und Anmeldung in der grafischen Benutzeroberfläche sind folgende Schritte empfehlenswert:

1. System vollständig aktualisieren:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. Installieren Sie wichtige Basis-Pakete:
   ```bash
   sudo apt install build-essential dkms git curl wget nano
   ```

Die folgenden Kapitel dieser Dokumentation setzen eine funktionierende Debian-Installation voraus und konzentrieren sich auf die Optimierung für X-Plane.

## X-Plane 12 unter Linux installieren

X-Plane 12 läuft nativ unter Linux und benötigt im Gegensatz zu vielen anderen Spielen und Simulatoren keine Kompatibilitätsschicht wie Wine oder Proton. Hier sind die Schritte zur Installation:

### Vorbereitungen
Bevor Sie X-Plane 12 installieren, sollten Sie folgende Vorbereitungen treffen:

1. **Grafiktreiber aktualisieren** - Für Nvidia-GPUs installieren Sie den aktuellen proprietären Treiber:
   ```bash
   sudo apt install nvidia-driver
   ```
   *Weitere Details finden Sie im Kapitel [Nvidia-Treiber](nvidia.md).*

2. **OpenGL-Bibliotheken installieren**:
   ```bash
   sudo apt install libgl1-mesa-glx libgl1-mesa-dri
   ```

3. **Audiokomponenten sicherstellen**:
   ```bash
   sudo apt install pulseaudio pavucontrol
   ```

### Installationsmethoden

Sie haben zwei Hauptmöglichkeiten, X-Plane 12 zu installieren:

#### 1. Steam-Version (empfohlen für Einsteiger)
1. [Steam für Linux installieren](https://store.steampowered.com/about/)
2. X-Plane 12 in der Steam-Bibliothek kaufen und installieren
3. Folgen Sie den Anweisungen des Steam-Installers

**Vorteile der Steam-Version:**
- Automatische Updates
- Einfache Installation
- Steam-Workshop-Integration für Addons
- Komfortabler Support für Steam-Controller und andere Hardware

#### 2. Standalone-Version (direkter Download von Laminar Research)
1. Besuchen Sie die [offizielle X-Plane-Website](https://www.x-plane.com/)
2. Kaufen Sie X-Plane 12 und laden Sie den Installer herunter
3. Installer ausführbar machen:
   ```bash
   chmod +x X-Plane-installer.run
   ```
4. Installer starten:
   ```bash
   ./X-Plane-installer.run
   ```
5. Folgen Sie den Anweisungen des grafischen Installers

**Vorteile der Standalone-Version:**
- Volle Kontrolle über Installationsverzeichnis
- Unabhängig von Steam
- Direktes Update über den X-Plane Updater
- Oft schnellere Updates bei neuen Versionen

### Nach der Installation

Nach erfolgreicher Installation sollten Sie folgende Schritte durchführen:

1. **Erstes Starten**: Starten Sie X-Plane einmal und schließen Sie es wieder, damit Konfigurationsdateien erstellt werden

2. **Leistungseinstellungen optimieren**:
   - Starten Sie X-Plane
   - Gehen Sie zu "Einstellungen" > "Grafik"
   - Passen Sie die Einstellungen entsprechend Ihrer Hardware an:
     - Für höhere FPS: Reduzieren Sie Sichtweite und Objektdetails
     - Für bessere Qualität: Erhöhen Sie Texturqualität und Anti-Aliasing
     - Aktivieren Sie die Vulkan-Rendering-API für bessere Performance

3. **Speichern Sie ein benutzerdefiniertes Grafikprofil** für verschiedene Szenarien (Flugtraining, Fotografie, etc.)

4. **Prüfen Sie die Performance** mit den eingebauten FPS-Anzeige (Aktivierung mit der Taste `Shift+Strg+F`)

### Fehlerbehebung bei X-Plane Installation

Falls Probleme auftreten:

- **X-Plane startet nicht**: Prüfen Sie das Logfile in `~/X-Plane 12/Log.txt`
- **Schlechte Performance**: Aktualisieren Sie die Grafiktreiber und reduzieren Sie die Grafikeinstellungen
- **Abstürze**: Stellen Sie sicher, dass alle X-Plane-Dateien korrekt heruntergeladen wurden
- **Eingabegeräte werden nicht erkannt**: Installieren Sie `jstest-gtk` zur Diagnose und Kalibrierung

## Probleme bei der Installation

Bei Problemen können folgende Schritte helfen:

- Prüfen Sie die GPU-Treiber-Kompatibilität
- Stellen Sie sicher, dass alle Linux-Pakete aktuell sind
- Überprüfen Sie die X-Plane-Systemanforderungen auf der offiziellen Website
- Konsultieren Sie das [Glossar](glossary.md) für technische Begriffe

Je nach verwendeter Hardware und Linux-Distribution können spezifische Anpassungen erforderlich sein. Die hier gezeigten Beispiele wurden mit Debian getestet, funktionieren aber mit geringfügigen Änderungen auch auf anderen Distributionen. 