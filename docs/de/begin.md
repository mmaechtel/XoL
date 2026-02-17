---
description: "Einstieg in X-Plane 12 unter Linux — Systemanforderungen, Standalone- und Steam-Installation, Bibliotheksabhängigkeiten und erster Start."
---
# Erste Schritte mit X-Plane unter Linux

Diese Anleitung behandelt Systemvoraussetzungen, X-Plane-Installation und Ersteinrichtung. Hintergründe zu den Vorteilen von Linux für X-Plane finden sich in der [Einführung](intro.md).

## Systemvoraussetzungen

X-Plane 12 benötigt erhebliche Systemressourcen, besonders für realistische Simulationen in hohen Auflösungen. Ideal ist eine schnelle CPU mit guter Single-Core- *und* Multi-Core-Leistung.

### Empfohlene Anforderungen

- **CPU**: Aktuelle Generation mit hoher Single-Core- und Multi-Core-Leistung (Intel Core i7/i9 oder AMD Ryzen 7/9)
- **RAM**: 32 GB oder mehr
- **Grafikkarte**: Hochleistungs-GPU mit mindestens 8 GB [VRAM](glossary.md#vram-video-ram) (z.B. NVIDIA RTX 3080/4080 oder höher)
- **Speicherplatz**: 250 GB oder mehr SSD-Speicher ([NVMe](glossary.md#nvme-non-volatile-memory-express) empfohlen)
- **Netzwerk**: Schnelle Internetverbindung für Ortho-Streaming und Kartenaktualisierungen

??? info "Warum diese Spezifikationen?"

    - **CPU**: X-Plane profitiert von hoher Single-Core-Geschwindigkeit und verteilt Rendering-Arbeit auf mehrere Kerne. Diese Empfehlungen zielen auf Addon-lastige Setups mit [Orthofotos](glossary.md#orthofotos) — Laminar Researchs offizielles Minimum liegt niedriger (z.B. Intel i5-12600K).
    - **RAM**: Speicherhungrige Addons, detaillierte Szenerien und Orthofotos können den RAM-Verbrauch drastisch erhöhen.
    - **GPU**: Insbesondere für 4K-Auflösung oder Multi-Monitor-Setups werden viel Grafikleistung und VRAM benötigt. Hochauflösende Texturen und komplexe Beleuchtungseffekte fordern selbst High-End-GPUs.
    - **Speicherplatz**: Die Basisinstallation benötigt ca. 25 GB, eine Vollinstallation mit allen Szenerien-Regionen ca. 75–80 GB. Orthofotos können schnell Hunderte von GB hinzufügen. SSD-Geschwindigkeit reduziert Nachladezeiten während des Flugs.
    - **Netzwerk**: Echtzeitdaten wie Wetter und Luftverkehr sowie Streaming-Orthofotos benötigen eine zuverlässige Verbindung.

### Hardware-Optimierungen

- SSD/NVMe-Laufwerk für Betriebssystem und X-Plane-Installation
- Dedizierte Grafikkarte mit aktuellen Treibern
- Mehrere Monitore für erweitertes Cockpit-Setup
- Gutes Kühlsystem, da X-Plane CPU und GPU stark belastet

??? tip "Debian-Linux-Installation"

    Diese Dokumentation setzt eine bestehende Debian-Installation in der aktuellen Stable-Version mit funktionierender grafischer Benutzeroberfläche voraus. Falls Debian noch installiert werden muss:

    **Offizielle Installationsquellen**

    - [Debian-Hauptserver](https://www.debian.org/) — Immer die aktuelle Stable-Version
    - [Weltweite Debian-Spiegelserver](https://www.debian.org/mirror/list) — Nahegelegenen Server für schnellere Downloads wählen
    - [Debian-Netzwerkinstallation](https://www.debian.org/distrib/netinst) — Minimale ISO für Netzwerkinstallation (empfohlen)

    **Wahl der richtigen Version**

    - Stets die aktuelle **Stable**-Version von Debian verwenden — maximale Stabilität
    - Die Stable-Version wird auf der [Debian-Hauptseite](https://www.debian.org/) prominent angezeigt
    - Für X-Plane-Performance immer die 64-Bit-Version (amd64) wählen

    **Tipps für die Installation**

    - Jede gängige Desktop-Umgebung funktioniert mit X-Plane. "GNOME" oder "KDE Plasma" werden für Einsteiger empfohlen — große Community-Unterstützung und ausgereifte [Wayland](glossary.md#wayland)-Integration
    - Bei der Partitionierung den Swap-Speicher konfigurieren: ca. 4 GB genügen ohne Hibernation, oder in Höhe des vorhandenen RAMs bei geplanter Hibernation-Nutzung
    - Separate Partitionen für `/` (root, mindestens 30 GB) und `/home` (restlicher Speicher) einrichten
    - Den [GRUB](glossary.md#grub-grand-unified-bootloader)-Bootloader auf dem Hauptlaufwerk installieren

    **Nach der Installation**

    1. System vollständig aktualisieren:
        ```bash
        sudo apt update && sudo apt upgrade -y
        ```

    2. Wichtige Basis-Pakete installieren:
        ```bash
        sudo apt install build-essential dkms git curl wget nano
        ```

## X-Plane 12 unter Linux installieren

X-Plane 12 ist sowohl über Steam als auch direkt vom Entwickler Laminar Research erhältlich.

### Steam

Diese Dokumentation fokussiert auf die Standalone-Installation. Alle beschriebenen Optimierungen lassen sich 1:1 mit einer Steam-Installation nachvollziehen — lediglich die Pfade müssen entsprechend der Steam-Verzeichnisstruktur angepasst werden (typischerweise `~/.steam/steam/steamapps/common/X-Plane 12/`).

### Standalone-Version (Laminar Research)

Die Standalone-Version bietet:

- Volle Kontrolle über Installationsverzeichnis und -optionen
- Direktes Update über den X-Plane-Updater ohne Drittanbieter
- Einfache Backups und Migration auf andere Rechner
- Uneingeschränkter Zugriff auf die Dateien für Modifikationen

**Installationsschritte:**

1. **X-Plane herunterladen**
    - Die [offizielle X-Plane-Website](https://www.x-plane.com/) aufrufen
    - X-Plane 12 erwerben (oder die Demo-Version herunterladen)
    - Den Linux-Installer herunterladen (`X-Plane12InstallerLinux.zip`, ca. 25 MB)

2. **Installer vorbereiten**
    - In den Download-Ordner wechseln und die Datei entpacken:
        ```bash
        cd ~/Downloads
        unzip X-Plane12InstallerLinux.zip
        ```
    - Den Installer ausführbar machen (falls nötig):
        ```bash
        chmod +x "X-Plane 12 Installer Linux"
        ```

3. **Installation starten**
    - Den Installer ausführen:
        ```bash
        ./"X-Plane 12 Installer Linux"
        ```
    - Im grafischen Installer auswählen:
        - Installationsverzeichnis (empfohlen: `/home/[username]/X-Plane 12/`)
        - Zu ladende Szeneriepakete
        - Weltabdeckung (mindestens das Hauptfluggebiet auswählen)

4. **Download-Prozess**
    - Der Installer lädt die ausgewählten Inhalte herunter (25–80 GB je nach Szenerien-Auswahl)
    - Dieser Vorgang kann mehrere Stunden dauern
    - Der Download kann jederzeit unterbrochen und später fortgesetzt werden

### Nach der Installation

1. **Erstes Starten**: X-Plane einmal starten und wieder schließen, damit Konfigurationsdateien erstellt werden

2. **Leistungseinstellungen optimieren**: Grafikeinstellungen entsprechend der vorhandenen Hardware anpassen. Siehe [X-Plane-Konfiguration](xplane/setup_diagnose/config.md) für Linux-spezifische Hinweise.

3. **Performance prüfen** mit der eingebauten [FPS](glossary.md#fps-frames-per-second)-Anzeige (Aktivierung mit `Shift+Strg+F`)

??? note "Fehlerbehebung: Bibliotheksabhängigkeiten (ldd)"

    Falls X-Plane nicht startet oder unerwartet abstürzt, kann das an fehlenden Bibliotheken liegen. Abhängigkeiten mit [ldd](glossary.md#ldd) prüfen:

    ```bash
    cd ~/X-Plane\ 12/
    ldd X-Plane-x86_64
    ```

    Nach Zeilen mit `not found` suchen:

    ```
    libvulkan.so.1 => not found
    ```

    **Häufige fehlende Abhängigkeiten**

    | Bibliothek | Paket | Installationsbefehl |
    |------------|-------|---------------------|
    | libvulkan.so.1 | libvulkan1 | `sudo apt install libvulkan1` |
    | libGL.so.1 | libgl1 | `sudo apt install libgl1` |
    | libX11.so.6 | libx11-6 | `sudo apt install libx11-6` |
    | libasound.so.2 | libasound2 | `sudo apt install libasound2` |
    | libpulse.so.0 | libpulse0 | `sudo apt install libpulse0` |

    Für vollständigen Vulkan-Support (erforderlich):

    ```bash
    sudo apt install libvulkan1 mesa-vulkan-drivers vulkan-tools
    ```

    Für Audio-Support:

    ```bash
    sudo apt install libasound2 libasound2-plugins libpulse0
    ```

    Nach der Installation fehlender Bibliotheken X-Plane erneut starten.

### Fehlerbehebung

Falls Probleme auftreten:

- **X-Plane startet nicht**: Logfile in `~/X-Plane 12/Log.txt` prüfen
- **Schlechte Performance**: Grafiktreiber aktualisieren und Grafikeinstellungen reduzieren
- **Abstürze**: Sicherstellen, dass alle X-Plane-Dateien korrekt heruntergeladen wurden
- **Eingabegeräte werden nicht erkannt**: `jstest-gtk` zur Diagnose und Kalibrierung installieren

Für technische Begriffe steht das [Glossar](glossary.md) zur Verfügung.

## Nächste Schritte

Nach einer erfolgreichen Installation geht es weiter mit:

1. [Performance](fundamentals/performance/performance_overview.md) — Die drei Lastdimensionen verstehen (CPU, I/O, Netzwerk)
2. [NVIDIA-Treiber](linux/optimizations/nvidia.md) — Proprietäre NVIDIA-Treiber installieren und konfigurieren
3. [Liquorix-Kernel](linux/optimizations/liquorix.md) — Low-Latency-Kernel optimiert für Desktop-Workloads
4. [System-Tuning](linux/system/systemtuning.md) — CPU-Governor, Interrupt-Shielding und Kernel-Parameter
5. [Display-Server](linux/optimizations/displayserver.md) — Wayland vs. X11 für X-Plane
6. [X-Plane-Konfiguration](xplane/setup_diagnose/config.md) — Linux-spezifische Grafik- und Performance-Einstellungen
