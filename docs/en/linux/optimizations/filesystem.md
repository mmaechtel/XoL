---
description: "Filesystem optimization for X-Plane on Linux: NVMe SSD setup, Ext4/Btrfs/XFS comparison, mount options, RAID-0 configuration, and backup strategies."
---
# Filesystem

## Overview

X-Plane, a data-intensive flight simulator, places high demands on storage bandwidth and access times, especially when using extensive scenery, high-resolution textures, and add-ons. The organization of **partitions** on **SSDs** or multiple hard drives, as well as the choice of **filesystem** under Linux, significantly impacts performance. This chapter explains how partitions on SSDs, distributed data across multiple drives, and filesystems under Linux can be optimized to achieve the best performance for X-Plane.

## Hardware Recommendations

### SSD Types and Sizes

For optimal performance, an **NVMe SSD** (PCIe 3.0 or better 4.0) with at least 1 TB capacity is recommended. **NVMe SSDs** (Non-Volatile Memory Express) offer significantly higher read and write speeds of up to 7000 MB/s (PCIe 4.0) compared to **SATA SSDs**, which reach a maximum of 550 MB/s. The higher speed is achieved through a direct connection to the **PCIe bus**, bypassing the slower SATA interface.

The minimum size of 1 TB is recommended because X-Plane itself requires about 100-150 GB, and scenery and add-ons can quickly occupy several hundred GB. Additionally, at least 20% free storage space is required for optimal performance, as SSDs need this overhead for **wear leveling** and **garbage collection**.

### Multi-Drive Configurations

A combination of **SSD** and **HDD** provides a practical solution for storing X-Plane data. The main program and frequently used scenery should be stored on the SSD, while rarely needed scenery or backups can be stored on the HDD. Distributing X-Plane data across different SSDs enables **load balancing** through parallel operation of the drives. However, this configuration increases complexity in file management and may result in slightly longer loading times.

### Multi-SSD Configurations with RAID

For users seeking maximum performance, combining multiple SSDs in a **RAID** array (Redundant Array of Independent Disks) offers interesting possibilities. The most common configurations are **RAID-0** and **RAID-1**, each with its own advantages and disadvantages.

**RAID-0** (Striping) distributes data across all SSDs and offers the highest performance, as read and write speeds scale almost linearly with the number of SSDs. With three SSDs, performance can be nearly tripled. However, **RAID-0** offers no redundancy – failure of one SSD leads to loss of all data. This configuration is particularly interesting for X-Plane, as the performance benefits are noticeable with large scenery and complex airports. The lack of redundancy, however, requires a careful backup strategy.

**RAID-1** (Mirroring) stores data redundantly on all SSDs. Performance corresponds to that of a single SSD, but data is protected against failures. This configuration is particularly useful when data integrity is more important than maximum performance. However, the available capacity is divided by the number of SSDs – with three SSDs, only one-third of the total capacity is available.

An interesting alternative is the combination of **RAID-0** and **RAID-1** in a **RAID-10** setup. This requires at least four SSDs but offers both high performance and redundancy. Data is striped across two **RAID-0** arrays, which are then mirrored. Performance lies between that of a single **RAID-0** and **RAID-1**, while maintaining redundancy.

When planning a **RAID** setup, the following aspects should be considered:

- All SSDs should be identical (same capacity and speed)
- Total capacity must be sufficient for X-Plane and all scenery
- Choice of filesystem (**Btrfs**, **ZFS**) can affect **RAID** functionality

A detailed guide for setting up a **RAID-0** configuration can be found in the section [Practical Example: RAID-0 with Three SSDs](#practical-example-raid-0-with-three-ssds).

## Filesystem Types

The standard filesystem **Ext4** for most Linux distributions offers a good balance between performance and stability. It is a safe choice for X-Plane as it supports fast read and write access and can be optimized for SSDs. **Ext4** includes features such as **journaling** (for data integrity), **extents** (for better handling of large files), and **delayed allocation** (for improved performance).

**Btrfs** offers modern features such as **snapshots** (point-in-time copies of the filesystem) and **data integrity checks** (with checksums), which can be particularly beneficial for X-Plane installations. It supports **compression** and is more complex to manage, but may be slightly slower than **ext4** during intensive write operations. **Btrfs** also includes built-in **RAID** support and **subvolume** management.

**XFS** is a powerful **journaling** filesystem particularly well-suited for large files. It offers excellent performance for sequential read operations and is ideal for X-Plane scenery with large texture files. **XFS** is known for its **scalability** and **reliability**, especially with large files and high **I/O** loads.

## Optimizations

Using a single **partition** on an SSD simplifies management and allows X-Plane quick access to all data. Modern SSDs, especially **NVMe** models, suffer no significant performance degradation from **fragmentation**. With multiple partitions on an SSD, there is minimal overhead from partition switching. This impact is usually negligible with high-performance SSDs. Nevertheless, it is recommended to store X-Plane and related data on a single partition.

The right **mount options** can significantly improve performance. The `noatime` option reduces unnecessary write operations by not updating file access times, while `discard` enables **TRIM** (a command that helps SSDs manage free storage space) for SSDs, and `autodefrag` optimizes file arrangement for large files. These options can be configured in `/etc/fstab`. For optimal SSD performance, regular SSD health checks should be performed and current drivers and kernel updates should be used.

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
   UUID=<btrfs-uuid> /mnt/xplane btrfs defaults,discard 0 2
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

9. **Optimize for X-Plane**
   Extend mount options in `/etc/fstab`:
   ```
   UUID=<btrfs-uuid> /mnt/xplane btrfs defaults,discard,noatime,autodefrag 0 2
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

The **RAID-0** setup with three SSDs achieves nearly triple read and write speeds compared to a single SSD. This results in shorter loading times for scenery, faster texture streaming, and a smoother experience in complex environments.

All three SSDs must be identical, both in capacity and speed. The condition of the SSDs should be regularly checked, for example with the command `sudo smartctl -a /dev/sda`.

## Backup Strategies

Backing up X-Plane data is a critical aspect of system configuration, especially with **RAID-0** setups without redundancy. An effective backup strategy includes regular backups of important configuration files and settings (daily), complete backups of all X-Plane data including scenery and add-ons (weekly), and archiving of weekly backups for long-term storage (monthly).

Suitable backup media include external **SSDs** for fast backups and restores, **NAS/RAID** systems for redundant storage and network access, and **cloud storage** for additional security and access from various locations. The most important backup contents include the X-Plane main program and configuration files, scenery and add-ons, user data and settings, and log files for error analysis.

Tools like `rsync` or `borg` are used for automated backups:

```bash
# Example for daily backup with rsync
rsync -av --delete /mnt/xplane/ /backup/xplane/daily/

# Example for weekly backup with borg
borg create /backup/xplane/weekly::$(date +%Y-%m-%d) /mnt/xplane/
```

Regular recovery tests are performed to verify backup integrity. The recovery process is documented and necessary tools are kept ready.

## Conclusion

The optimal configuration for X-Plane under Linux consists of a single partition on a fast **NVMe SSD** with the **Ext4** filesystem. Enabled **TRIM** and optimized **mount options**, as well as sufficient free storage space, are additional important factors. This configuration minimizes loading times and ensures a smooth flight experience in X-Plane.

For users seeking maximum performance, a **RAID-0** with **Btrfs** on three SSDs offers a powerful alternative. The configuration minimizes loading times and optimizes scenery streaming. Using **Btrfs** with **TRIM**, noatime, and autodefrag maintains SSD performance long-term. A carefully planned backup strategy is essential to prevent data loss and ensure flight operation continuity.

---

## Further Reading

| Topic | Page | Focus |
|---|---|---|
| Kernel Tuning | [Kernel Tuning](../system/systemtuning.md) | NVMe power saving, writeback parameters |
| Monitoring | [Monitoring](../system/systemtools.md) | iotop, iostat, ioping for disk latency analysis |
| Load Dimensions | [Load Dimensions](../../fundamentals/performance/performance_overview.md) | IO as a performance dimension |
| Configuration | [Configuration](../../xplane/setup_diagnose/config.md) | X-Plane file paths and data locations |
| Scenery Components | [Scenery Components](../../scenery/aufbau_quellen/scenery_components.md) | What files X-Plane reads from disk |