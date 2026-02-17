---
description: "Linux monitoring tools for X-Plane: htop, btop, turbostat, mpstat, ioping, and more — verify CPU governor, interrupt shielding, and NVMe latency."
---
# Linux System Tools

The settings from [System Tuning](systemtuning.md) shouldn't be applied blindly — they need to be verified. Is the governor actually working? Are interrupts landing on the right cores? Is the [NVMe](../../glossary.md#nvme-non-volatile-memory-express) waking from sleep mode?

This page describes monitoring tools that check exactly that. Each tool is presented with its main purpose and key commands. Cross-references to System Tuning show which setting is verified by which tool.

## Installation

All recommended tools in one command:

```bash
sudo apt install htop btop sysstat linux-cpupower s-tui powertop iotop-c ioping nvme-cli glances util-linux-extra nmon
```

The `sysstat` package contains `mpstat` and `iostat`. The `linux-cpupower` package contains `cpupower` and `turbostat`. The `util-linux-extra` package contains `lsirq`.

---

## CPU Monitoring

### htop — Processes and CPU Utilization

Interactive process viewer with colored per-core bars in the header. Shows at a glance which cores are under load and which processes are consuming CPU.

```bash
htop
```

**Key hotkeys**

| Key | Function |
|-----|----------|
| `H` | Toggle user threads (X-Plane uses many threads) |
| `t` | Tree view (shows thread hierarchy) |
| `P` | Sort by CPU usage |
| `F4` | Filter (e.g., for "X-Plane") |

The **PROCESSOR** column shows which CPU core a process last ran on — useful for checking whether the interrupt separation from [System Tuning](systemtuning.md#interrupt-shielding) is working.

**Limitation:** Shows no CPU frequency, no [C-states](../../glossary.md#c-states-cpu-idle-states), and no per-core interrupt breakdown.

### btop — System Dashboard

Modern system monitor with time-series graphs for CPU, RAM, disk I/O, and network in one window. Good for spotting correlations — e.g., CPU spikes during scenery loading.

```bash
btop
```

Supports mouse interaction, process filtering (`f`), tree view (`e`), and layout presets (`p`).

**Limitation:** CPU frequency only as an aggregate value, no per-core frequency. No [IRQ](../../glossary.md#irq-interrupt-request) statistics.

### cpupower — Check and Set Governor

Shows the active [CPU frequency governor](../../glossary.md#cpu-governor) and can change it. Essential for checking whether the governor configured in [System Tuning](systemtuning.md#cpu-clock-and-sleep-states) is actually active.

```bash
# Show active policy (governor and frequency range) of all cores
cpupower -c all frequency-info -p

# Available governors
cpupower frequency-info -g

# Active cpufreq driver
cpupower frequency-info -d

# Set governor (e.g., performance for Profile A)
sudo cpupower frequency-set -g performance
```

### s-tui — Governor Verification and Thermal Throttling

Terminal tool with four real-time graphs: CPU frequency, utilization, temperature, and power consumption. Makes the effect of a governor switch immediately visible.

```bash
sudo s-tui
```

**Governor verification:** With the `performance` governor, all cores stay at maximum frequency. With `ondemand`, frequency ramps up under load and drops when idle. If frequency drops while temperature is high, that's thermal throttling.

Optional stress test: `sudo apt install stress-ng`, then activate stress mode in the s-tui menu.

Verifies: [Profile A Governor](systemtuning.md#cpu-clock-and-sleep-states) and [Profile B Governor](systemtuning.md#cpu-clock-and-power-management)

### turbostat — Hardware Frequencies and C-States

Shows **actual hardware frequencies per core** (not just what the governor reports), C-state residency, and power consumption. Requires root.

```bash
# Standard overview
sudo turbostat --interval 2

# Focused: frequency and load per core
sudo turbostat --interval 1 --show Core,CPU,Avg_MHz,Bzy_MHz,Busy%,IRQ,CoreTmp

# Log to file (during a flight)
sudo turbostat --interval 2 --out turbostat_session.log
```

**Key columns**

| Column | Meaning |
|--------|---------|
| `Bzy_MHz` | Clock speed during active phases — the real speed |
| `Busy%` | Percentage of time in active state (C0) |
| `CPU%c1`, `CPU%c3`, … | C-state residency — available states depend on hardware |
| `IRQ` | Interrupts per interval and core |

!!! note "AMD Note"
    turbostat works on AMD Zen processors. Available columns depend on the processor's MSR support — some Intel-specific columns (e.g., certain package-level power metrics) may not appear on AMD systems.

Verifies: [C-States](systemtuning.md#cpu-clock-and-sleep-states) and governor effectiveness

### mpstat — Per-Core Statistics and Interrupt Distribution

Most precise per-core breakdown: shows user, system, I/O wait, **IRQ**, and **[SoftIRQ](../../glossary.md#softirq-software-interrupt) percentage** per CPU core. Essential for verifying interrupt shielding.

```bash
# All cores, 1-second interval
mpstat -P ALL 1

# Individual interrupts per CPU per second
mpstat -I CPU 1

# Everything: CPU + interrupts + NUMA
mpstat -A 1
```

**Checking interrupt shielding:** The application cores (e.g., CPU 4–15) should show close to 0% in the `%irq` and `%soft` columns. If values rise there, interrupts are reaching the protected cores.

Verifies: [Interrupt Shielding](systemtuning.md#interrupt-shielding) (Profile B)

---

## IO Monitoring

### iotop — Which Process Is Causing IO?

Shows disk read/write rates per process in real time. Identifies whether stutters come from X-Plane itself, a compositor, journald, or another background process.

```bash
# Only active IO processes, half-second refresh
sudo iotop -oPd 0.5

# Accumulated: who read the most data total
sudo iotop -oPa
```

### iostat — Device-Level Latency

Shows throughput, IOPS, queue depth, and **average request [latency](../../glossary.md#latency)** per device. The key value is `r_await` — the average read latency in milliseconds.

```bash
# Extended stats for NVMe, 1-second interval
iostat -xdth -p nvme0n1 1
```

**Key fields**

| Field | Meaning |
|-------|---------|
| `r_await` | Average read latency (ms) — spikes indicate problems |
| `%util` | Device utilization — at 100% the device is saturated |
| `aqu-sz` | Queue length — high values mean requests are waiting |

**NVMe [APST](../../glossary.md#apst-autonomous-power-state-transitions) signature:** A sudden jump in `r_await` from <1 ms to 50–500 ms after an idle period indicates NVMe wake-up latency.

### ioping — Measure Disk Latency

Measures individual IO request latencies, similar to `ping` for network. The most direct tool for detecting NVMe wake-up latencies.

```bash
# Direct IO latency (bypass cache, true device latency)
sudo ioping -c 20 -D /dev/nvme0n1

# Simulate ortho texture reads: 256K sequential
sudo ioping -c 50 -s 256k -D -L /dev/nvme0n1
```

**NVMe APST wake-up test:**

```bash
# 5x idle + measure — first request after idle shows wake-up latency
for i in $(seq 1 5); do
    sleep 5
    sudo ioping -c 1 -D /dev/nvme0n1
done
```

If the first request shows 10–500 ms while subsequent requests show <0.1 ms, APST wake-up is the cause.

Verifies: [NVMe Power Saving](systemtuning.md#disable-nvme-power-saving) (Profile B)

### nvme-cli — Query NVMe Power States

Shows the NVMe drive's power states with their entry/exit latencies. Complements ioping by revealing the cause: which power state is causing the delay.

```bash
# Show power states with latencies
sudo nvme id-ctrl /dev/nvme0 | grep -A 5 "ps "

# Check APST configuration
sudo nvme get-feature /dev/nvme0 -f 0x0c -H

# Check current power state
sudo nvme get-feature /dev/nvme0 -f 0x02 -H
```

---

## Interrupt Analysis

### /proc/interrupts — Reading Interrupt Counters

The kernel interface for interrupt statistics. Shows per IRQ the number of interrupts on each CPU core since boot.

```bash
# Show all interrupts
cat /proc/interrupts

# Watch NVMe interrupts (real-time)
watch -n 1 'grep nvme /proc/interrupts'
```

**Key columns**

| Column | Meaning |
|--------|---------|
| IRQ number | Interrupt identifier |
| CPU0..CPUn | Counter per core (since boot) |
| Handler type | `IR-IO-APIC`, `PCI-MSI`, etc. |
| Device name | Associated hardware |

Special entries: **LOC** = Local Timer Interrupts (per CPU), **RES** = Rescheduling Interrupts (IPI), **NMI** = Non-Maskable Interrupts.

### lsirq — Sorted Interrupt Snapshot

`lsirq` provides a sorted snapshot of interrupt counters. Part of `util-linux-extra`.

```bash
# Sorted by total count (most active IRQs on top)
lsirq -s TOTAL

# Show only counters for specific CPUs
lsirq -C 0-3

# Softirqs instead of hardware interrupts
lsirq -S
```

For real-time monitoring, use `watch -n 1 lsirq -s TOTAL` or the `/proc/interrupts` methods described above.

### Verifying Interrupt Shielding

After configuring [Interrupt Shielding](systemtuning.md#interrupt-shielding) (Profile B), you need to verify that the application cores are actually free from interrupts.

**Step 1 — Check IRQ percentage per core:**

```bash
# CPU 4-15 should show ~0% in %irq and %soft
mpstat -P ALL 1 5
```

**Step 2 — Watch interrupt counters:**

```bash
# Counters on protected cores should not increase
watch -n 1 'grep -E "^[[:space:]]*[0-9]" /proc/interrupts'
```

**Step 3 — Check IRQ affinity directly:**

```bash
# List all IRQ affinities
for d in /proc/irq/[0-9]*/; do
    irq=$(basename "$d")
    cpus=$(cat "$d/smp_affinity_list" 2>/dev/null)
    name=$(awk -v irq="$irq:" '$1==irq {print $NF}' /proc/interrupts 2>/dev/null)
    printf "IRQ %4s -> CPU %-10s  %s\n" "$irq" "$cpus" "$name"
done
```

---

## System Dashboards

### glances — Everything at a Glance

Comprehensive system dashboard with CPU, RAM, disk I/O (including latency), network, sensors, and process list in one window.

```bash
# Terminal dashboard
glances

# Web UI mode (access at http://localhost:61208)
glances -w
```

The **web UI mode** is ideal for X-Plane in fullscreen: monitoring runs on a second device (tablet, laptop) in the browser. Press `L` (uppercase) to activate the disk IO latency view — directly relevant for detecting NVMe wake-up latencies.

### powertop — C-States and Power Behavior

Diagnostic tool for power consumption and power management. The most important tab is **Idle Stats** — shows C-state residency per core. Requires root.

```bash
sudo powertop
```

**Relevant tabs**

| Tab | Shows |
|-----|-------|
| **Idle Stats** | C-state residency per core — deep C-states cause wake-up latency |
| **Frequency Stats** | P-state/Turbo usage — is the CPU running at expected frequency? |
| **Device Stats** | Which devices are causing wakeups |

```bash
# Generate HTML report (for documentation)
sudo powertop --html=powertop_report.html
```

!!! warning "Avoid auto-tune"
    `powertop --auto-tune` enables aggressive power-saving settings — the **opposite** of the recommendations in [System Tuning](systemtuning.md). Do not use for latency-sensitive applications.

Verifies: [C-States](systemtuning.md#cpu-clock-and-sleep-states) and [C-States Liquorix](systemtuning.md#cpu-clock-and-power-management)

---

## Scenario Table

| What do I want to check? | Tool | Command |
|--------------------------|------|---------|
| Which core is under load? | htop | `htop` (header bars) |
| CPU + RAM + disk at a glance | btop | `btop` |
| Which governor is active? | cpupower | `cpupower -c all frequency-info -p` |
| Verify governor switch visually | s-tui | `sudo s-tui` |
| Real hardware frequency per core | turbostat | `sudo turbostat --show Core,CPU,Bzy_MHz,Busy%` |
| Check C-state residency | powertop | `sudo powertop` (Tab: Idle Stats) |
| Verify interrupt shielding | mpstat | `mpstat -I CPU -P ALL 1` |
| Identify interrupt sources | lsirq | `watch -n 1 lsirq -s TOTAL` |
| Which process is causing IO? | iotop | `sudo iotop -oPd 0.5` |
| Measure NVMe latency | ioping | `sudo ioping -c 20 -D /dev/nvme0n1` |
| Test NVMe APST wake-up | ioping | `sleep 5 && sudo ioping -c 1 -D /dev/nvme0n1` |
| Show NVMe power states | nvme-cli | `sudo nvme get-feature /dev/nvme0 -f 0x02 -H` |
| Monitor everything (web UI) | glances | `glances -w` |
| Record session | nmon | `nmon -f -s 5 -c 720` |

---

??? abstract "Advanced: nmon — Batch Recording"

    nmon records system metrics in the background to CSV files. Ideal for recording a complete flight session and analyzing afterward.

    ```bash
    sudo apt install nmon

    # Record 1 hour (5-second interval, 720 snapshots)
    nmon -f -s 5 -c 720

    # Record 2 hours (10-second interval)
    nmon -f -s 10 -c 720
    ```

    The recording runs in the background. The file is automatically named (`hostname_YYYYMMDD_HHMM.nmon`). Use `nmonchart` for visualization, which converts the CSV data into interactive HTML charts.

??? abstract "Advanced: fatrace — Observing File Access"

    fatrace shows real-time file access events from all processes with full paths. Answers: "Which files does X-Plane read during a scenery transition?"

    ```bash
    sudo apt install fatrace

    # Which files is X-Plane reading right now?
    sudo fatrace -t -f R -C X-Plane -o /tmp/xplane_reads.log

    # Background processes writing to disk during flight
    sudo fatrace -t -f W -s 120 -o /tmp/writes_during_flight.log
    ```

    Always redirect output to a file (`-o`), as terminal output itself causes disk IO.

??? abstract "Advanced: perf and trace-cmd — Kernel-Level Analysis"

    For deep scheduling and interrupt latency analysis. These tools require root and an understanding of Linux kernel internals.

    ```bash
    sudo apt install linux-perf trace-cmd
    ```

    **perf sched** — Detect scheduling latency:

    ```bash
    # Record scheduling events
    sudo perf sched record -- sleep 10
    sudo perf sched latency
    ```

    Shows per-task average and maximum scheduling delay. High values on application cores indicate that interrupts or other tasks are preempting the render thread.

    **trace-cmd** — Measure IRQ-off latency:

    ```bash
    sudo trace-cmd record -p irqsoff sleep 10
    sudo trace-cmd report
    ```

    Measures the longest period during which interrupts were disabled — an indicator of kernel-side delays.

---

## Further Reading

| Topic | Page | Focus |
|---|---|---|
| Kernel Tuning | [Kernel Tuning](systemtuning.md) | The settings these tools verify |
| Why Latency Matters | [Why Latency Matters](latency.md) | Motivation for monitoring system latency |
| Latency and Predictability | [Latency and Predictability](../../fundamentals/performance/latency.md) | Theoretical foundations of system latency |
| Liquorix Kernel | [Liquorix Kernel](../optimizations/liquorix.md) | Low-latency kernel requiring different monitoring approach |
| Performance Analysis | [Performance Analysis](../../xplane/setup_diagnose/performance.md) | X-Plane-specific performance tools |
| Nvidia Drivers | [Nvidia Drivers](../optimizations/nvidia.md) | MangoHud and GPU monitoring |

---

## Sources

- [htop-dev/htop](https://github.com/htop-dev/htop) — Interactive process viewer
- [aristocratos/btop](https://github.com/aristocratos/btop) — System monitor
- [sysstat/sysstat](https://github.com/sysstat/sysstat) — mpstat, iostat, pidstat
- [amanusk/s-tui](https://github.com/amanusk/s-tui) — CPU monitoring and stress test
- [nicolargo/glances](https://github.com/nicolargo/glances) — System dashboard with web UI
- [fenrus75/powertop](https://github.com/fenrus75/powertop) — Power management diagnostics
- [koct9i/ioping](https://github.com/koct9i/ioping) — Disk IO latency measurement
- [linux-nvme/nvme-cli](https://github.com/linux-nvme/nvme-cli) — NVMe management
