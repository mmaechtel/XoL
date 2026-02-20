---
description: "Filesystem optimization for X-Plane on Linux: NVMe SSD setup, Ext4/Btrfs/XFS comparison, mount options, RAID-0 configuration, and backup strategies."
---
# Filesystem

## Overview

X-Plane, a data-intensive flight simulator, places high demands on storage bandwidth and access times, especially when using extensive scenery, high-resolution textures, and add-ons. The organization of **partitions** on **SSDs** or multiple hard drives, as well as the choice of **filesystem** under Linux, significantly impacts performance. This chapter explains how partitions on SSDs, distributed data across multiple drives, and filesystems under Linux can be optimized to achieve the best performance for X-Plane.

## Hardware Recommendations

### SSD Types and Sizes

For optimal performance, an **NVMe SSD** (PCIe 3.0 or better 4.0) with at least 1 TB capacity is recommended. NVMe SSDs offer significantly higher read and write speeds — up to ~3500 MB/s (PCIe 3.0) or ~7000 MB/s (PCIe 4.0) — compared to SATA SSDs, which reach a maximum of 550 MB/s. The higher speed is achieved through a direct connection to the PCIe bus, bypassing the slower SATA interface.

The minimum size of 1 TB is recommended because X-Plane 12 with full global scenery requires approximately 80–100 GB, and third-party scenery and add-ons can quickly add several hundred GB more. Additionally, at least 10–15% free storage space is recommended for optimal performance, as SSDs use this headroom for wear leveling and garbage collection.

### Multi-Drive Configurations

A combination of **SSD** and **HDD** provides a practical solution for storing X-Plane data. The main program and frequently used scenery should be stored on the SSD, while rarely needed scenery or backups can be stored on the HDD. Distributing X-Plane data across different SSDs enables **load balancing** through parallel operation of the drives. However, this configuration increases complexity in file management and may result in slightly longer loading times.

### Multi-SSD Configurations with RAID

For users seeking maximum performance, combining multiple SSDs in a **RAID** array (Redundant Array of Independent Disks) offers interesting possibilities. The most common configurations are **RAID-0** and **RAID-1**, each with its own advantages and disadvantages.

**RAID-0** (Striping) distributes data across all SSDs and offers the highest throughput for sequential operations. With three SSDs, sequential read/write speeds can approach triple that of a single drive — random I/O improvements are smaller. However, RAID-0 offers no redundancy — failure of one SSD leads to loss of all data.

!!! warning "RAID-0: No redundancy"
    Any single drive failure destroys all data in the array. A backup strategy is essential — see [Backup Strategies](#backup-strategies).

**RAID-1** (Mirroring) stores data redundantly. In standard RAID-1, data is mirrored across two drives, providing 50% usable capacity. Btrfs RAID-1 stores two copies regardless of drive count, so with three SSDs, approximately half the total capacity is available. Read performance improves (reads can be distributed), but write speed corresponds to a single drive.

When planning a RAID setup, the following aspects should be considered:

- All SSDs should be identical (same capacity and speed)
- Total capacity must be sufficient for X-Plane and all scenery
- Choice of filesystem (Btrfs, ZFS) can affect RAID functionality

A detailed guide for setting up a RAID-0 configuration can be found in the section [Practical Example: RAID-0 with Three SSDs](#practical-example-raid-0-with-three-ssds).

## Filesystem Types

The standard filesystem **Ext4** for most Linux distributions offers a good balance between performance and stability. It is a safe choice for X-Plane as it supports fast read and write access and can be optimized for SSDs. **Ext4** includes features such as **journaling** (for data integrity), **extents** (for better handling of large files), and **delayed allocation** (for improved performance).

**Btrfs** offers modern features such as **snapshots** (point-in-time copies of the filesystem) and **data integrity checks** (with checksums), which can be particularly beneficial for X-Plane installations. It supports **compression** and is more complex to manage, but may be slightly slower than **ext4** during intensive write operations. **Btrfs** also includes built-in **RAID** support and **subvolume** management.

**XFS** is a powerful **journaling** filesystem particularly well-suited for large files. It offers excellent performance for sequential read operations and is ideal for X-Plane scenery with large texture files. **XFS** is known for its **scalability** and **reliability**, especially with large files and high **I/O** loads.

## Optimizations

Using a single **partition** on an SSD simplifies management and allows X-Plane quick access to all data. Modern SSDs, especially **NVMe** models, suffer no significant performance degradation from **fragmentation**. With multiple partitions on an SSD, there is minimal overhead from partition switching. This impact is usually negligible with high-performance SSDs. Nevertheless, it is recommended to store X-Plane and related data on a single partition.

The right mount options can reduce unnecessary I/O overhead:

| Option | Effect | Recommended for |
|--------|--------|-----------------|
| `noatime` | Skips access time updates on reads | All filesystems on SSDs |
| `discard=async` | Asynchronous TRIM (Btrfs default since kernel 6.2) | Btrfs — usually not needed in fstab |
| `fstrim.timer` | Periodic TRIM via systemd timer | Ext4, XFS — preferred over `discard` mount option |

!!! tip "Quick recommendation"
    For most users: NVMe SSD, Ext4 with `noatime`, enable `fstrim.timer`. That covers the essentials.

**Ext4 example** (`/etc/fstab`):

```
UUID=<ext4-uuid> /mnt/xplane ext4 defaults,noatime 0 2
```

Enable periodic TRIM:

```bash
sudo systemctl enable --now fstrim.timer
```

## Practical Example: RAID-0 with Three SSDs

A user running X-Plane on a Linux system with three SSDs can set up a **RAID-0** array with the **Btrfs** filesystem to maximize read and write speeds.

**Important Note**: Not all Linux distributions support **Btrfs-RAID-0** equally well. Ubuntu, Fedora, and openSUSE are particularly well-tested.

### Prerequisites

Setting up a **RAID-0** array requires three identical SSDs (same capacity and speed), ideally **NVMe** SSDs. The system should use a current Linux distribution such as Debian 13 (Trixie) and have the **btrfs-progs** package installed. Root or sudo privileges are required. It is important to note that all data on the SSDs will be deleted – backups should therefore be created beforehand.

### Step-by-Step Guide

1. **Identify SSDs**
   ```bash
   lsblk
   ```
   Assuming the SSDs are /dev/sda, /dev/sdb, and /dev/sdc. Ensure there are no partitions or data on these drives.

2. **Delete Partitions (if present)**
   ```bash
   sudo wipefs -a /dev/sda
   sudo wipefs -a /dev/sdb
   sudo wipefs -a /dev/sdc
   ```
   This removes all existing filesystems and partitions.

3. **Create RAID-0 with Btrfs**
   ```bash
   sudo mkfs.btrfs -d raid0 -m raid1 /dev/sda /dev/sdb /dev/sdc
   ```
    - `-d raid0`: Data is striped across all three SSDs in **RAID-0** mode
    - `-m raid1`: Metadata is stored in **RAID-1** mode (for additional filesystem metadata security)
    - `/dev/sda /dev/sdb /dev/sdc`: The three SSDs forming the array

4. **Create Mount Point and Mount Filesystem**
   ```bash
   sudo mkdir /mnt/xplane
   sudo mount /dev/sda /mnt/xplane
   ```
   Since **Btrfs** is a multi-device filesystem, mounting one device is sufficient – **Btrfs** automatically recognizes the other array devices.

5. **Check Btrfs Status**
   ```bash
   sudo btrfs filesystem show /mnt/xplane
   ```
   The output shows the three SSDs and confirms that data is striped in **RAID-0** mode.

6. **Enable TRIM**
   Add the following line to `/etc/fstab`:
   ```
   UUID=<btrfs-uuid> /mnt/xplane btrfs defaults,noatime 0 0
   ```
   The UUID is determined with:
   ```bash
   sudo blkid /dev/sda
   ```

7. **Adjust Permissions**
   ```bash
   sudo chown $USER:$USER /mnt/xplane
   ```

8. **Install X-Plane**
   ```bash
   cp -r /path/to/xplane /mnt/xplane/
   ```

9. **Verify TRIM**
   Btrfs enables `discard=async` by default on SSDs since kernel 6.2. Verify:
   ```bash
   findmnt -o FSTYPE,OPTIONS /mnt/xplane | grep discard
   ```

10. **Restart System and Test**
    ```bash
    sudo reboot
    ```
    After restart, check mount status:
    ```bash
    df -h /mnt/xplane
    ```

### Performance Benefits and Important Notes

The RAID-0 setup with three SSDs can approach triple sequential throughput compared to a single SSD. For X-Plane's scenery loading (many small texture files), the improvement is smaller but still noticeable — shorter loading times and smoother texture streaming in complex environments.

All three SSDs must be identical, both in capacity and speed. The condition of the SSDs should be regularly checked, for example with the command `sudo smartctl -a /dev/sda`.

## Backup Strategies

Backing up X-Plane data is a critical aspect of system configuration, especially with **RAID-0** setups without redundancy. An effective backup strategy includes regular backups of important configuration files and settings (daily), complete backups of all X-Plane data including scenery and add-ons (weekly), and archiving of weekly backups for long-term storage (monthly).

Suitable backup media include external **SSDs** for fast backups and restores, **NAS/RAID** systems for redundant storage and network access, and **cloud storage** for additional security and access from various locations. The most important backup contents include the X-Plane main program and configuration files, scenery and add-ons, user data and settings, and log files for error analysis.

Tools like `rsync` or `borg` are used for automated backups:

```bash
# Example for daily backup with rsync
rsync -av --delete /mnt/xplane/ /backup/xplane/daily/

# Example for weekly backup with borg (Borg 2.x syntax)
borg -r /backup/xplane/weekly create $(date +%Y-%m-%d) /mnt/xplane/
```

Regular recovery tests are performed to verify backup integrity. The recovery process is documented and necessary tools are kept ready.

## Conclusion

The optimal configuration for X-Plane under Linux consists of a single partition on a fast **NVMe SSD** with the **Ext4** filesystem. Enabled **TRIM** and optimized **mount options**, as well as sufficient free storage space, are additional important factors. This configuration minimizes loading times and ensures a smooth flight experience in X-Plane.

For users seeking maximum performance, a **RAID-0** with **Btrfs** on three SSDs offers a powerful alternative. The configuration minimizes loading times and optimizes scenery streaming. Using **Btrfs** with **TRIM** and `noatime` maintains SSD performance long-term. A carefully planned backup strategy is essential to prevent data loss and ensure flight operation continuity.

---

## Sources

- [Btrfs Wiki — Mount Options](https://btrfs.readthedocs.io/en/latest/Administration.html)
- [Arch Wiki — Btrfs](https://wiki.archlinux.org/title/Btrfs)
- [Arch Wiki — Solid state drive](https://wiki.archlinux.org/title/Solid_state_drive)
- [Kernel Documentation — Ext4](https://docs.kernel.org/filesystems/ext4/index.html)
- [BorgBackup Documentation](https://borgbackup.readthedocs.io/en/stable/)

---

## Further Reading

| Topic | Page | Focus |
|---|---|---|
| Kernel Tuning | [Kernel Tuning](../system/systemtuning.md) | NVMe power saving, writeback parameters |
| Monitoring | [Monitoring](../system/systemtools.md) | iotop, iostat, ioping for disk latency analysis |
| Load Dimensions | [Load Dimensions](../../fundamentals/performance/performance_overview.md) | IO as a performance dimension |
| Configuration | [Configuration](../../xplane/setup_diagnose/config.md) | X-Plane file paths and data locations |
| Scenery Components | [Scenery Components](../../scenery/aufbau_quellen/scenery_components.md) | What files X-Plane reads from disk |