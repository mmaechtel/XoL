# Liquorix Kernel on Debian

The standard Debian kernel is configured for broad compatibility and server workloads. The [Liquorix Kernel](../glossary.md#liquorix-kernel) takes a different approach — it is based on the Zen kernel patchset and tuned specifically for desktop responsiveness and low-latency workloads like gaming and flight simulation. It is maintained by Steven Barrett and not part of the official Debian archive. Before installation, creating a system backup is recommended.

## Installation

### Prerequisites

- Debian installed and updated
- Root or sudo rights

### Quick Install (Recommended)

The official installer script handles key import, repository setup, and installation automatically:

```bash
curl -s 'https://liquorix.net/install-liquorix.sh' | sudo bash
```

### Manual Installation

1. **Update system**

    ```bash
    sudo apt update && sudo apt upgrade -y
    ```

2. **Add repository**

    - **Install dependencies**

        ```bash
        sudo apt install -y curl gpg ca-certificates
        ```

    - **Add repository key**

        ```bash
        sudo mkdir -p /etc/apt/keyrings
        curl -s 'https://liquorix.net/liquorix-keyring.gpg' | sudo gpg --batch --yes --dearmor -o /etc/apt/keyrings/liquorix-keyring.gpg
        ```

    - **Set up repository**

        ```bash
        CODENAME="$(. /etc/os-release && echo "$VERSION_CODENAME")"
        echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/liquorix-keyring.gpg] https://liquorix.net/debian $CODENAME main" | sudo tee /etc/apt/sources.list.d/liquorix.list
        ```

    - **Update package sources**

        ```bash
        sudo apt update
        ```

3. **Install kernel**

    ```bash
    sudo apt install linux-image-liquorix-amd64 linux-headers-liquorix-amd64
    ```

4. **Reboot system**

    ```bash
    sudo reboot
    ```

5. **Verify installation**

    After reboot, check the active kernel version:

    ```bash
    uname -r
    ```

    The output should show a Liquorix kernel version (e.g., `6.18.10-1-liquorix-amd64`).

## Why Liquorix?

The advantages of the Liquorix kernel come from a fundamentally different configuration compared to the standard Debian kernel:

| Setting | Debian Stock | Liquorix |
|---------|-------------|----------|
| **Scheduler** | EEVDF (mainline) | PDS (Priority and Deadline based Skiplist) |
| **Timer Frequency** | 250 Hz | 1000 Hz |
| **Preemption** | Lazy / Dynamic | Full Preempt |
| **Default Governor** | `schedutil` | `performance` |
| **Tick Model** | Idle (NO_HZ_IDLE) | Full adaptive (NO_HZ_FULL) |

The **PDS scheduler** (by Alfred Chen, part of the Project C patchset) replaces the mainline EEVDF scheduler entirely. It uses a skiplist data structure to manage task priorities and deadlines, enabling fast scheduling decisions with low overhead. Combined with the 1000 Hz timer and full kernel preemption, Liquorix can react to load changes within 1 ms — four times faster than the stock kernel at 250 Hz.

### Optimization Model

The key difference lies in what each kernel type needs for best results:

- A **stock kernel** benefits from explicit tuning — CPU affinity, `SCHED_FIFO`, or `nice` values — because its conservative defaults prioritize throughput over latency.
- **Liquorix** benefits from a **quiet system** — minimizing external disturbances like interrupt storms, NVMe power-saving transitions, and uneven writeback pressure allows PDS to optimize task placement autonomously.

Manual CPU pinning or aggressive priority escalation can be counterproductive under Liquorix: they override exactly the adaptive decisions that PDS is designed to make.

Concrete configuration steps for both kernel types can be found on the [System Tuning](../system/systemtuning.md) page.

!!! warning "Security consideration"
    Liquorix tracks the latest upstream kernel series, which means it includes upstream security fixes present in those releases. However, it is **not covered by Debian Security Advisories** — DSAs apply only to packages in the official Debian archive. Security updates depend on a single maintainer's release cycle, which may lag behind Debian's security team. Switching back to the stock kernel is always possible via the GRUB boot menu.

---

## Maintenance

### Updates

The kernel is updated like other system packages:

```bash
sudo apt update && sudo apt upgrade
```

### Removal

If switching back to the standard kernel is necessary:

1. **Install standard kernel**

    ```bash
    sudo apt install linux-image-amd64 linux-headers-amd64
    ```

2. **Remove Liquorix kernel**

    ```bash
    sudo apt remove linux-image-liquorix-amd64 linux-headers-liquorix-amd64
    ```

3. **Reboot system**

    ```bash
    sudo reboot
    ```

## Support

### Troubleshooting

- **Boot issues**: If the new kernel doesn't start, the standard Debian kernel can be selected in the GRUB menu
- **DKMS modules**: For drivers like [Nvidia](nvidia.md), [DKMS](../glossary.md#dkms-dynamic-kernel-module-support) is important

    ```bash
    sudo apt install dkms
    ```

- **Performance issues**

    - Check system logs: `dmesg | grep -i error`
    - Monitor CPU frequency: `cpupower frequency-info`
    - Verify active scheduler: `dmesg | grep sched`

### Resources

- Official website: [liquorix.net](https://liquorix.net)
- Community forum: [Liquorix Forum](https://techpatterns.com/forums/forum-34.html)
- Bug reports: [GitHub Issues](https://github.com/damentz/liquorix-package/issues)

---

## Sources

- [Liquorix Kernel](https://liquorix.net) — Official project page with feature list and installation instructions
- [Project C / PDS Scheduler](https://gitlab.com/alfredchen/projectc) — Alfred Chen's alternative CPU scheduler patchset
- [Liquorix Package Repository](https://github.com/damentz/liquorix-package) — Build configuration and release history
- [Linux Kernel Scheduler Documentation](https://docs.kernel.org/scheduler/index.html) — Official kernel documentation on CPU scheduling
