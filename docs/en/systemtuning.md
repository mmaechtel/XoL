# System Tuning for X-Plane

!!! danger "Work in Progress"
    The kernel tuning parameters are currently still under review and may not all work as described. Subject to change.

## Distributions and Their Target Profiles

Linux distributions differ not just in package manager and desktop environment, but primarily in the **interplay between kernel and system software**. Each distribution makes configuration decisions for a specific use case:

- **General-purpose distributions** (Debian, Ubuntu, Fedora) — optimize for stability and broad hardware compatibility. The kernel is conservatively configured, power saving has high priority.
- **Gaming/multimedia distributions** (Nobara, Pop!_OS) — ship with pre-tuned kernel parameters, scheduler settings, and driver configurations for low latency.
- **Audio production** (Ubuntu Studio, AV Linux) — use realtime kernels and prioritize audio pipelines.
- **Server distributions** (Debian Server, Rocky Linux) — maximize throughput and stability under sustained load.

The combination of kernel version, scheduler configuration, power management, drivers, and sysctl parameters determines system behavior. Distributions that are already optimized for low latency or gaming include many of the settings described here out of the box.

!!! info "Debian as baseline"
    The following guides are based on **Debian** (Trixie/13) as the starting point — a general-purpose distribution that requires no adjustment for general use but can be specifically optimized for latency-sensitive applications like X-Plane. The standard kernel is replaced with the optimized [Liquorix Kernel](liquorix.md).

    If you're using an already-tuned distribution like Nobara or Ubuntu Studio, you should **not blindly apply these recommendations**. There, a kernel swap can break existing optimizations, and double-tuning often leads to worse results. In that case, it's better to check individual parameters selectively rather than applying the entire profile.

## Performance and Latency — An Important Distinction

When people talk about "performance," they usually mean high FPS. That's correct for shooters or racing games — throughput matters there: as many frames per second as possible. A flight simulator like X-Plane is different.

X-Plane calculates a complex world with physics, weather, scenery, and input devices. Individual frames are expensive, and the target framerate is typically 30–40 FPS. What matters is not the average, but **consistency** — frame-time regularity. A system delivering a stable 35 FPS feels better than one fluctuating between 25 and 50.

The cause of inconsistency is usually not insufficient computing power, but **latency** — short delays from system events that interrupt the main thread.

Typical symptoms of poor latency:

- Micro-stutters despite stable CPU/GPU load
- Delayed input response (joystick, rudder pedals)
- Inconsistent reaction time in the same scene

**Key insight:** For X-Plane, latency optimization matters more than throughput maximization. Temporal predictability beats raw computing power.

## Understanding Latency Sources

System latency doesn't originate from a single source but from four independent categories:

| Category | Impact | Typical Symptom |
|---|---|---|
| **Scheduling** | Delayed thread start | Stutters after load spikes |
| **Power Management** | Wake-up latency from sleep states | Periodic brief interruptions |
| **Interrupts** | Competition for CPU time | Stutters during I/O or input |
| **Memory/IO** | Blocking background operations | Stutters when loading new scenery |

### Scheduling

The Linux scheduler decides when a thread gets CPU time. A conservative scheduler waits longer before reacting — this saves power but increases latency. Modern schedulers (EEVDF) consider cache locality and wake frequency, automatically placing latency-sensitive threads more efficiently.

### Power Management

CPU load doesn't cause stutters — transitions between power states do. When a core wakes from a deep sleep state, delays of up to several hundred microseconds occur. NVMe SSDs in power-saving mode also produce noticeable wake-up latencies (details under [Disable NVMe Power Saving](#4-disable-nvme-power-saving)).

### Interrupts

Hardware interrupts (USB devices, network, storage) preempt the running thread. A single interrupt at the wrong time can violate a frame deadline:

```
periodic main thread + random interrupt = missed deadline
```

### Memory/IO

The kernel optimizes throughput through batched background work (writeback, cache cleanup, paging). This creates rare but noticeable blocks — especially when loading large ortho textures.

## Two Optimization Models

The right tuning strategy depends on the kernel. The standard kernel and Liquorix follow fundamentally different approaches:

**Standard kernel** = open-loop control → response must be forced

The generic Debian kernel prioritizes fairness and throughput. It reacts conservatively to load changes. Tuning here means: explicitly giving the application priority.

**Liquorix** = closed-loop control → disturbances must be removed

Liquorix uses the EEVDF scheduler with shorter preemption windows and higher timer frequency. It responds autonomously to load changes. Tuning here means: minimizing external sources of interference.

!!! warning "Same setting, opposite result"
    Identical parameters can have opposite effects depending on the kernel. A `performance` governor helps with the standard kernel but hurts under Liquorix (thermal headroom is lost). CPU isolation helps with the standard kernel but prevents Liquorix's adaptive optimization.

| Parameter Area | Standard Kernel | Liquorix |
|---|---|---|
| CPU clock | Constant high | Adaptive |
| Scheduler influence | Reinforce | Don't restrict |
| CPU pinning | Possible | Avoid |
| Interrupt routing | Optional | Essential |
| Power saving | Limit | Fine-tune |
| Writeback | Neutral | Smooth |

### Which kernel am I using?

```bash
uname -r
```

- Contains `liquorix` → Profile B (Liquorix)
- Otherwise → Profile A (Standard kernel)

For installing Liquorix, see [Liquorix Kernel](liquorix.md).

## Profile A: Debian Standard Kernel

**Goal:** Scheduler reacts conservatively → actively prioritize the application.

### 1. CPU Governor

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

### 2. Limit CPU Sleep States

In `/etc/default/grub`, extend `GRUB_CMDLINE_LINUX_DEFAULT`:

```
processor.max_cstate=2
```

!!! note "AMD vs. Intel"
    **AMD Zen:** Exports only C1 and C2 to the OS via ACPI. Deeper hardware C-states (C6) are managed autonomously by firmware. The value `2` ensures all available OS-visible C-states are used. Additionally, `amd_pstate=active` can be set (default since kernel 6.5 for Zen 2+).

    **Intel:** Deeper ACPI C-states (C3, C6, C8, C10) are visible and controllable. Here, `processor.max_cstate=3` can be useful to avoid C6+ with 170–680 µs wake-up latency.

Apply:

```bash
sudo update-grub
```

Reboot required.

### 3. Prioritize the Application (Affinity + Priority)

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
    `SCHED_FIFO` priority 45 is below critical kernel migration threads (priority 50) but well above normal processes. Values above 50 can preempt kernel housekeeping and cause instability.

### 4. Optional: CPU Isolation

Only useful under high background load. Add to `/etc/default/grub`:

```
isolcpus=4-11
```

!!! note "Deprecation notice"
    `isolcpus` has been semi-deprecated since kernel 5.4. The modern alternative is **cgroup v2 cpusets**, which can be configured at runtime without rebooting. For a simple desktop use case, `isolcpus` remains the more straightforward option.

### 5. Memory Behavior

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

### 1. Adaptive CPU Governor

Switch immediately:

```bash
echo ondemand | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
```

Verify:

```bash
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
```

!!! note "Why `ondemand` instead of `schedutil`?"
    `schedutil` relies on utilization signals from the CFS scheduler. However, Liquorix uses the BORE scheduler, which doesn't provide these signals — `schedutil` is therefore not compiled in. `ondemand` also adjusts CPU frequency based on load but works independently of the scheduler.

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

### 2. C-States and Power Management

!!! note "AMD vs. Intel"
    **AMD Zen:** Only C1/C2 are OS-visible — no C-state limitation needed. Deeper hardware C-states benefit the thermal budget.

    **Intel:** `processor.max_cstate=5` allows moderate sleep states while avoiding the deepest states (C8/C10 with 280–680 µs latency).

In `/etc/default/grub` — for Intel:

```
processor.max_cstate=5
```

### 3. Interrupt Shielding

The most important measure under Liquorix. Concentrate hardware interrupts on the first cores so the scheduler can use the remaining cores undisturbed for the application.

!!! warning "IRQ affinity under Liquorix"
    Liquorix manages IRQ distribution internally within the kernel. On AMD systems, `/proc/irq/*/smp_affinity_list` and `/proc/irq/*/smp_affinity` are read-only even as root — manual affinity changes at runtime are not possible.

    The solution is the kernel parameter `noirqbalance`, which disables the kernel's internal IRQ distribution and hands control to userspace.

In `/etc/default/grub`, extend `GRUB_CMDLINE_LINUX_DEFAULT`:

```
noirqbalance
```

```bash
sudo update-grub
```

Reboot required. Then use `irqbalance` with targeted configuration. In `/etc/default/irqbalance`, add:

```
IRQBALANCE_BANNED_CPULIST="4-15"
```

This excludes the specified cores from interrupt distribution. CPU 0–3 = system/interrupts, rest = application.

```bash
sudo systemctl enable --now irqbalance
```

!!! tip "Why irqbalance instead of manual affinity?"
    `irqbalance` with `BANNED_CPULIST` is more maintainable than manual affinity: it automatically adapts to new hardware IRQs and distributes load intelligently across the allowed cores.

### 4. Disable NVMe Power Saving

NVMe SSDs can have wake-up latencies of 5–22 ms in power-saving mode — longer than a complete frame at 60 Hz (e.g., Samsung 950 Pro State 4: 22 ms exit latency).

Disable immediately:

```bash
echo 0 | sudo tee /sys/module/nvme_core/parameters/default_ps_max_latency_us
```

To make the setting persistent across reboots, extend `GRUB_CMDLINE_LINUX_DEFAULT` in `/etc/default/grub`:

```
nvme_core.default_ps_max_latency_us=0
```

```bash
sudo update-grub
```

### 5. Smooth Memory Writeback

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

### 6. Light Prioritization

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

### List Installed Kernels

```bash
dpkg --list | grep linux-image
```

### Identify GRUB Menu Entries

GRUB numbers entries starting from 0. Kernels in the "Advanced options" submenu are addressed with `>`:

```bash
grep -E "menuentry |submenu " /boot/grub/grub.cfg | head -20
```

The format for submenu entries is `"Parent>Entry"`, e.g.:

```
"Advanced options for Debian GNU/Linux>Debian GNU/Linux, with Linux 6.12.6-1-liquorix-amd64"
```

### One-Time Switch

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

### Check Current Kernel

```bash
uname -r
```

### What Can Be Switched at Runtime?

Not all settings require a reboot. The following table shows which parameters can be changed while the system is running:

| Parameter | Changeable at runtime? | Method |
|---|---|---|
| Governor | Yes | `echo ... \| sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor` |
| NVMe APST | Yes | `echo 0 \| sudo tee /sys/module/nvme_core/parameters/default_ps_max_latency_us` |
| sysctl (vm.*) | Yes | `sudo sysctl --system` |
| irqbalance service | Yes | `sudo systemctl stop/start irqbalance` |
| nice / chrt / taskset | Yes | Set when launching the application |
| IRQ affinity | **No** (Liquorix/AMD) | Kernel locks `/proc/irq/*/smp_affinity` — `noirqbalance` via GRUB required |
| processor.max_cstate | **No** | GRUB only, reboot required |
| isolcpus | **No** | GRUB only (alternative: cgroup v2 cpusets) |

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
