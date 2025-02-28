## Liquorix Kernel unter Debian

Der [Liquorix-Kernel](../glossary.md#liquorix-kernel) ist eine optimierte Version des Linux-Kernels, die auf Desktop- und Gaming-Performance ausgerichtet ist. Er bietet verbesserte Reaktionszeiten und Leistung durch spezielle Konfigurationen und Patches.

## Voraussetzungen

- Debian installiert und aktualisiert
- Root- oder Sudo-Rechte

## Schritt 1: System aktualisieren

Aktualisieren Sie zunächst Ihr System:
```bash
sudo apt update && sudo apt upgrade -y
```

## Schritt 2: Repository hinzufügen

Fügen Sie das Liquorix-Repository hinzu:

1. **Abhängigkeiten installieren:**
```bash
sudo apt install -y curl gpg
```

2. **Repository-Schlüssel hinzufügen:**
```bash
curl -s 'https://liquorix.net/linux-liquorix-keyring.gpg' | sudo gpg --dearmor -o /usr/share/keyrings/liquorix-keyring.gpg
```

3. **Repository einrichten:**
```bash
echo 'deb [signed-by=/usr/share/keyrings/liquorix-keyring.gpg] https://liquorix.net/debian $(lsb_release -cs) main' | sudo tee /etc/apt/sources.list.d/liquorix.list
```

4. **Paketquellen aktualisieren:**
```bash
sudo apt update
```

## Schritt 3: Kernel installieren

Installieren Sie den Liquorix-Kernel und Header:
```bash
sudo apt install linux-image-liquorix-amd64 linux-headers-liquorix-amd64
```

## Schritt 4: System neu starten

Starten Sie das System neu, um den neuen Kernel zu laden:
```bash
sudo reboot
```

## Schritt 5: Installation überprüfen

Nach dem Neustart können Sie die aktive Kernel-Version überprüfen:
```bash
uname -r
```

Die Ausgabe sollte eine Liquorix-Kernel-Version anzeigen (z.B. `6.6.0-1-liquorix-amd64`).

## Fehlerbehebung

- **Bootprobleme**: Falls der neue Kernel nicht startet, können Sie im GRUB-Menü den Standard-Debian-Kernel auswählen.
- **DKMS-Module**: Für Treiber wie [Nvidia](nvidia.md) ist [DKMS](../glossary.md#dkms-dynamic-kernel-module-support) wichtig:
  ```bash
  sudo apt install dkms
  ```

## Fazit

Der Liquorix-Kernel kann die System-Performance verbessern, besonders für Desktop-Anwendungen und Gaming. Bei Problemen kann jederzeit zum Standard-Kernel zurückgewechselt werden. 