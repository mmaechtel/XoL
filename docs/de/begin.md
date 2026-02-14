# Erste Schritte mit X-Plane unter Linux

Diese Anleitung beschreibt die ersten Schritte, um X-Plane unter Linux optimal einzurichten. Sie richtet sich an Linux-erfahrene Benutzer und baut auf einer bestehenden Linux-Installation auf.

## Systemvoraussetzungen

X-Plane 12 ist ein anspruchsvoller Flugsimulator, der erhebliche Systemressourcen benötigt, besonders für realistische Simulationen in hohen Auflösungen. Single-Core-Performance bleibt zwar wichtig, aber X-Plane 12 verteilt einen erheblichen Teil der Frame-Arbeit auf mehrere Kerne. Ideal ist eine schnelle CPU mit guter Single-Core- *und* Multi-Core-Leistung.

### Empfohlene Anforderungen

- **CPU**: Aktuelle Generation mit hoher Single-Core- und Multi-Core-Leistung (Intel Core i7/i9 oder AMD Ryzen 7/9)
    - *Warum?* X-Plane profitiert von hoher Single-Core-Geschwindigkeit und verteilt Rendering-Arbeit auf mehrere Kerne. Diese Empfehlungen zielen auf Addon-lastige Setups mit [Orthofotos](../glossary.md#orthofotos) — Laminar Researchs offizielles Minimum liegt niedriger (z.B. Intel i5-12600K).

- **RAM**: 32 GB oder mehr
    - *Warum?* Speicherhungrige Addons, detaillierte Szenerien und Orthofotos können den RAM-Verbrauch drastisch erhöhen.

- **Grafikkarte**: Hochleistungs-GPU mit mindestens 8 GB [VRAM](../glossary.md#vram-video-ram) (z.B. NVIDIA RTX 3080/4080 oder höher)
    - *Warum?* Insbesondere für 4K-Auflösung oder Multi-Monitor-Setups wird viel Grafikleistung und VRAM benötigt. Hochauflösende Texturen und komplexe Beleuchtungseffekte fordern selbst High-End-GPUs.

- **Speicherplatz**: 250 GB oder mehr SSD-Speicher ([NVMe](../glossary.md#nvme-non-volatile-memory-express) empfohlen)
    - *Warum?* Die Basisinstallation benötigt ca. 25 GB, eine Vollinstallation mit allen Szenerien-Regionen ca. 75–80 GB. Orthofotos können schnell Hunderte von GB hinzufügen. SSD-Geschwindigkeit reduziert Nachladezeiten während des Flugs.

- **Netzwerk**: Schnelle Internetverbindung für Ortho-Streaming und Kartenaktualisierungen
    - *Warum?* Echtzeitdaten wie Wetter und Luftverkehr sowie Streaming-Orthofotos benötigen eine zuverlässige Verbindung.

### Hardware-Optimierungen

- SSD/NVMe-Laufwerk für Betriebssystem und X-Plane-Installation
- Dedizierte Grafikkarte mit aktuellen Treibern
- Mehrere Monitore für erweitertes Cockpit-Setup
- Gutes Kühlsystem, da X-Plane CPU und GPU stark belastet

*Hinweis: Selbst mit High-End-Hardware kann X-Plane anspruchsvoll sein. Die empfohlenen Optimierungen in dieser Dokumentation helfen, das Beste aus dem vorhandenen System herauszuholen.*

## Debian Linux installieren

Diese Dokumentation setzt eine bestehende Debian-Installation in der aktuellen Stable-Version mit funktionierender grafischer Benutzeroberfläche voraus. Falls Debian noch installiert werden muss, finden sich hier die wichtigsten Ressourcen:

### Offizielle Installationsquellen

- [Debian-Hauptserver](https://www.debian.org/) — Hier findet sich immer die aktuelle Stable-Version
- [Weltweite Debian-Spiegelserver](https://www.debian.org/mirror/list) — Nahegelegenen Server für schnellere Downloads wählen
- [Debian-Netzwerkinstallation](https://www.debian.org/distrib/netinst) — Minimale ISO für Netzwerkinstallation (empfohlen)

### Wahl der richtigen Version

- Stets die aktuelle **Stable**-Version von Debian verwenden — maximale Stabilität
- Die Stable-Version wird auf der [Debian-Hauptseite](https://www.debian.org/) prominent angezeigt
- Für X-Plane-Performance immer die 64-Bit-Version (amd64) wählen

### Tipps für die Installation

- Jede gängige Desktop-Umgebung funktioniert mit X-Plane. "GNOME" oder "KDE Plasma" werden für Einsteiger empfohlen — große Community-Unterstützung und ausgereifte [Wayland](../glossary.md#wayland)-Integration
- Bei der Partitionierung den Swap-Speicher konfigurieren: ca. 4 GB genügen ohne Hibernation, oder in Höhe des vorhandenen RAMs bei geplanter Hibernation-Nutzung
- Separate Partitionen für `/` (root, mindestens 30 GB) und `/home` (restlicher Speicher) einrichten
- Den [GRUB](../glossary.md#grub-grand-unified-bootloader)-Bootloader auf dem Hauptlaufwerk installieren

### Nach der Installation

Nach erfolgreicher Installation und Anmeldung in der grafischen Benutzeroberfläche sind folgende Schritte empfehlenswert:

1. System vollständig aktualisieren:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. Wichtige Basis-Pakete installieren:
   ```bash
   sudo apt install build-essential dkms git curl wget nano
   ```

Die folgenden Kapitel dieser Dokumentation setzen eine funktionierende Debian-Installation voraus und konzentrieren sich auf die Optimierung für X-Plane.

## X-Plane 12 unter Linux installieren

X-Plane 12 ist sowohl über Steam als auch direkt vom Entwickler Laminar Research erhältlich. Obwohl die Steam-Version für Einsteiger bequem sein kann, konzentriert sich diese Dokumentation auf die Standalone-Version, die mehr Kontrolle und Flexibilität bietet.

### Installationsmethoden

#### Standalone-Version (direkter Download von Laminar Research)

Die direkte Installation von X-Plane bietet zahlreiche Vorteile für erfahrene Nutzer:

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
    - Im grafischen Installer lassen sich auswählen:
        - Installationsverzeichnis (empfohlen: `/home/[username]/X-Plane 12/`)
        - Zu ladende Szeneriepakete
        - Weltabdeckung (mindestens das Hauptfluggebiet auswählen)

4. **Download-Prozess**
    - Der Installer lädt die ausgewählten Inhalte herunter (25–80 GB je nach Szenerien-Auswahl)
    - Dieser Vorgang kann mehrere Stunden dauern
    - Der Download kann jederzeit unterbrochen und später fortgesetzt werden

**Vorteile der Standalone-Version**

- Volle Kontrolle über Installationsverzeichnis und -optionen
- Direktes Update über den X-Plane-Updater ohne Drittanbieter
- Oft schnellere Updates bei neuen Versionen
- Einfache Backups und Migration auf andere Rechner
- Uneingeschränkter Zugriff auf die Dateien für Modifikationen

### Nach der Installation

Nach erfolgreicher Installation sind folgende Schritte empfehlenswert:

1. **Erstes Starten**: X-Plane einmal starten und wieder schließen, damit Konfigurationsdateien erstellt werden

2. **Leistungseinstellungen optimieren**: Grafikeinstellungen entsprechend der vorhandenen Hardware anpassen. Siehe die Seite [X-Plane-Konfiguration](xplane/config.md) für detaillierte Linux-spezifische Hinweise.

3. **Performance prüfen** mit der eingebauten [FPS](../glossary.md#fps-frames-per-second)-Anzeige (Aktivierung mit `Shift+Strg+F`)

### Überprüfung der Bibliotheksabhängigkeiten

Wenn X-Plane nicht startet oder unerwartet abstürzt, kann das an fehlenden Bibliotheken liegen. Linux bietet mit dem [ldd](../glossary.md#ldd)-Tool eine einfache Möglichkeit, Abhängigkeiten zu überprüfen:

#### Abhängigkeiten mit ldd überprüfen

1. **Terminal öffnen** und zum X-Plane-Verzeichnis navigieren:
   ```bash
   cd ~/X-Plane\ 12/
   ```

2. **[ldd](../glossary.md#ldd) auf die X-Plane-Executable anwenden**:
   ```bash
   ldd X-Plane-x86_64
   ```

3. **Die Ausgabe analysieren**:
    - Normale Abhängigkeiten erscheinen im Format: `libname.so => /pfad/zu/libname.so`
    - Problematische Abhängigkeiten zeigen `not found` oder fehlen komplett:
     ```
     libvulkan.so.1 => not found
     ```

#### Interpretation der ldd-Ausgabe

Die [ldd](../glossary.md#ldd)-Ausgabe zeigt alle [dynamischen Bibliotheken](../glossary.md#dynamische-bibliotheken), die X-Plane benötigt:

```
linux-vdso.so.1 (0x00007ffcb9192000)
libdl.so.2 => /lib/x86_64-linux-gnu/libdl.so.2 (0x00007f040d8e5000)
libpthread.so.0 => /lib/x86_64-linux-gnu/libpthread.so.0 (0x00007f040d8c6000)
libGL.so.1 => /usr/lib/x86_64-linux-gnu/libGL.so.1 (0x00007f040d83a000)
libvulkan.so.1 => not found
...
```

- **Gefundene Bibliotheken**: Mit vollständigem Pfad aufgelistet
- **Fehlende Bibliotheken**: Mit `not found` markiert
- **Abhängigkeiten der Abhängigkeiten**: Werden ebenfalls angezeigt

#### Behebung fehlender Abhängigkeiten

1. **Beispiel: Fehlende [Vulkan API](../glossary.md#vulkan-api)-Bibliothek**:
   ```bash
   sudo apt install libvulkan1 mesa-vulkan-drivers vulkan-tools
   ```

2. **Beispiel: Fehlende Audio-Bibliotheken**:
   ```bash
   sudo apt install libasound2 libasound2-plugins libpulse0
   ```

3. **Beispiel: Fehlende OpenGL-Bibliotheken**:
   ```bash
   sudo apt install libgl1 libgl1-mesa-dri
   ```

4. **Beispiel: [32-Bit-Kompatibilität](../glossary.md#32-bit-kompatibilität) (selten nötig — nur für bestimmte Drittanbieter-Plugins oder Wine-basierte Tools)**:
   ```bash
   sudo dpkg --add-architecture i386
   sudo apt update
   sudo apt install libgl1:i386 libvulkan1:i386
   ```

#### Häufige fehlende Abhängigkeiten

| Bibliothek | Paket | Installationsbefehl |
|------------|-------|---------------------|
| libvulkan.so.1 | libvulkan1 | `sudo apt install libvulkan1` |
| libGL.so.1 | libgl1 | `sudo apt install libgl1` |
| libX11.so.6 | libx11-6 | `sudo apt install libx11-6` |
| libasound.so.2 | libasound2 | `sudo apt install libasound2` |
| libpulse.so.0 | libpulse0 | `sudo apt install libpulse0` |

Nach der Installation fehlender Bibliotheken X-Plane erneut starten. In den meisten Fällen werden dadurch Startprobleme behoben, die durch fehlende Abhängigkeiten verursacht wurden.

### Fehlerbehebung

Falls Probleme auftreten:

- **X-Plane startet nicht**: Logfile in `~/X-Plane 12/Log.txt` prüfen
- **Schlechte Performance**: Grafiktreiber aktualisieren und Grafikeinstellungen reduzieren
- **Abstürze**: Sicherstellen, dass alle X-Plane-Dateien korrekt heruntergeladen wurden
- **Eingabegeräte werden nicht erkannt**: `jstest-gtk` zur Diagnose und Kalibrierung installieren
- **Allgemeine Probleme**: GPU-Treiber-Kompatibilität prüfen, sicherstellen, dass alle Linux-Pakete aktuell sind, und X-Plane-Systemanforderungen auf der [offiziellen Website](https://www.x-plane.com/) überprüfen

Je nach verwendeter Hardware und Linux-Distribution können spezifische Anpassungen erforderlich sein. Die hier gezeigten Beispiele wurden mit Debian getestet, funktionieren aber mit geringfügigen Änderungen auch auf anderen Distributionen. Für technische Begriffe steht das [Glossar](glossary.md) zur Verfügung.

## Nächste Schritte

Nach einer erfolgreichen Installation geht es mit folgenden Themen weiter:

- [NVIDIA-Treiber](nvidia.md) — Proprietäre NVIDIA-Treiber installieren und konfigurieren
- [Liquorix-Kernel](liquorix.md) — Low-Latency-Kernel optimiert für Desktop-Workloads
- [System-Tuning](systemtuning.md) — CPU-Governor, Interrupt-Shielding und Kernel-Parameter
- [Display-Server](displayserver.md) — Wayland vs. X11 für X-Plane
- [X-Plane-Konfiguration](xplane/config.md) — Linux-spezifische Grafik- und Performance-Einstellungen
