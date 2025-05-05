# Dateisystem

## Übersicht

X-Plane, ein datenintensiver Flugsimulator, stellt hohe Anforderungen an Speicherbandbreite und Zugriffszeiten, insbesondere bei der Nutzung umfangreicher Szenerien, hochauflösender Texturen und Add-ons. Die Organisation von **Partitionen** auf **SSDs** oder mehreren Festplatten sowie die Wahl des **Dateisystems** unter Linux beeinflussen die Performance erheblich. Dieser Artikel erläutert, wie Partitionen auf SSDs, verteilte Daten auf mehreren Laufwerken und Dateisysteme unter Linux optimiert werden können, um die beste Leistung für X-Plane zu erzielen.

## Hardware-Empfehlungen

### SSD-Typen und Größen

Für optimale Performance wird eine **NVMe-SSD** (PCIe 3.0 oder besser 4.0) mit mindestens 1 TB Kapazität empfohlen. **NVMe-SSDs** (Non-Volatile Memory Express) bieten mit bis zu 7000 MB/s (PCIe 4.0) deutlich höhere Lese- und Schreibgeschwindigkeiten als **SATA-SSDs**, die maximal 550 MB/s erreichen. Die höhere Geschwindigkeit wird durch eine direkte Verbindung zum **PCIe-Bus** erreicht, wodurch der langsamere SATA-Interface umgangen wird.

Die Mindestgröße von 1 TB ist empfehlenswert, da X-Plane selbst etwa 100-150 GB benötigt und Szenerien sowie Add-ons schnell mehrere hundert GB belegen können. Zusätzlich ist ein freier Speicherplatz von mindestens 20% für optimale Performance erforderlich, da SSDs diesen Overhead für **Wear Leveling** (Verschleißausgleich) und **Garbage Collection** (Speicherbereinigung) benötigen.

### Multi-Laufwerk-Konfigurationen

Eine Kombination aus **SSD** und **HDD** bietet eine praktische Lösung für die Speicherung von X-Plane-Daten. Das Hauptprogramm und häufig genutzte Szenerien sollten auf der SSD gespeichert werden, während selten benötigte Szenerien oder Backups auf der HDD liegen können. Die Verteilung von X-Plane-Daten auf verschiedene SSDs ermöglicht eine **Lastbalancierung** durch parallele Arbeit der Laufwerke. Diese Konfiguration erhöht jedoch die Komplexität im Dateimanagement und kann zu geringfügig längeren Ladezeiten führen.

### Multi-SSD-Konfigurationen mit RAID

Für Nutzer, die maximale Performance anstreben, bietet die Kombination mehrerer SSDs in einem **RAID**-Verbund (Redundant Array of Independent Disks) interessante Möglichkeiten. Die häufigsten Konfigurationen sind **RAID-0** und **RAID-1**, wobei jede ihre eigenen Vor- und Nachteile hat.

**RAID-0** (Striping) verteilt die Daten über alle SSDs und bietet die höchste Performance, da die Lese- und Schreibgeschwindigkeiten nahezu linear mit der Anzahl der SSDs skalieren. Bei drei SSDs kann die Performance nahezu verdreifacht werden. Allerdings bietet **RAID-0** keine Redundanz – ein Ausfall einer SSD führt zum Verlust aller Daten. Diese Konfiguration ist besonders für X-Plane interessant, da die Performance-Vorteile bei großen Szenerien und komplexen Flughäfen spürbar sind. Die fehlende Redundanz erfordert jedoch eine sorgfältige Backup-Strategie.

**RAID-1** (Mirroring) speichert die Daten redundant auf allen SSDs. Die Performance entspricht dabei der einer einzelnen SSD, aber die Daten sind vor Ausfällen geschützt. Diese Konfiguration ist besonders sinnvoll, wenn die Datenintegrität wichtiger ist als die maximale Performance. Allerdings wird die verfügbare Kapazität durch die Anzahl der SSDs geteilt – bei drei SSDs steht nur ein Drittel der Gesamtkapazität zur Verfügung.

Eine interessante Alternative ist die Kombination von **RAID-0** und **RAID-1** in einem **RAID-10**-Setup. Dies erfordert mindestens vier SSDs, bietet aber sowohl hohe Performance als auch Redundanz. Die Daten werden über zwei **RAID-0**-Arrays gestreift, die wiederum gespiegelt werden. Die Performance liegt zwischen der eines einzelnen **RAID-0** und eines **RAID-1**, während die Redundanz erhalten bleibt.

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

Die richtigen **Mount-Optionen** können die Performance erheblich verbessern. Die Option `noatime` reduziert unnötige Schreibzugriffe, indem sie die Zugriffszeiten von Dateien nicht aktualisiert, während `discard` **TRIM** (ein Befehl, der SSDs bei der Verwaltung freien Speicherplatzes hilft) für SSDs aktiviert und `autodefrag` die Dateianordnung für große Dateien optimiert. Diese Optionen können in der `/etc/fstab` konfiguriert werden. Für optimale SSD-Performance sollten regelmäßige SSD-Gesundheitsüberprüfungen durchgeführt und aktuelle Treiber sowie Kernel-Updates verwendet werden.

## Praktisches Beispiel: RAID-0 mit drei SSDs

Ein Nutzer, der X-Plane auf einem Linux-System mit drei SSDs betreibt, kann ein **RAID-0**-Array mit dem **Btrfs**-Dateisystem einrichten, um die Lese- und Schreibgeschwindigkeiten zu maximieren.

**Wichtiger Hinweis**: Nicht alle Linux-Distributionen unterstützen **Btrfs-RAID-0** gleich gut. Besonders gut getestet sind Ubuntu, Fedora und openSUSE.

### Voraussetzungen

Für die Einrichtung eines **RAID-0**-Arrays werden drei identische SSDs (gleiche Kapazität und Geschwindigkeit) benötigt, idealerweise **NVMe**-SSDs. Das System sollte eine aktuelle Linux-Distribution wie Ubuntu 24.04 verwenden und das Paket **btrfs-progs** installiert haben. Root- oder Sudo-Rechte sind erforderlich. Wichtig zu beachten ist, dass alle Daten auf den SSDs gelöscht werden – vorab sollten daher unbedingt Backups erstellt werden.

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
   UUID=<btrfs-uuid> /mnt/xplane btrfs defaults,discard 0 2
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

9. **Optimierung für X-Plane**
   Die Mount-Optionen in `/etc/fstab` werden erweitert:
   ```
   UUID=<btrfs-uuid> /mnt/xplane btrfs defaults,discard,noatime,autodefrag 0 2
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

Durch das **RAID-0**-Setup mit drei SSDs wird eine nahezu dreifache Lese- und Schreibgeschwindigkeit im Vergleich zu einer einzelnen SSD erreicht. Dies führt zu kürzeren Ladezeiten für Szenerien, schnellerem Textur-Streaming und einem flüssigeren Erlebnis in komplexen Umgebungen.

Alle drei SSDs müssen identisch sein, sowohl in der Kapazität als auch in der Geschwindigkeit. Der Zustand der SSDs sollte regelmäßig überprüft werden, beispielsweise mit dem Befehl `sudo smartctl -a /dev/sda`.

## Backup-Strategien

Die Sicherung der X-Plane-Daten ist ein kritischer Aspekt der Systemkonfiguration, besonders bei **RAID-0**-Setups ohne Redundanz. Eine effektive Backup-Strategie umfasst regelmäßige Sicherungen wichtiger Konfigurationsdateien und Einstellungen (täglich), vollständige Sicherungen aller X-Plane-Daten inklusive Szenerien und Add-ons (wöchentlich) sowie die Archivierung der wöchentlichen Backups für die langfristige Aufbewahrung (monatlich).

Als Backup-Medien eignen sich externe **SSDs** für schnelle Backups und Wiederherstellungen, **NAS/RAID**-Systeme für redundante Speicherung und Netzwerkzugriff sowie **Cloud-Speicher** für zusätzliche Sicherheit und Zugriff von verschiedenen Standorten. Zu den wichtigsten Backup-Inhalten gehören das X-Plane-Hauptprogramm und Konfigurationsdateien, Szenerien und Add-ons, Benutzerdaten und Einstellungen sowie Log-Dateien für die Fehleranalyse.

Für automatisierte Backups werden Tools wie `rsync` oder `borg` verwendet:

```bash
# Beispiel für ein tägliches Backup mit rsync
rsync -av --delete /mnt/xplane/ /backup/xplane/daily/

# Beispiel für ein wöchentliches Backup mit borg
borg create /backup/xplane/weekly::$(date +%Y-%m-%d) /mnt/xplane/
```

Regelmäßige Wiederherstellungstests werden durchgeführt, um die Integrität der Backups zu überprüfen. Der Wiederherstellungsprozess wird dokumentiert und die notwendigen Tools werden bereitgehalten.

## Fazit

Die optimale Konfiguration für X-Plane unter Linux besteht aus einer einzelnen Partition auf einer schnellen **NVMe-SSD** mit dem **Ext4**-Dateisystem. Aktiviertes **TRIM** und optimierte **Mount-Optionen** sowie ausreichend freier Speicherplatz sind weitere wichtige Faktoren. Diese Konfiguration minimiert Ladezeiten und gewährleistet ein flüssiges Flugerlebnis in X-Plane.

Für Nutzer, die maximale Performance anstreben, bietet ein **RAID-0** mit **Btrfs** auf drei SSDs eine leistungsstarke Alternative. Die Konfiguration minimiert Ladezeiten und optimiert das Streaming von Szenerien. Durch die Verwendung von **Btrfs** mit **TRIM**, noatime und autodefrag wird die SSD-Leistung langfristig erhalten. Eine sorgfältig geplante Backup-Strategie ist dabei unerlässlich, um Datenverluste zu vermeiden und die Kontinuität des Flugbetriebs zu gewährleisten.