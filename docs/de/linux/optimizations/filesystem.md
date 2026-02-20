---
description: "Dateisystem-Optimierung für X-Plane unter Linux: NVMe-SSD-Setup, Ext4/Btrfs/XFS-Vergleich, Mount-Optionen, RAID-0-Konfiguration und Backup-Strategien."
---
# Dateisystem

## Übersicht

X-Plane, ein datenintensiver Flugsimulator, stellt hohe Anforderungen an Speicherbandbreite und Zugriffszeiten, insbesondere bei der Nutzung umfangreicher Szenerien, hochauflösender Texturen und Add-ons. Die Organisation von **Partitionen** auf **SSDs** oder mehreren Festplatten sowie die Wahl des **Dateisystems** unter Linux beeinflussen die Performance erheblich. Dieses Kapitel erläutert, wie Partitionen auf SSDs, verteilte Daten auf mehreren Laufwerken und Dateisysteme unter Linux optimiert werden können, um die beste Leistung für X-Plane zu erzielen.

## Hardware-Empfehlungen

### SSD-Typen und Größen

Für optimale Performance wird eine **NVMe-SSD** (PCIe 3.0 oder besser 4.0) mit mindestens 1 TB Kapazität empfohlen. NVMe-SSDs bieten deutlich höhere Lese- und Schreibgeschwindigkeiten — bis zu ~3500 MB/s (PCIe 3.0) oder ~7000 MB/s (PCIe 4.0) — im Vergleich zu SATA-SSDs, die maximal 550 MB/s erreichen. Die höhere Geschwindigkeit wird durch eine direkte Verbindung zum PCIe-Bus erreicht, wodurch das langsamere SATA-Interface umgangen wird.

Die Mindestgröße von 1 TB ist empfehlenswert, da X-Plane 12 mit globaler Szenerie etwa 80–100 GB benötigt und Drittanbieter-Szenerien sowie Add-ons schnell mehrere hundert GB belegen können. Zusätzlich werden mindestens 10–15% freier Speicherplatz für optimale Performance empfohlen, da SSDs diesen Spielraum für Wear Leveling und Garbage Collection nutzen.

### Multi-Laufwerk-Konfigurationen

Eine Kombination aus **SSD** und **HDD** bietet eine praktische Lösung für die Speicherung von X-Plane-Daten. Das Hauptprogramm und häufig genutzte Szenerien sollten auf der SSD gespeichert werden, während selten benötigte Szenerien oder Backups auf der HDD liegen können. Die Verteilung von X-Plane-Daten auf verschiedene SSDs ermöglicht eine **Lastbalancierung** durch parallele Arbeit der Laufwerke. Diese Konfiguration erhöht jedoch die Komplexität im Dateimanagement und kann zu geringfügig längeren Ladezeiten führen.

### Multi-SSD-Konfigurationen mit RAID

Für Nutzer, die maximale Performance anstreben, bietet die Kombination mehrerer SSDs in einem **RAID**-Verbund (Redundant Array of Independent Disks) interessante Möglichkeiten. Die häufigsten Konfigurationen sind **RAID-0** und **RAID-1**, wobei jede ihre eigenen Vor- und Nachteile hat.

**RAID-0** (Striping) verteilt die Daten über alle SSDs und bietet den höchsten Durchsatz für sequentielle Operationen. Bei drei SSDs kann der sequentielle Lese-/Schreibdurchsatz nahezu das Dreifache einer einzelnen SSD erreichen — die Verbesserung bei zufälligen I/O-Zugriffen ist geringer. Allerdings bietet RAID-0 keine Redundanz — ein Ausfall einer SSD führt zum Verlust aller Daten.

!!! warning "RAID-0: Keine Redundanz"
    Der Ausfall eines einzelnen Laufwerks zerstört alle Daten im Array. Eine Backup-Strategie ist zwingend erforderlich — siehe [Backup-Strategien](#backup-strategien).

**RAID-1** (Mirroring) speichert die Daten redundant. Bei Standard-RAID-1 werden Daten auf zwei Laufwerke gespiegelt, was 50% nutzbare Kapazität ergibt. Btrfs-RAID-1 speichert zwei Kopien unabhängig von der Laufwerkanzahl — bei drei SSDs steht somit etwa die Hälfte der Gesamtkapazität zur Verfügung. Die Leseleistung verbessert sich (Lesezugriffe können verteilt werden), die Schreibgeschwindigkeit entspricht einer einzelnen SSD.

Bei der Planung eines **RAID**-Setups sollten folgende Aspekte berücksichtigt werden:

- Alle SSDs sollten identisch sein (gleiche Kapazität und Geschwindigkeit)
- Die Gesamtkapazität muss ausreichend für X-Plane und alle Szenerien sein
- Die Wahl des Dateisystems (**Btrfs**, **ZFS**) kann die **RAID**-Funktionalität beeinflussen

Eine detaillierte Anleitung zur Einrichtung eines **RAID-0**-Setups findet sich im Abschnitt [Praktisches Beispiel: RAID-0 mit drei SSDs](#praktisches-beispiel-raid-0-mit-drei-ssds).

## Dateisystem-Typen

Das Standard-Dateisystem **Ext4** für die meisten Linux-Distributionen bietet eine gute Balance zwischen Performance und Stabilität. Es ist für X-Plane eine sichere Wahl, da es schnelle Lese- und Schreibzugriffe unterstützt und für SSDs optimiert werden kann. **Ext4** enthält Features wie **Journaling** (für Datenintegrität), **Extents** (für bessere Handhabung großer Dateien) und **Delayed Allocation** (für verbesserte Performance).

**Btrfs** bietet moderne Features wie **Snapshots** (zeitpunktgenaue Kopien des Dateisystems) und **Datenintegritätsprüfungen** (mit Prüfsummen), die besonders für X-Plane-Installationen von Vorteil sein können. Es unterstützt **Kompression** und ist komplexer zu verwalten, kann aber bei intensiven Schreibvorgängen geringfügig langsamer sein als **ext4**. **Btrfs** enthält zudem eingebaute **RAID**-Unterstützung und **Subvolume**-Management.

**XFS** ist ein leistungsstarkes **Journaling**-Dateisystem, das besonders gut für große Dateien geeignet ist. Es bietet hervorragende Performance bei sequentiellen Lesevorgängen und ist ideal für X-Plane-Szenerien mit großen Texturdateien. **XFS** ist bekannt für seine **Skalierbarkeit** und **Zuverlässigkeit**, besonders bei großen Dateien und hohen **I/O**-Lasten.

## Optimierungen

Die Verwendung einer einzelnen **Partition** auf einer SSD vereinfacht die Verwaltung und ermöglicht X-Plane schnellen Zugriff auf alle Daten. Moderne SSDs, insbesondere **NVMe**-Modelle, erleiden keine nennenswerten Performance-Einbußen durch **Fragmentierung**. Bei mehreren Partitionen auf einer SSD entsteht ein minimaler Overhead durch Partitionswechsel. Dieser Einfluss ist bei leistungsstarken SSDs meist vernachlässigbar. Dennoch wird empfohlen, X-Plane und zugehörige Daten auf einer Partition zu speichern.

Die richtigen Mount-Optionen können unnötigen I/O-Overhead reduzieren:

| Option | Wirkung | Empfohlen für |
|--------|---------|---------------|
| `noatime` | Überspringt Zugriffszeit-Updates bei Lesevorgängen | Alle Dateisysteme auf SSDs |
| `discard=async` | Asynchrones TRIM (Btrfs-Standard seit Kernel 6.2) | Btrfs — meist nicht nötig in fstab |
| `fstrim.timer` | Periodisches TRIM über systemd-Timer | Ext4, XFS — bevorzugt gegenüber `discard`-Mount-Option |

!!! tip "Schnellempfehlung"
    Für die meisten Nutzer: NVMe-SSD, Ext4 mit `noatime`, `fstrim.timer` aktivieren. Damit sind die wichtigsten Punkte abgedeckt.

**Ext4-Beispiel** (`/etc/fstab`):

```
UUID=<ext4-uuid> /mnt/xplane ext4 defaults,noatime 0 2
```

Periodisches TRIM aktivieren:

```bash
sudo systemctl enable --now fstrim.timer
```

## Praktisches Beispiel: RAID-0 mit drei SSDs

Ein Nutzer, der X-Plane auf einem Linux-System mit drei SSDs betreibt, kann ein **RAID-0**-Array mit dem **Btrfs**-Dateisystem einrichten, um die Lese- und Schreibgeschwindigkeiten zu maximieren.

**Wichtiger Hinweis**: Nicht alle Linux-Distributionen unterstützen **Btrfs-RAID-0** gleich gut. Besonders gut getestet sind Ubuntu, Fedora und openSUSE.

### Voraussetzungen

Für die Einrichtung eines **RAID-0**-Arrays werden drei identische SSDs (gleiche Kapazität und Geschwindigkeit) benötigt, idealerweise **NVMe**-SSDs. Das System sollte eine aktuelle Linux-Distribution wie Debian 13 (Trixie) verwenden und das Paket **btrfs-progs** installiert haben. Root- oder Sudo-Rechte sind erforderlich. Wichtig zu beachten ist, dass alle Daten auf den SSDs gelöscht werden – vorab sollten daher unbedingt Backups erstellt werden.

### Schritt-für-Schritt-Anleitung

1. **SSDs identifizieren**
   ```bash
   lsblk
   ```
   Angenommen, die SSDs sind /dev/sda, /dev/sdb und /dev/sdc. Es ist sicherzustellen, dass keine Partitionen oder Daten auf diesen Laufwerken vorhanden sind.

2. **Partitionen löschen (falls vorhanden)**
   ```bash
   sudo wipefs -a /dev/sda
   sudo wipefs -a /dev/sdb
   sudo wipefs -a /dev/sdc
   ```
   Dies entfernt alle vorhandenen Dateisysteme und Partitionen.

3. **RAID-0 mit Btrfs erstellen**
   ```bash
   sudo mkfs.btrfs -d raid0 -m raid1 /dev/sda /dev/sdb /dev/sdc
   ```
    - `-d raid0`: Daten werden im **RAID-0**-Modus über alle drei SSDs gestreift
    - `-m raid1`: Metadaten werden im **RAID-1**-Modus gespeichert (für zusätzliche Sicherheit der Dateisystem-Metadaten)
    - `/dev/sda /dev/sdb /dev/sdc`: Die drei SSDs, die das Array bilden

4. **Mount-Punkt erstellen und Dateisystem mounten**
   ```bash
   sudo mkdir /mnt/xplane
   sudo mount /dev/sda /mnt/xplane
   ```
   Da **Btrfs** ein Multi-Device-Dateisystem ist, reicht es, eines der Geräte zu mounten – **Btrfs** erkennt automatisch die anderen Geräte des Arrays.

5. **Btrfs-Status überprüfen**
   ```bash
   sudo btrfs filesystem show /mnt/xplane
   ```
   Die Ausgabe zeigt die drei SSDs und bestätigt, dass die Daten im **RAID-0**-Modus gestreift werden.

6. **TRIM aktivieren**
   In `/etc/fstab` wird folgende Zeile hinzugefügt:
   ```
   UUID=<btrfs-uuid> /mnt/xplane btrfs defaults,noatime 0 0
   ```
   Die UUID wird mit folgendem Befehl ermittelt:
   ```bash
   sudo blkid /dev/sda
   ```

7. **Berechtigungen anpassen**
   ```bash
   sudo chown $USER:$USER /mnt/xplane
   ```

8. **X-Plane installieren**
   ```bash
   cp -r /path/to/xplane /mnt/xplane/
   ```

9. **TRIM überprüfen**
   Btrfs aktiviert `discard=async` seit Kernel 6.2 standardmäßig auf SSDs. Überprüfung:
   ```bash
   findmnt -o FSTYPE,OPTIONS /mnt/xplane | grep discard
   ```

10. **System neustarten und testen**
    ```bash
    sudo reboot
    ```
    Nach dem Neustart wird der Mount-Status überprüft:
    ```bash
    df -h /mnt/xplane
    ```

### Performance-Vorteile und Wichtige Hinweise

Das RAID-0-Setup mit drei SSDs kann den sequentiellen Durchsatz nahezu verdreifachen im Vergleich zu einer einzelnen SSD. Beim Laden von X-Plane-Szenerien (viele kleine Texturdateien) ist die Verbesserung geringer, aber dennoch spürbar — kürzere Ladezeiten und flüssigeres Textur-Streaming in komplexen Umgebungen.

Alle drei SSDs müssen identisch sein, sowohl in der Kapazität als auch in der Geschwindigkeit. Der Zustand der SSDs sollte regelmäßig überprüft werden, beispielsweise mit dem Befehl `sudo smartctl -a /dev/sda`.

## Backup-Strategien

Die Sicherung der X-Plane-Daten ist ein kritischer Aspekt der Systemkonfiguration, besonders bei **RAID-0**-Setups ohne Redundanz. Eine effektive Backup-Strategie umfasst regelmäßige Sicherungen wichtiger Konfigurationsdateien und Einstellungen (täglich), vollständige Sicherungen aller X-Plane-Daten inklusive Szenerien und Add-ons (wöchentlich) sowie die Archivierung der wöchentlichen Backups für die langfristige Aufbewahrung (monatlich).

Als Backup-Medien eignen sich externe **SSDs** für schnelle Backups und Wiederherstellungen, **NAS/RAID**-Systeme für redundante Speicherung und Netzwerkzugriff sowie **Cloud-Speicher** für zusätzliche Sicherheit und Zugriff von verschiedenen Standorten. Zu den wichtigsten Backup-Inhalten gehören das X-Plane-Hauptprogramm und Konfigurationsdateien, Szenerien und Add-ons, Benutzerdaten und Einstellungen sowie Log-Dateien für die Fehleranalyse.

Für automatisierte Backups werden Tools wie `rsync` oder `borg` verwendet:

```bash
# Beispiel für ein tägliches Backup mit rsync
rsync -av --delete /mnt/xplane/ /backup/xplane/daily/

# Beispiel für ein wöchentliches Backup mit borg (Borg 2.x Syntax)
borg -r /backup/xplane/weekly create $(date +%Y-%m-%d) /mnt/xplane/
```

Regelmäßige Wiederherstellungstests werden durchgeführt, um die Integrität der Backups zu überprüfen. Der Wiederherstellungsprozess wird dokumentiert und die notwendigen Tools werden bereitgehalten.

## Fazit

Die optimale Konfiguration für X-Plane unter Linux besteht aus einer einzelnen Partition auf einer schnellen **NVMe-SSD** mit dem **Ext4**-Dateisystem. Aktiviertes **TRIM** und optimierte **Mount-Optionen** sowie ausreichend freier Speicherplatz sind weitere wichtige Faktoren. Diese Konfiguration minimiert Ladezeiten und gewährleistet ein flüssiges Flugerlebnis in X-Plane.

Für Nutzer, die maximale Performance anstreben, bietet ein **RAID-0** mit **Btrfs** auf drei SSDs eine leistungsstarke Alternative. Die Konfiguration minimiert Ladezeiten und optimiert das Streaming von Szenerien. Die Verwendung von **Btrfs** mit **TRIM** und `noatime` erhält die SSD-Leistung langfristig. Eine sorgfältig geplante Backup-Strategie ist dabei unerlässlich, um Datenverluste zu vermeiden und die Kontinuität des Flugbetriebs zu gewährleisten.

---

## Quellen

- [Btrfs Wiki — Mount Options](https://btrfs.readthedocs.io/en/latest/Administration.html)
- [Arch Wiki — Btrfs](https://wiki.archlinux.org/title/Btrfs)
- [Arch Wiki — Solid state drive](https://wiki.archlinux.org/title/Solid_state_drive)
- [Kernel Documentation — Ext4](https://docs.kernel.org/filesystems/ext4/index.html)
- [BorgBackup Documentation](https://borgbackup.readthedocs.io/en/stable/)

---

## Weiterführende Kapitel

| Thema | Seite | Schwerpunkt |
|---|---|---|
| Kernel-Tuning | [Kernel-Tuning](../system/systemtuning.md) | NVMe-Energiesparen, Writeback-Parameter |
| Monitoring | [Monitoring](../system/systemtools.md) | iotop, iostat, ioping für Disk-Latenz-Analyse |
| Lastdimensionen | [Lastdimensionen](../../fundamentals/performance/performance_overview.md) | IO als Performance-Dimension |
| Konfiguration | [Konfiguration](../../xplane/setup_diagnose/config.md) | X-Plane-Dateipfade und Datenablage |
| Szenerie-Komponenten | [Szenerie-Komponenten](../../scenery/aufbau_quellen/scenery_components.md) | Welche Dateien X-Plane von der Disk liest |