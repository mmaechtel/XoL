## [Nvidia-Treiber](../glossary.md#nvidia-treiber)-Installation unter Debian von der offiziellen Website

Die Installation der [Nvidia-Treiber](../glossary.md#nvidia-treiber) direkt von der offiziellen Nvidia-Website ist eine weitere Option, um Nvidia-Grafikkarten unter Debian zu unterstützen – besonders für die neueste Treiberversion. Dieser Artikel beschreibt den Prozess präzise, nutzt `systemctl set-default` für den Wechsel zwischen Nicht-Grafik- und Grafik-Modus und geht auf die Verwendung des [Liquorix-Kernel](../glossary.md#liquorix-kernel)s ein.

## Voraussetzungen
- Kompatible Nvidia-Grafikkarte
- Debian installiert und aktualisiert
- Optional: Liquorix-Kernel (falls genutzt)
- Root- oder Sudo-Rechte

## Schritt 1: System aktualisieren
Aktualisieren Sie das System:
```bash
sudo apt update && sudo apt upgrade -y
```

## Schritt 2: Abhängigkeiten installieren
Für den Standard-Debian-Kernel installieren Sie Kernel-Header und Build-Tools:
```bash
sudo apt install linux-headers-$(uname -r) build-essential dkms
```
**Hinweis zum [Liquorix-Kernel](../glossary.md#liquorix-kernel)**: Wenn Sie den Liquorix-Kernel nutzen (eine optimierte Kernel-Variante für Performance), sind die Kernel-Header bereits über die Liquorix-Paketquellen verfügbar, nachdem Sie den Kernel installiert haben. Überprüfen Sie mit `uname -r`, ob der Liquorix-Kernel aktiv ist (z. B. `6.6.0-1-liquorix-amd64`). In diesem Fall müssen Sie nur sicherstellen, dass [DKMS](../glossary.md#dkms-dynamic-kernel-module-support) installiert ist, da der Nvidia-Treiber es benötigt, um das Kernel-Modul dynamisch zu kompilieren:
```bash
sudo apt install dkms
```

## Schritt 3: Nvidia-Treiber herunterladen
1. Besuchen Sie [https://www.nvidia.com/Download/index.aspx](https://www.nvidia.com/Download/index.aspx).
2. Wählen Sie Ihre Grafikkarte, "Linux 64-bit" und die Treiberversion aus.
3. Laden Sie die `.run`-Datei (z. B. `NVIDIA-Linux-x86_64-550.54.14.run`) in Ihr Home-Verzeichnis (`/home/user`) herunter.

## Schritt 4: In den Nicht-Grafik-Modus wechseln
Wechseln Sie mit `systemctl` in den Nicht-Grafik-Modus:
1. Ändern Sie den Standard-Boot-Target:
```bash
sudo systemctl set-default multi-user.target
```
2. Starten Sie das System neu:
```bash
sudo reboot
```
Das System bootet in eine Textkonsole ohne Grafikoberfläche.

## Schritt 5: Treiberinstallation durchführen
1. Navigieren Sie zur `.run`-Datei:
```bash
cd /home/user
```
2. Machen Sie die Datei ausführbar:
```bash
chmod +x NVIDIA-Linux-x86_64-550.54.14.run
```
3. Starten Sie die Installation:
```bash
sudo ./NVIDIA-Linux-x86_64-550.54.14.run
```
4. Folgen Sie dem Installationsassistenten:
   - Akzeptieren Sie die Lizenz.
   - Wählen Sie "Ja" für 32-Bit-Kompatibilitätsbibliotheken, falls nötig.
   - Bestätigen Sie die Deaktivierung des [Nouveau](../glossary.md#nouveau)-Treibers, wenn gefragt.
**Liquorix-Kernel**: Dank `dkms` wird das Nvidia-Modul automatisch für den Liquorix-Kernel kompiliert und bei Kernel-Updates aktualisiert.

## Schritt 6: Installation prüfen
Überprüfen Sie den Treiber:
```bash
nvidia-smi
```
Eine Ausgabe mit GPU-Details bestätigt die erfolgreiche Installation.

## Schritt 7: Zurück in den Grafik-Modus wechseln
Setzen Sie den Standard-Boot-Target zurück:
```bash
sudo systemctl set-default graphical.target
```
Starten Sie erneut:
```bash
sudo reboot
```

## Fehlerbehebung
- **Schwarzer Bildschirm**: Falls der Grafik-Modus nicht startet, fügen Sie `nouveau.modeset=0` in `/etc/default/grub` unter `GRUB_CMDLINE_LINUX_DEFAULT` hinzu und führen Sie `sudo update-grub` aus.
- **Fehlende Abhängigkeiten**: Bei Standard-Kerneln prüfen Sie `linux-headers-$(uname -r)`; beim Liquorix-Kernel stellen Sie sicher, dass `dkms` vorhanden ist.

