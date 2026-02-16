# Liquorix Kernel unter Debian

Der Standard-Debian-Kernel ist auf breite Kompatibilität und Server-Workloads ausgelegt. Der [Liquorix-Kernel](../glossary.md#liquorix-kernel) geht einen anderen Weg — er basiert auf dem Zen-Kernel-Patchset und ist gezielt auf Desktop-Reaktionsfähigkeit und latenzempfindliche Anwendungen wie Gaming und Flugsimulation optimiert. Er wird von Steven Barrett gepflegt und ist nicht Teil des offiziellen Debian-Archivs. Vor der Installation empfiehlt sich ein System-Backup.

## Installation

### Voraussetzungen

- Debian installiert und aktualisiert
- Root- oder Sudo-Rechte

### Schnellinstallation (empfohlen)

Das offizielle Installer-Skript übernimmt Schlüsselimport, Repository-Einrichtung und Installation automatisch:

```bash
curl -s 'https://liquorix.net/install-liquorix.sh' | sudo bash
```

### Manuelle Installation

1. **System aktualisieren**

    ```bash
    sudo apt update && sudo apt upgrade -y
    ```

2. **Repository hinzufügen**

    - **Abhängigkeiten installieren**

        ```bash
        sudo apt install -y curl gpg ca-certificates
        ```

    - **Repository-Schlüssel hinzufügen**

        ```bash
        sudo mkdir -p /etc/apt/keyrings
        curl -s 'https://liquorix.net/liquorix-keyring.gpg' | sudo gpg --batch --yes --dearmor -o /etc/apt/keyrings/liquorix-keyring.gpg
        ```

    - **Repository einrichten**

        ```bash
        CODENAME="$(. /etc/os-release && echo "$VERSION_CODENAME")"
        echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/liquorix-keyring.gpg] https://liquorix.net/debian $CODENAME main" | sudo tee /etc/apt/sources.list.d/liquorix.list
        ```

    - **Paketquellen aktualisieren**

        ```bash
        sudo apt update
        ```

3. **Kernel installieren**

    ```bash
    sudo apt install linux-image-liquorix-amd64 linux-headers-liquorix-amd64
    ```

4. **System neu starten**

    ```bash
    sudo reboot
    ```

5. **Installation überprüfen**

    Nach dem Neustart die aktive Kernel-Version prüfen:

    ```bash
    uname -r
    ```

    Die Ausgabe sollte eine Liquorix-Kernel-Version anzeigen (z.B. `6.18.10-1-liquorix-amd64`).

## Warum Liquorix?

Die Vorteile des Liquorix-Kernels ergeben sich aus einer grundlegend anderen Konfiguration im Vergleich zum Standard-Debian-Kernel:

| Einstellung | Debian Stock | Liquorix |
|-------------|-------------|----------|
| **Scheduler** | EEVDF (Mainline) | PDS (Priority and Deadline based Skiplist) |
| **Timer-Frequenz** | 250 Hz | 1000 Hz |
| **Preemption** | Lazy / Dynamic | Full Preempt |
| **Standard-Governor** | `schedutil` | `performance` |
| **Tick-Modell** | Idle (NO_HZ_IDLE) | Full adaptive (NO_HZ_FULL) |

Der **PDS-Scheduler** (von Alfred Chen, Teil des Project-C-Patchsets) ersetzt den Mainline-EEVDF-Scheduler vollständig. Er nutzt eine Skiplist-Datenstruktur zur Verwaltung von Task-Prioritäten und Deadlines und ermöglicht schnelle Scheduling-Entscheidungen mit geringem Overhead. In Kombination mit dem 1000-Hz-Timer und Full-Kernel-Preemption kann Liquorix auf Laständerungen innerhalb von 1 ms reagieren — viermal schneller als der Stock-Kernel mit 250 Hz.

### Optimierungsmodell

Der entscheidende Unterschied liegt darin, was jeder Kernel-Typ für optimale Ergebnisse braucht:

- Ein **Stock-Kernel** profitiert von explizitem Tuning — CPU-Affinität, `SCHED_FIFO` oder `nice`-Werte — weil seine konservativen Defaults Durchsatz über Latenz priorisieren.
- **Liquorix** profitiert von einem **ruhigen System** — werden externe Störungen wie Interrupt-Stürme, NVMe-Energiespar-Übergänge und ungleichmäßiger Writeback-Druck minimiert, kann PDS die Task-Platzierung autonom optimieren.

Manuelles CPU-Pinning oder aggressive Prioritätseskalation können unter Liquorix kontraproduktiv sein: Sie überschreiben genau die adaptiven Entscheidungen, für die PDS ausgelegt ist.

Konkrete Konfigurationsschritte für beide Kernel-Typen finden sich auf der Seite [Systemtuning](../system/systemtuning.md).

!!! warning "Sicherheitshinweis"
    Liquorix folgt der jeweils aktuellen Upstream-Kernel-Reihe und enthält damit die dort enthaltenen Sicherheitskorrekturen. Er wird jedoch **nicht von Debian Security Advisories abgedeckt** — DSAs gelten nur für Pakete im offiziellen Debian-Archiv. Sicherheitsupdates hängen vom Release-Zyklus eines einzelnen Maintainers ab, der hinter dem Debian-Sicherheitsteam zurückbleiben kann. Ein Wechsel zurück zum Stock-Kernel ist jederzeit über das GRUB-Bootmenü möglich.

---

## Wartung

### Updates

Der Kernel wird wie andere Systempakete aktualisiert:

```bash
sudo apt update && sudo apt upgrade
```

### Deinstallation

Falls ein Wechsel zurück zum Standard-Kernel notwendig ist:

1. **Standard-Kernel installieren**

    ```bash
    sudo apt install linux-image-amd64 linux-headers-amd64
    ```

2. **Liquorix-Kernel entfernen**

    ```bash
    sudo apt remove linux-image-liquorix-amd64 linux-headers-liquorix-amd64
    ```

3. **System neu starten**

    ```bash
    sudo reboot
    ```

## Support

### Fehlerbehebung

- **Bootprobleme**: Falls der neue Kernel nicht startet, kann im GRUB-Menü der Standard-Debian-Kernel ausgewählt werden
- **DKMS-Module**: Für Treiber wie [Nvidia](nvidia.md) ist [DKMS](../glossary.md#dkms-dynamic-kernel-module-support) wichtig

    ```bash
    sudo apt install dkms
    ```

- **Performance-Probleme**

    - System-Logs prüfen: `dmesg | grep -i error`
    - CPU-Frequenz überwachen: `cpupower frequency-info`
    - Aktiven Scheduler prüfen: `dmesg | grep sched`

### Ressourcen

- Offizielle Website: [liquorix.net](https://liquorix.net)
- Community-Forum: [Liquorix Forum](https://techpatterns.com/forums/forum-34.html)
- Bug-Reports: [GitHub Issues](https://github.com/damentz/liquorix-package/issues)

---

## Quellen

- [Liquorix Kernel](https://liquorix.net) — Offizielle Projektseite mit Feature-Liste und Installationsanleitung
- [Project C / PDS Scheduler](https://gitlab.com/alfredchen/projectc) — Alfred Chens alternativer CPU-Scheduler-Patchset
- [Liquorix Package Repository](https://github.com/damentz/liquorix-package) — Build-Konfiguration und Release-Historie
- [Linux Kernel Scheduler Documentation](https://docs.kernel.org/scheduler/index.html) — Offizielle Kernel-Dokumentation zum CPU-Scheduling
