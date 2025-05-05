## Offizieller Nvidia-Treiber

Die Installation der [Nvidia-Treiber](../glossary.md#nvidia-treiber) direkt von der offiziellen Nvidia-Website ist eine weitere Option, um Nvidia-Grafikkarten unter Debian zu unterstützen – besonders für die neueste Treiberversion. Dieses Kapitel beschreibt den Prozess präzise, nutzt `systemctl set-default` für den Wechsel zwischen Nicht-Grafik- und Grafik-Modus und geht auf die Verwendung des [Liquorix-Kernel](../glossary.md#liquorix-kernel)s ein.

## Voraussetzungen

- Kompatible Nvidia-Grafikkarte
- Debian installiert und aktualisiert
- Optional: Liquorix-Kernel (falls genutzt)
- Root- oder Sudo-Rechte

## Installation

### System-Vorbereitung

Das System wird aktualisiert:
```bash
sudo apt update && sudo apt upgrade -y
```

Für den Standard-Debian-Kernel werden Kernel-Header und Build-Tools installiert:
```bash
sudo apt install linux-headers-$(uname -r) build-essential dkms
```

**Hinweis zum [Liquorix-Kernel](../glossary.md#liquorix-kernel)**: Bei Nutzung des Liquorix-Kernels (eine optimierte Kernel-Variante für Performance) sind die Kernel-Header bereits über die Liquorix-Paketquellen verfügbar, nachdem der Kernel installiert wurde. Mit `uname -r` wird überprüft, ob der Liquorix-Kernel aktiv ist (z. B. `6.6.0-1-liquorix-amd64`). In diesem Fall muss nur sichergestellt werden, dass [DKMS](../glossary.md#dkms-dynamic-kernel-module-support) installiert ist, da der Nvidia-Treiber es benötigt, um das Kernel-Modul dynamisch zu kompilieren:
```bash
sudo apt install dkms
```

### Treiber-Installation

1. Die Seite [https://www.nvidia.com/Download/index.aspx](https://www.nvidia.com/Download/index.aspx) wird aufgerufen.
2. Die Grafikkarte, "Linux 64-bit" und die Treiberversion werden ausgewählt.
3. Die `.run`-Datei (z. B. `NVIDIA-Linux-x86_64-550.54.14.run`) wird im Home-Verzeichnis (`/home/user`) heruntergeladen.

Der Wechsel in den Nicht-Grafik-Modus erfolgt mit `systemctl`:
1. Der Standard-Boot-Target wird geändert:
```bash
sudo systemctl set-default multi-user.target
```
2. Das System wird neu gestartet:
```bash
sudo reboot
```

Das System bootet in eine Textkonsole ohne Grafikoberfläche.

Zur `.run`-Datei wird navigiert:
```bash
cd /home/user
```

Die Datei wird ausführbar gemacht:
```bash
chmod +x NVIDIA-Linux-x86_64-550.54.14.run
```

Die Installation wird gestartet:
```bash
sudo ./NVIDIA-Linux-x86_64-550.54.14.run
```

Dem Installationsassistenten wird gefolgt:
- Die Lizenz wird akzeptiert.
- Für 32-Bit-Kompatibilitätsbibliotheken wird "Ja" gewählt, falls nötig.
- Die Deaktivierung des [Nouveau](../glossary.md#nouveau)-Treibers wird bestätigt, wenn gefragt.

**Liquorix-Kernel**: Dank `dkms` wird das Nvidia-Modul automatisch für den Liquorix-Kernel kompiliert und bei Kernel-Updates aktualisiert.

### Installation prüfen

Der Treiber wird überprüft:
```bash
nvidia-smi
```

Eine Ausgabe mit GPU-Details bestätigt die erfolgreiche Installation.

### Zurück in den Grafik-Modus

Der Standard-Boot-Target wird zurückgesetzt:
```bash
sudo systemctl set-default graphical.target
```

Das System wird erneut gestartet:
```bash
sudo reboot
```

## Fehlerbehebung

- **Schwarzer Bildschirm**: Falls der Grafik-Modus nicht startet, wird `nouveau.modeset=0` in `/etc/default/grub` unter `GRUB_CMDLINE_LINUX_DEFAULT` hinzugefügt und `sudo update-grub` ausgeführt.
- **Fehlende Abhängigkeiten**: Bei Standard-Kerneln wird `linux-headers-$(uname -r)` geprüft; beim Liquorix-Kernel wird sichergestellt, dass `dkms` vorhanden ist.

## Performance-Optimierung

### Treiber-Einstellungen

Das NVIDIA-Einstellungsprogramm wird gestartet:
```bash
nvidia-settings
```

Im Programm stehen folgende optionale Einstellungen zur Verfügung, die je nach Bedarf getestet werden können:
- Unter "X Server Display Configuration" → "Advanced" → "Force Full Composition Pipeline":
    - Diese Einstellung verhindert Tearing (Bildschirmrisse) bei Spielen
    - Kann zu leicht erhöhter Latenz führen
    - Empfohlen für Spiele, die unter Tearing leiden
- Unter "X Server Display Configuration" → "Advanced" → "Force Composition Pipeline":
    - Verbessert die Bildqualität und Stabilität
    - Kann die GPU-Auslastung leicht erhöhen
    - Hilft bei Problemen mit der Bildschirmaktualisierung

**Hinweis**: Diese Einstellungen sind optional und können je nach Spiel und Systemkonfiguration unterschiedliche Auswirkungen haben. Es empfiehlt sich, die Einstellungen einzeln zu testen und nur die zu aktivieren, die tatsächlich eine Verbesserung bringen. Falls Performance-Probleme auftreten, können die Einstellungen jederzeit deaktiviert werden.

### Performance-Modi

Der Performance-Modus kann optional über die Kommandozeile aktiviert werden:
```bash
sudo nvidia-smi -pm 1
```

Diese Einstellung hält die GPU in einem höheren Leistungszustand, was die Reaktionszeit verbessert, aber auch den Stromverbrauch erhöht. Sie kann besonders nützlich sein für:
- Spiele mit hohen FPS-Anforderungen
- Anwendungen, die von einer konstanten GPU-Leistung profitieren
- Systeme, bei denen die GPU-Leistung schwankt

**Hinweis**: Der Performance-Modus ist nicht zwingend erforderlich und sollte nur aktiviert werden, wenn tatsächlich Performance-Schwankungen bemerkt werden. Bei X-Plane kann er helfen, wenn die GPU-Leistung unregelmäßig ist oder wenn FPS-Einbrüche in bestimmten Situationen auftreten.

### Kernel-Parameter

In Debian 12 sind die meisten NVIDIA-Optimierungen bereits standardmäßig aktiviert. Falls dennoch manuelle Anpassungen vorgenommen werden sollen, können in `/etc/default/grub` unter `GRUB_CMDLINE_LINUX_DEFAULT` folgende Parameter hinzugefügt werden:
```bash
nvidia-drm.modeset=1
```

Dieser Parameter aktiviert den Direct Rendering Manager (DRM) für NVIDIA. Er ermöglicht:
- Bessere Integration mit dem Linux-Grafik-Stack
- Verbesserte Unterstützung für Wayland
- Optimierte Bildschirmaktualisierung
- Bessere Handhabung von Multi-Monitor-Setups

Danach wird GRUB aktualisiert:
```bash
sudo update-grub
```

**Hinweis**: Die meisten dieser Parameter sind in Debian 12 bereits standardmäßig konfiguriert. Eine manuelle Anpassung ist nur in seltenen Fällen notwendig, z.B. bei spezifischen Performance-Problemen oder wenn Probleme mit der Bildschirmaktualisierung auftreten.

### Zusätzliche Optimierungen

**MangoHud** (optional): Für erweiterte Performance-Monitoring-Funktionen:
```bash
sudo apt install mangohud
```

**Hinweis**: X-Plane bietet bereits eine eingebaute FPS-Anzeige (Strg+Shift+F). MangoHud ist nur notwendig, wenn zusätzliche Monitoring-Funktionen benötigt werden.

### Wichtige Hinweise

- Die Performance kann je nach Systemkonfiguration variieren
- Regelmäßige Treiber-Updates können die Performance verbessern
- Die Einstellungen im NVIDIA-Einstellungsprogramm (`nvidia-settings`) können je nach Treiberversion und Systemkonfiguration variieren

