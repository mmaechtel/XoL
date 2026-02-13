# Erste Schritte mit X-Plane unter Linux

Diese Anleitung führt Sie durch die ersten Schritte, um X-Plane unter Linux optimal einzurichten. Sie richtet sich an Linux-erfahrene Benutzer und baut auf einer bestehenden Linux-Installation auf.

## Systemvoraussetzungen

X-Plane 12 ist ein anspruchsvoller Flugsimulator, der erhebliche Systemressourcen benötigt, besonders für realistische Simulationen in hohen Auflösungen. Single-Core-Performance bleibt zwar wichtig, aber X-Plane 12 verteilt einen erheblichen Teil der Frame-Arbeit auf mehrere Kerne. Ideal ist eine schnelle CPU mit guter Single-Core- *und* Multi-Core-Leistung.

### Empfohlene Anforderungen

- **CPU**: Aktuelle Generation mit hoher Single-Core- und Multi-Core-Leistung (Intel Core i7/i9 oder AMD Ryzen 7/9)
    - *Warum?* X-Plane profitiert von hoher Single-Core-Geschwindigkeit und verteilt Rendering-Arbeit auf mehrere Kerne. Diese Empfehlungen zielen auf Addon-lastige Setups mit Orthofotos — Laminar Researchs offizielles Minimum liegt niedriger (z.B. Intel i5-12600K).

- **RAM**: 32 GB oder mehr
    - *Warum?* Speicherhungrige Addons, detaillierte Szenerien und Orthofotos können den RAM-Verbrauch drastisch erhöhen.

- **Grafikkarte**: Hochleistungs-GPU mit mindestens 8 GB VRAM (z.B. NVIDIA RTX 3080/4080 oder höher)
    - *Warum?* Insbesondere für 4K-Auflösung oder Multi-Monitor-Setups benötigen Sie viel Grafikleistung und VRAM. Hochauflösende Texturen und komplexe Beleuchtungseffekte fordern selbst High-End-GPUs.

- **Speicherplatz**: 250 GB oder mehr SSD-Speicher (NVMe empfohlen)
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

Diese Dokumentation geht davon aus, dass Sie Debian Linux in der aktuellen Stable-Version bereits installiert haben und mit einer funktionierenden grafischen Benutzeroberfläche arbeiten. Falls Sie Debian noch installieren müssen, finden Sie hier die wichtigsten Ressourcen:

### Offizielle Installationsquellen

- [Debian-Hauptserver](https://www.debian.org/) — Hier finden Sie immer die aktuelle Stable-Version
- [Weltweite Debian-Spiegelserver](https://www.debian.org/mirror/list) — Wählen Sie einen Server in Ihrer Nähe für schnellere Downloads
- [Debian-Netzwerkinstallation](https://www.debian.org/distrib/netinst) — Minimale ISO für Netzwerkinstallation (empfohlen)

### Wahl der richtigen Version

- Verwenden Sie stets die aktuelle **Stable**-Version von Debian für maximale Stabilität
- Die Stable-Version wird auf der [Debian-Hauptseite](https://www.debian.org/) prominent angezeigt
- Für X-Plane-Performance immer die 64-Bit-Version (amd64) wählen

### Tipps für die Installation

- Jede gängige Desktop-Umgebung funktioniert mit X-Plane. "GNOME" oder "KDE Plasma" werden für Einsteiger empfohlen — große Community-Unterstützung und ausgereifte Wayland-Integration
- Konfigurieren Sie bei der Partitionierung den Swap-Speicher: ca. 4 GB genügen ohne Hibernation, oder in Höhe Ihres RAMs, wenn Sie Hibernation nutzen möchten
- Richten Sie separate Partitionen für `/` (root, mindestens 30 GB) und `/home` (restlicher Speicher) ein
- Installieren Sie den GRUB-Bootloader auf dem Hauptlaufwerk

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

X-Plane 12 ist sowohl über Steam als auch direkt vom Entwickler Laminar Research erhältlich. Obwohl die Steam-Version für Einsteiger bequem sein kann, konzentrieren wir uns in dieser Dokumentation auf die Standalone-Version, die mehr Kontrolle und Flexibilität bietet.

### Installationsmethoden

#### Standalone-Version (direkter Download von Laminar Research)

Die direkte Installation von X-Plane bietet zahlreiche Vorteile für erfahrene Nutzer:

1. **X-Plane herunterladen**
    - Besuchen Sie die [offizielle X-Plane-Website](https://www.x-plane.com/)
    - Erwerben Sie X-Plane 12 (oder laden Sie die Demo-Version herunter)
    - Laden Sie den Linux-Installer herunter (`X-Plane12InstallerLinux.zip`, ca. 25 MB)

2. **Installer vorbereiten**
    - Wechseln Sie in den Download-Ordner und entpacken Sie die Datei:
        ```bash
        cd ~/Downloads
        unzip X-Plane12InstallerLinux.zip
        ```
    - Machen Sie den Installer ausführbar (falls nötig):
        ```bash
        chmod +x "X-Plane 12 Installer Linux"
        ```

3. **Installation starten**
    - Führen Sie den Installer aus:
        ```bash
        ./"X-Plane 12 Installer Linux"
        ```
    - Im grafischen Installer können Sie auswählen:
        - Installationsverzeichnis (empfohlen: `/home/[username]/X-Plane 12/`)
        - Zu ladende Szeneriepakete
        - Weltabdeckung (mindestens Ihr Hauptfluggebiet auswählen)

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

Nach erfolgreicher Installation sollten Sie folgende Schritte durchführen:

1. **Erstes Starten**: Starten Sie X-Plane einmal und schließen Sie es wieder, damit Konfigurationsdateien erstellt werden

2. **Leistungseinstellungen optimieren**: Passen Sie die Grafikeinstellungen entsprechend Ihrer Hardware an. Siehe die Seite [X-Plane-Konfiguration](xplane/config.md) für detaillierte Linux-spezifische Hinweise.

3. **Performance prüfen** mit der eingebauten FPS-Anzeige (Aktivierung mit `Shift+Strg+F`)

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

4. **Beispiel: [32-Bit-Kompatibilität](../glossary.md#32-bit-kompatibilität) (falls notwendig)**:
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

Nach der Installation fehlender Bibliotheken sollten Sie X-Plane erneut starten. In den meisten Fällen werden dadurch Startprobleme behoben, die durch fehlende Abhängigkeiten verursacht wurden.

### Fehlerbehebung bei X-Plane-Installation

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

## Nächste Schritte

Nach einer erfolgreichen Installation geht es mit folgenden Themen weiter:

- [NVIDIA-Treiber](nvidia.md) — Proprietäre NVIDIA-Treiber installieren und konfigurieren
- [Liquorix-Kernel](liquorix.md) — Low-Latency-Kernel optimiert für Desktop-Workloads
- [System-Tuning](systemtuning.md) — CPU-Governor, Interrupt-Shielding und Kernel-Parameter
- [X-Plane-Konfiguration](xplane/config.md) — Linux-spezifische Grafik- und Performance-Einstellungen
