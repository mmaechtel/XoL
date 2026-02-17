# System Tuning for X-Plane

!!! warning "Work in Progress"
    The kernel tuning parameters are currently still under review and may not all work as described. Subject to change.

## Distributions and Their Target Profiles

Linux distributions differ not just in package manager and desktop environment, but primarily in the **interplay between kernel and system software**. Each distribution makes configuration decisions for a specific use case:

- **General-purpose distributions** (Debian, Ubuntu, Fedora) — optimize for stability and broad hardware compatibility. The kernel is conservatively configured, power saving has high priority.
- **Gaming/multimedia distributions** (Nobara, Pop!_OS) — ship with pre-tuned kernel parameters, scheduler settings, and driver configurations for low latency.
- **Audio production** (Ubuntu Studio, AV Linux) — use realtime kernels and prioritize audio pipelines.
- **Server distributions** (Debian Server, Rocky Linux) — maximize throughput and stability under sustained load.

The combination of kernel version, scheduler configuration, power management, drivers, and sysctl parameters determines system behavior. Distributions that are already optimized for low latency or gaming include many of the settings described here out of the box.

!!! info "Debian as baseline"
    The following guides are based on **Debian** (Trixie/13) as the starting point — a general-purpose distribution that requires no adjustment for general use but can be specifically optimized for latency-sensitive applications like X-Plane. The standard kernel is replaced with the optimized [Liquorix Kernel](../optimizations/liquorix.md).

    If you're using an already-tuned distribution like Nobara or Ubuntu Studio, you should **not blindly apply these recommendations**. There, a kernel swap can break existing optimizations, and double-tuning often leads to worse results. In that case, it's better to check individual parameters selectively rather than applying the entire profile.

Why latency matters more than throughput for X-Plane, and which system sources generate latency, is covered in the [Latency and Predictability](../../fundamentals/performance/latency.md) chapter.

## Two Optimization Models

The right tuning strategy depends on the kernel. The standard kernel and Liquorix follow fundamentally different approaches:

**Standard kernel** = open-loop control → response must be forced

The generic Debian kernel prioritizes fairness and throughput. It reacts conservatively to load changes. Tuning here means: explicitly giving the application priority.

**Liquorix** = closed-loop control → disturbances must be removed

Liquorix uses the [PDS](../../glossary.md#pds-priority-and-deadline-based-skiplist) (Priority and Deadline based Skiplist) scheduler with shorter preemption windows and a 1000 Hz timer frequency. It responds autonomously to load changes. Tuning here means: minimizing external sources of interference.

!!! warning "Same setting, opposite result"
    Identical parameters can have opposite effects depending on the kernel. A `performance` governor helps with the standard kernel but can be counterproductive under Liquorix (thermal headroom is lost). CPU isolation helps with the standard kernel but prevents Liquorix's adaptive optimization.

| Parameter Area | Standard Kernel | Liquorix |
|---|---|---|
| CPU clock | Constant high | Adaptive |
| Scheduler influence | Reinforce | Don't restrict |
| CPU pinning | Possible | Avoid |
| Interrupt routing | Optional | Essential |
| Power saving | Limit | Fine-tune |
| Writeback | Neutral | Smooth |

**Which kernel am I using?**

```bash
uname -r
```

- Contains `liquorix` → Profile B (Liquorix)
- Otherwise → Profile A (Standard kernel)

For installing Liquorix, see [Liquorix Kernel](../optimizations/liquorix.md).

## Profile A: Debian Standard Kernel

**Goal:** Scheduler reacts conservatively → actively prioritize the application.

### CPU Clock and Sleep States

**Governor**

Set the governor to a fixed high-performance clock to reduce reaction time and compensate for the lack of load prediction.

Switch immediately:

```bash
echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
```

Verify:

```bash
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
```

To make the setting persistent across reboots, extend `GRUB_CMDLINE_LINUX_DEFAULT` in `/etc/default/grub`:

```
cpufreq.default_governor=performance
```

```bash
sudo update-grub
```

**Limit CPU Sleep States**

In `/etc/default/grub`, extend `GRUB_CMDLINE_LINUX_DEFAULT`:

```
processor.max_cstate=2
```

!!! note "AMD vs. Intel"
    **AMD Zen:** Exports only C1 and C2 to the OS via ACPI. Deeper hardware [C-states](../../glossary.md#c-states-cpu-idle-states) (C6) are managed autonomously by firmware. The value `2` ensures all available OS-visible C-states are used. Additionally, `amd_pstate=active` can be set for modern Zen processors with CPPC support.

    **Intel:** Deeper ACPI C-states (C3, C6, C8, C10) are visible and controllable. Here, `processor.max_cstate=3` can be useful to limit deep states. On systems using the `intel_idle` driver (default on modern Intel), `intel_idle.max_cstate` may also be needed.

Apply:

```bash
sudo update-grub
```

Reboot required.

### Prioritize the Application (Affinity + Priority)

A launcher script that pins X-Plane to specific cores and starts it with elevated scheduling priority:

```bash title="~/run_xplane.sh"
#!/bin/bash
exec taskset -c 4-11 chrt -f 45 "$@"
```

```bash
chmod +x ~/run_xplane.sh
```

Launch:

```bash
~/run_xplane.sh /path/to/X-Plane-x86_64
```

!!! note "About the priority"
    `SCHED_FIFO` priority 45 is below critical kernel threads such as IRQ handlers (priority 50) but well above normal processes. Values above 50 can preempt kernel housekeeping and cause instability.

**Optional: CPU Isolation**

Only useful under high background load. Add to `/etc/default/grub`:

```
isolcpus=4-11
```

!!! note "Deprecation notice"
    `isolcpus` is marked as deprecated in the kernel documentation. The modern alternative is **cpusets**, which can be configured at runtime without rebooting. For a simple desktop use case, `isolcpus` remains the more straightforward option.

**Memory Behavior**

```ini title="/etc/sysctl.d/60-desktop.conf"
vm.swappiness=20
vm.dirty_ratio=20
vm.dirty_background_ratio=10
vm.vfs_cache_pressure=100
```

Apply:

```bash
sudo sysctl --system
```

### Result Profile A

The kernel reacts faster because CPU time is guaranteed for the application.

---

## Profile B: Liquorix Kernel

**Goal:** Scheduler already works optimally → remove external disturbances.

**Important:** No `isolcpus`, no `taskset` — these would prevent the scheduler's adaptive optimization.

### CPU Clock and Power Management

**Governor**

Switch immediately:

```bash
echo ondemand | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
```

Verify:

```bash
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
```

!!! note "Why `ondemand` instead of `schedutil`?"
    `schedutil` relies on utilization signals from the mainline CFS/[EEVDF](../../glossary.md#eevdf-earliest-eligible-virtual-deadline-first) scheduler. However, Liquorix uses the PDS alternative scheduler, which does not provide these signals — `schedutil` is therefore not compiled in. `ondemand` also adjusts CPU frequency based on load but works independently of the scheduler.

Optionally set Energy Performance Preference:

```bash
echo balance_performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/energy_performance_preference
```

To make the setting persistent across reboots, extend `GRUB_CMDLINE_LINUX_DEFAULT` in `/etc/default/grub`:

```
cpufreq.default_governor=ondemand
```

```bash
sudo update-grub
```

!!! tip "Persistence"
    The terminal commands apply until the next reboot. The GRUB method makes the setting permanent. For permanent EPP settings, create a systemd unit or udev rule.

**C-States and Power Management**

!!! note "AMD vs. Intel"
    **AMD Zen:** Only C1/C2 are OS-visible — no C-state limitation needed. Deeper hardware C-states benefit the thermal budget.

    **Intel:** `processor.max_cstate=5` allows moderate sleep states while avoiding the deepest states. On systems using `intel_idle` (default), also set `intel_idle.max_cstate=5`.

In `/etc/default/grub` — for Intel:

```
processor.max_cstate=5
```

### Interrupt Shielding

The most important measure under Liquorix. Concentrate hardware interrupts on the first cores so the scheduler can use the remaining cores undisturbed for the application.

!!! warning "IRQ affinity on modern kernels"
    Modern kernels use managed interrupts for MSI-X devices (NVMe, GPU, etc.). The kernel controls affinity allocation for these IRQs, and writes to `/proc/irq/*/smp_affinity` are rejected by design — regardless of kernel variant. This is not Liquorix-specific but a general kernel mechanism.

    The userspace daemon [`irqbalance`](../../glossary.md#irqbalance) handles redistribution of non-managed IRQs and respects these kernel constraints automatically.

For non-managed IRQs, `irqbalance` provides effective CPU exclusion. In `/etc/default/irqbalance`, add:

```
IRQBALANCE_BANNED_CPULIST="4-15"
```

This excludes the specified cores from interrupt distribution. CPU 0–3 = system/interrupts, rest = application.

```bash
sudo systemctl enable --now irqbalance
```

!!! tip "Why irqbalance instead of manual affinity?"
    `irqbalance` with `BANNED_CPULIST` is more maintainable than manual affinity: it automatically adapts to new hardware IRQs and distributes load intelligently across the allowed cores.

### Disable NVMe Power Saving

NVMe SSDs in power-saving mode can have wake-up latencies in the millisecond range — longer than a complete frame at 60 Hz. Exit latencies vary by manufacturer and power state.

To disable NVMe power saving, extend `GRUB_CMDLINE_LINUX_DEFAULT` in `/etc/default/grub`:

```
nvme_core.default_ps_max_latency_us=0
```

```bash
sudo update-grub
```

Reboot required.

!!! note "Runtime changes"
    The sysfs parameter `/sys/module/nvme_core/parameters/default_ps_max_latency_us` only affects **newly initialized** NVMe devices. For already-active devices, use per-device PM QOS:
    ```bash
    for dev in /sys/class/nvme/nvme*/device/power/pm_qos_latency_tolerance_us; do echo 0 | sudo tee "$dev"; done
    ```
    The GRUB method is the most reliable approach.

**Smooth Memory Writeback**

```ini title="/etc/sysctl.d/99-lowlatency.conf"
vm.swappiness=10
vm.dirty_background_ratio=3
vm.dirty_ratio=10
vm.vfs_cache_pressure=100
```

Apply:

```bash
sudo sysctl --system
```

**Light Prioritization**

Under Liquorix, a moderate `nice` adjustment is sufficient:

```bash title="~/run_xplane.sh"
#!/bin/bash
exec nice -n -10 "$@"
```

### Result Profile B

Not maximum performance — but minimal frame-time spikes. The scheduler can optimize freely because external disturbances are reduced.

---

## Switching Between Kernels

If you have both kernels installed in parallel (standard Debian + Liquorix), you can choose which one to boot. This lets you use the matching tuning profile depending on your use case — without uninstalling either kernel.

**List Installed Kernels**

```bash
dpkg --list | grep linux-image
```

**Identify GRUB Menu Entries**

GRUB numbers entries starting from 0. Kernels in the "Advanced options" submenu are addressed with `>`:

```bash
grep -E "menuentry |submenu " /boot/grub/grub.cfg | head -20
```

The format for submenu entries is `"Parent>Entry"`, e.g.:

```
"Advanced options for Debian GNU/Linux>Debian GNU/Linux, with Linux 6.12.6-1-liquorix-amd64"
```

**One-Time Switch**

!!! note "Prerequisite"
    `grub-reboot` requires `GRUB_DEFAULT=saved` in `/etc/default/grub` (see [Permanent Switch](#permanent-switch) below). Without it, GRUB ignores the saved entry.

Boot a specific kernel on the next reboot, then return to the default:

```bash
sudo grub-reboot "Advanced options for Debian GNU/Linux>Debian GNU/Linux, with Linux 6.12.6-1-liquorix-amd64"
sudo reboot
```

### Permanent Switch

Change the default boot entry permanently:

1. In `/etc/default/grub`, set:

    ```
    GRUB_DEFAULT=saved
    ```

2. Set the desired kernel as default:

    ```bash
    sudo grub-set-default "Advanced options for Debian GNU/Linux>Debian GNU/Linux, with Linux 6.12.6-1-liquorix-amd64"
    sudo update-grub
    ```

After this setup, `grub-reboot` also works for one-time deviations from the saved default.

**Check Current Kernel**

```bash
uname -r
```

### What Can Be Switched at Runtime?

Not all settings require a reboot. The following table shows which parameters can be changed while the system is running:

| Parameter | Changeable at runtime? | Method |
|---|---|---|
| Governor | Yes | `echo ... \| sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor` |
| NVMe APST | **No** | GRUB only — sysfs parameter only affects newly initialized devices |
| sysctl (vm.*) | Yes | `sudo sysctl --system` |
| irqbalance service | Yes | `sudo systemctl stop/start irqbalance` |
| nice / chrt / taskset | Yes | Set when launching the application |
| IRQ affinity | **No** (managed IRQs) | Kernel manages MSI-X affinity — use `irqbalance` with `BANNED_CPULIST` for non-managed IRQs |
| processor.max_cstate | **No** | GRUB only, reboot required |
| isolcpus | **No** | GRUB only (alternative: cpusets) |

!!! warning "Match your tuning profile"
    After switching kernels, use the matching profile: [Profile A](#profile-a-debian-standard-kernel) for the standard kernel, [Profile B](#profile-b-liquorix-kernel) for Liquorix. The governor and sysctl settings differ fundamentally — the wrong combination will degrade performance.

---

## Overall Comparison

| Area | Standard Kernel | Liquorix |
|---|---|---|
| Governor | `performance` | `ondemand` |
| CPU pinning | Yes (`taskset`) | No |
| Interrupt separation | Optional | Important |
| NVMe APST | Optionally disabled | Disabled |
| Writeback | Normal | Smoothed |
| Prioritization | `SCHED_FIFO` + affinity | `nice -n -10` |
| **Goal** | **Force responsiveness** | **Prevent disturbances** |

!!! info "Core rule"
    **Standard kernel needs prioritization — Liquorix needs quiet.**

    Configuring both kernels the same way almost always makes things worse.

---

## Sources

The most important sources for the topics covered on this page:

- [CPU Performance Scaling — Linux Kernel Documentation](https://docs.kernel.org/admin-guide/pm/cpufreq.html) — CPU frequency governors and scaling drivers
- [CPU Idle Time Management — Linux Kernel Documentation](https://docs.kernel.org/admin-guide/pm/cpuidle.html) — C-states and idle drivers (acpi_idle, intel_idle)
- [amd-pstate CPU Performance Scaling Driver — Linux Kernel Documentation](https://docs.kernel.org/admin-guide/pm/amd-pstate.html) — AMD P-State driver modes
- [Liquorix Kernel](https://liquorix.net/) — PDS scheduler, Zen Interactive Tuning, kernel features
- [irqbalance(1) — Debian Man Page](https://manpages.debian.org/testing/irqbalance/irqbalance.1.en.html) — IRQ distribution daemon configuration
- [Solid State Drive/NVMe — Arch Wiki](https://wiki.archlinux.org/title/Solid_state_drive/NVMe) — NVMe power management (APST)
- [sysctl.d(5) — Linux Man Page](https://man7.org/linux/man-pages/man5/sysctl.d.5.html) — sysctl drop-in configuration
- [GNU GRUB Manual](https://www.gnu.org/software/grub/manual/grub/html_node/Simple-configuration.html) — GRUB configuration and kernel selection
