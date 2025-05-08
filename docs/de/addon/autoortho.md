# AutoOrtho

Die visuelle Qualität der Landschaften ist entscheidend für Sichtflüge (VFR) in Flugsimulatoren. Während X-Plane Standardtexturen bereitstellt, werden diese oft als veraltet empfunden. AutoOrtho behebt dieses Problem durch die Echtzeit-Integration von Satellitenbildern und bietet eine detaillierte Darstellung von Straßen, Wäldern und anderen Merkmalen. Die aktuelle Version 0.7.2, veröffentlicht am 28. Januar 2024, optimiert die Integration mit X-Plane und reduziert häufige Probleme wie Szenerie-Konflikte oder Leistungseinbußen.

## Funktionsweise

AutoOrtho streamt Orthophotos basierend auf der Flugzeugposition und rendert sie als Texturen in X-Plane. Das System arbeitet über mehrere Schlüsselmechanismen:

Das Echtzeit-Streaming-System lädt Satellitenbilder in Kacheln von Anbietern wie Bing, wobei eine Zoomstufe von 16 (ZL16) verwendet wird, um Detail und Ladezeit auszubalancieren. Kacheln für aktuelle und angrenzende Bereiche werden vorab geladen, um nahtlose Übergänge zu gewährleisten, was eine stabile Internetverbindung von mindestens 100 Mbps erfordert.

Geladene Kacheln werden lokal zwischengespeichert, um wiederholte Downloads zu vermeiden. Der Cache, der mehrere Gigabyte umfassen kann, wird auf einer SSD gespeichert. Benutzer können die Cache-Größe anpassen oder bei Bedarf leeren. Ein virtuelles Dateisystem (WinFSP/Dokan unter Windows, FUSE unter Linux) stellt die Kacheln als Szenerie-Dateien dar und füllt den z_autoortho-Ordner im Custom Scenery-Verzeichnis dynamisch.

AutoOrtho liefert 2D-Orthophotos ohne 3D-Objekte. Für Gebäude und Bäume wird SimHeaven (X-World) empfohlen, das OpenStreetMap-Daten nutzt. Overlays passen die Bilder an das X-Plane-Terrain-Mesh an. Diese Overlays enthalten wichtige Informationen wie Flughafen-Glättungen, Straßen, Eisenbahnlinien und andere Geländemerkmale, die für eine realistische Darstellung notwendig sind. Bei Verwendung von SimHeaven X-World sind die yOrtho-Overlays nicht erforderlich, da SimHeaven bereits alle notwendigen Overlay-Daten enthält und diese sogar noch detaillierter darstellt.

Der Streaming-Prozess beeinflusst CPU, RAM (bis zu 64 GB) und Festplattenleistung. Während SSDs Engpässe minimieren, können bei langsamen Verbindungen oder unzureichender Hardware Frame-Drops auftreten.

## Installation und Konfiguration

### Systemanforderungen

Das System erfordert X-Plane 11.50+ oder X-Plane 12, läuft unter Windows, Linux (mit FUSE) oder macOS (experimentell). Abhängigkeiten umfassen WinFSP/Dokan (Windows), FUSE (Linux) und optional Python 3.x für Quellcode. Hardwareanforderungen umfassen 16 GB RAM, SSD-Speicher und eine schnelle Internetverbindung (≥100 Mbps).

### Installationsprozess

AutoOrtho wird von GitHub (kubilus1/autoortho) heruntergeladen, entweder als Binary oder Installer. Windows-Benutzer installieren WinFSP/Dokan und starten autoortho_win.exe, während Linux-Benutzer FUSE benötigen und macOS-Benutzer den experimentellen Anweisungen folgen sollten.

Die Benutzeroberfläche erfordert die Angabe des X-Plane-Hauptverzeichnisses und des Custom Scenery-Verzeichnisses. Regionale Overlays (wenige GB) werden über den "Scenery"-Tab installiert. Die scenery_packs.ini wird mit folgender Struktur konfiguriert:

```
SCENERY_PACK Custom Scenery/yAutoOrtho_Overlays/
SCENERY_PACK Custom Scenery/z_ao_eur/
SCENERY_PACK Custom Scenery/z_autoortho/
```

Der z_autoortho-Eintrag wird am Ende platziert, um anderen Szenerien Priorität zu geben. Die aktuelle Version stellt Platzhalterverzeichnisse wieder her, um eine stabile Reihenfolge zu gewährleisten. AutoOrtho muss vor X-Plane gestartet werden, um das virtuelle Dateisystem zu mounten, und die scenery_packs.ini sollte schreibgeschützt sein.

Für optimale Erfahrung fügt SimHeaven X-World 3D-Objekte und Autogen hinzu, während xOrganizer/xToolbox die Szenerie-Verwaltung vereinfacht. vStates bietet eine Alternative für vorgefertigte Orthophotos.

### Vergleich mit Ortho4XP

AutoOrtho und Ortho4XP erfüllen unterschiedliche Zwecke im X-Plane-Ökosystem. AutoOrtho streamt Daten in Echtzeit von Bing/USGS, benötigt minimalen Speicher (wenige GB Cache) aber eine konstante Internetverbindung. Es arbeitet mit ZL16, was einen guten Kompromiss zwischen Detail und Leistung bietet. Im Gegensatz dazu verwendet Ortho4XP vorbereitete lokale Kacheln von Bing/Google, benötigt hunderte GB Speicher, unterstützt aber bis zu ZL19 für maximale Details.

AutoOrthos Leistung kann gelegentliches Ruckeln zeigen und stellt höhere Anforderungen an CPU/RAM, während Ortho4XP stabilere Leistung mit lokal gespeicherten Daten bietet. Die Einrichtung ist mit AutoOrtho nach der initialen Konfiguration einfacher, während Ortho4XP zeitaufwändige Kachelerstellung erfordert, aber detailliertere Szenerien für bestimmte Regionen bietet.

### Häufige Probleme und Lösungen

Benutzer können mehrere häufige Probleme bei der Verwendung von AutoOrtho erleben:

1. **Startfehler**:
    - Ursache: Falsche WinFSP/Dokan-Installation oder fehlerhafte scenery_packs.ini-Konfiguration
    - Lösung: Nochmalige Installation/Konfiguration WinFSP/Dokan. Korrigieren der scenery_packs.ini.

2. **FUSE-Probleme** (Linux):
    - Log-Eintrag: `FUSE error: Failed to mount filesystem`
    - Ursache: Fehlende fuse3-Installation oder Berechtigungsprobleme
    - Lösung: fuse3 installieren und Berechtigungen prüfen (Linux: ls -l /dev/fuse)

3. **Python-Modul-Probleme**:
    - Log-Eintrag: `ModuleNotFoundError: No module named 'pyfuse3'`
    - Ursache: Fehlende Abhängigkeiten
    - Lösung: Fehlende Abhängigkeiten in der virtuellen Umgebung installieren

4. **Ruckeln und Frame-Drops**:
    - Ursache: Langsame Verbindungen oder unzureichende Hardware
    - Lösung: Verwendung einer SSD und reduzierten Grafikeinstellungen

5. **Unebene Flughäfen**:
    - Ursache: Fehlende automatische Flughafen-Glättung
    - Lösung: Verwendung von SimHeaven und Priorisierung von Flughafen-Szenerien

6. **Netzwerkprobleme**:
    - Log-Eintrag: `HTTP 429: Too Many Requests`
    - Ursache: Bing-Blacklisting
    - Lösung: VPN verwenden oder zu USGS-Quellen wechseln

7. **Szenerie-Konflikte**:
    - Log-Eintrag: `Warning: z_autoortho not found in scenery_packs.ini`
    - Ursache: Falsche Szenerie-Reihenfolge
    - Lösung: Reihenfolge in scenery_packs.ini korrigieren

8. **Speicherprobleme**:
    - Log-Eintrag: `MemoryError: Out of memory`
    - Ursache: Hohe RAM-Auslastung
    - Lösung: Cache-Größe reduzieren, X-Plane-Grafikeinstellungen senken

9. **Abstürze**:
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

Für detailliertere Log-Informationen kann in der `.autoortho` Konfigurationsdatei der Debug-Modus aktiviert werden:

```ini
# Debug-Modus
debug = true
```


## Linux-spezifische Installation

### Installationsbeispiel: AutoOrtho auf Debian 12 mit pyenv

Dieser Abschnitt bietet eine detaillierte Anleitung zur Installation von AutoOrtho mit der Python-Version auf einem Debian 12-System. Das Beispiel zeigt, wie eine isolierte Python-Umgebung mit pyenv eingerichtet wird und enthält umfassende Fehlerbehebung mit der autoortho.log-Datei.

### Systemanforderungen

Das Beispielsystem läuft mit Debian 12 (Bookworm) und X-Plane 12, verfügt über eine SSD, 32 GB RAM und eine stabile Internetverbindung mit 200 Mbps. Erforderliche Abhängigkeiten umfassen:

- fuse3 für das virtuelle Dateisystem
- git, build-essential, libssl-dev, zlib1g-dev für pyenv und Python
- Python 3.8+ (verwaltet über pyenv)
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

    Python 3.10.13 installieren:
    ```bash
    pyenv install 3.10.13
    pyenv global 3.10.13
    ```

3. **AutoOrtho-Installation**:
    Repository klonen und virtuelle Umgebung einrichten:

    ```bash
    git clone https://github.com/kubilus1/autoortho.git ~/autoortho
    cd ~/autoortho
    git checkout v0.7.2

    pyenv virtualenv 3.10.13 autoortho
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