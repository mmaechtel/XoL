# AutoOrtho

Die visuelle Qualität der Landschaftsdarstellung ist ein entscheidender Faktor für **Sichtflüge (VFR)** in Flugsimulatoren. Während X-Plane mit Standardtexturen arbeitet, werden diese häufig als veraltet empfunden. **AutoOrtho** behebt diese Einschränkung durch die **Echtzeit-Integration** von Satellitenbildern und ermöglicht eine präzise Darstellung von Infrastruktur, Vegetation und weiteren Geländemerkmalen. Die letzte von kubilus1 veröffentlichte Version 0.7.2 (21. Januar 2024) optimierte die Integration mit X-Plane und minimiert typische Probleme wie **Szenerie-Konflikte** oder **Leistungseinbußen**.

Inzwischen existiert ein aktiver Fork unter [https://github.com/ProgrammingDinosaur/autoortho4xplane](https://github.com/ProgrammingDinosaur/autoortho4xplane), in dem AutoOrtho kontinuierlich weiterentwickelt wird.

## Funktionsweise

**AutoOrtho** implementiert ein **Streaming-System** für Orthophotos basierend auf der Flugzeugposition und rendert diese als Texturen in X-Plane. Das System operiert über mehrere Schlüsselmechanismen:

- Das **Echtzeit-Streaming-System** lädt Satellitenbilder in Kacheln von Anbietern wie Bing, wobei eine **Zoomstufe** von bis zu 18 (ZL18) implementiert wird, um Detailgenauigkeit und Ladezeit zu optimieren. Kacheln für aktuelle und angrenzende Bereiche werden präventiv geladen, um nahtlose Übergänge zu gewährleisten, was eine stabile Internetverbindung von mindestens 100 Mbps erfordert.

- Ein **virtuelles Dateisystem** (`WinFSP`/`Dokan` unter Windows, `FUSE` unter Linux) verwaltet die Kacheln in einem lokalen Cache auf SSD und stellt sie als Szenerie-Dateien im `z_autoortho`-Ordner des `Custom Scenery`-Verzeichnisses dar.

**AutoOrtho** liefert **2D-Orthophotos** ohne 3D-Objekte. Für die Darstellung von Gebäuden und Vegetation wird **SimHeaven (X-World)** empfohlen, das OpenStreetMap-Daten implementiert. Overlays adaptieren die Bilder an das **X-Plane-Terrain-Mesh** und enthalten essentielle Informationen wie Flughafen-Glättungen, Verkehrsinfrastruktur und Eisenbahnlinien. Bei Verwendung von **SimHeaven X-World** sind die `yOrtho-Overlays` redundant.

Der **Streaming-Prozess** beeinflusst CPU-Auslastung, RAM-Verbrauch (bis zu 64 GB) und Festplattenleistung. Während SSDs Engpässe minimieren, können bei suboptimalen Verbindungen oder unzureichender Hardware **Frame-Drops** auftreten.

### Erweiterte Funktionen des Forks

Der [ProgrammingDinosaur Fork](https://github.com/ProgrammingDinosaur/autoortho4xplane) baut auf der ursprünglichen Codebasis auf und erweitert AutoOrtho um zusätzliche Funktionen:

- **Erhöhte Zoomstufen und Auflösung** für X-Plane 12
- **Neue Benutzeroberfläche** mit modernen Frameworks
- **Überarbeiteter Installer** mit Sicherheitsprüfungen für Zielverzeichnisse
- **Verbesserte Szenerie-Download-Erfahrung** (schneller und benutzerfreundlicher)
- **macOS-Kompatibilität** (nur Apple Silicon)
- **Zusätzliche Kartenanbieter**: Yandex und Apple Maps
- **Automatische scenery_packs.ini-Konfiguration** für die Verwendung mit SimHeaven

## Installation und Konfiguration

### Systemanforderungen

Das System erfordert X-Plane 11.50+ oder X-Plane 12, läuft unter Windows, Linux (mit `FUSE`) oder macOS (Apple Silicon). **Abhängigkeiten** umfassen `WinFSP`/`Dokan` (Windows), `FUSE` (Linux) und optional **Python** 3.x für Quellcode. **Hardwareanforderungen** umfassen 16 GB **RAM**, **SSD**-Speicher und eine schnelle **Internetverbindung** (≥100 Mbps).

**Hinweis**: Der [ProgrammingDinosaur Fork](https://github.com/ProgrammingDinosaur/autoortho4xplane) bietet vollständige macOS-Kompatibilität für Apple Silicon-Prozessoren und erweiterte Funktionen für X-Plane 12.

### Installationsprozess

**AutoOrtho** wird von GitHub (`kubilus1/autoortho`) heruntergeladen, entweder als Binary oder Installer. Für die neuesten Funktionen und Verbesserungen wird der [ProgrammingDinosaur Fork](https://github.com/ProgrammingDinosaur/autoortho4xplane) empfohlen, der einen überarbeiteten Installer mit Sicherheitsprüfungen bietet. Windows-Benutzer installieren `WinFSP`/`Dokan` und starten `autoortho_win.exe`, während Linux-Benutzer `FUSE` benötigen und macOS-Benutzer (Apple Silicon) den entsprechenden Anweisungen folgen sollten.

Die Benutzeroberfläche erfordert die Angabe des X-Plane-Hauptverzeichnisses und des `Custom Scenery`-Verzeichnisses. Regionale Overlays (wenige GB) werden über den "Scenery"-Tab installiert. Der [ProgrammingDinosaur Fork](https://github.com/ProgrammingDinosaur/autoortho4xplane) bietet eine automatische `scenery_packs.ini`-Konfiguration für die Verwendung mit SimHeaven. Die manuelle Konfiguration erfolgt mit folgender Struktur:

```
SCENERY_PACK Custom Scenery/yAutoOrtho_Overlays/
SCENERY_PACK Custom Scenery/z_ao_eur/
SCENERY_PACK Custom Scenery/z_autoortho/
```

Der `z_autoortho`-Eintrag wird am Ende platziert, um anderen Szenerien Priorität zu geben. Die aktuelle Version stellt Platzhalterverzeichnisse wieder her, um eine stabile Reihenfolge zu gewährleisten. **AutoOrtho** muss vor X-Plane gestartet werden, um das **virtuelle Dateisystem** zu mounten, und die `scenery_packs.ini` sollte schreibgeschützt sein bzw. von einem Tool wie xOrganizer verwaltet werden.

Das Verzeichnis `yAutoOrtho_Overlays` wird nur benötigt, sofern nicht **SimHeaven** benutzt wird.

### Konfiguration

Der [ProgrammingDinosaur Fork](https://github.com/ProgrammingDinosaur/autoortho4xplane) bietet eine moderne GUI für alle Konfigurationseinstellungen, die eine einfache Einrichtung ohne manuelle Dateibearbeitung ermöglicht. Die wichtigsten Einstellungen umfassen:

- **X-Plane-Pfad**: Verzeichnis des X-Plane-Installationsordners
- **Cache-Verzeichnis**: Speicherort für Orthofoto-Cache (empfohlen: schnelle SSD)
- **Kartenanbieter**: Auswahl zwischen Bing, Google, Here, Yandex und Apple Maps
- **Cache-Größe**: Maximale Cache-Größe in GB
- **Wartezeit**: Balance zwischen Qualität und Reaktionszeit
- **Zoom-Level**: Mindest- und Maximalzoom für Satellitenbilder
- **Autostart**: Automatischer Start mit X-Plane
- **Debug-Modus**: Erweiterte Logging-Informationen

Für erweiterte Konfigurationen kann weiterhin die `.autoortho`-Konfigurationsdatei manuell bearbeitet werden, wenn gewünscht.

Für optimale Erfahrung fügt SimHeaven X-World 3D-Objekte und Autogen hinzu, während xOrganizer/xToolbox die Szenerie-Verwaltung vereinfacht. vStates bietet eine Alternative für vorgefertigte Orthophotos.

### Vergleich mit Ortho4XP

AutoOrtho und Ortho4XP erfüllen unterschiedliche Zwecke im X-Plane-Ökosystem. AutoOrtho streamt Daten in Echtzeit von Bing/USGS, benötigt minimalen Speicher (wenige GB Cache) aber eine konstante Internetverbindung. Es arbeitet mit bis zu ZL16, was einen guten Kompromiss zwischen Detail und Leistung bietet. Im Gegensatz dazu verwendet Ortho4XP vorbereitete lokale Kacheln von Bing/Google, benötigt hunderte GB Speicher, unterstützt aber bis zu ZL19 für maximale Details.

AutoOrthos Leistung kann gelegentliches Ruckeln zeigen und stellt höhere Anforderungen an CPU/RAM, während Ortho4XP stabilere Leistung mit lokal gespeicherten Daten bietet. Die Einrichtung ist mit AutoOrtho nach der initialen Konfiguration einfacher, während Ortho4XP zeitaufwändige Kachelerstellung erfordert, aber detailliertere Szenerien für bestimmte Regionen bietet.

### Häufige Probleme und Lösungen

Für grundlegende Installations- und Konfigurationsprobleme (Initialisierungsfehler, FUSE-Probleme, Python-Modul-Probleme, Performance-Probleme) wird auf die aktuelle Dokumentation des [ProgrammingDinosaur Forks](https://github.com/ProgrammingDinosaur/autoortho4xplane) verwiesen, da diese Probleme in der neueren Version behoben oder vereinfacht wurden.

Weitere spezifische Probleme bei der Verwendung von AutoOrtho:

1. **Flughafen-Topographie-Probleme**:
    - Ursache: Fehlende automatische **Flughafen-Glättung** bzw. fehlende **Ortho Patches** für die **Flughafen-Szenerie**
    - Lösung: Implementierung von **Ortho Patches** oder dem `flatten 1` Parameter in der `apt.dat` und Überprüfung der **Priorisierung** von **Flughafen-Szenerien**

2. **Netzwerkprobleme**:
    - Log-Eintrag: `HTTP 429: Too Many Requests`
    - Ursache: Bing-Blacklisting
    - Lösung: VPN verwenden oder zu USGS-Quellen wechseln

3. **Szenerie-Konflikte**:
    - Log-Eintrag: `Warning: z_autoortho not found in scenery_packs.ini`
    - Ursache: Falsche Szenerie-Reihenfolge
    - Lösung: Reihenfolge in scenery_packs.ini korrigieren

4. **Speicherprobleme**:
    - Log-Eintrag: `MemoryError: Out of memory`
    - Ursache: Hohe RAM-Auslastung
    - Lösung: Cache-Größe reduzieren, X-Plane-Grafikeinstellungen senken. 
    
5. **Abstürze**:
    - Ursache: RAM-Überlastung oder Add-on-Konflikte
    - Lösung: Deaktivieren von Add-ons, Erhöhen des RAMs oder Reduzieren der Cache-Größe

### Log-Analyse

Der Benutzer kann die autoortho.log mit verschiedenen Methoden analysieren:

- Gesamtes Log anzeigen:
    ```bash
    cat ~/.autoortho-data/autoortho.log | less
    ```

- Log in Echtzeit überwachen:
    ```bash
    tail -f ~/.autoortho-data/autoortho.log
    ```

- Nach spezifischen Fehlern suchen:
    ```bash
    grep -i "error" ~/.autoortho-data/autoortho.log
    ```

Für detailliertere Log-Informationen kann in den Settings oder der `.autoortho` Konfigurationsdatei der Debug-Modus aktiviert werden:

```ini
# Debug-Modus
debug = true
```

## Linux-spezifische Installation

### Installationsbeispiel: AutoOrtho auf Debian 12 mit pyenv

Dieser Abschnitt bietet eine detaillierte Anleitung zur Installation von AutoOrtho mit der Python-Version auf einem Debian 12-System. Das Beispiel zeigt, wie eine isolierte Python-Umgebung mit pyenv eingerichtet wird und enthält umfassende Fehlerbehebung mit der autoortho.log-Datei.

**Hinweis**: Für die neuesten Funktionen wird der [ProgrammingDinosaur Fork](https://github.com/ProgrammingDinosaur/autoortho4xplane) empfohlen, der eine verbesserte GUI und erweiterte Kompatibilität bietet.

### Systemanforderungen

Das Beispielsystem läuft mit Debian 12 (Bookworm) und X-Plane 12, verfügt über eine SSD, 32 GB RAM und eine stabile Internetverbindung mit 200 Mbps. Erforderliche Abhängigkeiten umfassen:

- fuse3 für das virtuelle Dateisystem
- git, build-essential, libssl-dev, zlib1g-dev für pyenv und Python
- Python 3.12+ (verwaltet über pyenv) - empfohlen für den ProgrammingDinosaur Fork
- Einige GB SSD-Speicher für Overlays und Cache

### Schritt-für-Schritt Installation

1. **Systemvorbereitung**:
    Der Benutzer aktualisiert das System und installiert grundlegende Abhängigkeiten:

    ```bash
    sudo apt update && sudo apt upgrade -y
    sudo apt install -y fuse3 libfuse2 git curl build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev wget llvm libncurses5-dev libncursesw5-dev \
    xz-utils tk-dev libffi-dev liblzma-dev python3-openssl
    ```

2. **pyenv-Einrichtung**:
    Nach der Installation von pyenv konfiguriert der Benutzer seine Umgebung:

    ```bash
    curl https://pyenv.run | bash
    ```

    Zu ~/.bashrc hinzufügen:
    ```bash
    export PATH="$HOME/.pyenv/bin:$PATH"
    eval "$(pyenv init --path)"
    eval "$(pyenv init -)"
    ```

    Python 3.12.0 installieren:
    ```bash
    pyenv install 3.12.0
    pyenv global 3.12.0
    ```

3. **AutoOrtho-Installation**:
    Repository klonen und virtuelle Umgebung einrichten:

    ```bash
    # Für den ProgrammingDinosaur Fork (empfohlen):
    git clone https://github.com/ProgrammingDinosaur/autoortho4xplane.git ~/autoortho
    cd ~/autoortho

    pyenv virtualenv 3.12.0 autoortho
    pyenv activate autoortho
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

4. **X-Plane-Konfiguration**:
    scenery_packs.ini mit der korrekten Reihenfolge konfigurieren:

    ```
    SCENERY_PACK Custom Scenery/yAutoOrtho_Overlays/
    SCENERY_PACK Custom Scenery/z_ao_eur/
    SCENERY_PACK Custom Scenery/z_autoortho/
    ```

    Datei schreibgeschützt machen:
    ```bash
    chmod 444 ~/X-Plane-12/Custom\ Scenery/scenery_packs.ini
    ```

## Fazit

Dieses Installationsbeispiel zeigt, wie AutoOrtho in einer Python-Umgebung auf Debian 12 eingerichtet wird. Die Python-Version bietet Flexibilität durch Quellcode-Zugriff, während die autoortho.log-Datei detaillierte Einblicke in den Systembetrieb liefert. Mit korrekter Konfiguration und Optimierung können Benutzer hochwertige Orthophotos in X-Plane 12 genießen, verbessert durch 3D-Objekte von SimHeaven.

Die Kombination von AutoOrtho mit SimHeaven X-World schafft eine umfassende Szenerie-Lösung, die sowohl detaillierte Orthophotos als auch präzise 3D-Objekte bietet. Während AutoOrtho die Bodentexturen handhabt, fügt SimHeaven Gebäude, Bäume und andere 3D-Elemente basierend auf OpenStreetMap-Daten hinzu.

## Ressourcen

- [GitHub Repository](https://github.com/kubilus1/autoortho)
- [X-Plane.org Forum](https://forums.x-plane.org/forums/forum/802-autoortho-streaming-ortho-imagery-for-x-plane/)