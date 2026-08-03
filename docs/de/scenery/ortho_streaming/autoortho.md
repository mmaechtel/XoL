---
description: "AutoOrtho streamt Satellitenbilder in Echtzeit per FUSE in X-Plane. Einrichtung unter Linux mit Konfiguration, Fehlerbehebung und Ortho4XP-Vergleich."
---
# AutoOrtho

Die visuelle Qualität der Landschaftsdarstellung ist ein entscheidender Faktor für **Sichtflüge (VFR)** in Flugsimulatoren. Während X-Plane mit Standardtexturen arbeitet, werden diese häufig als veraltet empfunden. **AutoOrtho** behebt diese Einschränkung durch die **Echtzeit-Integration** von Satellitenbildern und ermöglicht eine präzise Darstellung von Infrastruktur, Vegetation und weiteren Geländemerkmalen. Die letzte Veröffentlichung von kubilus1 (Januar 2024) optimierte die Integration mit X-Plane und minimierte typische Probleme wie **Szenerie-Konflikte** oder **Leistungseinbußen**.

Inzwischen existiert ein aktiver Fork unter [https://github.com/ProgrammingDinosaur/autoortho4xplane](https://github.com/ProgrammingDinosaur/autoortho4xplane), in dem AutoOrtho kontinuierlich weiterentwickelt wird.

## Funktionsweise

AutoOrtho implementiert ein [FUSE-basiertes Streaming-System](how_streaming_works.md) für [Orthophotos](../../glossary.md#orthofotos) basierend auf der Flugzeugposition. Kacheln für aktuelle und angrenzende Bereiche werden von Anbietern wie Bing mit Zoomstufen bis [ZL18](../../glossary.md#zl-zoom-level) vorgeladen. Die allgemeine Streaming-Architektur — X-Planes DSF → .ter → DDS-Texturkette, FUSE-Interception, Cache-System — beschreibt [Wie Ortho-Streaming funktioniert](how_streaming_works.md).

AutoOrtho liefert 2D-Orthophotos ohne 3D-Objekte. Für die Darstellung von Gebäuden und Vegetation wird [SimHeaven (X-World)](../../glossary.md#simheaven-x-world) empfohlen, das OpenStreetMap-Daten implementiert. [Overlays](../../glossary.md#overlay-szenerie) adaptieren die Bilder an das X-Plane-Terrain-[Mesh](../../glossary.md#mesh) und enthalten essentielle Informationen wie Flughafen-Glättungen, Verkehrsinfrastruktur und Eisenbahnlinien. Bei Verwendung von SimHeaven X-World sind die yOrtho-Overlays redundant.

Der Streaming-Prozess beeinflusst CPU-Auslastung, RAM-Verbrauch und Festplattenleistung. Der RAM-Bedarf hängt von der Konfiguration ab (Zoomstufe, Buffer-Pool, Pre-Fetch-Einstellungen). Während SSDs Engpässe minimieren, können bei suboptimalen Verbindungen oder unzureichender Hardware Frame-Drops auftreten.

### Der ProgrammingDinosaur Fork

Der [ProgrammingDinosaur Fork](https://github.com/ProgrammingDinosaur/autoortho4xplane) ist die aktiv gepflegte Weiterentwicklung von AutoOrtho. Er hat sich zu einem eigenständigen Projekt mit signifikanten Verbesserungen gegenüber dem Original entwickelt:

- **C-Pipeline für Texturverarbeitung**: Native C-Implementierung für JPEG-Dekodierung und DDS-Generierung mit dediziertem Decode-Pool und verbessertem Speichermanagement. Vier Pipeline-Modi: Auto, Native (reines C), Hybrid (C + Python) und Python (Fallback)
- **~2x schnellere Ladezeiten**: Optimierte Download- und JPEG-Verarbeitung, bessere Auslastung von CPU- und Netzwerk-Ressourcen, reduzierte Leerlaufphasen bei der Tile-Generierung
- **Vereinheitlichte Single-Process-Architektur** über Windows, Linux und macOS für höhere Stabilität und besseres Subprozess-Handling
- **VRAM-Optimierung** durch dynamische DDS-Dimensionierung
- **.aob2 Bundle-Format**: Kompaktes Datenformat für Szenerie-Pakete
- **Seasons-Unterstützung**: Saisonale Texturvariationen
- **Erhöhte Zoomstufen und Auflösung** für X-Plane 12
- **Schlanke Karten-UI**: Die integrierte Karte wird über einen lokalen Endpunkt bereitgestellt statt über einen gebündelten Chromium-Browser — kleinere Installation und höhere Stabilität
- **Überarbeiteter Installer** mit Sicherheitsprüfungen für Zielverzeichnisse
- **macOS-Kompatibilität** (nur Apple Silicon)
- **Erweiterte Kartenanbieter**: Bing, Google, Here, Yandex und Apple Maps
- **Automatische [scenery_packs.ini](../../glossary.md#scenery_packsini)-Konfiguration** für die Verwendung mit SimHeaven
- **SimBrief-Integration**: Importiert den Flugplan und lädt Kacheln entlang der geplanten Route vor. Konfigurierbarer Radius und Abweichungsschwelle — weicht das Flugzeug zu weit von der SimBrief-Route ab, fällt das Prefetching auf positionsbasierte Berechnung zurück
- **Cache- und FUSE-Robustheit**: Korrektur des Küstenlinien-Blendings, Vermeidung partieller Caches und degradierter Zoomstufen

---

## Installation und Konfiguration

### Systemanforderungen

Das System erfordert X-Plane 11.50+ oder X-Plane 12, läuft unter Windows, Linux (mit FUSE) oder macOS (Apple Silicon). Abhängigkeiten umfassen WinFSP/Dokan (Windows), FUSE (Linux) und optional Python 3.x für Quellcode. Hardwareanforderungen umfassen 16 GB RAM, SSD-Speicher und eine schnelle, stabile Internetverbindung.

**Hinweis**: Der [ProgrammingDinosaur Fork](https://github.com/ProgrammingDinosaur/autoortho4xplane) bietet vollständige macOS-Kompatibilität für Apple Silicon-Prozessoren und erweiterte Funktionen für X-Plane 12.

### Installationsprozess

AutoOrtho wird von GitHub (kubilus1/autoortho) heruntergeladen, entweder als [Binary](../../glossary.md#binary) oder Installer. Der [ProgrammingDinosaur Fork](https://github.com/ProgrammingDinosaur/autoortho4xplane) bietet einen überarbeiteten Installer mit Sicherheitsprüfungen. Windows-Benutzer installieren `WinFSP`/`Dokan` und starten `autoortho_win.exe`, während Linux-Benutzer `FUSE` benötigen und macOS-Benutzer (Apple Silicon) den entsprechenden Anweisungen folgen sollten.

Die Benutzeroberfläche erfordert die Angabe des X-Plane-Hauptverzeichnisses und des `Custom Scenery`-Verzeichnisses. Regionale Overlays (wenige GB) werden über den "Scenery"-Tab installiert. Der [ProgrammingDinosaur Fork](https://github.com/ProgrammingDinosaur/autoortho4xplane) bietet eine automatische `scenery_packs.ini`-Konfiguration für die Verwendung mit SimHeaven. Die manuelle Konfiguration erfolgt mit folgender Struktur:

```
SCENERY_PACK Custom Scenery/yAutoOrtho_Overlays/
SCENERY_PACK Custom Scenery/z_ao_eur/
SCENERY_PACK Custom Scenery/z_autoortho/
```

Der `z_autoortho`-Eintrag wird am Ende platziert, um anderen Szenerien Priorität zu geben. Die aktuelle Version stellt Platzhalterverzeichnisse wieder her, um eine stabile Reihenfolge zu gewährleisten. AutoOrtho muss vor X-Plane gestartet werden, um das virtuelle Dateisystem zu mounten, und die `scenery_packs.ini` sollte schreibgeschützt sein bzw. von einem Tool wie xOrganizer verwaltet werden.

Das Verzeichnis `yAutoOrtho_Overlays` wird nur benötigt, sofern nicht SimHeaven benutzt wird.

### Konfiguration

Der [ProgrammingDinosaur Fork](https://github.com/ProgrammingDinosaur/autoortho4xplane) bietet eine moderne [GUI](../../glossary.md#gui-graphical-user-interface) für alle Konfigurationseinstellungen, die eine einfache Einrichtung ohne manuelle Dateibearbeitung ermöglicht. Die wichtigsten Einstellungen umfassen:

- **X-Plane-Pfad**: Verzeichnis des X-Plane-Installationsordners
- **Cache-Verzeichnis**: Speicherort für Orthofoto-Cache (empfohlen: schnelle SSD)
- **Kartenanbieter**: Auswahl zwischen Bing, Google, Here, Yandex und Apple Maps
- **Cache-Größe**: Maximale Cache-Größe in GB — wird das Limit erreicht, werden ältere Kacheln automatisch entfernt
- **Wartezeit**: Balance zwischen Qualität und Reaktionszeit
- **Zoom-Level**: Mindest- und Maximalzoom für Satellitenbilder
- **Autostart**: Automatischer Start mit X-Plane
- **Debug-Modus**: Erweiterte Logging-Informationen

Für erweiterte Konfigurationen kann weiterhin die `.autoortho`-Konfigurationsdatei manuell bearbeitet werden, wenn gewünscht.

Für optimale Erfahrung fügt SimHeaven X-World 3D-Objekte und [Autogen](../../glossary.md#autogen) hinzu, während xOrganizer/xToolbox die Szenerie-Verwaltung vereinfacht.

Für einen Vergleich mit der Rust-basierten Linux-Alternative siehe [XEarthLayer](xearthlayer.md#vergleich-mit-autoortho).

---

## Vergleich mit Ortho4XP

AutoOrtho und [Ortho4XP](../../glossary.md#ortho4xp) verfolgen architektonisch unterschiedliche Ansätze, die jeweils für verschiedene Spielerprofile optimiert sind.

| Dimension | AutoOrtho | Ortho4XP |
|---|---|---|
| Datenbeschaffung | On-Demand-Streaming zur Laufzeit | Vorab generiert (offline) |
| Speicherbedarf | Cache mit automatischer Bereinigung (Limit konfigurierbar) | Dauerhaft pro Region (1–8 GB bei ZL17) |
| Internetbedarf | Ja (bei Cache-Miss) | Nein (nach Generierung) |
| Max. Zoomstufe | Bis ZL18 | Bis ZL19 |
| Spontanität | Sofort fliegbar, weltweit | Vorab-Generierung erforderlich (30 Min. bis Stunden) |
| Visuelle Konsistenz | Progressives Laden bei Erstbesuch | Sofort volle Qualität |
| Offline-Fähigkeit | Nur gecachte Regionen | Vollständig |

**Welches System passt besser?**

- **Habitueller Spieler** (wiederkehrende Stammflughäfen): Ortho4XP bietet hier strukturelle Vorteile — nach einmaliger Generierung liegt der gesamte Datenbestand lokal vor, die Cache-Trefferquote beträgt 100 %, und es bestehen keine Laufzeitabhängigkeiten von Netzwerk oder Kartenservern.

- **Explorativer Spieler** (ständig neue Destinationen): AutoOrtho ist die bessere Wahl — keine Vorab-Generierung, spontanes Anfliegen weltweit möglich. Ortho4XP würde hier zu einem stetig wachsenden Datenbestand führen, der kaum wiederverwendet wird.

- **Hybrider Spieler**: Die [Kombination beider Systeme](static_plus_streaming.md) bietet das Beste aus beiden Welten.

!!! info "Cache-Verhalten"
    AutoOrtho verfügt über eine automatische Cache-Bereinigung: Wird die konfigurierte Cache-Größe erreicht, werden ältere Kacheln automatisch entfernt, um Platz für neue zu schaffen. Im Gegensatz zu Ortho4XP, wo generierte Tiles dauerhaft auf der Festplatte verbleiben, reguliert AutoOrtho seinen Speicherverbrauch somit selbstständig.

### Häufige Probleme und Lösungen

Für grundlegende Installations- und Konfigurationsprobleme (Initialisierungsfehler, FUSE-Probleme, Python-Modul-Probleme, Performance-Probleme) wird auf die aktuelle Dokumentation des [ProgrammingDinosaur Forks](https://github.com/ProgrammingDinosaur/autoortho4xplane) verwiesen, da diese Probleme in der neueren Version behoben oder vereinfacht wurden.

Weitere spezifische Probleme bei der Verwendung von AutoOrtho:

1. **Flughafen-Topographie-Probleme**:
    - Ursache: Fehlende automatische Flughafen-Glättung bzw. fehlende Ortho Patches für die Flughafen-Szenerie
    - Lösung: Implementierung von Ortho Patches oder dem `flatten 1` Parameter in der `apt.dat` und Überprüfung der Priorisierung von Flughafen-Szenerien

2. **Netzwerkprobleme**:
    - Log-Eintrag: `HTTP 429: Too Many Requests`
    - Ursache: Bing-Blacklisting
    - Lösung: VPN verwenden oder zu einem anderen Kartenanbieter wechseln (z. B. Google oder Here)

3. **Szenerie-Konflikte**:
    - Log-Eintrag: `Warning: z_autoortho not found in scenery_packs.ini`
    - Ursache: Falsche Szenerie-Reihenfolge
    - Lösung: Reihenfolge in scenery_packs.ini korrigieren

4. **Speicherprobleme**:
    - Log-Eintrag: `MemoryError: Out of memory`
    - Ursache: Hohe RAM-Auslastung
    - Lösung: Cache-Größe reduzieren, X-Plane-Grafikeinstellungen senken

5. **Abstürze**:
    - Ursache: RAM-Überlastung oder Add-on-Konflikte
    - Lösung: Deaktivieren von Add-ons, Erhöhen des RAMs oder Reduzieren der Cache-Größe

### Log-Analyse

Die autoortho.log lässt sich mit verschiedenen Methoden analysieren:

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

---

## Linux-spezifische Installation

### Installationsbeispiel: AutoOrtho auf Debian 12 mit pyenv

Dieser Abschnitt bietet eine detaillierte Anleitung zur Installation von AutoOrtho mit der Python-Version auf einem Debian 12-System. Das Beispiel zeigt, wie eine isolierte Python-Umgebung mit [pyenv](../../glossary.md#pyenv) eingerichtet wird und enthält umfassende Fehlerbehebung mit der autoortho.log-Datei.

**Hinweis**: Der [ProgrammingDinosaur Fork](https://github.com/ProgrammingDinosaur/autoortho4xplane) bietet einen verbesserten Installer und erweiterte Kompatibilität — die Binary-Installation wird gegenüber dem hier gezeigten Python-Setup empfohlen.

### Beispielumgebung

Das Beispielsystem läuft mit Debian 12 (Bookworm) und X-Plane 12, verfügt über eine SSD, 32 GB RAM und eine stabile Internetverbindung mit 200 Mbps. Erforderliche Abhängigkeiten umfassen:

- fuse3 für das virtuelle Dateisystem
- git, build-essential, libssl-dev, zlib1g-dev für pyenv und Python
- Python 3.x (verwaltet über pyenv) — die Binary-Installation wird empfohlen und erfordert keine separate Python-Installation
- Einige GB SSD-Speicher für Overlays und Cache

### Schritt-für-Schritt Installation

1. **Systemvorbereitung**:
    Das System aktualisieren und grundlegende Abhängigkeiten installieren:

    ```bash
    sudo apt update && sudo apt upgrade -y
    sudo apt install -y fuse3 libfuse2 git curl build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev wget llvm libncurses5-dev libncursesw5-dev \
    xz-utils tk-dev libffi-dev liblzma-dev python3-openssl
    ```

2. **pyenv-Einrichtung**:
    Nach der Installation von pyenv die Umgebung konfigurieren:

    ```bash
    curl https://pyenv.run | bash
    ```

    Zu ~/.bashrc hinzufügen:
    ```bash
    export PATH="$HOME/.pyenv/bin:$PATH"
    eval "$(pyenv init --path)"
    eval "$(pyenv init -)"
    ```

    Eine kompatible Python-Version installieren:
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

---

## Weiterführende Kapitel

| Thema | Seite | Schwerpunkt |
|---|---|---|
| XPME | [XPME](xpme.md) | Closed-Source-Freemium-Alternative, hochauflösende Stufe kostenpflichtig |
| XEarthLayer | [XEarthLayer](xearthlayer.md) | Rust-basierte Streaming-Alternative mit adaptivem Prefetch |
| Ortho4XP | [Ortho4XP](../orthophotography/ortho4xp.md) | Statische Ortho-Kachel-Generierung für Offline-Nutzung |
| Statisch + Streaming | [Statisch + Streaming](static_plus_streaming.md) | Kombination lokaler Kacheln mit Streaming |
| Szenerie-Komponenten | [Wie X-Plane die Welt aufbaut](../aufbau_quellen/scenery_components.md) | scenery_packs.ini-Ladereihenfolge und Schicht-Interaktion |
| Dateisystem | [Dateisystem](../../linux/optimizations/filesystem.md) | I/O-Optimierung für Cache- und SSD-Performance |
| XOrganizer | [XOrganizer](../../addon/tools/xorganizer.md) | Szenerie-Verwaltung und scenery_packs.ini-Editor |

---

## Quellen

- [GitHub Repository (Original)](https://github.com/kubilus1/autoortho)
- [GitHub Repository (ProgrammingDinosaur Fork)](https://github.com/ProgrammingDinosaur/autoortho4xplane)
- [X-Plane.org Forum](https://forums.x-plane.org/forums/forum/802-autoortho-streaming-ortho-imagery-for-x-plane/)